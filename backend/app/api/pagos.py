from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.pago import PagoRegistrar, PagoResponse
from app.schemas.common import SuccessResponse
from app.services.pago_service import PagoService
from app.repositories.pago_repository import PagoRepository
from app.security.auth import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/v1/pagos", tags=["Pagos"])


@router.post("/calcular")
def calcular_pago(
    data: PagoRegistrar,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    service = PagoService(db)
    try:
        result = service.calcular(
            prestamo_id=data.prestamo_id,
            valor_pagado=data.valor_pagado,
            fecha_pago=data.fecha_pago,
            aplicar_interes=data.aplicar_interes,
            tasa_interes=data.tasa_interes,
        )
        return SuccessResponse(data=result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def registrar_pago(
    request: Request,
    data: PagoRegistrar,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = PagoService(db)
    try:
        result = service.registrar(
            prestamo_id=data.prestamo_id,
            valor_pagado=data.valor_pagado,
            fecha_pago=data.fecha_pago,
            observaciones=data.observaciones,
            usuario_id=current_user.id,
            ip=request.client.host if request.client else None,
            aplicar_interes=data.aplicar_interes,
            tasa_interes=data.tasa_interes,
        )
        return SuccessResponse(message="Pago registrado correctamente.", data={
            "pago": PagoResponse(
                id=result["pago"].id, prestamo_id=result["pago"].prestamo_id,
                numero_factura=result["pago"].numero_factura,
                fecha_pago=result["pago"].fecha_pago,
                dias_calculados=result["pago"].dias_calculados,
                dias_mora=result["pago"].dias_mora,
                saldo_anterior=result["pago"].saldo_anterior,
                intereses=result["pago"].intereses,
                capital=result["pago"].capital,
                valor_pagado=result["pago"].valor_pagado,
                saldo_nuevo=result["pago"].saldo_nuevo,
                observaciones=result["pago"].observaciones,
                usuario_nombre=current_user.nombre,
                tasa_interes_aplicada=result["pago"].tasa_interes_aplicada,
                created_at=result["pago"].created_at,
            ).model_dump(),
            "factura": result["factura"].numero_factura,
            "factura_id": result["factura"].id,
        })
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("")
def listar_pagos(
    prestamo_id: int | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    repo = PagoRepository(db)
    items, total = repo.list(prestamo_id=prestamo_id, page=page, page_size=page_size)
    result = []
    for p in items:
        result.append(PagoResponse(
            id=p.id, prestamo_id=p.prestamo_id,
            numero_factura=p.numero_factura, fecha_pago=p.fecha_pago,
            dias_calculados=p.dias_calculados, dias_mora=p.dias_mora,
            saldo_anterior=p.saldo_anterior, intereses=p.intereses, intereses_mora=p.intereses_mora or 0,
            capital=p.capital, valor_pagado=p.valor_pagado,
            saldo_nuevo=p.saldo_nuevo, observaciones=p.observaciones,
            usuario_nombre=p.usuario.nombre if p.usuario else "",
            tasa_interes_aplicada=p.tasa_interes_aplicada,
            created_at=p.created_at,
        ).model_dump())
    return SuccessResponse(data={"items": result, "total": total, "page": page, "page_size": page_size})


@router.get("/{pago_id}")
def obtener_pago(
    pago_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    repo = PagoRepository(db)
    p = repo.get_by_id(pago_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado.")
    return SuccessResponse(data=PagoResponse(
        id=p.id, prestamo_id=p.prestamo_id,
        numero_factura=p.numero_factura, fecha_pago=p.fecha_pago,
        dias_calculados=p.dias_calculados, dias_mora=p.dias_mora,
        saldo_anterior=p.saldo_anterior, intereses=p.intereses, intereses_mora=p.intereses_mora or 0,
        capital=p.capital, valor_pagado=p.valor_pagado,
        saldo_nuevo=p.saldo_nuevo, observaciones=p.observaciones,
        usuario_nombre=p.usuario.nombre if p.usuario else "",
        tasa_interes_aplicada=p.tasa_interes_aplicada,
        created_at=p.created_at,
    ).model_dump())
