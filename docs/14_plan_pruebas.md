# PLAN DE PRUEBAS
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento define el plan oficial de pruebas del Sistema de Administración de Préstamos.

Su propósito es garantizar que cada funcionalidad implementada funcione correctamente antes de ser utilizada en producción.

Toda funcionalidad deberá ser probada.

Ningún módulo podrá considerarse terminado sin superar satisfactoriamente las pruebas correspondientes.

---

# Filosofía

Las pruebas deberán validar que el sistema funciona exactamente igual que el proceso manual actual de la empresa.

El objetivo no es únicamente comprobar que el software no presenta errores.

El objetivo es garantizar que los cálculos financieros sean correctos y que la información nunca se pierda.

---

# Tipos de Pruebas

El proyecto deberá incluir.

Pruebas unitarias.

Pruebas de integración.

Pruebas funcionales.

Pruebas de aceptación.

Pruebas de rendimiento.

Pruebas de recuperación.

---

# Pruebas Unitarias

Las pruebas unitarias validarán funciones individuales.

Especialmente.

Cálculo de intereses.

Cálculo de mora.

Abono a capital.

Actualización del saldo.

Generación del número de factura.

Actualización de fechas.

Validación de archivos Excel.

Generación del PDF.

---

# Pruebas de Integración

Las pruebas de integración comprobarán que los módulos funcionan correctamente entre sí.

Ejemplo.

Registrar pago.

↓

Actualizar SQLite.

↓

Actualizar Excel.

↓

Generar PDF.

↓

Actualizar Dashboard.

↓

Registrar Logs.

Todo el proceso deberá finalizar correctamente.

---

# Pruebas Funcionales

Cada caso de uso definido en la documentación deberá tener al menos una prueba funcional.

Ejemplos.

Crear cliente.

Editar cliente.

Buscar cliente.

Registrar pago.

Reimprimir factura.

Consultar historial.

Cargar archivos Excel.

Restaurar respaldo.

---

# Pruebas de Aceptación

Las pruebas de aceptación serán realizadas simulando el trabajo diario de la empresa.

Se verificará que el sistema permita realizar las tareas habituales sin modificar el flujo de trabajo existente.

---

# Prueba 1

## Inicio de Sesión

Objetivo.

Verificar que un usuario pueda ingresar correctamente.

Resultado esperado.

Acceso autorizado.

Dashboard cargado.

Registro del inicio de sesión.

---

# Prueba 2

## Buscar Cliente

Ingresar una placa existente.

Resultado esperado.

El cliente deberá aparecer inmediatamente.

Toda la información deberá cargarse correctamente.

---

# Prueba 3

## Registrar Pago Normal

Seleccionar un cliente.

Ingresar exactamente el valor de la cuota.

Resultado esperado.

Intereses calculados.

Capital calculado.

Saldo actualizado.

Factura generada.

PDF generado.

SQLite actualizado.

Excel actualizado.

Dashboard actualizado.

---

# Prueba 4

## Pago Superior a la Cuota

Ingresar un valor mayor al de la cuota.

Resultado esperado.

Los intereses se calculan normalmente.

El excedente se aplica completamente al capital.

El nuevo saldo disminuye correctamente.

No se generan cuotas futuras.

---

# Prueba 5

## Pago con Mora

Registrar un pago con más de cinco días de retraso.

Resultado esperado.

Calcular intereses normales.

Calcular intereses por mora.

Sumar ambos valores.

Mostrar únicamente el campo.

Intereses.

Actualizar correctamente el saldo.

---

# Prueba 6

## Reimpresión

Seleccionar una factura antigua.

Resultado esperado.

El sistema deberá abrir exactamente el mismo PDF.

No recalcular información.

No modificar datos.

---

# Prueba 7

## Registro de Cliente

Objetivo.

Verificar la creación completa de un nuevo cliente.

Procedimiento.

Ingresar toda la información solicitada.

Guardar.

