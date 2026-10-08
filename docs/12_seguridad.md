# SEGURIDAD
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento define todas las políticas de seguridad que deberán implementarse en el Sistema de Administración de Préstamos.

El propósito es proteger la información financiera de la empresa, garantizar la integridad de los datos y controlar el acceso a todas las funcionalidades del sistema.

La seguridad deberá implementarse desde el primer día de desarrollo.

No deberá agregarse al final del proyecto.

---

# Principios

Todo el sistema deberá cumplir los siguientes principios.

• Confidencialidad.

• Integridad.

• Disponibilidad.

• Trazabilidad.

• Autenticidad.

• Responsabilidad.

---

# Autenticación

Todo usuario deberá autenticarse antes de utilizar el sistema.

No existirá ninguna funcionalidad pública.

Todo acceso requerirá.

Usuario.

Contraseña.

Las credenciales serán verificadas por el Backend.

Nunca por el Frontend.

---

# Usuarios

Cada usuario tendrá una cuenta individual.

No deberán compartirse cuentas.

Cada acción realizada dentro del sistema deberá poder asociarse a un único usuario.

Esto permitirá realizar auditorías posteriormente.

---

# Contraseñas

Las contraseñas nunca deberán almacenarse en texto plano.

Deberán cifrarse utilizando algoritmos seguros.

El sistema nunca deberá poder recuperar la contraseña original.

Únicamente podrá verificar si la contraseña ingresada coincide con el hash almacenado.

---

# Cambio de Contraseña

Todo usuario podrá cambiar su contraseña.

El proceso será.

Ingresar contraseña actual.

↓

Ingresar nueva contraseña.

↓

Confirmar nueva contraseña.

↓

Guardar.

↓

Cerrar sesiones activas.

↓

Solicitar nuevamente el inicio de sesión.

---

# Recuperación de Contraseña

La primera versión no implementará recuperación automática.

Únicamente un administrador podrá restablecer la contraseña de otro usuario.

El sistema generará una contraseña temporal.

El usuario deberá cambiarla en el siguiente inicio de sesión.

---

# Roles

Inicialmente existirán dos roles.

Administrador.

Empleado.

Toda autorización dependerá exclusivamente del rol asignado.

---

# Permisos del Administrador

Podrá realizar todas las operaciones.

Clientes.

Préstamos.

Pagos.

Facturación.

Usuarios.

Configuración.

Archivos.

Respaldos.

Logs.

Sincronización.

Dashboard.

---

# Permisos del Empleado

Podrá.

Buscar clientes.

Consultar clientes.

Registrar pagos.

Consultar historial.

Reimprimir recibos.

Consultar Dashboard.

No podrá.

Crear usuarios.

Modificar configuración.

Restaurar respaldos.

Reemplazar archivos Excel.

Modificar parámetros financieros.

---

# Tokens

La autenticación utilizará JWT.

Cada sesión tendrá un token independiente.

Toda solicitud protegida deberá incluir dicho token.

Si el token expira.

El usuario deberá autenticarse nuevamente.

---

# Expiración de la Sesión

Las sesiones deberán expirar automáticamente después de un período de inactividad configurable.

El sistema deberá advertir al usuario antes de cerrar la sesión.

Esto evitará accesos no autorizados cuando un equipo quede desatendido.

---

# Cierre de Sesión

Al cerrar sesión.

El sistema deberá.

Invalidar el token.

↓

Registrar el evento.

↓

Redireccionar al inicio de sesión.

No deberá mantenerse ninguna información sensible en memoria.

---

# Protección de Endpoints

Todos los endpoints protegidos deberán validar.

Autenticación.

Permisos.

Estado del usuario.

Validez del token.

Ningún endpoint deberá confiar en información enviada por el Frontend.

Toda validación se realizará en el Backend.

---

# Protección de Datos

Nunca deberán enviarse al Frontend.

Contraseñas.

Hashes.

Rutas internas.

Información técnica del servidor.

Consultas SQL.

Errores internos.

El usuario únicamente recibirá la información necesaria para realizar su trabajo.

---

# Protección de la Base de Datos

SQLite representa la fuente oficial de información del sistema.

