# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Sistema de administración de préstamos (compra de taxis) de CREEMOS EN TI SAS. Reemplaza el manejo manual en Excel sin cambiar el flujo del personal, por eso el Excel sigue siendo parte central del sistema. Código, dominio y mensajes están en español. Especificaciones funcionales y reglas de negocio detalladas en `docs/` (p. ej. `02_reglas_negocio.md`, `11_sincronizacion_excel.md`).

## Comandos

Windows. Backend: FastAPI (puerto 8765). Frontend: React 19 + TS + Vite + Tailwind v3 (puerto 5173).

- Iniciar todo: `.\iniciar.bat` o `.\iniciar.ps1 [-BackendOnly|-FrontendOnly]` (ojo: ambos matan procesos `uvicorn`/`node` existentes)
- Backend: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8765` (debe ejecutarse desde `backend/`; las rutas de `database/`, `logs/`, `backups/` son relativas)
- Frontend: `cd frontend && npm run dev` — Vite hace proxy de `/api` a `localhost:8765`
- Build frontend: `cd frontend && npm run build` (`tsc -b && vite build`). Si existe `frontend/dist`, el backend lo sirve como SPA.
- Lint frontend: `cd frontend && npm run lint` (oxlint)
- Tests: `cd backend && python -m pytest tests/ -v`
- Un test: `cd backend && python -m pytest tests/test_excel_writer.py::nombre_test -v`
- Migraciones: `cd backend && alembic upgrade head` (nota: al arrancar, `create_all` también crea tablas faltantes)
- Sync de cartera por CLI: `cd backend && python sync_cartera.py [--dry-run] [--creemos RUTA] [--db RUTA]`

`tests/conftest.py` apunta `DATABASE_URL` a un SQLite temporal antes de importar la app y el fixture `client` ya viene autenticado (`admin_test` / `Test1234`).

## Arquitectura backend (`backend/app/`)

Capas: `api/` (routers, `APIRouter(prefix="/api/v1/...")`) → `services/` → `repositories/` → `models/` (SQLAlchemy), con `schemas/` (Pydantic) para I/O. Auth JWT en `security/auth.py`; configuración vía `core/config.py` (pydantic-settings, lee `.env`). Las respuestas usan un envoltorio `{"data": ...}` (ver `schemas/common.py`).

Hay **dos bases SQLite** en `backend/database/`:
- `prestamos.db` — base operacional de la app (clientes, préstamos, pagos, facturas, usuarios, configuración, logs). `app/database/database.py`.
- `cartera.db` — espejo de la cartera histórica parseada de `Creemos.xlsx` (`clientes_cartera`, `creditos`, pagos históricos, snapshots mensuales). Modelos/engine propios en `app/cartera/` (`BaseCartera`, separado de `Base`).

### Integración con Excel (lo más delicado)

Existen dos flujos distintos:

1. **Excel de clientes "activo"** (registro `Archivo` con `tipo="clientes"`, `activo=True`): al iniciar, `SyncService.sincronizar_clientes` lo importa a SQLite. `app/utils/excel_export.py` (`exportar_a_excel`, `trigger_auto_export`) escribe de vuelta solo las filas de datos preservando encabezados/formato. Actualmente solo `api/excel.py` invoca la exportación; no hay middleware de auto-export en `main.py` pese a lo que dice `AGENTS.md`.

2. **Cartera `Creemos.xlsx`** (en la raíz del repo, fuera de `backend/`): libro con la hoja `CXCOBRAR` organizada en bloques mensuales (encabezado tipo `"JULIO DE 2026"`) más una hoja individual por crédito (placa).
   - Lectura: `parser_creemos.py` / `parser_joglo.py` → `SincronizadorCartera.ejecutar()` llena `cartera.db` → `importar_a_sistema.importar_cartera_a_sistema()` pasa la cartera a `prestamos.db`.
   - Escritura: `excel_writer.py` crea el bloque del mes (`verificar_bloque_mes_actual`/`crear_bloque_mes`), escribe pagos del sistema (facturas `FACT-*`) en el bloque y en las hojas individuales (`escribir_pagos`), hace backup antes de modificar y recalcula fórmulas con Excel vía COM (`recalcular_excel`, requiere `pywin32` y Excel instalado).
   - Disparadores: startup en `main.py` (sync inicial si `creditos` está vacío + cierre de mes automático), y endpoints en `api/sync.py` (`/cartera/actualizar-excel`) y `api/excel.py`.
   - Siempre se verifica que el archivo no esté abierto en Excel (`PermissionError` → se omite o 409).

El Excel es fuente de verdad al inicio; SQLite es la fuente de verdad durante la operación.

## Frontend (`frontend/src/`)

Rutas en `App.tsx` (todas salvo `/login` bajo `ProtectedLayout`). `services/api.ts` es la instancia axios con `baseURL: '/api/v1'`, añade el token de `localStorage.access_token` y redirige a `/login` en 401; cada dominio tiene su `*.service.ts`. Estado de servidor con TanStack Query, formularios con react-hook-form + zod. Alias `@` → `src/`. Montos en pesos se manejan con `components/CurrencyInput.tsx` y `utils/currency.ts`.

## Convenciones

- `sub` del JWT es string; convertir con `int()` al decodificar.
- Montos: `Numeric(12, 0)` — pesos colombianos sin decimales.
- Tasa de interés por defecto 2.5% mensual (tabla `Configuracion`, también días de gracia y consecutivo de factura).
- No usar trailing slash en las URLs del cliente (FastAPI responde 307).
- En el primer arranque se crea el admin `jugarciamar`; la contraseña sale de `DEFAULT_ADMIN_PASSWORD` o se genera y se registra en el log.
- `SECRET_KEY` se genera aleatoriamente si no está en `.env`, así que los tokens se invalidan al reiniciar el backend.
