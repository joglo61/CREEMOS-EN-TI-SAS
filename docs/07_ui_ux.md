# DISEÑO DE INTERFAZ (UI/UX)
# Sistema de Administración de Préstamos
## CREEMOS EN TI SAS

Versión 1.0

---

# Objetivo

Este documento define la experiencia de usuario (UX) y el diseño de la interfaz (UI) del Sistema de Administración de Préstamos.

El objetivo principal no es construir una aplicación visualmente llamativa.

El objetivo es construir una herramienta de trabajo rápida, sencilla y eficiente para el personal administrativo de la empresa.

Cada pantalla deberá estar diseñada para reducir el tiempo de atención al cliente y minimizar la posibilidad de cometer errores.

---

# Filosofía de Diseño

Toda la interfaz deberá respetar los siguientes principios.

• Simplicidad.

• Rapidez.

• Claridad.

• Consistencia.

• Legibilidad.

• Estabilidad.

No deberán utilizarse elementos visuales innecesarios.

No deberán utilizarse animaciones excesivas.

No deberán utilizarse ventanas complejas.

El operador debe encontrar cualquier función en pocos segundos.

---

# Perfil del Usuario

El sistema será utilizado por personas que realizan tareas administrativas diariamente.

No se puede asumir que todos los usuarios tengan conocimientos avanzados de informática.

Por esta razón.

La interfaz deberá ser intuitiva.

Los textos deberán ser claros.

Los botones deberán identificarse fácilmente.

Las acciones deberán ser evidentes.

---

# Paleta de Colores

Se utilizará una paleta sobria y profesional.

Color principal.

Azul oscuro.

Color secundario.

Blanco.

Color de éxito.

Verde.

Color de advertencia.

Amarillo.

Color de error.

Rojo.

Color de fondo.

Gris muy claro.

No utilizar colores excesivamente llamativos.

---

# Tipografía

La tipografía deberá ser moderna y altamente legible.

Preferiblemente.

Inter.

Roboto.

Open Sans.

El tamaño mínimo recomendado será de 14 px.

Los títulos deberán utilizar un tamaño superior.

---

# Distribución General

Todas las pantallas compartirán la misma estructura.

----------------------------------------------------

Barra superior

----------------------------------------------------

Menú lateral

|

|

Contenido principal

|

|

----------------------------------------------------

Barra inferior (opcional)

----------------------------------------------------

El usuario nunca deberá perder la orientación dentro del sistema.

---

# Barra Superior

La barra superior permanecerá siempre visible.

Mostrará.

Logo de la empresa.

Nombre del sistema.

Nombre del usuario conectado.

Rol.

Fecha.

Hora.

Botón de cerrar sesión.

---

# Menú Lateral

El menú lateral permanecerá visible durante toda la sesión.

Opciones.

Dashboard.

Clientes.

Pagos.

Historial.

Facturas.

Archivos.

Reportes.

Configuración.

Usuarios.

Cerrar sesión.

Cada opción utilizará un icono sencillo.

El menú deberá poder contraerse para aprovechar mejor el espacio.

---

# Dashboard

Será la primera pantalla después del inicio de sesión.

Mostrará tarjetas con indicadores.

Clientes activos.

Clientes en mora.

Capital pendiente.

Ingresos del día.

Cantidad de pagos registrados.

Facturas generadas.

Última sincronización.

Último respaldo.

Debajo aparecerá una tabla con los últimos pagos registrados.

---

# Diseño de Tarjetas

Todas las tarjetas deberán compartir el mismo diseño.

Título.

Valor.

Icono.

Color representativo.

No utilizar gráficos innecesarios.

La información deberá poder entenderse con una sola mirada.

---

# Tabla Principal

Las tablas utilizadas en todo el sistema deberán compartir el mismo comportamiento.

Permitir ordenar.

Permitir buscar.

Permitir paginación.

Permitir seleccionar filas.

Permitir acciones rápidas.

El diseño deberá ser uniforme en todos los módulos.

---

# Botones

Todos los botones deberán utilizar el mismo estilo.

Botón principal.

Guardar.

Color azul.

Botón secundario.

Cancelar.

Color gris.

Botón de éxito.

Imprimir.

Color verde.

Botón de advertencia.

Editar.

Color amarillo.

Botón de peligro.

Eliminar (si aplica en futuras versiones).

Color rojo.

---

# Formularios

Todos los formularios deberán seguir la misma estructura.

Etiqueta.

Campo.

Mensaje de validación.

Separación uniforme.

Los campos obligatorios deberán identificarse claramente.

Nunca permitir guardar formularios incompletos.

---

# Mensajes

Toda comunicación con el usuario deberá ser clara.

Ejemplos.

Cliente creado correctamente.

Pago registrado correctamente.

Factura generada correctamente.

Archivo actualizado correctamente.

Nunca mostrar mensajes técnicos.

Nunca mostrar excepciones del sistema.

Nunca mostrar trazas de errores.

