def test_login_success(client):
    r = client.post("/api/v1/auth/login", json={"usuario": "admin_test", "password": "Test1234"})
    assert r.status_code == 200
    data = r.json()
    assert data["success"] is True
    assert "access_token" in data["data"]


def test_login_invalid_password(client):
    r = client.post("/api/v1/auth/login", json={"usuario": "admin_test", "password": "wrong"})
    assert r.status_code == 401


def test_login_nonexistent_user(client):
    r = client.post("/api/v1/auth/login", json={"usuario": "no_existe", "password": "x"})
    assert r.status_code == 401


def test_me_endpoint(client):
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 200
    assert r.json()["data"]["usuario"] == "admin_test"


def test_me_unauthorized():
    from fastapi.testclient import TestClient
    from app.main import app
    c = TestClient(app)
    r = c.get("/api/v1/auth/me")
    assert r.status_code in (401, 403)
