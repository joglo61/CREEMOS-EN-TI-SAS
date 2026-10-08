from datetime import datetime, timedelta, timezone
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse, UserInfo
from app.schemas.common import SuccessResponse
from app.security.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from app.repositories.usuario_repository import UsuarioRepository
from app.services.log_service import crear_log
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])

_login_attempts: dict[str, list[datetime]] = defaultdict(list)
_LOGIN_RATE_LIMIT = 30
_LOGIN_RATE_WINDOW = 60


def _check_login_rate(ip: str):
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(seconds=_LOGIN_RATE_WINDOW)
    attempts = [t for t in _login_attempts[ip] if t > window_start]
    _login_attempts[ip] = attempts
    if len(attempts) >= _LOGIN_RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Demasiados intentos. Intente de nuevo en un minuto.",
        )
    attempts.append(now)


@router.post("/login", response_model=SuccessResponse)
def login(request: Request, data: LoginRequest, db: Session = Depends(get_db)):
    ip = request.client.host if request.client else "unknown"
    _check_login_rate(ip)
    repo = UsuarioRepository(db)
    usuario = repo.get_by_usuario(data.usuario)
    ip = request.client.host if request.client else None
    ahora = datetime.now(timezone.utc)

    if not usuario or not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
        )

    if usuario.bloqueado_hasta and usuario.bloqueado_hasta.replace(tzinfo=timezone.utc) > ahora:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
        )

    if not verify_password(data.password, usuario.password_hash):
        usuario.intentos_fallidos = (usuario.intentos_fallidos or 0) + 1
        if usuario.intentos_fallidos >= 3:
            usuario.bloqueado_hasta = datetime.now(timezone.utc) + timedelta(minutes=30)
        repo.update(usuario)
        crear_log(db, usuario.id, "INTENTO_FALLIDO", "Autenticación",
                  f"Intento fallido #{usuario.intentos_fallidos} para {usuario.usuario}.", ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
        )

    usuario.intentos_fallidos = 0
    usuario.bloqueado_hasta = None
    usuario.ultimo_acceso = None
    repo.update(usuario)

    crear_log(db, usuario.id, "INICIO_SESION", "Autenticación", f"Usuario {usuario.usuario} inició sesión.", ip)

    return SuccessResponse(
        message="Inicio de sesión exitoso.",
        data=TokenResponse(
            access_token=create_access_token({"sub": str(usuario.id)}),
            usuario=usuario.usuario,
            nombre=usuario.nombre,
            rol=usuario.rol,
        ),
    )


@router.post("/logout", response_model=SuccessResponse)
def logout(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    crear_log(db, current_user.id, "CIERRE_SESION", "Autenticación", f"Usuario {current_user.usuario} cerró sesión.", None)
    return SuccessResponse(message="Sesión cerrada correctamente.")


@router.get("/me", response_model=SuccessResponse)
def get_me(current_user: Usuario = Depends(get_current_user)):
    return SuccessResponse(
        data=UserInfo(
            id=current_user.id,
            usuario=current_user.usuario,
            nombre=current_user.nombre,
            rol=current_user.rol,
            activo=current_user.activo,
        )
    )
