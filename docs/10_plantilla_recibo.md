# PLANTILLA DEL RECIBO
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento define el diseño exacto que deberá utilizar el sistema para generar los recibos en formato PDF.

La finalidad es reproducir un recibo tradicional utilizado por entidades financieras, conservando un aspecto serio, sencillo y optimizado para impresión.

El diseño deberá ser idéntico tanto en la vista previa como en el documento PDF final.

---

# Filosofía del Diseño

El recibo NO deberá parecer una factura electrónica.

El recibo NO deberá parecer un documento moderno.

El recibo NO deberá utilizar:

• Sombras.

• Tarjetas.

• Bordes redondeados.

• Gradientes.

• Fondos de colores.

• Iconos decorativos.

El recibo deberá parecer un formulario físico diligenciado automáticamente.

---

# Tamaño del Documento

Formato.

Carta.

Medidas.

8.5 x 11 pulgadas.

Orientación.

Vertical.

---

# Distribución General

Cada hoja contendrá exactamente dos recibos.

-----------------------------------------

RECIBO SUPERIOR

(Copia Cliente)

-----------------------------------------

Línea de separación

-----------------------------------------

RECIBO INFERIOR

(Copia Contabilidad)

-----------------------------------------

Ambos recibos deberán ser completamente iguales.

Únicamente cambiará el texto identificando la copia.

---

# Distribución Vertical

Cada recibo ocupará aproximadamente la mitad de la hoja.

La separación entre ambos recibos será de aproximadamente 15 mm.

Esta separación facilitará un eventual corte manual.

---

# Márgenes

Margen superior.

15 mm.

Margen inferior.

15 mm.

Margen izquierdo.

15 mm.

Margen derecho.

15 mm.

---

# Encabezado

El encabezado ocupará toda la parte superior del recibo.

Lado izquierdo.

Nombre de la empresa.

Dirección.

Teléfono.

Ciudad.

Lado derecho.

Factura No.

Fecha del pago.

Fecha correspondiente a la cuota.

Todo deberá estar alineado horizontalmente.

---

# Nombre de la Empresa

El nombre de la empresa será el elemento visual más importante.

Se imprimirá utilizando.

Fuente.

Helvetica Bold.

Tamaño.

14 pt.

Alineación.

Centro.

---

# Información del Cliente

Debajo del encabezado aparecerán los siguientes campos.

Recibí de:

Nombre del cliente.

Placa:

Valor de la cuota:

Estado:

Todos estos datos serán obtenidos automáticamente desde SQLite.

Nunca serán digitados manualmente.

---

# Tabla Financiera

Debajo de la información del cliente.

Se mostrará una tabla sencilla.

Dos columnas.

Concepto.

Valor.

Filas.

Saldo anterior.

Intereses.

Capital.

Valor recibido.

Nuevo saldo.

Todos los valores deberán alinearse a la derecha.

Todos los conceptos deberán alinearse a la izquierda.

---

# Campo Intereses

Aunque internamente el sistema calcule.

Intereses normales.

Intereses por mora.

El recibo mostrará únicamente.

INTERESES

El valor corresponderá a la suma de ambos conceptos.

Nunca deberán mostrarse por separado.

---

# Valores Monetarios

Todos los valores utilizarán formato colombiano.

Ejemplos.

$ 850.000

$ 1.200.000

$ 25.450.000

Nunca mostrar decimales.

Siempre utilizar separadores de miles.

---

# Observaciones

Después de la tabla financiera existirá un espacio completamente libre.

Altura aproximada.

30 mm.

El sistema nunca escribirá automáticamente en este espacio.

Será utilizado manualmente por la empresa cuando sea necesario.

---

# Espacio para Firma

En la parte inferior del recibo deberá existir una única línea horizontal.

Debajo de la línea únicamente aparecerá el texto.

Firma

No agregar.

Firma del cliente.

Recibido por.

Autorizado por.

Responsable.

Únicamente.

Firma

---

# Identificación de la Copia

