# La piedra que aprendió a contar — tanda de correcciones

Fecha: 2026-09-09
Notebook: `la-piedra-que-aprendio-a-contar.ipynb`
Paquete: `shift_enter/`

## Por qué

Enrique corrió la notebook completa en Colab y levantó dieciséis correcciones:
dos bugs reproducibles, un cambio de plataforma, una reescritura de la parte
cinco, y una lista de problemas de tono y de vocabulario. Este documento fija
qué se cambia y por qué, para que el plan de implementación no tenga que
volver a decidir nada.

## Decisiones de fondo

**Colab es el único blanco.** Se deja de diseñar para que la notebook se lea en
GitHub sin ejecutarla. Esto autoriza dos cosas que antes estaban prohibidas:
quitar los cuadros fijos que se dibujaban antes de cada widget, y dejar que
plotly elija su propio renderer. Los resultados ejecutados se siguen guardando
en el archivo, pero ahora solo como verificación, no como lectura.

**En la notebook no queda ningún `def` a la vista, ni ningún `if` salvo la
excepción que se describe abajo.** Es una
notebook de descubrimiento y todavía no se enseñan funciones. Todo lo que hoy
es código de funciones se muda al paquete. Lo que el alumno construye, lo
construye con el dedo sobre un widget.

**Esto redefine cómo se cumple la promesa.** La celda tres promete construir
con tus manos la pieza que suma, sin escribir nunca el signo de más. La promesa
se sostiene, pero ahora el verbo construir apunta a un widget donde el alumno
arma el sumador de ocho columnas y ve los llevos brincar, no a código que
escribe. La redacción de la promesa se ajusta para decir con el dedo.

**Una sola excepción a la regla del código invisible.** La celda que califica el
sumador contra el `+` de Python se queda visible. Son dos ciclos y un `if`, sin ningún `def`,
y es la única celda donde ver el código es lo que hace que la prueba valga: si
la comparación se esconde, la calificación deja de ser una prueba y se vuelve
una afirmación del taller.

## Los dos bugs, con su causa

**La foto por dentro no dibuja en Colab.** `imagen.mostrar_con_numeros` usa
plotly. El código de plotly detecta Colab solo y elige el renderer correcto,
pero la celda de taller le impone `plotly_mimetype+notebook_connected` encima y
pisa esa detección. Se verificó leyendo `plotly.io._renderers`, donde la
detección de `google.colab` es explícita. Arreglo: quitar esa línea y el import
de `plotly.io` de la celda de taller. Instalar plotly no era el arreglo, porque
Colab ya lo trae.

**`Glyph 20 missing from font`.** `cifra.MENSAJE_RETO` guarda el espacio cifrado
como `%`, que es el carácter 37. Cuando el slider va en 17, la resta cae en el
carácter 20, que es un carácter de control sin dibujo. Arreglo: el espacio
tiene que seguir corriéndose, porque de ahí sale la pregunta para pensar que
cierra la parte uno, así que la corrección va en el dibujo. `cifra.disco`
sustituye cualquier carácter no imprimible por `▯` antes de mandarlo a
matplotlib.

## Cambios por archivo

### Celda de taller

- Fuera `import plotly.io as pio` y la línea que fija el renderer.
- Fuera `import time`, que solo servía para el cronómetro de la parte seis.
- Entra `compuertas` en la lista de imports de `shift_enter`.
- Sale `simbolo` de los imports sueltos: su única celda desaparece con la
  reescritura de la parte cinco. Se quedan `TABLA_DE_VALORES`, `a_binario` y
  `a_decimal`, que siguen usándose en las partes cuatro y cinco.
- Se conservan los silenciadores del eco de texto de figuras y widgets.

### `shift_enter/compuertas.py` — nuevo

Concentra todo lo que hoy vive en celdas visibles de la parte cinco.

- `NOT(a)`, `AND(a, b)`, `OR(a, b)`, `XOR(a, b)`. Nombres en inglés, como los
  conceptos reales. `XOR` se sigue construyendo con las otras tres, porque de
  eso trata la sección.
- `medio_sumador(a, b)` y `sumador_completo(a, b, llevo)`.
- `sumar(a, b, ancho=8)`.
- `tabla_de_verdad(nombre, compuerta, entradas=2)`, mudada desde
  `interruptores`, con el renglón activo resaltable.
- `probador()`. Widget: dos interruptores de entrada que se prenden con el
  dedo, las salidas de NOT, AND y OR encendiéndose al mismo tiempo, y la tabla
  de verdad al lado con el renglón vigente iluminado.
- `diagrama_xor()`. Widget: el cableado del XOR, entradas a la izquierda y
  salida a la derecha, con los cables que están conduciendo encendidos. Sustituye
  al remate que hoy vive en las tres líneas de código del XOR.
- `medio_sumador_vivo()`. Widget: dos interruptores, dos focos de salida
  rotulados suma y llevo, con el cableado de XOR y AND a la vista.
