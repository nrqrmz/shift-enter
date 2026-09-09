# Rediseño de «La piedra que aprendió a contar»

Fecha: 2026-09-09
Estado: aprobado, listo para plan de implementación

## 1. El problema

La notebook corre sin un solo error. Se ejecuta completa en 6.4 segundos y el
sumador acierta las 16,384 sumas. Lo que está roto no es el código: es el
recorrido.

Cuatro fallas, todas confirmadas por el autor:

1. **El alumno lee mucho y hace poco.** De treinta celdas de código, veintinueve
   ya vienen escritas. El único hueco real que llena es `NAND`.
2. **El wow llega tarde.** Lo que de verdad asombra (el nombre convertido en
   números, la carita dibujada con listas, la foto por dentro, el acorde) vive en
   la §4, después de atravesar la §2 del binario, que es la más árida y la más
   larga.
3. **No hay reto ni meta.** Nada que ganar, nada que perder, ningún marcador.
4. **Ritmo de ensayo.** Párrafos largos entre celda y celda. Se lee como un
   artículo, no como algo que se juega.

Y el diagnóstico del autor, que es el que manda: **el alumno le da play y el
output tiene que capturarlo.** Hoy el output es una figura estática de matplotlib
o un `print`. El público objetivo tiene entre 12 y 14 años.

## 2. El objetivo

Que al terminar el alumno diga: *claro, yo quiero programar, y quiero aprenderlo
bien.*

Sigue siendo **una sola notebook**. La duración baja de unos cuarenta y cinco
minutos a unos veinticinco o treinta.

## 3. La idea que reorganiza todo

Las cuatro cosas que ya funcionan en la notebook comparten un verbo. En el
cifrado de César el alumno le suma 3 a cada letra. En la foto le suma 70 a cada
pixel. En el acorde suma tres ondas. En el sumador, suma.

Ese verbo es el hilo, y da el final: *todo el día estuviste sumando; allá abajo,
adentro de la piedra, ¿quién suma? Nadie. No hay nadie. Vamos a construirlo.*

Por eso se voltea la torre. La notebook arranca donde hoy termina.

### La promesa nueva

> Hoy vas a abrir tu nombre, tu foto y tu música por dentro, y vas a descubrir
> que las tres son la misma cosa: números. Y al final vas a construir con tus
> manos la pieza de la computadora que suma esos números, sin escribir ni una
> sola vez el signo `+`.

La segunda mitad de la promesa es el pago más fuerte que ya tiene el archivo y se
conserva intacta.

### El costo de voltear

Las compuertas dejan de ser el requisito de entrada y pasan a ser la recompensa
de salida. Se simplifican de verdad: `NO`, `Y`, `O` como tres `if`, la tabla que
revela que la suma es `XOR` y el llevo es `Y`, y el sumador corriendo. **Se
eliminan `NAND`, su ejercicio y su «para pensar».** El tratamiento a detalle de
las compuertas se va a su propia notebook, fuera de este alcance.

## 4. El recorrido nuevo

Cada sección abre con algo que el alumno hace en menos de un minuto.

### §1 · Tu nombre

- Escribe su nombre y sale convertido en números.
- Lo escucha: cada letra es un número, cada número es una frecuencia.
- Le suma 3 a cada letra y queda cifrado. `correr` la escribe el alumno.
- **El disco cifrador.** Dos tiras del alfabeto, una sobre otra, y un deslizador
  que corre la de abajo. Al arrastrarlo la tira se mueve y el mensaje se
  descifra al mismo tiempo.
- **El reto.** Un mensaje cifrado y ningún número. Encuéntralo.

### §2 · Tu foto

- Dibuja una carita de ocho por ocho escribiendo puntos y gatos en un texto.
- Sube su propia foto, o se queda con la de respaldo.
- La recorre con el mouse leyendo el número de cada pixel, y se acerca.
- Le mueve el brillo, la invierte.
- Arma cualquier color del mundo con tres deslizadores.

### §3 · Tu música

- Escucha una onda y le mueve los hertz.
- La pone al doble de velocidad y al revés.
- Suma tres ondas y sale un acorde de do mayor.

### §4 · ¿Y cómo cabe eso en una piedra?

Aquí recién aparece el interruptor, como respuesta a una pregunta que el alumno
ya se está haciendo.

