"""Motor financiero: intereses, mora, abono a capital, saldo, factura y prÃ³xima fecha.

Escenario base: capital $30.000.000, cuota $1.200.000, tasa 2.5 % mensual,
vencimiento 15-feb-2026 â†’ interÃ©s de 30 dÃ­as = 30.000.000 Ã— 2.5 % = $750.000.
Mora (como cobra la empresa): VALOR PAGADO Ã— tasa Ã· 30 Ã— dÃ­as de mora, solo desde 5 dÃ­as.
"""
from datetime import date
from decimal import Decimal

import pytest

from app.database.database import SessionLocal
from app.models.configuracion import Configuracion
from app.models.factura import Factura
from app.models.prestamo import Prestamo
from app.services.cliente_service import ClienteService
from app.services.pago_service import PagoService

D = Decimal


@pytest.fixture
def db():
    s = SessionLocal()
    yield s
    s.close()


def _prestamo(db, capital=30_000_000, cuota=1_200_000, primer_pago=date(2026, 2, 15), sufijo="1") -> Prestamo:
    res = ClienteService(db).crear(
        nombre=f"Cliente {sufijo}", cedula=f"100{sufijo}", placa=f"AAA{sufijo}",
        telefono=None, direccion=None, correo=None, observaciones=None,
        capital_inicial=D(capital), valor_cuota=D(cuota),
        fecha_inicio=date(2026, 1, 15), fecha_primer_pago=primer_pago,
    )
    return res["prestamo"]


def _calc(db, prestamo, valor, fecha, **kw):
    return PagoService(db).calcular(prestamo.id, D(valor), fecha, **kw)


def test_pago_a_tiempo_cuota_exacta(db):
    p = _prestamo(db)
    r = _calc(db, p, 1_200_000, date(2026, 2, 15))
    assert r["intereses"] == D(750_000)
    assert r["intereses_mora"] == 0
    assert r["dias_mora"] == 0
    assert r["dias_calculados"] == 30
    assert r["capital"] == D(450_000)
    assert r["saldo_nuevo"] == D(29_550_000)


def test_mora_menor_a_5_dias_no_se_cobra(db):
    p = _prestamo(db)
    r = _calc(db, p, 1_200_000, date(2026, 2, 18))  # 3 dÃ­as tarde
    assert r["dias_mora"] == 3
    assert r["dias_calculados"] == 33
    assert r["intereses_mora"] == 0
    assert r["capital"] == D(450_000)


def test_mora_desde_5_dias_sobre_valor_pagado(db):
    p = _prestamo(db)
    r = _calc(db, p, 1_200_000, date(2026, 2, 22))  # 7 dÃ­as tarde
    # 1.200.000 Ã— 2.5 % Ã· 30 Ã— 7 = 7.000
    assert r["intereses_mora"] == D(7_000)
    assert r["intereses_totales"] == D(757_000)
    assert r["capital"] == D(443_000)
    assert r["saldo_nuevo"] == D(29_557_000)


def test_pago_menor_a_intereses_no_abona_capital(db):
    p = _prestamo(db)
    r = _calc(db, p, 500_000, date(2026, 2, 15))
    assert r["intereses"] == D(500_000)
    assert r["capital"] == 0
    assert r["saldo_nuevo"] == D(30_000_000)


def test_pago_cubre_interes_pero_no_toda_la_mora(db):
    p = _prestamo(db)
    r = _calc(db, p, 752_000, date(2026, 2, 22))
    assert r["intereses"] == D(750_000)
    assert r["intereses_mora"] == D(2_000)
    assert r["capital"] == 0
    assert r["saldo_nuevo"] == D(30_000_000)


def test_pago_superior_abona_todo_a_capital(db):
    p = _prestamo(db)
    r = _calc(db, p, 5_000_000, date(2026, 2, 15))
    assert r["intereses"] == D(750_000)
    assert r["capital"] == D(4_250_000)
    assert r["saldo_nuevo"] == D(25_750_000)


def test_sin_interes_todo_va_a_capital(db):
    p = _prestamo(db)
    r = _calc(db, p, 1_200_000, date(2026, 2, 15), aplicar_interes=False)
    assert r["intereses"] == 0
    assert r["capital"] == D(1_200_000)
    assert r["tasa_interes_aplicada"] == 0


