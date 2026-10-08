from __future__ import annotations
import os
import shutil
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.core.config import settings
from app.schemas.common import SuccessResponse
from app.security.auth import get_current_user, require_admin
from app.models.usuario import Usuario
from app.models.backup import Backup
from app.models.log import Log


def _get_db_path() -> str:
    raw = settings.DATABASE_URL.replace("sqlite:///", "")
    if not os.path.isabs(raw):
        raw = os.path.normpath(os.path.join(os.getcwd(), raw))
    return raw

router = APIRouter(prefix="/api/v1/backups", tags=["Backups"])


@router.post("/crear")
def crear_backup(
    request: Request,
    tipo: str = "completo",
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    os.makedirs(settings.BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    if tipo in ("completo", "base_datos"):
        db_path = _get_db_path()
        if os.path.exists(db_path):
            backup_name = f"db_{ts}.sqlite3"
            backup_path = os.path.join(settings.BACKUP_DIR, backup_name)
            shutil.copy2(db_path, backup_path)
            b = Backup(tipo="base_datos", archivo=backup_name, ruta=backup_path,
                       tamano=os.path.getsize(backup_path), usuario_id=current_user.id)
            db.add(b)

    if tipo in ("completo", "config"):
        from app.models.configuracion import Configuracion
        cfg_data = db.query(Configuracion).first()
        if cfg_data:
            import json
            cfg_dict = {c.name: str(getattr(cfg_data, c.name, "")) for c in Configuracion.__table__.columns}
            cfg_name = f"config_{ts}.json"
            cfg_path = os.path.join(settings.BACKUP_DIR, cfg_name)
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(cfg_dict, f, ensure_ascii=False, indent=2)
            b = Backup(tipo="config", archivo=cfg_name, ruta=cfg_path,
                       tamano=os.path.getsize(cfg_path), usuario_id=current_user.id)
            db.add(b)

    log = Log(
        usuario_id=current_user.id, accion="CREAR_BACKUP", modulo="Backups",
        descripcion=f"Backup {tipo} creado.",
        direccion_ip=request.client.host if request.client else None,
    )
    db.add(log)
    db.commit()
    return SuccessResponse(message=f"Backup {tipo} creado correctamente.")


@router.get("")
def listar_backups(
    tipo: str = "",
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    q = db.query(Backup).order_by(Backup.id.desc())
    if tipo:
        q = q.filter(Backup.tipo == tipo)
    items = q.limit(100).all()
    return SuccessResponse(data={
        "items": [{
            "id": b.id, "tipo": b.tipo, "archivo": b.archivo,
            "tamano": b.tamano, "fecha": str(b.created_at) if b.created_at else None,
            "usuario": b.usuario.nombre if b.usuario else "",
        } for b in items]
    })


@router.post("/restaurar/{backup_id}")
def restaurar_backup(
    request: Request,
    backup_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    backup = db.query(Backup).filter(Backup.id == backup_id).first()
    if not backup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Backup no encontrado.")
    if not os.path.exists(backup.ruta):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El archivo de backup no existe.")

    if backup.tipo == "base_datos":
        db_path = _get_db_path()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        pre_restore = os.path.join(settings.BACKUP_DIR, f"pre_restore_{ts}.sqlite3")
        shutil.copy2(db_path, pre_restore)
        b2 = Backup(tipo="base_datos", archivo=f"pre_restore_{ts}.sqlite3",
                    ruta=pre_restore, tamano=os.path.getsize(pre_restore),
                    usuario_id=current_user.id)
        db.add(b2)
        db.flush()
        shutil.copy2(backup.ruta, db_path)

    log = Log(
        usuario_id=current_user.id, accion="RESTAURAR_BACKUP", modulo="Backups",
        descripcion=f"Backup {backup.tipo} ({backup.archivo}) restaurado.",
        direccion_ip=request.client.host if request.client else None,
    )
    db.add(log)
    db.commit()
    return SuccessResponse(message=f"Backup {backup.tipo} restaurado correctamente. Se recomienda reiniciar la aplicación.")
