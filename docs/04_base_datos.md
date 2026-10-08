# BASE DE DATOS
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento define la estructura oficial de la base de datos del sistema.

Toda la información de la empresa será almacenada en SQLite.

SQLite será la única fuente oficial de información.

Microsoft Excel únicamente será un mecanismo de sincronización y compatibilidad con el proceso actual de trabajo.

Toda modificación realizada por el sistema deberá almacenarse primero en SQLite.

---

# Motor de Base de Datos

El sistema utilizará SQLite.

Razones:

• Fácil administración.

• No requiere instalación adicional.

• Excelente rendimiento para una empresa del tamaño de CREEMOS EN TI SAS.

• Facilidad para realizar respaldos.

• Integración sencilla con Python.

---

# ORM

Toda la interacción con SQLite deberá realizarse utilizando SQLAlchemy.

No deberán escribirse consultas SQL directamente dentro de los servicios.

Toda interacción con la base de datos deberá pasar por los repositorios.

---

# Principios de Diseño

La base de datos deberá cumplir los siguientes principios.

• Integridad.

• Consistencia.

• Escalabilidad.

• Facilidad de mantenimiento.

• Alta disponibilidad.

• Evitar duplicidad de información.

• Mantener historial completo.

---

# Entidades Principales

La base de datos estará compuesta inicialmente por las siguientes entidades.

Clientes.

Préstamos.

Pagos.

Facturas.

Cronograma.

Usuarios.

Configuración.

Archivos.

Logs.

Backups.

---

# Tabla CLIENTES

Esta tabla almacenará toda la información personal de cada cliente.

Cada cliente tendrá inicialmente un único préstamo activo.

En futuras versiones la estructura permitirá múltiples préstamos.

Campos.

id

nombre

cedula

placa

telefono

direccion

correo

estado

observaciones

created_at

updated_at

---

# Reglas

La placa deberá ser única.

La cédula deberá ser única.

No se permitirá eliminar clientes.

Cuando un cliente deje de operar.

Simplemente cambiará a estado Inactivo.

---

# Tabla PRESTAMOS

Almacena toda la información financiera del préstamo.

Campos.

id

cliente_id

capital_inicial

saldo_actual

valor_cuota

tasa_interes

fecha_inicio

fecha_primer_pago

fecha_proximo_pago

estado

created_at

updated_at

---

# Reglas

Todo préstamo pertenece a un único cliente.

Nunca eliminar préstamos.

Cuando el saldo llegue a cero.

El préstamo cambiará automáticamente al estado Finalizado.

---

# Tabla PAGOS

Cada vez que un cliente realice un pago.

Se creará un nuevo registro.

Nunca se actualizarán pagos históricos.

Nunca se eliminarán.

Campos.

id

prestamo_id

numero_factura

fecha_pago

dias_calculados

dias_mora

saldo_anterior

intereses

capital

valor_pagado

saldo_nuevo

observaciones

usuario_id

created_at

---

# Reglas

Cada pago pertenece a un préstamo.

Cada pago genera una factura.

Cada pago representa una operación irreversible.

---

# Tabla FACTURAS

Representa cada recibo generado por el sistema.

Campos.

id

numero_factura

cliente_id

pago_id

fecha

ruta_pdf

estado

created_at

---

# Reglas

Nunca reutilizar números.

Nunca eliminar facturas.

Siempre permitir reimpresión.

El PDF siempre deberá permanecer disponible.

---

# Tabla CRONOGRAMA

Contendrá el cronograma estimado generado al crear un préstamo.

Campos.

id

prestamo_id

numero_cuota

fecha_estimada

capital_estimado

interes_estimado

valor_estimado

saldo_estimado

estado

created_at

---

# Reglas

El cronograma será únicamente informativo.

Nunca será utilizado para realizar cálculos financieros.

Los cálculos reales dependerán siempre de los pagos realizados por el cliente.

---

# Tabla USUARIOS

Almacenará todos los usuarios autorizados para ingresar al sistema.

Campos.

id

nombre

usuario

password_hash

rol

activo

ultimo_acceso

created_at

updated_at

---

# Reglas

Nunca almacenar contraseñas en texto plano.

Todas las contraseñas deberán almacenarse utilizando hash seguro.

Los roles iniciales serán.

Administrador.

Empleado.

En futuras versiones podrán agregarse nuevos roles.

---

