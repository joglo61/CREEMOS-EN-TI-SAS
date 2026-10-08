# VISIÓN DEL NEGOCIO
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Introducción

Este documento tiene como objetivo explicar completamente el funcionamiento del negocio de CREEMOS EN TI SAS.

Antes de desarrollar cualquier componente del software, todo desarrollador o agente de inteligencia artificial deberá comprender este documento en su totalidad.

La tecnología deberá adaptarse al negocio.

El negocio nunca deberá adaptarse a la tecnología.

Todas las decisiones técnicas deberán respetar la forma en que actualmente opera la empresa.

---

# Descripción de la Empresa

CREEMOS EN TI SAS es una empresa dedicada al financiamiento para la compra de vehículos tipo taxi.

La empresa otorga préstamos de dinero a personas interesadas en adquirir un taxi.

Posteriormente realiza el seguimiento de cada préstamo mediante el cobro periódico de cuotas, intereses y abonos a capital.

Actualmente toda la operación administrativa se realiza utilizando archivos Microsoft Excel y recibos físicos diligenciados manualmente.

El crecimiento de la empresa hace necesario automatizar completamente este proceso sin modificar la metodología de trabajo utilizada por el personal administrativo.

---

# Problema Actual

Actualmente existen varios procesos manuales que consumen una gran cantidad de tiempo y aumentan el riesgo de errores humanos.

Entre ellos:

• Búsqueda manual de clientes.

• Consulta manual del saldo.

• Cálculo manual de intereses.

• Cálculo manual de intereses por mora.

• Actualización manual del saldo.

• Actualización manual del archivo Excel.

• Escritura manual de los recibos.

• Administración manual del consecutivo de facturas.

Todo esto provoca retrasos durante la atención al cliente y aumenta la probabilidad de errores financieros.

---

# Objetivo del Sistema

El objetivo del sistema es reemplazar completamente estas tareas manuales por procesos automáticos.

El sistema deberá encargarse de todos los cálculos financieros.

El operador únicamente deberá ingresar la información estrictamente necesaria.

Toda la lógica del negocio será responsabilidad del software.

---

# Filosofía del Proyecto

El propósito del proyecto NO es cambiar la forma en que trabaja la empresa.

El propósito es automatizar la forma en que actualmente trabaja.

Cuando el sistema entre en funcionamiento, el personal administrativo deberá sentir que continúa realizando exactamente el mismo proceso, pero de forma automática.

Por esta razón:

No deberán modificarse las reglas financieras.

No deberán modificarse los procesos administrativos.

No deberán modificarse las fórmulas actualmente utilizadas.

La única diferencia será que ahora todo será realizado por el sistema.

---

# Público Objetivo

El sistema será utilizado por:

• Administradores.

• Auxiliares administrativos.

• Personal encargado de registrar pagos.

Los usuarios no necesariamente tendrán conocimientos técnicos.

Por esta razón la aplicación deberá ser extremadamente sencilla.

---

# Forma de Trabajo

La empresa trabaja mediante préstamos individuales.

Cada cliente posee un préstamo asociado.

Cada préstamo tiene:

• Un capital inicial.

• Un saldo pendiente.

• Una cuota periódica.

• Una tasa de interés.

Cada vez que un cliente realiza un pago, el sistema deberá recalcular automáticamente el estado del préstamo.

---

# Forma Actual de Trabajo

Actualmente el procedimiento es el siguiente.

1.

El cliente llega a la oficina.

2.

Se busca manualmente la información del cliente.

3.

Se consulta el archivo Excel.

4.

Se calcula manualmente el interés.

5.

Se calcula manualmente la mora.

6.

Se calcula el abono a capital.

7.

Se calcula el nuevo saldo.

8.

Se llena un recibo manualmente.

9.

Se actualiza nuevamente el archivo Excel.

Todo este proceso será reemplazado por una única operación realizada desde el sistema.

---

# Forma de Trabajo Esperada

