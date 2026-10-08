# ARQUITECTURA DEL SISTEMA
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento define la arquitectura oficial del sistema.

Toda la implementación deberá respetar esta arquitectura.

No se permitirá modificar la estructura principal sin una justificación técnica.

El objetivo es construir un sistema robusto, escalable, mantenible y preparado para evolucionar durante muchos años.

---

# Filosofía

El sistema deberá dividirse en módulos independientes.

Cada módulo tendrá una única responsabilidad.

Cada componente deberá poder mantenerse sin afectar el resto del sistema.

La arquitectura deberá minimizar el acoplamiento entre módulos.

La reutilización de código será una prioridad.

---

# Arquitectura General

El sistema estará compuesto por cuatro capas principales.

Frontend

↓

API REST

↓

Servicios de Negocio

↓

Persistencia

Cada capa deberá comunicarse únicamente con la capa inmediatamente inferior.

Nunca deberán omitirse capas.

---

# Frontend

El Frontend será desarrollado utilizando:

React

TypeScript

Vite

TailwindCSS

React Router

Axios

TanStack Query

React Hook Form

Zod

El Frontend tendrá únicamente responsabilidades de presentación.

Nunca contendrá lógica financiera.

Nunca realizará cálculos.

Nunca modificará directamente la base de datos.

Su responsabilidad será únicamente:

Mostrar información.

Capturar información.

Consumir la API.

Mostrar mensajes.

Mostrar errores.

---

# Backend

El Backend será desarrollado utilizando:

Python

FastAPI

SQLAlchemy

Alembic

Pydantic

JWT

Passlib

El Backend será el núcleo del sistema.

Toda la lógica del negocio deberá vivir aquí.

Toda decisión financiera deberá implementarse exclusivamente en el Backend.

---

# Base de Datos

SQLite será la única fuente oficial de información.

Toda operación deberá almacenarse inicialmente en SQLite.

Nunca deberá utilizarse Excel como fuente principal.

Toda consulta financiera deberá obtener la información desde SQLite.

---

# Excel

Microsoft Excel continuará formando parte del proceso de trabajo de la empresa.

Sin embargo.

El sistema nunca dependerá directamente de un archivo Excel.

Los archivos Excel serán administrados desde el sistema.

Podrán cambiarse.

Podrán reemplazarse.

Podrán sincronizarse.

Toda esta lógica será independiente del resto del sistema.

---

# PDF

La generación de recibos será completamente independiente del módulo financiero.

El módulo PDF únicamente recibirá información ya calculada.

Nunca calculará intereses.

Nunca calculará mora.

Nunca modificará saldos.

Su única responsabilidad será construir el documento PDF.

---

# API REST

Toda comunicación entre Frontend y Backend deberá realizarse mediante una API REST.

No se permitirá acceder directamente a SQLite desde React.

No se permitirá acceder directamente a archivos Excel desde React.

Toda comunicación pasará por FastAPI.

---

# Organización General del Proyecto

El proyecto tendrá la siguiente estructura.

backend/

frontend/

database/

docs/

assets/

data/

backups/

recibos/

Cada carpeta tendrá una responsabilidad claramente definida.

---

# Backend

La estructura propuesta será.

backend/

app/

api/

core/

database/

models/

schemas/

repositories/

services/

utils/

pdf/

excel/

security/

config/

tests/

main.py

Cada directorio representará un módulo independiente.

---

# Frontend

La estructura propuesta será.

frontend/

src/

components/

pages/

layouts/

hooks/

services/

contexts/

types/

styles/

utils/

assets/

App.tsx

main.tsx

Toda la interfaz deberá organizarse siguiendo esta estructura.

---

# Base de Datos

Toda modificación deberá realizarse utilizando SQLAlchemy.

Nunca escribir consultas SQL distribuidas por todo el proyecto.

Toda interacción con SQLite deberá pasar por los repositorios.

---

# Repositorios

Cada entidad principal tendrá su propio repositorio.

ClienteRepository

PrestamoRepository

PagoRepository

FacturaRepository

UsuarioRepository

ConfiguracionRepository

El repositorio será responsable únicamente de acceder a la base de datos.

Nunca contendrá reglas de negocio.

---

# Servicios

Toda la lógica del negocio estará implementada mediante servicios.

Por ejemplo.

ClienteService

PrestamoService

PagoService

FacturaService

ExcelService

PDFService

ConfiguracionService

DashboardService

Cada servicio tendrá una única responsabilidad.

Toda la lógica financiera deberá centralizarse en PagoService.

---

# Inyección de Dependencias

Todos los servicios deberán ser independientes entre sí.

Cuando un servicio necesite utilizar otro servicio.

Deberá hacerlo mediante inyección de dependencias.

No crear instancias manualmente dentro del código.

