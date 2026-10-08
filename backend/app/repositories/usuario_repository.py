from sqlalchemy.orm import Session
from app.models.usuario import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_usuario(self, usuario: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.usuario == usuario).first()

    def get_by_id(self, usuario_id: int) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def get_all(self) -> list[Usuario]:
        return self.db.query(Usuario).order_by(Usuario.nombre).all()

    def create(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def update(self, usuario: Usuario) -> Usuario:
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
