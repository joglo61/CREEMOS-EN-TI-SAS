from __future__ import annotations
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.models.prestamo import Prestamo
from app.models.cliente import Cliente


class PrestamoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, prestamo_id: int) -> Prestamo | None:
        return self.db.query(Prestamo).options(joinedload(Prestamo.cliente)).filter(Prestamo.id == prestamo_id).first()

    def list(
        self, term: str = "", estado: str = "", cliente_id: int | None = None,
        page: int = 1, page_size: int = 25,
    ) -> tuple[list[Prestamo], int]:
        q = self.db.query(Prestamo).options(joinedload(Prestamo.cliente))
        if estado:
            q = q.filter(Prestamo.estado == estado.upper())
        if cliente_id:
            q = q.filter(Prestamo.cliente_id == cliente_id)
        if term:
            like = f"%{term}%"
            q = q.join(Cliente).filter(
                or_(Cliente.placa.like(like), Cliente.nombre.ilike(like), Cliente.cedula.like(like))
            )
        total = q.count()
        items = q.order_by(Prestamo.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def create(self, prestamo: Prestamo) -> Prestamo:
        self.db.add(prestamo)
        self.db.flush()
        return prestamo

    def update(self, prestamo: Prestamo) -> Prestamo:
        self.db.flush()
        return prestamo

    def get_by_cliente(self, cliente_id: int) -> list[Prestamo]:
        return self.db.query(Prestamo).options(joinedload(Prestamo.cliente)).filter(Prestamo.cliente_id == cliente_id).order_by(Prestamo.id.desc()).all()
