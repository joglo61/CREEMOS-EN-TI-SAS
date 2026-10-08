"""Cartera por cobrar de un mes (reemplazo del bloque mensual CXCOBRAR del Excel).

Se calcula desde los pagos registrados, sin snapshots: el saldo de cualquier mes pasado
es el `saldo_nuevo` del último pago anterior a ese mes (o el capital si no hay pagos).
"""
from __future__ import annotations

from calendar import monthrange
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session, joinedload

from app.models.prestamo import Prestamo

MESES = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO",
         "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]


def cartera_del_mes(db: Session, anio: int, mes: int) -> dict:
    inicio = date(anio, mes, 1)
    fin = date(anio, mes, monthrange(anio, mes)[1])
    prestamos = (db.query(Prestamo).options(joinedload(Prestamo.cliente), joinedload(Prestamo.pagos))
                 .filter(Prestamo.fecha_inicio <= fin, Prestamo.estado != "CANCELADO").all())

    filas = []
    for p in prestamos:
        pagos = sorted(p.pagos, key=lambda x: (x.fecha_pago, x.id))
        antes = [x for x in pagos if x.fecha_pago < inicio]
        del_mes = [x for x in pagos if inicio <= x.fecha_pago <= fin]
        alta = p.fecha_inicio >= inicio
        # Sin pagos anteriores: saldo previo al primer pago conocido (préstamos migrados traen
        # historia parcial) o, si nunca ha pagado, su saldo actual
        saldo_ini = (antes[-1].saldo_nuevo if antes
                     else pagos[0].saldo_anterior if pagos else p.saldo_actual)
        if saldo_ini <= 0 and not del_mes:
            continue  # crédito ya saldado: sale de la cartera, como en el Excel

        filas.append({
            "prestamo_id": p.id,
            "fecha_desembolso": p.fecha_inicio.isoformat(),
            "placa": p.placa or (p.cliente.placa if p.cliente else ""),
            "cliente": p.cliente.nombre if p.cliente else "",
            "vr_credito": p.capital_inicial,
            "vr_cuota": p.valor_cuota,
            "saldo_anterior": saldo_ini,
            "fecha_inicial": (antes[-1].fecha_pago if antes else p.fecha_inicio).isoformat(),
            "fecha_final": del_mes[-1].fecha_pago.isoformat() if del_mes else None,
            "dias": sum(x.dias_calculados or 0 for x in del_mes) or None,
            "intereses": sum((x.intereses for x in del_mes), Decimal(0)),
            "interes_mora": sum((x.intereses_mora or 0 for x in del_mes), Decimal(0)),
            "abono_capital": sum((x.capital for x in del_mes), Decimal(0)),
            "cuota": sum((x.valor_pagado for x in del_mes), Decimal(0)),
            "saldo_final": del_mes[-1].saldo_nuevo if del_mes else saldo_ini,
            "pago_en_mes": bool(del_mes),
            "alta": alta,
            "estado": p.estado,
            "facturas": [x.numero_factura for x in del_mes],
        })

    filas.sort(key=lambda f: (f["fecha_desembolso"], f["placa"]))

    def total(k):
        return sum((f[k] for f in filas), Decimal(0))

    saldo_anterior = total("saldo_anterior")
    return {
        "mes": f"{MESES[mes - 1]} DE {anio}",
        "anio": anio,
        "numero_mes": mes,
        "items": filas,
        "totales": {
            "creditos": len(filas),
            "pagaron": sum(1 for f in filas if f["pago_en_mes"]),
            "saldo_anterior": saldo_anterior,
            "recaudo": total("cuota"),
            "abono_capital": total("abono_capital"),
            "abono_intereses": total("intereses") + total("interes_mora"),
            "interes_mora": total("interes_mora"),
            "saldo_final": total("saldo_final"),
            "interes_esperado": (saldo_anterior * Decimal("0.025")).quantize(Decimal(1)),  # 2,5 % sobre el saldo
        },
    }
