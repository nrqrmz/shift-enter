"""La torre de capas, de la arena hasta esta celda."""

import time

import matplotlib.pyplot as plt

from .compuertas import sumar

LAS_CAPAS = [
    ("Arena y electricidad", "física. Aquí no hay ideas todavía"),
    ("Transistor", "un interruptor sin partes móviles"),
    ("Compuerta", "NOT, AND, OR        ← lo armaste en la parte 5"),
    ("Bit", "prendido o apagado  ← parte 4"),
    ("Byte", "ocho bits: un número, una letra, un pixel  ← partes 1, 2 y 4"),
    ("Sumador", "13 + 29 = 42        ← parte 5"),
    ("Instrucción", "lo único que el procesador entiende"),
    ("Python", "el + que usaste sin pensarlo"),
    ("Esta celda", "aquí estás tú"),
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


def _comparar_velocidad(a=13, b=29, veces=300):
    """Mide los dos sumadores y devuelve los segundos de cada uno. Version interna."""
    inicio = time.perf_counter()
    for _ in range(veces):
        sumar(a, b)
    tuyo = (time.perf_counter() - inicio) / veces

    muchas = veces * 1000
    inicio = time.perf_counter()
    for _ in range(muchas):
        a + b
    de_python = (time.perf_counter() - inicio) / muchas

    return tuyo, de_python


def comparar_velocidad(a=13, b=29, veces=300):
    """Cronometra el sumador de compuertas contra el + que trae Python."""
    tuyo, de_python = _comparar_velocidad(a, b, veces)
    print(f"   tu sumador:      {tuyo * 1e6:>10.1f} microsegundos")
    print(f"   el + de Python:  {de_python * 1e6:>10.4f} microsegundos")
    print()
    print(f"   El tuyo es unas {tuyo / de_python:,.0f} veces más lento.")
