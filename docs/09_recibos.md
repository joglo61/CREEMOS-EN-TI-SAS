# RECIBOS
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento define todas las reglas relacionadas con la generación, almacenamiento, impresión y reimpresión de los recibos emitidos por el sistema.

El recibo constituye el comprobante oficial de cada pago registrado.

Todo pago deberá generar automáticamente un recibo.

No existirá la posibilidad de registrar un pago sin generar su respectivo recibo.

---

# Filosofía

El recibo deberá reemplazar completamente el formato físico utilizado actualmente por la empresa.

El operador nunca deberá escribir un recibo manualmente.

Toda la información será diligenciada automáticamente por el sistema.

El objetivo es mantener el mismo formato tradicional, pero eliminando el trabajo manual.

---

# Generación

El recibo será generado inmediatamente después de registrar un pago.

El proceso será completamente automático.

Registrar pago.

↓

Actualizar SQLite.

↓

Actualizar Excel.

↓

Generar PDF.

↓

Guardar PDF.

↓

Abrir vista previa.

↓

Enviar a impresión.

---

# Número de Factura

Cada recibo deberá contener un número de factura único.

Características.

• Consecutivo.

• Automático.

• Nunca repetido.

• Nunca editable.

El número de factura será administrado exclusivamente por el sistema.

---

# Fecha

Cada recibo mostrará dos fechas.

Fecha correspondiente a la cuota que está siendo cancelada.

Fecha real en la que el cliente realizó el pago.

Ambas fechas deberán visualizarse claramente.

Formato.

DD/MM/AAAA

---

# Información del Cliente

El recibo deberá mostrar.

Nombre completo.

Placa.

Número de factura.

Fecha.

Valor de la cuota.

Toda esta información será obtenida automáticamente desde SQLite.

Nunca será digitada manualmente.

---

# Información Financiera

El recibo mostrará únicamente los valores finales.

Saldo anterior.

Intereses.

Capital.

Valor recibido.

Nuevo saldo.

No deberá mostrar cálculos internos.

No deberá mostrar intereses normales separados de intereses por mora.

El campo.

INTERESES.

Corresponderá a.

Intereses normales + intereses de mora.

---

# Observaciones

Cada recibo deberá incluir un espacio completamente vacío.

Este espacio permitirá realizar anotaciones manuales.

El sistema nunca escribirá automáticamente dentro de esta sección.

El espacio deberá tener aproximadamente dos líneas disponibles.

---

# Firma

Cada recibo deberá finalizar con una única línea destinada para la firma.

Debajo únicamente aparecerá el texto.

Firma

No deberán utilizarse textos como.

Firma del cliente.

Recibido por.

Responsable.

---

# Cantidad de Copias

Cada impresión contendrá exactamente dos recibos.

Recibo superior.

COPIA CLIENTE.

Recibo inferior.

COPIA CONTABILIDAD.

Ambos deberán ser completamente idénticos.

La única diferencia será el texto que identifica la copia.

---

# Impresión

Los dos recibos deberán imprimirse en una única hoja.

Nunca deberán dividirse entre páginas.

La impresión deberá estar optimizada para papel tamaño carta.

No deberá requerirse configuración adicional por parte del usuario.

---

# Almacenamiento

Cada recibo generado deberá almacenarse automáticamente.

No deberá eliminarse.

No deberá sobrescribirse.

Cada PDF quedará asociado a la factura correspondiente.

Esto permitirá reimprimir cualquier recibo en el futuro.

---

# Reimpresión

Cuando un usuario solicite reimprimir un recibo.

El sistema nunca recalculará intereses.

Nunca recalculará capital.

Nunca recalculará mora.

Nunca modificará el saldo.

Simplemente recuperará el PDF asociado a la factura y lo enviará nuevamente a impresión.

Esto garantiza que el documento reimpreso sea idéntico al original.

---

# Formato Monetario

Todos los valores deberán mostrarse utilizando formato colombiano.

Ejemplos.

$ 850.000

$ 1.250.000

$ 15.800.000

No mostrar decimales.

Utilizar separador de miles.

---

# Responsabilidad del Módulo

El módulo de recibos únicamente será responsable de.

Construir el PDF.

Guardar el archivo.

Abrir la vista previa.

Enviar a impresión.

Permitir reimpresión.

Nunca realizará cálculos financieros.

Nunca consultará directamente el archivo Excel.

