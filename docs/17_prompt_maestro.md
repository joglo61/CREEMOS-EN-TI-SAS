# PROMPT MAESTRO PARA OPENCODE
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento define la forma en la que OpenCode deberá trabajar durante todo el desarrollo del proyecto.

No describe una funcionalidad específica.

Describe la metodología que deberá seguir para construir todo el sistema.

Estas instrucciones tienen prioridad sobre cualquier decisión técnica que OpenCode considere conveniente.

---

# Contexto del Proyecto

Se desarrollará un sistema de escritorio para CREEMOS EN TI SAS.

La empresa realiza préstamos para la compra de taxis.

Actualmente toda la información se administra mediante archivos Microsoft Excel.

El objetivo del proyecto NO es cambiar la forma de trabajar de la empresa.

El objetivo es automatizar exactamente el proceso actual.

---

# Objetivo Principal

Construir un software profesional que permita.

• Administrar clientes.

• Administrar préstamos.

• Registrar pagos.

• Calcular intereses.

• Calcular mora.

• Generar recibos.

• Imprimir recibos.

• Actualizar automáticamente SQLite.

• Sincronizar automáticamente Microsoft Excel.

• Mantener historial.

• Generar respaldos.

Todo el sistema deberá funcionar sin modificar el flujo de trabajo actual de la empresa.

---

# Forma de Trabajar

OpenCode deberá trabajar únicamente por fases.

Nunca desarrollar todo simultáneamente.

Cada módulo deberá quedar completamente terminado antes de iniciar el siguiente.

Cada fase deberá incluir.

Implementación.

Pruebas.

Correcciones.

Documentación.

Solo entonces podrá comenzar la siguiente fase.

---

# Documentación

Toda la documentación ubicada dentro de la carpeta docs constituye la especificación oficial del sistema.

Nunca asumir comportamientos.

Nunca inventar reglas.

Nunca implementar funcionalidades no documentadas.

Si existe cualquier duda.

Detener el desarrollo correspondiente.

Explicar el problema.

Esperar una decisión.

---

# Prioridad

Siempre priorizar.

Integridad de la información.

↓

Seguridad.

↓

Calidad del código.

↓

Mantenibilidad.

↓

Escalabilidad.

↓

Rendimiento.

Nunca sacrificar integridad por velocidad.

---

# Arquitectura

El proyecto deberá respetar estrictamente la arquitectura definida.

Frontend.

React.

TypeScript.

Vite.

TailwindCSS.

Backend.

Python.

FastAPI.

SQLite.

SQLAlchemy.

Alembic.

ReportLab.

Nunca modificar esta arquitectura sin autorización.

---

# SQLite

SQLite será siempre la fuente oficial.

Toda modificación deberá almacenarse primero allí.

Después.

Excel.

Después.

PDF.

Nunca invertir este orden.

---

# Excel

Microsoft Excel continuará utilizándose únicamente porque la empresa ya está acostumbrada a trabajar con él.

Excel nunca será la fuente oficial.

El sistema deberá permitir.

Cargar.

Reemplazar.

Sincronizar.

Respaldar.

Restaurar.

Archivos Excel.

Nunca depender de nombres específicos.

---

# Flujo Principal

Buscar cliente.

↓

Consultar información.

↓

Ingresar valor recibido.

↓

Calcular intereses.

↓

Calcular mora.

↓

Actualizar saldo.

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

Este flujo nunca deberá modificarse.

---

# Calidad

Todo el código deberá cumplir.

SOLID.

DRY.

KISS.

Clean Code.

Clean Architecture.

PEP 8.

TypeScript Strict.

Nunca escribir código rápido sacrificando calidad.

---

# Código

Cada función deberá resolver un único problema.

Cada archivo deberá tener una única responsabilidad.

Cada módulo deberá ser independiente.

Nunca duplicar lógica.

Nunca copiar código.

Siempre reutilizar componentes.

---

# Seguridad

Nunca almacenar contraseñas en texto plano.

Nunca confiar en información enviada por React.

Toda validación deberá realizarse nuevamente en el Backend.

Nunca mostrar información sensible.

Nunca mostrar errores internos.

---

# Información Financiera

Nunca eliminar.

Clientes.

Préstamos.

Pagos.

Facturas.

Historial.

Recibos.

Toda la información financiera deberá conservarse permanentemente.

---

# Recibos

Todo recibo deberá cumplir exactamente el diseño definido en.

PLANTILLA_RECIBO.md

No modificar distribución.

No agregar decoración.

No convertirlo en una factura electrónica.

Debe conservar apariencia de recibo tradicional.

---

# Desarrollo

OpenCode deberá trabajar como si desarrollara un software bancario.

Toda operación financiera deberá ser considerada crítica.

Todo cambio deberá mantener la consistencia de la información.

---

# Pruebas

Cada módulo desarrollado deberá incluir.

Pruebas unitarias.

Pruebas de integración.

Pruebas funcionales cuando corresponda.

No considerar terminado ningún módulo sin pruebas.

---

# Comunicación

Cuando OpenCode termine una funcionalidad.

Deberá indicar.

Qué hizo.

Qué archivos modificó.

Qué pruebas ejecutó.

Qué falta por implementar.

Nunca avanzar silenciosamente.

---

# Prohibiciones

Nunca.

Modificar pagos antiguos.

Modificar facturas.

Modificar recibos.

Eliminar información financiera.

Escribir lógica financiera en React.

Acceder directamente a SQLite desde React.

Utilizar Excel como base principal.

Duplicar código.

Ignorar errores.

---

# Resultado Esperado

Al finalizar el proyecto deberá existir un sistema profesional.

Seguro.

Escalable.

Rápido.

Fácil de mantener.

Preparado para crecer durante muchos años.

Y completamente adaptado al funcionamiento actual de CREEMOS EN TI SAS.

---

# Declaración Final

Este documento representa la guía principal de trabajo para OpenCode.

Durante todo el desarrollo deberá respetar este documento y toda la documentación ubicada dentro de la carpeta docs.

En caso de conflicto.

La documentación tendrá prioridad sobre cualquier decisión técnica.

---

**Fin del documento.**