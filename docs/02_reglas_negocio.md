# REGLAS DEL NEGOCIO
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento define todas las reglas financieras, administrativas y operativas que deberán implementarse dentro del sistema.

Estas reglas tienen prioridad sobre cualquier decisión técnica.

Si durante el desarrollo existe una contradicción entre la implementación y este documento, siempre prevalecerán las reglas aquí definidas.

---

# Regla Fundamental

El sistema deberá comportarse exactamente igual que la empresa trabaja actualmente.

El objetivo no es cambiar el negocio.

El objetivo es automatizarlo.

---

# Tasa de Interés

La empresa trabaja con una tasa mensual del:

**2.5%**

Esta tasa será configurable desde el módulo de configuración.

Sin embargo, el valor inicial será:

2.5%

---

# Fórmula de Intereses

El cálculo deberá realizarse exactamente como actualmente lo hace la empresa.

La fórmula es:

Interés = Saldo × Tasa ÷ 30 × Días

Donde:

Saldo = saldo pendiente antes del pago.

Tasa = tasa mensual.

30 = número de días utilizados por la empresa.

Días = cantidad de días transcurridos.

No deberá utilizarse otra fórmula.

---

# Días para el Cálculo

Siempre deberán utilizarse los días reales transcurridos.

No deberán utilizarse aproximaciones.

No deberán utilizarse meses comerciales diferentes a los definidos por la empresa.

---

# Fecha del Pago

Cada préstamo tendrá registrada una fecha del próximo pago.

Esta fecha será utilizada para determinar:

- Cálculo de intereses.
- Cálculo de mora.
- Estado del préstamo.

---

# Período de Gracia

La empresa maneja un período de gracia de cinco (5) días.

Este período únicamente sirve para determinar cuándo un cliente entra en estado de mora.

Sin embargo.

Cuando un cliente paga después del vencimiento.

La empresa cobra TODOS los días transcurridos.

Ejemplo.

Fecha de vencimiento

20 de julio

Fecha de pago

27 de julio

Días de mora

7 días.

No deberán descontarse los cinco días de gracia.

El cálculo deberá respetar exactamente la forma de trabajo actual de la empresa.

---

# Intereses por Mora

La mora utilizará exactamente la misma tasa del interés normal.

La fórmula será:

Mora = Saldo × Tasa ÷ 30 × Días de mora

---

# Presentación de los Intereses

Internamente existirán dos cálculos.

Intereses normales.

Intereses por mora.

Sin embargo.

El recibo únicamente mostrará un único valor llamado:

INTERESES

Ese valor será:

Intereses normales + intereses por mora.

Nunca deberán mostrarse por separado al cliente.

---

# Pago Inferior a la Cuota

Cuando el cliente pague un valor inferior a la cuota establecida.

El sistema deberá realizar el siguiente procedimiento.

1.

Calcular intereses.

2.

Calcular mora.

3.

Sumar ambos valores.

4.

Descontar primero los intereses.

5.

El dinero restante será abonado al capital.

6.

Actualizar el saldo.

---

# Pago Igual a la Cuota

Cuando el cliente pague exactamente el valor de la cuota.

El sistema calculará automáticamente.

Intereses.

Mora.

Capital.

Saldo nuevo.

Fecha siguiente.

Factura.

Historial.

Sin requerir ninguna intervención adicional del usuario.

---

# Pago Superior a la Cuota

Cuando el cliente entregue un valor superior a la cuota.

El sistema calculará normalmente los intereses correspondientes.

Todo el dinero restante será abonado directamente al capital.

Nunca se adelantarán cuotas.

Nunca se crearán pagos futuros.

Simplemente disminuirá el saldo del préstamo.

---

# Saldo Pendiente

El saldo únicamente disminuirá por el valor abonado al capital.

Los intereses nunca disminuirán el saldo.

Los intereses representan el costo financiero del préstamo.

El capital representa la amortización de la deuda.

---

# Nuevo Saldo

El nuevo saldo será calculado como:

Saldo anterior

menos

Capital abonado

Nunca deberán descontarse intereses del saldo.

---

# Fecha del Próximo Pago

Una vez registrado correctamente el pago.

El sistema actualizará automáticamente la fecha del próximo vencimiento.

Esta actualización deberá seguir exactamente las reglas utilizadas actualmente por la empresa.

---

# Estado del Cliente

Cada cliente podrá encontrarse en uno de los siguientes estados.

Al día.

Próximo a vencer.

En mora.

Cancelado.

El estado será calculado automáticamente.

Nunca será ingresado manualmente.

---

# Número de Factura

Cada pago registrado deberá generar automáticamente un número de factura consecutivo.

Características.

• Nunca podrá repetirse.

• Nunca podrá quedar vacío.

• Nunca podrá ser ingresado manualmente.

• Será administrado exclusivamente por el sistema.

El siguiente número disponible se almacenará en la tabla de configuración.