Con el nuevo sistema el procedimiento será el siguiente.

El cliente llega.

↓

Buscar cliente.

↓

Seleccionar cliente.

↓

Ingresar valor recibido.

↓

El sistema calcula automáticamente:

• Intereses.

• Mora.

• Capital.

• Nuevo saldo.

↓

Vista previa del recibo.

↓

Confirmar.

↓

Actualizar SQLite.

↓

Actualizar Excel.

↓

Guardar historial.

↓

Generar PDF.

↓

Imprimir.

↓

Proceso finalizado.

---

# Principios del Sistema

Durante todo el desarrollo deberán respetarse los siguientes principios.

• Automatizar.

• Simplificar.

• Reducir errores.

• Reducir tiempos.

• Mantener la forma de trabajo actual.

• Facilitar el crecimiento futuro.

---

# Automatización

El operador nunca deberá realizar cálculos manuales.

El operador únicamente deberá ingresar:

• Cliente.

• Valor recibido.

Todo lo demás será calculado automáticamente por el sistema.

---

# Experiencia del Usuario

El sistema deberá ser rápido.

El registro de un pago completo deberá realizarse en menos de un minuto.

La interfaz deberá requerir la menor cantidad posible de clics.

La información deberá aparecer automáticamente sin necesidad de múltiples búsquedas.

---

# Objetivo Final

El objetivo de CREEMOS EN TI SAS es abandonar completamente el proceso manual actual y administrar toda la cartera de préstamos mediante un único sistema centralizado, confiable y preparado para crecer durante muchos años.

Este documento constituye la base conceptual del proyecto y deberá ser respetado durante todo el desarrollo.

# Visión a Largo Plazo

El sistema deberá convertirse en la herramienta principal de administración de la empresa.

Todas las operaciones relacionadas con los préstamos deberán realizarse desde esta plataforma.

El objetivo es eliminar completamente la dependencia de procesos manuales sin eliminar el uso de Microsoft Excel, ya que este hace parte del flujo de trabajo de la empresa.

SQLite será la fuente oficial de información.

Microsoft Excel será un archivo sincronizado automáticamente para mantener la compatibilidad con el proceso actual de trabajo.

---

# Administración de Clientes

Cada cliente representará una obligación financiera.

Cada cliente tendrá asociado un préstamo activo.

Inicialmente el sistema administrará un único préstamo por cliente.

Sin embargo, toda la arquitectura deberá quedar preparada para soportar múltiples préstamos en futuras versiones.

Cada cliente tendrá como información mínima:

• Nombre completo.

• Número de identificación.

• Placa del vehículo.

• Teléfono.

• Dirección.

• Valor del préstamo.

• Valor de la cuota.

• Fecha de inicio.

• Fecha del primer pago.

• Fecha del próximo pago.

• Saldo pendiente.

• Estado.

---

# Administración de Préstamos

El préstamo será el elemento financiero principal del sistema.

Cada préstamo deberá conservar toda su historia desde el momento de su creación hasta su cancelación.

Nunca deberá eliminarse un préstamo.

En caso de finalizar completamente una deuda, simplemente cambiará su estado a:

Finalizado.

Toda la información histórica deberá conservarse permanentemente.

---

# Administración de Pagos

Cada pago registrado representa un movimiento financiero.

Los pagos nunca podrán eliminarse.

Los pagos nunca podrán modificarse.

Toda corrección deberá realizarse mediante nuevos movimientos definidos por la empresa en futuras versiones.

El historial financiero deberá permanecer intacto.

---

# Administración de Facturas

Cada pago generará automáticamente una factura.

Cada factura tendrá un número consecutivo único.

Nunca podrán existir dos facturas con el mismo número.

El consecutivo será administrado automáticamente por el sistema.

Cada factura deberá almacenarse permanentemente.

Cada factura tendrá asociado un archivo PDF.

Ese PDF podrá imprimirse nuevamente en cualquier momento.