Resultado esperado.

Cliente creado.

Préstamo creado.

Cronograma generado.

SQLite actualizado.

Excel actualizado.

Registro en logs.

Mensaje de confirmación.

---

# Prueba 8

## Cliente Duplicado

Intentar registrar un cliente con una placa ya existente.

Resultado esperado.

El sistema deberá impedir el registro.

Mostrar un mensaje indicando que la placa ya existe.

No modificar ninguna información.

---

# Prueba 9

## Factura Consecutiva

Registrar dos pagos consecutivos.

Resultado esperado.

Cada factura deberá recibir un número consecutivo.

Nunca deberán repetirse.

---

# Prueba 10

## Actualización de Excel

Registrar un pago.

Resultado esperado.

SQLite actualizado.

Archivo Excel actualizado.

La información deberá coincidir exactamente.

---

# Prueba 11

## Error durante Sincronización

Simular un error al actualizar Excel.

Resultado esperado.

SQLite conserva el pago.

Registrar incidente.

Mostrar advertencia.

Permitir sincronizar nuevamente.

---

# Prueba 12

## Generación del PDF

Registrar un pago.

Resultado esperado.

Generar PDF.

Guardar PDF.

Abrir vista previa.

Mostrar dos recibos.

Cliente.

Contabilidad.

---

# Prueba 13

## Reemplazo del Archivo Excel

Cargar un nuevo archivo Excel.

Resultado esperado.

Validar estructura.

Crear respaldo.

Actualizar configuración.

Registrar en logs.

Mantener disponible la versión anterior.

---

# Prueba 14

## Restauración de Archivo

Restaurar una versión anterior.

Resultado esperado.

Crear respaldo del estado actual.

Restaurar correctamente.

Registrar la operación.

---

# Prueba 15

## Cambio de Configuración

Modificar la tasa de interés.

Resultado esperado.

Actualizar SQLite.

Registrar modificación.

Aplicar la nueva tasa únicamente a los cálculos posteriores.

---

# Prueba 16

## Inicio de Sesión Inválido

Ingresar credenciales incorrectas.

Resultado esperado.

No permitir acceso.

Registrar intento fallido.

Mostrar mensaje amigable.

---

# Prueba 17

## Permisos

Ingresar como empleado.

Intentar acceder a Configuración.

Resultado esperado.

Acceso denegado.

No mostrar información sensible.

Registrar intento.

---

# Prueba 18

## Respaldo

Crear respaldo manual.

Resultado esperado.

Respaldar.

SQLite.

Excel.

Configuración.

Registrar respaldo.

Mostrar ubicación.

---

# Prueba 19

## Restauración

Restaurar un respaldo.

Resultado esperado.

Crear respaldo previo.

Restaurar.

Validar integridad.

Registrar operación.

Mostrar confirmación.

---

# Prueba 20

## Dashboard

Registrar un pago.

Resultado esperado.

Actualizar.

Ingresos.

Capital pendiente.

Últimos pagos.

Clientes en mora.

Sin necesidad de recargar la aplicación.

---

# Pruebas de Rendimiento

El sistema deberá cumplir como mínimo.

Buscar cliente.

Menos de 1 segundo.

Registrar pago.

Menos de 10 segundos.

Generar PDF.

Menos de 3 segundos.

Actualizar Dashboard.

Menos de 1 segundo.

Actualizar Excel.

Menos de 3 segundos.

---

# Pruebas de Recuperación

Simular.

Cierre inesperado.

Falla eléctrica.

Error durante sincronización.

Error durante impresión.

Resultado esperado.

No perder información.

SQLite consistente.

Posibilidad de recuperar el proceso.

---

# Pruebas de Auditoría

Verificar que cada acción importante genere un registro.

Como mínimo.

Inicio de sesión.

Registro de pago.

Creación de cliente.

Cambio de configuración.

Carga de archivo.

Generación de recibo.

Restauración.