---

# Pantalla de Inicio de Sesión

La pantalla de inicio deberá ser sencilla.

Elementos.

Logo de la empresa.

Nombre del sistema.

Campo Usuario.

Campo Contraseña.

Botón Ingresar.

Mensaje de versión.

No deberán existir opciones innecesarias.

El usuario deberá poder iniciar sesión en pocos segundos.

---

# Pantalla Clientes

Será una de las pantallas más utilizadas.

La distribución será.

--------------------------------------------------

Botón Nuevo Cliente

Campo Buscar

--------------------------------------------------

Tabla

--------------------------------------------------

Placa

Nombre

Teléfono

Saldo

Próximo Pago

Estado

Acciones

--------------------------------------------------

Las acciones disponibles serán.

Ver.

Editar.

Registrar Pago.

Historial.

Cronograma.

---

# Pantalla Nuevo Cliente

El formulario deberá organizarse por secciones.

Información Personal.

Nombre.

Cédula.

Teléfono.

Dirección.

Correo.

Información del Préstamo.

Valor del préstamo.

Valor de la cuota.

Fecha del primer pago.

Observaciones.

Botones.

Guardar.

Cancelar.

Después de guardar.

Mostrar confirmación.

Redireccionar automáticamente a la ficha del cliente.

---

# Pantalla Información del Cliente

Al abrir un cliente.

La información deberá distribuirse mediante tarjetas.

Tarjeta 1.

Información personal.

Tarjeta 2.

Información financiera.

Tarjeta 3.

Estado del préstamo.

Tarjeta 4.

Acciones rápidas.

Registrar pago.

Editar.

Ver historial.

Ver cronograma.

En la parte inferior.

Historial reciente.

---

# Pantalla Registrar Pago

Esta será la pantalla más importante del sistema.

Debe permitir registrar un pago en menos de un minuto.

Distribución.

--------------------------------------------------

Información del Cliente

Nombre

Placa

Saldo

Valor Cuota

Fecha Próximo Pago

Estado

--------------------------------------------------

Valor Recibido

[__________________]

Observaciones

[__________________]

--------------------------------------------------

Resultados Calculados

Intereses

Mora

Intereses Totales

Capital

Nuevo Saldo

--------------------------------------------------

Botones

Guardar e Imprimir

Cancelar

--------------------------------------------------

Mientras el operador escribe el valor recibido.

Todos los cálculos deberán actualizarse automáticamente.

No deberá existir un botón llamado.

Calcular.

---

# Vista Previa del Recibo

Antes de guardar definitivamente.

El sistema mostrará una vista previa.

La vista deberá mostrar exactamente el mismo diseño que tendrá el PDF.

El usuario podrá comprobar.

Número de factura.

Cliente.

Fecha.

Valores.

Firma.

Observaciones.

Botones.

Guardar e Imprimir.

Cancelar.

---

# Pantalla Historial

El historial deberá mostrarse mediante una tabla.

Columnas.

Factura.

Fecha.

Valor.

Intereses.

Capital.

Saldo anterior.

Saldo nuevo.

Usuario.

Acciones.

Ver.

Reimprimir.

Descargar PDF.

La búsqueda deberá funcionar en tiempo real.

---

# Pantalla Facturas

Permitirá consultar todas las facturas emitidas.

Filtros.

Número.

Cliente.

Placa.

Fecha.

Estado.

Cada fila tendrá.

Ver.

Descargar.

Reimprimir.

---

# Pantalla Administración de Archivos

Esta pantalla permitirá administrar los archivos Excel utilizados por el sistema.

Se dividirá en dos tarjetas.

--------------------------------------------------

Base de Datos Excel

Archivo cargado.

Fecha de carga.

Versión.

Estado.

Botón.

Reemplazar.

--------------------------------------------------

Archivo Financiero

Archivo cargado.

Fecha de carga.

Versión.

Estado.

Botón.

Reemplazar.

--------------------------------------------------

En la parte inferior.

Historial de archivos cargados.

Nunca deberá solicitar rutas manuales.

El usuario únicamente seleccionará el archivo.

---

# Pantalla Configuración

Solo estará disponible para administradores.

Se organizará mediante pestañas.

Empresa.

Sistema.

Facturación.

Archivos.

Respaldos.

Usuarios.

Cada pestaña contendrá únicamente información relacionada.

---

# Pantalla Usuarios

Mostrará una tabla.

Usuario.

Nombre.

Rol.

Estado.

Último acceso.

Acciones.

Editar.

Activar.

Desactivar.

Cambiar contraseña.

No se permitirá eliminar usuarios.

---

# Pantalla Backups

Mostrará todos los respaldos disponibles.

Información.

Tipo.

Fecha.

Hora.

Usuario.

Tamaño.

Acciones.

Restaurar.

Descargar.

Eliminar (solo futuras versiones).

Antes de restaurar.

Mostrar una ventana de confirmación.

---

