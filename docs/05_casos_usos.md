# CASOS DE USO
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento describe detalladamente todos los procesos que podrán realizar los usuarios dentro del sistema.

Cada caso de uso representa una funcionalidad completa que deberá implementarse exactamente como se describe.

Estos casos de uso serán la guía principal para el desarrollo del Frontend y del Backend.

---

# Actores

El sistema contará inicialmente con dos tipos de usuarios.

## Administrador

Tiene acceso completo.

Puede realizar todas las operaciones disponibles dentro del sistema.

Incluyendo.

Administrar clientes.

Administrar préstamos.

Registrar pagos.

Consultar historial.

Reimprimir recibos.

Administrar usuarios.

Administrar archivos Excel.

Modificar configuraciones.

Crear respaldos.

Restaurar respaldos.

Consultar Dashboard.

---

## Empleado

Tiene acceso operativo.

Puede.

Buscar clientes.

Consultar información.

Registrar pagos.

Consultar historial.

Reimprimir recibos.

No podrá modificar configuraciones críticas.

No podrá administrar usuarios.

No podrá cargar nuevos archivos Excel.

---

# Caso de Uso 1

## Inicio de Sesión

### Objetivo

Permitir el acceso seguro al sistema.

### Actor

Administrador.

Empleado.

### Flujo Principal

El usuario abre el sistema.

↓

Se muestra la pantalla de inicio de sesión.

↓

Ingresa usuario.

↓

Ingresa contraseña.

↓

Presiona Ingresar.

↓

El sistema valida las credenciales.

↓

Si son correctas.

Genera un token de autenticación.

↓

Registra el inicio de sesión.

↓

Redirecciona al Dashboard.

---

### Flujo Alternativo

Si las credenciales son incorrectas.

Mostrar mensaje.

Usuario o contraseña incorrectos.

No revelar cuál dato es incorrecto.

---

# Caso de Uso 2

## Cerrar Sesión

### Actor

Administrador.

Empleado.

### Flujo

Seleccionar Cerrar sesión.

↓

Eliminar token.

↓

Registrar cierre de sesión.

↓

Regresar a la pantalla principal.

---

# Caso de Uso 3

## Buscar Cliente

### Objetivo

Encontrar rápidamente un cliente.

### Actor

Administrador.

Empleado.

### Criterios de búsqueda

Placa.

Nombre.

Cédula.

### Flujo

El usuario comienza a escribir.

↓

El sistema realiza la búsqueda automáticamente.

↓

Se muestran las coincidencias.

↓

El usuario selecciona un cliente.

↓

Se abre la ficha completa.

---

# Caso de Uso 4

## Consultar Cliente

### Actor

Administrador.

Empleado.

### Información mostrada

Nombre.

Cédula.

Placa.

Teléfono.

Dirección.

Valor del préstamo.

Saldo actual.

Valor de la cuota.

Fecha del próximo pago.

Estado.

Historial reciente.

Botones disponibles.

Registrar pago.

Ver historial.

Ver cronograma.

Editar.

---

# Caso de Uso 5

## Crear Cliente

### Actor

Administrador.

### Flujo

Seleccionar Nuevo Cliente.

↓

Mostrar formulario.

↓

Completar información.

↓

Guardar.

↓

El sistema valida.

↓

Crear cliente.

↓

Crear préstamo.

↓

Generar cronograma.

↓

Guardar en SQLite.

↓

Actualizar Excel.

↓

Registrar en logs.

↓

Mostrar confirmación.

---

### Validaciones

No permitir.

Cédulas repetidas.

Placas repetidas.

Campos obligatorios vacíos.

Fechas inválidas.

Valores negativos.

---

# Caso de Uso 6

## Editar Cliente

### Actor

Administrador.

### Información editable

Nombre.

Teléfono.

Dirección.

Correo.

Observaciones.

### Información NO editable

Pagos.

Facturas.

Historial.

Saldo.

Cronograma.

Número de préstamo.

Toda modificación deberá registrarse en los logs.

---

# Caso de Uso 7

## Consultar Cronograma

### Actor

Administrador.

Empleado.

### Información mostrada

Número de cuota.

Fecha estimada.

Capital estimado.

Interés estimado.

Valor estimado.

Saldo proyectado.

Estado.

Este cronograma tendrá únicamente carácter informativo.

No será utilizado para realizar cálculos financieros.

---

# Caso de Uso 8

## Registrar Pago

### Objetivo

Registrar un pago realizado por un cliente y actualizar automáticamente toda la información financiera relacionada.

### Actor

Administrador.

Empleado.

### Flujo Principal

El usuario busca el cliente.

↓

Selecciona el cliente.

↓

El sistema carga automáticamente.

Nombre.

Placa.

Saldo pendiente.

Valor de la cuota.