---

# Registro del Pago

Cuando un pago sea confirmado, el sistema deberá ejecutar automáticamente las siguientes acciones.

1.

Validar la información ingresada.

↓

2.

Calcular intereses.

↓

3.

Calcular mora.

↓

4.

Calcular abono a capital.

↓

5.

Calcular nuevo saldo.

↓

6.

Actualizar préstamo.

↓

7.

Registrar pago.

↓

8.

Generar factura.

↓

9.

Actualizar consecutivo de factura.

↓

10.

Actualizar historial.

↓

11.

Actualizar SQLite.

↓

12.

Actualizar archivo Excel.

↓

13.

Generar PDF.

↓

14.

Enviar a impresión.

Todas estas operaciones deberán ejecutarse como una única transacción.

---

# Transacciones

El registro de un pago nunca podrá quedar incompleto.

Si cualquiera de las operaciones falla.

Toda la transacción deberá revertirse.

Ejemplo.

Si el PDF no puede generarse.

No deberá registrarse el pago.

Si el Excel no puede actualizarse.

El sistema conservará la información en SQLite, registrará el error y notificará al usuario para que pueda volver a sincronizar posteriormente.

---

# Historial

Cada operación deberá quedar registrada permanentemente.

Nunca eliminar registros históricos.

Nunca modificar registros históricos.

Cada pago deberá conservar.

• Fecha.

• Hora.

• Usuario.

• Factura.

• Cliente.

• Saldo anterior.

• Intereses.

• Capital.

• Valor recibido.

• Nuevo saldo.

---

# Creación de Clientes

Los clientes serán creados exclusivamente desde el sistema.

No deberán agregarse directamente al archivo Excel.

El formulario deberá solicitar como mínimo.

Nombre.

Cédula.

Placa.

Teléfono.

Dirección.

Valor del préstamo.

Valor de la cuota.

Fecha del primer pago.

Observaciones.

Al guardar.

El sistema deberá.

Crear cliente.

↓

Crear préstamo.

↓

Generar cronograma.

↓

Guardar SQLite.

↓

Actualizar Excel.

↓

Mostrar confirmación.

---

# Edición de Clientes

Se permitirá modificar únicamente información administrativa.

Nombre.

Teléfono.

Dirección.

Observaciones.

Nunca deberá modificarse.

Historial.

Pagos.

Facturas.

Cronograma ejecutado.

---

# Eliminación de Clientes

No se eliminarán clientes físicamente.

Cuando un cliente deje de operar.

Simplemente cambiará su estado.

Inactivo.

De esta manera se conservará toda la información histórica.

---

# Búsqueda de Clientes

El sistema deberá permitir búsquedas por.

Placa.

Nombre.

Cédula.

La búsqueda deberá realizarse mientras el usuario escribe.

No será necesario presionar un botón de búsqueda.

---

# Cronograma

Al crear un préstamo.

El sistema generará automáticamente un cronograma estimado.

Este cronograma será únicamente informativo.

No será utilizado para realizar cálculos financieros.

Los cálculos reales siempre dependerán de.

Fecha real del pago.

Valor realmente pagado.

Estado del préstamo.

---

# Administración de Archivos Excel

El sistema no dependerá de nombres específicos de archivos.

Existirá un módulo denominado.

Administración de Archivos.

Desde este módulo será posible.

Cargar archivo de clientes.

Cargar archivo financiero.

Reemplazar archivos.

Validar estructura.

Consultar fecha de carga.

Consultar estado.

Crear respaldo antes del reemplazo.

---

# Validación de Archivos

Antes de aceptar un archivo Excel.

El sistema deberá verificar.

Que sea un archivo Excel válido.

Que pueda abrirse correctamente.

Que contenga las hojas requeridas.

Que existan todas las columnas obligatorias.

Que la información sea consistente.

Si alguna validación falla.

El archivo será rechazado.

No deberá sobrescribirse el archivo existente.

---

# Sincronización con Excel

Después de cada operación financiera exitosa.

El sistema deberá.

Actualizar SQLite.

↓

Crear copia de seguridad del Excel.

↓

Actualizar el archivo Excel.

↓

Validar que la actualización fue correcta.

↓

Registrar fecha y hora.

Si ocurre un error.

SQLite continuará siendo la fuente oficial.

El usuario podrá volver a ejecutar la sincronización posteriormente.

---

# Backups

Antes de modificar.

Base de datos SQLite.

Archivo Excel.

Configuración.

El sistema deberá generar automáticamente una copia de seguridad.

Los respaldos deberán organizarse por fecha y hora.

Nunca deberán sobrescribirse.

---

# Dashboard

El Dashboard deberá mostrar información en tiempo real.

Clientes activos.

Clientes en mora.

Ingresos del día.

Capital pendiente.

Últimos pagos.

Cantidad de pagos registrados.

Toda la información deberá obtenerse directamente desde SQLite.

Nunca desde Excel.