# Pantalla Logs

Permitirá consultar todas las acciones realizadas.

Filtros.

Usuario.

Fecha.

Módulo.

Acción.

Resultado.

Tabla.

Fecha.

Hora.

Usuario.

Descripción.

Resultado.

Los logs únicamente podrán consultarse.

Nunca modificarse.

Nunca eliminarse.

# Responsividad

Aunque el sistema estará diseñado principalmente para computadores de escritorio.

Toda la interfaz deberá adaptarse correctamente a diferentes resoluciones.

Resoluciones mínimas soportadas.

1366 × 768

1600 × 900

1920 × 1080

No es prioridad el uso desde teléfonos móviles.

Sin embargo.

La interfaz no deberá romperse si es abierta desde una tablet.

---

# Espaciado

Toda la aplicación deberá mantener un espaciado uniforme.

Entre tarjetas.

24 px.

Entre formularios.

20 px.

Entre botones.

12 px.

Entre campos.

16 px.

No deberán existir elementos visualmente amontonados.

---

# Iconografía

Los iconos deberán ser simples.

Se recomienda utilizar Heroicons o Lucide.

Nunca utilizar iconos decorativos.

Cada icono deberá ayudar al usuario a identificar rápidamente la función del botón.

---

# Confirmaciones

Toda operación crítica deberá solicitar confirmación.

Ejemplos.

Registrar pago.

Restaurar respaldo.

Cambiar configuración.

Reemplazar archivo Excel.

La ventana de confirmación deberá explicar claramente lo que ocurrirá.

---

# Carga de Información

Mientras el sistema procese información deberá mostrarse un indicador visual.

Ejemplos.

Cargando cliente...

Generando recibo...

Actualizando Excel...

Sincronizando información...

Nunca dejar la interfaz congelada.

---

# Estados Vacíos

Cuando una tabla no tenga información.

Mostrar un mensaje amigable.

Ejemplo.

"No existen registros para mostrar."

Cuando una búsqueda no encuentre resultados.

Mostrar.

"No se encontraron clientes con esa información."

Nunca mostrar tablas completamente vacías sin explicación.

---

# Colores de Estado

Todos los estados utilizarán colores consistentes.

Activo.

Verde.

Inactivo.

Gris.

En Mora.

Rojo.

Próximo a vencer.

Amarillo.

Finalizado.

Azul.

Los colores deberán utilizarse en todas las pantallas de manera uniforme.

---

# Accesibilidad

Toda la aplicación deberá ser fácil de utilizar.

Botones grandes.

Texto legible.

Buen contraste.

Navegación mediante teclado cuando sea posible.

Los formularios deberán permitir avanzar utilizando la tecla TAB.

---

# Atajos

Se recomienda implementar atajos de teclado para acelerar el trabajo diario.

Ejemplos.

F2

Buscar cliente.

F3

Registrar pago.

F4

Nuevo cliente.

ESC

Cancelar.

CTRL + P

Imprimir.

Estos atajos deberán mostrarse en los botones correspondientes.

---

# Flujo de Atención

La navegación deberá seguir siempre el mismo orden.

Dashboard.

↓

Buscar Cliente.

↓

Seleccionar Cliente.

↓

Registrar Pago.

↓

Vista Previa.

↓

Imprimir.

↓

Regresar automáticamente al buscador.

El operador deberá estar listo para atender al siguiente cliente inmediatamente.

---

# Tiempo de Operación

Objetivos máximos.

Buscar cliente.

Menos de 1 segundo.

Abrir ficha.

Menos de 1 segundo.

Registrar pago.

Menos de 10 segundos.

Generar PDF.

Menos de 3 segundos.

Abrir impresión.

Menos de 2 segundos.

El sistema deberá sentirse inmediato.

---

# Diseño del Recibo

La vista previa deberá ser idéntica al PDF.

No deberá existir diferencia entre ambos.

Lo que el usuario visualice será exactamente lo que se imprimirá.

Esto evitará errores de impresión.

---

# Consistencia Visual

Todas las pantallas deberán compartir.

La misma tipografía.

Los mismos botones.

Los mismos colores.

Las mismas tablas.

Los mismos formularios.

Los mismos mensajes.

El usuario nunca deberá sentir que está utilizando aplicaciones diferentes.

---

# Principio Fundamental

La interfaz deberá diseñarse pensando en personas que utilizarán el sistema durante toda la jornada laboral.

Cada clic innecesario representa tiempo perdido.

Cada pantalla deberá construirse buscando reducir el esfuerzo del operador.

La prioridad absoluta será la productividad.

---

# Declaración Final

Este documento define oficialmente la experiencia de usuario y el diseño visual del Sistema de Administración de Préstamos de CREEMOS EN TI SAS.

Toda interfaz desarrollada deberá respetar estas especificaciones.

Cualquier modificación visual deberá mantener la simplicidad, la claridad y la eficiencia definidas en este documento.

---

**Fin del documento.**