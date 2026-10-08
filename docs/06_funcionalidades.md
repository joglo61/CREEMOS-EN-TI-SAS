# FUNCIONALIDADES DEL SISTEMA
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento describe todas las funcionalidades que deberá implementar el sistema.

A diferencia de los Casos de Uso, este documento describe el comportamiento funcional de cada módulo y las responsabilidades de cada componente del sistema.

Todas las funcionalidades aquí descritas deberán implementarse respetando las reglas del negocio definidas en la documentación oficial.

---

# Módulos del Sistema

La primera versión del sistema estará compuesta por los siguientes módulos.

• Inicio de sesión

• Dashboard

• Clientes

• Préstamos

• Pagos

• Facturación

• Historial

• Cronograma

• Administración de archivos

• Configuración

• Usuarios

• Backups

• Logs

---

# Módulo Inicio de Sesión

Este será el primer módulo que visualizará el usuario.

Su objetivo será controlar el acceso al sistema.

Características.

• Inicio de sesión seguro.

• Validación de usuario.

• Validación de contraseña.

• Control de roles.

• Registro del acceso.

• Registro del cierre de sesión.

El usuario únicamente podrá ingresar si sus credenciales son válidas.

---

# Módulo Dashboard

Después del inicio de sesión el sistema mostrará automáticamente el Dashboard.

El Dashboard será el centro de operaciones del sistema.

Desde aquí el usuario podrá acceder rápidamente a todas las funciones principales.

El Dashboard mostrará.

Clientes activos.

Clientes en mora.

Capital pendiente.

Pagos realizados hoy.

Valor recaudado hoy.

Últimos pagos registrados.

Cantidad de préstamos activos.

Estado del sistema.

Última sincronización.

Último respaldo.

---

# Módulo Clientes

Este módulo permitirá administrar toda la información de los clientes.

Funciones.

Crear cliente.

Consultar cliente.

Editar cliente.

Buscar cliente.

Consultar historial.

Consultar préstamo.

Consultar cronograma.

Registrar pago.

Nunca permitirá eliminar clientes.

---

# Crear Cliente

El formulario deberá solicitar únicamente la información necesaria.

Nombre.

Cédula.

Placa.

Teléfono.

Dirección.

Correo.

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

Registrar logs.

↓

Mostrar confirmación.

Todo este proceso deberá realizarse automáticamente.

---

# Consulta de Cliente

Al seleccionar un cliente el sistema mostrará.

Información personal.

Información financiera.

Saldo.

Próximo pago.

Estado.

Historial.

Cronograma.

Botones rápidos.

Registrar pago.

Editar.

Ver historial.

Ver cronograma.

---

# Búsqueda Inteligente

La búsqueda deberá funcionar mientras el usuario escribe.

No será necesario presionar Enter.

La búsqueda aceptará.

Nombre.

Placa.

Cédula.

Cualquier coincidencia deberá aparecer inmediatamente.

---

# Módulo Préstamos

Este módulo administrará exclusivamente la información financiera del préstamo.

Permitirá consultar.

Capital inicial.

Saldo actual.

Valor de la cuota.

Tasa.

Fecha de inicio.

Fecha del próximo pago.

Estado.

No permitirá modificar pagos históricos.

No permitirá alterar el historial financiero.

---

# Módulo Cronograma

Cada préstamo tendrá un cronograma estimado.

Este cronograma será generado automáticamente al crear el préstamo.

El cronograma mostrará.

Número de cuota.

Fecha estimada.

Interés estimado.

Capital estimado.

Saldo proyectado.

Valor proyectado.

El cronograma será únicamente informativo.

Los cálculos reales dependerán siempre de los pagos registrados.

---

# Módulo Pagos

Este módulo representa el núcleo financiero del sistema.

Será responsable de.

Registrar pagos.

Calcular intereses.

Calcular mora.

Calcular capital.

Actualizar saldo.

Actualizar fechas.

Generar factura.

Actualizar Excel.

Actualizar Dashboard.

Registrar historial.

Generar PDF.

Toda la lógica financiera estará concentrada exclusivamente en este módulo.

---

# Registro de Pagos

El proceso de registro de pagos deberá ser el más rápido de todo el sistema.

El operador únicamente deberá realizar las siguientes acciones.

Buscar cliente.

↓

Seleccionar cliente.

↓

Ingresar el valor recibido.

↓

Agregar observaciones (opcional).

↓

