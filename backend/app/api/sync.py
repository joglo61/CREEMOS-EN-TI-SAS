from __future__ import annotations
from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Query, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.common import SuccessResponse
from app.services.sync_service import SyncService
from app.security.auth import get_current_user
from app.models.usuario import Usuario
from app.models.log import Log
from app.cartera.sincronizador import SincronizadorCartera
from app.cartera.database import get_cartera_db, get_cartera_session

router = APIRouter(prefix="/api/v1/sync", tags=["Sincronizacion"])


@router.post("/sincronizar")
def sincronizar(
    request: Request,
    tipo: str = Query(..., pattern=r"^(clientes|financiero|cartera)$"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    if tipo == "cartera":
        try:
            from app.cartera.sincronizador import SincronizadorCartera
            sync = SincronizadorCartera()
            resultado = sync.ejecutar()
            from app.cartera.importar_a_sistema import importar_cartera_a_sistema
            importacion = importar_cartera_a_sistema(db, usuario_id=current_user.id)
            resultado["importados"] = importacion
            log = Log(
                usuario_id=current_user.id, accion="SINCRONIZAR_CARTERA", modulo="Cartera",
                descripcion=f"Sync: {resultado.get('creditos', 0)} créditos. Import: {importacion.get('clientes', 0)} clientes, {importacion.get('prestamos', 0)} préstamos, {importacion.get('pagos', 0)} pagos",
                direccion_ip=request.client.host if request.client else None,
            )
            db.add(log)
            db.commit()
            return SuccessResponse(message="Sincronización de cartera completada.", data=resultado)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    service = SyncService(db)
    try:
        service = SyncService(db)
        if tipo == "clientes":
            result = service.sincronizar_clientes(usuario_id=current_user.id)
        else:
            result = service.sincronizar_financiero(usuario_id=current_user.id)
        return SuccessResponse(message=f"Sincronización de {tipo} completada.", data=result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        import traceback, os
        tb = traceback.format_exc()
        os.makedirs("logs", exist_ok=True)
        with open("logs/sync_error.log", "a") as f:
            f.write(f"Sync error: {e}\n{tb}\n---\n")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/exportar-pagos")
def exportar_pagos(
    request: Request,
    dias: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = SyncService(db)
    fecha_desde = date.today() - timedelta(days=dias)
    try:
        filepath = service.exportar_pagos_a_excel(fecha_desde=fecha_desde)
        log = Log(
            usuario_id=current_user.id, accion="EXPORTAR_PAGOS_EXCEL", modulo="Sincronizacion",
            descripcion=f"Pagos exportados a Excel ({dias} días).",
            direccion_ip=request.client.host if request.client else None,
        )
        db.add(log)
        db.commit()
        return SuccessResponse(message=f"Pagos exportados a Excel.", data={"ruta": filepath})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/cartera")
def sincronizar_cartera(
    request: Request,
    dry_run: bool = Query(False),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        sync = SincronizadorCartera(dry_run=dry_run)
        resultado = sync.ejecutar()
        db = next(get_db())
        from app.cartera.importar_a_sistema import importar_cartera_a_sistema
        importacion = importar_cartera_a_sistema(db, usuario_id=current_user.id)
        resultado["importados"] = importacion
        log = Log(
            usuario_id=current_user.id, accion="SINCRONIZAR_CARTERA", modulo="Cartera",
            descripcion=f"Sync: {resultado.get('creditos', 0)} créditos. Import: {importacion.get('clientes', 0)} clientes, {importacion.get('prestamos', 0)} préstamos, {importacion.get('pagos', 0)} pagos",
            direccion_ip=request.client.host if request.client else None,
        )
        db.add(log)
        db.commit()
        db.close()
        return SuccessResponse(data=resultado)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/cartera/actualizar-excel")
def actualizar_excel_cartera(
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Botón 'Actualizar Excel': escribe pagos del sistema en Creemos.xlsx
    (bloque del mes + hojas individuales, con color), crea el bloque del mes
    si falta, recalcula con Excel COM y re-sincroniza hacia las bases."""
    from pathlib import Path
    from datetime import date as _date
    from app.cartera.excel_writer import (
        verificar_bloque_mes_actual, escribir_pagos, recalcular_excel,
    )
    from app.models.pago import Pago
    from app.models.prestamo import Prestamo
    from app.models.cliente import Cliente

    ruta = Path(__file__).resolve().parent.parent.parent.parent / "Creemos.xlsx"
    if not ruta.exists():
        raise HTTPException(status_code=404, detail="Creemos.xlsx no encontrado en la raíz del proyecto.")

    try:
        with open(str(ruta), "r+b"):
            pass
    except PermissionError:
        raise HTTPException(status_code=409, detail="Cierra Creemos.xlsx en Excel antes de actualizar.")

    try:
        # 1. Crear bloque del mes actual si falta (cierre de mes)
        bloque = verificar_bloque_mes_actual(str(ruta), db)

        # 2. Escribir pagos del sistema (FACT-*) al Excel
        pagos_sistema = (
            db.query(Pago, Prestamo, Cliente)
            .join(Prestamo, Pago.prestamo_id == Prestamo.id)
            .join(Cliente, Prestamo.cliente_id == Cliente.id)
            .filter(Pago.numero_factura.like("FACT-%"))
            .all()
        )
        pagos_data = [{
            "placa": cli.placa or "",
            "fecha_pago": p.fecha_pago,
            "valor_pagado": float(p.valor_pagado),
            "intereses_mora": float(p.intereses_mora or 0),
            "numero_factura": p.numero_factura,
            "dias": p.dias_calculados or 30,
            "intereses": float(p.intereses or 0),
            "capital": float(p.capital or 0),
            "saldo_nuevo": float(p.saldo_nuevo or 0),
        } for p, pre, cli in pagos_sistema]

        escritura = escribir_pagos(str(ruta), pagos_data) if pagos_data else {
            "escritos_bloque": 0, "escritos_hoja": 0, "omitidos": 0}

        # 3. Recalcular fórmulas con Excel COM
        recalcular_excel(str(ruta))

        # 4. Re-sincronizar Excel → bases
        sync = SincronizadorCartera()
        resultado = sync.ejecutar()
        from app.cartera.importar_a_sistema import importar_cartera_a_sistema
        importacion = importar_cartera_a_sistema(db, usuario_id=current_user.id)

        log = Log(
            usuario_id=current_user.id, accion="ACTUALIZAR_EXCEL_CARTERA", modulo="Cartera",
            descripcion=(
                f"Excel actualizado: {escritura['escritos_bloque']} pagos al bloque, "
                f"{escritura['escritos_hoja']} a hojas. "
                f"Bloque nuevo: {bloque['label'] if bloque else 'no'}. "
                f"Import: {importacion.get('prestamos', 0)} préstamos."
            ),
            direccion_ip=request.client.host if request.client else None,
        )
        db.add(log)
        db.commit()

        return SuccessResponse(
            message="Creemos.xlsx actualizado y sincronizado.",
            data={
                "bloque_nuevo": bloque,
                "pagos_excel": escritura,
                "sync": {"creditos": resultado.get("creditos"), "pagos": resultado.get("pagos")},
                "importacion": importacion,
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/cartera/status")
def status_cartera(_: Usuario = Depends(get_current_user)):
    try:
        session = get_cartera_session()
        from app.cartera.models import ClienteCartera, Credito, PagoHistorico, SnapshotMensual
        stats = {
            "clientes": session.query(ClienteCartera).count(),
            "creditos": session.query(Credito).count(),
            "creditos_con_historial": session.query(Credito).filter(Credito.tiene_historial_detallado == True).count(),
            "pagos": session.query(PagoHistorico).count(),
            "snapshots_creemos": session.query(SnapshotMensual).filter(SnapshotMensual.origen_archivo == "CREEMOS").count(),
        }
        session.close()
        return SuccessResponse(data=stats)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/historial")
def historial_sync(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    q = db.query(Log).filter(Log.modulo == "Sincronizacion").order_by(Log.id.desc())
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    result = []
    for l in items:
        result.append({
            "id": l.id, "accion": l.accion, "descripcion": l.descripcion,
            "usuario": l.usuario.nombre if l.usuario else "",
            "fecha": str(l.created_at) if l.created_at else None,
        })
    return SuccessResponse(data={"items": result, "total": total, "page": page, "page_size": page_size})
