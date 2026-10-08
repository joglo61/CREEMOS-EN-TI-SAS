# DESPLIEGUE E INSTALACIÓN
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

> **Despliegue web en VPS (Linux + Docker + HTTPS):** ver `23_despliegue_vps.md`. Este documento describe la instalación local en Windows.

---

# Objetivo

Este documento define cómo deberá instalarse, configurarse, actualizarse y ejecutarse el Sistema de Administración de Préstamos.

El objetivo es que cualquier computador de la empresa pueda instalar el sistema sin necesidad de realizar configuraciones complejas.

Toda la instalación deberá ser sencilla, segura y repetible.

---

# Filosofía

El sistema será una aplicación de escritorio.

No dependerá de internet para funcionar.

Toda la información permanecerá almacenada localmente.

El sistema únicamente necesitará conexión a internet cuando en futuras versiones se implementen servicios externos.

---

# Sistema Operativo

La primera versión será desarrollada para.

Windows 10.

Windows 11.

No será obligatorio soportar Linux ni macOS en esta versión.

Sin embargo.

La arquitectura deberá permitir una futura adaptación.

---

# Componentes del Sistema

La aplicación estará compuesta por.

Frontend.

Backend.

SQLite.

Archivos Excel.

Recibos PDF.

Respaldos.

Todos estos componentes deberán instalarse automáticamente.

---

# Estructura de Carpetas

Después de la instalación.

La estructura será.

Sistema/

backend/

frontend/

database/

data/

backups/

recibos/

logs/

docs/

config/

Todos los directorios deberán crearse automáticamente.

---

# Base de Datos

Durante la primera ejecución.

El sistema verificará si existe la base de datos.

Si no existe.

La creará automáticamente.

También generará.

Configuración inicial.

Usuario administrador.

Parámetros del sistema.

No será necesaria ninguna intervención manual.

---

# Primera Ejecución

Cuando el sistema se ejecute por primera vez.

Deberá solicitar.

Archivo Excel de clientes.

Archivo Excel financiero.

Nombre de la empresa.

Datos básicos de configuración.

Una vez finalizado este proceso.

El sistema quedará listo para utilizarse.

---

# Actualizaciones

Las futuras actualizaciones nunca deberán eliminar.

Clientes.

Préstamos.

Pagos.

Facturas.

Configuraciones.

Usuarios.

Archivos Excel.

Respaldos.

Toda actualización deberá preservar la información existente.

---

# Migraciones

Si una nueva versión requiere modificar la base de datos.

La actualización deberá ejecutarse automáticamente utilizando Alembic.

Nunca modificar SQLite manualmente.

Toda modificación estructural deberá realizarse mediante migraciones.

---

# Instalación de Dependencias

El instalador deberá verificar automáticamente.

Python.

SQLite.

Dependencias del Backend.

Dependencias del Frontend.

Si alguna dependencia no existe.

El sistema deberá instalarla o informar claramente al usuario.

---

# Configuración Inicial

Después de instalar.

El sistema deberá crear automáticamente.

Usuario administrador.

Configuración por defecto.

Número inicial de factura.

Tasa inicial.

Días de gracia.

Rutas de almacenamiento.

Toda esta información podrá modificarse posteriormente desde el sistema.

---

# Configuración de Carpetas

Si alguna carpeta necesaria no existe.

El sistema deberá crearla automáticamente.

Ejemplos.

backups/

recibos/

logs/

data/

No deberán producirse errores por carpetas inexistentes.

---

# Respaldos

Antes de instalar una actualización.

El sistema deberá generar automáticamente un respaldo de.

SQLite.

Archivos Excel.

Configuración.

Esto permitirá regresar a una versión anterior si ocurre algún inconveniente.

---

# Verificación

Al finalizar la instalación.

El sistema comprobará.

SQLite.

Frontend.

Backend.

API.

Configuración.

Archivos.

Permisos.

Si todo es correcto.

Mostrará un mensaje indicando que el sistema está listo para utilizarse.

---

# Proceso de Actualización