- `sumador_vivo()`. Widget: dos filas de ocho interruptores, la fila del
  resultado abajo, y los llevos visibles brincando de columna en columna. Este
  es el momento de armarlo con el dedo.

### `shift_enter/cifra.py`

- `_corrido` se vuelve pública como `correr(texto, salto)`. Es la función que
  hoy está escrita a mano en la celda doce de la notebook.
- `DESPLAZAMIENTO_RETO` pasa a `SALTO_RETO`. El parámetro `desplazamiento` pasa
  a `salto` en `disco` y en `deslizador_disco`.
- La etiqueta del slider deja de decir corrimiento y dice salto.
- El slider se ensancha y el número del salto se dibuja grande dentro de la
  figura, no solo en la perilla del widget.
- Helper interno que sustituye caracteres no imprimibles por `▯` al dibujar.
- Fuera el cuadro fijo que se dibujaba antes del widget.

### `shift_enter/imagen.py`

- Fuera los cuadros fijos de `deslizador_brillo` y `mezclador_color`.
- Sin más cambios. El dibujo de la carita vive en la notebook, no aquí.

### `shift_enter/interruptores.py`

- `tablero()` deja de dibujar la figura previa. Solo los ocho botones y el
  marcador.
- `contador()` deja de dibujar la figura previa. Gana un slider ancho y, a su
  lado, un solo botón que dice play y cambia a pausa mientras corre. El botón
  único no existe en ipywidgets: se construye con un hilo en segundo plano que
  avanza el valor del slider. La animación la verifica Enrique en Colab, porque
  no hay Colab en el entorno de desarrollo.
- `dibujar_palabra()` pasa de una figura por letra a una sola figura de un
  renglón por letra, con la letra y su número a la izquierda. Con Ada eran tres
  figuras; con Fernanda serían ocho.
- `tabla_de_verdad` y `_tabla_de_verdad` se van a `compuertas.py`.

### `shift_enter/torre.py`

- Las cuatro apariciones de `§` pasan a parte cuatro, parte cinco y partes uno,
  dos y cuatro.
- La capa de compuertas deja de decir NO, Y, O y dice NOT, AND, OR.
- Nueva `comparar_velocidad()`, que se lleva el cronómetro que hoy está escrito
  a mano en la celda sesenta y nueve. Medir es plomería.

### Tests

`tests/test_interruptores.py`, `tests/test_cifra.py`, `tests/test_tablero.py`,
`tests/test_notebook.py` y `conftest.py` nombran símbolos que se mudan o se
renombran. Se actualizan, y se agrega `tests/test_compuertas.py` que cubra las
cuatro compuertas, el medio sumador, el sumador completo y `sumar`, incluyendo
el desbordamiento de 255 más 1.

## Cambios en la notebook, parte por parte

### Promesa y uso

La promesa cambia construir con tus manos por construir con el dedo, para que
siga siendo cierta ahora que el alumno no escribe el sumador.

### Parte 1

- Título: de *Tu nombre ya está adentro* a **Tu nombre es una lista de
  números**. Queda paralelo con la parte dos, tu foto es una tabla de números,
  y la parte tres, tu música es una lista de números.
- `mi_nombre = "Fernanda"`. Ocho letras, sin acentos ni ñ, de una sola palabra.
  Ocho letras dan una lista de `ord()` que llena la celda y una melodía que
  dura lo suficiente para oírse como melodía. Sin acentos, la suma de César no
  produce caracteres raros.
- Prosa nueva: puedes volver a esta celda cuando quieras, cambiar el nombre y
  volver a correr de aquí para abajo.
- La celda del cifrado pierde el `def correr` y gana la variable del salto:

  ```python
  salto = 3    # ← cámbialo

  secreto = cifra.correr(mi_nombre, salto)
  print("   cifrado:   ", secreto)
  print("   descifrado:", cifra.correr(secreto, -salto))
  ```

  Un solo número gobierna el cifrado y el descifrado. Hoy hay que cambiar el 3
  en dos lugares.
- La celda que anuncia el cifrado se reescribe: ya no dice que el `correr` de
  aquí abajo está completo, dice que lo único que le toca al alumno es cambiar
  el salto.
- César deja de decir que sus enemigos veían basura. Queda: quien interceptaba
  el mensaje se quedaba viendo letras que no decían nada.
- La prosa del reto deja de decir corrimiento y dice salto.

### Parte 2

- `mi_dibujo` pasa de ocho por ocho a dieciséis por dieciséis, en blanco y
  negro. La referencia que dio Enrique tiene fondo azul, cara amarilla y
  contorno negro; traducida a dos tonos, el fondo y la cara quedan blancos y
  el contorno, los ojos y la sonrisa quedan negros. `desde_texto` no cambia:
  sigue entendiendo solo `#` y `.`. El dibujo queda así:

  ```
  .....######.....
  ...##......##...
  ..#..........#..
  .#............#.
  .#............#.
  #....##..##....#
  #....##..##....#
  #....##..##....#
  #..............#
  #..............#
  #..#........#..#
  .#..#......#..#.
  .#...######...#.
  ..#..........#..
  ...##......##...
  .....######.....
  ```
