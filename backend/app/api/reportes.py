from __future__ import annotations
from datetime import date, datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from app.database.database import get_db
from app.schemas.common import SuccessResponse
from app.security.auth import get_current_user
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.prestamo import Prestamo
from app.models.pago import Pago
from app.models.factura import Factura
from app.models.log import Log

router = APIRouter(prefix="/api/v1/reportes", tags=["Reportes"])


@router.get("/clientes")
def reporte_clientes(
    estado: str = Query("", max_length=20),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    q = db.query(Cliente).order_by(Cliente.nombre)
    if estado:
        q = q.filter(Cliente.estado == estado)
    items = q.all()
    return SuccessResponse(data={
        "items": [{
            "id": c.id, "nombre": c.nombre, "cedula": c.cedula, "placa": c.placa,
            "telefono": c.telefono, "estado": c.estado, "created_at": str(c.created_at) if c.created_at else None,
        } for c in items]
    })


@router.get("/pagos")
def reporte_pagos(
    desde: str = Query(""), hasta: str = Query(""),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    q = db.query(Pago).options(joinedload(Pago.prestamo).joinedload(Prestamo.cliente)).order_by(Pago.fecha_pago.desc())
    if desde:
        q = q.filter(Pago.fecha_pago >= date.fromisoformat(desde))
    if hasta:
        q = q.filter(Pago.fecha_pago <= date.fromisoformat(hasta))
    items = q.limit(500).all()
    return SuccessResponse(data={
        "items": [{
            "id": p.id, "numero_factura": p.numero_factura, "fecha_pago": str(p.fecha_pago),
            "valor_pagado": str(p.valor_pagado), "intereses": str(p.intereses),
            "capital": str(p.capital), "saldo_anterior": str(p.saldo_anterior),
            "saldo_nuevo": str(p.saldo_nuevo),
            "cliente": p.prestamo.cliente.nombre if p.prestamo and p.prestamo.cliente else "",
        } for p in items]
    })


@router.get("/ingresos")
def reporte_ingresos(
    desde: str = Query(""), hasta: str = Query(""),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    q = db.query(
        Pago.fecha_pago,
        (Pago.intereses + Pago.intereses_mora).label("valor")
    ).order_by(Pago.fecha_pago)
    if desde:
        q = q.filter(Pago.fecha_pago >= date.fromisoformat(desde))
    if hasta:
        q = q.filter(Pago.fecha_pago <= date.fromisoformat(hasta))
    items = q.all()
    total = sum(float(r.valor) for r in items)
    return SuccessResponse(data={
        "items": [{"fecha": str(r.fecha_pago), "valor": str(r.valor)} for r in items],
        "total": round(total),
    })


@router.get("/mora")
def reporte_mora(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    prestamos = db.query(Prestamo).options(joinedload(Prestamo.cliente)).filter(Prestamo.estado == "MORA").order_by(Prestamo.fecha_proximo_pago).all()
    return SuccessResponse(data={
        "items": [{
            "id": p.id, "cliente": p.cliente.nombre if p.cliente else "", "saldo": str(p.saldo_actual),
            "cuota": str(p.valor_cuota), "proximo_pago": str(p.fecha_proximo_pago),
            "dias_mora": (date.today() - p.fecha_proximo_pago).days if p.fecha_proximo_pago else 0,
        } for p in prestamos]
    })


@router.get("/facturas")
def reporte_facturas(
    desde: str = Query(""), hasta: str = Query(""),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    q = db.query(Factura).options(joinedload(Factura.cliente), joinedload(Factura.pago)).order_by(Factura.fecha.desc())
    if desde:
        q = q.filter(Factura.fecha >= date.fromisoformat(desde))
    if hasta:
        q = q.filter(Factura.fecha <= date.fromisoformat(hasta))
    items = q.limit(500).all()
    return SuccessResponse(data={
        "items": [{
            "id": f.id, "numero": f.numero_factura, "fecha": str(f.fecha),
            "cliente": f.cliente.nombre if f.cliente else "", "valor": str(f.pago.valor_pagado) if f.pago else "",
            "estado": f.estado,
        } for f in items]
    })


@router.get("/flujo-mensual")
def flujo_mensual(
    meses: int = Query(12, ge=1, le=60),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    from calendar import monthrange
    hoy = date.today()
    labels: list[str] = []
    ingresos: list[float] = []
    intereses: list[float] = []
    capital_recuperado: list[float] = []
    nuevos_prestamos: list[float] = []
    saldo_final: list[float] = []

    half = meses // 2
    for i in range(half, -half - 1, -1):
        m = hoy.month - i
        y = hoy.year
        while m < 1:
            m += 12
            y -= 1
        while m > 12:
            m -= 12
            y += 1
        _, last_day = monthrange(y, m)
        month_start = date(y, m, 1)
        month_end = date(y, m, last_day)
        labels.append(f"{y}-{m:02d}")

        # Ingresos (pagos) del mes
        row = db.query(
            func.coalesce(func.sum(Pago.valor_pagado), 0),
            func.coalesce(func.sum(Pago.intereses), 0),
            func.coalesce(func.sum(Pago.capital), 0),
        ).filter(Pago.fecha_pago >= month_start, Pago.fecha_pago <= month_end).first()
        tot, inte, cap = (float(r) if r else 0 for r in row) if row else (0, 0, 0)
        ingresos.append(tot)
        intereses.append(inte)
        capital_recuperado.append(cap)

        # Nuevos préstamos del mes
        new_row = db.query(func.coalesce(func.sum(Prestamo.capital_inicial), 0)).filter(
            Prestamo.fecha_inicio >= month_start, Prestamo.fecha_inicio <= month_end,
        ).first()
        nuevos_prestamos.append(float(new_row[0]) if new_row else 0)

        # Saldo total al final del mes
        saldo_row = db.query(func.coalesce(func.sum(Prestamo.saldo_actual), 0)).filter(
            Prestamo.estado.in_(["ACTIVO", "MORA"]),
            Prestamo.fecha_inicio <= month_end,
        ).first()
        saldo_final.append(float(saldo_row[0]) if saldo_row else 0)

    flujo_neto = [i - n for i, n in zip(intereses, nuevos_prestamos)]

    return SuccessResponse(data={
        "labels": labels,
        "ingresos": intereses,
        "intereses": intereses,
        "capital_recuperado": capital_recuperado,
        "nuevos_prestamos": nuevos_prestamos,
        "flujo_neto": flujo_neto,
        "saldo_final": saldo_final,
    })


@router.get("/exportar-excel")
def exportar_excel(
    reporte: str = Query(..., pattern=r"^(clientes|pagos|ingresos|mora|facturas)$"),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    import openpyxl
    from openpyxl.styles import Font, Alignment
    from app.core.config import settings
    import os

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = reporte.capitalize()
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    filename = f"reporte_{reporte}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = os.path.join(settings.DATA_DIR, filename)

    if reporte == "clientes":
        ws.append(["Nombre", "Cédula", "Placa", "Teléfono", "Estado", "Creado"])
        for c in db.query(Cliente).order_by(Cliente.nombre).all():
            ws.append([c.nombre, c.cedula, c.placa, c.telefono or "", c.estado, str(c.created_at or "")])
    elif reporte == "pagos":
        ws.append(["Factura", "Fecha", "Cliente", "Valor", "Interés", "Capital", "Saldo Anterior", "Saldo Nuevo"])
        q = db.query(Pago).options(joinedload(Pago.prestamo).joinedload(Prestamo.cliente)).order_by(Pago.fecha_pago.desc()).limit(500)
        for p in q:
            ws.append([p.numero_factura, str(p.fecha_pago), p.prestamo.cliente.nombre if p.prestamo and p.prestamo.cliente else "",
                       str(p.valor_pagado), str(p.intereses), str(p.capital), str(p.saldo_anterior), str(p.saldo_nuevo)])
    elif reporte == "ingresos":
        ws.append(["Fecha", "Intereses"])
        q = db.query(Pago.fecha_pago, (Pago.intereses + Pago.intereses_mora).label("total_intereses")).order_by(Pago.fecha_pago).all()
        for r in q:
            ws.append([str(r.fecha_pago), str(r.total_intereses)])
    elif reporte == "mora":
        ws.append(["Cliente", "Saldo", "Cuota", "Próximo Pago", "Días Mora"])
        q = db.query(Prestamo).options(joinedload(Prestamo.cliente)).filter(Prestamo.estado == "MORA").all()
        for p in q:
            ws.append([p.cliente.nombre if p.cliente else "", str(p.saldo_actual), str(p.valor_cuota),
                       str(p.fecha_proximo_pago), (date.today() - p.fecha_proximo_pago).days if p.fecha_proximo_pago else 0])
    elif reporte == "facturas":
        ws.append(["Factura", "Fecha", "Cliente", "Valor", "Estado"])
        q = db.query(Factura).options(joinedload(Factura.cliente), joinedload(Factura.pago)).order_by(Factura.fecha.desc()).limit(500)
        for f in q:
            ws.append([f.numero_factura, str(f.fecha), f.cliente.nombre if f.cliente else "",
                       str(f.pago.valor_pagado) if f.pago else "", f.estado])

    for col in ws.columns:
        max_len = max((len(str(c.value or "")) for c in col), default=0)
        ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 40)
    header_font = Font(bold=True)
    for cell in ws[1]:
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    wb.save(filepath)
    return FileResponse(filepath, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=filename)
