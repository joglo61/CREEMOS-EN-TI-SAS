"""Escritura a Creemos.xlsx — creación de bloques mensuales, pagos del sistema, recálculo COM.

Convenciones del archivo:
- Hoja CXCOBRAR con bloques mensuales apilados ("AGOSTO DE 2026", etc.)
- Cada bloque: título en col A, encabezados 2 filas abajo, datos, totales SUM, resumen
- Columnas: B=Fecha desembolso, C=Placa, D=Cliente, E=Vr.credito, F=Vr.Cuota,
  G=Saldo anterior, H=Fecha Inicial, I=Fecha Final, J=Dias, K=Intereses,
  L=Int.Mora, M=Abono K, N=Cuota, O=Saldo Final
- Fórmulas: J==+I-H, K==(G*0.025)/30*J, M==+N-K-L, O==+G-M, A==1+A(prev)
- Relleno de color en celda D (cliente) = pagó ese mes (color distinto por mes)
- Hojas individuales por placa: fila de pago con fórmulas G==+J(prev)*2.5%/30*E,
  I==+F-G, J==+J(prev)-I

openpyxl no preserva valores cacheados de fórmulas al guardar, por eso después
de cada escritura se recalcula con Excel COM (win32com) para que el parser
pueda leer valores con data_only=True.
"""
import logging
import re
import shutil
from copy import copy
from datetime import date, datetime
from pathlib import Path

import openpyxl
from openpyxl.styles import PatternFill

logger = logging.getLogger(__name__)

MESES_ES = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
            "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]

# Colores claros rotativos por mes (ARGB con alfa FF)
COLORES_MES = [
    "FFD9E1F2",  # azul claro
    "FFE2EFDA",  # verde claro
    "FFFFF2CC",  # amarillo claro
    "FFFCE4D6",  # naranja claro
    "FFE4DFEC",  # púrpura claro
    "FFDDEBF7",  # azul pálido
    "FFE2F0D9",  # verde pálido
    "FFFFF2CC",  # amarillo claro
    "FFF8CBAD",  # melocotón
    "FFD6DCE4",  # gris azulado
    "FFEAD1DC",  # rosa claro
    "FFDAEEF3",  # turquesa claro
]


def color_mes(mes_num: int) -> str:
    """Color ARGB para un mes (1-12)."""
    return COLORES_MES[(mes_num - 1) % len(COLORES_MES)]


def mes_label(anio: int, mes: int) -> str:
    return f"{MESES_ES[mes - 1]} DE {anio}"


def parse_mes_label(label: str) -> tuple[int, int] | None:
    """'AGOSTO DE 2026' → (2026, 8). None si no calza."""
    m = re.match(r"^(\w+)\s+DE\s+(\d{4})", label.strip().upper())
    if not m:
        return None
    nombre, anio = m.group(1), int(m.group(2))
    try:
        return (anio, MESES_ES.index(nombre) + 1)
    except ValueError:
        return None


def localizar_bloques(ws) -> list[dict]:
    """Escanea CXCOBRAR y retorna metadata de cada bloque mensual."""
    bloques = []
    r = 1
    while r <= ws.max_row:
        v = ws.cell(r, 1).value
        if isinstance(v, str):
            parsed = parse_mes_label(v)
            if parsed:
                titulo = r
                header = r + 2
                datos_inicio = r + 3
                # Fin de datos: primera fila sin placa (C) ni cliente (D)
                datos_fin = datos_inicio
                while datos_fin <= ws.max_row:
                    if not ws.cell(datos_fin, 3).value and not ws.cell(datos_fin, 4).value:
                        break
                    datos_fin += 1
                datos_fin -= 1
                totales = datos_fin + 1
                resumen = None
                for sr in range(totales, min(totales + 6, ws.max_row + 1)):
                    ev = ws.cell(sr, 5).value
                    if isinstance(ev, str) and "Recaudo" in ev:
                        resumen = sr
                        break
                bloques.append({
                    "label": v.strip(), "anio": parsed[0], "mes": parsed[1],
                    "titulo": titulo, "header": header,
                    "datos_inicio": datos_inicio, "datos_fin": datos_fin,
                    "totales": totales, "resumen": resumen,
                })
                r = datos_fin + 1
                continue
        r += 1
    return bloques


def _copy_row_style(ws, src_row: int, dst_row: int, max_col: int = 15):
    for c in range(1, max_col + 1):
        src = ws.cell(src_row, c)
        dst = ws.cell(dst_row, c)
        if src.has_style:
            dst._style = copy(src._style)


