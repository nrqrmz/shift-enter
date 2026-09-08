# shift-enter

> `Shift + Enter` es el atajo que ejecuta una celda. Es donde empieza todo.

Una colección de notebooks para explorar matemáticas, ciencias, lenguaje y humanidades **ejecutando código**, no leyendo sobre él. Están pensadas para alumnos de secundaria y son multidisciplinarias a propósito: casi ningún tema interesante cabe en una sola materia.

No hace falta instalar nada. Todo corre en el navegador.

---

## Cómo empezar

1. Haz clic en el badge **Open in Colab** de la notebook que quieras abrir.
2. En Colab, ve a **Archivo → Guardar una copia en Drive**. Trabaja siempre sobre tu copia: si no lo haces, pierdes todo lo que escribas al cerrar la pestaña.
3. Para ejecutar una celda, presiona **`Shift + Enter`**.

Puedes cambiar el código, romperlo y volver a correrlo cuantas veces quieras. Tu copia es tuya.

---

## Las Grandes Presentaciones

Cinco notebooks que dan el marco general. No son de un área en particular: son el mapa donde todo lo demás encuentra su lugar. Conviene recorrerlas antes de entrar a las secuencias.

1. **El Dios sin manos** — el origen del universo y la formación de la Tierra
2. **La venida de la vida** — el tiempo profundo y la evolución de los seres vivos
3. **La venida de los seres humanos** — de dónde venimos y qué nos hizo distintos
4. **La comunicación en signos** — la historia de la escritura y del lenguaje
5. **La historia de los números** — cómo la humanidad aprendió a contar y a medir

_(en construcción)_

---

## Las Grandes Presentaciones del Código

Si el código es la herramienta con la que se recorre todo lo demás, el código también merece sus propias grandes historias. Cinco presentaciones que dan el todo del cómputo antes que las partes. Aquí la demostración dramática no es el globo negro ni la tira del tiempo: es código que corre.

Cada presentación abre su propia secuencia de notebooks. Los nombres propios que aparecen ahí no son adorno: cada uno es una notebook.

**1. La máquina sin manos** — *el origen del cómputo*

Un interruptor. Prendido, apagado. De ahí sale todo. Cómo se le enseñó a contar a una piedra: electricidad → binario → compuertas → capas de abstracción. La ley de este universo: todo es número, y todo es estado que cambia.

- *Demostración:* construir un sumador con AND/OR/NOT; abrir una imagen, un sonido y un texto y ver que son la misma sustancia.
- *Abre:* representación, tipos, binario, hardware, abstracción.

*Secuencia:*

- **El interruptor** — prendido y apagado: construir NOT, AND y OR desde cero
- **Leibniz y el binario** — contar con dos dedos; de 0 y 1 a cualquier número
- **El sumador** — cómo un montón de compuertas aprende a sumar
- **Todo es número** — un texto, una imagen y un sonido abiertos por dentro: la misma sustancia
- **Las capas** — de la compuerta al lenguaje, y por qué ya nadie programa con interruptores

**2. La venida del proceso** — *el algoritmo y la vida*

Una receta que se ejecuta sin su autor presente. De Euclides y al-Juarismi al telar de Jacquard y a Ada Lovelace. Y el asombro central: reglas simples → comportamiento complejo. La vida en la Tierra es un algoritmo corriendo hace 3,800 millones de años.

- *Demostración:* Game of Life de Conway; el MCD de Euclides; un árbol fractal con turtle.
- *Abre:* secuencia, ciclo, condición, función, recursión, emergencia, simulación.

*Secuencia:*

- **al-Juarismi** — la palabra "algoritmo" viene de un nombre; el MCD de Euclides, vivo desde hace 2,300 años
- **El telar de Jacquard** — la tarjeta perforada: el primer programa tejía flores
- **Ada Lovelace** — la Nota G: un programa escrito para una máquina que nunca se construyó
- **Conway** — Game of Life: cuatro reglas, un universo
- **La rama que se repite** — recursión y fractales con turtle
- **3,800 millones de años** — la evolución como algoritmo: mutar, seleccionar, repetir

**3. La venida de quien programa** — *el humano en la máquina*

El tercer regalo montessoriano: mano, mente y corazón. El código no tiene propósito propio: lo pone alguien. Las necesidades humanas fundamentales que resuelve el software. Y el error como práctica humana: depurar. Toda decisión automatizada decide sobre alguien (Therac-25, el Mars Climate Orbiter, un algoritmo que otorga créditos).

- *Demostración:* arreglar un programa roto; escribir uno que resuelva una necesidad real de un compañero.
- *Abre:* descomposición de problemas, depuración, ética, diseño para usuarios, micro-empresa.

*Secuencia:*

