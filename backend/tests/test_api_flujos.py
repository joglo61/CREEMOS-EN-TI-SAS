"""Flujos por API: validaciones, cliente duplicado, pago → factura, estado de mora y roles."""
from datetime import date, timedelta

from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.models.prestamo import Prestamo
from app.models.usuario import Usuario
from app.security.auth import hash_password


def _cliente(client, sufijo="1", primer_pago=None):
    hoy = date.today()
    r = client.post("/api/v1/clientes", json={
        "nombre": f"Cliente API {sufijo}", "cedula": f"200{sufijo}", "placa": f"API{sufijo}",
        "capital_inicial": 10_000_000, "valor_cuota": 500_000,
        "fecha_inicio": str(hoy - timedelta(days=30)),
        "fecha_primer_pago": str(primer_pago or hoy),
    })
    assert r.status_code == 201, r.text
    cid = r.json()["data"]["cliente"]["id"]
    db = SessionLocal()
    pid = db.query(Prestamo).filter(Prestamo.cliente_id == cid).first().id
    db.close()
    return cid, pid


def test_cedula_y_placa_duplicadas_se_rechazan(client):
    _cliente(client, "1")
    base = {"nombre": "Otro", "capital_inicial": 1, "valor_cuota": 1, "fecha_inicio": str(date.today())}
    assert client.post("/api/v1/clientes", json={**base, "cedula": "2001", "placa": "NUEVA"}).status_code == 409
    assert client.post("/api/v1/clientes", json={**base, "cedula": "NUEVA", "placa": "API1"}).status_code == 409


def test_pago_cero_o_negativo_se_rechaza(client):
    _, pid = _cliente(client)
    for valor in (0, -1000):
        r = client.post("/api/v1/pagos/registrar", json={"prestamo_id": pid, "valor_pagado": valor, "fecha_pago": str(date.today())})
        assert r.status_code == 422


def test_registrar_pago_genera_factura_consultable(client):
    _, pid = _cliente(client)
    r = client.post("/api/v1/pagos/registrar", json={"prestamo_id": pid, "valor_pagado": 500_000, "fecha_pago": str(date.today())})
    assert r.status_code == 201, r.text
    data = r.json()["data"]
    assert data["factura"] == "FACT-000001"
    assert data["pago"]["intereses"] == "250000"  # 10.000.000 × 2.5 %
    assert data["pago"]["saldo_nuevo"] == "9750000"

    f = client.get(f"/api/v1/facturas/{data['factura_id']}")
    assert f.status_code == 200
    assert client.get(f"/api/v1/pagos?prestamo_id={pid}").json()["data"]["total"] == 1


def test_estado_mora_respeta_dias_de_gracia(client):
    hoy = date.today()
    _, pid_gracia = _cliente(client, "1", primer_pago=hoy - timedelta(days=5))
    _, pid_mora = _cliente(client, "2", primer_pago=hoy - timedelta(days=6))
    assert client.post(f"/api/v1/prestamos/{pid_gracia}/actualizar-estado").json()["data"]["estado"] == "ACTIVO"
    assert client.post(f"/api/v1/prestamos/{pid_mora}/actualizar-estado").json()["data"]["estado"] == "MORA"


def test_empleado_no_administra_usuarios_pero_si_registra_pagos(client):
    _, pid = _cliente(client)
    db = SessionLocal()
    db.add(Usuario(nombre="Empleado", usuario="empleado_test", password_hash=hash_password("Test1234"), rol="EMPLEADO", activo=True))
    db.commit()
    db.close()

    from app.main import app
    with TestClient(app) as emp:
        tok = emp.post("/api/v1/auth/login", json={"usuario": "empleado_test", "password": "Test1234"}).json()["data"]["access_token"]
        emp.headers["Authorization"] = f"Bearer {tok}"
        assert emp.get("/api/v1/usuarios").status_code == 403
        assert emp.post("/api/v1/usuarios", json={"nombre": "X", "usuario": "xxx", "password": "123456"}).status_code == 403
        r = emp.post("/api/v1/pagos/registrar", json={"prestamo_id": pid, "valor_pagado": 500_000, "fecha_pago": str(date.today())})
        assert r.status_code == 201


def test_sin_token_no_hay_acceso(client):
    from app.main import app
    anon = TestClient(app)
    for path in ("/api/v1/clientes", "/api/v1/pagos", "/api/v1/facturas", "/api/v1/dashboard"):
        assert anon.get(path).status_code in (401, 403), path
