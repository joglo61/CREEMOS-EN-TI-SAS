# SINCRONIZACIÓN CON MICROSOFT EXCEL
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento define el funcionamiento del módulo de sincronización entre SQLite y Microsoft Excel.

El objetivo principal es permitir que la empresa continúe utilizando sus archivos Excel como apoyo operativo, mientras que SQLite se convierte en la fuente oficial de información.

Toda la sincronización deberá realizarse automáticamente.

El usuario nunca deberá modificar archivos internos del sistema.

---

# Filosofía

SQLite será la base de datos principal.

Excel será un archivo sincronizado.

Nunca deberá utilizarse Excel como fuente oficial.

Toda modificación seguirá siempre este flujo.

Usuario

↓

Sistema

↓

SQLite

↓

Excel

Nunca deberá invertirse este proceso.

---

# Archivos Administrados

El sistema administrará inicialmente dos archivos Excel.

Archivo de Base de Datos.

Archivo Financiero.

El usuario podrá reemplazar cualquiera de estos archivos desde la interfaz del sistema.

Los nombres de los archivos podrán cambiar.

El sistema nunca dependerá de nombres específicos.

---

# Administración de Archivos

Existirá un módulo denominado.

Administración de Archivos.

Desde esta pantalla el administrador podrá.

Cargar un nuevo archivo.

Reemplazar un archivo existente.

Consultar el estado.

Consultar la versión.

Consultar la fecha de carga.

Restaurar versiones anteriores.

Descargar respaldos.

Toda la administración se realizará desde esta pantalla.

---

# Primera Configuración

Cuando el sistema sea ejecutado por primera vez.

No existirán archivos configurados.

El sistema solicitará.

Archivo Excel de Base de Datos.

Archivo Excel Financiero.

Hasta que ambos archivos sean configurados.

Las funciones relacionadas permanecerán deshabilitadas.

---

# Flujo de Carga

Cuando el usuario seleccione un archivo.

El sistema realizará automáticamente.

Seleccionar archivo.

↓

Validar formato.

↓

Validar estructura.

↓

Crear respaldo.

↓

Copiar archivo.

↓

Actualizar configuración.

↓

Registrar en logs.

↓

Mostrar confirmación.

---

# Validación del Archivo

Antes de aceptar un archivo.

El sistema verificará.

Que exista.

Que sea un archivo Excel.

Que no esté dañado.

Que pueda abrirse.

Que no esté protegido.

Que contenga las hojas requeridas.

Que contenga las columnas obligatorias.

Que la estructura sea válida.

Si cualquiera de estas validaciones falla.

El archivo será rechazado.

---

# Columnas Obligatorias

El sistema deberá validar automáticamente que existan todas las columnas necesarias para realizar la sincronización.

Si falta una columna crítica.

El archivo será rechazado.

El usuario recibirá un mensaje indicando exactamente cuál columna falta.

---

# Copia del Archivo

Después de validar correctamente.

El sistema realizará una copia interna del archivo.

Nunca trabajará directamente sobre el archivo seleccionado por el usuario.

Esto evitará problemas si posteriormente el archivo original es movido, eliminado o renombrado.

---

# Ubicación Interna

Los archivos administrados por el sistema se almacenarán en.

data/

clientes.xlsx

intereses.xlsx

El usuario nunca deberá modificar estos archivos manualmente.

Toda modificación deberá realizarse mediante el sistema.

---

# Registro del Archivo

Cada archivo cargado generará un registro en SQLite.

La información almacenada será.

Tipo.

Nombre original.

Nombre interno.

Fecha de carga.

Usuario.

Versión.

Estado.

Ruta interna.

Esto permitirá mantener un historial completo de todos los archivos utilizados.

---

# Sustitución de Archivos

Cuando un administrador cargue una nueva versión.

El sistema nunca eliminará inmediatamente el archivo anterior.

Primero.

Creará un respaldo.

↓

Registrará la nueva versión.

↓

Activará el nuevo archivo.

↓

Mantendrá el anterior para recuperación.

