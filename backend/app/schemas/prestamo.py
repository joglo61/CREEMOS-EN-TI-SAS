from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class PrestamoCreate(BaseModel):
    cliente_id: int = Field(..., gt=0)
    capital_inicial: Decimal = Field(..., gt=0)
    valor_cuota: Decimal = Field(..., gt=0)
    fecha_inicio: date
    fecha_primer_pago: Optional[date] = None


class PrestamoUpdate(BaseModel):
    valor_cuota: Optional[Decimal] = Field(None, gt=0)
    estado: Optional[str] = Field(None, pattern=r"^(ACTIVO|MORA|PAGADO|CANCELADO)$")


class PrestamoResponse(BaseModel):
    id: int
    cliente_id: int
    cliente_nombre: str = ""
    cliente_placa: str = ""
    capital_inicial: Decimal
    saldo_actual: Decimal
    valor_cuota: Decimal
    tasa_interes: Decimal
    fecha_inicio: date
    fecha_primer_pago: date
    fecha_proximo_pago: date
    estado: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