Ningún usuario tendrá acceso directo al archivo de la base de datos.

Toda operación deberá realizarse exclusivamente mediante el Backend.

No deberán existir herramientas que permitan modificar SQLite manualmente desde la interfaz.

---

# Protección de los Archivos Excel

Los archivos Excel utilizados por el sistema tampoco deberán ser modificados directamente.

El sistema será el único encargado de.

Leer.

Validar.

Actualizar.

Respaldar.

Restaurar.

Los usuarios únicamente podrán cargar nuevas versiones desde el módulo Administración de Archivos.

---

# Protección de los Recibos

Los recibos PDF generados por el sistema representan documentos oficiales.

Una vez creados.

Nunca deberán modificarse.

Nunca deberán sobrescribirse.

Nunca deberán eliminarse automáticamente.

Cada recibo permanecerá asociado permanentemente a la factura correspondiente.

---

# Protección del Historial

Toda operación realizada dentro del sistema generará un registro histórico.

El historial será de solo lectura.

No existirá ninguna funcionalidad para modificarlo.

No existirá ninguna funcionalidad para eliminarlo.

Esto garantizará la trazabilidad completa de todas las operaciones.

---

# Validaciones

Toda información recibida por la API deberá validarse.

Como mínimo.

Campos obligatorios.

Tipos de datos.

Longitudes.

Valores mínimos.

Valores máximos.

Fechas válidas.

Relaciones existentes.

No confiar nunca en la información enviada por el Frontend.

---

# Prevención de Duplicados

El sistema deberá impedir.

Clientes duplicados.

Placas duplicadas.

Cédulas duplicadas.

Usuarios duplicados.

Facturas repetidas.

Archivos duplicados activos.

Estas validaciones deberán realizarse antes de guardar la información.

---

# Protección contra Manipulación

Los cálculos financieros nunca deberán depender de información enviada por el navegador.

El Backend recalculará.

Intereses.

Mora.

Capital.

Nuevo saldo.

Número de factura.

Toda la lógica financiera permanecerá protegida.

---

# Manejo de Errores

Cuando ocurra un error.

El usuario recibirá un mensaje sencillo.

Ejemplos.

No fue posible registrar el pago.

Archivo inválido.

Cliente no encontrado.

Nunca mostrar.

Stack traces.

Consultas SQL.

Mensajes internos de Python.

Rutas del servidor.

Información técnica.

Los detalles completos únicamente deberán almacenarse en los logs.

---

# Registro de Actividades

El sistema registrará automáticamente.

Inicio de sesión.

Cierre de sesión.

Registro de pagos.

Creación de clientes.

Edición de clientes.

Carga de archivos.

Sincronización.

Generación de recibos.

Restauración de respaldos.

Errores.

Cada registro incluirá.

Fecha.

Hora.

Usuario.

Acción.

Resultado.

Descripción.

---

# Auditoría

El administrador podrá consultar todos los registros de auditoría.

La información será únicamente de lectura.

Permitirá filtrar por.

Usuario.

Fecha.

Acción.

Módulo.

Resultado.

Esto facilitará la investigación de cualquier incidente.

---

# Copias de Seguridad

Antes de cualquier operación crítica.

El sistema generará automáticamente un respaldo.

Como mínimo.

SQLite.

Excel.

Configuración.

Los respaldos nunca deberán sobrescribirse.

Cada respaldo conservará.

Fecha.

Hora.

Usuario.

Tipo.

Observaciones.

---

# Restauración

Solo los administradores podrán restaurar respaldos.

Antes de restaurar.

El sistema deberá.

Crear un respaldo del estado actual.

↓

Solicitar confirmación.

↓

Restaurar.

↓

Validar integridad.

↓

Registrar la operación.

Nunca restaurar información sin respaldo previo.

---

# Seguridad Física

Aunque el sistema implementará controles de acceso.

También será responsabilidad de la empresa.

Proteger los equipos.

Restringir el acceso físico.

Realizar copias externas.

Mantener actualizado el sistema operativo.

La seguridad del software no reemplaza las buenas prácticas administrativas.

---

# Seguridad en la Impresión

