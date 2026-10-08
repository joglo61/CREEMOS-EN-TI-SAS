# VISIÓN DEL PROYECTO
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento explica el propósito general del proyecto y la filosofía que deberá guiar todas las decisiones de desarrollo.

Mientras los demás documentos describen qué debe hacer el sistema, este documento explica por qué el sistema existe y cuál es el problema que pretende resolver.

Toda decisión técnica deberá respetar esta visión.

---

# Contexto

CREEMOS EN TI SAS administra préstamos destinados principalmente a la financiación de taxis.

Durante muchos años la empresa ha trabajado utilizando Microsoft Excel como herramienta principal para registrar clientes, controlar pagos y calcular intereses.

Este proceso ha permitido operar correctamente, pero también presenta limitaciones.

Mayor posibilidad de errores manuales.

Duplicación de información.

Procesos repetitivos.

Mayor tiempo de atención.

Mayor dificultad para consultar información histórica.

Dependencia de cálculos manuales.

El propósito del proyecto es eliminar estos problemas sin cambiar la forma de trabajar de la empresa.

---

# Filosofía del Proyecto

Este sistema NO busca transformar completamente la operación de la empresa.

El objetivo es conservar el proceso actual y automatizar todas aquellas tareas que hoy consumen tiempo o generan errores.

El usuario deberá sentir que continúa trabajando de la misma manera, pero con un sistema que realiza automáticamente el trabajo repetitivo.

La tecnología deberá adaptarse a la empresa.

La empresa no deberá adaptarse a la tecnología.

---

# Objetivo Principal

Construir un sistema profesional que permita.

Administrar clientes.

Administrar préstamos.

Registrar pagos.

Calcular intereses.

Calcular mora.

Actualizar saldos.

Generar recibos.

Imprimir recibos.

Sincronizar Microsoft Excel.

Mantener historial.

Crear respaldos.

Todo ello sin modificar el flujo operativo actual.

---

# Principios Fundamentales

Durante todo el desarrollo deberán respetarse los siguientes principios.

Simplicidad.

Automatización.

Consistencia.

Seguridad.

Escalabilidad.

Facilidad de uso.

Mantenibilidad.

Toda decisión deberá favorecer estos principios.

---

# El Usuario es la Prioridad

El sistema será utilizado diariamente por personal administrativo.

No puede asumirse que todos los usuarios tengan conocimientos técnicos.

Por esta razón.

La interfaz deberá ser sencilla.

Las acciones deberán ser claras.

Los mensajes deberán ser fáciles de entender.

Los procesos deberán requerir la menor cantidad posible de clics.

---

# Automatización

Siempre que el sistema pueda realizar una tarea automáticamente.

Deberá hacerlo.

Ejemplos.

Calcular intereses.

Actualizar saldos.

Actualizar SQLite.

Actualizar Excel.

Generar PDF.

Guardar recibos.

Registrar logs.

Crear respaldos.

Actualizar Dashboard.

El usuario únicamente deberá ingresar la información que el sistema no pueda conocer automáticamente.

---

# Microsoft Excel

Microsoft Excel continuará formando parte del proceso porque la empresa está acostumbrada a utilizarlo.

Sin embargo.

Excel dejará de ser el lugar donde ocurre la lógica del negocio.

Toda la lógica financiera dependerá exclusivamente de SQLite.

Excel existirá únicamente como un archivo sincronizado.

Esto permitirá conservar la forma de trabajo actual sin sacrificar la confiabilidad del sistema.

---

# Integridad de la Información

La información financiera representa el activo más importante del sistema.

Nunca deberán perderse.

Pagos.

Facturas.

Recibos.

Historiales.

Respaldos.

Toda operación deberá proteger la integridad de los datos antes que cualquier otro aspecto.

---

# Crecimiento del Sistema

El proyecto deberá desarrollarse pensando en el largo plazo.

Aunque la primera versión será utilizada por una única empresa.

La arquitectura deberá permitir incorporar posteriormente.

Facturación electrónica.

WhatsApp.

Correo electrónico.

Portal de clientes.

Aplicación móvil.

Múltiples sucursales.

Múltiples cajas.

Nuevos tipos de préstamos.

Reportes avanzados.

Sin necesidad de reconstruir el sistema.

---

# Calidad

La primera versión deberá desarrollarse con calidad de producción.

No deberán existir.

Funciones temporales.

Soluciones provisionales.

Código experimental.

Funcionalidades incompletas.

El objetivo es construir una herramienta que pueda utilizarse diariamente desde el primer día.

---

# Papel de OpenCode

OpenCode no deberá comportarse únicamente como un generador de código.

Deberá actuar como un desarrollador senior responsable del proyecto.

Antes de implementar cualquier funcionalidad deberá verificar.

Que respeta la documentación.

Que mantiene la arquitectura.

Que no rompe funcionalidades existentes.

Que conserva la integridad de la información.

Que la solución es mantenible.

Si identifica una mejor alternativa técnica que no modifique las reglas del negocio.

Podrá proponerla antes de implementarla.

---

# Criterio para Tomar Decisiones

Cuando existan varias soluciones posibles.

OpenCode deberá elegir la que mejor cumpla los siguientes criterios.

Mayor simplicidad.

Mayor claridad.

Mayor seguridad.

Mayor mantenibilidad.

Mayor escalabilidad.

Menor complejidad.

Nunca deberá elegir una solución únicamente porque requiere menos líneas de código.

---

# Éxito del Proyecto

El proyecto se considerará exitoso cuando el personal de CREEMOS EN TI SAS pueda utilizar el sistema diariamente sin cambiar su forma habitual de trabajar.

El sistema deberá reducir tiempos.

Reducir errores.

Automatizar procesos.

Facilitar consultas.

Mejorar el control de la información.

Y aumentar la confiabilidad de toda la operación administrativa.

---

# Declaración Final

Este documento representa la visión oficial del Sistema de Administración de Préstamos de CREEMOS EN TI SAS.

Toda decisión de diseño, desarrollo e implementación deberá respetar esta visión.

Si en algún momento una decisión técnica entra en conflicto con esta filosofía.

Deberá priorizarse siempre la simplicidad, la seguridad y la continuidad del proceso de trabajo de la empresa.

---

**Fin del documento.**