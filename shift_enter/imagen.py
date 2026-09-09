"""Una imagen es una tabla de numeros."""

from importlib import resources

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def de_respaldo():
    """La foto de Leibniz, empacada dentro del paquete."""
    with resources.files("shift_enter").joinpath("datos/leibniz.jpg").open("rb") as archivo:
        return np.array(Image.open(archivo).convert("L"), dtype=np.uint8)


def desde_texto(dibujo):
    """Convierte un texto de puntos y gatos en una tabla de numeros."""
    filas = [linea.strip() for linea in dibujo.strip().splitlines()]
    ancho = max(len(fila) for fila in filas)
    return np.array([[0 if letra == "#" else 255 for letra in fila.ljust(ancho, ".")]
                     for fila in filas], dtype=np.uint8)


def mas_brillo(arreglo, cuanto):
    """Sumarle un numero a cada pixel, sin salirse de 0 y 255."""
    return np.clip(arreglo.astype(int) + cuanto, 0, 255).astype(np.uint8)


def mostrar(arreglo, titulo=None, ax=None):
    """La imagen, sin ejes ni adornos."""
    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(5, 6))
    ax.imshow(arreglo, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    ax.axis("off")
    if titulo:
        ax.set_title(titulo)
    if propia:
        plt.tight_layout()
        plt.show()
    return ax