- **La primera polilla** — Grace Hopper y el bug; depurar como oficio, no como castigo
- **Mano, mente y corazón** — qué necesidad humana resuelve cada programa que usas
- **Therac-25** — cuando el error mata: una condición de carrera y seis pacientes
- **El Mars Climate Orbiter** — una sonda perdida por confundir libras con newtons
- **Un programa para alguien más** — resolver la necesidad real de un compañero y verlo usarlo
- **El algoritmo que decide** — quién recibe el crédito, quién no, y quién escribió esa regla

**4. La comunicación en código** — *lenguajes y redes*

El espejo directo de "La comunicación en signos": de los interruptores al código máquina, al ensamblador, a Python — la historia de los lenguajes de programación es la historia de la escritura. Y el código se lee mucho más de lo que se ejecuta: nombrar bien es escribir bien. Luego, máquinas hablándose: protocolos, internet, APIs. Y git como la escritura de la historia entre personas.

- *Demostración:* el mismo programa en tres niveles de lenguaje; llamar a una API pública y ver el mensaje crudo.
- *Abre:* sintaxis, nombres, web, redes, formatos, control de versiones, colaboración.

*Secuencia:*

- **De la compuerta a Python** — el mismo programa en tres niveles de lenguaje
- **Grace Hopper y el compilador** — la idea de hablarle a la máquina en nuestro idioma
- **Nombrar es escribir** — el código se lee mucho más de lo que se ejecuta
- **El mensaje crudo** — abrir una petición HTTP por dentro: pedir, responder, JSON
- **Llamar al mundo** — una API pública y datos que no son tuyos
- **Git** — escribir la historia entre varios sin pisarse

**5. La historia de los datos** — *contar, medir y decidir*

El espejo de "La historia de los números": del hueso de Ishango al censo, a la hoja de cálculo, al dataset. Cómo la humanidad guardó lo que sabe y cómo la máquina aprendió a encontrar patrones ahí: ordenar, buscar, medir, y finalmente modelos que aprenden. Cierra con humildad: lo que una computadora no puede hacer (el programa que nunca termina, lo que los datos no pueden decir).

- *Demostración:* ordenar a mano vs. ordenar con código y cronometrar; un dataset real; un modelito que aprende; un programa que no se detiene.
- *Abre:* estructuras de datos, archivos, estadística, IA, complejidad, límites.

*Secuencia:*

- **El hueso de Ishango** — veinte mil años de rayitas: la primera base de datos
- **Del censo a la hoja de cálculo** — guardar lo que sabe un pueblo entero
- **Ordenar y buscar** — a mano contra la máquina, con cronómetro
- **Medir el mundo** — un dataset real y las preguntas que sí se pueden responder
- **La máquina que aprende** — un modelito entrenado desde cero, y qué aprendió de verdad
- **El programa que nunca termina** — lo que una computadora no puede hacer, y por qué eso es hermoso

_(en construcción)_

---

## Secuencias

Después de las Grandes Presentaciones, el material se organiza en tres grandes dominios.

### Expresión Creativa

- **Lenguaje y composición** — escribir, analizar textos, jugar con las palabras
- **Música** — ritmo, escalas y armonía como estructuras que se pueden calcular y escuchar
- **Artes visuales** — geometría, color y composición
- **Medios y narrativa digital** — contar historias con imagen, sonido y datos

_(en construcción)_

### Desarrollo Cognitivo

- **Matemáticas** — aritmética, proporción, probabilidad y estadística
- **Geometría** — figuras, transformaciones y demostración
- **Álgebra** — patrones, variables y funciones
- **Lengua y segunda lengua** — estructura del idioma propio y de otro

_(en construcción)_

### Preparación para la Vida Adulta

- **La Tierra y los seres vivos** — geología, clima, botánica y zoología
- **El progreso humano** — física y química detrás de los inventos que cambiaron el mundo
- **Historia y humanidades** — geografía, economía, política y sociedad
- **Ocupaciones y micro-empresa** — producción, intercambio y trabajo real

_(en construcción)_

---

## Estado del proyecto

El repositorio está arrancando. Las secciones de arriba son el mapa de lo que viene; las notebooks se irán publicando por área y este índice es el lugar donde aparecerán.

## Licencia

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.es) — puedes usar, adaptar y compartir este material, incluso en tu propia escuela, siempre que des crédito y lo compartas bajo la misma licencia.

<!-- Plantilla para agregar una notebook al índice:

| Notebook | De qué trata | Abrir |
|---|---|---|
| [Nombre](ruta/notebook.ipynb) | Descripción en una línea | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nrqrmz/shift-enter/blob/main/ruta/notebook.ipynb) |

Nota: las URLs apuntan a la rama `main`. Al crear el remote, renombrar con `git branch -M main`.
-->
