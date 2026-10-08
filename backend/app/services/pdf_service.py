from __future__ import annotations
import os
from decimal import Decimal
from datetime import date, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Flowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

from app.core.config import settings
from app.models.pago import Pago
from app.models.factura import Factura
from app.models.cliente import Cliente
from app.models.configuracion import Configuracion
from sqlalchemy.orm import Session


class FullWidthHR(Flowable):
    """Horizontal line that spans the full page width (ignoring margins)."""
    def __init__(self, thickness=0.3, color=colors.grey, spaceBefore=0, spaceAfter=0):
        Flowable.__init__(self)
        self.thickness = thickness
        self.color = color
        self.spaceBefore = spaceBefore
        self.spaceAfter = spaceAfter
        self.width = 1  # will be set by drawOn
        self.height = thickness + spaceBefore + spaceAfter

    def drawOn(self, canvas, x, y, _sW=0):
        # Draw from page edge to page edge
        pw = canvas._pagesize[0] if hasattr(canvas, '_pagesize') else letter[0]
        canvas.saveState()
        canvas.setStrokeColor(self.color)
        canvas.setLineWidth(self.thickness)
        canvas.line(0, y + self.spaceAfter, pw, y + self.spaceAfter)
        canvas.restoreState()


def _format(val: Decimal | None) -> str:
    if val is None:
        return "$0"
    return f"${int(val):,}".replace(",", ".")


def _recibo_elements(styles, factura, pago, cliente, fecha_vencimiento):
    elements = []

    elements.append(Paragraph("RECIBO DE PAGO", styles["CenterTitle"]))
    elements.append(Paragraph(f"<b>No. {factura.numero_factura}</b>", styles["CenterSub"]))
    elements.append(Spacer(1, 2*mm))

    info_data = [
        [f"Fecha Pago: {factura.fecha}    |    Vencimiento: {fecha_vencimiento}"],
        [f"Cliente: {cliente.nombre}    |    Placa: {cliente.placa}"],
    ]
    info_table = Table(info_data, colWidths=[175*mm])
    info_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 2*mm))

    extra_row = ["", ""]

    header = ["Concepto", "Valor"]
    detail_data = [
        ["Saldo Anterior", _format(pago.saldo_anterior)],
        ["Intereses", _format(pago.intereses + (pago.intereses_mora or 0))],
        ["Abono a Capital", _format(pago.capital)],
        ["Valor Pagado", _format(pago.valor_pagado)],
        ["Saldo Nuevo", _format(pago.saldo_nuevo)],
        extra_row,
    ]

    detail_table = Table([header] + detail_data, colWidths=[100*mm, 65*mm])
    detail_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a5f")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (-1, 1), colors.white),
        ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#f8f9fa")),
        ("BACKGROUND", (0, 3), (-1, 3), colors.white),
        ("BACKGROUND", (0, 4), (-1, 4), colors.HexColor("#e8f5e9")),
        ("FONTNAME", (0, 4), (-1, 4), "Helvetica-Bold"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(detail_table)

    elements.append(Spacer(1, 12*mm))

    sig_data = [
        ["___________________________________________"],
        ["Firma y Sello"],
    ]
    sig_table = Table(sig_data, colWidths=[175*mm])
    sig_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
    ]))
    elements.append(sig_table)

    elements.append(Spacer(1, 2*mm))
    elements.append(HRFlowable(width="100%", thickness=0.3, color=colors.grey))
    elements.append(Paragraph("Este es un documento de soporte de pago.", ParagraphStyle("footer", parent=styles["Normal"], fontSize=6, textColor=colors.grey, alignment=TA_CENTER)))

    return elements


def generar_recibo(db: Session, factura: Factura) -> str:
    pago: Pago = factura.pago
    cliente: Cliente = factura.cliente
    config: Configuracion = db.query(Configuracion).first()

    empresa = config.empresa if config else "CREEMOS EN TI SAS"
    nit = config.nit if config else ""
    empresa_dir = config.direccion if config else ""
    empresa_tel = config.telefono if config else ""

    fecha_vencimiento = pago.fecha_pago - timedelta(days=pago.dias_mora)

    filename = f"recibo_{factura.numero_factura}.pdf"
    filepath = os.path.join(settings.RECIBOS_DIR, filename)
    os.makedirs(settings.RECIBOS_DIR, exist_ok=True)

    doc = SimpleDocTemplate(filepath, pagesize=letter, topMargin=0.8*cm, bottomMargin=0.8*cm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CenterTitle", parent=styles["Title"], alignment=TA_CENTER, fontSize=11, spaceAfter=1))
    styles.add(ParagraphStyle(name="CenterSub", parent=styles["Normal"], alignment=TA_CENTER, fontSize=8, textColor=colors.gray))
    styles.add(ParagraphStyle(name="RightSmall", parent=styles["Normal"], alignment=TA_RIGHT, fontSize=7))
    styles.add(ParagraphStyle(name="LeftSmall", parent=styles["Normal"], fontSize=7))

    def _build_half():
        half = []
        half.append(Paragraph(empresa, styles["CenterTitle"]))
        if nit:
            half.append(Paragraph(f"NIT: {nit}", styles["CenterSub"]))
        if empresa_dir:
            half.append(Paragraph(empresa_dir, styles["CenterSub"]))
        if empresa_tel:
            half.append(Paragraph(f"Tel: {empresa_tel}", styles["CenterSub"]))
        half.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#1e3a5f")))
        half.append(Spacer(1, 1*mm))
        half.extend(_recibo_elements(styles, factura, pago, cliente, fecha_vencimiento))
        return half

    top_half = _build_half()
    bottom_half = _build_half()

    top_spacer = 10*mm
    cut_gap = 12*mm
    cut_line_spacer = (cut_gap - 2*mm) / 2

    elements = (
        [Spacer(1, top_spacer)]
        + top_half
        + [Spacer(1, cut_line_spacer)]
        + [FullWidthHR(thickness=0.3, color=colors.grey)]
        + [Spacer(1, cut_line_spacer)]
        + bottom_half
    )

    doc.build(elements)

    factura.ruta_pdf = filepath
    return filepath