Nunca deberán perderse versiones anteriores.

---

# Sincronización Automática

Cada vez que el sistema registre correctamente un pago.

Deberá iniciar automáticamente el proceso de sincronización.

El flujo será.

Registrar pago.

↓

Actualizar SQLite.

↓

Crear respaldo del archivo Excel.

↓

Actualizar archivo Excel.

↓

Validar actualización.

↓

Registrar resultado.

↓

Actualizar Dashboard.

↓

Finalizar proceso.

Todo este procedimiento deberá ejecutarse automáticamente.

---

# Sincronización Manual

Además de la sincronización automática.

El sistema permitirá ejecutar una sincronización manual.

Esta opción estará disponible únicamente para administradores.

Su objetivo será resolver posibles inconsistencias detectadas durante una sincronización automática.

---

# Validación Posterior

Después de actualizar el archivo Excel.

El sistema deberá comprobar.

Que el archivo pueda abrirse.

Que la información haya sido escrita correctamente.

Que no existan errores de formato.

Que las hojas permanezcan intactas.

Si alguna validación falla.

El sistema registrará el incidente.

---

# Manejo de Errores

Si ocurre un error durante la sincronización.

El sistema deberá.

Conservar la información almacenada en SQLite.

↓

Registrar el error.

↓

Mostrar un mensaje al usuario.

↓

Permitir volver a intentar la sincronización.

Nunca deberá perderse un pago debido a un error de Excel.

---

# Estado de Sincronización

El sistema mostrará permanentemente el estado de la sincronización.

Estados posibles.

Sincronizado.

Pendiente.

Error.

Procesando.

La información estará visible desde.

Dashboard.

Administración de Archivos.

Configuración.

---

# Historial de Sincronizaciones

Toda sincronización deberá quedar registrada.

Cada registro almacenará.

Fecha.

Hora.

Usuario.

Archivo.

Resultado.

Duración.

Observaciones.

Este historial permitirá auditar cualquier inconveniente ocurrido.

---

# Sustitución de Archivos

Cuando un archivo sea reemplazado.

El sistema deberá.

Crear respaldo.

↓

Copiar nuevo archivo.

↓

Actualizar configuración.

↓

Actualizar registro.

↓

Realizar validación.

↓

Mostrar confirmación.

El archivo anterior permanecerá disponible para restauración.

---

# Restauración

El administrador podrá restaurar cualquier versión anterior.

Proceso.

Seleccionar archivo.

↓

Seleccionar versión.

↓

Confirmar.

↓

Crear respaldo del estado actual.

↓

Restaurar versión.

↓

Validar.

↓

Registrar operación.

Nunca sobrescribir información sin respaldo previo.

---

# Compatibilidad

Los archivos deberán ser compatibles con.

Microsoft Excel (.xlsx)

Microsoft Excel (.xls)

No deberán aceptarse otros formatos.

CSV.

ODS.

PDF.

TXT.

No serán soportados en la primera versión.

---

# Integridad

Durante toda sincronización.

El sistema deberá preservar.

Formato.

Hojas.

Columnas.

Orden.

Información existente.

No deberá modificar elementos ajenos a la información administrada por el sistema.

---

# Rendimiento

Objetivos.

Validación del archivo.

Menos de 3 segundos.

Carga inicial.

Menos de 5 segundos.

Sincronización después de un pago.

Menos de 3 segundos.

Reemplazo de archivos.

Menos de 10 segundos.

Estos tiempos podrán variar dependiendo del tamaño del archivo.

---

# Seguridad

Únicamente los administradores podrán.

Cargar archivos.

Reemplazar archivos.

Eliminar versiones.

Restaurar respaldos.

Consultar historial completo.

Los empleados únicamente podrán visualizar el estado de sincronización.

---

# Auditoría

Toda acción relacionada con archivos Excel deberá generar un registro.

Carga.

Reemplazo.

Restauración.

Sincronización.

Error.

Cada registro almacenará.

Usuario.

Fecha.

Hora.

Archivo.

Resultado.

Observaciones.

---

# Escalabilidad

