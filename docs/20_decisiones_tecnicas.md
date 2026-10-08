# DECISIONES TÉCNICAS
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento define todas las decisiones técnicas oficiales del proyecto.

Estas decisiones no deberán modificarse durante el desarrollo salvo autorización expresa.

El propósito es evitar cambios innecesarios de arquitectura y mantener la consistencia del sistema.

---

# Arquitectura

La arquitectura oficial será.

Frontend.

React.

TypeScript.

Vite.

TailwindCSS.

React Router.

React Query.

Backend.

Python.

FastAPI.

SQLAlchemy.

Alembic.

SQLite.

ReportLab.

No utilizar tecnologías diferentes sin autorización.

---

# Base de Datos

La única base de datos oficial será SQLite.

No reemplazar SQLite por.

PostgreSQL.

MySQL.

MariaDB.

SQL Server.

MongoDB.

Firebase.

La arquitectura deberá permitir futuras migraciones, pero la primera versión utilizará exclusivamente SQLite.

---

# Persistencia

Toda la información oficial será almacenada en SQLite.

Microsoft Excel únicamente será utilizado como archivo sincronizado.

Nunca utilizar Excel como fuente principal de información.

---

# Generación de PDF

Todos los recibos deberán generarse utilizando ReportLab.

No utilizar.

HTML.

Puppeteer.

Playwright.

wkhtmltopdf.

Librerías basadas en navegador.

El PDF deberá generarse directamente desde Python.

---

# Interfaz

Toda la interfaz deberá desarrollarse utilizando React y TailwindCSS.

No utilizar.

Bootstrap.

Material UI.

Ant Design.

Bulma.

Semantic UI.

El diseño será completamente personalizado.

---

# Estado Global

La información compartida por la aplicación deberá administrarse utilizando React Query y Context API cuando corresponda.

Evitar estados globales innecesarios.

No incorporar Redux salvo que exista una necesidad real documentada.

---

# Comunicación

Toda comunicación entre Frontend y Backend deberá realizarse mediante la API REST.

Nunca acceder directamente a SQLite desde React.

Nunca acceder directamente a archivos Excel desde React.

---

# Validaciones

Las validaciones deberán realizarse en dos niveles.

Frontend.

Mejorar experiencia del usuario.

Backend.

Garantizar integridad.

La validación del Backend siempre tendrá prioridad.

---

# Sincronización

Todo cambio seguirá este flujo.

Usuario.

↓

Backend.

↓

SQLite.

↓

Respaldo.

↓

Excel.

↓

PDF.

↓

Dashboard.

Nunca alterar este orden.

---

# Gestión de Archivos

Los archivos Excel serán administrados exclusivamente mediante el sistema.

No utilizar rutas absolutas.

No depender del nombre del archivo.

Toda la configuración deberá almacenarse en SQLite.

---

# Impresión

La impresión deberá realizarse desde el PDF generado.

Nunca imprimir directamente desde una vista HTML.

La vista previa y el PDF deberán ser idénticos.

---

# Backups

Todo respaldo deberá crearse automáticamente.

Nunca sobrescribir respaldos.

Toda restauración deberá crear previamente un nuevo respaldo.

---

# Seguridad

Autenticación.

JWT.

Contraseñas.

Hash seguro.

Roles.

Administrador.

Empleado.

Nunca almacenar información sensible en texto plano.

---

# Código

Seguir obligatoriamente.

PEP 8.

SOLID.

DRY.

KISS.

Clean Code.

Clean Architecture.

TypeScript Strict Mode.

ESLint.

Prettier.

No desactivar reglas para evitar corregir errores.

---

# Dependencias

Antes de incorporar una nueva librería.

OpenCode deberá verificar.

Que tenga mantenimiento activo.

Que sea ampliamente utilizada.

Que sea compatible con la arquitectura.

Que realmente sea necesaria.

Evitar dependencias innecesarias.

---

# Principios

Siempre priorizar.

Integridad.

Seguridad.

Mantenibilidad.

Escalabilidad.

Legibilidad.

Consistencia.

El rendimiento será importante, pero nunca comprometerá estos principios.

---

# Tecnologías Aprobadas

Frontend.

React.

TypeScript.

Vite.

TailwindCSS.

React Router.

React Query.

Backend.

Python.

FastAPI.

SQLAlchemy.

Alembic.

SQLite.

ReportLab.

Herramientas.

Git.

GitHub.

Pytest.

ESLint.

Prettier.

---

# Tecnologías No Aprobadas

No utilizar.

Electron.

Vue.

Angular.

Laravel.

Django.

MongoDB.

Firebase.

Bootstrap.

Material UI.

Redux (salvo necesidad justificada).

---

# Declaración Final

Este documento define las decisiones técnicas oficiales del Sistema de Administración de Préstamos de CREEMOS EN TI SAS.

Toda implementación deberá respetar estas decisiones durante el desarrollo del proyecto.

---

**Fin del documento.**