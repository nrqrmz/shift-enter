"""Construye la-piedra-que-aprendio-a-contar.ipynb desde cero.

Andamio, no producto. La notebook es el entregable. Este archivo se
borra cuando el rediseno queda terminado.
"""

import nbformat as nbf

CELDAS = []


def md(texto):
    CELDAS.append(nbf.v4.new_markdown_cell(texto.strip("\n")))


def codigo(fuente):
    CELDAS.append(nbf.v4.new_code_cell(fuente.strip("\n")))


def forma(fuente):
    celda = nbf.v4.new_code_cell(fuente.strip("\n"))
    celda.metadata["cellView"] = "form"
    CELDAS.append(celda)


def portada():
    md("# 🪨 La piedra que aprendió a contar")
    md("Una computadora es arena.")
    md("Arena a la que le enseñamos a contar.")
    md("""
## 🎯 La promesa

**Hoy vas a abrir tu nombre, tu foto y tu música por dentro, y vas a descubrir
que las tres son la misma cosa: números.**

Y al final vas a construir con tus manos la pieza de la computadora que suma
esos números, sin escribir ni una sola vez el signo `+`.
""")
    md("""
### Cómo se usa

Presiona **`Shift + Enter`** en cada celda, **de arriba abajo y en orden**. Cada
sección usa lo que construiste en la anterior.

Cambia los números. Rompe las cosas. Vuelve a correr. No puedes descomponer nada.
""")
    forma('''
#@title 🔧 Prepara el taller  { display-mode: "form" }
# Corre esta celda y olvidala. Es el escenario, no la obra.
import importlib.util
import subprocess
import sys
import time

from ipywidgets import Widget
from matplotlib.axes import Axes
from plotly.graph_objects import Figure

if importlib.util.find_spec("shift_enter") is None:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                    "git+https://github.com/nrqrmz/shift-enter"], check=True)

from shift_enter import cifra, imagen, interruptores, paleta, sonido, torre
from shift_enter.binario import TABLA_DE_VALORES, a_binario, a_decimal
from shift_enter.interruptores import simbolo

paleta.aplicar_estilo()

# Silencia el eco de las celdas: una figura no debe imprimir su
# representación de texto debajo del dibujo que ya se guardó.
_ip = get_ipython()
if _ip is not None:
    _formateador = _ip.display_formatter.formatters["text/plain"]
    _formateador.for_type(Axes, lambda obj, p, ciclo: p.text(""))
    _formateador.for_type(Figure, lambda obj, p, ciclo: p.text(""))
    _formateador.for_type(Widget, lambda obj, p, ciclo: p.text(""))

print("Listo. La piedra esta encendida.")
''')
    md("**Corre esa celda antes que nada.** Trae las herramientas. Es el escenario, no la obra.")


def seccion_nombre():
    md("""
---

# 1 · Tu nombre ya está adentro

Escribe tu nombre. Está guardado en esta computadora ahorita mismo.

No como letras. Aquí adentro no hay letras. Solo hay números.
""")
    codigo('''
mi_nombre = "Ada"    # ← pon el tuyo

for letra in mi_nombre:
    print(letra, "→", ord(letra))
''')
    md("""
Ese número no es un apodo ni una traducción. **Es** la letra. Es lo único que
hay de tu nombre dentro de la máquina.

Y si tu nombre es una lista de números, entonces se puede escuchar.
""")
    codigo('''
sonido.reproducir(sonido.melodia_del_nombre(mi_nombre))
''')
    md("""
### 🔧 Prueba tú

Si una letra es un número, súmale 3 y mira qué sale.
""")
    codigo('''
def correr(texto, cuanto):
    salida = ""
    for letra in texto:
        salida = salida + chr(ord(letra) + cuanto)
    return salida


secreto = correr(mi_nombre, 3)
print("   cifrado:   ", secreto)
print("   descifrado:", correr(secreto, -3))
''')
    md("""
Julio César mandaba sus órdenes militares así, hace dos mil años. Le sumaba un
número a cada letra y sus enemigos veían basura.

Tú lo acabas de hacer con una suma.
""")
    md("""
### 🎯 El reto

Aquí hay un mensaje cifrado. Nadie te va a decir con qué número.

Arrastra el corrimiento hasta que el mensaje se vuelva español.
""")
    codigo('''
cifra.deslizador_disco(cifra.MENSAJE_RETO)
''')
    md("""
### 🤔 Para pensar

El espacio también se convirtió en otro símbolo cuando corriste las letras.

¿Por qué? ¿Qué número crees que es un espacio?
""")


