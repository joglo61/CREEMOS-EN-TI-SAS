from __future__ import annotations
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session, contains_eager
from fastapi import APIRouter, Depends
from app.database.database import get_db
from app.schemas.common import SuccessResponse
from app.security.auth import get_current_user
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.prestamo import Prestamo
from app.models.pago import Pago
from app.models.factura import Factura

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


@router.get("")
def dashboard(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    hoy = date.today()
    inicio_mes = date(hoy.year, hoy.month, 1)

    clientes_activos = db.query(Cliente).filter(Cliente.estado == "ACTIVO").count()

    prestamos_mora = db.query(Prestamo).join(Cliente).filter(
        Cliente.estado == "ACTIVO",
        Prestamo.estado == "MORA",
    ).count()

    capital_pendiente = db.query(Prestamo).join(Cliente).filter(
        Cliente.estado == "ACTIVO",
        Prestamo.estado.in_(["ACTIVO", "MORA"]),
    ).with_entities(Prestamo.saldo_actual).all()
    total_pendiente = sum(float(r[0]) for r in capital_pendiente) if capital_pendiente else 0

    lunes = hoy - timedelta(days=hoy.weekday())
    from sqlalchemy import func
    ingresos_hoy = db.query(
        func.coalesce(func.sum(Pago.intereses), 0) + func.coalesce(func.sum(Pago.intereses_mora), 0)
    ).filter(Pago.fecha_pago == hoy).first()
    total_hoy = float(ingresos_hoy[0]) if ingresos_hoy and ingresos_hoy[0] else 0

    ingresos_semana = db.query(
        func.coalesce(func.sum(Pago.intereses), 0) + func.coalesce(func.sum(Pago.intereses_mora), 0)
    ).filter(Pago.fecha_pago >= lunes).first()
    total_semana = float(ingresos_semana[0]) if ingresos_semana and ingresos_semana[0] else 0

    ingresos_mes = db.query(
        func.coalesce(func.sum(Pago.intereses), 0) + func.coalesce(func.sum(Pago.intereses_mora), 0)
    ).filter(Pago.fecha_pago >= inicio_mes).first()
    total_mes = float(ingresos_mes[0]) if ingresos_mes and ingresos_mes[0] else 0

    ultimos_pagos = db.query(Pago).join(Prestamo, Prestamo.id == Pago.prestamo_id).join(
        Cliente, Cliente.id == Prestamo.cliente_id,
    ).options(
        contains_eager(Pago.prestamo).contains_eager(Prestamo.cliente),
    ).filter(Cliente.estado == "ACTIVO").order_by(Pago.id.desc()).limit(5).all()
    pagos_data = []
    for p in ultimos_pagos:
        total_intereses = float(p.intereses) + float(p.intereses_mora)
        pagos_data.append({
            "id": p.id, "factura": p.numero_factura,
            "cliente": p.prestamo.cliente.nombre,
            "valor": str(total_intereses),
            "fecha": str(p.fecha_pago),
        })

    ultimas_facturas = db.query(Factura).join(Cliente, Cliente.id == Factura.cliente_id).options(
        contains_eager(Factura.cliente),
    ).filter(
        Cliente.estado == "ACTIVO",
    ).order_by(Factura.id.desc()).limit(5).all()
    facturas_data = []
    for f in ultimas_facturas:
        facturas_data.append({
            "id": f.id, "numero": f.numero_factura,
            "cliente": f.cliente.nombre,
            "fecha": str(f.fecha), "estado": f.estado,
        })

    return SuccessResponse(data={
        "clientes_activos": clientes_activos,
        "prestamos_mora": prestamos_mora,
        "capital_pendiente": round(total_pendiente),
        "ingresos_hoy": round(total_hoy),
        "ingresos_semana": round(total_semana),
        "ingresos_mes": round(total_mes),
        "ultimos_pagos": pagos_data,
        "ultimas_facturas": facturas_data,
    })
