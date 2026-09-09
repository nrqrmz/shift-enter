"""El disco cifrador de Julio Cesar."""

import ipywidgets as widgets
import matplotlib.pyplot as plt
from ipywidgets import interact

from .paleta import ENCENDIDO, TENUE

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SALTO_RETO = 5
MENSAJE_RETO = "QF%UNJIWF%^F%HZJSYF"

# El espacio cifrado es '%'. Al restarle ciertos saltos cae en caracteres de
# control, que la fuente no sabe dibujar y que hacen que matplotlib avise
# "Glyph 20 missing from font". El mensaje tiene que seguir corriendose
# completo, porque de ahi sale la pregunta que cierra la parte 1, asi que la
# correccion va aqui, al pintar.
SIN_DIBUJO = "▯"


def correr(texto, salto):
    """Le suma el salto al numero de cada letra."""
    return "".join(chr(ord(letra) + salto) for letra in texto)


def _imprimible(texto):
    """Cambia por un recuadro cualquier caracter que la fuente no dibuje."""
    return "".join(letra if 32 <= ord(letra) < 127 else SIN_DIBUJO
                   for letra in texto)


def _deslizador_de_salto():
    """El deslizador del salto, ancho y rotulado en espanol de Mexico."""
    return widgets.IntSlider(min=0, max=25, value=0, description="salto",
                             continuous_update=False,
                             layout=widgets.Layout(width="620px"))


def disco(mensaje, salto, ax=None):
    """Las dos tiras del alfabeto y el mensaje descifrandose."""
    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(13, 3.8))

    abajo = ALFABETO[salto % 26:] + ALFABETO[:salto % 26]
    for i, (arriba_letra, abajo_letra) in enumerate(zip(ALFABETO, abajo)):
        ax.text(i, 1.0, arriba_letra, ha="center", va="center",
                fontsize=13, family="monospace", color=TENUE)
        ax.text(i, 0.45, abajo_letra, ha="center", va="center",
                fontsize=13, family="monospace", weight="bold")
    ax.text(-1.6, 1.0, "cifrado", ha="right", va="center", fontsize=10, color=TENUE)
    ax.text(-1.6, 0.45, "de verdad", ha="right", va="center", fontsize=10, color=TENUE)

    ax.text(-1.6, -0.55, f"salto: {salto}", ha="right", va="center",
            fontsize=15, weight="bold", family="monospace")

    ax.text(12.5, -0.55, _imprimible(correr(mensaje, -salto)),
            ha="center", va="center",
            fontsize=22, family="monospace", weight="bold", color=ENCENDIDO,
            bbox=dict(facecolor="#2b2b2b", edgecolor="none", pad=10))

    ax.set_xlim(-6, 27)
    ax.set_ylim(-1.2, 1.5)
    ax.axis("off")
    if propia:
        plt.tight_layout()
        plt.show()
    return ax


def deslizador_disco(mensaje):
    """Arrastra el salto y mira el mensaje volverse espanol."""
    @interact(salto=_deslizador_de_salto())
    def _(salto):
        disco(mensaje, salto)