Todos deberán aparecer correctamente en los logs.

# Criterios de Aprobación

Una funcionalidad únicamente podrá considerarse terminada cuando cumpla todos los siguientes criterios.

• Funciona correctamente.

• No presenta errores críticos.

• Supera todas las pruebas unitarias.

• Supera todas las pruebas de integración.

• Supera las pruebas funcionales.

• La documentación correspondiente está actualizada.

• Los cálculos financieros coinciden con los resultados esperados.

• La información permanece consistente después de cada operación.

---

# Pruebas de Usabilidad

El sistema también deberá ser probado desde el punto de vista del usuario.

Se verificará.

Facilidad de uso.

Tiempo necesario para registrar un pago.

Claridad de los mensajes.

Facilidad para encontrar clientes.

Facilidad para imprimir recibos.

El objetivo es que cualquier empleado pueda aprender a utilizar el sistema en muy poco tiempo.

---

# Pruebas de Seguridad

Se deberán realizar pruebas relacionadas con.

Inicio de sesión.

Permisos.

Acceso a rutas protegidas.

Usuarios sin permisos.

Intentos de modificación de datos.

Manipulación de peticiones.

Todas estas pruebas deberán confirmar que la seguridad definida en la documentación se cumple correctamente.

---

# Pruebas de Regresión

Cada vez que se agregue una nueva funcionalidad.

Deberán ejecutarse nuevamente todas las pruebas críticas.

Especialmente.

Registro de pagos.

Generación de recibos.

Actualización de Excel.

Sincronización.

Dashboard.

El objetivo será asegurar que una nueva funcionalidad no afecte las ya existentes.

---

# Registro de Resultados

Cada prueba ejecutada deberá registrar.

Nombre de la prueba.

Fecha.

Hora.

Versión del sistema.

Usuario.

Resultado.

Observaciones.

Los resultados deberán conservarse para futuras auditorías.

---

# Automatización de Pruebas

Siempre que sea posible.

Las pruebas unitarias y de integración deberán ejecutarse automáticamente.

Antes de aceptar cambios en la rama principal.

El sistema deberá comprobar que todas las pruebas continúan siendo exitosas.

---

# Entorno de Pruebas

Las pruebas deberán ejecutarse utilizando una base de datos independiente.

Nunca utilizar información real de producción.

También deberán utilizarse archivos Excel de prueba.

Los recibos generados durante las pruebas deberán almacenarse en una carpeta independiente.

---

# Datos de Prueba

El proyecto deberá incluir información de ejemplo.

Clientes.

Préstamos.

Pagos.

Facturas.

Usuarios.

Configuración.

Esta información permitirá probar rápidamente el sistema después de una instalación nueva.

---

# Cierre de una Fase

Una fase únicamente podrá darse por terminada cuando.

Todas las funcionalidades previstas estén implementadas.

Todas las pruebas sean exitosas.

Toda la documentación correspondiente esté actualizada.

No existan errores críticos pendientes.

El sistema permanezca estable.

---

# Principio Fundamental

Las pruebas representan la garantía de calidad del proyecto.

Nunca deberá considerarse terminada una funcionalidad únicamente porque compila correctamente.

Toda funcionalidad deberá demostrar mediante pruebas que cumple exactamente las reglas del negocio definidas por CREEMOS EN TI SAS.

---

# Responsabilidad de OpenCode

OpenCode deberá crear las pruebas necesarias para validar todas las funcionalidades implementadas.

No deberá asumir que una funcionalidad funciona sin haber sido probada.

Cada nuevo módulo desarrollado deberá incorporar sus pruebas correspondientes antes de considerarse finalizado.

---

# Declaración Final

Este documento define oficialmente el plan de pruebas del Sistema de Administración de Préstamos de CREEMOS EN TI SAS.

Toda funcionalidad desarrollada deberá validarse utilizando este plan antes de ser entregada para producción.

---

**Fin del documento.**