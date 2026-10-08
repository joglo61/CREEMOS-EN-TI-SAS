"""Cartera mensual (reemplazo del bloque CXCOBRAR): saldos por mes desde los pagos."""
from datetime import date
from decimal import Decimal as D

import pytest

from app.database.database import SessionLocal
from app.services.cartera_mensual import cartera_del_mes
from app.services.cliente_service import ClienteService
from app.services.pago_service import PagoService


@pytest.fixture
def db():
    s = SessionLocal()
    yield s
    s.close()


def _prestamo(db, placa, capital, cuota, inicio, primer_pago):
    return ClienteService(db).crear(
        nombre=f"CLIENTE {placa}", cedula=placa, placa=placa, telefono=None, direccion=None, correo=None,
        observaciones=None, capital_inicial=D(capital), valor_cuota=D(cuota),
        fecha_inicio=inicio, fecha_primer_pago=primer_pago)["prestamo"]


def test_cartera_por_mes(db):
    a = _prestamo(db, "AAA001", 30_000_000, 1_200_000, date(2026, 1, 15), date(2026, 2, 15))
    _prestamo(db, "BBB002", 10_000_000, 500_000, date(2026, 1, 20), date(2026, 2, 20))  # nunca paga
    svc = PagoService(db)
    svc.registrar(a.id, D(1_200_000), date(2026, 2, 15), usuario_id=1)   # feb: 750.000 int + 450.000 cap
    svc.registrar(a.id, D(1_200_000), date(2026, 3, 22), usuario_id=1)   # mar: 7 días de mora

    feb = cartera_del_mes(db, 2026, 2)
    fa = next(f for f in feb["items"] if f["placa"] == "AAA001")
    assert fa["pago_en_mes"] and fa["saldo_anterior"] == D(30_000_000) and fa["saldo_final"] == D(29_550_000)
    assert fa["intereses"] == D(750_000) and fa["abono_capital"] == D(450_000)
    fb = next(f for f in feb["items"] if f["placa"] == "BBB002")
    assert not fb["pago_en_mes"] and fb["saldo_final"] == D(10_000_000)
    assert feb["totales"]["recaudo"] == D(1_200_000)
    assert feb["totales"]["saldo_final"] == D(29_550_000 + 10_000_000)
    assert feb["totales"]["pagaron"] == 1 and feb["totales"]["creditos"] == 2

    mar = cartera_del_mes(db, 2026, 3)
    fa = next(f for f in mar["items"] if f["placa"] == "AAA001")
    assert fa["saldo_anterior"] == D(29_550_000)  # arrastra el saldo de febrero
    assert fa["interes_mora"] > 0
    assert mar["totales"]["abono_intereses"] == fa["intereses"] + fa["interes_mora"]

    # Enero: ambos recién desembolsados, nadie pagó
    ene = cartera_del_mes(db, 2026, 1)
    assert ene["totales"]["recaudo"] == 0 and all(f["alta"] for f in ene["items"])
    # Diciembre 2025: aún no existían
    assert cartera_del_mes(db, 2025, 12)["items"] == []


def test_credito_saldado_sale_de_la_cartera(db):
    p = _prestamo(db, "CCC003", 1_000_000, 100_000, date(2026, 1, 1), date(2026, 2, 1))
    PagoService(db).registrar(p.id, D(2_000_000), date(2026, 2, 1), usuario_id=1)
    assert any(f["placa"] == "CCC003" for f in cartera_del_mes(db, 2026, 2)["items"])  # el mes que pagó
    assert not any(f["placa"] == "CCC003" for f in cartera_del_mes(db, 2026, 3)["items"])


def test_endpoint_y_excel(client):
    r = client.get("/api/v1/reportes/cartera-mensual?anio=2026&mes=2")
    assert r.status_code == 200 and r.json()["data"]["mes"] == "FEBRERO DE 2026"
    x = client.get("/api/v1/reportes/cartera-mensual/excel?anio=2026&mes=2")
    assert x.status_code == 200 and x.content[:2] == b"PK"