# Tabla CONFIGURACION

Esta tabla almacenará toda la configuración general del sistema.

Campos.

id

empresa

nit

direccion

telefono

correo

logo

tasa_interes

dias_gracia

siguiente_factura

ruta_recibos

ruta_backups

created_at

updated_at

---

# Reglas

Solo existirá un registro activo.

Toda la configuración deberá obtenerse desde esta tabla.

Nunca escribir configuraciones directamente en el código.

---

# Tabla ARCHIVOS

Permitirá administrar los archivos Excel utilizados por la empresa.

El sistema nunca dependerá de nombres específicos.

Campos.

id

tipo

nombre_original

nombre_interno

ruta

version

fecha_carga

usuario_id

activo

created_at

---

# Tipos de Archivo

Inicialmente existirán dos tipos.

CLIENTES

INTERESES

En futuras versiones podrán agregarse nuevos tipos.

---

# Reglas

Siempre deberá existir únicamente un archivo activo por cada tipo.

Cuando un archivo sea reemplazado.

El anterior permanecerá almacenado para auditoría.

Nunca deberá eliminarse automáticamente.

---

# Tabla LOGS

Permitirá registrar todas las acciones importantes realizadas por el sistema.

Campos.

id

usuario_id

accion

modulo

descripcion

direccion_ip

created_at

---

# Acciones Registradas

Inicio de sesión.

Cierre de sesión.

Creación de clientes.

Edición de clientes.

Registro de pagos.

Carga de archivos.

Generación de facturas.

Sincronización.

Errores.

Restauración de respaldos.

---

# Tabla BACKUPS

Permitirá registrar todos los respaldos generados automáticamente.

Campos.

id

tipo

archivo

ruta

tamano

usuario_id

created_at

---

# Tipos

SQLite.

Excel Clientes.

Excel Intereses.

Configuración.

Sistema Completo.

---

# Relaciones

CLIENTE

↓

1

↓

N

PRESTAMOS

---

PRESTAMO

↓

1

↓

N

PAGOS

---

PAGO

↓

1

↓

1

FACTURA

---

PRESTAMO

↓

1

↓

N

CRONOGRAMA

---

USUARIO

↓

1

↓

N

PAGOS

---

USUARIO

↓

1

↓

N

LOGS

---

USUARIO

↓

1

↓

N

ARCHIVOS

---

USUARIO

↓

1

↓

N

BACKUPS

---

# Índices

Deberán crearse índices sobre los siguientes campos.

Clientes.

placa

cedula

nombre

Prestamos.

estado

fecha_proximo_pago

Pagos.

numero_factura

fecha_pago

Factura.

numero_factura

Usuarios.

usuario

Logs.

created_at

Archivos.

tipo

activo

Estos índices permitirán búsquedas rápidas incluso con grandes volúmenes de información.

---

# Restricciones

No permitir placas duplicadas.

No permitir cédulas duplicadas.

No permitir números de factura repetidos.

No permitir usuarios duplicados.

No permitir archivos activos duplicados para el mismo tipo.

No permitir préstamos sin cliente.

No permitir pagos sin préstamo.

No permitir facturas sin pago.

Toda relación deberá mantenerse mediante claves foráneas.

---

# Integridad Referencial

Todas las tablas deberán utilizar claves foráneas.

Nunca deberán existir registros huérfanos.

Cuando un registro cambie de estado.

Las relaciones deberán mantenerse.

No utilizar eliminaciones físicas cuando exista información relacionada.

# Sincronización entre SQLite y Excel

SQLite será siempre la fuente oficial de información.

Microsoft Excel será una representación sincronizada de dicha información.

Nunca deberá ocurrir el siguiente flujo:

Excel

↓

SQLite

El flujo correcto será siempre:

Usuario

↓

Sistema

↓

SQLite

↓

Excel

---

# Administración de Archivos Excel

El sistema contará con un módulo denominado:

Administración de Archivos

Desde este módulo el administrador podrá:

• Cargar el archivo Excel que contiene la base de datos utilizada actualmente por la empresa.

• Cargar el archivo Excel utilizado para el cálculo financiero.

• Reemplazar cualquiera de los dos archivos.

• Ver la fecha de la última actualización.

• Consultar la versión cargada.

• Restaurar una versión anterior.

• Descargar una copia de seguridad.

El sistema nunca dependerá de un nombre específico de archivo.

