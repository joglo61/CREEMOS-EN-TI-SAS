from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioPasswordChange, UsuarioResponse
from app.schemas.common import SuccessResponse
from app.repositories.usuario_repository import UsuarioRepository
from app.security.auth import hash_password, get_current_user, require_admin
from app.models.usuario import Usuario
from app.models.log import Log

router = APIRouter(prefix="/api/v1/usuarios", tags=["Usuarios"])


@router.get("")
def listar_usuarios(
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    repo = UsuarioRepository(db)
    usuarios = repo.get_all()
    return SuccessResponse(data={
        "items": [UsuarioResponse.model_validate(u).model_dump() for u in usuarios],
    })


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_usuario(
    request: Request,
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    repo = UsuarioRepository(db)
    existente = repo.get_by_usuario(data.usuario)
    if existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El nombre de usuario ya existe.")
    usuario = Usuario(
        nombre=data.nombre, usuario=data.usuario,
        password_hash=hash_password(data.password), rol=data.rol, activo=True,
    )
    repo.create(usuario)
    log = Log(
        usuario_id=current_user.id, accion="CREAR_USUARIO", modulo="Usuarios",
        descripcion=f"Usuario {data.usuario} ({data.rol}) creado.",
        direccion_ip=request.client.host if request.client else None,
    )
    db.add(log)
    db.commit()
    return SuccessResponse(message="Usuario creado correctamente.", data=UsuarioResponse.model_validate(usuario).model_dump())


@router.put("/{usuario_id}")
def actualizar_usuario(
    request: Request,
    usuario_id: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    repo = UsuarioRepository(db)
    usuario = repo.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
    updates = data.model_dump(exclude_none=True)
    for k, v in updates.items():
        setattr(usuario, k, v)
    repo.update(usuario)
    log = Log(
        usuario_id=current_user.id, accion="EDITAR_USUARIO", modulo="Usuarios",
        descripcion=f"Usuario {usuario.usuario} actualizado: {', '.join(updates.keys())}.",
        direccion_ip=request.client.host if request.client else None,
    )
    db.add(log)
    db.commit()
    return SuccessResponse(message="Usuario actualizado correctamente.", data=UsuarioResponse.model_validate(usuario).model_dump())


@router.post("/{usuario_id}/cambiar-password")
def cambiar_password(
    request: Request,
    usuario_id: int,
    data: UsuarioPasswordChange,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    repo = UsuarioRepository(db)
    usuario = repo.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
    usuario.password_hash = hash_password(data.password)
    repo.update(usuario)
    log = Log(
        usuario_id=current_user.id, accion="CAMBIAR_PASSWORD", modulo="Usuarios",
        descripcion=f"Contraseña cambiada para usuario {usuario.usuario}.",
        direccion_ip=request.client.host if request.client else None,
    )
    db.add(log)
    db.commit()
    return SuccessResponse(message="Contraseña actualizada correctamente.")


@router.post("/{usuario_id}/desbloquear")
def desbloquear_usuario(
    request: Request,
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    repo = UsuarioRepository(db)
    usuario = repo.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
    usuario.intentos_fallidos = 0
    usuario.bloqueado_hasta = None
    repo.update(usuario)
    log = Log(
        usuario_id=current_user.id, accion="DESBLOQUEAR_USUARIO", modulo="Usuarios",
        descripcion=f"Usuario {usuario.usuario} desbloqueado.",
        direccion_ip=request.client.host if request.client else None,
    )
    db.add(log)
    db.commit()
    return SuccessResponse(message="Usuario desbloqueado correctamente.", data=UsuarioResponse.model_validate(usuario).model_dump())
