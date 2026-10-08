---
name: sincronizar-cartera-excel
description: "Usar esta skill cuando la tarea sea implementar, modificar o depurar la sincronización entre el archivo Excel de cartera Creemos.xlsx y las bases SQLite del sistema (cartera.db → prestamos.db). Se activa con menciones a: sincronizar Excel, cartera, Creemos.xlsx, CXCOBRAR, importar pagos desde Excel, snapshots mensuales de cartera, bloques mensuales, pago_del_mes, o cualquier tarea sobre el módulo de sincronización de préstamos. NO usar para lógica de negocio de intereses/cuotas que no tenga que ver con la sincronización de archivos, ni para otras partes del sistema de préstamos."
---

# Sincronización Excel ↔ SQLite (Cartera CREEMOS EN TI SAS)

> Contrato funcional del módulo de sincronización vigente. Los archivos antiguos `CUENTAS JOGLO.xlsx` y `CUENTAS POR COBRAR.xlsx` fueron reemplazados por un único archivo unificado: `Creemos.xlsx`.

---

## 1. Objetivo

Sincronizar `Creemos.xlsx` (raíz del proyecto) con las dos bases SQLite:

```
Creemos.xlsx  →  cartera.db (staging: parser + sincronizador)  →  prestamos.db (sistema: importación)
```

- `cartera.db` (`backend/database/cartera.db`): espejo completo del Excel (clientes, créditos, pagos históricos, snapshots mensuales). Se **reconstruye entera** en cada sync (borra y recarga).
- `prestamos.db` (`backend/database/prestamos.db`): base operativa del sistema. Solo recibe los **créditos vigentes** (presentes en el último bloque mensual de CXCOBRAR) con sus pagos. Los registros importados llevan cédula `CARTERA-CC<id>` y se limpian y recrean en cada importación.

---

## 2. Estructura verificada de `Creemos.xlsx`

### 2.1 Hoja `CXCOBRAR` — 8 bloques mensuales apilados (ENERO→AGOSTO DE 2026)

- El nombre del mes está en la **columna A** (ej. `ENERO DE 2026`); encabezados 2 filas abajo; datos desde ahí.
- Filas de bloque: ENERO=1, FEBRERO=111, MARZO=222, ABRIL=330, MAYO=438, JUNIO=547, JULIO=655, AGOSTO=762 (aprox., varía al editar).
- Columnas por fila de datos:
  - `B`=Fecha desembolso (fecha original del crédito)
  - `C`=Placa
  - `D`=Cliente
  - `E`=Vr.credito, `F`=Vr.Cuota
  - `G`=Saldo anterior, `H`=Fecha Inicial, `I`=Fecha Final, `J`=Dias
  - `K`=Intereses, `L`=Int. Mora, `M`=Abono K, `N`=Cuota, `O`=Saldo Final
  - **No hay columna Prenda** (a diferencia del JOGLO antiguo).
- Fórmulas cacheadas (leer con `data_only=True`): `A`=numeración, `K=(G*0.025)`, `M=N-K`, `O=G-M`.
- **Relleno de color sólido** (theme) en la celda del cliente = pagó ese mes. Cada mes usa un color distinto. Doble verificación con columna N no vacía.
- **Filas de ALTA**: cuando un crédito entra a cartera, su fila tiene fecha desembolso = fecha inicial = fecha final y montos vacíos; el relleno ahí NO es pago → `pago_del_mes = (relleno OR cuota no vacía) AND fecha_original != fecha_final`.
- Filas de totales al final de cada bloque (sin placa ni cliente) se saltan.
- Una misma placa puede aparecer 2 veces en un bloque (cliente con 2 créditos: base y `-1`); cada fila es un crédito distinto.

### 2.2 Hojas individuales (30) — historial detallado por placa

- Nombradas con la placa (`SNY460`, `WDY291-1`, ...). Sufijo `-N` = crédito adicional sobre la misma garantía.
- Encabezado: cliente, teléfono, valor crédito, cuota, fecha desembolso, plazo, placa.
- Tabla de pagos: `PAGOS, RECIBO, FECHA U. PAGO, FECHA PAGO, DIAS, CUOTA, INTERES, SALDO INTERESES, CAPITAL, SALDO REAL`.
- Hojas excluidas (`EXCLUIDAS` en `parser_joglo.py`): COMPRAS, CUPO, CAJA, CR TAMAYO, CR SUFI, CR FALABELLA, AUX.JOGLO, AUX. KARIME, AUX. FCIA, AUX.ESTELLA, AUX.BCO FALABELLA, CR CAMIONETA, CR LIBRE INVERSION.