- La foto por dentro vuelve a dibujarse, por el arreglo del renderer.

### Parte 3

- El cierre gana las unidades: le sumaste tres lugares del alfabeto a cada
  letra de tu nombre, le sumaste setenta niveles de luz a cada pixel de tu
  foto, sumaste tres ondas y salió un acorde.

### Parte 4

- La apertura conserva la arena, el cristal y el grabado, y cambia el final.
  Hoy termina en que ninguno sabe sumar y ninguno sabe leer. La versión nueva
  cierra en que cada transistor, por su cuenta, solo sabe estar prendido o
  apagado, y que juntos están corriendo esta página ahorita mismo. Salen las
  palabras aburrido y no hace absolutamente nada.
- Leibniz: el binario deja de ser un juguete inútil y pasa a ser un juguete sin
  ningún uso. Y deja de decir que lo escribió en un papel, que se lee como
  calco del inglés: en 1679 no publicó un artículo, dejó un manuscrito. Queda
  que lo escribió a mano, sin computadoras y sin electricidad.
- La referencia a `§1` pasa a la parte 1.
- El tablero y el contador quedan sin gráfica previa, con los cambios de widget
  ya descritos.
- Tu nombre en interruptores queda en una sola figura de ocho renglones.

### Parte 5

Se reescribe completa. Hoy son tres `if` que el alumno lee, más cuatro
funciones que el alumno no escribió pero ve. Queda así:

1. Apertura con unidades, igual que el cierre de la parte tres, cerrando en que
   allá abajo no hay nadie que sepa sumar.
2. Las tres reglas, con `compuertas.probador()`. Un solo widget dice las dos
   cosas que hoy dicen dos celdas: qué hace cada compuerta, y que la tabla de
   verdad es la definición completa porque no hay caso escondido.
3. El XOR, con `compuertas.diagrama_xor()`. El remate de que XOR no es una
   pieza nueva sobrevive como cableado encendido en vez de como tres líneas de
   código.
4. Las cuatro sumas que existen, con `compuertas.medio_sumador_vivo()`. La
   columna de la suma es XOR y la columna del llevo es AND.
5. El sumador de ocho columnas, con `compuertas.sumador_vivo()`. Aquí se cumple
   la promesa.
6. La calificación contra el `+` de Python. Única celda de código visible de la
   sección, y única de toda la notebook que conserva un `if`:

   ```python
   aciertos = 0
   for a in range(128):
       for b in range(128):
           if a_decimal(compuertas.sumar(a, b)) == a + b:
               aciertos = aciertos + 1

   print(f"✅ {aciertos:,} de 16,384 sumas correctas")
   ```
7. El desbordamiento de 255 más 1, con su Pac-Man y su Ariane 5. Pac-Man deja
   de decir basura: media pantalla se llenó de símbolos revueltos.
8. La celda que enumera de qué está hecho el 42 deja de terminar en que NO, Y y
   O son tres `if`, porque ya no hay `if` que señalar.

### Una consecuencia aceptada

La celda que define `prendido = True` y `apagado = False` hoy alimenta a las
compuertas de la parte cinco. Cuando esas compuertas se van al paquete, esas
dos variables ya no las usa nadie más abajo. Se quedan de todos modos: el
booleano es la lección de esa celda, no un insumo para otra.

### Parte 6

- El cronómetro se va a `torre.comparar_velocidad()`.
- La torre pierde los `§`.

## Verificación

1. `pytest`, con la suite actualizada y `test_compuertas.py` nuevo.
2. Re-ejecutar la notebook con `nbclient`, como indica `CLAUDE.md`, con la
   variable de entorno `PLOTLY_RENDERER=colab` puesta antes de correr el
   comando (plotly la lee antes de autodetectar el entorno, y sin ella un
   kernel local incrusta la librería completa y el archivo pasa de dos y
   medio a doce megabytes), y confirmar con el revisor de errores que no hay
   ninguna celda con `output_type: error`.
3. Confirmar a mano que en la notebook ya no aparece ningún `def` ni ningún
   `if` fuera de la celda de calificación, y que no queda ninguna de las
   palabras retiradas: basura, corrimiento, inútil, aburrido, `§`.
4. Enrique corre la notebook en Colab y verifica las tres cosas que aquí no se
   pueden probar: que la foto por dentro dibuja con su hover, que el botón de
   play anima el contador, y que ningún widget escupe la advertencia de la
   fuente.

## Fuera de alcance

- Cualquier notebook que no sea `la-piedra-que-aprendio-a-contar.ipynb`.
- `legacy-la-piedra-que-aprendio-a-contar.ipynb`, que es un borrador superado.
- Actualizar `CLAUDE.md`, que está en el `.gitignore` del repo.
