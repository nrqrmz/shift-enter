"""La torre de capas, de la arena hasta esta celda."""

import matplotlib.pyplot as plt

LAS_CAPAS = [
    ("Arena y electricidad", "fisica. Aqui no hay ideas todavia"),
    ("Transistor", "un interruptor sin partes moviles"),
    ("Compuerta", "NO, Y, O            ← lo construiste en §5"),
    ("Bit", "prendido o apagado  ← §4"),
    ("Byte", "ocho bits: un numero, una letra, un pixel  ← §1, §2 y §4"),
    ("Sumador", "13 + 29 = 42        ← §5"),
    ("Instruccion", "lo unico que el procesador entiende"),
    ("Python", "el + que usaste sin pensarlo"),
    ("Esta celda", "aqui estas tu"),
]


def dibujar(capas=None, ax=None):
    """La torre completa, de abajo hacia arriba."""
    capas = LAS_CAPAS if capas is None else capas
    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(11, 7))

    for i, (nombre, detalle) in enumerate(capas):
        tono = 0.94 - i * 0.055
        ax.add_patch(plt.Rectangle((0, i), 10, 0.86, facecolor=str(tono),
                                   edgecolor="white", linewidth=2))
        color = "black" if tono > 0.5 else "white"
        ax.text(0.25, i + 0.43, nombre, va="center", ha="left",
                fontsize=13, weight="bold", color=color)
        ax.text(3.6, i + 0.43, detalle, va="center", ha="left",
                fontsize=10.5, color=color)

    ax.set_xlim(0, 10)
    ax.set_ylim(-0.3, len(capas) + 0.2)
    ax.axis("off")
    ax.set_title("La torre", fontsize=15, pad=15)
    if propia:
        plt.tight_layout()
        plt.show()
    return ax
