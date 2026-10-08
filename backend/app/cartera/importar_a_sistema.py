from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal
from calendar import monthrange
import logging

from app.models.cliente import Cliente
from app.models.prestamo import Prestamo
from app.models.pago import Pago
from app.models.factura import Factura
from app.models.log import Log
from app.cartera.database import CarteraDatabase
from app.cartera.models import ClienteCartera, Credito, PagoHistorico, SnapshotMensual

logger = logging.getLogger("app.cartera.importar")

CEDULA_PREFIX = "CARTERA-"

def importar_cartera_a_sistema(db_main: Session, usuario_id: int = 1) -> dict:

    cdb = CarteraDatabase()
    ses_cartera = cdb.get_session()
    resultado = {"clientes": 0, "prestamos": 0, "pagos": 0, "eliminados": 0, "errores": []}

    try:
        for col in ["vr_credito NUMERIC(14,0)", "vr_cuota NUMERIC(14,0)", "fecha_original DATE",
                    "numero_bloque INTEGER", "pago_del_mes BOOLEAN"]:
            try:
                from sqlalchemy import text as _text
                ses_cartera.execute(_text(f"ALTER TABLE snapshots_mensuales ADD COLUMN {col}"))
                ses_cartera.commit()
            except Exception:
                ses_cartera.rollback()

        # Preservar pagos del sistema (FACT-*) de clientes cartera antes de limpiar
        pagos_sistema_previos = []
        q_prev = db_main.query(Pago, Prestamo, Cliente).join(
            Prestamo, Pago.prestamo_id == Prestamo.id
        ).join(
            Cliente, Prestamo.cliente_id == Cliente.id
        ).filter(
            Cliente.cedula.like(f"{CEDULA_PREFIX}%"),
            Pago.numero_factura.like("FACT-%"),
        ).all()
        for p_sys, pre_sys, cli_sys in q_prev:
            pagos_sistema_previos.append({
                "cliente_nombre": cli_sys.nombre,
                "prestamo_fecha_inicio": pre_sys.fecha_inicio,
                "numero_factura": p_sys.numero_factura,
                "fecha_pago": p_sys.fecha_pago,
                "dias_calculados": p_sys.dias_calculados,
                "dias_mora": p_sys.dias_mora,
                "saldo_anterior": p_sys.saldo_anterior,
                "intereses": p_sys.intereses,
                "intereses_mora": p_sys.intereses_mora,
                "capital": p_sys.capital,
                "valor_pagado": p_sys.valor_pagado,
                "saldo_nuevo": p_sys.saldo_nuevo,
                "observaciones": p_sys.observaciones,
                "usuario_id": p_sys.usuario_id,
                "tasa_interes_aplicada": p_sys.tasa_interes_aplicada,
            })
        if pagos_sistema_previos:
            logger.info(f"Pagos del sistema a preservar: {len(pagos_sistema_previos)}")

        # Limpiar importaciones previas (CARTERA-*)
        cartera_ids = [
            c.id for c in db_main.query(Cliente.id).filter(
                Cliente.cedula.like(f"{CEDULA_PREFIX}%")
            ).all()
        ]
        if cartera_ids:
            prestamo_ids = [
                p.id for p in db_main.query(Prestamo.id).filter(
                    Prestamo.cliente_id.in_(cartera_ids)
                ).all()
            ]
            if prestamo_ids:
                db_main.query(Factura).filter(Factura.cliente_id.in_(cartera_ids)).delete(
                    synchronize_session=False
                )
                db_main.query(Pago).filter(Pago.prestamo_id.in_(prestamo_ids)).delete(
                    synchronize_session=False
                )
            db_main.query(Prestamo).filter(Prestamo.cliente_id.in_(cartera_ids)).delete(
                synchronize_session=False
            )
            db_main.query(Cliente).filter(Cliente.id.in_(cartera_ids)).delete(
                synchronize_session=False
            )
            resultado["eliminados"] = len(cartera_ids)
        db_main.flush()

        # Snapshots CREEMOS (todos los bloques)
        snapshots = ses_cartera.query(SnapshotMensual).filter(
            SnapshotMensual.origen_archivo == "CREEMOS"
        ).all()
        logger.info(f"Snapshots CREEMOS en DB: {len(snapshots)}")

        # Último bloque (AGOSTO) = estado actual de la cartera
        ultimo_bloque = max((s.numero_bloque or 0 for s in snapshots), default=1)
        placas_activas: set[str] = set()
        for s in snapshots:
            if (s.numero_bloque or 0) == ultimo_bloque and s.placa_textual:
                placas_activas.add(s.placa_textual)
        logger.info(f"Último bloque: {ultimo_bloque} - placas vigentes: {len(placas_activas)}")

        snapshots_por_placa: dict[str, list[SnapshotMensual]] = {}
        for s in snapshots:
            if (s.numero_bloque or 0) == ultimo_bloque and s.placa_textual:
                snapshots_por_placa.setdefault(s.placa_textual, []).append(s)
        logger.info(f"Snapshots del último bloque en DB: {sum(len(v) for v in snapshots_por_placa.values())}")

        # Todos los créditos con cliente
        todos_creditos = ses_cartera.query(Credito).all()
        creditos_cc_ids = {c.cliente_id for c in todos_creditos if c.cliente_id}

        # Solo clientes con al menos un crédito vigente (placa en último bloque)
        cc_ids_activos = {
            c.cliente_id for c in todos_creditos
            if c.cliente_id and c.placa.strip().upper() in placas_activas
        }
        logger.info(f"Clientes de cartera con crédito vigente: {len(cc_ids_activos)}")

        clientes_cartera = ses_cartera.query(ClienteCartera).filter(
            ClienteCartera.id.in_(list(cc_ids_activos))
        ).all() if cc_ids_activos else []
        cc_por_id = {c.id: c for c in clientes_cartera}
        logger.info(f"Clientes a importar: {len(cc_por_id)}")

        # Crear clientes en DB principal
        cliente_por_cc: dict[int, Cliente] = {}
        placas_usadas: set[str] = set()

        for cc_id, cc in cc_por_id.items():
            cedula = f"{CEDULA_PREFIX}CC{cc_id}"
            cliente_main = db_main.query(Cliente).filter(
                Cliente.cedula == cedula
            ).first()
            if cliente_main:
                cliente_por_cc[cc_id] = cliente_main
                continue

            # Reusar cliente del sistema (no CARTERA-*) con el mismo nombre:
            # créditos creados en el sistema que entraron al Excel como altas
            nombre_cc = (cc.nombre or "").upper().strip()
            if nombre_cc:
                sistema_existente = db_main.query(Cliente).filter(
                    Cliente.nombre == nombre_cc,
                    ~Cliente.cedula.like(f"{CEDULA_PREFIX}%"),
                ).first()
                if sistema_existente:
                    logger.info(f"Cliente del sistema reutilizado por nombre: {cc.nombre}")
                    cliente_por_cc[cc_id] = sistema_existente
                    continue

            # Buscar placa asociada al cliente (desde cualquiera de sus créditos)
            creditos_cc = ses_cartera.query(Credito).filter(
                Credito.cliente_id == cc_id
            ).all()
            placa_cliente = None
            for cred in creditos_cc:
                p = cred.placa.strip().upper()
                if p and p in placas_activas:
                    placa_cliente = p
                    break
            if not placa_cliente:
                placa_cliente = f"SN-{cc_id}"

            if placa_cliente not in placas_usadas:
                placa_final = placa_cliente
                placas_usadas.add(placa_final)
            else:
                placa_final = f"{placa_cliente}-{cc_id}"

            cliente_main = Cliente(
                nombre=cc.nombre or f"Cliente {cc_id}",
                cedula=cedula,
                placa=placa_final,
                telefono=cc.telefono,
                estado="ACTIVO",
            )
            db_main.add(cliente_main)
            db_main.flush()
            resultado["clientes"] += 1
            cliente_por_cc[cc_id] = cliente_main

        # Solo créditos vigentes (placa en último bloque)
        creditos = ses_cartera.query(Credito).filter(
            Credito.cliente_id.in_(list(cc_por_id.keys()))
        ).all() if cc_por_id else []
        creditos = [c for c in creditos if c.placa.strip().upper() in placas_activas]
        logger.info(f"Creditos vigentes a importar: {len(creditos)}")

        for cred in creditos:
            placa = cred.placa.strip().upper()
            cc_id = cred.cliente_id
            if cc_id not in cliente_por_cc:
                continue
            cliente_main = cliente_por_cc[cc_id]

            # Asignar un snapshot del último bloque por crédito (placas duplicadas = 2 créditos)
            snaps_placa = snapshots_por_placa.get(placa) or []
            snap = snaps_placa.pop(0) if snaps_placa else None
            fecha_inicio = (snap.fecha_original or cred.fecha_desembolso or date(2022, 10, 1)) if snap else (cred.fecha_desembolso or date(2022, 10, 1))

            # Crédito del sistema (cliente reutilizado por nombre): no recrear el préstamo
            if not cliente_main.cedula.startswith(CEDULA_PREFIX):
                prestamo_existente = db_main.query(Prestamo).filter(
                    Prestamo.cliente_id == cliente_main.id,
                    Prestamo.fecha_inicio == fecha_inicio,
                ).first()
                if prestamo_existente:
                    logger.info(f"Préstamo del sistema ya existe ({placa}, {cliente_main.nombre}); se conserva tal cual")
                    continue

            # Cada crédito vigente genera un préstamo (los previos se limpiaron arriba)
            if snap:
                capital_inicial = Decimal(str(snap.vr_credito)) if snap.vr_credito else (Decimal(str(cred.valor_credito)) if cred.valor_credito else Decimal("0"))
                cuota_val = Decimal(str(snap.vr_cuota)) if snap.vr_cuota else (Decimal(str(cred.valor_cuota or 0)))
                if snap.saldo_final is not None:
                    saldo_actual = Decimal(str(snap.saldo_final))
                elif snap.saldo_anterior is not None:
                    saldo_actual = Decimal(str(snap.saldo_anterior))
                else:
                    saldo_actual = capital_inicial
            else:
                capital_inicial = Decimal(str(cred.valor_credito)) if cred.valor_credito else Decimal("0")
                cuota_val = Decimal(str(cred.valor_cuota or 0))
                saldo_actual = capital_inicial

            fecha_primer_pago = date(fecha_inicio.year, fecha_inicio.month + 1, min(fecha_inicio.day, 28)) if fecha_inicio.month < 12 else date(fecha_inicio.year + 1, 1, min(fecha_inicio.day, 28))

            prestamo_main = Prestamo(
                cliente_id=cliente_main.id,
                capital_inicial=capital_inicial,
                saldo_actual=saldo_actual,
                valor_cuota=cuota_val,
                tasa_interes=Decimal("2.5"),
                fecha_inicio=fecha_inicio,
                fecha_primer_pago=fecha_primer_pago,
                fecha_proximo_pago=fecha_primer_pago,
                estado="ACTIVO",
            )
            db_main.add(prestamo_main)
            db_main.flush()
            resultado["prestamos"] += 1

            if prestamo_main:
                pagos_historicos = ses_cartera.query(PagoHistorico).filter(
                    PagoHistorico.credito_id == cred.id
                ).order_by(PagoHistorico.numero_pago).all()

                # Meses (año, mes) ya cubiertos por la hoja individual
                meses_hoja: set[tuple[int, int]] = set()
                # Fecha del último pago real (para fecha_proximo_pago y mora)
                ultima_fecha_pago: date | None = None

                for ph in pagos_historicos:
                    fpago_raw = ph.fecha_pago or ph.fecha_ultimo_pago
                    if fpago_raw and fpago_raw.year < 2020:
                        fpago_raw = None
                    fpago = fpago_raw or (cred.fecha_desembolso or date(2022, 10, 1))
                    meses_hoja.add((fpago.year, fpago.month))
                    if ultima_fecha_pago is None or fpago > ultima_fecha_pago:
                        ultima_fecha_pago = fpago

                    factura_num = f"HIST-{cred.id}-{ph.numero_pago or 0}"
                    existente = db_main.query(Pago).filter(
                        Pago.prestamo_id == prestamo_main.id,
                        Pago.numero_factura == factura_num,
                    ).first()
                    if existente:
                        continue

                    capital_val = Decimal(str(ph.capital or 0))
                    cuota_val = Decimal(str(ph.cuota or 0))
                    interes_val = Decimal(str(ph.interes or 0))
                    saldo_real = Decimal(str(ph.saldo_real or 0))
                    saldo_anterior = saldo_real + capital_val

                    pago_main = Pago(
                        prestamo_id=prestamo_main.id,
                        numero_factura=factura_num,
                        fecha_pago=fpago,
                        dias_calculados=ph.dias or 30,
                        dias_mora=0,
                        saldo_anterior=saldo_anterior,
                        intereses=interes_val,
                        intereses_mora=Decimal("0"),
                        capital=capital_val,
                        valor_pagado=cuota_val,
                        saldo_nuevo=saldo_real,
                        observaciones=f"Importado cartera - recibo #{ph.recibo or ''}",
                        usuario_id=usuario_id,
                    )
                    db_main.add(pago_main)
                    db_main.flush()

                    factura = Factura(
                        numero_factura=factura_num,
                        cliente_id=cliente_main.id,
                        pago_id=pago_main.id,
                        fecha=fpago,
                        estado="EMITIDA",
                    )
                    db_main.add(factura)
                    resultado["pagos"] += 1

                # Pagos de bloques CXCOBRAR (pago_del_mes) sin duplicar meses de la hoja
                for s in snapshots:
                    if s.credito_id != cred.id or not s.pago_del_mes:
                        continue
                    fp_bloque = s.fecha_final or s.fecha_inicial
                    if not fp_bloque:
                        continue
                    if ultima_fecha_pago is None or fp_bloque > ultima_fecha_pago:
                        ultima_fecha_pago = fp_bloque
                    if (fp_bloque.year, fp_bloque.month) in meses_hoja:
                        continue

                    capital_b = Decimal(str(s.abono_capital or 0))
                    interes_b = Decimal(str(s.intereses or 0))
                    if s.cuota:
                        pagado_b = Decimal(str(s.cuota))
                    elif s.abono_capital:
                        pagado_b = capital_b + interes_b
                    else:
                        pagado_b = interes_b
                    saldo_nuevo_b = (
                        Decimal(str(s.saldo_final)) if s.saldo_final is not None
                        else Decimal(str(s.saldo_anterior or 0)) - capital_b
                    )

                    factura_b = f"BLOQ-{cred.id}-{s.numero_bloque or 0}"
                    # Placa duplicada en el mismo bloque (2 filas pagadas el mismo mes):
                    # acumular en el pago BLOQ ya creado en vez de descartar la 2ª fila
                    existente_b = db_main.query(Pago).filter(
                        Pago.prestamo_id == prestamo_main.id,
                        Pago.numero_factura == factura_b,
                    ).first()
                    if existente_b:
                        existente_b.valor_pagado = existente_b.valor_pagado + pagado_b
                        existente_b.capital = existente_b.capital + capital_b
                        existente_b.intereses = existente_b.intereses + interes_b
                        if s.saldo_final is not None:
                            existente_b.saldo_nuevo = Decimal(str(s.saldo_final))
                        continue
                    pago_bloque = Pago(
                        prestamo_id=prestamo_main.id,
                        numero_factura=factura_b,
                        fecha_pago=fp_bloque,
                        dias_calculados=s.dias or 30,
                        dias_mora=0,
                        saldo_anterior=saldo_nuevo_b + capital_b,
                        intereses=interes_b,
                        intereses_mora=Decimal("0"),
                        capital=capital_b,
                        valor_pagado=pagado_b,
                        saldo_nuevo=saldo_nuevo_b,
                        observaciones=f"Pago del mes {s.mes_reportado} (bloque)",
                        usuario_id=usuario_id,
                    )
                    db_main.add(pago_bloque)
                    db_main.flush()

                    factura = Factura(
                        numero_factura=factura_b,
                        cliente_id=cliente_main.id,
                        pago_id=pago_bloque.id,
                        fecha=fp_bloque,
                        estado="EMITIDA",
                    )
                    db_main.add(factura)
                    resultado["pagos"] += 1

                # Col I (Fecha Final) del último bloque: si no pagó ese mes,
                # arrastra la fecha de su último pago (col H/I del período)
                if snap and snap.fecha_final:
                    if ultima_fecha_pago is None or snap.fecha_final > ultima_fecha_pago:
                        ultima_fecha_pago = snap.fecha_final

                # El próximo pago vence un mes después del último pago real;
                # de esta fecha salen los días de mora al registrar el siguiente pago
                if ultima_fecha_pago:
                    y = ultima_fecha_pago.year
                    m = ultima_fecha_pago.month + 1
                    if m > 12:
                        m = 1
                        y += 1
                    d = min(ultima_fecha_pago.day, monthrange(y, m)[1])
                    prestamo_main.fecha_proximo_pago = date(y, m, d)

        # Re-crear pagos del sistema (FACT-*) preservados antes de la limpieza
        restaurados = 0
        for ps in pagos_sistema_previos:
            cli = db_main.query(Cliente).filter(
                Cliente.nombre == ps["cliente_nombre"],
                Cliente.cedula.like(f"{CEDULA_PREFIX}%"),
            ).first()
            if not cli:
                continue
            prestamos_cli = db_main.query(Prestamo).filter(
                Prestamo.cliente_id == cli.id
            ).all()
            target = None
            for pr in prestamos_cli:
                if pr.fecha_inicio == ps["prestamo_fecha_inicio"]:
                    target = pr
                    break
            if not target and prestamos_cli:
                target = prestamos_cli[0]
            if not target:
                continue

            # Ya vino del Excel (botón escribió primero): no duplicar
            dup = db_main.query(Pago).filter(
                Pago.prestamo_id == target.id,
                Pago.fecha_pago == ps["fecha_pago"],
                Pago.valor_pagado == ps["valor_pagado"],
            ).first()
            if dup:
                continue

            pago_restore = Pago(
                prestamo_id=target.id,
                numero_factura=ps["numero_factura"],
                fecha_pago=ps["fecha_pago"],
                dias_calculados=ps["dias_calculados"],
                dias_mora=ps["dias_mora"],
                saldo_anterior=ps["saldo_anterior"],
                intereses=ps["intereses"],
                intereses_mora=ps["intereses_mora"],
                capital=ps["capital"],
                valor_pagado=ps["valor_pagado"],
                saldo_nuevo=ps["saldo_nuevo"],
                observaciones=ps["observaciones"],
                usuario_id=ps["usuario_id"],
                tasa_interes_aplicada=ps["tasa_interes_aplicada"],
            )
            db_main.add(pago_restore)
            db_main.flush()

            # Ajustar saldo y próxima fecha como si el pago se hubiera registrado
            target.saldo_actual = ps["saldo_nuevo"]
            nm = target.fecha_proximo_pago.month + 1
            ny = target.fecha_proximo_pago.year
            if nm > 12:
                nm = 1
                ny += 1
            nd = min(target.fecha_proximo_pago.day, monthrange(ny, nm)[1])
            target.fecha_proximo_pago = date(ny, nm, nd)

            fact_restore = Factura(
                numero_factura=ps["numero_factura"],
                cliente_id=cli.id,
                pago_id=pago_restore.id,
                fecha=ps["fecha_pago"],
                estado="EMITIDA",
            )
            db_main.add(fact_restore)
            restaurados += 1
        if restaurados:
            logger.info(f"Pagos del sistema restaurados tras importación: {restaurados}")

        db_main.commit()
        log = Log(
            usuario_id=usuario_id, accion="IMPORTAR_CARTERA", modulo="Cartera",
            descripcion=f"Importados {resultado['clientes']} clientes, {resultado['prestamos']} prestamos, {resultado['pagos']} pagos (eliminados {resultado['eliminados']} previos)",
        )
        db_main.add(log)
        db_main.commit()

    except Exception as e:
        db_main.rollback()
        logger.error(f"Error importando cartera: {e}")
        resultado["errores"].append(str(e))
    finally:
        ses_cartera.close()

    return resultado
