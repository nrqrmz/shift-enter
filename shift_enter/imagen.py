"""Una imagen es una tabla de numeros."""

from importlib import resources
from io import BytesIO

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from IPython.display import display
from ipywidgets import interact
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


_SUBIDA = {"arreglo": None}


def _recordar(arreglo):
    _SUBIDA["arreglo"] = arreglo


def olvidar():
    """Vuelve a la foto de respaldo."""
    _SUBIDA["arreglo"] = None


def actual():
    """La foto del alumno si ya subio una, o la de respaldo."""
    return _SUBIDA["arreglo"] if _SUBIDA["arreglo"] is not None else de_respaldo()


def selector():
    """El boton para subir tu propia foto. No bloquea si nadie sube nada."""
    subir = widgets.FileUpload(accept="image/*", multiple=False,
                               description="sube tu foto")
    aviso = widgets.HTML("Mientras no subas nada, trabajas con la foto de respaldo.")

    def recibir(cambio):
        archivos = cambio["new"]
        if not archivos:
            return
        crudo = (archivos[0]["content"] if isinstance(archivos, (list, tuple))
                 else list(archivos.values())[0]["content"])
        _recordar(np.array(Image.open(BytesIO(bytes(crudo))).convert("L"), dtype=np.uint8))
        aviso.value = "Listo. Vuelve a correr las celdas de abajo y va a salir tu cara."

    subir.observe(recibir, names="value")
    display(widgets.VBox([subir, aviso]))
    return subir


def mostrar_con_numeros(arreglo, titulo=None):
    """La foto por dentro. Pasa el mouse y lee el numero de cada pixel."""
    figura = px.imshow(arreglo, color_continuous_scale="gray", zmin=0, zmax=255,
                       title=titulo)
    figura.update_traces(
        hovertemplate="fila %{y}, columna %{x}<br><b>%{z}</b><extra></extra>")
    figura.update_layout(coloraxis_showscale=False, dragmode="zoom",
                         margin=dict(l=10, r=10, t=45, b=10))
    figura.show()
    return figura


def deslizador_brillo(arreglo):
    """Sumale un numero a cada pixel y mira que pasa."""
    # Un cuadro fijo antes del widget: el estado de los widgets no se guarda,
    # asi que sin esto la celda se ve vacia para quien lee en GitHub.
    mostrar(arreglo, titulo="foto + (0)")

    @interact(brillo=widgets.IntSlider(min=-150, max=150, value=0, description="+"))
    def _(brillo):
        mostrar(mas_brillo(arreglo, brillo), titulo=f"foto + ({brillo})")


def _dibujar_muestra(rojo, verde, azul):
    """Un rectangulo pintado de un solo color. Version interna."""
    _, eje = plt.subplots(figsize=(4, 2.4))
    eje.add_patch(plt.Rectangle((0, 0), 1, 1,
                                facecolor=(rojo / 255, verde / 255, azul / 255)))
    eje.set_xlim(0, 1)
    eje.set_ylim(0, 1)
    eje.axis("off")
    eje.set_title(f"[{rojo}, {verde}, {azul}]", family="monospace")
    plt.tight_layout()
    plt.show()


def mezclador_color():
    """Cualquier color del mundo, con tres numeros."""
    # Un cuadro fijo antes del widget: el estado de los widgets no se guarda,
    # asi que sin esto la celda se ve vacia para quien lee en GitHub.
    _dibujar_muestra(200, 90, 30)

    @interact(rojo=widgets.IntSlider(min=0, max=255, value=200, description="rojo"),
              verde=widgets.IntSlider(min=0, max=255, value=90, description="verde"),
              azul=widgets.IntSlider(min=0, max=255, value=30, description="azul"))
    def _(rojo, verde, azul):
        _dibujar_muestra(rojo, verde, azul)