def seccion_foto():
    md("""
---

# 2 · Tu foto es una tabla de números

Tu nombre era una lista. Una imagen es una tabla: un número por cada punto de
la pantalla.

Empieza al revés. En vez de abrir una foto, dibuja una escribiendo. Cada `#` es
un punto negro y cada `.` uno blanco.
""")
    codigo('''
mi_dibujo = """
..####..
.#....#.
#.#..#.#
#......#
#.#..#.#
#..##..#
.#....#.
..####..
"""

imagen.mostrar(imagen.desde_texto(mi_dibujo), titulo="lo que escribiste")
''')
    md("""
Cámbiale los puntos y los gatos. Dibuja lo tuyo y vuelve a correr la celda.

Los números no representan el dibujo. Los números **son** el dibujo.
""")
    md("""
### 🔧 Ahora la tuya

Sube una foto tuya. Si no quieres, no subas nada: el taller trae una de
repuesto y todo lo de abajo funciona igual.
""")
    codigo('''
imagen.selector()
''')
    md("""
Aquí está por dentro. **Pasa el mouse por encima** y vas a ver el número de cada
pixel. Acércate con dos dedos hasta que los puntos se vuelvan cuadrados.
""")
    codigo('''
imagen.mostrar_con_numeros(imagen.actual(), titulo="pasa el mouse por encima")
''')
    md("""
Si una foto es una tabla de números, entonces **editar una foto es hacer
aritmética**. Nada más.

Arrastra y mírala aclararse. Le estás sumando el mismo número a cada pixel.
""")
    codigo('''
imagen.deslizador_brillo(imagen.actual())
''')
    md("""
### Y ahora al revés

Sumarle a cada pixel lo aclara. Restarle lo oscurece.

¿Y si le restas cada pixel a 255? El negro se vuelve blanco, el blanco se vuelve
negro, y la foto se da la vuelta entera. Una resta.
""")
    codigo('''
imagen.mostrar(255 - imagen.actual(), titulo="la misma foto, al revés")
''')
    md("""
### El color son tres números

Hasta aquí todo fue gris, que es un número por punto. El color son tres:
cuánto rojo, cuánto verde y cuánto azul.

Con esos tres cabe cualquier color que hayas visto en una pantalla. Búscate uno.
""")
    codigo('''
imagen.mezclador_color()
''')


def seccion_musica():
    md("""
---

# 3 · Tu música es una lista de números

Un sonido es aire que empuja y jala tu tímpano. Si mides cuánto empuja, muchísimas
veces por segundo, te queda una lista de números.

Aquí está una, vista de muy cerca. Y escuchada.
""")
    codigo('''
la = sonido.onda(440)

sonido.dibujar_onda(la)
sonido.reproducir(la)
''')
    md("""
### 🔧 Prueba tú

Un solo número decide qué nota es. Arrástralo.
""")
    codigo('''
sonido.deslizador_de_tono()
''')
    md("""
### Y ahora rómpelo

Si el sonido es una lista, se le puede hacer lo que sea a una lista. Toma menos
números y sale más rápido. Léela del final al principio y sale al revés.
""")
    codigo('''
sonido.reproducir(sonido.a_velocidad(la, 2))
sonido.reproducir(sonido.al_reves(sonido.melodia_del_nombre(mi_nombre)))
''')
    md("""
### Y ahora súmalos

Tres sonidos. Súmalos como sumarías tres números.
""")
    codigo('''
do  = sonido.onda(261.63)
mi  = sonido.onda(329.63)
sol = sonido.onda(392.00)

acorde = do + mi + sol

sonido.dibujar_onda([do, mi, sol, acorde],
                    etiquetas=["do", "mi", "sol", "los tres sumados"],
                    muestras=600)
sonido.reproducir(acorde)
''')
    md("""
### Lo que llevas

Eso es un acorde de do mayor. No lo compusiste: lo **sumaste**.

Tu nombre, tu cara y ese acorde entraron a la máquina y se convirtieron en lo
mismo: listas de números.

Y a los tres les hiciste exactamente la misma cosa para cambiarlos. Le sumaste 3
a cada letra. Le sumaste 70 a cada pixel. Sumaste tres ondas.

Por eso una sola máquina puede tocar música, editar fotos y guardar mensajes. No
tiene tres talentos. Tiene uno.
""")


