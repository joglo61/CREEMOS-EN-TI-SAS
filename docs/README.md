# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión: 1.0

---

# Descripción General

El Sistema de Administración de Préstamos de CREEMOS EN TI SAS es una plataforma desarrollada para administrar completamente el proceso de otorgamiento y recaudo de préstamos destinados a la compra de taxis.

El propósito principal del sistema es reemplazar el proceso manual realizado actualmente mediante archivos de Microsoft Excel y recibos físicos escritos a mano, automatizando toda la operación financiera de la empresa sin modificar la forma en que actualmente trabaja el personal administrativo.

Este sistema deberá convertirse en la herramienta principal utilizada por la empresa para administrar la totalidad de la cartera de clientes.

El software deberá ser confiable, rápido, intuitivo y preparado para crecer durante muchos años.

---

# Objetivos del Proyecto

El sistema tendrá como objetivos principales:

• Automatizar el cálculo de intereses.

• Automatizar el cálculo de intereses por mora.

• Automatizar la actualización del saldo de cada préstamo.

• Automatizar la generación de recibos.

• Automatizar el consecutivo de facturas.

• Automatizar la sincronización de información con Microsoft Excel.

• Eliminar completamente los cálculos manuales.

• Reducir errores humanos.

• Disminuir el tiempo de atención al cliente.

• Mantener un historial completo de todas las operaciones realizadas.

• Facilitar la administración de la cartera.

---

# Alcance

El sistema administrará completamente:

- Clientes
- Préstamos
- Pagos
- Facturación
- Historial
- Cronogramas
- Usuarios
- Configuración
- Reportes
- Sincronización con Excel

El sistema será utilizado únicamente por el personal administrativo de la empresa.

No será un sistema público.

No existirá acceso para clientes.

---

# Filosofía del Proyecto

Este proyecto NO busca modernizar la forma de trabajar de la empresa.

Busca automatizarla.

El usuario deberá sentir que continúa realizando exactamente el mismo trabajo que realiza actualmente, únicamente reemplazando el papel y los cálculos manuales por un sistema que realiza todas esas tareas automáticamente.

Por esta razón el diseño deberá priorizar:

• Rapidez.

• Simplicidad.

• Claridad.

• Estabilidad.

• Facilidad de uso.

No deberá priorizar animaciones, efectos visuales o diseños llamativos.

---

# Objetivos Técnicos

El sistema deberá ser:

• Modular.

• Escalable.

• Seguro.

• Fácil de mantener.

• Fácil de ampliar.

• Fácil de documentar.

• Fácil de probar.

Toda la arquitectura deberá permitir agregar nuevas funcionalidades sin modificar las ya existentes.

---

# Tecnologías

## Frontend

React

TypeScript

Vite

TailwindCSS

Axios

React Router

React Hook Form

Zod

TanStack Query

---

## Backend

Python

FastAPI

SQLAlchemy

Alembic

Pydantic

JWT

Passlib

---

## Base de Datos

SQLite

SQLite será la única base de datos oficial del sistema.

Toda la información será almacenada aquí.

---

## Archivos Excel

Los archivos Excel NO serán la base principal.

El sistema utilizará SQLite como fuente oficial.

Los archivos Excel funcionarán como archivos sincronizados para mantener la compatibilidad con el flujo de trabajo actual de la empresa.

---

## PDFs

Los recibos serán generados mediante ReportLab.

Todos los recibos deberán almacenarse automáticamente.

Todos deberán poder reimprimirse posteriormente.

---

# Arquitectura General

El sistema estará dividido en cuatro capas principales.

Frontend

↓

API REST

↓

Servicios de Negocio

↓

Persistencia

Cada capa tendrá una única responsabilidad.

No se permitirá mezclar responsabilidades entre capas.

---

# Fuente Oficial de Información

Toda la información del negocio será almacenada exclusivamente en SQLite.

El sistema nunca utilizará Excel como base principal.

SQLite siempre tendrá prioridad sobre cualquier otro origen de datos.

---

# Sincronización con Excel

La empresa continuará utilizando archivos Microsoft Excel.

Sin embargo, dichos archivos dejarán de ser la fuente oficial de información.

El sistema permitirá cargar los archivos Excel desde la interfaz de administración.

Los nombres de los archivos NO serán fijos.

El usuario podrá reemplazarlos cuando sea necesario.

Los archivos serán:

• Base de datos de clientes.

• Archivo utilizado para cálculos financieros.

Después de cada operación exitosa, el sistema actualizará automáticamente los archivos correspondientes.

Antes de actualizar cualquier archivo Excel, el sistema deberá generar automáticamente una copia de seguridad.

---

# Administración de Archivos

El sistema contará con un módulo específico para administrar los archivos utilizados por la empresa.

Desde este módulo será posible:

• Cargar el archivo Excel de clientes.

• Cargar el archivo Excel utilizado para cálculos financieros.

• Reemplazar cualquiera de los archivos.

• Validar la estructura antes de aceptarlos.

• Ver la fecha de la última carga.

• Verificar si los archivos están sincronizados.

• Restaurar la última copia de seguridad en caso de error.