---

# Regla General

Siempre que exista una operación que pueda automatizarse.

El sistema deberá automatizarla.

El operador únicamente deberá ingresar la información estrictamente necesaria.

Toda la lógica financiera será responsabilidad del software.

# Impresión de Recibos

Cada pago registrado deberá generar automáticamente un recibo listo para impresión.

El usuario no deberá diligenciar ningún dato manualmente.

Toda la información será obtenida automáticamente desde la base de datos.

Cada impresión contendrá:

Recibo superior.

COPIA CLIENTE.

Recibo inferior.

COPIA CONTABILIDAD.

Ambos deberán contener exactamente la misma información.

---

# Contenido del Recibo

Cada recibo deberá mostrar como mínimo.

Empresa.

Número de factura.

Fecha.

Nombre del cliente.

Placa.

Saldo anterior.

Intereses.

Capital.

Valor recibido.

Nuevo saldo.

Observaciones.

Firma.

No deberán mostrarse datos internos utilizados por el sistema.

---

# Observaciones

El recibo deberá dejar un espacio completamente vacío destinado para observaciones escritas manualmente.

Este espacio deberá contener al menos dos líneas libres.

El sistema nunca escribirá automáticamente dentro de este espacio.

---

# Firma

En la parte inferior del recibo únicamente deberá aparecer el texto.

Firma

No deberán utilizarse textos como.

Firma del cliente.

Recibido por.

Responsable.

Únicamente deberá mostrarse.

Firma

---

# Reimpresión

Cualquier factura podrá reimprimirse desde el historial.

Cuando se reimprima una factura.

El sistema nunca recalculará intereses.

Nunca recalculará mora.

Nunca recalculará capital.

Simplemente utilizará la información almacenada cuando el pago fue registrado.

Esto garantiza que el documento reimpreso sea exactamente igual al original.

---

# Administración de Usuarios

Existirán dos tipos de usuarios.

Administrador.

Empleado.

El administrador tendrá acceso completo al sistema.

El empleado únicamente podrá registrar pagos y consultar información.

Los permisos deberán validarse siempre desde el Backend.

Nunca desde el Frontend.

---

# Configuración

El sistema deberá permitir modificar sin cambiar código.

Nombre de la empresa.

NIT.

Dirección.

Teléfono.

Logo.

Tasa de interés.

Días de gracia.

Número siguiente de factura.

Ubicación de los archivos Excel.

Ubicación donde se almacenarán los recibos PDF.

Toda esta información será almacenada en SQLite.

---

# Registro de Actividades

El sistema deberá registrar automáticamente.

Inicio de sesión.

Cierre de sesión.

Creación de clientes.

Edición de clientes.

Registro de pagos.

Generación de facturas.

Carga de archivos Excel.

Sincronización.

Errores.

Toda esta información permitirá realizar auditorías futuras.

---

# Validaciones

Nunca permitir.

Pagos negativos.

Pagos iguales a cero.

Clientes duplicados.

Placas duplicadas.

Facturas repetidas.

Archivos Excel inválidos.

Campos obligatorios vacíos.

Fechas inconsistentes.

Si una validación falla.

La operación no deberá ejecutarse.

El usuario deberá recibir un mensaje claro indicando el problema.

---

# Integridad Financiera

Toda la información financiera deberá conservarse permanentemente.

Nunca eliminar.

Pagos.

Facturas.

Clientes.

Préstamos.

Historial.

La integridad de la información tendrá prioridad sobre cualquier otra característica del sistema.

---

# Escalabilidad

Aunque la primera versión del sistema cubre únicamente la operación actual de CREEMOS EN TI SAS.

Toda la arquitectura deberá permitir agregar posteriormente.

Facturación electrónica.

Aplicación móvil.

Portal de clientes.

Integración con WhatsApp.

Reportes financieros avanzados.

Nuevos tipos de préstamos.

Múltiples sucursales.

Múltiples cajas.

Sin necesidad de rehacer el proyecto.

---

# Responsabilidad del Sistema

El sistema será responsable de.

Calcular.

Actualizar.

Registrar.

Generar.

Sincronizar.

Respaldar.

Imprimir.

El usuario únicamente será responsable de ingresar la información que el sistema no pueda conocer automáticamente.

---

# Principio Fundamental

Siempre que exista una decisión entre facilitar el trabajo del operador o aumentar la complejidad del sistema.

Deberá priorizarse facilitar el trabajo del operador.

El sistema existe para servir a la empresa.

La empresa no deberá modificar su forma de trabajar para adaptarse al sistema.

---

# Declaración Final

Este documento define oficialmente todas las reglas de negocio del Sistema de Administración de Préstamos de CREEMOS EN TI SAS.

Toda implementación realizada durante el desarrollo deberá respetar estrictamente estas reglas.

Cualquier modificación futura deberá actualizar este documento antes de implementarse en el software.

---

**Fin del documento.**