- Prendido y apagado. `True` y `False`. `True == 1`.
- **Ocho botones que prende con el dedo**, y el número aparece vivo.
- **El botón de play contando de 0 a 255.** El interruptor de la derecha
  parpadea, el de la izquierda casi no se mueve.
- Su nombre, otra vez, ahora en interruptores. Devolución a la §1.
- **El desbordamiento.** El contador trepa 253, 254, 255 y cae a cero. Pac-Man y
  el nivel 256. El Ariane 5 y los 370 millones de dólares.

### §5 · ¿Quién suma allá abajo? Nadie

- `NO`, `Y`, `O`: tres `if` escritos por el alumno.
- `XOR`: prendido cuando son distintos.
- La tabla de sumar un bit, que revela que la suma es `XOR` y el llevo es `Y`.
- `medio_sumador`, `sumador_completo`, `sumar`.
- 13 + 29 = 42, columna por columna.
- Se califica solo contra el `+` de Python.

### §6 · La torre

Cierre y puerta a la siguiente notebook, «la venida del proceso».

## 5. Inventario de wow

Lo que ya existe y sube de volumen:

| Hoy | Queda |
|---|---|
| Dibujo estático de interruptores | Ocho botones que se prenden con el dedo |
| Tabla impresa contando de 0 a 31 | `widgets.Play` corriendo de 0 a 255 |
| Desbordamiento contado en prosa | El contador cayendo a cero en vivo |
| Carita escrita como lista de listas | Un texto de `.` y `#` que el alumno dibuja |
| César impreso | El disco cifrador con deslizador y un reto |
| Foto de Leibniz | Su propia foto, recorrida con el mouse |

Lo que se incorpora y hoy no existe:

- **Color.** Todo el archivo es gris. Tres deslizadores de rojo, verde y azul.
- **Voz de ardilla.** El mismo sonido al doble de velocidad, y al revés.
- **El nombre como melodía.**

Descartado por costo, con la decisión ya tomada:

- **Animaciones incrustadas.** No hacen falta: `widgets.Play` da el contador y
  plotly da el acercamiento, y ninguna de las dos pesa en el archivo.
- **La lista de misión que se palomea sola.** El reto del disco cifrador y el
  autocalificado del sumador ya cubren la meta que faltaba.

## 6. El paquete `shift_enter`

El repo conserva su nombre. El paquete se importa como `shift_enter`, porque
`shift-enter` no es un identificador válido de Python.

### La regla que decide qué entra

**El paquete es plomería y nada más.** Si dibuja, mide, formatea, descarga o
anima, entra. Si es lo que se está enseñando, no entra nunca.

Se escriben a mano en celdas visibles, aunque sea más largo: `correr`, `NO`, `Y`,
`O`, `XOR`, `medio_sumador`, `sumador_completo` y `sumar`. Si el sumador viviera
en el paquete, el alumno ya no construiría nada y la promesa se cae.

### Los módulos

- `paleta` — colores y estilo, en un solo lugar.
- `binario` — `TABLA_DE_VALORES`, `a_binario`, `a_decimal`.
- `interruptores` — `simbolo`, `dibujar`, `tablero`, `contador`,
  `tabla_de_verdad`.
- `imagen` — `de_respaldo`, `selector`, `mostrar_con_numeros`, `desde_texto`,
  `deslizador_brillo`, `mezclador_color`.
- `sonido` — `onda`, `reproducir`, `dibujar_onda`, `melodia_del_nombre`,
  `a_velocidad`, `al_reves`.
- `cifra` — `disco`, `deslizador_disco`, `MENSAJE_RETO`.

La foto de respaldo viaja **dentro** del paquete como dato empacado. Hoy se baja
de Wikimedia y si Wikimedia falla se cae media notebook.

### Distribución

Una sola línea escondida en la celda de forma:

```
!pip install -q git+https://github.com/nrqrmz/shift-enter
```

Se descarta PyPI por ahora. Da instalación más rápida y versiones de verdad,
pero obliga a un release cada vez que se toca un helper. Si el repo crece a
veinte notebooks, se migra.

Requisitos que esto impone:

- **El repo tiene que ser público** y necesita un `pyproject.toml`. Si está
  privado, ninguna notebook abre para ningún alumno.
- **Hay que unificar la rama.** El repo local está en `master` y el README apunta
  a `main`. Se decide antes de que existan enlaces de Colab en el mundo.