---

## 3. Pipeline

1. **Parser** — `backend/app/cartera/parser_creemos.py` (`CreemosParser`):
   - `parse_all()` → `(creditos, pagos_hoja, snapshots)`.
   - Reusa `parse_client_sheet`, `parse_sheet_name`, `EXCLUIDAS`, `_to_int` de `parser_joglo.py` (que se mantiene solo como librería de utilidades).
   - Cada snapshot lleva `numero_bloque` (1..N), `mes_reportado`, `pago_del_mes`.
   - `parser_por_cobrar.py` ya no se usa (POR COBRAR no existe).

2. **Sincronizador** — `backend/app/cartera/sincronizador.py` (`SincronizadorCartera`):
   - Ruta por defecto: `<raíz del proyecto>/Creemos.xlsx`. CLI: `python sync_cartera.py [--dry-run] [--creemos RUTA] [--db RUTA]`.
   - Borra tablas de cartera.db y recarga: clientes, créditos (hojas), pagos históricos (`fuente="excel_creemos"`), snapshots (`origen_archivo="CREEMOS"`).
   - `_cruzar_creditos_sin_historial`: crea créditos para placas que solo existen en CXCOBRAR (sin hoja propia) con `tiene_historial_detallado=False`; placas vacías usan nombre del cliente truncado a 15 chars.
   - Migraciones inline: `ALTER TABLE snapshots_mensuales ADD COLUMN ...` para columnas nuevas (idempotentes vía try/except).

3. **Importación al sistema** — `backend/app/cartera/importar_a_sistema.py` (`importar_cartera_a_sistema`):
   - Limpia clientes `CARTERA-*` de prestamos.db (con sus préstamos, pagos y facturas) y recrea.
   - **Preserva pagos del sistema** (`FACT-*`): antes de limpiar los guarda en memoria y tras importar los re-crea (dedup por factura/fecha/valor), ajustando saldo y fecha_proximo_pago.
   - **Solo créditos del último bloque** (`numero_bloque` máximo) se importan como préstamos ACTIVOS; lo que salió del último bloque ya no está vigente.
   - **Clientes del sistema se reusan por nombre**: si el nombre calza con un cliente no-CARTERA existente (crédito creado desde el sistema que entró al Excel como alta), se reusa y su préstamo NO se recrea ni se tocan sus pagos.
   - Cada crédito vigente genera su propio préstamo (placas duplicadas en el bloque = 2 préstamos; snapshots asignados uno por crédito con pop).
   - Datos del préstamo: `capital_inicial`=Vr.credito, `valor_cuota`=Vr.Cuota, `saldo_actual`=Saldo Final (O) del último bloque (fallback: Saldo anterior G si O es None), `fecha_inicio`=col B, tasa 2.5%. `fecha_proximo_pago` = último pago real + 1 mes (base del cálculo de mora).
   - **Pagos combinados sin duplicar por mes**: pagos de la hoja individual (detallados, con recibo) + pagos de bloques (`pago_del_mes=True`, factura `BLOQ-<credito>-<bloque>`, fecha=col I). Si el mes ya está cubierto por la hoja, el pago de bloque se omite. Si dos filas del mismo crédito pagan en el mismo bloque, la 2ª se **acumula** en el pago BLOQ.
   - La placa del cliente en prestamos.db = placa de su crédito vigente (permite buscar por placa).