Confirmar.

Todo el resto del proceso será automático.

---

# Cálculo Automático

Mientras el operador escribe el valor recibido.

El sistema actualizará inmediatamente.

Intereses normales.

Intereses por mora.

Intereses totales.

Abono a capital.

Nuevo saldo.

Fecha del siguiente pago.

Estado del préstamo.

Toda la información deberá actualizarse en tiempo real.

No será necesario presionar botones para recalcular.

---

# Confirmación

Antes de registrar definitivamente el pago.

El sistema mostrará una vista previa.

La vista previa contendrá.

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

Botones.

Guardar e Imprimir.

Cancelar.

Si el usuario cancela.

No se registrará ninguna información.

---

# Proceso Automático Posterior al Pago

Una vez confirmado.

El sistema ejecutará automáticamente.

Actualizar préstamo.

↓

Actualizar saldo.

↓

Actualizar fecha del próximo pago.

↓

Registrar pago.

↓

Crear factura.

↓

Actualizar consecutivo.

↓

Actualizar SQLite.

↓

Crear respaldo.

↓

Actualizar archivo Excel.

↓

Guardar PDF.

↓

Actualizar Dashboard.

↓

Registrar log.

↓

Abrir impresión.

Todo este flujo deberá ejecutarse automáticamente.

---

# Módulo Facturación

Cada pago generará inmediatamente un recibo.

El usuario nunca deberá diligenciar un recibo manualmente.

Toda la información será obtenida desde SQLite.

Cada factura tendrá.

Número consecutivo.

Cliente.

Fecha.

Saldo anterior.

Intereses.

Capital.

Valor recibido.

Saldo nuevo.

Observaciones.

Firma.

El formato deberá respetar el diseño definido en la documentación de recibos.

---

# Módulo Historial

Cada cliente tendrá un historial completo.

Nunca deberán eliminarse registros.

Cada registro mostrará.

Factura.

Fecha.

Valor recibido.

Intereses.

Capital.

Saldo anterior.

Saldo nuevo.

Usuario.

Botón Reimprimir.

El historial deberá ordenarse desde el pago más reciente.

---

# Reimpresión

El sistema permitirá reimprimir cualquier factura.

La reimpresión nunca recalculará información.

Simplemente utilizará la información almacenada cuando el pago fue registrado.

Esto garantiza la consistencia histórica.

---

# Módulo Administración de Archivos

Este módulo permitirá administrar todos los archivos utilizados por la empresa.

Inicialmente existirá soporte para.

Archivo Excel de clientes.

Archivo Excel utilizado actualmente para cálculos financieros.

El sistema permitirá.

Cargar.

Reemplazar.

Validar.

Consultar.

Respaldar.

Restaurar.

Los archivos nunca serán modificados manualmente dentro del proyecto.

Toda la administración se realizará desde la interfaz.

---

# Validación de Archivos

Antes de aceptar un archivo.

El sistema verificará.

Formato.

Integridad.

Hojas requeridas.

Columnas obligatorias.

Tipo de datos.

Si alguna validación falla.

El archivo será rechazado.

El archivo actualmente activo permanecerá sin cambios.

---

# Sincronización

Después de cualquier operación financiera.

El sistema sincronizará automáticamente.

SQLite.

↓

Archivo Excel.

↓

Dashboard.

↓

Historial.

Si ocurre un error.

SQLite conservará la información.

El sistema registrará el incidente.

Permitirá reintentar posteriormente.

---

# Módulo Usuarios

Permitirá administrar el acceso al sistema.

Funciones.

Crear usuario.

Editar usuario.

Cambiar contraseña.

Activar.

Desactivar.

Asignar rol.

Restablecer contraseña.

Todas las acciones quedarán registradas.

---

# Módulo Configuración

Toda la configuración del sistema estará centralizada.

Permitirá modificar.

Empresa.

NIT.

Dirección.

Teléfono.

Correo.

Logo.

Tasa de interés.

Días de gracia.

Número siguiente de factura.

Ruta de respaldos.

Ruta de recibos.

Rutas de archivos Excel.

No será necesario modificar el código para cambiar estos parámetros.

---

# Módulo Logs

El sistema registrará automáticamente todas las acciones importantes.

Inicio de sesión.

Cierre de sesión.

Creación de clientes.

Edición de clientes.

Registro de pagos.

Carga de archivos.

Errores.

Respaldos.

Sincronización.