Esto facilitará.

Pruebas.

Mantenimiento.

Escalabilidad.

---

# Flujo General de una Solicitud

Toda solicitud seguirá el siguiente recorrido.

Frontend

↓

API

↓

Controlador

↓

Servicio

↓

Repositorio

↓

SQLite

↓

Repositorio

↓

Servicio

↓

API

↓

Frontend

Nunca deberán omitirse pasos.

Toda la lógica deberá permanecer centralizada.

---

# Controladores

Los controladores deberán ser extremadamente pequeños.

Su única responsabilidad será.

Recibir solicitudes.

Validar formato.

Llamar al servicio correspondiente.

Retornar la respuesta.

Nunca deberán contener.

Consultas SQL.

Cálculos.

Lógica financiera.

Manipulación de archivos.

Generación de PDF.

---

# Modelos

Los modelos representarán exclusivamente las tablas de SQLite.

No contendrán lógica del negocio.

Cada modelo representará una única entidad.

Ejemplos.

Cliente.

Prestamo.

Pago.

Factura.

Usuario.

Configuracion.

---

# Schemas

Los Schemas definirán la información que entra y sale de la API.

Existirán como mínimo.

Create.

Update.

Response.

Nunca devolver directamente un modelo de SQLAlchemy.

Toda respuesta deberá pasar por un Schema.

---

# Configuración

Toda configuración deberá centralizarse.

No deberán existir valores escritos directamente dentro del código.

Ejemplos.

Tasa de interés.

Días de gracia.

Ruta de respaldos.

Ruta de recibos.

Ruta de archivos Excel.

Empresa.

NIT.

Logo.

Número siguiente de factura.

Todo deberá almacenarse en SQLite.

---

# Seguridad

La autenticación utilizará JWT.

Las contraseñas serán cifradas utilizando algoritmos seguros.

Nunca almacenar contraseñas en texto plano.

Nunca devolver información sensible al Frontend.

Todo endpoint deberá validar permisos.

---

# Manejo de Errores

Todos los errores deberán manejarse de manera uniforme.

No deberán existir mensajes técnicos para el usuario.

El Backend devolverá mensajes claros.

Ejemplo.

Cliente no encontrado.

Pago registrado correctamente.

Archivo Excel inválido.

Error al sincronizar el archivo.

Los errores internos deberán registrarse en los logs.

---

# Sistema de Logs

El sistema registrará automáticamente.

Inicio de sesión.

Errores.

Creación de clientes.

Registro de pagos.

Generación de facturas.

Carga de archivos.

Sincronización.

Restauración de respaldos.

Todos los logs deberán incluir.

Fecha.

Hora.

Usuario.

Acción.

Resultado.

---

# Transacciones

Toda operación financiera deberá ejecutarse dentro de una transacción.

Registrar un pago implica.

Actualizar préstamo.

Crear pago.

Crear factura.

Actualizar configuración.

Actualizar historial.

Actualizar Excel.

Generar PDF.

Si alguna operación falla.

La transacción deberá revertirse.

La única excepción será la sincronización con Excel.

Si SQLite fue actualizado correctamente y posteriormente falla la sincronización.

La información permanecerá almacenada en SQLite.

El sistema registrará el incidente y permitirá reintentar la sincronización posteriormente.

---

# Módulo Excel

El módulo Excel será completamente independiente.

Será responsable de.

Leer archivos.

Validar estructura.

Actualizar información.

Crear respaldos.

Sincronizar.

Nunca contendrá lógica financiera.

---

# Módulo PDF

El módulo PDF recibirá toda la información ya calculada.

Será responsable únicamente de.

Construir el PDF.

Guardar el archivo.

Preparar impresión.

Permitir reimpresión.

Nunca realizará cálculos.

---

# Módulo Dashboard

El Dashboard obtendrá toda la información desde SQLite.

Nunca leerá directamente archivos Excel.

Deberá calcular.

Clientes activos.

Clientes en mora.

Ingresos.

Capital pendiente.

Pagos recientes.

Toda la información deberá actualizarse automáticamente.

---

# Módulo Configuración

Toda la configuración del sistema estará centralizada.

Desde este módulo podrán modificarse.

Empresa.

Logo.

Teléfono.

Dirección.

Tasa.

Días de gracia.

Número siguiente de factura.

Rutas.

Configuración de impresión.

No será necesario modificar el código para cambiar estos parámetros.

---

# Módulo Administración de Archivos

Existirá un módulo independiente para administrar los archivos utilizados por la empresa.

Permitirá.

Cargar archivo Excel de clientes.

Cargar archivo Excel financiero.

Validar archivos.

Reemplazar archivos.

Consultar fecha de carga.

Consultar estado.

Restaurar respaldo.

