from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class ConfigUpdate(BaseModel):
    empresa: Optional[str] = Field(None, min_length=1, max_length=200)
    nit: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=300)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[str] = Field(None, max_length=100)
    logo: Optional[str] = Field(None, max_length=500)
    tasa_interes: Optional[Decimal] = Field(None, ge=0, le=100)
    dias_gracia: Optional[int] = Field(None, ge=0, le=365)
    siguiente_factura: Optional[int] = Field(None, ge=1)
    ruta_recibos: Optional[str] = Field(None, max_length=500)
    ruta_backups: Optional[str] = Field(None, max_length=500)


class ConfigResponse(BaseModel):
    id: int
    empresa: str
    nit: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    logo: Optional[str] = None
    tasa_interes: Decimal
    dias_gracia: int
    siguiente_factura: int
    ruta_recibos: str
    ruta_backups: str

    class Config:
        from_attributes = True