def _backup(ruta: str) -> Path:
    bdir = Path(ruta).parent / "backend" / "data"
    bdir.mkdir(parents=True, exist_ok=True)
    bpath = bdir / f"backup_Creemos_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
    shutil.copy2(ruta, bpath)
    return bpath


def crear_bloque_mes(ruta: str, altas: list[dict] | None = None) -> dict | None:
    """Crea el bloque del mes siguiente al último, si el mes actual aún no tiene bloque.

    altas: créditos nuevos del sistema [{fecha_desembolso, placa, cliente,
    vr_credito, vr_cuota, saldo_anterior, fecha_inicial}]. Solo se incluyen si
    el bloque que se crea es el del mes en curso.
    Retorna {"label", "filas", "altas"} o None si no se creó nada.
    """
    hoy = date.today()

    # Leer valores del bloque anterior (data_only=True da los cacheados)
    wb_vals = openpyxl.load_workbook(ruta, data_only=True)
    ws_vals = wb_vals["CXCOBRAR"]
    bloques_vals = localizar_bloques(ws_vals)
    if not bloques_vals:
        wb_vals.close()
        return None
    ultimo_v = bloques_vals[-1]

    # Si casi todos los saldos finales vienen None, el archivo quedó sin caché
    # de fórmulas (guardado por openpyxl sin recalcular): recalcular y releer
    total_filas = ultimo_v["datos_fin"] - ultimo_v["datos_inicio"] + 1
    sin_cache = sum(
        1 for r in range(ultimo_v["datos_inicio"], ultimo_v["datos_fin"] + 1)
        if ws_vals.cell(r, 15).value is None
    )
    if total_filas > 0 and sin_cache > total_filas / 2:
        wb_vals.close()
        if recalcular_excel(ruta):
            wb_vals = openpyxl.load_workbook(ruta, data_only=True)
            ws_vals = wb_vals["CXCOBRAR"]
            bloques_vals = localizar_bloques(ws_vals)
            ultimo_v = bloques_vals[-1]
        else:
            wb_vals = openpyxl.load_workbook(ruta, data_only=True)
            ws_vals = wb_vals["CXCOBRAR"]
            bloques_vals = localizar_bloques(ws_vals)
            ultimo_v = bloques_vals[-1]

    if (hoy.year, hoy.month) <= (ultimo_v["anio"], ultimo_v["mes"]):
        wb_vals.close()
        return None  # el mes actual ya tiene bloque

    next_mes = ultimo_v["mes"] + 1
    next_anio = ultimo_v["anio"]
    if next_mes > 12:
        next_mes = 1
        next_anio += 1
    nuevo_label = mes_label(next_anio, next_mes)
    es_mes_actual = (next_anio == hoy.year and next_mes == hoy.month)

    # Filas que se arrastran del bloque anterior (se omiten saldos <= 0)
    filas_previas = []
    for r in range(ultimo_v["datos_inicio"], ultimo_v["datos_fin"] + 1):
        placa = str(ws_vals.cell(r, 3).value or "").strip()
        cliente = str(ws_vals.cell(r, 4).value or "").strip()
        if not placa and not cliente:
            continue
        saldo_final = ws_vals.cell(r, 15).value
        saldo_ant = ws_vals.cell(r, 7).value
        if saldo_final is not None:
            try:
                if float(saldo_final) <= 0:
                    continue  # crédito terminado → sale de la tabla
            except (ValueError, TypeError):
                pass
        filas_previas.append({
            "fecha_desembolso": ws_vals.cell(r, 2).value,
            "placa": placa,
            "cliente": cliente,
            "vr_credito": ws_vals.cell(r, 5).value,
            "vr_cuota": ws_vals.cell(r, 6).value,
            "saldo_anterior": saldo_final if saldo_final is not None else saldo_ant,
            "fecha_inicial": ws_vals.cell(r, 9).value,  # I prev → H nueva
        })
    wb_vals.close()

    if not es_mes_actual:
        altas = []

    # Abrir para escribir (data_only=False preserva fórmulas)
    wb = openpyxl.load_workbook(ruta, data_only=False)
    ws = wb["CXCOBRAR"]
    bloques_w = localizar_bloques(ws)
    ultimo_w = bloques_w[-1]

    _backup(ruta)

    tpl_titulo = ultimo_w["titulo"]
    tpl_header = ultimo_w["header"]
    tpl_data = ultimo_w["datos_inicio"]
    tpl_totales = ultimo_w["totales"]
    tpl_resumen = ultimo_w["resumen"]

    T = ws.max_row + 2  # fila del título (1 fila en blanco de separación)

    # Título
    _copy_row_style(ws, tpl_titulo, T)
    ws.cell(T, 1).value = nuevo_label

    # Fila en blanco entre título y encabezado
    ws.cell(T + 1, 12).value = " "
    ws.cell(T + 1, 15).value = " "

    # Encabezado
    _copy_row_style(ws, tpl_header, T + 2)
    for c in range(1, 16):
        ws.cell(T + 2, c).value = ws.cell(tpl_header, c).value

    # Datos
    all_filas = filas_previas + list(altas or [])
    first_data = T + 3
    for i, fila in enumerate(all_filas):
        r = first_data + i
        _copy_row_style(ws, tpl_data, r)
        # Limpiar relleno de "pagó" heredado de la fila plantilla (nadie ha pagado aún)
        ws.cell(r, 4).fill = PatternFill(fill_type=None)
        ws.cell(r, 1).value = 1 if i == 0 else f"=1+A{r - 1}"
        ws.cell(r, 2).value = fila.get("fecha_desembolso")
        ws.cell(r, 3).value = fila.get("placa")
        ws.cell(r, 4).value = fila.get("cliente")
        ws.cell(r, 5).value = fila.get("vr_credito")
        ws.cell(r, 6).value = fila.get("vr_cuota")
        ws.cell(r, 7).value = fila.get("saldo_anterior")
        fi = fila.get("fecha_inicial") or fila.get("fecha_desembolso")
        ws.cell(r, 8).value = fi
        ws.cell(r, 9).value = fi
        ws.cell(r, 10).value = f"=+I{r}-H{r}"
        ws.cell(r, 11).value = f"=(G{r}*0.025)/30*J{r}"
        ws.cell(r, 13).value = f"=+N{r}-K{r}-L{r}"
        ws.cell(r, 15).value = f"=+G{r}-M{r}"

    # Totales
    tr = first_data + len(all_filas)
    _copy_row_style(ws, tpl_totales, tr)
    for col_idx in (7, 11, 12, 13, 14, 15):
        letra = openpyxl.utils.get_column_letter(col_idx)
        ws.cell(tr, col_idx).value = f"=SUM({letra}{first_data}:{letra}{tr - 1})"

    # Filas intermedias en blanco
    ws.cell(tr + 1, 11).value = " "
    ws.cell(tr + 2, 14).value = " "

    # Resumen (Recaudo / Abono Capital / Abono Intereses)
    sr = tr + 3
    if tpl_resumen:
        _copy_row_style(ws, tpl_resumen, sr)
        _copy_row_style(ws, tpl_resumen + 1, sr + 1)
        _copy_row_style(ws, tpl_resumen + 2, sr + 2)
    mes_nombre = MESES_ES[next_mes - 1].capitalize()

    ws.cell(sr, 5).value = f"Recaudo de {mes_nombre} de {next_anio}"
    ws.cell(sr, 8).value = f"=+N{tr}"
    ws.cell(sr, 11).value = f"=(G{tr})*2.5%"
    ws.cell(sr, 12).value = 2.5
    ws.cell(sr, 15).value = " "

    ws.cell(sr + 1, 5).value = "Abono a Capital "
    ws.cell(sr + 1, 8).value = f"=+M{tr}"
    ws.cell(sr + 1, 11).value = f"=+K{tr}+L{tr}"
    ws.cell(sr + 1, 12).value = "**"
    ws.cell(sr + 1, 13).value = f"=+K{sr + 1}*L{sr}/K{sr}"
    ws.cell(sr + 1, 14).value = " "

    ws.cell(sr + 2, 5).value = "Abono Intereses "
    ws.cell(sr + 2, 8).value = f"=+K{tr}+L{tr}"
    ws.cell(sr + 2, 15).value = " "

    wb.save(ruta)
    wb.close()

    logger.info(
        f"Bloque '{nuevo_label}' creado: {len(filas_previas)} arrastradas + "
        f"{len(altas or [])} altas = {len(all_filas)} filas"
    )
    return {"label": nuevo_label, "filas": len(all_filas), "altas": len(altas or [])}


