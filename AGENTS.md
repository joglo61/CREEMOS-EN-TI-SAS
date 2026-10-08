# CREEMOS EN TI SAS - Contexto del Proyecto

## Stack
- Backend: Python FastAPI + SQLAlchemy + SQLite (puerto 8765)
- Frontend: React 19 + TypeScript + Vite + TailwindCSS v3 (puerto 5173)

## Inicio Rápido
- `.\iniciar.bat` o `.\iniciar.ps1` - Inicia backend y frontend
- Backend manual: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8765`
- Frontend manual: `cd frontend && npm run dev`
- Tests: `cd backend && python -m pytest tests/ -v`

## Comandos
- Build frontend: `cd frontend && npm run build`
- Migraciones: `cd backend && alembic upgrade head`
- Tests Excel: `cd backend && python test_excel.py`

## Híbrido Excel-SQLite
- **Startup**: Al iniciar el backend, se sincronizan clientes desde el Excel activo a SQLite
- **Auto-export**: Tras cada operación de escritura (crear/actualizar/eliminar clientes, préstamos, pagos, facturas) el sistema exporta automáticamente los datos actualizados de vuelta al archivo Excel
- El Excel original se conserva con su estructura (encabezados, formato); solo se actualizan las filas de datos
- `exportar_a_excel()` en `app/utils/excel_export.py` — lee datos actuales de SQLite y escribe al Excel
- `auto_export_background()` — wrapper que captura errores y escribe logs
- Middleware en `main.py` intercepta POST/PUT/PATCH/DELETE en rutas de escritura y dispara auto-export
- El Excel es la fuente de verdad al inicio; SQLite es la fuente de verdad operacional durante la sesión

## Convenciones
- `sub` en JWT debe ser string; convertir a `int()` al decodificar
- Montos: `Numeric(12, 0)` para pesos colombianos sin decimales
- Tasa interés: 2.5% mensual
- Router prefixes: APIRouter(prefix="/api/v1/...")
- NO usar trailing slashes en URLs al cliente (FastAPI redirects 307)
