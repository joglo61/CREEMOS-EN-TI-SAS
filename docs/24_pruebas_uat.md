# Pruebas de aceptación (UAT) — CREEMOS EN TI SAS

Checklist para que el personal pruebe la aplicación **antes de salir a producción**. Hacerlo sobre una **copia** de los datos (nunca sobre la base real): copiar `backend/database/` y `Creemos.xlsx` a otra carpeta o usar el servidor de pruebas.

Marque cada punto con ✅ (funciona), ❌ (falla: anote qué pasó) o N/A.

Datos de referencia para validar cálculos (tasa 2.5 %):

| Caso | Saldo | Pago | Días de retraso | Intereses | Mora | Capital | Saldo nuevo |
|---|---|---|---|---|---|---|---|
| A tiempo | 30.000.000 | 1.200.000 | 0 | 750.000 | 0 | 450.000 | 29.550.000 |
| 3 días tarde | 30.000.000 | 1.200.000 | 3 | 750.000 | 0 | 450.000 | 29.550.000 |
| 7 días tarde | 30.000.000 | 1.200.000 | 7 | 750.000 | 7.000 | 443.000 | 29.557.000 |
| Pago menor al interés | 30.000.000 | 500.000 | 0 | 500.000 | 0 | 0 | 30.000.000 |
| Pago mayor a la cuota | 30.000.000 | 5.000.000 | 0 | 750.000 | 0 | 4.250.000 | 25.750.000 |

## 1. Acceso
- [ ] Ingresar con usuario y contraseña correctos → abre el Dashboard.
- [ ] Contraseña incorrecta → mensaje de error, no entra.
- [ ] 3 intentos fallidos → el usuario queda bloqueado; el administrador lo desbloquea en **Usuarios**.
- [ ] Cerrar sesión y volver a `/clientes` en el navegador → pide login.
- [ ] Usuario EMPLEADO no puede administrar **Usuarios** ni guardar cambios en **Configuración**.

## 2. Clientes
- [ ] Crear cliente con préstamo (nombre, cédula, placa, valor, cuota, primer pago) → aparece en la lista.
- [ ] Crear otro cliente con la **misma cédula** o **misma placa** → el sistema lo rechaza.
- [ ] Buscar por placa, nombre y cédula mientras se escribe.
- [ ] Editar teléfono/dirección → se guardan; cédula, placa y pagos no son editables.
- [ ] Ver cronograma estimado del cliente: primera cuota con interés = saldo × 2.5 %.
- [ ] Desactivar un cliente → sigue existiendo, marcado inactivo, con su historial.

## 3. Pagos (lo más importante)
Para cada fila de la tabla de referencia, en **Préstamos → Registrar pago**:
- [ ] El cálculo previo muestra intereses, capital y saldo nuevo iguales a la tabla.
- [ ] Al confirmar se genera la factura con número consecutivo (FACT-000001, FACT-000002…), sin saltos ni repetidos.
- [ ] El saldo del préstamo y la **fecha del próximo pago** (un mes después) se actualizan.
- [ ] Pago de valor 0 o negativo → rechazado.
- [ ] Pago con fecha anterior al período → rechazado con mensaje claro.
- [ ] Pago que cubre todo el saldo → préstamo queda **PAGADO** y no admite más pagos.
- [ ] Préstamo con primer pago el día 31 → el siguiente vencimiento queda en el último día del mes siguiente (p. ej. 28 de febrero).

## 4. Recibos / facturas
- [ ] Descargar el PDF del recibo: tiene COPIA CLIENTE y COPIA CONTABILIDAD con los mismos datos.
- [ ] El recibo muestra un solo valor **INTERESES** (normal + mora), espacio de observaciones vacío y la palabra **Firma**.
- [ ] Reimprimir una factura antigua → mismos valores que el original (no recalcula).
- [ ] Imprimir en la impresora de la oficina: tamaño y márgenes correctos.

## 5. Estados y Dashboard
- [ ] Préstamo vencido hace 5 días → sigue **ACTIVO** (gracia); vencido hace 6 → **MORA**.
- [ ] Dashboard: clientes activos, en mora, ingresos del día y capital pendiente coinciden con lo registrado en la prueba.
- [ ] Reportes: los pagos del día aparecen con sus totales.

## 6. Excel (transición)
- [ ] **Excel → Descargar**: baja `Creemos.xlsx` y abre en Excel.
- [ ] **Actualizar Excel**: los pagos registrados en la prueba aparecen en el bloque del mes (con color) y en la hoja de cada placa.
- [ ] Editar el Excel descargado, volverlo a **Subir** → los cambios se reflejan en la app.
- [ ] Subir un archivo que no es Excel → rechazado, el archivo anterior no se pierde.

## 7. Respaldos
- [ ] **Backups → Crear respaldo** → aparece en la lista con fecha y hora.
- [ ] Restaurar un respaldo en el servidor de pruebas → los datos vuelven al estado de ese momento.

## 8. Producción (después del deploy)
- [ ] La dirección abre con candado (HTTPS) desde el celular y el PC de la oficina.
- [ ] `https://<dominio>/docs` no muestra la documentación de la API.
- [ ] Reiniciar el servidor → los datos siguen ahí y hay que volver a iniciar sesión.
- [ ] El backup diario se generó (revisar `datos/backups/diario/`) y la copia externa existe.

**Resultado:** salir a producción solo con todos los puntos de las secciones 1, 3 y 4 en ✅.

Pruebas automáticas equivalentes: `backend/tests/` (motor financiero y API) y `frontend/e2e/` (navegador).
