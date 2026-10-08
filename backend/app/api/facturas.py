from __future__ import annotations
import os
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload
from app.database.database import get_db
from app.schemas.factura import FacturaResponse
from app.schemas.common import SuccessResponse
from app.services.pdf_service import generar_recibo
from app.security.auth import get_current_user
from app.models.usuario import Usuario
from app.models.factura import Factura
from app.models.cliente import Cliente
from app.models.log import Log

router = APIRouter(prefix="/api/v1/facturas", tags=["Facturas"])


@router.get("")
def listar_facturas(
    search: str = Query("", max_length=200),
    estado: str = Query("", max_length=20),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    q = db.query(Factura).options(joinedload(Factura.cliente), joinedload(Factura.pago))
    if search:
        q = q.join(Cliente, Factura.cliente_id == Cliente.id).filter(
            Cliente.nombre.ilike(f"%{search}%") | Factura.numero_factura.ilike(f"%{search}%")
        )
    if estado:
        q = q.filter(Factura.estado == estado)
    q = q.order_by(Factura.id.desc())
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    result = []
    for f in items:
        result.append(FacturaResponse(
            id=f.id, numero_factura=f.numero_factura, cliente_id=f.cliente_id,
            pago_id=f.pago_id, fecha=f.fecha, ruta_pdf=f.ruta_pdf, estado=f.estado,
            created_at=f.created_at, cliente_nombre=f.cliente.nombre if f.cliente else "",
            pago_valor=str(f.pago.valor_pagado) if f.pago else "",
        ).model_dump())
    return SuccessResponse(data={"items": result, "total": total, "page": page, "page_size": page_size})


@router.get("/{factura_id}")
def obtener_factura(
    factura_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    f = db.query(Factura).options(joinedload(Factura.cliente), joinedload(Factura.pago)).filter(Factura.id == factura_id).first()
    if not f:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada.")
    return SuccessResponse(data=FacturaResponse(
        id=f.id, numero_factura=f.numero_factura, cliente_id=f.cliente_id,
        pago_id=f.pago_id, fecha=f.fecha, ruta_pdf=f.ruta_pdf, estado=f.estado,
        created_at=f.created_at, cliente_nombre=f.cliente.nombre if f.cliente else "",
        pago_valor=str(f.pago.valor_pagado) if f.pago else "",
    ).model_dump())


@router.post("/{factura_id}/generar-pdf")
def generar_pdf(
    factura_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    f = db.query(Factura).options(joinedload(Factura.cliente), joinedload(Factura.pago)).filter(Factura.id == factura_id).first()
    if not f:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada.")
    try:
        filepath = generar_recibo(db, f)
        db.commit()
        log = Log(
            usuario_id=current_user.id, accion="GENERAR_PDF", modulo="Facturacion",
            descripcion=f"PDF generado para factura {f.numero_factura}.",
        )
        db.add(log)
        db.commit()
        return SuccessResponse(message="PDF generado correctamente.", data={"ruta_pdf": filepath, "factura_id": f.id})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al generar PDF: {str(e)}")


@router.get("/{factura_id}/pdf")
def descargar_pdf(
    factura_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    f = db.query(Factura).filter(Factura.id == factura_id).first()
    if not f:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada.")
    if not f.ruta_pdf or not os.path.exists(f.ruta_pdf):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PDF no generado. Use POST /generar-pdf primero.")
    filename = f"recibo_{f.numero_factura}.pdf"
    return FileResponse(f.ruta_pdf, media_type="application/pdf", filename=filename)


@router.delete("/{factura_id}")
def eliminar_factura(
    factura_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    f = db.query(Factura).filter(Factura.id == factura_id).first()
    if not f:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada.")
    if f.ruta_pdf and os.path.exists(f.ruta_pdf):
        try:
            os.remove(f.ruta_pdf)
        except OSError:
            pass
    log = Log(
        usuario_id=current_user.id, accion="ELIMINAR_FACTURA", modulo="Facturacion",
        descripcion=f"Factura {f.numero_factura} eliminada.",
    )
    db.add(log)
    db.delete(f)
    db.commit()
    return SuccessResponse(message="Factura eliminada correctamente.")