---

# Historial

Toda operación realizada deberá conservarse.

El historial permitirá conocer exactamente:

• Cuándo se realizó un pago.

• Quién realizó el pago.

• Qué factura fue generada.

• Cuánto dinero ingresó.

• Cuánto correspondió a intereses.

• Cuánto correspondió a capital.

• Cuál era el saldo antes del pago.

• Cuál quedó siendo el saldo después del pago.

La empresa nunca perderá la trazabilidad de sus operaciones.

---

# Dashboard

El sistema contará con un panel principal.

Este panel deberá mostrar información relevante para la administración diaria.

Como mínimo deberá mostrar:

Clientes activos.

Clientes en mora.

Capital pendiente.

Ingresos del día.

Cantidad de pagos realizados.

Últimos pagos registrados.

El Dashboard deberá actualizarse automáticamente conforme se registren nuevos pagos.

---

# Administración de Archivos

El sistema no dependerá de archivos con nombres específicos.

El administrador podrá cargar los archivos necesarios desde una pantalla dedicada.

Existirán dos archivos principales.

Archivo de clientes.

Archivo utilizado actualmente por la empresa para realizar cálculos financieros.

Estos archivos podrán reemplazarse cuando sea necesario.

Antes de aceptar un archivo nuevo el sistema deberá validar:

• Que sea un archivo Excel.

• Que la estructura sea correcta.

• Que contenga las hojas requeridas.

• Que las columnas obligatorias existan.

Si alguna validación falla.

El sistema rechazará el archivo y mostrará un mensaje indicando el problema.

---

# Sincronización

Después de cada operación financiera exitosa.

El sistema deberá:

Actualizar SQLite.

↓

Actualizar el archivo Excel correspondiente.

↓

Guardar una copia de seguridad.

↓

Registrar la fecha de sincronización.

Si la sincronización falla.

La información almacenada en SQLite nunca deberá perderse.

El sistema deberá registrar el error y permitir reintentar la sincronización posteriormente.

---

# Generación de Recibos

Cada pago registrado generará automáticamente un recibo.

El recibo deberá estar listo para impresión inmediatamente.

El usuario no deberá llenar manualmente ningún dato.

Toda la información será tomada automáticamente desde la base de datos.

Cada impresión contendrá dos copias.

Una para el cliente.

Una para la contabilidad.

Ambas deberán imprimirse en una única hoja.

---

# Escalabilidad del Negocio

La empresa espera continuar creciendo.

Por esta razón el sistema deberá estar preparado para incorporar nuevas funcionalidades.

Entre ellas:

Múltiples préstamos por cliente.

Nuevos tipos de créditos.

Nuevas tasas.

Facturación electrónica.

Portal para clientes.

Aplicación móvil.

Integración con servicios externos.

Sin necesidad de modificar completamente la arquitectura existente.

---

# Principio General

Cada decisión tomada durante el desarrollo deberá responder una única pregunta.

¿Esta solución facilita el trabajo diario de CREEMOS EN TI SAS?

Si la respuesta es no.

La solución deberá replantearse.

El sistema existe para apoyar la operación de la empresa y no para obligarla a cambiar su forma de trabajar.

# Beneficios Esperados

La implementación del sistema deberá generar beneficios tanto operativos como administrativos.

## Beneficios Operativos

• Disminución significativa del tiempo de atención al cliente.

• Eliminación de cálculos manuales.

• Eliminación de errores en operaciones matemáticas.

• Eliminación del diligenciamiento manual de recibos.

• Reducción del tiempo requerido para consultar información.

• Acceso inmediato al historial de cada cliente.

---

## Beneficios Administrativos

La administración de la empresa contará con información actualizada en tiempo real.

Será posible conocer inmediatamente:

- Capital pendiente.
- Número de clientes activos.
- Clientes en mora.
- Ingresos diarios.
- Historial de recaudo.
- Estado de cada préstamo.