---

# Validación de Archivos

Antes de aceptar un archivo Excel.

El sistema deberá verificar.

• Que el archivo exista.

• Que sea un archivo Excel válido.

• Que pueda abrirse.

• Que no esté protegido con contraseña.

• Que contenga todas las hojas necesarias.

• Que todas las columnas obligatorias existan.

• Que no existan columnas críticas faltantes.

Si cualquiera de estas validaciones falla.

El archivo será rechazado.

No reemplazará el archivo actualmente activo.

---

# Flujo de Reemplazo de Archivos

Cuando el administrador cargue un nuevo archivo.

El sistema realizará el siguiente proceso.

Seleccionar archivo.

↓

Validar formato.

↓

Validar estructura.

↓

Crear respaldo del archivo actual.

↓

Copiar el nuevo archivo.

↓

Actualizar configuración.

↓

Registrar el cambio en los logs.

↓

Mostrar confirmación.

---

# Ubicación de los Archivos

Los archivos utilizados por el sistema deberán almacenarse dentro de una carpeta administrada por la aplicación.

Ejemplo.

data/

clientes.xlsx

intereses.xlsx

Los usuarios nunca deberán modificar manualmente estos archivos.

Toda modificación deberá realizarse desde el sistema.

---

# Respaldo Automático

Antes de modificar.

SQLite.

Excel.

Configuración.

El sistema generará automáticamente un respaldo.

La estructura sugerida será.

backups/

2026/

07/

02/

sqlite/

excel_clientes/

excel_intereses/

configuracion/

Cada respaldo deberá conservar.

Fecha.

Hora.

Usuario.

Tipo.

Ruta.

Observaciones.

---

# Restauración

El administrador podrá restaurar cualquier respaldo.

El proceso será.

Seleccionar respaldo.

↓

Confirmar.

↓

Crear respaldo del estado actual.

↓

Restaurar.

↓

Validar integridad.

↓

Mostrar confirmación.

Nunca deberá sobrescribirse información sin crear primero un respaldo.

---

# Auditoría

Toda modificación realizada sobre la base de datos deberá quedar registrada.

Como mínimo.

Usuario.

Fecha.

Hora.

Acción.

Tabla afectada.

Registro afectado.

Resultado.

Esta información permitirá reconstruir cualquier operación realizada dentro del sistema.

---

# Rendimiento

La base de datos deberá optimizarse para responder rápidamente.

Las consultas más frecuentes serán.

Buscar cliente por placa.

Buscar cliente por nombre.

Buscar cliente por cédula.

Consultar historial.

Consultar pagos recientes.

Consultar clientes en mora.

Estas consultas deberán responder prácticamente de manera inmediata.

---

# Escalabilidad

Aunque inicialmente SQLite será suficiente.

La arquitectura deberá permitir migrar en el futuro hacia motores como.

PostgreSQL.

MySQL.

SQL Server.

Sin modificar la lógica del negocio.

Para ello.

Toda interacción con la base de datos deberá realizarse mediante SQLAlchemy.

Nunca deberán escribirse consultas específicas del motor utilizado.

---

# Migraciones

Toda modificación estructural deberá realizarse utilizando Alembic.

Nunca modificar directamente la base de datos en producción.

Cada cambio deberá generar una migración claramente identificada.

Las migraciones deberán conservar el historial completo de la evolución de la base de datos.

---

# Integridad de la Información

Toda operación deberá cumplir las propiedades ACID.

Atomicidad.

Consistencia.

Aislamiento.

Durabilidad.

Nunca deberán existir operaciones parcialmente ejecutadas.

La integridad de la información financiera tendrá prioridad absoluta sobre el rendimiento.

---

# Principio Fundamental

La base de datos constituye el núcleo del Sistema de Administración de Préstamos.

Toda la operación financiera dependerá de la información almacenada en ella.

Por esta razón.

Toda decisión relacionada con la persistencia deberá priorizar.

Integridad.

Confiabilidad.

Trazabilidad.

Seguridad.

Escalabilidad.

---

# Declaración Final

Este documento define oficialmente la estructura y las reglas de la base de datos del Sistema de Administración de Préstamos de CREEMOS EN TI SAS.

Toda implementación deberá respetar este diseño.

Cualquier modificación futura deberá reflejarse primero en este documento antes de implementarse en el software.

---

**Fin del documento.**