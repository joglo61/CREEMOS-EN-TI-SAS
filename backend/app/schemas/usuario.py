from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    usuario: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)
    rol: str = Field(default="EMPLEADO", pattern=r"^(ADMINISTRADOR|EMPLEADO)$")


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=200)
    rol: Optional[str] = Field(None, pattern=r"^(ADMINISTRADOR|EMPLEADO)$")
    activo: Optional[bool] = None


class UsuarioPasswordChange(BaseModel):
    password: str = Field(..., min_length=6, max_length=100)


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    usuario: str
    rol: str
    activo: bool
    intentos_fallidos: int = 0
    bloqueado_hasta: Optional[datetime] = None
    ultimo_acceso: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