Cada recibo deberá indicar claramente si corresponde a.

COPIA CLIENTE

o

COPIA CONTABILIDAD

Este texto deberá ubicarse debajo del encabezado.

Fuente.

Helvetica Bold.

Tamaño.

10 pt.

Alineación.

Centro.

---

# Líneas Separadoras

El recibo utilizará únicamente líneas horizontales.

No utilizar cuadros completos.

No utilizar tablas con bordes gruesos.

No utilizar elementos decorativos.

La prioridad será la facilidad de impresión.

---

# Distribución Aproximada

Cada recibo tendrá la siguiente organización.

-----------------------------------------------------

Empresa

Factura

Fecha

-----------------------------------------------------

Recibí de:

Cliente

Placa

Valor Cuota

Estado

-----------------------------------------------------

Saldo anterior

Intereses

Capital

Valor recibido

Nuevo saldo

-----------------------------------------------------

Observaciones

(espacio completamente vacío)

-----------------------------------------------------

Firma

-----------------------------------------------------

Todo deberá mantenerse perfectamente alineado.

---

# Espaciado

Entre encabezado e información del cliente.

10 mm.

Entre cliente y tabla.

8 mm.

Entre filas de la tabla.

6 mm.

Entre tabla y observaciones.

8 mm.

Entre observaciones y firma.

12 mm.

---

# Fuentes

Título empresa.

Helvetica Bold.

14 pt.

Encabezados.

Helvetica Bold.

10 pt.

Contenido.

Helvetica.

10 pt.

Valores.

Helvetica.

10 pt.

Texto copia.

Helvetica Bold.

10 pt.

Firma.

Helvetica.

10 pt.

---

# Alineación

Todos los conceptos.

Izquierda.

Todos los valores.

Derecha.

Título.

Centro.

Empresa.

Centro.

Observaciones.

Izquierda.

Firma.

Centro.

---

# Vista Previa

La vista previa mostrada por el sistema deberá ser exactamente igual al PDF.

No podrá existir ninguna diferencia entre.

Posiciones.

Márgenes.

Fuentes.

Espaciados.

Líneas.

El usuario deberá visualizar exactamente el documento que será impreso.

---

# Impresión

Al presionar.

Guardar e Imprimir.

El sistema realizará automáticamente.

Guardar SQLite.

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

El usuario no deberá descargar manualmente el archivo.

---

# Nombre del Archivo

Todos los PDFs deberán utilizar la siguiente nomenclatura.

Factura_000001.pdf

Factura_000002.pdf

Factura_000003.pdf

El número corresponderá exactamente al número de factura.

---

# Organización

Los archivos PDF deberán almacenarse automáticamente.

recibos/

AAAA/

MM/

Factura_000001.pdf

Factura_000002.pdf

Factura_000003.pdf

Esto permitirá localizar rápidamente cualquier documento.

---

# Reimpresión

Cuando un usuario solicite reimprimir una factura.

El sistema deberá.

Buscar el PDF.

↓

Abrir el PDF.

↓

Enviar a impresión.

Nunca deberá reconstruir el documento.

Nunca recalcular información.

---

# Escalabilidad

La plantilla deberá diseñarse para permitir agregar posteriormente.

Código QR.

Código de barras.

Firma digital.

Logotipo adicional.

Información tributaria.

Mensajes personalizados.

Sin modificar la distribución principal del documento.

---

# Compatibilidad

El diseño deberá imprimirse correctamente utilizando.

ReportLab.

Impresoras láser.

Impresoras de inyección.

Papel tamaño carta.

Sin necesidad de realizar ajustes manuales.

---

# Principio Fundamental

La plantilla deberá conservar el aspecto de un recibo financiero tradicional.

La prioridad será.

Legibilidad.

Rapidez de impresión.

Simplicidad.

Consistencia.

Facilidad de archivo.

El usuario deberá sentir que el sistema está diligenciando automáticamente un recibo físico tradicional y no generando una factura electrónica.