Toda actualización deberá seguir el siguiente flujo.

Crear respaldo.

↓

Verificar versión actual.

↓

Aplicar migraciones de SQLite.

↓

Actualizar Backend.

↓

Actualizar Frontend.

↓

Verificar integridad.

↓

Validar configuración.

↓

Iniciar servicios.

↓

Mostrar confirmación.

Si cualquiera de estos pasos falla.

La actualización deberá detenerse.

Nunca deberá dejar el sistema en un estado inconsistente.

---

# Recuperación ante Fallos

Si una actualización falla.

El sistema deberá.

Detener el proceso.

↓

Restaurar el respaldo creado previamente.

↓

Validar la integridad.

↓

Registrar el incidente.

↓

Informar al usuario.

Nunca deberá perderse información durante una actualización.

---

# Configuración del Backend

El Backend deberá iniciarse automáticamente.

Configuraciones iniciales.

Puerto.

Host.

Ubicación de SQLite.

Ruta de respaldos.

Ruta de recibos.

Ruta de logs.

Ruta de archivos Excel.

Toda esta información deberá almacenarse en SQLite y podrá modificarse desde el sistema.

---

# Configuración del Frontend

El Frontend deberá iniciar automáticamente conectado al Backend.

No deberá requerirse configuración manual del usuario.

Las direcciones de conexión deberán obtenerse automáticamente desde la configuración del sistema.

---

# Configuración de Impresión

Durante la instalación.

El sistema detectará las impresoras disponibles.

Permitirá seleccionar una impresora predeterminada.

Esta configuración podrá modificarse posteriormente.

---

# Configuración de Archivos Excel

Después de la primera instalación.

El sistema solicitará.

Archivo Excel correspondiente a la base de datos.

Archivo Excel correspondiente al cálculo financiero.

Una vez cargados.

Ambos archivos quedarán administrados por el sistema.

No será necesario volver a seleccionarlos salvo que el administrador desee reemplazarlos.

---

# Configuración del Usuario Administrador

Durante la primera ejecución.

El sistema solicitará.

Nombre.

Usuario.

Contraseña.

Confirmación de contraseña.

Este usuario tendrá permisos completos sobre el sistema.

Posteriormente podrá crear nuevos usuarios.

---

# Validación del Entorno

Antes de iniciar.

El sistema verificará.

Existencia de SQLite.

Permisos de escritura.

Espacio disponible.

Acceso a carpetas.

Disponibilidad de la impresora.

Estado de los archivos Excel.

Si alguna validación falla.

Mostrar un mensaje claro indicando el problema.

---

# Inicio Automático

Una vez instalado.

El usuario únicamente deberá ejecutar la aplicación.

El sistema iniciará automáticamente.

Backend.

↓

Base de datos.

↓

Servicios.

↓

Frontend.

↓

Pantalla de inicio de sesión.

El usuario nunca deberá iniciar procesos manualmente.

---

# Registros de Instalación

Toda instalación deberá generar un registro.

Información.

Versión instalada.

Fecha.

Hora.

Usuario.

Equipo.

Resultado.

Observaciones.

Esto facilitará el soporte técnico.

---

# Desinstalación

Si en el futuro se implementa un desinstalador.

Nunca deberá eliminar automáticamente.

Base de datos.

Recibos.

Respaldos.

Archivos Excel.

Logs.

El usuario decidirá si desea eliminar estos datos.

Por defecto.

Toda la información deberá conservarse.

---

# Portabilidad

La aplicación deberá poder copiarse a otro computador.

Restaurando.

SQLite.

Archivos Excel.

Configuración.

Respaldos.

Recibos.

El sistema deberá reconocer automáticamente estos archivos al iniciar.

---

# Compatibilidad de Versiones

Cada versión del sistema deberá ser compatible con la estructura de datos creada por la versión anterior.

Cuando esto no sea posible.

Las migraciones deberán ejecutarse automáticamente.

Nunca solicitar modificaciones manuales de la base de datos.

# Seguridad durante el Despliegue

