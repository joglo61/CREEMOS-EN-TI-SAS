"""Migración ÚNICA y definitiva de Creemos.xlsx → prestamos.db.

Cada fila del ÚLTIMO bloque mensual de CXCOBRAR es un préstamo activo, identificado
por (placa, fecha de desembolso). Así el saldo total cuadra por construcción con el
Excel y un taxi con dos préstamos queda como dos préstamos.

Historial de cada préstamo:
  - Hoja individual de la placa (pagos HIST-*), cuando se puede asignar sin ambigüedad.
  - Filas pagadas de los bloques mensuales (pagos BLOQ-*) para los meses que la hoja no cubre,
    con su interés de mora.

Uso (desde backend/):
  python migrar_excel.py --dry-run            # solo muestra el informe
  python migrar_excel.py                      # migra (hace backup de la BD antes)
  python migrar_excel.py --excel RUTA.xlsx

Se niega a correr si ya existe una migración final (Log MIGRACION_FINAL).
"""
from __future__ import annotations

import argparse
import shutil
import sys
from calendar import monthrange
from collections import defaultdict
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from app.cartera.parser_creemos import MESES, CreemosParser
from app.core.config import settings
from app.models.cliente import Cliente
from app.models.factura import Factura
from app.models.log import Log
from app.models.pago import Pago
from app.models.prestamo import Prestamo
from app.models.usuario import Usuario
from app.services.prestamo_service import PrestamoService

PREFIJO = "CARTERA-"
ACCION = "MIGRACION_FINAL"
EXCEL_DEFECTO = Path(__file__).resolve().parent.parent / "Creemos.xlsx"


def _norm(texto) -> str:
    return " ".join(str(texto or "").upper().split())


def _d(v) -> Decimal:
    return Decimal(str(v or 0))


def _anio_mes(etiqueta: str) -> tuple[int, int]:
    """'OCTUBRE DE 2026' → (2026, 10)"""
    partes = _norm(etiqueta).split()
    return int(partes[-1]), MESES.index(partes[0]) + 1


def _mes_siguiente(d: date, dia: int | None = None) -> date:
    y, m = (d.year + 1, 1) if d.month == 12 else (d.year, d.month + 1)
    return date(y, m, min(dia or d.day, monthrange(y, m)[1]))