# Reglas de Impresión

La generación del recibo deberá priorizar siempre la impresión física.

El documento deberá aprovechar correctamente toda el área imprimible de una hoja tamaño carta.

No deberán existir espacios desperdiciados.

No deberán existir elementos decorativos.

Todo el diseño deberá mantenerse limpio y profesional.

---

# Colores

Toda la impresión será monocromática.

Color.

Negro.

No utilizar.

Azul.

Rojo.

Verde.

Fondos grises.

Gradientes.

El recibo deberá poder imprimirse perfectamente incluso en impresoras básicas.

---

# Líneas

Todas las líneas utilizadas serán de grosor fino.

Las líneas servirán únicamente para organizar visualmente la información.

No deberán utilizarse bordes gruesos.

No deberán utilizarse cajas innecesarias.

---

# Ajuste Automático

Si algún dato supera el espacio disponible.

El sistema deberá.

Reducir ligeramente el tamaño de la fuente.

o

Ajustar automáticamente el texto.

Nunca cortar información.

Nunca permitir que un texto salga del área imprimible.

---

# Manejo de Nombres Largos

Si el nombre del cliente es muy largo.

El sistema deberá extender el campo automáticamente.

Sin alterar la posición del resto de la información.

La tabla financiera nunca deberá desplazarse.

---

# Manejo de Valores Grandes

Si el valor monetario contiene muchos dígitos.

Deberá mantenerse alineado a la derecha.

Nunca deberá invadir la columna de conceptos.

---

# Calidad del PDF

El PDF deberá generarse con calidad suficiente para impresión.

Todo el texto deberá permanecer nítido.

No utilizar imágenes rasterizadas para construir el recibo.

Todo el documento deberá generarse mediante texto vectorial.

---

# Configuración de Impresión

El sistema deberá abrir automáticamente el cuadro de impresión del sistema operativo.

No deberá requerir que el usuario descargue el PDF.

No deberá requerir buscar el archivo manualmente.

El flujo esperado será.

Guardar.

↓

Vista previa.

↓

Imprimir.

↓

Cerrar.

↓

Regresar automáticamente al sistema.

---

# Recuperación del Archivo

Todos los recibos deberán poder recuperarse utilizando cualquiera de los siguientes criterios.

Número de factura.

Nombre del cliente.

Placa.

Fecha.

Usuario.

Estado.

La búsqueda deberá ser inmediata.

---

# Conservación

Los recibos nunca deberán eliminarse automáticamente.

Nunca deberán sobrescribirse.

Nunca deberán regenerarse si ya existen.

El PDF generado el día del pago será el documento oficial durante toda la vida útil del préstamo.

---

# Auditoría

Cada generación de un recibo deberá registrar.

Número de factura.

Fecha.

Hora.

Usuario.

Cliente.

Ruta del PDF.

Resultado.

Cada reimpresión deberá registrar.

Fecha.

Hora.

Usuario.

Número de factura.

Motivo (si se proporciona).

---

# Errores

Si ocurre un error durante la generación del PDF.

El sistema deberá.

Registrar el error.

Conservar el pago.

Informar claramente al usuario.

Permitir generar nuevamente el PDF sin modificar la información financiera.

Nunca deberá registrarse un segundo pago por un problema de impresión.

---

# Preparación para Futuras Versiones

La plantilla deberá diseñarse de forma que permita agregar posteriormente.

Logotipo institucional.

Código QR.

Código de barras.

Firma digital.

Información tributaria.

Mensajes personalizados.

Publicidad institucional.

Sin modificar la estructura principal del recibo.

---

# Declaración Final

Esta plantilla constituye el diseño oficial que deberá utilizar el Sistema de Administración de Préstamos para generar todos los recibos de CREEMOS EN TI SAS.

Toda implementación deberá respetar esta distribución, garantizando que los documentos impresos conserven un aspecto tradicional, profesional, legible y optimizado para el trabajo diario de la empresa.

---

**Fin del documento.**