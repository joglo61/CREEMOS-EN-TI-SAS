# INSTRUCCIONES PARA OPENCODE
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento contiene las instrucciones que OpenCode deberá seguir durante todo el desarrollo del proyecto.

Estas instrucciones tienen prioridad sobre cualquier decisión técnica que OpenCode considere conveniente.

El objetivo es garantizar que todo el proyecto sea desarrollado exactamente como lo necesita la empresa.

---

# Regla Principal

OpenCode no deberá improvisar funcionalidades.

No deberá asumir comportamientos.

No deberá inventar reglas del negocio.

Toda implementación deberá basarse únicamente en la documentación existente dentro de la carpeta **docs/**.

Si encuentra información insuficiente.

Deberá detener esa funcionalidad y solicitar una aclaración.

Nunca deberá tomar decisiones financieras por su cuenta.

---

# Prioridad de la Documentación

En caso de existir dos documentos relacionados con una misma funcionalidad.

La prioridad será.

1.
README.md

↓

2.
REQUERIMIENTOS.md

↓

3.
REGLAS_NEGOCIO.md

↓

4.
ARQUITECTURA.md

↓

5.
BASE_DATOS.md

↓

6.
CASOS_USO.md

↓

7.
FUNCIONALIDADES.md

↓

8.
UI_UX.md

↓

9.
API.md

↓

10.
RECIBOS.md

↓

11.
PLANTILLA_RECIBO.md

↓

12.
SINCRONIZACION_EXCEL.md

↓

13.
SEGURIDAD.md

↓

14.
DESARROLLO.md

↓

15.
PLAN_PRUEBAS.md

↓

16.
DESPLIEGUE.md

Si existe una contradicción.

Siempre deberá respetarse el documento con mayor prioridad.

---

# Desarrollo por Etapas

OpenCode no deberá desarrollar todo el sistema simultáneamente.

Cada módulo deberá terminarse completamente antes de comenzar el siguiente.

El orden obligatorio será.

Autenticación.

↓

Base de datos.

↓

Clientes.

↓

Préstamos.

↓

Pagos.

↓

Recibos.

↓

Dashboard.

↓

Archivos Excel.

↓

Configuración.

↓

Usuarios.

↓

Logs.

↓

Backups.

↓

Optimización.

Nunca comenzar un módulo sin terminar completamente el anterior.

---

# Prohibiciones

OpenCode nunca deberá.

Eliminar información financiera.

Eliminar pagos.

Eliminar facturas.

Eliminar historiales.

Modificar pagos antiguos.

Modificar facturas antiguas.

Modificar recibos emitidos.

Modificar registros históricos.

Toda la información financiera deberá conservarse permanentemente.

---

# Automatización

Siempre que una tarea pueda automatizarse.

OpenCode deberá automatizarla.

El operador únicamente deberá ingresar la información que el sistema no pueda conocer automáticamente.

Toda la lógica deberá ejecutarse dentro del Backend.

Nunca dentro del Frontend.

---

# SQLite

SQLite será siempre la fuente oficial.

Nunca utilizar Excel como base principal.

Nunca leer información financiera directamente desde Excel.

Toda consulta deberá obtener la información desde SQLite.

Excel únicamente deberá sincronizarse.

---

# Excel

El sistema nunca dependerá del nombre de los archivos Excel.

Siempre deberá existir un módulo para.

Cargar.

Reemplazar.

Validar.

Sincronizar.

Respaldar.

Restaurar.

Nunca utilizar rutas fijas escritas dentro del código.

---

# Calidad del Código

Todo el proyecto deberá respetar.

SOLID.

DRY.

KISS.

Clean Code.

Clean Architecture.

El código deberá ser fácil de leer.

Fácil de modificar.

Fácil de mantener.

Nunca priorizar escribir menos líneas sobre escribir un código claro.

---

# Organización

Cada archivo deberá tener una única responsabilidad.

Cada función deberá resolver un único problema.

Cada clase deberá representar una única entidad.

Nunca crear archivos excesivamente grandes.

Nunca mezclar lógica financiera con lógica de interfaz.

---

# Backend

Toda la lógica del negocio deberá implementarse en el Backend.

Nunca calcular intereses en React.

Nunca calcular mora en React.

Nunca generar números de factura en React.

Nunca actualizar saldos en React.

El Frontend únicamente solicitará información al Backend.

---

# Frontend

El Frontend será responsable únicamente de.

Mostrar información.

Capturar información.

Consumir la API.

Mostrar mensajes.

Mostrar errores.

Nunca deberá contener reglas del negocio.

# Base de Datos

Toda modificación de información deberá realizarse utilizando SQLAlchemy.

Nunca escribir consultas SQL distribuidas por el proyecto.

Toda interacción con SQLite deberá pasar por los repositorios.

Nunca acceder directamente a la base de datos desde los controladores.

---

# API

Todos los datos deberán pasar por la API REST.

Nunca permitir acceso directo desde React hacia SQLite.

Todos los endpoints deberán utilizar.

Schemas.

Validaciones.

Autenticación.

Autorización.

Logs.

---

# Seguridad

Toda información deberá validarse dos veces.

Frontend.

↓

Backend.

La validación del Backend será la única considerada definitiva.

Nunca confiar en información enviada por el navegador.

---

# Manejo de Errores

Nunca mostrar errores técnicos al usuario.

Nunca mostrar.

Stack Trace.

Errores SQL.

Errores de Python.

Rutas del servidor.

Información sensible.

Los detalles completos únicamente deberán registrarse en los logs.

---

# Registro de Logs

Toda operación importante deberá generar un registro.

Como mínimo.

Inicio de sesión.

Cerrar sesión.

Crear cliente.

Editar cliente.

Registrar pago.

Generar recibo.

Actualizar Excel.

Crear respaldo.

Restaurar respaldo.

Modificar configuración.

Error.

Toda esta información permitirá realizar auditorías posteriormente.

---

# Cálculos Financieros

Todos los cálculos deberán realizarse utilizando las reglas definidas en.

REGLAS_NEGOCIO.md

Nunca modificar las fórmulas.

Nunca aproximar resultados.

Nunca cambiar el comportamiento financiero sin autorización.

---

# Pagos

Todo pago deberá seguir exactamente este flujo.

Buscar cliente.

↓

Ingresar valor recibido.

↓

Calcular intereses.

↓

Calcular mora.

↓

Calcular capital.

↓

Actualizar saldo.

↓

Actualizar fecha.

↓

Registrar pago.

↓

Crear factura.

↓

Actualizar SQLite.

↓

Respaldar.

↓

Actualizar Excel.

↓

Generar PDF.

↓

Guardar PDF.

↓

Actualizar Dashboard.

↓

Registrar logs.

↓

Imprimir.

Nunca alterar este flujo.

---

# Facturas

Cada factura deberá ser.

Única.

Consecutiva.

Inmutable.

Nunca reutilizar números.

Nunca modificar una factura emitida.

Nunca eliminar una factura.

---

# Recibos

Todo recibo deberá cumplir exactamente el diseño definido en.

PLANTILLA_RECIBO.md

Nunca modificar la distribución.

Nunca agregar elementos decorativos.

Nunca cambiar el formato sin autorización.

---

# Dashboard

Toda la información del Dashboard deberá obtenerse desde SQLite.

Nunca consultar directamente Excel.

Nunca calcular indicadores desde React.

Toda la lógica deberá permanecer en el Backend.

---

# Sincronización

Después de cada operación financiera.

Actualizar SQLite.

↓

Crear respaldo.

↓

Actualizar Excel.

↓

Validar.

↓

Registrar.

Si Excel falla.

SQLite continuará siendo la fuente oficial.

Nunca perder información financiera debido a un error de sincronización.

---

# Backups

Antes de modificar.

SQLite.

Configuración.

Excel.

El sistema deberá crear automáticamente un respaldo.

Nunca sobrescribir respaldos existentes.

---

# Pruebas

Cada funcionalidad desarrollada deberá incluir.

Pruebas unitarias.

Pruebas de integración.

Cuando corresponda.

Pruebas funcionales.

No considerar terminada una funcionalidad sin pruebas.

---

# Documentación

Cada módulo implementado deberá mantenerse sincronizado con la documentación.

Si durante el desarrollo se modifica una funcionalidad.

La documentación correspondiente deberá actualizarse inmediatamente.

Nunca permitir que el código y la documentación diverjan.

---

# Código

Todo código deberá ser.

Legible.

Modular.

Escalable.

Reutilizable.

Bien organizado.

Antes de escribir código.

Priorizar siempre una arquitectura limpia sobre una solución rápida.

# Convenciones

Todo el proyecto deberá utilizar una única convención de nombres.

Archivos.

snake_case

Funciones.

snake_case

Variables.

snake_case

Clases.

PascalCase

Constantes.

UPPER_CASE

Endpoints.

RESTful.

Modelos.

Singular.

Tablas.

Plural.

No mezclar estilos.

---

# Rendimiento

OpenCode deberá evitar.

Consultas innecesarias.

Código duplicado.

Operaciones repetidas.

Procesos bloqueantes.

Siempre que una tarea pesada pueda ejecutarse en segundo plano sin afectar la integridad de la información.

Deberá implementarse de esa forma.

---

# Escalabilidad

Todo el código deberá prepararse para futuras funcionalidades.

Entre ellas.

Facturación electrónica.

WhatsApp.

Portal de clientes.

Aplicación móvil.

Múltiples sucursales.

Múltiples cajas.

Reportes avanzados.

Nuevos tipos de préstamos.

Nunca escribir código que impida agregar estas funcionalidades posteriormente.

---

# Código Prohibido

OpenCode nunca deberá.

Duplicar lógica.

Copiar código entre módulos.

Crear funciones gigantes.

Crear archivos excesivamente grandes.

Escribir lógica financiera dentro de componentes React.

Acceder directamente a SQLite desde el Frontend.

Modificar información histórica.

Eliminar información financiera.

---

# Calidad Esperada

Todo el código deberá cumplir.

PEP 8.

TypeScript Strict Mode.

ESLint.

Prettier.

Tipado fuerte.

Separación de responsabilidades.

Arquitectura modular.

No deberá existir código muerto.

No deberán existir funciones sin utilizar.

No deberán existir dependencias innecesarias.

---

# Revisión Antes de Finalizar una Funcionalidad

Antes de considerar terminada cualquier funcionalidad.

OpenCode deberá verificar.

✓ El código compila.

✓ No existen errores.

✓ Todas las pruebas pasan correctamente.

✓ La documentación está actualizada.

✓ La funcionalidad respeta las reglas del negocio.

✓ La interfaz coincide con el diseño definido.

✓ SQLite se actualiza correctamente.

✓ Excel se sincroniza correctamente.

✓ El PDF se genera correctamente.

✓ Los logs se registran correctamente.

✓ No se rompió ninguna funcionalidad existente.

Solo después de cumplir todos estos puntos.

La funcionalidad podrá considerarse terminada.

---

# Forma de Trabajar

Durante todo el proyecto.

OpenCode deberá trabajar de forma incremental.

Cada entrega deberá ser completamente funcional.

No dejar funcionalidades a medio terminar.

No escribir código temporal.

No utilizar soluciones provisionales.

No agregar comentarios como.

TODO

FIXME

TEMP

HACK

La primera versión deberá desarrollarse con calidad de producción.

---

# Comunicación

Si durante el desarrollo existe cualquier ambigüedad.

OpenCode deberá detener la implementación.

Explicar claramente el problema.

Indicar las alternativas posibles.

Esperar una decisión antes de continuar.

Nunca asumir reglas del negocio.

Nunca inventar comportamientos.

---

# Responsabilidad

OpenCode será responsable de mantener.

La arquitectura.

La calidad.

La seguridad.

La escalabilidad.

La mantenibilidad.

La consistencia.

Durante todo el desarrollo.

Cada cambio deberá respetar todos los documentos existentes en la carpeta docs.

---

# Principio Fundamental

OpenCode deberá comportarse como un desarrollador senior especializado en software financiero.

La prioridad absoluta será.

Integridad de la información.

Seguridad.

Calidad.

Mantenibilidad.

Escalabilidad.

Las decisiones de implementación nunca deberán comprometer estos principios.

---

# Declaración Final

Este documento define oficialmente las reglas que OpenCode deberá seguir durante el desarrollo del Sistema de Administración de Préstamos de CREEMOS EN TI SAS.

Todas las implementaciones deberán respetar estas instrucciones además de la documentación técnica y funcional del proyecto.

---

**Fin del documento.**