Los recibos generados deberán permanecer visibles únicamente el tiempo necesario para su impresión.

El sistema no deberá dejar documentos abiertos innecesariamente.

Los PDFs deberán almacenarse únicamente en la carpeta definida por la configuración del sistema.

---

# Protección de la Configuración

Toda la configuración del sistema deberá almacenarse en SQLite.

No deberán existir archivos de configuración modificables por el usuario.

Toda modificación deberá realizarse desde el módulo Configuración.

Cada cambio quedará registrado en los logs.

---

# Protección de Facturas

Cada factura generada será considerada un documento oficial.

No podrá modificarse.

No podrá eliminarse.

No podrá reutilizarse su número.

Si una factura presenta un error.

La corrección deberá realizarse mediante un nuevo movimiento administrativo.

Nunca alterando la factura original.

---

# Integridad Financiera

Toda operación relacionada con dinero deberá ejecutarse mediante transacciones.

Si una operación falla.

El sistema deberá garantizar que la información permanezca consistente.

Nunca deberán existir pagos parcialmente registrados.

Nunca deberán existir saldos inconsistentes.

---

# Protección frente a Fallos

Ante un cierre inesperado.

Una pérdida de energía.

Una interrupción del sistema.

O cualquier otro error.

El sistema deberá conservar la información previamente confirmada.

Nunca deberán perderse registros financieros ya almacenados.

---

# Protección del Código

El código fuente deberá mantenerse organizado.

Nunca almacenar.

Contraseñas.

Llaves privadas.

Tokens.

Credenciales.

Directamente en el código.

Toda información sensible deberá utilizar variables de entorno o configuraciones protegidas.

---

# Registro de Incidentes

Todo incidente de seguridad deberá registrarse.

Ejemplos.

Intentos fallidos de inicio de sesión.

Accesos sin permisos.

Errores de autenticación.

Errores durante sincronización.

Errores al generar recibos.

Errores de restauración.

Cada incidente almacenará.

Fecha.

Hora.

Usuario.

Dirección IP (si aplica).

Descripción.

Resultado.

---

# Disponibilidad

El sistema deberá permanecer disponible durante toda la jornada laboral.

Las tareas automáticas.

Respaldos.

Sincronizaciones.

Generación de recibos.

No deberán bloquear el funcionamiento general de la aplicación.

---

# Seguridad de los Archivos

Los directorios.

data/

backups/

recibos/

No deberán ser visibles desde el Frontend.

Toda interacción con estos directorios deberá realizarse únicamente mediante el Backend.

---

# Seguridad de las Sesiones

Cada usuario únicamente podrá mantener una sesión activa si así lo permite la configuración.

En futuras versiones el sistema podrá limitar múltiples sesiones simultáneas para un mismo usuario.

La arquitectura deberá quedar preparada para esta funcionalidad.

---

# Actualizaciones

Toda actualización futura del sistema deberá preservar.

La información existente.

Los respaldos.

Las configuraciones.

Los usuarios.

Los historiales.

Nunca deberán perderse datos durante una actualización.

---

# Principios Generales

La seguridad deberá implementarse bajo los siguientes principios.

Mínimo privilegio.

Defensa en profundidad.

Seguridad por defecto.

Validación permanente.

Trazabilidad completa.

Recuperación ante fallos.

Integridad de la información.

---

# Responsabilidad de OpenCode

Durante el desarrollo.

OpenCode deberá asumir que toda información financiera es crítica.

Por lo tanto.

Nunca implementará funcionalidades que permitan.

Eliminar pagos.

Eliminar facturas.

Modificar historiales.

Alterar recibos emitidos.

Omitir validaciones.

Reducir controles de acceso.

Si identifica una implementación que comprometa la seguridad.

Deberá detener el desarrollo de dicha funcionalidad y proponer una alternativa segura.

---

# Declaración Final

Este documento define oficialmente las políticas de seguridad del Sistema de Administración de Préstamos de CREEMOS EN TI SAS.

Toda implementación deberá respetar estas políticas desde el inicio del desarrollo.

La seguridad no deberá considerarse una característica adicional, sino un requisito fundamental del sistema.

---

**Fin del documento.**