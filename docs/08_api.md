# API
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento define la API REST oficial del sistema.

Toda comunicación entre el Frontend y el Backend deberá realizarse exclusivamente mediante esta API.

Ningún componente del Frontend accederá directamente a SQLite.

Ningún componente del Frontend accederá directamente a los archivos Excel.

Toda la lógica permanecerá centralizada en el Backend.

---

# Arquitectura

Frontend

↓

HTTP

↓

FastAPI

↓

Servicios

↓

Repositorios

↓

SQLite

---

# Formato

Todas las solicitudes utilizarán JSON.

Todas las respuestas utilizarán JSON.

Todos los endpoints deberán responder utilizando códigos HTTP estándar.

---

# Autenticación

El sistema utilizará JWT.

Después del inicio de sesión el Backend devolverá un token.

Todas las solicitudes protegidas deberán incluir.

Authorization

Bearer TOKEN

Si el token no existe.

Responder.

401 Unauthorized

Si el usuario no tiene permisos.

Responder.

403 Forbidden

---

# Versionado

La API utilizará versionado.

Ejemplo.

api/v1/

Esto permitirá crear futuras versiones sin romper la compatibilidad.

---

# Módulo Autenticación

## POST

/api/v1/auth/login

Descripción.

Iniciar sesión.

Entrada.

Usuario.

Contraseña.

Salida.

Token.

Información del usuario.

Rol.

---

## POST

/api/v1/auth/logout

Descripción.

Cerrar sesión.

Entrada.

Token.

Salida.

Confirmación.

---

## GET

/api/v1/auth/me

Descripción.

Consultar información del usuario autenticado.

---

# Módulo Clientes

## GET

/api/v1/clientes

Consultar clientes.

Permitir filtros.

Nombre.

Placa.

Cédula.

Estado.

Paginación.

---

## GET

/api/v1/clientes/{id}

Consultar un cliente específico.

La respuesta incluirá.

Información personal.

Información financiera.

Préstamo.

Estado.

Historial resumido.

---

## POST

/api/v1/clientes

Crear cliente.

Entrada.

Información personal.

Información del préstamo.

Observaciones.

Salida.

Cliente creado.

---

## PUT

/api/v1/clientes/{id}

Actualizar información administrativa.

Nunca actualizará.

Pagos.

Facturas.

Saldo.

Cronograma.

---

## DELETE

/api/v1/clientes/{id}

No eliminará físicamente.

Cambiará el estado.

Inactivo.

---

# Módulo Préstamos

## GET

/api/v1/prestamos

Consultar préstamos.

Permitir filtros.

Estado.

Cliente.

Fecha.

---

## GET

/api/v1/prestamos/{id}

Consultar préstamo específico.

Incluir.

Saldo.

Cronograma.

Pagos.

Estado.

---

## GET

/api/v1/prestamos/{id}/cronograma

Consultar cronograma estimado.

No realizará cálculos.

Únicamente devolverá la información almacenada.

---

# Módulo Pagos

## POST

/api/v1/pagos

Registrar un pago.

Entrada.

Cliente.

Valor recibido.

Observaciones.

Salida.

Pago registrado.

Factura.

Nuevo saldo.

Ruta del PDF.

---

## POST

/api/v1/pagos/simular

Este endpoint permitirá calcular un pago sin registrarlo.

La respuesta mostrará.

Intereses.

Mora.

Capital.

Nuevo saldo.

Factura estimada.

Esta funcionalidad será utilizada por la vista previa del recibo.

---

## GET

/api/v1/pagos/{id}

Consultar un pago específico.

---

# Módulo Facturas

## GET

/api/v1/facturas

Consultar facturas.

Permitir filtros.

Número.

Cliente.

Placa.

Fecha.

Estado.

Usuario.

---

## GET

/api/v1/facturas/{id}

Consultar una factura específica.

La respuesta incluirá.

Número.

Cliente.

Pago.