Toda la información será suministrada por el módulo de pagos.

# Estructura del Recibo

Cada recibo deberá estar compuesto por las siguientes secciones.

1.

Encabezado.

2.

Información del cliente.

3.

Información financiera.

4.

Observaciones.

5.

Firma.

La distribución deberá mantenerse exactamente igual en todos los recibos generados.

---

# Encabezado

El encabezado contendrá.

Nombre de la empresa.

Dirección.

Teléfono.

Ciudad.

Número de factura.

Fecha de emisión.

Fecha correspondiente a la cuota.

El número de factura deberá ubicarse en la parte superior derecha.

La información de la empresa deberá ubicarse en la parte superior izquierda.

---

# Información del Cliente

Debajo del encabezado aparecerán los siguientes campos.

Recibí de.

Nombre del cliente.

Placa.

Valor de la cuota.

Estado del préstamo.

Toda esta información será llenada automáticamente.

---

# Información Financiera

La información financiera deberá organizarse mediante una tabla sencilla.

La tabla tendrá dos columnas.

Concepto.

Valor.

Las filas serán.

Saldo anterior.

Intereses.

Capital.

Valor recibido.

Nuevo saldo.

Todos los valores monetarios deberán alinearse a la derecha.

Los conceptos deberán alinearse a la izquierda.

---

# Intereses

Aunque internamente el sistema calculará.

Intereses normales.

Intereses por mora.

El recibo únicamente mostrará.

Intereses.

El valor corresponderá a la suma de ambos conceptos.

Esto mantiene la forma de trabajo actual de la empresa.

---

# Observaciones

Debajo de la tabla financiera.

Existirá un espacio completamente libre.

Este espacio permitirá escribir observaciones manuales.

El sistema nunca imprimirá texto en esta zona.

El espacio deberá permitir al menos dos líneas escritas a mano.

---

# Firma

La parte inferior del recibo contendrá.

Una línea horizontal.

Debajo.

Firma

No deberá incluir nombres.

No deberá incluir cargos.

No deberá incluir otros textos.

---

# Vista Previa

Antes de imprimir.

El sistema mostrará exactamente el mismo documento que será enviado a la impresora.

La vista previa deberá utilizar el mismo diseño.

Las mismas posiciones.

Las mismas fuentes.

Los mismos márgenes.

No deberá existir ninguna diferencia entre la vista previa y el PDF final.

---

# Almacenamiento de PDFs

Todos los recibos deberán almacenarse automáticamente.

La estructura sugerida será.

recibos/

2026/

07/

Factura_000001.pdf

Factura_000002.pdf

Factura_000003.pdf

El nombre del archivo deberá utilizar el número de factura.

Nunca deberá sobrescribirse un archivo existente.

---

# Consulta de Recibos

El sistema permitirá consultar recibos utilizando.

Número de factura.

Nombre del cliente.

Placa.

Fecha.

Usuario.

Desde cualquier recibo será posible.

Visualizar.

Reimprimir.

Descargar.

---

# Seguridad

Los recibos no podrán modificarse después de haber sido generados.

Si posteriormente cambia.

El saldo.

La tasa.

La configuración.

La información del cliente.

El PDF permanecerá exactamente igual.

Los recibos representan evidencia histórica.

Nunca deberán alterarse.

---

# Errores

Si durante la generación ocurre un error.

El sistema deberá.

Registrar el incidente.

Mostrar un mensaje claro.

Conservar la información del pago.

Permitir generar nuevamente el PDF.

Nunca deberá perderse un pago porque falle la generación del recibo.

---

# Rendimiento

La generación del PDF deberá realizarse en menos de tres segundos.

La apertura de la vista previa deberá ser inmediata.

La reimpresión deberá recuperar directamente el PDF almacenado.

Nunca deberá reconstruir el documento.

---

# Compatibilidad

Los recibos deberán poder imprimirse correctamente en.

Impresoras láser.

Impresoras de inyección.

Impresoras térmicas tamaño carta (si en el futuro se implementan).

Los márgenes deberán garantizar una impresión correcta sin cortes.

# Diseño de Impresión

El diseño del recibo deberá priorizar la impresión sobre la visualización en pantalla.

Todo el contenido deberá estar perfectamente alineado.

No deberán existir elementos decorativos.

No deberán utilizarse fondos de color.

No deberán utilizarse degradados.