def seccion_piedra():
    md("""
---

# 4 · ¿Y cómo cabe todo eso en una piedra?

Toma un puñado de arena de playa. Es dióxido de silicio.

Derrítela. Purifícala hasta que de cada mil millones de átomos solo uno sea de
otra cosa. Te queda un cristal gris, aburrido, que no hace absolutamente nada.

Ahora graba en su superficie algo diminuto, miles de veces más delgado que un
cabello, que hace **una sola cosa**: deja pasar la electricidad, o no la deja.

Eso es un **transistor**. Un interruptor sin partes móviles.

En el aparato donde estás leyendo esto hay varios **miles de millones**. Ninguno
sabe sumar. Ninguno sabe leer. Solo están prendidos o apagados.
""")
    codigo('''
prendido = True    # este es un valor booleano
apagado  = False   # este es un valor booleano

print("Para la maquina no se llaman 'prendido' y 'apagado'. Se llaman 1 y 0.")
print("Y no es un apodo. Compruebalo:")
print()
print("   True  == 1   →", True == 1)
print("   False == 0   →", False == 0)
''')
    md("""
### Ocho interruptores

Un interruptor solo tiene dos estados, así que solo puede guardar 0 o 1. Con
ocho ya cabe cualquier número hasta 255.

El truco es que cada columna vale **el doble** que su vecina de la derecha. En
el sistema que ya usas cada columna vale diez veces más, y es diez solo porque
tenemos diez dedos. Por nada más.

**Préndelos con el dedo** y mira qué número sale.
""")
    codigo('''
interruptores.tablero(valor_inicial=42)
''')
    md("""
### Dale play

Ahora míralos contar solos, del 0 al 255. **Mira las columnas, no el número.**
""")
    codigo('''
interruptores.contador()
''')
    md("""
El interruptor de la derecha se prende y se apaga en cada número. El siguiente,
cada dos. El siguiente, cada cuatro.

Cada uno va exactamente al doble de lento que su vecino de la derecha. Eso es
todo lo que significa contar en binario.

En 1679 Gottfried Leibniz escribió esto en un papel, sin computadoras y sin
electricidad. Le pareció bello y ya. Fue un juguete inútil durante doscientos
setenta años, hasta que alguien conectó unos interruptores y descubrió que el
juguete era exactamente lo que la máquina necesitaba.
""")
    md("""
### Tu nombre, otra vez

En la §1 tu nombre era una lista de números. Así es como está guardado de verdad.
""")
    codigo('''
interruptores.dibujar_palabra(mi_nombre)
''')
    md("""
### Donde se acaban

Con ocho interruptores el número más grande que existe es este. No hay uno más.
""")
    codigo('''
interruptores.dibujar(a_binario(255), etiquetas=TABLA_DE_VALORES,
                      mostrar_bool=False, titulo="el mas grande que cabe")
''')
    md("""
### 🤔 Para pensar

¿Por qué justo 255, y no 256? ¿Y cuántos números distintos caben en ocho
interruptores, contando el cero?
""")


