import datetime

def _create_payload(suffix=""):
    today = datetime.date.today()
    return {
        "nombre": f"Cliente Test{suffix}",
        "cedula": f"999999{suffix}",
        "placa": f"TEST{suffix}",
        "telefono": "3001234567",
        "direccion": "Calle 123",
        "correo": "test@test.com",
        "capital_inicial": 1000000,
        "valor_cuota": 100000,
        "fecha_inicio": str(today),
        "fecha_primer_pago": str(today + datetime.timedelta(days=30)),
    }


def test_create_cliente(client):
    r = client.post("/api/v1/clientes", json=_create_payload("1"))
    assert r.status_code == 201
    assert r.json()["success"] is True


def test_list_clientes(client):
    r = client.get("/api/v1/clientes")
    assert r.status_code == 200
    assert "items" in r.json()["data"]


def test_get_cliente(client):
    cr = client.post("/api/v1/clientes", json=_create_payload("2"))
    assert cr.status_code == 201
    cid = cr.json()["data"]["cliente"]["id"]
    r = client.get(f"/api/v1/clientes/{cid}")
    assert r.status_code == 200


def test_update_cliente(client):
    cr = client.post("/api/v1/clientes", json=_create_payload("3"))
    assert cr.status_code == 201
    cid = cr.json()["data"]["cliente"]["id"]
    r = client.put(f"/api/v1/clientes/{cid}", json={"nombre": "New Name"})
    assert r.status_code == 200
    assert r.json()["data"]["nombre"] == "New Name"


def test_delete_cliente(client):
    cr = client.post("/api/v1/clientes", json=_create_payload("4"))
    assert cr.status_code == 201
    cid = cr.json()["data"]["cliente"]["id"]
    r = client.delete(f"/api/v1/clientes/{cid}")
    assert r.status_code == 200