Todo el documento deberá imprimirse utilizando tinta negra.

---

# Márgenes

Los márgenes deberán ser pequeños para aprovechar el área imprimible de la hoja.

Margen superior.

15 mm.

Margen inferior.

15 mm.

Margen izquierdo.

15 mm.

Margen derecho.

15 mm.

La distribución deberá mantenerse uniforme.

---

# Fuente

Se utilizarán fuentes estándar disponibles en cualquier sistema.

Preferiblemente.

Helvetica.

Arial.

Liberation Sans.

No utilizar fuentes decorativas.

---

# Tamaños de Fuente

Nombre de la empresa.

14 pt.

Encabezados.

11 pt.

Contenido.

10 pt.

Valores monetarios.

10 pt.

Observaciones.

10 pt.

Firma.

10 pt.

Todos los tamaños deberán mantenerse consistentes.

---

# Líneas

El recibo utilizará líneas horizontales para separar la información.

No utilizar cuadros complejos.

No utilizar tablas con colores.

No utilizar bordes gruesos.

El objetivo es obtener un documento limpio y fácil de imprimir.

---

# Distribución de la Hoja

Una hoja tamaño carta contendrá exactamente dos recibos.

------------------------------------------------------

COPIA CLIENTE

------------------------------------------------------

(Separación)

------------------------------------------------------

COPIA CONTABILIDAD

------------------------------------------------------

Ambos recibos deberán ocupar aproximadamente el mismo espacio.

La separación deberá permitir un corte sencillo si la empresa decide hacerlo.

---

# Identificación de las Copias

Cada recibo deberá mostrar claramente.

COPIA CLIENTE

o

COPIA CONTABILIDAD

Este texto deberá ubicarse debajo del encabezado.

No deberá afectar el resto del diseño.

---

# Espacio para Observaciones

El espacio destinado a observaciones deberá permanecer completamente vacío.

No deberá contener líneas de texto predeterminadas.

No deberá contener mensajes automáticos.

Será utilizado exclusivamente por el personal de la empresa cuando sea necesario.

---

# Firma

La línea de firma deberá ubicarse en la parte inferior derecha del recibo.

Debajo únicamente aparecerá.

Firma

No agregar otros textos.

---

# Nombre del Archivo PDF

Cada archivo PDF generado utilizará la siguiente estructura.

Factura_000001.pdf

Factura_000002.pdf

Factura_000003.pdf

El número corresponderá exactamente al número de factura registrado en la base de datos.

---

# Organización de los Archivos

Todos los PDFs deberán organizarse automáticamente por año y mes.

Ejemplo.

recibos/

2026/

01/

Factura_000001.pdf

Factura_000002.pdf

02/

Factura_000085.pdf

Factura_000086.pdf

Esto facilitará la organización de los documentos.

---

# Recuperación de Recibos

Cuando un usuario consulte una factura.

El sistema deberá localizar inmediatamente el PDF correspondiente.

Nunca deberá reconstruir el documento.

Siempre utilizará el archivo almacenado.

---

# Auditoría

Cada generación de un recibo deberá registrar.

Usuario.

Fecha.

Hora.

Número de factura.

Cliente.

Resultado.

Cada reimpresión también deberá registrarse.

Esto permitirá conocer cuántas veces fue reimpreso un documento.

---

# Errores de Impresión

Si la impresora presenta un problema.

El sistema conservará el PDF generado.

El usuario podrá intentar imprimir nuevamente sin registrar un nuevo pago.

Nunca generar una nueva factura por un problema de impresión.

---

# Escalabilidad

El diseño deberá permitir incorporar en el futuro.

Código QR.

Código de barras.

Firma digital.

Facturación electrónica.

Logotipos adicionales.

Mensajes personalizados.

Sin necesidad de rediseñar completamente el formato.

---

# Principio Fundamental

El recibo constituye el comprobante oficial del pago realizado por el cliente.

Por esta razón.

Debe ser claro.

Legible.

Consistente.

Fácil de imprimir.

Fácil de archivar.

Y permanecer inalterable durante toda la vida útil del préstamo.

---

# Declaración Final

Este documento define oficialmente las reglas relacionadas con la generación, almacenamiento, impresión y reimpresión de los recibos del Sistema de Administración de Préstamos de CREEMOS EN TI SAS.

Toda implementación deberá respetar estrictamente estas especificaciones.

---

**Fin del documento.**