---

# Flujo Diario de Trabajo

El sistema ha sido diseñado para utilizarse durante toda la jornada laboral.

Un día normal de operación será el siguiente.

Inicio de sesión.

↓

Consulta del Dashboard.

↓

Llegada del cliente.

↓

Búsqueda por placa.

↓

Consulta automática de la información.

↓

Registro del pago.

↓

Generación automática del recibo.

↓

Actualización automática del saldo.

↓

Actualización automática del archivo Excel.

↓

Registro del movimiento en el historial.

↓

Atención del siguiente cliente.

Todo este proceso deberá realizarse de manera continua durante el día.

---

# Dependencia de los Archivos Excel

Actualmente la empresa utiliza archivos Microsoft Excel para controlar la cartera.

El nuevo sistema continuará siendo compatible con dichos archivos.

Sin embargo.

Los archivos Excel dejarán de ser la fuente principal de información.

Serán utilizados únicamente como:

• Medio de compatibilidad.

• Respaldo operativo.

• Consulta externa.

Toda la lógica financiera dependerá exclusivamente de SQLite.

---

# Filosofía de Automatización

El sistema deberá minimizar la cantidad de decisiones que toma el operador.

Siempre que una información pueda calcularse automáticamente.

El sistema deberá hacerlo.

Nunca solicitar datos que ya existan en la base de datos.

Nunca solicitar datos que puedan calcularse automáticamente.

Nunca solicitar al usuario repetir información existente.

---

# Integridad de la Información

La información financiera representa el activo más importante del sistema.

Por esta razón.

Toda modificación deberá garantizar:

Consistencia.

Integridad.

Trazabilidad.

Seguridad.

Disponibilidad.

Cada operación deberá quedar registrada.

Cada modificación deberá ser identificable.

Cada pago deberá poder reconstruirse históricamente.

---

# Evolución del Sistema

El sistema deberá evolucionar de manera gradual.

Las nuevas funcionalidades deberán agregarse sin afectar el funcionamiento existente.

No deberán realizarse modificaciones que obliguen a cambiar la metodología de trabajo de la empresa.

Cada nueva versión deberá conservar la compatibilidad con la información ya registrada.

---

# Preparación para el Futuro

Aunque la primera versión estará enfocada exclusivamente en la administración de préstamos para compra de taxis.

La arquitectura deberá permitir ampliar el sistema para administrar otros productos financieros.

Esto significa que el diseño no deberá limitar el crecimiento del negocio.

---

# Criterios para la Toma de Decisiones

Cuando durante el desarrollo existan varias alternativas técnicas.

Siempre deberá seleccionarse aquella que:

Sea más estable.

Sea más fácil de mantener.

Sea más sencilla de comprender.

Genere menor riesgo para la operación diaria.

Facilite futuras ampliaciones.

La simplicidad tendrá prioridad sobre la complejidad.

---

# Papel de OpenCode

OpenCode participará como desarrollador principal del proyecto.

Antes de implementar cualquier funcionalidad deberá comprender completamente:

La visión del negocio.

Las reglas financieras.

La arquitectura.

La base de datos.

Los casos de uso.

Las funcionalidades.

La API.

La sincronización con Excel.

El diseño de los recibos.

Nunca deberá asumir reglas de negocio que no estén documentadas.

Si identifica ambigüedades o inconsistencias.

Deberá detener el desarrollo de esa funcionalidad y solicitar una aclaración.

---

# Declaración Final

Este documento representa la visión oficial del negocio para el Sistema de Administración de Préstamos de CREEMOS EN TI SAS.

Todas las decisiones funcionales y técnicas deberán alinearse con esta visión.

El propósito del proyecto es construir una herramienta confiable, robusta y preparada para acompañar el crecimiento de la empresa durante muchos años, manteniendo siempre la simplicidad de uso, la estabilidad del sistema y la fidelidad al proceso de negocio actual.

---

**Fin del documento.**