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

if importlib.util.find_spec("shift_enter") is None:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                    "git+https://github.com/nrqrmz/shift-enter"], check=True)

from shift_enter import cifra, imagen, interruptores, paleta, sonido, torre
from shift_enter.binario import TABLA_DE_VALORES, a_binario, a_decimal
from shift_enter.interruptores import simbolo

paleta.aplicar_estilo()

# Silencia el eco de las celdas: una figura no debe imprimir su
# representación de texto debajo del dibujo que ya se guardó.
from ipywidgets import Widget
from matplotlib.axes import Axes
from plotly.graph_objects import Figure

_ip = get_ipython()
if _ip is not None:
    _formateador = _ip.display_formatter.formatters["text/plain"]
    _formateador.for_type(Axes, lambda obj, p, ciclo: p.text(""))
    _formateador.for_type(Figure, lambda obj, p, ciclo: p.text(""))
    _formateador.for_type(Widget, lambda obj, p, ciclo: p.text(""))

print("Listo. La piedra esta encendida.")
''')
    md("**Corre esa celda antes que nada.** Trae las herramientas. Es el escenario, no la obra.")


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
    construir()