Fecha del próximo pago.

Número de factura siguiente.

↓

El usuario únicamente ingresa.

Valor recibido.

Observaciones (opcional).

↓

Mientras escribe el valor.

El sistema calcula automáticamente.

Intereses.

Intereses por mora.

Intereses totales.

Capital.

Nuevo saldo.

↓

Se muestra una vista previa.

↓

El usuario confirma.

↓

El sistema registra el pago.

↓

Actualiza SQLite.

↓

Actualiza el archivo Excel.

↓

Genera el PDF.

↓

Envía el recibo a impresión.

↓

Actualiza el Dashboard.

↓

Finaliza el proceso.

---

### Validaciones

No permitir.

Pagos negativos.

Pagos iguales a cero.

Pagos sobre préstamos finalizados.

Clientes inactivos.

Facturas duplicadas.

---

# Caso de Uso 9

## Vista Previa del Recibo

### Actor

Administrador.

Empleado.

### Flujo

Después del cálculo del pago.

El sistema mostrará exactamente el recibo que será impreso.

El usuario podrá verificar.

Fecha.

Factura.

Cliente.

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

# Caso de Uso 10

## Reimprimir Recibo

### Actor

Administrador.

Empleado.

### Flujo

Buscar cliente.

↓

Abrir historial.

↓

Seleccionar factura.

↓

Presionar Reimprimir.

↓

El sistema recupera el PDF almacenado.

↓

Envía nuevamente a impresión.

Nunca recalculará información financiera.

---

# Caso de Uso 11

## Consultar Historial

### Actor

Administrador.

Empleado.

### Flujo

Seleccionar cliente.

↓

Abrir historial.

↓

Mostrar todos los pagos registrados.

Cada registro deberá contener.

Factura.

Fecha.

Valor pagado.

Intereses.

Capital.

Saldo anterior.

Saldo nuevo.

Usuario.

Botón Reimprimir.

---

# Caso de Uso 12

## Dashboard

### Actor

Administrador.

Empleado.

### Flujo

Después del inicio de sesión.

El sistema mostrará automáticamente.

Clientes activos.

Clientes en mora.

Ingresos del día.

Capital pendiente.

Cantidad de pagos registrados.

Últimos pagos.

Toda la información será obtenida desde SQLite.

---

# Caso de Uso 13

## Configuración

### Actor

Administrador.

### Flujo

Abrir Configuración.

↓

Modificar información.

↓

Guardar.

↓

Actualizar SQLite.

↓

Registrar modificación.

↓

Mostrar confirmación.

Información configurable.

Empresa.

NIT.

Dirección.

Teléfono.

Logo.

Tasa de interés.

Días de gracia.

Número siguiente de factura.

Rutas.

---

# Caso de Uso 14

## Administración de Archivos Excel

### Actor

Administrador.

### Objetivo

Permitir administrar los archivos Excel utilizados por la empresa.

### Flujo

Ingresar al módulo Archivos.

↓

Seleccionar.

Cargar Base de Datos Excel.

o

Cargar Archivo Financiero.

↓

Seleccionar archivo.

↓

El sistema valida.

Formato.

Hojas.

Columnas.

Integridad.

↓

Si es correcto.

Crear respaldo.

↓

Copiar archivo.

↓

Actualizar configuración.

↓

Registrar evento.

↓

Mostrar confirmación.

Si ocurre un error.

No reemplazar el archivo actual.

Mostrar el motivo del rechazo.

---

# Caso de Uso 15

## Sincronizar Excel

### Actor

Administrador.

### Flujo

Seleccionar Sincronizar.

↓

El sistema compara SQLite con los archivos Excel.

↓

Actualiza la información.

↓

Valida los cambios.

↓

Registra el resultado.

↓

Muestra confirmación.

Si ocurre un error.

Registrar incidente.

Permitir reintentar posteriormente.

---

# Caso de Uso 16

## Crear Respaldo

### Actor

Administrador.

### Flujo

Seleccionar Crear Respaldo.

↓

Respaldar.

SQLite.

Archivo Excel de clientes.

Archivo Excel financiero.

Configuración.

↓

Registrar respaldo.

↓

Mostrar ubicación del respaldo.

---

# Caso de Uso 17

## Restaurar Respaldo

### Actor

Administrador.

### Flujo

Seleccionar respaldo.

↓

Mostrar información.

↓

Solicitar confirmación.

↓

Crear respaldo del estado actual.

↓

Restaurar información.

↓

Validar integridad.

↓

Registrar restauración.

↓

Mostrar confirmación.

---

# Caso de Uso 18

## Administración de Usuarios

### Actor

Administrador.

### Funciones

Crear usuario.

Editar usuario.

Cambiar contraseña.

Activar.

Desactivar.

Asignar rol.

