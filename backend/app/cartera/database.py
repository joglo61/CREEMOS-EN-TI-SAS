import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.cartera.models import BaseCartera

CARTERA_DB_DIR = Path(__file__).resolve().parent.parent.parent / "database"
CARTERA_DB_PATH = CARTERA_DB_DIR / "cartera.db"


class CarteraDatabase:
    def __init__(self, db_path=None):
        self.db_path = db_path or CARTERA_DB_PATH
        os.makedirs(self.db_path.parent, exist_ok=True)
        self.engine = create_engine(
            f"sqlite:///{self.db_path}",
            connect_args={"check_same_thread": False},
            echo=False,
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def init_db(self):
        BaseCartera.metadata.create_all(bind=self.engine)

    def get_session(self):
        return self.SessionLocal()


_default_db = None


def get_cartera_db():
    global _default_db
    if _default_db is None:
        _default_db = CarteraDatabase()
        _default_db.init_db()
    return _default_db


def get_cartera_session():
    return get_cartera_db().get_session()