Toda instalación deberá ejecutarse utilizando los permisos necesarios para crear las carpetas y archivos requeridos por el sistema.

Nunca deberán utilizarse permisos de administrador cuando no sean necesarios.

Las credenciales configuradas durante la instalación deberán almacenarse de forma segura.

Nunca deberán guardarse contraseñas en texto plano.

---

# Verificación Posterior a la Instalación

Al finalizar la instalación, el sistema ejecutará automáticamente una serie de verificaciones.

Como mínimo deberá comprobar.

• La base de datos SQLite puede abrirse correctamente.

• El Backend responde correctamente.

• El Frontend puede comunicarse con la API.

• Los directorios existen.

• Los permisos de escritura funcionan.

• La impresora configurada está disponible (si existe).

• Los archivos Excel están correctamente registrados.

• La configuración inicial fue creada.

Si todas las verificaciones son exitosas.

El sistema mostrará el mensaje.

Sistema instalado correctamente.

---

# Estructura Final del Sistema

Después de la instalación la estructura recomendada será.

Sistema/

├── backend/

├── frontend/

├── database/

│   └── prestamos.db

├── data/

│   ├── clientes.xlsx

│   └── intereses.xlsx

├── recibos/

│   ├── 2026/

│   └── ...

├── backups/

│   ├── sqlite/

│   ├── excel/

│   └── configuracion/

├── logs/

├── config/

└── docs/

Toda esta estructura será creada automáticamente.

---

# Copias de Seguridad

El sistema generará respaldos automáticos antes de.

Actualizar la base de datos.

Reemplazar archivos Excel.

Modificar configuraciones críticas.

Restaurar información.

Estos respaldos permitirán regresar rápidamente a un estado estable.

---

# Restauración Completa

En caso de una falla grave.

El administrador podrá restaurar completamente el sistema utilizando.

Base de datos SQLite.

Archivos Excel.

Configuración.

Recibos PDF.

Respaldos.

Después de la restauración.

El sistema validará automáticamente la integridad de todos los componentes.

---

# Mantenimiento

El sistema deberá permitir realizar tareas de mantenimiento sin afectar la información.

Ejemplos.

Optimizar la base de datos.

Eliminar archivos temporales.

Reindexar SQLite.

Verificar integridad.

Actualizar configuraciones.

Estas operaciones únicamente estarán disponibles para administradores.

---

# Registro de Versiones

Cada instalación y actualización deberá registrar.

Versión.

Fecha.

Hora.

Usuario.

Equipo.

Resultado.

Observaciones.

Esto permitirá conocer exactamente cuándo fue instalada cada versión.

---

# Escalabilidad

La forma de despliegue deberá permitir agregar posteriormente.

Servidor central.

Sincronización entre sucursales.

Aplicación móvil.

Portal web.

Servicios en la nube.

Sin modificar la arquitectura principal del sistema.

---

# Recuperación ante Desastres

En caso de pérdida total del equipo.

La recuperación deberá consistir únicamente en.

Instalar el sistema.

↓

Restaurar SQLite.

↓

Restaurar archivos Excel.

↓

Restaurar configuración.

↓

Restaurar recibos.

↓

Iniciar la aplicación.

Toda la información deberá quedar disponible nuevamente.

---

# Principio Fundamental

La instalación y el despliegue del Sistema de Administración de Préstamos deberán ser completamente automáticos.

El usuario no deberá realizar configuraciones técnicas complejas.

El sistema deberá prepararse automáticamente para comenzar a trabajar desde la primera ejecución.

---

# Responsabilidad de OpenCode

Durante el desarrollo.

OpenCode deberá crear todos los scripts necesarios para facilitar la instalación y actualización del sistema.

La instalación deberá ser repetible.

Segura.

Automática.

Y mantener la integridad de toda la información existente.

---

# Declaración Final

Este documento define oficialmente el proceso de despliegue e instalación del Sistema de Administración de Préstamos de CREEMOS EN TI SAS.

Toda instalación, actualización y restauración deberá seguir estas especificaciones.

---

**Fin del documento.**