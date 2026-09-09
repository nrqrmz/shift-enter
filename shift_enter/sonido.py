"""Sonido: una lista de numeros que se puede escuchar."""

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Audio, display
from ipywidgets import interact

MUESTREO = 22050


def onda(hz, segundos=2.0):
    """Una onda pura de la frecuencia que pidas."""
    t = np.linspace(0, segundos, int(MUESTREO * segundos), endpoint=False)
    return np.sin(2 * np.pi * hz * t)


def reproducir(arreglo):
    """Pone el reproductor de audio debajo de la celda."""
    display(Audio(arreglo, rate=MUESTREO))


def a_velocidad(arreglo, factor):
    """Mas rapido o mas lento: se toman menos o mas muestras."""
    indices = np.arange(0, len(arreglo), factor)
    return np.interp(indices, np.arange(len(arreglo)), arreglo)


def al_reves(arreglo):
    """La misma lista de numeros, leida del final al principio."""
    return np.ascontiguousarray(np.asarray(arreglo)[::-1])


def melodia_del_nombre(texto, segundos_por_letra=0.35):
    """Cada letra es un numero, cada numero es una nota."""
    if not texto:
        return np.zeros(1)
    notas = [onda(110 * 2 ** ((ord(letra) % 24) / 12), segundos_por_letra)
             for letra in texto]
    return np.concatenate(notas)


def dibujar_onda(ondas, etiquetas=None, muestras=300, ax=None):
    """Un sonido, visto de muy cerca."""
    if not isinstance(ondas, (list, tuple)):
        ondas = [ondas]
    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(11, 2.5))
    for i, arreglo in enumerate(ondas):
        etiqueta = None if etiquetas is None else etiquetas[i]
        ax.plot(np.arange(min(muestras, len(arreglo))) / MUESTREO,
                arreglo[:muestras], linewidth=1.5, label=etiqueta)
    if etiquetas is not None:
        ax.legend(loc="upper right", fontsize=9)
    ax.set_xlabel("segundos")
    if propia:
        plt.tight_layout()
        if plt.get_backend().lower() != 'agg':
            plt.show()
    return ax


def deslizador_de_tono():
    """Arrastra los hertz y escucha el cambio."""
    # Un cuadro fijo antes del widget: el estado de los widgets no se guarda,
    # asi que sin esto la celda se ve vacia para quien lee en GitHub.
    dibujar_onda(onda(440), etiquetas=["440 Hz"])

    @interact(hz=widgets.IntSlider(min=110, max=1760, step=10, value=440,
                                   description="Hz"))
    def _(hz):
        print(f"   Cambiaste un solo numero: {hz}")
        reproducir(onda(hz))
