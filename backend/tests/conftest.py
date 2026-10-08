import os
import tempfile
_db_fd, _db_path = tempfile.mkstemp(suffix='.db')
os.close(_db_fd)
os.environ['DATABASE_URL'] = 'sqlite:///' + _db_path.replace('\\', '/')
# No tocar Creemos.xlsx real ni logs/app.log durante los tests
os.environ['LOGS_DIR'] = tempfile.mkdtemp()

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.database import SessionLocal, engine, Base
from app.models import *  # noqa
from app.security.auth import hash_password
from app.models.usuario import Usuario
from app.models.configuracion import Configuracion


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    admin = Usuario(
        nombre="Admin Test",
        usuario="admin_test",
        password_hash=hash_password("Test1234"),
        rol="ADMINISTRADOR",
        activo=True,
    )
    db.add(admin)
    cfg = Configuracion(tasa_interes=2.5)
    db.add(cfg)
    db.commit()
    db.close()


def pytest_unconfigure():
    try:
        os.unlink(_db_path)
    except OSError:
        pass


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        r = c.post("/api/v1/auth/login", json={"usuario": "admin_test", "password": "Test1234"})
        token = r.json()["data"]["access_token"]
        c.headers.update({"Authorization": f"Bearer {token}"})
        yield c


@pytest.fixture(scope="function")
def auth_headers(client):
    return {"Authorization": client.headers["Authorization"]}
