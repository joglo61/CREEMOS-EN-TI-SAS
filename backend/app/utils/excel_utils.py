from __future__ import annotations
import unicodedata
from typing import Any

COL_ALIASES_CLIENTES: dict[str, list[str]] = {
    "nombre": ["nombre", "nombres", "name"],
    "cedula": ["cedula", "cédula", "cc", "documento", "identificacion", "identificación", "id"],
    "placa": ["placa", "placa_vehiculo", "vehiculo", "vehículo", "matricula", "matrícula"],
    "telefono": ["telefono", "teléfono", "celular", "movil", "móvil", "cel", "phone"],
    "direccion": ["direccion", "dirección", "address", "domicilio"],
    "correo": ["correo", "email", "e-mail", "mail"],
}

COL_ALIASES_FINANCIERO: dict[str, list[str]] = {
    "fecha": ["fecha", "date", "ulti fecha", "última fecha", "ultima fecha", "prox fecha", "próxima fecha", "proxima fecha"],
    "cliente": ["cliente", "nombre", "cedula", "cédula", "identificacion", "identificación", "placa"],
    "capital": ["capital", "capital_inicial", "monto", "cta inicial", "cta_inicial", "valor_inicial"],
    "cuota": ["cuota", "cuota_mensual", "pago", "valor_cuota"],
    "saldo": ["saldo", "saldo_actual", "balance"],
    "estado": ["estado", "status", "situacion"],
}

ALIASES_POR_TIPO = {
    "clientes": COL_ALIASES_CLIENTES,
    "financiero": COL_ALIASES_FINANCIERO,
}

COLUMNAS_ESPERADAS = {
    "clientes": ["nombre", "cedula", "placa", "telefono", "direccion", "correo"],
    "financiero": ["fecha", "cliente", "capital", "cuota", "saldo", "estado"],
}

COLUMNAS_REQUERIDAS = {
    "clientes": {"nombre", "placa"},
    "financiero": {"cuota", "saldo"},
}


def normalizar(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ASCII", "ignore").decode("ASCII").strip().lower()


def detectar_encabezados(ws: Any, tipo: str, max_scan: int = 20):
    aliases = ALIASES_POR_TIPO.get(tipo, {})
    all_known: set[str] = set()
    for lst in aliases.values():
        for a in lst:
            all_known.add(normalizar(a))

    best_row = 0
    best_headers: list[str] = []
    best_score = 0

    for i, row in enumerate(ws.iter_rows(max_row=max_scan, values_only=True), 1):
        headers = [str(v) if v is not None else "" for v in row]
        norm = [normalizar(h) for h in headers]
        score = sum(1 for h in norm if h in all_known)
        if score > best_score:
            best_score = score
            best_row = i
            best_headers = headers

    if best_row == 0:
        best_row = 1
        for row in ws.iter_rows(max_row=1, values_only=True):
            best_headers = [str(v) if v is not None else "" for v in row]

    return best_row, best_headers


def construir_mapa(headers: list[str], tipo: str) -> dict[str, int]:
    aliases = ALIASES_POR_TIPO.get(tipo, {})
    norm = [normalizar(h) for h in headers]
    mapa: dict[str, int] = {}
    for expected, alias_list in aliases.items():
        alias_norm = [normalizar(a) for a in alias_list]
        for idx, h_norm in enumerate(norm):
            if h_norm in alias_norm:
                mapa[expected] = idx
                break
    return mapa


def validar_columnas(headers: list[str], tipo: str) -> list[str]:
    requeridas = COLUMNAS_REQUERIDAS.get(tipo, set())
    mapa = construir_mapa(headers, tipo)
    encontradas = set(mapa.keys())
    faltantes = requeridas - encontradas
    if faltantes:
        raise ValueError(
            f"Columnas requeridas faltantes: {', '.join(sorted(faltantes))}. "
            f"Columnas detectadas: {headers}."
        )
    return headers
