# ROADMAP DEL PROYECTO
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento define el orden exacto en el que deberá desarrollarse el sistema.

OpenCode deberá seguir este roadmap estrictamente.

No deberá adelantar fases.

No deberá comenzar una nueva fase mientras la anterior no se encuentre completamente terminada.

El objetivo es construir un sistema estable desde el primer momento.

---

# Filosofía

Cada fase deberá entregar una parte completamente funcional del sistema.

Nunca deberán existir módulos a medio terminar.

Nunca deberán implementarse funcionalidades incompletas.

Cada fase deberá finalizar con.

• Código funcionando.

• Pruebas exitosas.

• Documentación actualizada.

• Integración completa con el resto del sistema.

---

# Flujo General

Cada fase seguirá siempre el mismo proceso.

Analizar.

↓

Diseñar.

↓

Implementar.

↓

Realizar pruebas.

↓

Corregir errores.

↓

Actualizar documentación.

↓

Aprobar.

↓

Continuar con la siguiente fase.

---

# FASE 1

## Preparación del Proyecto

Objetivo.

Crear la estructura base del sistema.

Tareas.

□ Crear repositorio.

□ Crear estructura de carpetas.

□ Configurar Backend.

□ Configurar Frontend.

□ Configurar SQLite.

□ Configurar SQLAlchemy.

□ Configurar Alembic.

□ Configurar FastAPI.

□ Configurar React.

□ Configurar TailwindCSS.

□ Configurar TypeScript.

□ Configurar ESLint.

□ Configurar Prettier.

□ Configurar autenticación JWT.

□ Configurar variables de entorno.

□ Crear configuración inicial.

□ Verificar que Backend y Frontend inicien correctamente.

Criterios de aprobación.

□ El proyecto compila.

□ Backend funcionando.

□ Frontend funcionando.

□ API responde correctamente.

□ Inicio de sesión disponible.

No comenzar la Fase 2 hasta cumplir todos los puntos anteriores.

---

# FASE 2

## Base de Datos

Objetivo.

Construir completamente la base de datos.

Tareas.

□ Crear modelos.

□ Crear migraciones.

□ Configurar relaciones.

□ Configurar repositorios.

□ Configurar datos iniciales.

□ Crear usuario administrador.

□ Crear configuración inicial.

□ Validar integridad.

□ Probar todas las relaciones.

Criterios de aprobación.

□ Todas las tablas creadas.

□ Relaciones funcionando.

□ Migraciones funcionando.

□ Integridad validada.

---

# FASE 3

## Gestión de Clientes

Objetivo.

Implementar completamente el módulo Clientes.

Tareas.

□ Crear cliente.

□ Editar cliente.

□ Consultar cliente.

□ Buscar por placa.

□ Buscar por nombre.

□ Buscar por cédula.

□ Consultar historial básico.

□ Consultar préstamo.

□ Consultar cronograma.

□ Validaciones.

□ Logs.

Criterios de aprobación.

□ CRUD completamente funcional.

□ Validaciones completas.

□ Sin errores.

---

# FASE 4

## Gestión de Préstamos

Objetivo.

Implementar toda la administración de préstamos.

Tareas.

□ Crear préstamo.

□ Consultar préstamo.

□ Consultar saldo.

□ Consultar estado.

□ Consultar fechas.

□ Generar cronograma.

□ Actualizar estado automáticamente.

□ Validaciones.

□ Logs.

Criterios de aprobación.

□ Toda la información financiera puede consultarse correctamente.

□ Cronograma generado automáticamente.

□ Estados funcionando correctamente.

---

# FASE 5

## Motor Financiero

Objetivo.

Implementar completamente la lógica financiera del sistema.

Esta fase constituye el núcleo del proyecto.

Tareas.

□ Registrar pagos.

□ Calcular intereses.

□ Calcular intereses por mora.

□ Calcular abono a capital.

□ Actualizar saldo.

□ Actualizar fecha del siguiente pago.

□ Actualizar estado del préstamo.

□ Registrar movimiento financiero.

□ Registrar historial.

