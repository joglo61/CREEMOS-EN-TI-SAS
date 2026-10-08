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
- Un test: `cd backend && python -m pytest tests/test_pagos.py::nombre_test -v`
- Esquema: al arrancar, `create_all` crea tablas y `main.create_tables` agrega columnas nuevas (Alembic no se usa en la BD real)
- Migración única desde Excel: `cd backend && python migrar_excel.py --dry-run --base-limpia --excel ../Creemos.xlsx` (sin `--dry-run` migra; se niega a correr dos veces)
- Conciliación del mes en paralelo (solo lectura): `cd backend && python conciliar_excel.py --excel ../Creemos.xlsx [--mes AAAA-MM | --todos]`
- E2E: `cd frontend && npm run build && npm run e2e` (Playwright; backend aislado con BD propia en `frontend/.e2e-run`)

`tests/conftest.py` apunta `DATABASE_URL` a un SQLite temporal antes de importar la app y el fixture `client` ya viene autenticado (`admin_test` / `Test1234`).

## Arquitectura backend (`backend/app/`)

Capas: `api/` (routers, `APIRouter(prefix="/api/v1/...")`) → `services/` → `repositories/` → `models/` (SQLAlchemy), con `schemas/` (Pydantic) para I/O. Auth JWT en `security/auth.py`; configuración vía `core/config.py` (pydantic-settings, lee `.env`). Las respuestas usan un envoltorio `{"data": ...}` (ver `schemas/common.py`).

Base SQLite única de operación: `backend/database/prestamos.db` (`app/database/database.py`).

### Salida del Excel (`Creemos.xlsx`)

El sistema es la **única fuente de verdad**: el servidor ya no lee ni escribe el Excel (sin sync al arrancar; `api/sync.py` y casi todo `api/excel.py` están desregistrados en `main.py`, solo queda `/api/v1/excel/exportar-todo`).
- Migración única: `backend/migrar_excel.py`. Cada fila del último bloque de CXCOBRAR = un préstamo, identificado por placa + fecha de desembolso (un taxi puede tener 2 préstamos → `Prestamo.placa`). Desde el primer bloque mandan los bloques (pagos `MIG-B…`, con mora); las hojas por placa solo aportan historia anterior (`MIG-H…`). El saldo total debe cuadrar con el Excel.
- Conciliación del mes en paralelo: `backend/conciliar_excel.py` (solo lectura).
- Reemplazos: `services/cartera_mensual.py` (`cartera_del_mes`, cartera por cobrar de un mes calculada desde los pagos; endpoints `reportes/cartera-mensual` y su `/excel`) y el historial por préstamo `prestamos/{id}/historial/excel`.
- Se conservan para migrar/conciliar: `app/cartera/parser_creemos.py` y las funciones de `parser_joglo.py`. Pendiente de borrar al apagar el Excel (fase 4): `cartera/excel_writer.py`, `importar_a_sistema.py`, `sincronizador.py`, `cartera/database.py`, `cartera/models.py`, `api/sync.py`, `services/sync_service.py`, `utils/excel_*.py`, modelo `Archivo`, `SynchronizationPage.tsx`, `sync.service.ts`, `sync_cartera.py`, `tests/test_excel_writer.py`.
- Estados MORA/ACTIVO: `PrestamoService.recalcular_estados()` se llama al abrir el dashboard y el reporte de mora.

## Frontend (`frontend/src/`)

Rutas en `App.tsx` (todas salvo `/login` bajo `ProtectedLayout`). `services/api.ts` es la instancia axios con `baseURL: '/api/v1'`, añade el token de `localStorage.access_token` y redirige a `/login` en 401; cada dominio tiene su `*.service.ts`. Estado de servidor con TanStack Query, formularios con react-hook-form + zod. Alias `@` → `src/`. Montos en pesos se manejan con `components/CurrencyInput.tsx` y `utils/currency.ts`.

## Convenciones

- `sub` del JWT es string; convertir con `int()` al decodificar.
- Montos: `Numeric(12, 0)` — pesos colombianos sin decimales.
- Tasa de interés por defecto 2.5% mensual (tabla `Configuracion`, también días de gracia y consecutivo de factura).
- No usar trailing slash en las URLs del cliente (FastAPI responde 307).
- En el primer arranque se crea el admin `jugarciamar`; la contraseña sale de `DEFAULT_ADMIN_PASSWORD` o se genera y se registra en el log.
- `SECRET_KEY` se genera aleatoriamente si no está en `.env`, así que los tokens se invalidan al reiniciar el backend.