def construir(snapshots: list[dict], creditos: list[dict], pagos_hoja: list[dict]) -> tuple[list[dict], list[str]]:
    """Arma la lista de préstamos (con sus pagos) a partir del Excel parseado. Sin tocar la BD."""
    avisos: list[str] = []
    ultimo = max(s["numero_bloque"] for s in snapshots)

    def clave(s):
        return (_norm(s["placa"]), s["fecha_original"] or s["vr_credito"])

    historia = defaultdict(list)
    for s in snapshots:
        historia[clave(s)].append(s)

    filas = [s for s in snapshots if s["numero_bloque"] == ultimo]
    vistas = set()
    for s in filas:
        if clave(s) in vistas:
            avisos.append(f"Fila repetida en el último bloque: {s['placa']} {s['fecha_original']} (se omite la 2ª)")
        vistas.add(clave(s))

    # Hojas individuales agrupadas por placa
    hojas = defaultdict(list)  # placa -> [(credito, [pagos])]
    pagos_por_hoja = defaultdict(list)
    for p in pagos_hoja:
        pagos_por_hoja[(_norm(p["placa"]), p["sufijo"])].append(p)
    for c in creditos:
        hojas[_norm(c["placa"])].append((c, pagos_por_hoja[(_norm(c["placa"]), c["sufijo_credito"])]))

    filas_por_placa = defaultdict(list)
    for s in filas:
        if clave(s) in vistas:
            filas_por_placa[_norm(s["placa"])].append(s)
            vistas.discard(clave(s))

    prestamos = []
    for placa, filas_placa in filas_por_placa.items():
        # Asignar hojas: 1 fila + 1 hoja → directo; si no, por valor del crédito
        asignacion: dict[int, tuple] = {}
        hojas_placa = hojas.get(placa, [])
        if len(filas_placa) == 1 and len(hojas_placa) == 1:
            asignacion[0] = hojas_placa[0]
        else:
            for cred, pgs in hojas_placa:
                idx = [i for i, f in enumerate(filas_placa) if cred["valor_credito"] and f["vr_credito"] == cred["valor_credito"]]
                if len(idx) != 1:
                    # 2º criterio: algún saldo de la hoja coincide con un saldo del préstamo en los bloques
                    saldos_hoja = {p["saldo_real"] for p in pgs if p["saldo_real"]}
                    idx = [i for i, f in enumerate(filas_placa)
                           if saldos_hoja & {s["saldo_final"] for s in historia[clave(f)] if s["saldo_final"]}]
                if len(idx) == 1 and idx[0] not in asignacion:
                    asignacion[idx[0]] = (cred, pgs)
                else:
                    avisos.append(f"Hoja {placa}{cred['sufijo_credito']} (crédito {cred['valor_credito']}) sin préstamo claro: "
                                  f"su historial anterior a los bloques no se importa")

        for i, fila in enumerate(filas_placa):
            cred, pgs = asignacion.get(i, (None, []))
            pagos = []
            # Los bloques CXCOBRAR son el estado oficial: desde el primer bloque mandan ellos;
            # la hoja individual solo aporta la historia anterior.
            primer_bloque = min(((s["fecha_inicial"] or s["fecha_final"]) for s in historia[clave(fila)]
                                 if s["fecha_inicial"] or s["fecha_final"]), default=None)
            for p in pgs:
                f = p["fecha_pago"] or p["fecha_ultimo_pago"]
                if not f or f.year < 2015 or (primer_bloque and f > primer_bloque):
                    continue
                capital = _d(p["capital"])
                pagos.append({
                    "factura": f"HIST-{p['numero_pago']}", "fecha": f, "dias": p["dias"] or 30,
                    "intereses": _d(p["interes"]), "mora": Decimal(0), "capital": capital,
                    "valor": _d(p["cuota"]), "saldo_nuevo": _d(p["saldo_real"]),
                    "saldo_anterior": _d(p["saldo_real"]) + capital,
                    "obs": f"Migrado de hoja {placa} - recibo #{p['recibo'] or ''}",
                })
            for s in historia[clave(fila)]:
                f = s["fecha_final"] or s["fecha_inicial"]
                if not s["pago_del_mes"] or not f:
                    continue
                # El pago pertenece al mes del bloque (recaudo de ese mes), aunque la
                # Fecha Final del periodo caiga en otro mes
                y, m = _anio_mes(s["mes_reportado"])
                f = min(max(f, date(y, m, 1)), date(y, m, monthrange(y, m)[1]))
                k, mora, cap = _d(s["intereses"]), _d(s["interes_mora"]), _d(s["abono_k"])
                pagos.append({
                    "factura": f"BLOQ-{s['numero_bloque']}", "fecha": f, "dias": s["dias"] or 30,
                    "intereses": k, "mora": mora, "capital": cap,
                    "valor": _d(s["cuota"]) if s["cuota"] is not None else k + mora + cap,
                    "saldo_anterior": _d(s["saldo_anterior"]), "saldo_nuevo": _d(s["saldo_final"]),
                    "obs": f"Migrado de {s['mes_reportado']}",
                })
            pagos.sort(key=lambda p: p["fecha"])

            # Controles de calidad para corregir en el Excel antes del corte
            hist = [p for p in pagos if p["factura"].startswith("HIST")]
            bloques_fila = sorted(historia[clave(fila)], key=lambda s: s["numero_bloque"])
            if hist and bloques_fila and bloques_fila[0]["saldo_anterior"] is not None:
                ultimo_hist = max(hist, key=lambda p: p["fecha"])["saldo_nuevo"]
                if abs(ultimo_hist - _d(bloques_fila[0]["saldo_anterior"])) > 100:  # ignora redondeos
                    avisos.append(f"{placa}: la hoja termina en saldo ${ultimo_hist:,.0f} pero CXCOBRAR "
                                  f"({bloques_fila[0]['mes_reportado']}) arranca en ${_d(bloques_fila[0]['saldo_anterior']):,.0f}")
            futuros = [p for p in pagos if p["fecha"] > date.today()]
            if futuros:
                avisos.append(f"{placa}: pago con fecha futura {futuros[0]['fecha']} ({futuros[0]['obs']}) — ¿error de digitación?")
            if not pagos:
                avisos.append(f"{placa} ({_norm(fila['cliente'])}): sin pagos marcados en hojas ni bloques; "
                              f"próximo pago = 1 mes después de la Fecha Final del bloque ({fila['fecha_final']})")

            saldo = fila["saldo_final"] if fila["saldo_final"] is not None else fila["saldo_anterior"]
            ultima = max([p["fecha"] for p in pagos] + [d for d in (fila["fecha_final"],) if d], default=None)
            fecha_inicio = fila["fecha_original"] or (pagos[0]["fecha"] if pagos else date.today())
            proximo = _mes_siguiente(ultima) if ultima else _mes_siguiente(fecha_inicio)
            prestamos.append({
                "placa": fila["placa"].strip().upper()[:20], "cliente": _norm(fila["cliente"]) or f"CLIENTE {placa}",
                "telefono": (cred or {}).get("telefono"), "fecha_inicio": fecha_inicio,
                "capital": _d(fila["vr_credito"]), "cuota": _d(fila["vr_cuota"]), "saldo": _d(saldo),
                "fecha_primer_pago": _mes_siguiente(fecha_inicio, proximo.day), "fecha_proximo_pago": proximo,
                "pagos": pagos,
            })
    return prestamos, avisos


