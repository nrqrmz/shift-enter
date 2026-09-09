"""El disco cifrador de Julio Cesar."""

import ipywidgets as widgets
import matplotlib.pyplot as plt
from ipywidgets import interact

from .paleta import ENCENDIDO, TENUE

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DESPLAZAMIENTO_RETO = 5
MENSAJE_RETO = "QF%UNJIWF%^F%HZJSYF"


def _corrido(texto, cuanto):
    return "".join(chr(ord(letra) + cuanto) for letra in texto)


def disco(mensaje, desplazamiento, ax=None):
    """Las dos tiras del alfabeto y el mensaje descifrandose."""
    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(13, 3.4))

    abajo = ALFABETO[desplazamiento % 26:] + ALFABETO[:desplazamiento % 26]
    for i, (arriba_letra, abajo_letra) in enumerate(zip(ALFABETO, abajo)):
        ax.text(i, 1.0, arriba_letra, ha="center", va="center",
                fontsize=13, family="monospace", color=TENUE)
        ax.text(i, 0.45, abajo_letra, ha="center", va="center",
                fontsize=13, family="monospace", weight="bold")
    ax.text(-1.6, 1.0, "cifrado", ha="right", va="center", fontsize=10, color=TENUE)
    ax.text(-1.6, 0.45, "de verdad", ha="right", va="center", fontsize=10, color=TENUE)

    ax.text(12.5, -0.55, _corrido(mensaje, -desplazamiento), ha="center", va="center",
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
    """Arrastra el desplazamiento y mira el mensaje volverse espanol."""
    # Un cuadro fijo antes del widget: el estado de los widgets no se guarda,
    # asi que sin esto la celda se ve vacia para quien lee en GitHub.
    disco(mensaje, 0)

    @interact(desplazamiento=widgets.IntSlider(min=0, max=25, value=0,
                                               description="corrimiento"))
    def _(desplazamiento):
        disco(mensaje, desplazamiento)
