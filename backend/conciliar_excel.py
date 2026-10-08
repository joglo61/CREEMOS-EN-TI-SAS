"""Conciliación de SOLO LECTURA: bloque mensual de Creemos.xlsx vs cartera mensual del sistema.

Para el mes en paralelo: el personal sigue anotando en el Excel y registra en la app;
este script lista, por préstamo (placa + fecha de desembolso), las diferencias en
"pagó / no pagó", valor pagado y saldo final.

Uso (desde backend/):
  python conciliar_excel.py --excel RUTA.xlsx                 # último bloque del Excel
  python conciliar_excel.py --excel RUTA.xlsx --mes 2026-10
  python conciliar_excel.py --excel RUTA.xlsx --todos         # todos los bloques (validación histórica)
"""
from __future__ import annotations

import argparse
from decimal import Decimal
from pathlib import Path

from app.cartera.parser_creemos import CreemosParser
from app.services.cartera_mensual import cartera_del_mes
from migrar_excel import _anio_mes

TOLERANCIA = Decimal(1)  # pesos (redondeos del Excel)


def _norm(t) -> str:
    return " ".join(str(t or "").upper().split())


def conciliar_mes(db, filas_excel: list[dict], anio: int, mes: int) -> dict:
    app = {(_norm(f["placa"]), f["fecha_desembolso"]): f for f in cartera_del_mes(db, anio, mes)["items"]}
    difs, solo_excel, coinciden = [], [], 0
    vistos = set()
    for s in filas_excel:
        clave = (_norm(s["placa"]), s["fecha_original"].isoformat() if s["fecha_original"] else None)
        vistos.add(clave)
        a = app.get(clave)
        if not a:
            solo_excel.append(f"{s['placa']} {s['cliente']} saldo={s['saldo_final']}")
            continue
        e_pago = bool(s["pago_del_mes"])
        e_valor = Decimal(s["cuota"] or 0) if e_pago else Decimal(0)
        e_saldo = Decimal(s["saldo_final"] if s["saldo_final"] is not None else (s["saldo_anterior"] or 0))
        problemas = []
        if e_pago != a["pago_en_mes"]:
            problemas.append(f"pagó: Excel={'sí' if e_pago else 'no'} app={'sí' if a['pago_en_mes'] else 'no'}")
        if abs(e_valor - a["cuota"]) > TOLERANCIA:
            problemas.append(f"valor: Excel={e_valor:,.0f} app={a['cuota']:,.0f}")
        if abs(e_saldo - a["saldo_final"]) > TOLERANCIA:
            problemas.append(f"saldo final: Excel={e_saldo:,.0f} app={a['saldo_final']:,.0f}")
        if problemas:
            difs.append(f"{s['placa']} ({s['cliente']}): " + "; ".join(problemas))
        else:
            coinciden += 1
    solo_app = [f"{a['placa']} {a['cliente']} saldo={a['saldo_final']:,.0f}" for k, a in app.items() if k not in vistos]
    return {"coinciden": coinciden, "diferencias": difs, "solo_excel": solo_excel, "solo_app": solo_app}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--excel", type=Path, required=True)
    ap.add_argument("--mes", help="AAAA-MM; por defecto el último bloque del Excel")
    ap.add_argument("--todos", action="store_true")
    args = ap.parse_args()

    import app.main  # noqa: F401
    from app.database.database import SessionLocal

    _, _, snapshots = CreemosParser(args.excel).parse_all()
    bloques: dict[str, list[dict]] = {}
    for s in snapshots:
        bloques.setdefault(s["mes_reportado"], []).append(s)
    etiquetas = list(bloques)
    if args.mes:
        y, m = map(int, args.mes.split("-"))
        etiquetas = [e for e in etiquetas if _anio_mes(e) == (y, m)]
    elif not args.todos:
        etiquetas = etiquetas[-1:]

    db = SessionLocal()
    try:
        total_difs = 0
        for e in etiquetas:
            r = conciliar_mes(db, bloques[e], *_anio_mes(e))
            total_difs += len(r["diferencias"])
            print(f"\n=== {e}: {r['coinciden']} coinciden, {len(r['diferencias'])} con diferencias, "
                  f"{len(r['solo_excel'])} solo en Excel, {len(r['solo_app'])} solo en la app")
            for linea in r["diferencias"]:
                print(f"  ≠ {linea}")
            for linea in r["solo_excel"]:
                print(f"  Excel sin préstamo en la app: {linea}")
            for linea in r["solo_app"]:
                print(f"  App sin fila en el Excel: {linea}")
        print(f"\nTotal diferencias: {total_difs}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