PDF.

Estado.

---

## GET

/api/v1/facturas/{id}/pdf

Obtener el archivo PDF correspondiente a la factura.

El sistema devolverá el documento listo para visualizar o imprimir.

---

## POST

/api/v1/facturas/{id}/reimprimir

Enviar nuevamente el recibo a impresión.

No recalculará intereses.

No recalculará capital.

No modificará ninguna información.

Únicamente utilizará la información almacenada cuando fue registrada la factura.

---

# Módulo Historial

## GET

/api/v1/historial

Consultar historial general.

Permitir filtros.

Cliente.

Placa.

Fecha.

Usuario.

Factura.

---

## GET

/api/v1/historial/{cliente_id}

Consultar historial completo de un cliente.

La respuesta incluirá.

Todos los pagos.

Todas las facturas.

Saldo histórico.

Fechas.

Usuarios responsables.

---

# Módulo Dashboard

## GET

/api/v1/dashboard

Obtener toda la información del Dashboard.

La respuesta contendrá.

Clientes activos.

Clientes en mora.

Capital pendiente.

Ingresos del día.

Pagos registrados.

Facturas emitidas.

Últimos pagos.

Última sincronización.

Último respaldo.

---

## GET

/api/v1/dashboard/resumen

Obtener únicamente los indicadores principales.

Será utilizado para actualizar el Dashboard rápidamente.

---

# Módulo Configuración

## GET

/api/v1/configuracion

Consultar configuración general.

---

## PUT

/api/v1/configuracion

Actualizar configuración.

Campos permitidos.

Empresa.

NIT.

Dirección.

Teléfono.

Correo.

Logo.

Tasa.

Días de gracia.

Número siguiente de factura.

Rutas.

Toda modificación quedará registrada.

---

# Módulo Usuarios

## GET

/api/v1/usuarios

Consultar usuarios.

---

## GET

/api/v1/usuarios/{id}

Consultar un usuario.

---

## POST

/api/v1/usuarios

Crear usuario.

---

## PUT

/api/v1/usuarios/{id}

Actualizar usuario.

---

## PUT

/api/v1/usuarios/{id}/password

Cambiar contraseña.

---

## PUT

/api/v1/usuarios/{id}/estado

Activar.

Desactivar.

---

## DELETE

/api/v1/usuarios/{id}

No eliminar físicamente.

Cambiar estado a inactivo.

---

# Módulo Administración de Archivos

## GET

/api/v1/archivos

Consultar todos los archivos administrados por el sistema.

Mostrar.

Tipo.

Nombre.

Versión.

Fecha de carga.

Usuario.

Estado.

---

## POST

/api/v1/archivos/clientes

Cargar un nuevo archivo Excel correspondiente a la base de datos utilizada por la empresa.

Proceso automático.

Validar.

Respaldar.

Copiar.

Registrar.

Actualizar configuración.

---

## POST

/api/v1/archivos/intereses

Cargar el archivo Excel utilizado actualmente para cálculos financieros.

Proceso automático.

Validar.

Respaldar.

Copiar.

Registrar.

Actualizar configuración.

---

## GET

/api/v1/archivos/{id}

Consultar información detallada del archivo.

---

## POST

/api/v1/archivos/{id}/restaurar

Restaurar una versión anterior.

---

## POST

/api/v1/archivos/sincronizar

Ejecutar manualmente la sincronización entre SQLite y Excel.

---

# Módulo Backups

## GET

/api/v1/backups

Consultar respaldos disponibles.

---

## POST

/api/v1/backups

Crear respaldo manual.

---

## POST

/api/v1/backups/{id}/restaurar

Restaurar respaldo.

---

## GET

/api/v1/backups/{id}

Consultar información del respaldo.

---

# Módulo Logs

## GET

/api/v1/logs

Consultar logs.

Permitir filtros.

Usuario.

Fecha.

Acción.

Módulo.

Resultado.

---

## GET

