from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.config import ConfigUpdate, ConfigResponse
from app.schemas.common import SuccessResponse
from app.security.auth import get_current_user, require_admin
from app.models.usuario import Usuario
from app.models.configuracion import Configuracion
from app.models.log import Log

router = APIRouter(prefix="/api/v1/config", tags=["Configuracion"])


@router.get("")
def obtener_config(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    config = db.query(Configuracion).first()
    if not config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuración no encontrada.")
    return SuccessResponse(data=ConfigResponse.model_validate(config).model_dump())


@router.put("")
def actualizar_config(
    request: Request,
    data: ConfigUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    config = db.query(Configuracion).first()
    if not config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuración no encontrada.")
    updates = data.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay campos para actualizar.")
    for k, v in updates.items():
        setattr(config, k, v)
    db.flush()
    log = Log(
        usuario_id=current_user.id, accion="EDITAR_CONFIGURACION", modulo="Configuracion",
        descripcion=f"Configuración actualizada: {', '.join(updates.keys())}.",
        direccion_ip=request.client.host if request.client else None,
    )
    db.add(log)
    db.commit()
    return SuccessResponse(message="Configuración actualizada correctamente.", data=ConfigResponse.model_validate(config).model_dump())