def _ruta_bd() -> Path | None:
    url = settings.DATABASE_URL
    return Path(url.replace("sqlite:///", "", 1)) if url.startswith("sqlite:///") else None


def migrar(db, ruta_excel: Path, dry_run: bool = True, descartar_pagos_sistema: bool = False, base_limpia: bool = False) -> dict:
    """base_limpia: borra TODOS los clientes/préstamos/pagos/facturas (datos de prueba) y deja solo lo del Excel.
    Conserva usuarios, configuración y logs."""
    if db.query(Log).filter(Log.accion == ACCION).first():
        raise SystemExit("Ya existe una migración final (Log MIGRACION_FINAL). No se vuelve a migrar.")

    creditos, pagos_hoja, snapshots = CreemosParser(ruta_excel).parse_all()
    prestamos, avisos = construir(snapshots, creditos, pagos_hoja)
    ultimo = max(s["numero_bloque"] for s in snapshots)
    filas_ult = [s for s in snapshots if s["numero_bloque"] == ultimo]
    saldo_excel = sum(_d(s["saldo_final"] if s["saldo_final"] is not None else s["saldo_anterior"]) for s in filas_ult)
    saldo_migrado = sum(p["saldo"] for p in prestamos)

    # Datos previos: importaciones viejas (CARTERA-*) se reemplazan; los pagos hechos en la app se avisan
    q_prev = db.query(Cliente) if base_limpia else db.query(Cliente).filter(Cliente.cedula.like(f"{PREFIJO}%"))
    previos = q_prev.all()
    ids_prev = [c.id for c in previos]
    pagos_app = db.query(Pago).join(Prestamo).filter(Prestamo.cliente_id.in_(ids_prev), Pago.numero_factura.like("FACT-%")).all() if ids_prev else []
    if base_limpia:
        descartar_pagos_sistema = True  # todo lo registrado en la app eran pruebas
    # Préstamos ya creados en la app (cliente no CARTERA) que también están en el Excel → no duplicar
    existentes = set() if base_limpia else {(_norm(c.nombre), p.fecha_inicio) for c, p in db.query(Cliente, Prestamo).join(Prestamo)
                                            .filter(~Cliente.cedula.like(f"{PREFIJO}%")).all()}
    omitidos = [p for p in prestamos if (p["cliente"], p["fecha_inicio"]) in existentes]
    prestamos = [p for p in prestamos if (p["cliente"], p["fecha_inicio"]) not in existentes]

    informe = {
        "bloque": filas_ult[0]["mes_reportado"] if filas_ult else "?", "filas_ultimo_bloque": len(filas_ult),
        "prestamos": len(prestamos) + len(omitidos), "omitidos_ya_en_app": [(p["placa"], p["cliente"]) for p in omitidos],
        "clientes": len({p["cliente"] for p in prestamos}),
        "pagos": sum(len(p["pagos"]) for p in prestamos),
        "mora_total": sum(x["mora"] for p in prestamos for x in p["pagos"]),
        "saldo_excel": saldo_excel, "saldo_migrado": saldo_migrado, "cuadra": saldo_excel == saldo_migrado,
        "clientes_previos_reemplazados": len(previos), "base_limpia": base_limpia,
        "pagos_app_en_previos": [(p.numero_factura, str(p.fecha_pago), str(p.valor_pagado)) for p in pagos_app],
        "avisos": avisos,
    }
    if dry_run:
        return informe
    if not informe["cuadra"]:
        raise SystemExit(f"El saldo no cuadra (Excel {saldo_excel} vs migrado {saldo_migrado}). Revise el dry-run.")
    if pagos_app and not descartar_pagos_sistema:
        raise SystemExit(f"Hay {len(pagos_app)} pagos registrados en la app sobre clientes importados: {informe['pagos_app_en_previos']}. "
                         "Use --descartar-pagos-sistema si son pruebas.")

    ruta = _ruta_bd()
    if ruta and ruta.exists():
        backup = ruta.with_name(f"{ruta.stem}_antes_migracion_{datetime.now():%Y%m%d_%H%M%S}{ruta.suffix}")
        shutil.copy2(ruta, backup)
        informe["backup"] = str(backup)

    admin = db.query(Usuario).filter(Usuario.rol == "ADMINISTRADOR").order_by(Usuario.id).first()
    usuario_id = admin.id if admin else 1

    # Borrado directo (sin depender de cascadas del ORM), en orden de llaves foráneas
    from app.models.cronograma import Cronograma
    ids_prest = [p.id for p in db.query(Prestamo.id).filter(Prestamo.cliente_id.in_(ids_prev))] if ids_prev else []
    ids_pagos = [p.id for p in db.query(Pago.id).filter(Pago.prestamo_id.in_(ids_prest))] if ids_prest else []
    for modelo, filtro in ((Factura, Factura.cliente_id.in_(ids_prev) | Factura.pago_id.in_(ids_pagos)),
                           (Pago, Pago.prestamo_id.in_(ids_prest)),
                           (Cronograma, Cronograma.prestamo_id.in_(ids_prest)),
                           (Prestamo, Prestamo.id.in_(ids_prest)),
                           (Cliente, Cliente.id.in_(ids_prev))):
        db.query(modelo).filter(filtro).delete(synchronize_session=False)
    db.flush()
    db.expunge_all()  # olvidar objetos ya borrados por SQL (SQLite reutiliza ids)
    numeros: set[str] = set()

    placas_cliente = {c.placa for c in db.query(Cliente.placa).all()}
    clientes: dict[str, Cliente] = {}
    servicio = PrestamoService(db)
    for n, p in enumerate(prestamos, start=1):
        cli = clientes.get(p["cliente"])
        if not cli:
            placa_cli = p["placa"] if p["placa"] not in placas_cliente else f"{p['placa'][:14]}-{n}"
            placas_cliente.add(placa_cli)
            cli = Cliente(nombre=p["cliente"][:200], cedula=f"{PREFIJO}{len(clientes) + 1:04d}", placa=placa_cli,
                          telefono=(p["telefono"] or None) and str(p["telefono"])[:20], estado="ACTIVO")
            db.add(cli)
            db.flush()
            clientes[p["cliente"]] = cli
        pr = Prestamo(cliente_id=cli.id, placa=p["placa"], capital_inicial=p["capital"], saldo_actual=p["saldo"],
                      valor_cuota=p["cuota"], tasa_interes=Decimal("2.5"), fecha_inicio=p["fecha_inicio"],
                      fecha_primer_pago=p["fecha_primer_pago"], fecha_proximo_pago=p["fecha_proximo_pago"], estado="ACTIVO")
        db.add(pr)
        db.flush()
        for x in p["pagos"]:
            # MIG-H007-12 = préstamo migrado 7, pago 12 de la hoja; MIG-B007-10 = bloque 10
            num = f"MIG-{x['factura'][0]}{n:03d}-{x['factura'].split('-', 1)[1]}"
            while num in numeros:  # numeración repetida en la hoja
                num += "b"
            numeros.add(num)
            pago = Pago(prestamo_id=pr.id, numero_factura=num, fecha_pago=x["fecha"], dias_calculados=x["dias"],
                        dias_mora=0, saldo_anterior=x["saldo_anterior"], intereses=x["intereses"], intereses_mora=x["mora"],
                        capital=x["capital"], valor_pagado=x["valor"], saldo_nuevo=x["saldo_nuevo"],
                        observaciones=x["obs"], usuario_id=usuario_id, tasa_interes_aplicada=Decimal("2.5"))
            db.add(pago)
            db.flush()
            db.add(Factura(numero_factura=num, cliente_id=cli.id, pago_id=pago.id, fecha=x["fecha"], estado="EMITIDA"))
        servicio.actualizar_estado_automatico(pr)  # MORA/ACTIVO/PAGADO reales (solo flush: todo es una transacción)

    db.add(Log(usuario_id=usuario_id, accion=ACCION, modulo="Migracion",
               descripcion=f"Migrados {informe['prestamos']} préstamos, {informe['clientes']} clientes, {informe['pagos']} pagos "
                           f"desde {ruta_excel.name} ({informe['bloque']}). Saldo {saldo_migrado}."))
    db.commit()
    return informe