/api/v1/logs/{id}

Consultar un registro específico.

# Respuestas Estándar

Todas las respuestas de la API deberán seguir la misma estructura.

## Respuesta Exitosa

```json
{
    "success": true,
    "message": "Pago registrado correctamente.",
    "data": {}
}
```

---

## Respuesta con Error

```json
{
    "success": false,
    "message": "No fue posible registrar el pago.",
    "errors": []
}
```

---

## Error de Validación

```json
{
    "success": false,
    "message": "Error de validación.",
    "errors": [
        {
            "field": "valor_pagado",
            "message": "El valor debe ser mayor que cero."
        }
    ]
}
```

---

# Códigos HTTP

La API utilizará los siguientes códigos.

200

Solicitud exitosa.

201

Recurso creado.

204

Operación realizada sin contenido de respuesta.

400

Solicitud incorrecta.

401

No autenticado.

403

Sin permisos.

404

Recurso no encontrado.

409

Conflicto de información.

422

Error de validación.

500

Error interno del servidor.

---

# Validaciones

Toda la validación deberá realizarse inicialmente en el Backend.

El Frontend únicamente realizará validaciones para mejorar la experiencia del usuario.

Nunca deberá confiarse en la validación realizada por el navegador.

---

# Seguridad

Todos los endpoints deberán validar.

Autenticación.

Permisos.

Integridad de los datos.

Formato de entrada.

Nunca devolver información sensible.

Nunca devolver contraseñas.

Nunca devolver hashes.

Nunca devolver rutas internas del servidor.

---

# Paginación

Todos los endpoints que consulten listas deberán soportar.

page

page_size

sort

order

search

Ejemplo.

GET

/api/v1/clientes?page=1&page_size=25

---

# Ordenamiento

Los endpoints permitirán ordenar la información por.

Nombre.

Fecha.

Número de factura.

Saldo.

Estado.

Valor.

El orden podrá ser.

ASC

DESC

---

# Búsquedas

La API permitirá búsquedas parciales.

Ejemplos.

Nombre.

Placa.

Cédula.

Número de factura.

No será necesario escribir el texto completo.

---

# Auditoría

Toda operación importante ejecutada mediante la API deberá generar automáticamente un registro en los logs.

Como mínimo.

Usuario.

Fecha.

Hora.

IP.

Endpoint.

Acción.

Resultado.

---

# Versionado

Toda modificación incompatible deberá crear una nueva versión.

Ejemplo.

/api/v2/

Nunca modificar el comportamiento de una versión ya publicada.

---

# Documentación Automática

FastAPI deberá generar automáticamente la documentación.

Swagger.

Redoc.

Toda la API deberá mantenerse completamente documentada.

Cada endpoint deberá incluir.

Descripción.

Parámetros.

Ejemplos.

Respuestas.

Errores posibles.

---

# Rendimiento

La API deberá responder rápidamente.

Objetivos.

Consultas.

Menos de 500 ms.

Registro de pagos.

Menos de 2 segundos.

Dashboard.

Menos de 1 segundo.

Carga de clientes.

Menos de 500 ms.

Estos tiempos no incluyen la generación del PDF.

---

# Escalabilidad

La API deberá diseñarse para permitir agregar nuevos módulos.

WhatsApp.

Facturación electrónica.

Correo electrónico.

Aplicación móvil.

Portal de clientes.

Integraciones externas.

Sin modificar los endpoints existentes.

---

# Principios

Toda la API deberá cumplir.

REST.

JSON.

Stateless.

Versionada.

Documentada.

Segura.

Escalable.

Consistente.

---

# Declaración Final

Este documento define oficialmente la API REST del Sistema de Administración de Préstamos de CREEMOS EN TI SAS.

Toda comunicación entre el Frontend y el Backend deberá realizarse mediante esta API.

Cualquier modificación futura deberá actualizar este documento antes de implementarse en el software.

---

**Fin del documento.**