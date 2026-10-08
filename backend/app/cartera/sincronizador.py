import logging
from datetime import datetime
from pathlib import Path

from app.cartera.database import CarteraDatabase
from app.cartera.models import ClienteCartera, Credito, PagoHistorico, SnapshotMensual
from app.cartera.parser_creemos import CreemosParser

logger = logging.getLogger(__name__)


class SincronizadorCartera:
    def __init__(self, ruta_creemos=None, db_path=None, dry_run=False):
        self.ruta_creemos = ruta_creemos or Path(__file__).resolve().parent.parent.parent.parent / "Creemos.xlsx"
        self.db = CarteraDatabase(db_path=db_path)
        self.dry_run = dry_run
        self.log = []
        self.discrepancias = []

    def _log(self, msg, nivel="info"):
        self.log.append((nivel, msg))
        if nivel == "error":
            logger.error(msg)
        elif nivel == "warning":
            logger.warning(msg)
        else:
            logger.info(msg)

    def _get_or_create_cliente(self, session, nombre, telefono=None):
        if not nombre:
            return None
        cl = session.query(ClienteCartera).filter(
            ClienteCartera.nombre == nombre.upper().strip()
        ).first()
        if not cl:
            if self.dry_run:
                self._log(f"[DRY-RUN] Se crearía cliente: {nombre}")
                return None
            cl = ClienteCartera(nombre=nombre.upper().strip(), telefono=telefono)
            session.add(cl)
            session.flush()
            self._log(f"Cliente creado: {nombre}")
        return cl

    def _get_or_create_credito(self, session, placa, sufijo, data):
        cred = session.query(Credito).filter(
            Credito.placa == placa,
            Credito.sufijo_credito == sufijo
        ).first()
        if not cred:
            if self.dry_run:
                self._log(f"[DRY-RUN] Se crearía crédito: {placa}{sufijo}")
                return None
            cred = Credito(
                placa=placa,
                sufijo_credito=sufijo,
                valor_credito=data.get("valor_credito"),
                valor_cuota=data.get("valor_cuota"),
                fecha_desembolso=data.get("fecha_desembolso"),
                plazo_meses=data.get("plazo_meses"),
                prenda=data.get("prenda"),
                tiene_historial_detallado=data.get("tiene_historial_detallado", True),
                activo=True,
            )
            session.add(cred)
            session.flush()
            self._log(f"Crédito creado: {placa}{sufijo}")
        return cred

    def _sync_pagos_joglo(self, session, creditos, pagos):
        for p in pagos:
            cred = session.query(Credito).filter(
                Credito.placa == p["placa"],
                Credito.sufijo_credito == p["sufijo"]
            ).first()
            if not cred:
                continue

            exists = session.query(PagoHistorico).filter(
                PagoHistorico.credito_id == cred.id,
                PagoHistorico.numero_pago == p["numero_pago"],
                PagoHistorico.recibo == p["recibo"]
            ).first()

            if exists:
                if p["interes"] is not None and exists.interes is not None:
                    diff = abs(float(p["interes"]) - float(exists.interes))
                    if diff > 1:
                        self.discrepancias.append(
                            f"Pago {p['numero_pago']} crédito {p['placa']}{p['sufijo']}: "
                            f"interés difiere (DB={float(exists.interes):.0f}, Excel={float(p['interes']):.0f})"
                        )
                continue

            if self.dry_run:
                self._log(f"[DRY-RUN] Se insertaría pago #{p['numero_pago']} de {p['placa']}{p['sufijo']}")
                continue

            ph = PagoHistorico(
                credito_id=cred.id,
                numero_pago=p["numero_pago"],
                recibo=p["recibo"],
                fecha_ultimo_pago=p["fecha_ultimo_pago"],
                fecha_pago=p["fecha_pago"],
                dias=p["dias"],
                cuota=p["cuota"],
                interes=p["interes"],
                saldo_intereses=p["saldo_intereses"],
                capital=p["capital"],
                saldo_real=p["saldo_real"],
                fuente="excel_creemos",
            )
            session.add(ph)

    def _sync_snapshots(self, session, snapshots, origen):
        for s in snapshots:
            placa = s.get("placa", "").strip().upper()
            cliente_nombre = s.get("cliente", "").upper().strip()
            mes = s.get("mes_reportado", "")

            # Generar placa para snapshots sin placa (ej: JOGLO-COMPRA EUROS)
            if not placa and cliente_nombre:
                placa = cliente_nombre[:15]

            exists = session.query(SnapshotMensual).filter(
                SnapshotMensual.placa_textual == placa,
                SnapshotMensual.mes_reportado == mes,
                SnapshotMensual.origen_archivo == origen
            ).first()

            if exists:
                continue

            # Buscar credito que coincida por placa o por nombre de cliente
            cred = session.query(Credito).filter(
                Credito.placa == placa,
                Credito.sufijo_credito == ""
            ).first()
            if not cred and cliente_nombre:
                cc = session.query(ClienteCartera).filter(
                    ClienteCartera.nombre == cliente_nombre
                ).first()
                if cc:
                    cred = session.query(Credito).filter(
                        Credito.cliente_id == cc.id
                    ).first()

            if self.dry_run:
                self._log(f"[DRY-RUN] Se insertaría snapshot {placa} / {mes} ({origen})")
                continue

            sm = SnapshotMensual(
                credito_id=cred.id if cred else None,
                placa_textual=placa,
                mes_reportado=mes,
                numero_bloque=s.get("numero_bloque"),
                pago_del_mes=bool(s.get("pago_del_mes")),
                fecha_original=s.get("fecha_original"),
                vr_credito=s.get("vr_credito"),
                vr_cuota=s.get("vr_cuota"),
                saldo_anterior=s.get("saldo_anterior"),
                fecha_inicial=s.get("fecha_inicial"),
                fecha_final=s.get("fecha_final"),
                dias=s.get("dias"),
                intereses=s.get("intereses"),
                interes_mora=s.get("interes_mora"),
                abono_capital=s.get("abono_k"),
                cuota=s.get("cuota"),
                saldo_final=s.get("saldo_final"),
                origen_archivo=origen,
            )
            session.add(sm)

    def _cruzar_creditos_sin_historial(self, session, snapshots):
        for s in snapshots:
            placa = s.get("placa", "").strip().upper()
            cliente_nombre = s.get("cliente", "").upper().strip()

            # Snapshots sin placa (ej: JOGLO-COMPRA EUROS) se les asigna una
            if not placa and cliente_nombre:
                placa = cliente_nombre[:15]

            if not placa:
                continue

            exists = session.query(Credito).filter(Credito.placa == placa).first()
            if exists and exists.cliente_id:
                continue

            if not exists and self.dry_run:
                self._log(f"[DRY-RUN] Se crearía crédito (solo snapshot) placa: {placa}")
                continue

            cl = self._get_or_create_cliente(session, cliente_nombre or placa)
            if exists and cl:
                exists.cliente_id = cl.id
                self._log(f"Cliente {cl.nombre} vinculado a crédito {placa}")
            elif cl:
                cred = Credito(
                    placa=placa,
                    sufijo_credito="",
                    cliente_id=cl.id,
                    tiene_historial_detallado=False,
                    activo=True,
                )
                session.add(cred)
                session.flush()
                self._log(f"Crédito creado desde snapshot (sin historial): {placa} para {cl.nombre}")

    def _revincular_snapshots_huerfanos(self, session):
        """Los snapshots se sincronizan antes de crear los créditos 'solo snapshot';
        re-vincula los que quedaron con credito_id=None."""
        huerfanos = session.query(SnapshotMensual).filter(
            SnapshotMensual.credito_id == None  # noqa: E711
        ).all()
        vinculados = 0
        for sm in huerfanos:
            cred = None
            if sm.placa_textual:
                cred = session.query(Credito).filter(
                    Credito.placa == sm.placa_textual,
                    Credito.sufijo_credito == "",
                ).first()
            if cred:
                sm.credito_id = cred.id
                vinculados += 1
        if vinculados:
            self._log(f"Snapshots re-vinculados a créditos: {vinculados}")

    def ejecutar(self):
        self._log("=== INICIANDO SINCRONIZACIÓN DE CARTERA ===")

        creemos_path = Path(self.ruta_creemos)

        if not creemos_path.exists():
            self._log(f"Archivo Creemos.xlsx no encontrado: {creemos_path}", "error")
            return {"status": "error", "error": f"No existe: {creemos_path}"}

        self.db.init_db()
        session = self.db.get_session()

        if self.dry_run:
            self._log("MODO DRY-RUN - No se escribirá nada")

        try:
            # Asegurar columnas nuevas en snapshots_mensuales (migración)
            for col in ["vr_credito NUMERIC(14,0)", "vr_cuota NUMERIC(14,0)",
                        "fecha_original DATE", "numero_bloque INTEGER", "pago_del_mes BOOLEAN"]:
                try:
                    from sqlalchemy import text as _text
                    session.execute(_text(f"ALTER TABLE snapshots_mensuales ADD COLUMN {col}"))
                    session.commit()
                except Exception:
                    session.rollback()

            # Limpiar datos previos de cartera.db para evitar acumulación
            for tabla in [PagoHistorico, SnapshotMensual, Credito, ClienteCartera]:
                session.query(tabla).delete(synchronize_session=False)
            session.flush()
            self._log("Datos previos de cartera.db eliminados.")

            self._log("Parseando Creemos.xlsx...")
            creemos = CreemosParser(str(creemos_path))
            creditos, pagos, snapshots = creemos.parse_all()
            if creemos.errores:
                for e in creemos.errores:
                    self._log(f"  CREEMOS: {e}", "warning")
            self._log(f"  Créditos: {len(creditos)}")
            self._log(f"  Pagos hoja: {len(pagos)}")
            self._log(f"  Snapshots CXCOBRAR: {len(snapshots)} ({len(set(s['mes_reportado'] for s in snapshots))} bloques)")

            if self.dry_run:
                session.close()
                return {"status": "dry_run", "log": self.log}

            for c in creditos:
                cl = self._get_or_create_cliente(
                    session, c["nombre_cliente"], c.get("telefono")
                )
                cred = self._get_or_create_credito(
                    session, c["placa"], c["sufijo_credito"], c
                )
                if cred and cl:
                    cred.cliente_id = cl.id

            self._sync_pagos_joglo(session, creditos, pagos)

            self._sync_snapshots(session, snapshots, "CREEMOS")
            self._cruzar_creditos_sin_historial(session, snapshots)
            self._revincular_snapshots_huerfanos(session)

            session.commit()

            total_pagos = session.query(PagoHistorico).count()
            total_snapshots = session.query(SnapshotMensual).count()
            total_creditos = session.query(Credito).count()
            total_clientes = session.query(ClienteCartera).count()

            self._log("=== SINCRONIZACIÓN COMPLETADA ===")
            self._log(f"  Clientes: {total_clientes}")
            self._log(f"  Créditos: {total_creditos}")
            self._log(f"  Pagos históricos: {total_pagos}")
            self._log(f"  Snapshots mensuales: {total_snapshots}")

            if self.discrepancias:
                self._log(f"  Discrepancias encontradas: {len(self.discrepancias)}", "warning")
                for d in self.discrepancias:
                    self._log(f"    {d}", "warning")

            return {
                "status": "ok",
                "clientes": total_clientes,
                "creditos": total_creditos,
                "pagos": total_pagos,
                "snapshots": total_snapshots,
                "discrepancias": len(self.discrepancias),
            }

        except Exception as e:
            session.rollback()
            self._log(f"Error durante sincronización: {e}", "error")
            raise
        finally:
            session.close()