def escribir_pagos(ruta: str, pagos: list[dict]) -> dict:
    """Escribe pagos del sistema en el bloque actual de CXCOBRAR y hojas individuales.

    pagos: [{placa, fecha_pago, valor_pagado, intereses_mora, numero_factura,
             dias, intereses, capital, saldo_nuevo}]
    Retorna {"escritos_bloque", "escritos_hoja", "omitidos"}.
    """
    wb = openpyxl.load_workbook(ruta, data_only=False)
    ws = wb["CXCOBRAR"]
    bloques = localizar_bloques(ws)
    if not bloques:
        wb.close()
        return {"escritos_bloque": 0, "escritos_hoja": 0, "omitidos": 0}

    ultimo = bloques[-1]
    fill_pago = PatternFill(patternType="solid", fgColor=color_mes(ultimo["mes"]))

    # Muestra de relleno ya existente en el bloque (mantiene el color del mes)
    for r in range(ultimo["datos_inicio"], ultimo["datos_fin"] + 1):
        f = ws.cell(r, 4).fill
        if f and f.patternType == "solid":
            fg = f.fgColor
            if fg and ((fg.type == "theme" and fg.theme not in (None, 0, 1)) or
                       (fg.type == "rgb" and fg.rgb not in (None, "00000000", "FFFFFFFF"))):
                fill_pago = copy(f)
                break

    placa_rows: dict[str, list[int]] = {}
    for r in range(ultimo["datos_inicio"], ultimo["datos_fin"] + 1):
        p = str(ws.cell(r, 3).value or "").strip().upper()
        if p:
            placa_rows.setdefault(p, []).append(r)

    escritos_bloque = 0
    escritos_hoja = 0
    omitidos = 0

    for pago in pagos:
        placa = (pago.get("placa") or "").strip().upper()
        if not placa:
            omitidos += 1
            continue

        fecha_p = pago["fecha_pago"]
        if isinstance(fecha_p, date) and not isinstance(fecha_p, datetime):
            fecha_p = datetime(fecha_p.year, fecha_p.month, fecha_p.day)

        # --- Bloque CXCOBRAR ---
        rows = placa_rows.get(placa, [])
        if rows:
            # Siempre la primera fila de la placa (placas duplicadas = 2 créditos;
            # el sistema no puede distinguirlas, se acumula en la primera).
            target = rows[0]

            # Dedup exacto por factura en columna P (libre en Creemos.xlsx)
            facturas_row = str(ws.cell(target, 16).value or "")
            factura = pago.get("numero_factura", "")
            if factura and factura in facturas_row:
                omitidos += 1
            else:
                existing_n = ws.cell(target, 14).value
                if isinstance(existing_n, (int, float)) and float(existing_n) > 0:
                    ws.cell(target, 14).value = float(existing_n) + float(pago["valor_pagado"])
                else:
                    ws.cell(target, 14).value = float(pago["valor_pagado"])
                ws.cell(target, 9).value = fecha_p
                if pago.get("intereses_mora") and float(pago["intereses_mora"]) > 0:
                    ws.cell(target, 12).value = float(pago["intereses_mora"])
                if factura:
                    ws.cell(target, 16).value = (
                        f"{facturas_row}, {factura}" if facturas_row.strip() else factura
                    )
                ws.cell(target, 4).fill = fill_pago
                escritos_bloque += 1

        # --- Hoja individual ---
        if placa in wb.sheetnames:
            if _append_pago_hoja(wb[placa], pago, fecha_p):
                escritos_hoja += 1
        elif not rows:
            omitidos += 1

    if escritos_bloque or escritos_hoja:
        _backup(ruta)
        wb.save(ruta)
    wb.close()
    return {"escritos_bloque": escritos_bloque, "escritos_hoja": escritos_hoja, "omitidos": omitidos}