def seccion_sumador():
    md("""
---

# 5 · ¿Y quién suma allá abajo? Nadie

Todo lo que hiciste hoy fue sumar. Le sumaste 3 a cada letra. Le sumaste 70 a
cada pixel. Sumaste tres ondas y salió un acorde.

Y allá abajo, adentro de la piedra, no hay nadie que sepa sumar. Solo hay
interruptores.

Vamos a construir al que suma.
""")
    md("""
### Tres reglas

Un interruptor solo no sirve. Lo interesante empieza cuando conectas dos y
decides qué pasa con el de salida.

Hay tres formas de conectarlos que resultaron suficientes para construir el
mundo entero. Se llaman **compuertas**. Son tres `if`, y las escribes tú.
""")
    codigo('''
def NO(a):
    if a == apagado:
        return prendido
    else:
        return apagado

def Y(a, b):
    if a == prendido and b == prendido:
        return prendido
    else:
        return apagado

def O(a, b):
    if a == apagado and b == apagado:
        return apagado
    else:
        return prendido


interruptores.tabla_de_verdad("NO", NO, entradas=1)
interruptores.tabla_de_verdad("Y", Y)
interruptores.tabla_de_verdad("O", O)
''')
    md("""
Esas tablas son la definición completa de una compuerta. Ahí está *todo* lo que
puede pasar. No hay caso escondido.

Con esas tres se puede construir cualquier otra cosa que haga una computadora.
Cualquiera. Empecemos por una cuarta que se prende cuando los dos interruptores
son **distintos**.
""")
    codigo('''
def XOR(a, b):
    """Prendido solo si a y b son DISTINTOS.
    No es una pieza nueva: es NO, Y y O acomodadas de cierta forma."""
    return O( Y(a, NO(b)),
              Y(NO(a), b) )


interruptores.tabla_de_verdad("XOR", XOR)
''')
    md("""
### Las cuatro sumas que existen

Sumar un interruptor más un interruptor. Eso es todo lo que hay:

```
0 + 0 = 0
0 + 1 = 1
1 + 0 = 1
1 + 1 = 10     ← se pasa: escribe 0 y lleva 1
```

Mira la columna de la suma y la columna del llevo.
""")
    codigo('''
print("     a    b          suma   llevo")
print("   " + "─" * 32)
for a in (apagado, prendido):
    for b in (apagado, prendido):
        print(f"     {simbolo(a)}   {simbolo(b)}     →      {simbolo(XOR(a, b))}     {simbolo(Y(a, b))}")
''')
    md("""
La columna de la suma es **XOR**. La columna del llevo es **Y**.

Las dos piezas ya estaban en tu caja. Nadie las inventó para esto.
""")
    codigo('''
def medio_sumador(a, b):
    suma    = XOR(a, b)
    acarreo = Y(a, b)
    return suma, acarreo


def sumador_completo(a, b, llevo_que_entra):
    suma_parcial, acarreo_1 = medio_sumador(a, b)
    suma_final,   acarreo_2 = medio_sumador(suma_parcial, llevo_que_entra)
    return suma_final, O(acarreo_1, acarreo_2)
''')
    md("""
### Encadenarlos

Cuando sumas 47 + 38 a mano empiezas por la derecha, y lo que llevas cae en la
siguiente columna. Aquí pasa igual: cada columna recibe tres cosas, el bit de
arriba, el de abajo, y lo que le llegó de la columna anterior.

Ocho sumadores completos en fila, cada uno pasándole su llevo al siguiente. Eso
es, literalmente, una pieza que existe dentro de tu procesador.
""")
    codigo('''
def sumar(a, b, ancho=8):
    bits_a = a_binario(a, ancho)
    bits_b = a_binario(b, ancho)
    resultado = []
    llevo = apagado

    for i in reversed(range(ancho)):
        suma, llevo = sumador_completo(bits_a[i], bits_b[i], llevo)
        resultado.insert(0, suma)

    return resultado


interruptores.dibujar(sumar(13, 29), etiquetas=TABLA_DE_VALORES,
                      mostrar_bool=False, titulo="13 + 29")
''')
    codigo('''
print("Esos interruptores, leidos como numero:", a_decimal(sumar(13, 29)))
print()
print("Ese 42 salio de:")
print("   • ocho sumadores completos encadenados,")
print("   • cada uno hecho de dos medios sumadores y una compuerta O,")
print("   • cada medio sumador hecho de un XOR y un Y,")
print("   • el XOR hecho de NO, Y y O,")
print("   • y NO, Y y O son tres if.")
print()
print("En ningun punto de esa cadena aparece el signo +.")
print("Acabas de construir la parte de la computadora que suma. 🎯")
''')
    md("""
### ✅ Que se califique solo

Un sumador que acierta una vez pudo tener suerte. Que lo pruebe con **todas** las
sumas posibles de 0 a 127, y que se compare contra el `+` de Python.
""")
    codigo('''
aciertos = 0
for a in range(128):
    for b in range(128):
        if a_decimal(sumar(a, b)) == a + b:
            aciertos = aciertos + 1

print(f"✅ {aciertos:,} de 16,384 sumas correctas")
''')
    md("""
### 🔧 Adivina antes de correr

Con ocho interruptores no cabe nada mayor que 255.

¿Qué crees que va a pasar con `sumar(255, 1)`? Adivina, y luego corre la celda.
""")
    codigo('''
interruptores.dibujar(sumar(255, 1), etiquetas=TABLA_DE_VALORES,
                      mostrar_bool=False, titulo="255 + 1")
''')
    md("""
Todos apagados. Cero.

Eso se llama **desbordamiento**, y no es un detalle académico:

- En **Pac-Man**, el contador de niveles usaba ocho interruptores. Al llegar al
  nivel 256 se desbordó y media pantalla se convirtió en basura. Nadie pudo pasar
  de ahí durante años.
- En 1996 el cohete **Ariane 5** se autodestruyó 37 segundos después de despegar.
  Un número no cupo donde lo estaban metiendo. Costó 370 millones de dólares.

Tu sumador tiene exactamente el mismo límite que ellos. No porque esté mal hecho:
porque los interruptores se acaban.

### 🤔 Para pensar

Si un interruptor solo puede estar prendido o apagado, no hay dónde poner el
signo menos. ¿Cómo guardarías un número **negativo**?
""")