- **La copia del alumno vive en Drive** e importa lo que haya hoy en el repo. Si
  cambia la firma de una función, se le rompe. Se mitiga clavando una etiqueta en
  la línea de instalación, o tratando la lista de arriba como API congelada una
  vez publicada.

## 7. Librerías de dibujo

`plotly` aparece **exactamente una vez** en toda la notebook: la foto que se
recorre con el mouse leyendo el número de cada pixel y se acerca con dos dedos.
Ahí la interacción es la lección.

Todo lo demás es matplotlib movido con `ipywidgets`.

La razón es que GitHub solo pinta salidas de imagen. Una figura de plotly se
guarda como JSON interactivo y en la página del repo queda un hueco en blanco, y
en este repo las salidas se comiten a propósito para que la notebook se lea en
GitHub. Acotar plotly a una sola celda paga la interacción donde importa sin
vaciar la página.

Ninguna dependencia nueva. Colab ya trae todo: `numpy`, `matplotlib`, `plotly`,
`requests`, `Pillow`, `ipywidgets`.

## 8. Cuando algo falla

- **La foto del alumno no bloquea.** Se usa el widget de subir archivo y no
  `files.upload()`, porque ese último se queda esperando para siempre cuando la
  notebook corre sola. Mientras el alumno no suba nada, la sección funciona
  completa con la foto de respaldo.
- **Sin red no se cae nada.** La foto de respaldo viene empacada.
- **Cada celda interactiva deja un primer cuadro fijo** antes de encender el
  widget, para que quien solo lee en GitHub vea algo. El estado de los widgets no
  se guarda nunca.
- **Nombres con acentos, eñes y emojis.** `a_binario` recibe hoy números
  mayores a 255 y devuelve listas de más de ocho bits, que revientan contra
  `TABLA_DE_VALORES`. Decisión: el ancho se queda en ocho y el carácter que no
  quepa no revienta, avisa. «Esa letra necesita más de ocho interruptores», que
  además es la lección de la §4 dicha antes de tiempo.

## 9. Deudas técnicas que se pagan de paso

- La celda 29 empieza con `# borrar` y define `display_binary`, que nadie usa.
- Las celdas 25 y 27 traen un `# revisar congruencia y continuidad` colgado.
- **La promesa tiene una fuga:** `a_decimal` convierte con `int(cadena, 2)`, o
  sea le pide a Python la conversión, y es la pieza que devuelve el resultado
  final de `sumar`. El texto promete que adentro no hay un solo `+`. Decisión:
  `sumar` devuelve los interruptores, no un número. El resultado se muestra como
  ocho focos encendidos, que además pega mucho más fuerte que imprimir 42, y
  `a_decimal` se presenta como «leer los interruptores», fuera de la suma.
- Diez celdas visibles contienen matplotlib, contra la regla explícita de
  CLAUDE.md. Con el paquete, quedan en cero.
- Las compuertas hablan `True`/`False`, las tablas hablan `1`/`0`, y `sumar`
  traduce entre los dos a mano con `x = (bits_a[i] == 1)`. Decisión: todo el
  archivo habla `True`/`False`, incluidas las listas de bits, y solo los dibujos
  y los `print` los pintan como 1 y 0. La lección «`True == 1`» de la §4 es
  exactamente lo que justifica esa mezcla, y así no queda una sola traducción a
  mano.

## 10. Verificación

Tres capas:

1. **Aserciones sobre el paquete.** `a_binario` y `a_decimal` son inversas para
   todo el rango, el sumador acierta las 16,384 sumas, `correr` es reversible.
   Esto hoy es imposible porque el código vive dentro del JSON de una notebook.
2. **La notebook re-ejecutada de arriba abajo** con `nbclient`, según el
   procedimiento de CLAUDE.md.
3. **Revisión de que ninguna celda quedó con salida de error**, porque una celda
   fallida es silenciosa en el archivo.

Ninguna de las tres cubre lo que de verdad importa, que es si un chico de doce
años se engancha. Eso se prueba con un chico de doce años.

## 11. Fuera de alcance

- La notebook a detalle de compuertas lógicas, que recibe `NAND`, `NOR` y la
  universalidad.
- Las otras notebooks de la secuencia.
- Publicar el paquete en PyPI.
- `legacy-la-piedra-que-aprendio-a-contar.ipynb`, que sigue siendo un borrador
  superado.