□ Registrar logs.

□ Validaciones.

Criterios de aprobación.

□ Todos los cálculos coinciden con las reglas del negocio.

□ Los saldos permanecen consistentes.

□ No existen diferencias entre los cálculos manuales y los del sistema.

No comenzar la siguiente fase hasta validar completamente el motor financiero.

---

# FASE 6

## Facturación y Recibos

Objetivo.

Implementar completamente la generación de recibos.

Tareas.

□ Generar número consecutivo de factura.

□ Crear recibo.

□ Generar PDF.

□ Guardar PDF.

□ Mostrar vista previa.

□ Imprimir.

□ Reimprimir.

□ Almacenar recibos.

□ Validaciones.

□ Logs.

Criterios de aprobación.

□ El PDF coincide exactamente con la plantilla.

□ La vista previa coincide con el PDF.

□ La impresión funciona correctamente.

□ La reimpresión utiliza el PDF almacenado.

---

# FASE 7

## Dashboard

Objetivo.

Construir completamente el Dashboard.

Tareas.

□ Clientes activos.

□ Clientes en mora.

□ Capital pendiente.

□ Ingresos diarios.

□ Ingresos mensuales.

□ Últimos pagos.

□ Últimas facturas.

□ Estado de sincronización.

□ Último respaldo.

□ Indicadores en tiempo real.

Criterios de aprobación.

□ Todos los indicadores se actualizan automáticamente.

□ No requiere recargar la aplicación.

---

# FASE 8

## Administración de Archivos Excel

Objetivo.

Implementar completamente el módulo encargado de administrar Microsoft Excel.

Tareas.

□ Cargar archivo de clientes.

□ Cargar archivo financiero.

□ Validar estructura.

□ Crear respaldos.

□ Reemplazar archivos.

□ Restaurar versiones.

□ Registrar historial.

□ Registrar logs.

□ Mostrar estado.

Criterios de aprobación.

□ Los archivos pueden administrarse completamente desde el sistema.

□ No existen rutas fijas.

□ Todo funciona desde la interfaz.

---

# FASE 9

## Sincronización

Objetivo.

Implementar la sincronización automática entre SQLite y Microsoft Excel.

Tareas.

□ Sincronización automática.

□ Sincronización manual.

□ Validación posterior.

□ Recuperación ante errores.

□ Registro de sincronizaciones.

□ Actualización automática después de registrar pagos.

□ Validación de integridad.

□ Logs.

Criterios de aprobación.

□ SQLite y Excel contienen la misma información.

□ No se pierde información si Excel presenta errores.

□ SQLite permanece como fuente oficial.

---

# FASE 10

## Configuración

Objetivo.

Implementar completamente el módulo de configuración.

Tareas.

□ Datos de la empresa.

□ Parámetros financieros.

□ Número siguiente de factura.

□ Configuración de impresión.

□ Configuración de rutas.

□ Configuración del sistema.

□ Validaciones.

□ Logs.

Criterios de aprobación.

□ Toda la configuración puede modificarse desde la interfaz.

□ Los cambios se aplican correctamente.

□ Toda modificación queda registrada.

# FASE 11

## Gestión de Usuarios

Objetivo.

Implementar completamente la administración de usuarios.

Tareas.

□ Crear usuario.

□ Editar usuario.

□ Activar usuario.

□ Desactivar usuario.

□ Cambiar contraseña.

□ Asignar roles.

□ Validaciones.

□ Logs.

Criterios de aprobación.

□ Todos los usuarios pueden administrarse desde la interfaz.

□ Los permisos funcionan correctamente.

□ No existen accesos no autorizados.

---

# FASE 12

## Seguridad

Objetivo.

Implementar todas las políticas de seguridad definidas para el sistema.

Tareas.

□ Protección mediante JWT.

□ Validaciones Backend.

□ Protección de endpoints.

□ Protección de SQLite.

□ Protección de archivos.

□ Protección de recibos.

□ Protección de historiales.

□ Registro de incidentes.

□ Auditoría.

□ Manejo seguro de errores.

Criterios de aprobación.