def test_tasa_personalizada(db):
    p = _prestamo(db)
    r = _calc(db, p, 1_200_000, date(2026, 2, 15), tasa_interes=D("2"))
    assert r["intereses"] == D(600_000)


def test_fecha_anterior_al_periodo_se_rechaza(db):
    p = _prestamo(db)
    with pytest.raises(ValueError):
        _calc(db, p, 1_200_000, date(2026, 1, 1))


def test_registrar_actualiza_prestamo_factura_y_consecutivo(db):
    p = _prestamo(db)
    svc = PagoService(db)
    r1 = svc.registrar(p.id, D(1_200_000), date(2026, 2, 15), usuario_id=1)
    r2 = svc.registrar(p.id, D(1_200_000), date(2026, 3, 15), usuario_id=1)

    assert r1["pago"].numero_factura == "FACT-000001"
    assert r2["pago"].numero_factura == "FACT-000002"
    assert db.query(Factura).count() == 2
    assert db.query(Configuracion).first().siguiente_factura == 3

    db.refresh(p)
    # 2Âº pago: 29.550.000 Ã— 2.5 % = 738.750 â†’ capital 461.250
    assert r2["pago"].intereses == D(738_750)
    assert p.saldo_actual == D(29_550_000 - 461_250)
    assert p.fecha_proximo_pago == date(2026, 4, 15)
    assert p.estado == "ACTIVO"


def test_proxima_fecha_fin_de_mes(db):
    p = _prestamo(db, primer_pago=date(2026, 1, 31))
    PagoService(db).registrar(p.id, D(1_200_000), date(2026, 1, 31), usuario_id=1)
    db.refresh(p)
    assert p.fecha_proximo_pago == date(2026, 2, 28)
    # Al mes siguiente vuelve al día 31 (no se queda en 28)
    PagoService(db).registrar(p.id, D(1_200_000), date(2026, 2, 28), usuario_id=1)
    db.refresh(p)
    assert p.fecha_proximo_pago == date(2026, 3, 31)


def test_recibo_pdf_una_pagina_con_copias_y_firma(db, tmp_path, monkeypatch):
    import re
    from app.core.config import settings
    from app.services.pdf_service import generar_recibo

    from reportlab import rl_config
    monkeypatch.setattr(rl_config, "pageCompression", 0)  # texto legible en el PDF
    monkeypatch.setattr(settings, "RECIBOS_DIR", str(tmp_path))
    p = _prestamo(db)
    r = PagoService(db).registrar(p.id, D(1_200_000), date(2026, 2, 22), usuario_id=1)
    ruta = generar_recibo(db, r["factura"])
    pdf = open(ruta, "rb").read()
    assert len(re.findall(rb"/Type\s*/Page[^s]", pdf)) == 1  # ambas copias en una hoja
    texto = pdf.decode("latin-1")
    for s in ("COPIA CLIENTE", "COPIA CONTABILIDAD", "Observaciones", "$757.000"):  # intereses = normal + mora
        assert s in texto, s
    assert "Firma y Sello" not in texto


def test_pago_que_cancela_deuda_marca_pagado_y_bloquea_nuevos_pagos(db):
    p = _prestamo(db, capital=1_000_000, cuota=100_000)
    svc = PagoService(db)
    r = svc.registrar(p.id, D(2_000_000), date(2026, 2, 15), usuario_id=1)
    assert r["pago"].capital == D(1_000_000)  # nunca abona mÃ¡s que el saldo
    assert r["pago"].saldo_nuevo == 0
    db.refresh(p)
    assert p.estado == "PAGADO"
    with pytest.raises(ValueError):
        svc.calcular(p.id, D(100_000), date(2026, 3, 15))


def test_cronograma_estimado(db):
    res = ClienteService(db).crear(
        nombre="Crono", cedula="555", placa="CRO555", telefono=None, direccion=None,
        correo=None, observaciones=None, capital_inicial=D(1_000_000), valor_cuota=D(100_000),
        fecha_inicio=date(2026, 1, 15), fecha_primer_pago=date(2026, 2, 15),
    )
    c = res["cronograma"]
    assert c[0].interes_estimado == D(25_000)
    assert c[0].capital_estimado == D(75_000)
    assert c[0].saldo_estimado == D(925_000)
    assert c[1].fecha_estimada == date(2026, 3, 15)
    assert c[-1].saldo_estimado == 0
    assert sum(x.capital_estimado for x in c) == D(1_000_000)
