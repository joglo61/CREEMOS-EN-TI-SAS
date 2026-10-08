from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse, CronogramaEntry, HistorialEntry
from app.schemas.common import SuccessResponse
from app.services.cliente_service import ClienteService
from app.security.auth import get_current_user
from app.models.usuario import Usuario
from app.repositories.cliente_repository import ClienteRepository
from app.models.log import Log

router = APIRouter(prefix="/api/v1/clientes", tags=["Clientes"])


@router.get("")
def listar_clientes(
    search: str = Query("", max_length=200),
    estado: str = Query("", max_length=20),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    repo = ClienteRepository(db)
    items, total = repo.search(term=search, estado=estado, page=page, page_size=page_size)
    return SuccessResponse(data={
        "items": [ClienteResponse.model_validate(c).model_dump() for c in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    })


@router.get("/{cliente_id}")
def obtener_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    repo = ClienteRepository(db)
    cliente = repo.get_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado.")
    prestamo = cliente.prestamos[0] if cliente.prestamos else None
    return SuccessResponse(data={
        **ClienteResponse.model_validate(cliente).model_dump(),
        "prestamo": {
            "id": prestamo.id,
            "capital_inicial": str(prestamo.capital_inicial),
            "saldo_actual": str(prestamo.saldo_actual),
            "valor_cuota": str(prestamo.valor_cuota),
            "tasa_interes": str(prestamo.tasa_interes),
            "fecha_inicio": str(prestamo.fecha_inicio),
            "fecha_proximo_pago": str(prestamo.fecha_proximo_pago),
            "estado": prestamo.estado,
        } if prestamo else None,
    })


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_cliente(
    request: Request,
    data: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = ClienteService(db)
    try:
        result = service.crear(
            nombre=data.nombre,
            cedula=data.cedula,
            placa=data.placa,
            telefono=data.telefono,
            direccion=data.direccion,
            correo=data.correo,
            observaciones=data.observaciones,
            capital_inicial=data.capital_inicial,
            valor_cuota=data.valor_cuota,
            fecha_inicio=data.fecha_inicio,
            fecha_primer_pago=data.fecha_primer_pago,
            usuario_id=current_user.id,
            ip=request.client.host if request.client else None,
        )
        return SuccessResponse(message="Cliente creado correctamente.", data={
            "cliente": ClienteResponse.model_validate(result["cliente"]).model_dump(),
        })
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{cliente_id}")
def actualizar_cliente(
    request: Request,
    cliente_id: int,
    data: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = ClienteService(db)
    try:
        cliente = service.actualizar(
            cliente_id=cliente_id,
            nombre=data.nombre,
            telefono=data.telefono,
            direccion=data.direccion,
            correo=data.correo,
            observaciones=data.observaciones,
            usuario_id=current_user.id,
            ip=request.client.host if request.client else None,
        )
        return SuccessResponse(message="Cliente actualizado correctamente.", data=ClienteResponse.model_validate(cliente).model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{cliente_id}")
def eliminar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    repo = ClienteRepository(db)
    cliente = repo.get_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado.")
    repo.soft_delete(cliente)
    log = Log(
        usuario_id=current_user.id, accion="DESACTIVAR_CLIENTE", modulo="Clientes",
        descripcion=f"Cliente {cliente.nombre} ({cliente.cedula}) desactivado.",
    )
    db.add(log)
    db.commit()
    return SuccessResponse(message="Cliente desactivado correctamente.")


@router.delete("/{cliente_id}/hard")
def eliminar_cliente_permanente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    repo = ClienteRepository(db)
    cliente = repo.get_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado.")
    log = Log(
        usuario_id=current_user.id, accion="ELIMINAR_CLIENTE", modulo="Clientes",
        descripcion=f"Cliente {cliente.nombre} ({cliente.cedula}) eliminado permanentemente.",
    )
    db.add(log)
    db.commit()
    repo.hard_delete(cliente)
    return SuccessResponse(message="Cliente eliminado permanentemente.")


@router.post("/{cliente_id}/toggle-estado")
def toggle_estado_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    repo = ClienteRepository(db)
    cliente = repo.get_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado.")
    repo.toggle_estado(cliente)
    nuevo_estado = cliente.estado
    log = Log(
        usuario_id=current_user.id, accion="TOGGLE_ESTADO_CLIENTE", modulo="Clientes",
        descripcion=f"Cliente {cliente.nombre} ({cliente.cedula}) cambiado a {nuevo_estado}.",
    )
    db.add(log)
    db.commit()
    return SuccessResponse(message=f"Cliente {nuevo_estado.lower()} correctamente.", data={"estado": nuevo_estado})


@router.get("/{cliente_id}/cronograma")
def obtener_cronograma(
    cliente_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(360, ge=1, le=360),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    service = ClienteService(db)
    try:
        result = service.obtener_cronograma(cliente_id, page=page, page_size=page_size)
        return SuccessResponse(data={
            "items": [CronogramaEntry.model_validate(c).model_dump(mode="json") for c in result["items"]],
            "total": result["total"],
            "page": result["page"],
            "page_size": result["page_size"],
            "prestamo_id": result["prestamo_id"],
        })
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{cliente_id}/historial")
def obtener_historial(
    cliente_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    service = ClienteService(db)
    try:
        result = service.obtener_historial(cliente_id, page=page, page_size=page_size)
        items = []
        for h in result["items"]:
            items.append(HistorialEntry(
                id=h.id,
                accion=h.accion,
                modulo=h.modulo,
                descripcion=h.descripcion,
                usuario=h.usuario.nombre if h.usuario else None,
                created_at=str(h.created_at) if h.created_at else None,
            ).model_dump())
        return SuccessResponse(data={
            "items": items,
            "total": result["total"],
            "page": result["page"],
            "page_size": result["page_size"],
        })
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
