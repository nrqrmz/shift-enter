"""Interruptores: dibujados, y prendibles con el dedo."""

import matplotlib.pyplot as plt

from .binario import TABLA_DE_VALORES, NoCabe, a_binario
from .paleta import APAGADO, BORDE, ENCENDIDO, TENUE

PRENDIDO = "●"
APAGADO_SIMBOLO = "○"


def simbolo(estado):
    """Un interruptor, en texto. Acepta True/False o 1/0."""
    return PRENDIDO if estado else APAGADO_SIMBOLO


def dibujar(bits, etiquetas=None, titulo=None, mostrar_bool=True, ax=None):
    """Dibuja uno o varios interruptores como focos."""
    if not isinstance(bits, (list, tuple)):
        bits = [bits]
    bits = [int(bool(b)) for b in bits]
    n = len(bits)

    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(1.05 * n + 0.6, 2.4 if mostrar_bool else 2.0))

    for i, b in enumerate(bits):
        ax.add_patch(plt.Circle((i, 0), 0.36, zorder=2, linewidth=1.6,
                                facecolor=ENCENDIDO if b else APAGADO, edgecolor=BORDE))
        ax.text(i, -0.72, str(b), ha="center", va="center",
                fontsize=15, weight="bold", family="monospace")
        if mostrar_bool:
            ax.text(i, -1.10, "True" if b else "False", ha="center", va="center",
                    fontsize=9, color=TENUE, family="monospace")
        if etiquetas is not None:
            ax.text(i, 0.68, str(etiquetas[i]), ha="center", va="center",
                    fontsize=10, color="0.35")

    ax.set_xlim(-0.7, n - 0.3)
    ax.set_ylim(-1.45 if mostrar_bool else -1.1, 1.0)
    ax.set_aspect("equal")
    ax.axis("off")
    if titulo:
        ax.set_title(titulo, fontsize=13, pad=10)
    if propia:
        plt.tight_layout()
        if plt.get_backend().lower() != 'agg':
            plt.show()
    return ax


def tabla_de_verdad(nombre, compuerta, entradas=2):
    """Todo lo que puede pasar con una compuerta, dibujado."""
    if entradas == 1:
        casos = [(a,) for a in (False, True)]
        encabezados = ["a"]
    else:
        casos = [(a, b) for a in (False, True) for b in (False, True)]
        encabezados = ["a", "b"]

    salida_x = len(encabezados) * 0.85 + 0.75
    figura, ax = plt.subplots(figsize=(salida_x + 1.3, 0.85 * len(casos) + 1.2))

    for j, h in enumerate(encabezados):
        ax.text(j * 0.85, 0.85, h, ha="center", fontsize=12, color="0.35")
    ax.text(salida_x, 0.85, nombre, ha="center", fontsize=12, weight="bold")

    for fila, caso in enumerate(casos):
        y = -fila
        for j, v in enumerate(caso):
            ax.add_patch(plt.Circle((j * 0.85, y), 0.28, zorder=2, linewidth=1.4,
                                    facecolor=ENCENDIDO if v else APAGADO, edgecolor=BORDE))
        ax.text(salida_x - 0.75, y, "→", ha="center", va="center",
                fontsize=15, color=TENUE)
        s = compuerta(*caso)
        ax.add_patch(plt.Circle((salida_x, y), 0.28, zorder=2, linewidth=1.4,
                                facecolor=ENCENDIDO if s else APAGADO, edgecolor=BORDE))

    ax.set_xlim(-0.55, salida_x + 0.55)
    ax.set_ylim(-len(casos) + 0.1, 1.25)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    if plt.get_backend().lower() != 'agg':
        plt.show()
    return figura


def dibujar_palabra(texto):
    """Cada letra de un texto, en ocho interruptores."""
    for letra in texto:
        numero = ord(letra)
        try:
            bits = a_binario(numero)
        except NoCabe as no_cabe:
            print(f"   {letra}  →  {numero}   {no_cabe}")
            continue
        dibujar(bits, etiquetas=TABLA_DE_VALORES, mostrar_bool=False,
                titulo=f"{letra}   →   {numero}")