def _append_pago_hoja(ws, pago: dict, fecha_p: datetime) -> bool:
    """Agrega una fila de pago al final de la hoja individual. False si ya existe."""
    factura = pago.get("numero_factura", "")

    data_start = None
    for r in range(1, min(20, ws.max_row + 1)):
        if ws.cell(r, 1).value == "PAGOS":
            data_start = r + 1
            break
    if data_start is None:
        return False

    # Última fila de pago y dedup por recibo (col B)
    last_row = None
    for r in range(data_start, ws.max_row + 1):
        a_val = ws.cell(r, 1).value
        es_num = False
        if a_val is not None:
            if isinstance(a_val, str) and a_val.startswith("="):
                es_num = True
            else:
                try:
                    int(float(str(a_val)))
                    es_num = True
                except (ValueError, TypeError):
                    pass
        if es_num:
            last_row = r
            if factura and str(ws.cell(r, 2).value or "") == factura:
                return False  # ya está escrito

    if last_row is None:
        return False
    new_row = last_row + 1

    for c in range(1, 11):
        src = ws.cell(last_row, c)
        dst = ws.cell(new_row, c)
        if src.has_style:
            dst._style = copy(src._style)

    ws.cell(new_row, 1).value = f"=1+A{last_row}"
    ws.cell(new_row, 2).value = factura
    ws.cell(new_row, 3).value = f"=+D{last_row}"
    ws.cell(new_row, 4).value = fecha_p
    ws.cell(new_row, 5).value = pago.get("dias", 30)
    ws.cell(new_row, 6).value = float(pago["valor_pagado"])
    ws.cell(new_row, 7).value = f"=+J{last_row}*2.5%/30*E{new_row}"
    ws.cell(new_row, 9).value = f"=+F{new_row}-G{new_row}"
    ws.cell(new_row, 10).value = f"=+J{last_row}-I{new_row}"
    return True