def _imprimir(inf: dict):
    print(f"Último bloque: {inf['bloque']} ({inf['filas_ultimo_bloque']} filas)")
    print(f"Préstamos: {inf['prestamos']}  Clientes: {inf['clientes']}  Pagos históricos: {inf['pagos']}")
    print(f"Interés de mora histórico: ${inf['mora_total']:,.0f}")
    print(f"Saldo Excel ${inf['saldo_excel']:,.0f}  |  Saldo migrado ${inf['saldo_migrado']:,.0f}  →  {'CUADRA' if inf['cuadra'] else 'NO CUADRA'}")
    print(f"Clientes que se borran antes de migrar ({'TODOS: base limpia' if inf['base_limpia'] else 'solo importaciones CARTERA-*'}): {inf['clientes_previos_reemplazados']}")
    if inf["omitidos_ya_en_app"]:
        print(f"Ya existen en la app (no se duplican): {inf['omitidos_ya_en_app']}")
    if inf["pagos_app_en_previos"]:
        print(f"{'Se descartan' if inf['base_limpia'] else '⚠'} pagos registrados en la app: {inf['pagos_app_en_previos']}")
    for a in inf["avisos"]:
        print(f"⚠ {a}")
    if inf.get("backup"):
        print(f"Backup: {inf['backup']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--excel", type=Path, default=EXCEL_DEFECTO)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--descartar-pagos-sistema", action="store_true")
    ap.add_argument("--base-limpia", action="store_true", help="borra todos los clientes/préstamos/pagos de prueba antes de migrar")
    args = ap.parse_args()

    import app.main  # noqa: F401  crea tablas/columnas faltantes
    from app.database.database import SessionLocal

    sesion = SessionLocal()
    try:
        _imprimir(migrar(sesion, args.excel, dry_run=args.dry_run, descartar_pagos_sistema=args.descartar_pagos_sistema,
                         base_limpia=args.base_limpia))
    finally:
        sesion.close()
    sys.exit(0)
