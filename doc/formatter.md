# Doc Lint

l archivo .blackrc te permite configurar diversas opciones para personalizar el comportamiento del formateador de código Black en tus proyectos Python. Además de establecer la longitud máxima de línea (line-length), puedes configurar lo siguiente:

## 1. Modo de formato

mode: Define el modo de formato que Black debe utilizar. Las opciones disponibles son:

standard (predeterminado): Formatea el código de acuerdo con las reglas estándar de Black.
safe: Formatea el código de manera segura, preservando comentarios y espacios en blanco existentes.
aggressive: Formatea el código de manera más agresiva, reestructurando el código y eliminando espacios en blanco innecesarios.

## 2. Estilo de sangría

indent: Define el estilo de sangría que Black debe usar. Las opciones disponibles son:

tab (predeterminado): Usa sangrías con tabuladores.
space: Usa sangrías con espacios en blanco.
four: Usa sangrías de 4 espacios en blanco.

## 3. Envoltura de texto

wrap: Define si Black debe envolver el texto en líneas separadas. Las opciones disponibles son:

never (predeterminado): No envuelve el texto.
always: Envuelve el texto en todas las líneas.
after: Envuelve el texto solo después de alcanzar la longitud máxima de línea.

## 4. Formato de cadenas

string-normalization: Define cómo Black debe manejar las cadenas de texto. Las opciones disponibles son:

none (predeterminado): No modifica las cadenas de texto.
case: Convierte las cadenas de texto a minúsculas.
upper: Convierte las cadenas de texto a mayúsculas.
quotes: Cambia las comillas dobles por comillas simples.

## 5. Formato de comentarios

comment-indentation: Define cómo Black debe indentar los comentarios. Las opciones disponibles son:

true (predeterminado): Indenta los comentarios al mismo nivel que el código.
false: No indenta los comentarios.

## 6. Formato de importaciones

import-sorting: Define cómo Black debe ordenar las importaciones. Las opciones disponibles son:

none (predeterminado): No ordena las importaciones.
alphabetical: Ordena las importaciones alfabéticamente.
depth: Ordena las importaciones por profundidad.
third-party: Ordena las importaciones de terceros por separado.

## 7. Formato de excepciones

except: Define cómo Black debe formatear las excepciones. Las opciones disponibles son:

simple (predeterminado): Formatea las excepciones de manera simple.
chained: Formatea las excepciones encadenadas en una sola línea.

## 8. Formato de clases

class-definition: Define cómo Black debe formatear las definiciones de clase. Las opciones disponibles son:

separate-header: Separa el encabezado de la clase del cuerpo de la clase.
single-line: Formatea la definición de la clase en una sola línea.

## 9. Formato de funciones

function-definition: Define cómo Black debe formatear las definiciones de función. Las opciones disponibles son:

separate-header: Separa el encabezado de la función del cuerpo de la función.
single-line: Formatea la definición de la función en una sola línea.

## 10. Opciones adicionales

target-version: Define la versión mínima de Python para la que debe ser compatible el código formateado.
ignore: Define patrones para excluir archivos o directorios del formateado.
include: Define patrones para incluir archivos o directorios en el formateado.
