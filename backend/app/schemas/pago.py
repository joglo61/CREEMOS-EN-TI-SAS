from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class PagoRegistrar(BaseModel):
    prestamo_id: int = Field(..., gt=0)
    valor_pagado: Decimal = Field(..., gt=0)
    fecha_pago: date
    observaciones: Optional[str] = None
    aplicar_interes: bool = True
    tasa_interes: Optional[Decimal] = None


class PagoResponse(BaseModel):
    id: int
    prestamo_id: int
    numero_factura: str
    fecha_pago: date
    dias_calculados: int
    dias_mora: int
    saldo_anterior: Decimal
    intereses: Decimal
    intereses_mora: Decimal = Decimal("0")
    capital: Decimal
    valor_pagado: Decimal
    saldo_nuevo: Decimal
    observaciones: Optional[str] = None
    usuario_nombre: str = ""
    tasa_interes_aplicada: Optional[Decimal] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