Todas las modificaciones deberán registrarse en los logs.

---

# Caso de Uso 19

## Consultar Logs del Sistema

### Actor

Administrador.

### Objetivo

Permitir consultar todas las acciones importantes realizadas dentro del sistema.

### Flujo

Ingresar al módulo Logs.

↓

Seleccionar filtros.

↓

Consultar.

↓

Mostrar resultados.

Los filtros disponibles serán.

Usuario.

Fecha.

Módulo.

Acción.

Resultado.

Cada registro mostrará.

Fecha.

Hora.

Usuario.

Acción realizada.

Descripción.

Resultado.

---

# Caso de Uso 20

## Consultar Clientes en Mora

### Actor

Administrador.

Empleado.

### Objetivo

Consultar rápidamente todos los clientes con pagos vencidos.

### Flujo

Ingresar al Dashboard.

↓

Seleccionar Clientes en Mora.

↓

Mostrar listado.

La información mostrará.

Cliente.

Placa.

Saldo.

Fecha de vencimiento.

Días de mora.

Valor de la cuota.

Estado.

Desde esta pantalla será posible abrir directamente la ficha del cliente.

---

# Caso de Uso 21

## Consultar Facturas

### Actor

Administrador.

Empleado.

### Flujo

Ingresar al módulo Facturas.

↓

Buscar por.

Número.

Cliente.

Placa.

Fecha.

↓

Seleccionar factura.

↓

Mostrar información completa.

Opciones disponibles.

Ver PDF.

Reimprimir.

Descargar.

---

# Caso de Uso 22

## Consulta Global

### Actor

Administrador.

Empleado.

### Objetivo

Permitir encontrar cualquier cliente desde cualquier pantalla.

### Flujo

Escribir.

Nombre.

Placa.

Cédula.

↓

Mostrar resultados inmediatamente.

↓

Seleccionar cliente.

↓

Abrir ficha.

La búsqueda deberá responder en tiempo real.

---

# Caso de Uso 23

## Cambio de Contraseña

### Actor

Administrador.

Empleado.

### Flujo

Abrir Perfil.

↓

Cambiar contraseña.

↓

Ingresar contraseña actual.

↓

Ingresar nueva contraseña.

↓

Confirmar.

↓

Guardar.

↓

Actualizar información.

↓

Mostrar confirmación.

La contraseña nunca será visible.

---

# Caso de Uso 24

## Consulta del Estado del Sistema

### Actor

Administrador.

### Flujo

Abrir módulo Estado.

↓

Mostrar.

Estado de SQLite.

Estado del archivo Excel de clientes.

Estado del archivo financiero.

Última sincronización.

Último respaldo.

Cantidad de clientes.

Cantidad de préstamos.

Cantidad de pagos.

Espacio ocupado.

Versión del sistema.

---

# Caso de Uso 25

## Cierre Diario

### Actor

Administrador.

### Objetivo

Consultar el resumen operativo del día.

### Información mostrada

Pagos registrados.

Valor recaudado.

Clientes atendidos.

Facturas generadas.

Errores ocurridos.

Última sincronización.

Respaldos generados.

Este reporte será únicamente informativo.

---

# Reglas Generales

Todos los casos de uso deberán respetar las siguientes reglas.

Nunca solicitar información que el sistema pueda calcular automáticamente.

Nunca duplicar información.

Nunca permitir operaciones incompletas.

Nunca modificar pagos históricos.

Nunca modificar facturas históricas.

Nunca eliminar información financiera.

Toda operación deberá quedar registrada.

Toda modificación deberá generar un log.

Toda operación crítica deberá generar un respaldo cuando corresponda.

---

# Flujo General del Usuario

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

Vista previa.

↓

Guardar.

↓

Actualizar SQLite.

↓

Actualizar Excel.

↓

Generar recibo.

↓

Imprimir.

↓

Actualizar Dashboard.

↓

Continuar con el siguiente cliente.

Este flujo representa el proceso principal del sistema y deberá optimizarse para reducir al mínimo el tiempo de atención.

---

# Principio Fundamental

Todos los casos de uso deberán diseñarse para que el operador necesite la menor cantidad posible de acciones manuales.

Siempre que una tarea pueda automatizarse sin afectar las reglas del negocio, deberá ser realizada por el sistema.

La prioridad será reducir errores humanos, aumentar la velocidad de atención y mantener la simplicidad del proceso operativo.

---

# Declaración Final

Este documento define oficialmente todos los casos de uso del Sistema de Administración de Préstamos de CREEMOS EN TI SAS.

Toda funcionalidad implementada deberá corresponder a uno o varios casos de uso definidos en este documento.

Ninguna funcionalidad deberá desarrollarse sin encontrarse previamente documentada.

---

**Fin del documento.**