El módulo deberá permitir agregar posteriormente.

Nuevos archivos Excel.

Importaciones automáticas.

Exportaciones programadas.

Sincronización en segundo plano.

Integraciones con Google Sheets.

Sin modificar la arquitectura existente.

---

# Principio Fundamental

Microsoft Excel continuará formando parte del flujo de trabajo de la empresa.

Sin embargo.

Toda la lógica del negocio dependerá exclusivamente de SQLite.

Excel será siempre una representación sincronizada de la información oficial.

Nunca la fuente principal de datos.

# Recuperación ante Fallos

Si durante cualquier proceso de sincronización ocurre un error inesperado.

El sistema deberá ejecutar el siguiente procedimiento.

Detectar el error.

↓

Cancelar la escritura en el archivo Excel.

↓

Conservar la información almacenada en SQLite.

↓

Registrar el incidente.

↓

Notificar al usuario.

↓

Permitir reintentar la sincronización.

Nunca deberá perderse información financiera debido a un error de sincronización.

---

# Consistencia de la Información

Toda la información almacenada en SQLite deberá ser idéntica a la información sincronizada en los archivos Excel.

Si el sistema detecta diferencias.

Deberá informar al administrador.

Nunca deberá modificar automáticamente la información sin autorización.

---

# Verificación de Integridad

Después de cada sincronización el sistema realizará automáticamente una verificación.

Como mínimo comprobará.

Cantidad de registros.

Integridad de los datos.

Formato del archivo.

Estado de las hojas.

Columnas obligatorias.

Si la verificación falla.

Registrar el incidente.

Mostrar advertencia.

Mantener el respaldo disponible.

---

# Versionado de Archivos

Cada vez que un archivo sea reemplazado.

El sistema aumentará automáticamente el número de versión.

Ejemplo.

Versión 1

↓

Versión 2

↓

Versión 3

Cada versión permanecerá registrada.

Esto permitirá conocer exactamente qué archivo se encontraba activo en cualquier momento.

---

# Organización del Historial

Cada archivo conservará.

Versión.

Fecha de carga.

Usuario responsable.

Observaciones.

Estado.

Archivo asociado.

Nunca deberán eliminarse registros históricos.

---

# Requisitos Técnicos

El módulo deberá desarrollarse de forma independiente del resto del sistema.

Toda la lógica relacionada con Excel estará encapsulada dentro de un único servicio.

Ejemplo.

ExcelService

Este servicio será el único autorizado para.

Leer archivos.

Escribir archivos.

Validar estructura.

Crear respaldos.

Sincronizar información.

Restaurar versiones.

Ningún otro módulo accederá directamente a los archivos Excel.

---

# Registro en Logs

Cada operación generará automáticamente un registro.

Ejemplos.

Archivo cargado.

Archivo reemplazado.

Archivo restaurado.

Sincronización ejecutada.

Sincronización fallida.

Respaldo creado.

Cada registro deberá contener.

Usuario.

Fecha.

Hora.

Archivo.

Resultado.

Descripción.

---

# Futuras Mejoras

La arquitectura deberá permitir incorporar posteriormente.

Sincronización automática programada.

Sincronización incremental.

Integración con OneDrive.

Integración con Google Drive.

Integración con SharePoint.

Integración con Google Sheets.

Notificaciones automáticas cuando falle una sincronización.

Sin modificar el diseño principal del módulo.

---

# Principio Fundamental

El objetivo del módulo de sincronización es permitir que CREEMOS EN TI SAS continúe utilizando Microsoft Excel como herramienta de apoyo sin depender de él como base principal de información.

Toda la operación financiera dependerá exclusivamente de SQLite.

Excel existirá únicamente para mantener la compatibilidad con el flujo de trabajo actual de la empresa.

---

# Declaración Final

Este documento define oficialmente el funcionamiento del módulo de sincronización entre SQLite y Microsoft Excel.

Toda implementación deberá respetar las reglas aquí definidas.

Cualquier modificación futura deberá actualizar este documento antes de implementarse en el software.

---

**Fin del documento.**