from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class ClienteCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    cedula: str = Field(..., min_length=1, max_length=20)
    placa: str = Field(..., min_length=1, max_length=20)
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=300)
    correo: Optional[str] = Field(None, max_length=100)
    observaciones: Optional[str] = None

    capital_inicial: Decimal = Field(..., gt=0)
    valor_cuota: Decimal = Field(..., gt=0)
    fecha_inicio: date
    fecha_primer_pago: Optional[date] = None


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=300)
    correo: Optional[str] = Field(None, max_length=100)
    observaciones: Optional[str] = None


class ClienteResponse(BaseModel):
    id: int
    nombre: str
    cedula: str
    placa: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    correo: Optional[str] = None
    estado: str
    observaciones: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CronogramaEntry(BaseModel):
    id: int
    numero_cuota: int
    fecha_estimada: date
    capital_estimado: Decimal
    interes_estimado: Decimal
    valor_estimado: Decimal
    saldo_estimado: Decimal
    estado: str

    class Config:
        from_attributes = True


class HistorialEntry(BaseModel):
    id: int
    accion: str
    modulo: str | None = None
    descripcion: str | None = None
    usuario: str | None = None
    created_at: str | None = None


class ClienteDetailResponse(ClienteResponse):
    prestamo: Optional[dict] = None
    historial: list = []
