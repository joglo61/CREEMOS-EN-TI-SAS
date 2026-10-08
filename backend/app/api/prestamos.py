from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.prestamo import PrestamoCreate, PrestamoUpdate, PrestamoResponse
from app.schemas.cliente import CronogramaEntry
from app.schemas.common import SuccessResponse
from app.services.prestamo_service import PrestamoService
from app.repositories.prestamo_repository import PrestamoRepository
from app.security.auth import get_current_user, require_admin
from app.models.usuario import Usuario
from app.models.log import Log

router = APIRouter(prefix="/api/v1/prestamos", tags=["Prestamos"])


@router.get("")
def listar_prestamos(
    search: str = Query("", max_length=200),
    estado: str = Query("", max_length=20),
    cliente_id: int | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    repo = PrestamoRepository(db)
    items, total = repo.list(term=search, estado=estado, cliente_id=cliente_id, page=page, page_size=page_size)
    result = []
    for p in items:
            result.append(PrestamoResponse(
            id=p.id, cliente_id=p.cliente_id, cliente_nombre=p.cliente.nombre if p.cliente else "",
            cliente_placa=p.cliente.placa if p.cliente else "",
            capital_inicial=p.capital_inicial, saldo_actual=p.saldo_actual,
            valor_cuota=p.valor_cuota, tasa_interes=p.tasa_interes,
            fecha_inicio=p.fecha_inicio, fecha_primer_pago=p.fecha_primer_pago,
            fecha_proximo_pago=p.fecha_proximo_pago, estado=p.estado,
            created_at=p.created_at, updated_at=p.updated_at,
        ).model_dump())
    return SuccessResponse(data={
        "items": result, "total": total, "page": page, "page_size": page_size,
    })


@router.get("/{prestamo_id}")
def obtener_prestamo(
    prestamo_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    repo = PrestamoRepository(db)
    p = repo.get_by_id(prestamo_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo no encontrado.")
    return SuccessResponse(data=PrestamoResponse(
        id=p.id, cliente_id=p.cliente_id, cliente_nombre=p.cliente.nombre if p.cliente else "",
        cliente_placa=p.cliente.placa if p.cliente else "",
        capital_inicial=p.capital_inicial, saldo_actual=p.saldo_actual,
        valor_cuota=p.valor_cuota, tasa_interes=p.tasa_interes,
        fecha_inicio=p.fecha_inicio, fecha_primer_pago=p.fecha_primer_pago,
        fecha_proximo_pago=p.fecha_proximo_pago, estado=p.estado,
        created_at=p.created_at, updated_at=p.updated_at,
    ).model_dump())


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_prestamo(
    request: Request,
    data: PrestamoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = PrestamoService(db)
    try:
        result = service.crear(
            cliente_id=data.cliente_id,
            capital_inicial=data.capital_inicial,
            valor_cuota=data.valor_cuota,
            fecha_inicio=data.fecha_inicio,
            fecha_primer_pago=data.fecha_primer_pago,
            usuario_id=current_user.id,
            ip=request.client.host if request.client else None,
        )
        return SuccessResponse(message="Préstamo creado correctamente.", data={
            "prestamo": PrestamoResponse(
                id=result["prestamo"].id, cliente_id=result["prestamo"].cliente_id,
                cliente_nombre="", cliente_placa="",
                capital_inicial=result["prestamo"].capital_inicial,
                saldo_actual=result["prestamo"].saldo_actual,
                valor_cuota=result["prestamo"].valor_cuota,
                tasa_interes=result["prestamo"].tasa_interes,
                fecha_inicio=result["prestamo"].fecha_inicio,
                fecha_primer_pago=result["prestamo"].fecha_primer_pago,
                fecha_proximo_pago=result["prestamo"].fecha_proximo_pago,
                estado=result["prestamo"].estado,
            ).model_dump(),
        })
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{prestamo_id}")
def actualizar_prestamo(
    request: Request,
    prestamo_id: int,
    data: PrestamoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = PrestamoService(db)
    try:
        p = service.actualizar(
            prestamo_id=prestamo_id,
            valor_cuota=data.valor_cuota,
            estado=data.estado,
            usuario_id=current_user.id,
            ip=request.client.host if request.client else None,
        )
        return SuccessResponse(message="Préstamo actualizado correctamente.", data=PrestamoResponse(
            id=p.id, cliente_id=p.cliente_id, cliente_nombre=p.cliente.nombre if p.cliente else "",
            capital_inicial=p.capital_inicial, saldo_actual=p.saldo_actual,
            valor_cuota=p.valor_cuota, tasa_interes=p.tasa_interes,
            fecha_inicio=p.fecha_inicio, fecha_primer_pago=p.fecha_primer_pago,
            fecha_proximo_pago=p.fecha_proximo_pago, estado=p.estado,
        ).model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{prestamo_id}/actualizar-estado")
def actualizar_estado(
    prestamo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = PrestamoService(db)
    repo = PrestamoRepository(db)
    prestamo = repo.get_by_id(prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo no encontrado.")
    nuevo_estado = service.actualizar_estado_automatico(prestamo)
    db.commit()
    log = Log(
        usuario_id=current_user.id, accion="ACTUALIZAR_ESTADO_PRESTAMO", modulo="Prestamos",
        descripcion=f"Estado del préstamo #{prestamo.id} actualizado a {nuevo_estado}.",
    )
    db.add(log)
    db.commit()
    return SuccessResponse(message=f"Estado actualizado a {nuevo_estado}.", data={"estado": nuevo_estado})


@router.post("/{prestamo_id}/anular")
def anular_prestamo(
    prestamo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    repo = PrestamoRepository(db)
    prestamo = repo.get_by_id(prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo no encontrado.")
    if prestamo.estado == "CANCELADO":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El préstamo ya está cancelado.")
    if prestamo.estado == "PAGADO":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se puede anular un préstamo pagado.")
    prestamo.estado = "CANCELADO"
    from app.models.cronograma import Cronograma
    db.query(Cronograma).filter(Cronograma.prestamo_id == prestamo_id, Cronograma.estado == "PENDIENTE").update({"estado": "CANCELADO"})
    log = Log(
        usuario_id=current_user.id, accion="ANULAR_PRESTAMO", modulo="Prestamos",
        descripcion=f"Préstamo #{prestamo.id} anulado por {current_user.usuario}.",
    )
    db.add(log)
    db.commit()
    return SuccessResponse(message="Préstamo anulado correctamente.", data={"estado": "CANCELADO"})


@router.post("/{prestamo_id}/cronograma/{cronograma_id}/toggle-estado")
def toggle_cronograma_estado(
    prestamo_id: int,
    cronograma_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    from app.models.cronograma import Cronograma
    from app.models.log import Log
    c = db.query(Cronograma).filter(Cronograma.id == cronograma_id, Cronograma.prestamo_id == prestamo_id).first()
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuota no encontrada.")
    nuevo_estado = "PAGADO" if c.estado == "PENDIENTE" else "PENDIENTE"
    c.estado = nuevo_estado
    log = Log(
        usuario_id=current_user.id, accion="TOGGLE_CRONOGRAMA", modulo="Préstamos",
        descripcion=f"Cuota #{c.numero_cuota} del préstamo #{prestamo_id} cambiada a {nuevo_estado}.",
    )
    db.add(log)
    db.commit()
    return SuccessResponse(message=f"Cuota #{c.numero_cuota} marcada como {nuevo_estado}.", data={"estado": nuevo_estado})


@router.get("/{prestamo_id}/cronograma")
def obtener_cronograma(
    prestamo_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(360, ge=1, le=360),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    from app.models.cronograma import Cronograma
    repo = PrestamoRepository(db)
    p = repo.get_by_id(prestamo_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo no encontrado.")
    q = db.query(Cronograma).where(Cronograma.prestamo_id == prestamo_id).order_by(Cronograma.numero_cuota)
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return SuccessResponse(data={
        "items": [CronogramaEntry.model_validate(c).model_dump(mode="json") for c in items],
        "total": total, "page": page, "page_size": page_size,
    })