□ Todas las rutas protegidas.

□ No existe acceso sin autenticación.

□ Los permisos funcionan correctamente.

---

# FASE 13

## Backups y Recuperación

Objetivo.

Implementar completamente el sistema de respaldos.

Tareas.

□ Respaldar SQLite.

□ Respaldar archivos Excel.

□ Respaldar configuración.

□ Restaurar respaldos.

□ Historial de respaldos.

□ Validaciones.

□ Logs.

Criterios de aprobación.

□ Todos los respaldos pueden restaurarse correctamente.

□ Nunca se sobrescriben respaldos existentes.

---

# FASE 14

## Reportes

Objetivo.

Implementar todos los reportes administrativos.

Tareas.

□ Reporte de clientes.

□ Reporte de pagos.

□ Reporte de ingresos.

□ Reporte de clientes en mora.

□ Reporte de facturas.

□ Reporte de movimientos.

□ Exportación.

□ Validaciones.

Criterios de aprobación.

□ Todos los reportes muestran información correcta.

□ Los filtros funcionan correctamente.

---

# FASE 15

## Optimización

Objetivo.

Optimizar completamente el sistema.

Tareas.

□ Optimizar consultas SQLite.

□ Optimizar Dashboard.

□ Optimizar búsquedas.

□ Optimizar generación de PDF.

□ Optimizar sincronización.

□ Optimizar tiempos de carga.

□ Optimizar consumo de memoria.

□ Optimizar API.

Criterios de aprobación.

□ El sistema cumple los tiempos definidos en la documentación.

---

# FASE 16

## Pruebas Finales

Objetivo.

Validar completamente el sistema antes de producción.

Tareas.

□ Ejecutar pruebas unitarias.

□ Ejecutar pruebas de integración.

□ Ejecutar pruebas funcionales.

□ Ejecutar pruebas de seguridad.

□ Ejecutar pruebas de rendimiento.

□ Corregir errores encontrados.

□ Actualizar documentación.

Criterios de aprobación.

□ Todas las pruebas son exitosas.

□ No existen errores críticos.

□ El sistema está listo para producción.

---

# FASE 17

## Preparación para Producción

Objetivo.

Preparar la versión final del software.

Tareas.

□ Revisar documentación.

□ Revisar configuración.

□ Verificar instalador.

□ Verificar estructura de carpetas.

□ Verificar migraciones.

□ Verificar respaldos.

□ Generar versión final.

□ Generar paquete de instalación.

□ Actualizar número de versión.

Criterios de aprobación.

□ El sistema puede instalarse desde cero.

□ Toda la documentación está actualizada.

□ El sistema se encuentra listo para ser utilizado por CREEMOS EN TI SAS.

---

# Reglas Durante el Desarrollo

Durante todo el proyecto OpenCode deberá respetar las siguientes reglas.

Nunca comenzar una fase sin finalizar la anterior.

Nunca dejar funcionalidades incompletas.

Nunca ignorar errores.

Nunca modificar reglas del negocio.

Nunca romper funcionalidades ya implementadas.

Siempre mantener actualizada la documentación.

Siempre ejecutar pruebas antes de continuar.

---

# Gestión de Incidencias

Si durante una fase se detecta un problema importante.

OpenCode deberá.

Detener el desarrollo.

↓

Analizar el problema.

↓

Proponer una solución.

↓

Esperar aprobación.

↓

Implementar la solución.

↓

Continuar.

Nunca implementar soluciones improvisadas.

---

# Principio Fundamental

El roadmap constituye el plan oficial de desarrollo del Sistema de Administración de Préstamos.

Todas las fases deberán completarse en el orden establecido.

La prioridad será siempre entregar módulos completamente funcionales antes de comenzar nuevos desarrollos.

---

# Declaración Final

Este documento define oficialmente el orden de desarrollo del Sistema de Administración de Préstamos de CREEMOS EN TI SAS.

OpenCode deberá seguir este roadmap durante todo el proyecto, garantizando un desarrollo ordenado, incremental y estable.

---

**Fin del documento.**