Toda esta lógica será independiente del resto del sistema.

# Comunicación entre Módulos

Cada módulo deberá comunicarse únicamente mediante servicios claramente definidos.

No se permitirá acceder directamente a componentes internos de otros módulos.

Ejemplo.

El módulo PDF nunca accederá directamente a SQLite.

El módulo Excel nunca calculará intereses.

El módulo Dashboard nunca modificará información.

Cada módulo tendrá una responsabilidad claramente definida.

---

# Sincronización de Información

Toda la información seguirá el siguiente flujo.

Usuario

↓

Frontend

↓

Backend

↓

SQLite

↓

Excel

↓

PDF

↓

Respuesta al usuario

SQLite será siempre la primera base de datos en actualizarse.

El Excel será sincronizado únicamente después de una operación exitosa.

---

# Copias de Seguridad

Antes de modificar cualquiera de los siguientes recursos.

SQLite.

Archivo Excel de clientes.

Archivo Excel financiero.

Configuración.

El sistema deberá generar automáticamente un respaldo.

Los respaldos deberán almacenarse organizados por.

Año.

Mes.

Día.

Hora.

Nunca deberán sobrescribirse.

---

# Escalabilidad

La arquitectura deberá permitir incorporar nuevos módulos sin modificar los existentes.

Ejemplos.

WhatsApp.

Correo electrónico.

Facturación electrónica.

Aplicación móvil.

API pública.

Portal de clientes.

Reportes financieros.

Múltiples sucursales.

Cada nueva funcionalidad deberá integrarse mediante nuevos servicios.

Nunca modificando innecesariamente los ya existentes.

---

# Rendimiento

El sistema deberá responder rápidamente incluso con miles de clientes registrados.

Se deberán minimizar.

Consultas repetidas.

Operaciones innecesarias.

Lecturas duplicadas.

Toda consulta deberá optimizarse.

Los índices de SQLite deberán aprovecharse correctamente.

---

# Mantenibilidad

Todo el proyecto deberá poder mantenerse fácilmente.

Para ello.

Cada archivo tendrá una única responsabilidad.

Cada función deberá ser pequeña.

Cada clase deberá resolver un único problema.

No deberán existir archivos excesivamente grandes.

La estructura deberá facilitar encontrar cualquier componente rápidamente.

---

# Convenciones

Todo el código deberá seguir una convención uniforme.

Archivos.

snake_case

Clases.

PascalCase

Funciones.

snake_case

Variables.

snake_case

Constantes.

UPPER_CASE

Endpoints.

RESTful.

Modelos.

Singular.

Tablas.

Plural.

---

# Calidad del Código

Todo el desarrollo deberá cumplir.

SOLID.

DRY.

KISS.

Clean Architecture.

Clean Code.

Se priorizará siempre.

Legibilidad.

Mantenibilidad.

Escalabilidad.

Antes que escribir menos líneas de código.

---

# Dependencias

Toda dependencia utilizada deberá justificarse.

No instalar librerías innecesarias.

No utilizar paquetes abandonados.

Preferir librerías ampliamente utilizadas y mantenidas.

---

# Compatibilidad

El sistema deberá ejecutarse correctamente en.

Windows 10.

Windows 11.

No será necesario soportar Linux o macOS en la primera versión.

Sin embargo.

La arquitectura no deberá impedir una futura compatibilidad multiplataforma.

---

# Pruebas

Cada módulo desarrollado deberá poder probarse de manera independiente.

Los servicios deberán diseñarse pensando en pruebas unitarias.

Las funcionalidades críticas deberán tener pruebas de integración.

Antes de dar una fase por terminada.

Todas las pruebas deberán ejecutarse satisfactoriamente.

---

# Documentación

Todo módulo nuevo deberá incluir.

Descripción.

Responsabilidad.

Dependencias.

Puntos de entrada.

Puntos de salida.

La documentación deberá mantenerse sincronizada con el código.

---

# Evolución

La arquitectura deberá permitir evolucionar el sistema sin reestructuraciones importantes.

Agregar nuevas funcionalidades nunca deberá requerir modificar grandes cantidades de código existente.

Se favorecerá la extensión sobre la modificación.

---

# Principio Fundamental

La arquitectura del Sistema de Administración de Préstamos deberá priorizar siempre.

Estabilidad.

Escalabilidad.

Legibilidad.

Mantenibilidad.

Seguridad.

Facilidad de evolución.

Toda decisión técnica deberá respetar estos principios.

---

# Declaración Final

Este documento define oficialmente la arquitectura del Sistema de Administración de Préstamos de CREEMOS EN TI SAS.

Toda implementación deberá seguir esta arquitectura.

Cualquier cambio estructural deberá reflejarse primero en este documento antes de implementarse en el software.

---

**Fin del documento.**