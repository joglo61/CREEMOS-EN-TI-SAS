from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class FacturaResponse(BaseModel):
    id: int
    numero_factura: str
    cliente_id: int
    pago_id: int
    fecha: date
    ruta_pdf: Optional[str] = None
    estado: str
    created_at: Optional[datetime] = None
    cliente_nombre: str = ""
    pago_valor: str = ""

    class Config:
        from_attributes = True