Los usuarios nunca deberán copiar archivos manualmente dentro de la carpeta del proyecto.

Toda la administración deberá realizarse desde la interfaz del sistema.

---

# Estructura General del Proyecto

El repositorio deberá mantener la siguiente estructura desde el inicio del desarrollo.

```
prestamos-creemos-en-ti/

│
├── README.md
│
├── docs/
│   ├── 01_VISION_NEGOCIO.md
│   ├── 02_REGLAS_NEGOCIO.md
│   ├── 03_ARQUITECTURA.md
│   ├── 04_BASE_DATOS.md
│   ├── 05_CASOS_USO.md
│   ├── 06_FUNCIONALIDADES.md
│   ├── 07_UI_UX.md
│   ├── 08_API.md
│   ├── 09_RECIBOS.md
│   ├── 10_PLANTILLA_RECIBO.md
│   ├── 11_SINCRONIZACION_EXCEL.md
│   ├── 12_SEGURIDAD.md
│   ├── 13_DESARROLLO.md
│   ├── 14_ROADMAP.md
│   ├── 15_PRUEBAS.md
│   ├── 16_BACKUPS.md
│   ├── 17_DESPLIEGUE.md
│   └── 18_FUTURAS_MEJORAS.md
│
├── backend/
│
├── frontend/
│
├── database/
│
├── data/
│
├── backups/
│
├── recibos/
│
└── assets/
```

---

# Usuarios del Sistema

Inicialmente existirán dos tipos de usuarios.

## Administrador

Podrá:

- Crear clientes.
- Editar clientes.
- Registrar pagos.
- Consultar historial.
- Reimprimir recibos.
- Configurar parámetros del sistema.
- Cargar archivos Excel.
- Crear usuarios.
- Editar usuarios.
- Consultar reportes.
- Administrar respaldos.

---

## Empleado

Podrá:

- Buscar clientes.
- Registrar pagos.
- Consultar historial.
- Reimprimir recibos.

No podrá modificar configuraciones críticas del sistema.

---

# Flujo General del Sistema

El funcionamiento esperado será el siguiente.

Inicio de sesión

↓

Dashboard

↓

Buscar Cliente

↓

Seleccionar Cliente

↓

Ingresar Valor del Pago

↓

El sistema calcula automáticamente:

- Intereses
- Mora
- Capital
- Nuevo saldo

↓

Vista previa del recibo

↓

Guardar

↓

Actualizar SQLite

↓

Actualizar Excel

↓

Generar PDF

↓

Imprimir

↓

Registrar historial

↓

Proceso finalizado

---

# Información Administrada

El sistema almacenará como mínimo la siguiente información.

## Clientes

Nombre

Cédula

Placa

Teléfono

Dirección

Estado

Observaciones

---

## Préstamos

Capital inicial

Saldo pendiente

Valor cuota

Fecha inicio

Fecha primer pago

Fecha próximo pago

Estado

---

## Pagos

Número factura

Fecha

Intereses

Capital

Valor recibido

Saldo anterior

Saldo nuevo

Usuario

Observaciones

---

## Facturas

Número

Fecha

PDF

Cliente

Pago asociado

---

## Usuarios

Nombre

Usuario

Contraseña cifrada

Rol

Estado

---

## Configuración

Empresa

NIT

Dirección

Teléfono

Logo

Tasa

Días de gracia

Número siguiente de factura

Ruta de archivos

---

# Principios de Desarrollo

Todo el desarrollo deberá respetar los siguientes principios.

- Código limpio.
- Arquitectura limpia.
- SOLID.
- DRY.
- KISS.
- Alta cohesión.
- Bajo acoplamiento.

No se aceptarán implementaciones rápidas que comprometan la calidad del sistema.

---

# Rendimiento

El sistema deberá responder rápidamente incluso con miles de clientes registrados.

La búsqueda de clientes deberá realizarse prácticamente en tiempo real.

Las consultas deberán optimizarse.

No deberán existir operaciones innecesarias sobre la base de datos.

---

# Seguridad

Todas las contraseñas deberán almacenarse utilizando hash seguro.

Nunca almacenar contraseñas en texto plano.

Todas las operaciones deberán validar permisos.

Toda modificación importante deberá registrarse.

---

# Escalabilidad

El proyecto deberá quedar preparado para incorporar en futuras versiones.

- Facturación electrónica.
- Portal para clientes.
- Aplicación móvil.
- Integración con WhatsApp.
- Reportes avanzados.
- Múltiples sucursales.
- Múltiples cajas.
- Nuevos tipos de préstamos.

Estas funcionalidades no harán parte de la primera versión pero la arquitectura deberá permitir incorporarlas sin rehacer el sistema.

---

# Objetivo del Desarrollo

El propósito de este proyecto no es únicamente automatizar el proceso actual.

El objetivo es construir una plataforma estable, profesional y preparada para convertirse en el sistema principal de administración de cartera de CREEMOS EN TI SAS durante muchos años.

Toda decisión técnica deberá favorecer la estabilidad, la mantenibilidad y la facilidad de evolución del software.

---

