from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.cliente import Cliente


class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, cliente_id: int) -> Cliente | None:
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def get_by_cedula(self, cedula: str) -> Cliente | None:
        return self.db.query(Cliente).filter(Cliente.cedula == cedula).first()

    def get_by_placa(self, placa: str) -> Cliente | None:
        return self.db.query(Cliente).filter(Cliente.placa == placa).first()

    def search(self, term: str = "", estado: str = "", page: int = 1, page_size: int = 25):
        query = self.db.query(Cliente)
        if term:
            like = f"%{term}%"
            query = query.filter(
                or_(
                    Cliente.nombre.ilike(like),
                    Cliente.placa.ilike(like),
                    Cliente.cedula.ilike(like),
                )
            )
        if estado:
            query = query.filter(Cliente.estado == estado)
        total = query.count()
        items = query.order_by(Cliente.nombre).offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def create(self, cliente: Cliente) -> Cliente:
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def update(self, cliente: Cliente) -> Cliente:
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def soft_delete(self, cliente: Cliente) -> Cliente:
        cliente.estado = "INACTIVO"
        return self.update(cliente)

    def hard_delete(self, cliente: Cliente) -> None:
        self.db.delete(cliente)
        self.db.commit()

    def toggle_estado(self, cliente: Cliente) -> Cliente:
        cliente.estado = "INACTIVO" if cliente.estado == "ACTIVO" else "ACTIVO"
        return self.update(cliente)
