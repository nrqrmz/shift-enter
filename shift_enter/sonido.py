"""Sonido: una lista de numeros que se puede escuchar."""

import ipywidgets as widgets
import numpy as np
import plotly.express as px
from IPython.display import Audio, display
from ipywidgets import interact

from shift_enter import paleta

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


def _dibujar_onda(ondas, etiquetas=None, muestras=300):
    """Construye la figura de un sonido visto de cerca. Version interna."""
    if not isinstance(ondas, (list, tuple)):
        ondas = [ondas]
    con_leyenda = etiquetas is not None
    if not con_leyenda:
        etiquetas = [f"onda {i + 1}" for i in range(len(ondas))]

    datos = {"segundos": [], "amplitud": [], "onda": []}
    for etiqueta, arreglo in zip(etiquetas, ondas):
        recorte = np.asarray(arreglo)[:muestras]
        datos["segundos"].extend(np.arange(len(recorte)) / MUESTREO)
        datos["amplitud"].extend(recorte)
        datos["onda"].extend([etiqueta] * len(recorte))

    # La ultima onda es el resultado, y se lleva el color de lo encendido.
    colores = {etiqueta: paleta.COLORES_ONDA[i % len(paleta.COLORES_ONDA)]
               for i, etiqueta in enumerate(etiquetas)}
    colores[etiquetas[-1]] = paleta.ENCENDIDO

    figura = px.line(datos, x="segundos", y="amplitud", color="onda",
                     color_discrete_map=colores,
                     category_orders={"onda": list(etiquetas)})
    figura.update_traces(line_width=1.6, hovertemplate="%{y:.2f}")
    figura.update_traces(selector={"name": etiquetas[-1]}, line_width=3)
    figura.update_layout(hovermode="x unified", showlegend=con_leyenda,
                         legend_title_text="", yaxis_title=None,
                         margin=dict(l=10, r=10, t=30, b=10), height=340)
    return figura


def dibujar_onda(ondas, etiquetas=None, muestras=300):
    """Un sonido, visto de muy cerca. En la leyenda se prende y se apaga."""
    _dibujar_onda(ondas, etiquetas, muestras).show()


def deslizador_de_tono():
    """Arrastra los hertz y escucha el cambio."""
    @interact(hz=widgets.IntSlider(min=110, max=1760, step=10, value=440,
                                   description="Hz"))
    def _(hz):
        print(f"   Cambiaste un solo número: {hz}")
        reproducir(onda(hz))
