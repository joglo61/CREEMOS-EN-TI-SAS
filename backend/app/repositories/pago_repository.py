from __future__ import annotations
from sqlalchemy.orm import Session, joinedload
from app.models.pago import Pago
from app.models.prestamo import Prestamo


class PagoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, pago_id: int) -> Pago | None:
        return self.db.query(Pago).options(joinedload(Pago.prestamo), joinedload(Pago.usuario)).filter(Pago.id == pago_id).first()

    def list(self, prestamo_id: int | None = None, page: int = 1, page_size: int = 50) -> tuple[list[Pago], int]:
        q = self.db.query(Pago).options(joinedload(Pago.prestamo), joinedload(Pago.usuario))
        if prestamo_id:
            q = q.filter(Pago.prestamo_id == prestamo_id)
        total = q.count()
        items = q.order_by(Pago.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def create(self, pago: Pago) -> Pago:
        self.db.add(pago)
        self.db.flush()
        return pago

    def get_ultimo_pago(self, prestamo_id: int) -> Pago | None:
        return self.db.query(Pago).filter(Pago.prestamo_id == prestamo_id).order_by(Pago.id.desc()).first()