# Documentación

Toda la documentación funcional y técnica del proyecto se encuentra en la carpeta `docs`.

Antes de implementar cualquier funcionalidad, es obligatorio leer completamente la documentación correspondiente.

Ningún desarrollador ni agente de inteligencia artificial deberá comenzar a escribir código sin comprender primero la lógica del negocio y la arquitectura definida en estos documentos.

# Flujo General del Desarrollo

El desarrollo del sistema deberá seguir estrictamente las fases definidas en la documentación del proyecto.

No se permitirá desarrollar funcionalidades de fases futuras antes de finalizar completamente la fase actual.

Cada fase deberá cumplir los siguientes requisitos antes de darse por terminada:

- Código funcional.
- Sin errores conocidos.
- Probado manualmente.
- Documentado.
- Integrado con el resto del sistema.
- Aprobado antes de continuar.

---

# Orden Oficial de Desarrollo

## Fase 1

Inicialización del proyecto.

Configuración del Backend.

Configuración del Frontend.

Configuración de SQLite.

Configuración del entorno de desarrollo.

Autenticación.

---

## Fase 2

Modelo de base de datos.

Migraciones.

Configuración inicial.

Relaciones.

Repositorio.

---

## Fase 3

Administración de clientes.

Crear.

Editar.

Consultar.

Buscar.

---

## Fase 4

Administración de préstamos.

Crear.

Editar.

Consultar.

Cronograma.

---

## Fase 5

Registro de pagos.

Cálculo de intereses.

Cálculo de mora.

Actualización de saldos.

---

## Fase 6

Facturación.

Generación de PDF.

Impresión.

Historial.

---

## Fase 7

Dashboard.

Indicadores.

Reportes.

Consultas.

---

## Fase 8

Sincronización con Excel.

Carga de archivos.

Validaciones.

Backups.

---

## Fase 9

Optimización.

Pruebas.

Preparación para producción.

---

# Restricciones del Proyecto

Durante todo el desarrollo deberán respetarse las siguientes restricciones.

Nunca realizar cálculos financieros desde el Frontend.

Nunca acceder directamente a SQLite desde React.

Nunca modificar la base de datos desde el Frontend.

Nunca utilizar el archivo Excel como fuente oficial de información.

Nunca duplicar lógica financiera.

Nunca generar recibos desde el Frontend.

Nunca almacenar información sensible sin cifrar.

Nunca reutilizar números de factura.

Nunca eliminar pagos registrados.

Nunca eliminar facturas.

Nunca eliminar clientes físicamente.

Toda eliminación deberá implementarse mediante estados de activo o inactivo.

---

# Copias de Seguridad

El sistema deberá crear automáticamente respaldos de:

Base de datos SQLite.

Archivo Excel de clientes.

Archivo Excel utilizado para cálculos.

Configuración del sistema.

Los respaldos deberán almacenarse organizados por fecha y hora.

El sistema deberá permitir restaurar respaldos desde la interfaz de administración.

---

# Calidad Esperada

El software deberá estar preparado para ser utilizado diariamente durante toda la jornada laboral.

La estabilidad será más importante que la cantidad de funcionalidades.

Toda funcionalidad deberá implementarse pensando en el largo plazo.

No deberán existir soluciones temporales.

No deberán existir módulos experimentales.

Todo el código deberá quedar listo para producción.

---

# Instrucciones para OpenCode

Antes de comenzar cualquier implementación deberás leer completamente todos los documentos ubicados dentro de la carpeta `/docs`.

No escribas código sin comprender completamente las reglas del negocio.

Si encuentras inconsistencias entre documentos, informa el problema antes de continuar.

Nunca modifiques una regla del negocio sin autorización.

Siempre propón mejoras técnicas cuando no alteren el funcionamiento esperado por la empresa.

Trabaja únicamente por fases.

No desarrolles funcionalidades de fases posteriores.

Al finalizar cada fase deberás entregar:

- Resumen técnico.
- Archivos creados.
- Archivos modificados.
- Explicación de la arquitectura implementada.
- Instrucciones para ejecutar.
- Instrucciones para realizar pruebas.
- Posibles mejoras detectadas.

No continúes automáticamente con la siguiente fase hasta recibir aprobación.

---

# Criterios de Éxito

Se considerará que el proyecto ha sido completado exitosamente cuando:

- Toda la información se almacene correctamente en SQLite.
- Los archivos Excel permanezcan sincronizados.
- El registro de pagos sea completamente automático.
- Los intereses y la mora sean calculados correctamente.
- Los recibos sean generados automáticamente con el formato definido.
- El sistema permita reimprimir cualquier recibo.
- El Dashboard muestre información en tiempo real.
- El sistema sea estable, rápido y fácil de utilizar.
- La empresa pueda abandonar completamente el proceso manual sin afectar su operación diaria.

---

# Licencia

Este software ha sido diseñado exclusivamente para CREEMOS EN TI SAS.

Toda la documentación contenida en este proyecto constituye la especificación oficial del sistema.

Cualquier modificación futura deberá respetar las reglas de negocio aquí definidas.

---

**Fin del documento.**