Cada registro incluirá.

Fecha.

Hora.

Usuario.

Acción.

Resultado.

Descripción.

# Módulo de Backups

El sistema deberá generar respaldos automáticos sin intervención del usuario.

Los respaldos se realizarán antes de cualquier operación crítica.

Como mínimo se respaldarán.

• Base de datos SQLite.

• Archivo Excel de clientes.

• Archivo Excel financiero.

• Configuración del sistema.

Cada respaldo deberá contener.

Fecha.

Hora.

Usuario.

Tipo.

Ruta.

Observaciones.

El administrador podrá restaurar cualquiera de estos respaldos desde la interfaz.

---

# Módulo de Restauración

El sistema permitirá restaurar un respaldo existente.

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

↓

Mostrar confirmación.

Nunca deberá sobrescribirse información sin crear previamente un respaldo.

---

# Módulo de Reportes

El sistema contará con un módulo de reportes administrativos.

Inicialmente incluirá.

Clientes activos.

Clientes en mora.

Pagos por fecha.

Ingresos diarios.

Ingresos mensuales.

Capital pendiente.

Facturas emitidas.

Historial de pagos.

Todos los reportes deberán permitir exportación futura a PDF y Excel.

---

# Módulo de Impresión

La impresión será completamente automática.

Después de registrar un pago.

El sistema deberá.

Generar el PDF.

↓

Guardar el PDF.

↓

Abrir la vista previa.

↓

Enviar a impresión.

El operador únicamente confirmará la impresión.

No deberá descargar archivos manualmente.

---

# Módulo de Estado del Sistema

El sistema mostrará permanentemente el estado de sus componentes.

SQLite.

Archivo Excel de clientes.

Archivo Excel financiero.

Última sincronización.

Último respaldo.

Espacio disponible.

Versión del sistema.

Si alguno de estos componentes presenta un problema.

El sistema mostrará una advertencia al administrador.

---

# Módulo de Notificaciones

El sistema utilizará notificaciones visuales para informar el resultado de las operaciones.

Tipos.

Éxito.

Advertencia.

Error.

Información.

Ejemplos.

Cliente creado correctamente.

Pago registrado correctamente.

Factura generada correctamente.

Archivo Excel actualizado correctamente.

Error al sincronizar el archivo Excel.

Las notificaciones deberán ser claras y fáciles de entender.

Nunca mostrar mensajes técnicos al usuario.

---

# Módulo de Auditoría

Toda operación importante deberá quedar registrada.

La auditoría almacenará.

Usuario.

Fecha.

Hora.

Módulo.

Acción.

Descripción.

Resultado.

Dirección IP (si aplica).

Esto permitirá reconstruir cualquier operación realizada dentro del sistema.

---

# Flujo Principal del Sistema

El funcionamiento esperado será.

Inicio de sesión.

↓

Dashboard.

↓

Buscar cliente.

↓

Consultar información.

↓

Registrar pago.

↓

Calcular intereses.

↓

Actualizar préstamo.

↓

Actualizar SQLite.

↓

Respaldar.

↓

Actualizar Excel.

↓

Generar PDF.

↓

Imprimir.

↓

Actualizar Dashboard.

↓

Registrar logs.

↓

Finalizar.

Todo este proceso deberá realizarse automáticamente.

---

# Rendimiento Esperado

El sistema deberá responder rápidamente incluso con miles de clientes.

Objetivos.

Búsqueda de clientes.

Menos de un segundo.

Carga del Dashboard.

Menos de dos segundos.

Registro completo de un pago.

Menos de diez segundos incluyendo generación del PDF.

La prioridad será siempre mantener una experiencia fluida para el usuario.

---

# Principios de Implementación

Todas las funcionalidades deberán respetar los siguientes principios.

Automatización.

Simplicidad.

Consistencia.

Seguridad.

Escalabilidad.

Mantenibilidad.

Toda funcionalidad nueva deberá integrarse siguiendo la arquitectura definida en el proyecto.

Nunca deberán desarrollarse módulos aislados o que rompan la estructura establecida.

---

# Declaración Final

Este documento define oficialmente todas las funcionalidades del Sistema de Administración de Préstamos de CREEMOS EN TI SAS.

Toda funcionalidad implementada deberá corresponder a alguno de los módulos aquí descritos.

Las futuras ampliaciones deberán mantener la misma filosofía de automatización, simplicidad y estabilidad.

---

**Fin del documento.**