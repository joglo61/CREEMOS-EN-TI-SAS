"""Parser para Creemos.xlsx — cartera unificada.

Formato:
- Hoja CXCOBRAR con N bloques mensuales (ENERO DE 2026 ... AGOSTO DE 2026).
  Cada bloque: mes en col A, encabezados 2 filas abajo, luego una tabla con
  toda la cartera. Columnas:
    B=Fecha (desembolso)  C=Placa  D=Cliente  E=Vr.credito  F=Vr.Cuota
    G=Saldo anterior  H=Fecha Inicial  I=Fecha Final  J=Dias  K=Intereses
    L=Int. Mora  M=Abono K  N=Cuota  O=Saldo Final
- El relleno de color en la celda del cliente indica "pagó ese mes"
  (cada mes usa un color distinto: azul, verde, etc.)
- Hojas individuales por placa con el historial de pagos detallado.
"""
from datetime import datetime
from pathlib import Path

import openpyxl

from app.cartera.parser_joglo import (
    EXCLUIDAS,
    _to_int,
    parse_client_sheet,
    parse_sheet_name,
)

MESES = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
         "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]


def _es_mes(texto):
    if not texto or not isinstance(texto, str):
        return False
    t = texto.upper().strip()
    return any(t.startswith(m) for m in MESES)


def _fecha_celda(val):
    if isinstance(val, datetime):
        return val.date()
    return val


def _tiene_relleno(ws, r, c):
    """True si la celda tiene relleno sólido de color (indica pago del mes)."""
    fill = ws.cell(r, c).fill
    if not fill or fill.patternType != "solid":
        return False
    col = fill.fgColor
    if col is None:
        return False
    if col.type == "theme" and col.theme not in (None, 0, 1):
        return True
    rgb = getattr(col, "rgb", None)
    if rgb and isinstance(rgb, str) and rgb not in ("00000000", "FFFFFFFF"):
        return True
    if col.type == "rgb":
        return True
    return False


class CreemosParser:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.creditos = []
        self.pagos = []
        self.snapshots = []
        self.errores = []

    def parse_all(self):
        wb = openpyxl.load_workbook(str(self.filepath), data_only=True)

        for sheet_name in wb.sheetnames:
            if sheet_name in EXCLUIDAS:
                continue
            if sheet_name == "CXCOBRAR":
                self._parse_cxcobrar(wb)
                continue

            ws = wb[sheet_name]
            result = parse_client_sheet(ws, sheet_name)
            if result["errores"]:
                self.errores.append(f"Hoja '{sheet_name}': {'; '.join(result['errores'])}")
            if not result["pagos"] and not result["valor_credito"]:
                continue

            base_placa, sufijo = parse_sheet_name(sheet_name)

            self.creditos.append({
                "placa": base_placa,
                "sufijo_credito": sufijo,
                "nombre_cliente": result["nombre_cliente"] or sheet_name,
                "telefono": result["telefono"],
                "valor_credito": result["valor_credito"],
                "valor_cuota": result["valor_cuota"],
                "fecha_desembolso": result["fecha_desembolso"],
                "plazo_meses": result["plazo_meses"],
                "prenda": None,
                "tiene_historial_detallado": True,
            })

            for p in result["pagos"]:
                p["placa"] = base_placa
                p["sufijo"] = sufijo
                self.pagos.append(p)

        wb.close()
        return self.creditos, self.pagos, self.snapshots

    def _parse_cxcobrar(self, wb):
        ws = wb["CXCOBRAR"]
        numero_bloque = 0

        r = 1
        while r <= ws.max_row:
            v = ws.cell(r, 1).value
            if not (v and isinstance(v, str) and _es_mes(v)):
                r += 1
                continue

            numero_bloque += 1
            month_label = str(v).strip()
            header_row = r + 2
            dr = header_row + 1

            while dr <= ws.max_row:
                placa = str(ws.cell(dr, 3).value or "").strip()
                cliente = str(ws.cell(dr, 4).value or "").strip()

                # Fin del bloque: fila sin placa ni cliente (totales o separador)
                if not placa and not cliente:
                    break

                # El relleno de color en la celda del cliente = pagó ese mes.
                # Doble verificación con la columna N (Cuota) no vacía.
                # Filas de ALTA (fecha desembolso = fecha final) no son pagos.
                cuota_val = _to_int(ws.cell(dr, 14).value)
                fecha_orig = _fecha_celda(ws.cell(dr, 2).value)
                fecha_fin = _fecha_celda(ws.cell(dr, 9).value)
                es_alta = fecha_orig is not None and fecha_orig == fecha_fin
                pago_del_mes = (_tiene_relleno(ws, dr, 4) or cuota_val is not None) and not es_alta

                row = {
                    "numero_bloque": numero_bloque,
                    "placa": placa,
                    "cliente": cliente,
                    "fecha_original": fecha_orig,
                    "vr_credito": _to_int(ws.cell(dr, 5).value),
                    "vr_cuota": _to_int(ws.cell(dr, 6).value),
                    "saldo_anterior": _to_int(ws.cell(dr, 7).value),
                    "fecha_inicial": _fecha_celda(ws.cell(dr, 8).value),
                    "fecha_final": fecha_fin,
                    "dias": _to_int(ws.cell(dr, 10).value),
                    "intereses": _to_int(ws.cell(dr, 11).value),
                    "interes_mora": _to_int(ws.cell(dr, 12).value),
                    "abono_k": _to_int(ws.cell(dr, 13).value),
                    "cuota": cuota_val,
                    "saldo_final": _to_int(ws.cell(dr, 15).value),
                    "pago_del_mes": pago_del_mes,
                    "mes_reportado": month_label,
                }
                self.snapshots.append(row)
                dr += 1

            r = dr