def seccion_torre():
    md("""
---

# 6 · Las capas

Tú escribiste `sumar` con compuertas. Python trae un `+` que ya venía hecho.

Hacen lo mismo. ¿Para qué existen los dos? Corre esto.
""")
    codigo('''
inicio = time.perf_counter()
for _ in range(300):
    sumar(13, 29)
tuyo = (time.perf_counter() - inicio) / 300

inicio = time.perf_counter()
for _ in range(300000):
    13 + 29
de_python = (time.perf_counter() - inicio) / 300000

print(f"   tu sumador:      {tuyo * 1e6:>10.1f} microsegundos")
print(f"   el + de Python:  {de_python * 1e6:>10.4f} microsegundos")
print()
print(f"   El tuyo es unas {tuyo / de_python:,.0f} veces mas lento.")
''')
    md("""
### Por qué

Tu sumador **simula** compuertas usando software, que a su vez corre sobre
compuertas de verdad grabadas en silicio, que hacen la misma operación miles de
millones de veces por segundo.

Construiste una computadora dentro de una computadora. Por eso es lenta, y por
eso valió la pena: pudiste verla por dentro.

El `+` de Python no es más listo que el tuyo. Solo está más abajo en la torre.
""")
    codigo('''
torre.dibujar()
''')
    md("""
### Lo que se aprende bajando

Cada capa de esa torre existe por una sola razón: **para que no tengas que pensar
en la de abajo**.

El que escribe un videojuego no piensa en transistores. El que diseña
transistores no piensa en videojuegos. Y así funciona todo, hasta el día que algo
se rompe y alguien tiene que saber bajar.

Hoy bajaste hasta el fondo. Abriste tu nombre, tu cara y tu música, tocaste el
interruptor, lo conectaste, le enseñaste a contar, le enseñaste a sumar, y
volviste a subir.

La piedra ya cuenta.
""")
    md("""
---

## 🤔 Y sin embargo

Tu sumador no ha hecho nada por su cuenta.

Se quedó ahí, quieto, esperando a que tú corrieras la celda. Sabe sumar, pero no
sabe **cuándo** sumar, ni **qué** sumar, ni qué hacer después.

Le falta algo que no es una compuerta ni un número:

> Una receta. Alguien que le diga qué hacer, y en qué orden.

Eso es la siguiente presentación: **la venida del proceso**.
""")


def construir(ruta="la-piedra-que-aprendio-a-contar.ipynb"):
    cuaderno = nbf.v4.new_notebook(cells=CELDAS)
    cuaderno.metadata.update({
        "colab": {"provenance": [], "toc_visible": True},
        "kernelspec": {"display_name": "Python 3 (ipykernel)",
                       "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12.9",
                          "file_extension": ".py", "mimetype": "text/x-python",
                          "nbconvert_exporter": "python",
                          "pygments_lexer": "ipython3",
                          "codemirror_mode": {"name": "ipython", "version": 3}},
    })
    nbf.write(cuaderno, ruta)
    print(f"escritas {len(CELDAS)} celdas en {ruta}")


if __name__ == "__main__":
    portada()
    seccion_nombre()
    seccion_foto()
    seccion_musica()
    seccion_piedra()
    seccion_sumador()
    seccion_torre()
    construir()
