from sqlalchemy.orm import Session
from app.models.log import Log
from app.repositories.log_repository import LogRepository


class LogService:
    def __init__(self, db: Session):
        self.repo = LogRepository(db)

    def registrar(self, usuario_id: int | None, accion: str, modulo: str | None = None, descripcion: str | None = None, direccion_ip: str | None = None) -> Log:
        log = Log(
            usuario_id=usuario_id,
            accion=accion,
            modulo=modulo,
            descripcion=descripcion,
            direccion_ip=direccion_ip,
        )
        return self.repo.create(log)


def crear_log(db: Session, usuario_id: int | None, accion: str, modulo: str | None = None, descripcion: str | None = None, direccion_ip: str | None = None):
    service = LogService(db)
    return service.registrar(usuario_id, accion, modulo, descripcion, direccion_ip)