4. **Escritura a Excel** — `backend/app/cartera/excel_writer.py` (nuevo):
   - `localizar_bloques(ws)`: metadata de cada bloque mensual en CXCOBRAR.
   - `crear_bloque_mes(ruta, altas)`: crea el bloque del mes siguiente si el actual no existe — arrastra filas del bloque previo (G=O previo, H=I previo, I=H, N vacía, fórmulas tal cual, totales SUM, resumen Recaudo/Abono Capital/Abono Intereses), omite saldados (O<=0), agrega altas de créditos del sistema. Limpia el relleno de pago heredado de la plantilla. Auto-recalcula vía COM si detecta caché vacío.
   - `escribir_pagos(ruta, pagos)`: escribe pagos del sistema (`FACT-*`) en el bloque actual (N=valor, I=fecha, L=mora, **relleno de color del mes** en celda D) y en la hoja individual de la placa (fila nueva con fórmulas). Dedup exacto por número de factura en **columna P** del bloque y por recibo en la hoja. Placas duplicadas: siempre escribe en la primera fila de la placa (acumula N).
   - `recalcular_excel(ruta)`: Excel COM (`win32com`) — abre invisible, CalculateFullRebuild, guarda. **Obligatorio tras toda escritura openpyxl** (openpyxl borra los valores cacheados de las fórmulas).
   - `verificar_bloque_mes_actual(ruta, db_main)`: crea bloques faltantes hasta el mes en curso (rollover), con altas del sistema solo en el mes actual.

5. **Rollover automático de mes** — en `app/main.py` startup: si falta el bloque del mes actual en Creemos.xlsx, lo crea, recalcula y re-sincroniza. Se omite si el archivo está abierto en Excel.

6. **Puntos de llamada**:
   - `backend/sync_cartera.py` — CLI manual.
   - `backend/app/api/excel.py` — upload de `tipo=cartera_creemos` guarda `Creemos.xlsx` en la raíz y dispara sync+import en background; `GET /excel/estado` reporta el archivo.
   - `backend/app/api/sync.py` — `POST /sync/cartera` (sync+import), `POST /sync/cartera/actualizar-excel` (**botón bidireccional**: rollover si falta → escribe pagos del sistema al Excel → recalc COM → sync+import de vuelta) y `GET /sync/cartera/status`.
   - Frontend: `ExcelManagementPage.tsx` (tarjeta "CREEMOS (Cartera)" con botón "Actualizar Excel"), `excel.service.ts` (tipo `cartera_creemos`, método `actualizarExcelCartera`).

---

## 4. Modelo de datos (cartera.db)

`SnapshotMensual` incluye: `numero_bloque`, `pago_del_mes`, `fecha_original`, `vr_credito`, `vr_cuota`, `saldo_anterior`, `fecha_inicial/fecha_final`, `dias`, `intereses`, `interes_mora`, `abono_capital`, `cuota`, `saldo_final`, `origen_archivo="CREEMOS"`, `placa_textual`, `credito_id` (nullable).

---

## 5. Reglas y notas operativas

- **Excel bloqueado**: si `Creemos.xlsx` está abierto en Excel, openpyxl lanza `PermissionError`. Cerrar el archivo antes de sincronizar. El endpoint devuelve 409 con mensaje claro.
- **Caché de fórmulas**: openpyxl al guardar borra los valores cacheados de TODAS las fórmulas del libro. Por eso: (a) siempre recalcular con `recalcular_excel()` (Excel COM) tras escribir; (b) el parser NO depende del caché para detectar filas (filas de bloque por placa/cliente; filas de pago por cuota/recibo/fecha), solo para los montos; (c) la importación tiene fallbacks (saldo_final None → saldo_anterior).
- **Filas fantasma en hojas individuales**: filas de plantilla con numeración pero sin pago real (cuota/recibo/fecha vacíos) NO son pagos — el parser las excluye siempre.
- **Re-vinculación de snapshots**: los créditos "solo snapshot" se crean después de insertar snapshots; `_revincular_snapshots_huerfanos` les asigna `credito_id` al final (sin esto, sus pagos de bloque no se importan).
- Tasa de interés: 2.5% mensual (fórmula `K=G*0.025` y `tasa_interes=2.5` en préstamos).
- El flujo de 2 bases se mantiene a propósito: `cartera.db` es staging fiel del Excel; `prestamos.db` solo lo vigente.
- Dashboards y reportes leen de `prestamos.db` en vivo — se actualizan solos con cada pago registrado en el sistema o tras cada importación.
- Verificación típica tras cambios: `python sync_cartera.py` (~778 snapshots, ~107 créditos, ~97 clientes), luego importación (~83 clientes, ~88 préstamos vigentes, ~715 pagos), `pytest tests/ -v` (18 tests), `npm run build` en frontend.