def verificar_bloque_mes_actual(ruta: str, db_main) -> dict | None:
    """Crea el/los bloques que falten hasta el mes actual. Retorna el último creado o None."""
    resultado = None
    for _ in range(24):  # tope de seguridad: máx 24 meses seguidos
        altas = _altas_sistema(ruta, db_main)
        r = crear_bloque_mes(ruta, altas)
        if r is None:
            break
        resultado = r
        recalcular_excel(ruta)  # valores frescos para la siguiente iteración
    return resultado


def _altas_sistema(ruta: str, db_main) -> list[dict]:
    """Créditos activos del sistema (no CARTERA-*) cuya placa no está en el último bloque."""
    from app.models.prestamo import Prestamo
    from app.models.cliente import Cliente

    placas_bloque: set[str] = set()
    try:
        wb = openpyxl.load_workbook(ruta, data_only=True)
        ws = wb["CXCOBRAR"]
        bloques = localizar_bloques(ws)
        if bloques:
            ultimo = bloques[-1]
            for r in range(ultimo["datos_inicio"], ultimo["datos_fin"] + 1):
                p = str(ws.cell(r, 3).value or "").strip().upper()
                if p:
                    placas_bloque.add(p)
        wb.close()
    except Exception as e:
        logger.warning(f"No se pudieron leer placas del bloque para altas: {e}")
        return []

    altas = []
    q = db_main.query(Prestamo).join(Cliente).filter(
        ~Cliente.cedula.like("CARTERA-%"),
        Prestamo.estado == "ACTIVO",
    ).all()
    for p in q:
        placa = (p.cliente.placa or "").strip().upper()
        if placa and placa not in placas_bloque:
            altas.append({
                "fecha_desembolso": p.fecha_inicio,
                "placa": placa,
                "cliente": p.cliente.nombre,
                "vr_credito": float(p.capital_inicial) if p.capital_inicial else None,
                "vr_cuota": float(p.valor_cuota) if p.valor_cuota else None,
                "saldo_anterior": float(p.saldo_actual) if p.saldo_actual else None,
                "fecha_inicial": p.fecha_inicio,
            })
    return altas


def recalcular_excel(ruta: str) -> bool:
    """Recalcula fórmulas con Excel COM y guarda (restaura valores cacheados)."""
    try:
        import pythoncom
        import win32com.client
    except ImportError:
        logger.warning("pywin32 no instalado; abrir y guardar Creemos.xlsx en Excel manualmente.")
        return False

    try:
        pythoncom.CoInitialize()
        try:
            xl = win32com.client.DispatchEx("Excel.Application")
            xl.Visible = False
            xl.DisplayAlerts = False
            xl.ScreenUpdating = False
            xl.EnableEvents = False
            try:
                wb = xl.Workbooks.Open(str(Path(ruta).resolve()))
                try:
                    xl.CalculateFullRebuild()
                    wb.Save()
                finally:
                    wb.Close(SaveChanges=False)
            finally:
                xl.Quit()
        finally:
            pythoncom.CoUninitialize()
        logger.info("Creemos.xlsx recalculado con Excel COM.")
        return True
    except Exception as e:
        logger.warning(f"Recálculo COM falló (abrir y guardar en Excel manualmente): {e}")
        return False
