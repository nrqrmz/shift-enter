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
    construir()
