"""Interruptores: dibujados, y prendibles con el dedo."""

import threading
import time

import ipywidgets as widgets
import matplotlib.pyplot as plt
from IPython.display import display

from .binario import TABLA_DE_VALORES, NoCabe, a_binario, a_decimal
from .paleta import APAGADO, BORDE, ENCENDIDO, TENUE

PRENDIDO = "●"
APAGADO_SIMBOLO = "○"
ENCENDIDO_HTML = ENCENDIDO
APAGADO_HTML = APAGADO


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
        plt.show()
    return ax


def dibujar_palabra(texto, ax=None):
    """Cada letra de un texto, en ocho interruptores, todas en una figura."""
    letras = list(texto)
    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(9.5, 0.95 * len(letras) + 0.8))

    for fila, letra in enumerate(letras):
        y = -fila
        numero = ord(letra)
        try:
            bits = a_binario(numero)
        except NoCabe as no_cabe:
            # El caracter no se dibuja: si no cabe en ocho interruptores,
            # tampoco hay glifo para el en la fuente, y mandarlo hace que
            # matplotlib avise. Se ensena el numero y el porque.
            ax.text(-1.2, y, str(numero), ha="right", va="center",
                    fontsize=12, family="monospace")
            ax.text(0, y, str(no_cabe), ha="left", va="center",
                    fontsize=11, color=TENUE)
            continue
        ax.text(-1.2, y, f"{letra}   →   {numero}", ha="right", va="center",
                fontsize=12, family="monospace")
        for i, bit in enumerate(bits):
            ax.add_patch(plt.Circle((i, y), 0.33, zorder=2, linewidth=1.5,
                                    facecolor=ENCENDIDO if bit else APAGADO,
                                    edgecolor=BORDE))

    for i, valor in enumerate(TABLA_DE_VALORES):
        ax.text(i, 0.85, str(valor), ha="center", va="center",
                fontsize=9, color=TENUE)

    ax.set_xlim(-5.2, 7.7)
    ax.set_ylim(-len(letras) + 0.3, 1.3)
    ax.set_aspect("equal")
    ax.axis("off")
    if propia:
        plt.tight_layout()
        plt.show()
    return ax


def como_html(bits, etiquetas=None):
    """Los interruptores como circulos de HTML. Se actualiza al instante."""
    piezas = []
    for i, bit in enumerate(bits):
        color = ENCENDIDO_HTML if bit else APAGADO_HTML
        etiqueta = "" if etiquetas is None else str(etiquetas[i])
        piezas.append(
            f"<div style='display:inline-block;text-align:center;margin:0 6px'>"
            f"<div style='font-size:11px;color:#777'>{etiqueta}</div>"
            f"<div style='width:38px;height:38px;border-radius:50%;"
            f"background:{color};border:2px solid {BORDE}'></div>"
            f"<div style='font-family:monospace;font-weight:bold'>{int(bool(bit))}</div>"
            f"</div>"
        )
    return "<div>" + "".join(piezas) + "</div>"


def _marcador(bits):
    numero = a_decimal(bits)
    partes = " + ".join(str(v) for b, v in zip(bits, TABLA_DE_VALORES) if b)
    return (f"{como_html(bits, TABLA_DE_VALORES)}"
            f"<div style='font-size:40px;font-weight:bold;margin-top:8px'>{numero}</div>"
            f"<div style='color:#777'>{partes or 'ningún interruptor prendido'}</div>")


def _tablero(valor_inicial=0):
    """Construye ocho interruptores que prendes con el dedo. Version interna."""
    botones = [widgets.ToggleButton(value=v, description=str(valor),
                                    layout=widgets.Layout(width="60px"))
               for v, valor in zip(a_binario(valor_inicial), TABLA_DE_VALORES)]
    marcador = widgets.HTML()

    def actualizar(_=None):
        marcador.value = _marcador([b.value for b in botones])

    for boton in botones:
        boton.observe(actualizar, names="value")
    actualizar()
    return botones, marcador


def tablero(valor_inicial=0):
    """Ocho interruptores que prendes con el dedo."""
    botones, marcador = _tablero(valor_inicial)
    display(widgets.VBox([widgets.HBox(botones), marcador]))


def _siguiente(valor, desde, hasta):
    """El numero que sigue, dando la vuelta al llegar al tope."""
    return desde if valor + 1 > hasta else valor + 1


def _contador(desde=0, hasta=255, ms=200):
    """Construye el contador con su boton de play. Version interna."""
    deslizador = widgets.IntSlider(value=desde, min=desde, max=hasta,
                                   description="número",
                                   layout=widgets.Layout(width="620px"))
    play = widgets.ToggleButton(value=False, description="play", icon="play",
                                layout=widgets.Layout(width="100px"))
    salida = widgets.HTML()

    def pintar(cambio):
        n = cambio["new"]
        salida.value = (f"{como_html(a_binario(n), TABLA_DE_VALORES)}"
                        f"<div style='font-size:40px;font-weight:bold'>{n}</div>")

    deslizador.observe(pintar, names="value")
    pintar({"new": desde})

    def avanzar():
        # ipywidgets no trae un boton de play solo: el suyo son tres botones
        # pegados. Este hilo es lo que lo sustituye. Es demonio, asi que no
        # deja al kernel colgado si alguien cierra la pestana con el play
        # prendido.
        while play.value:
            deslizador.value = _siguiente(deslizador.value, desde, hasta)
            time.sleep(ms / 1000)

    def al_presionar(cambio):
        if cambio["new"]:
            play.description, play.icon = "pausa", "pause"
            threading.Thread(target=avanzar, daemon=True).start()
        else:
            play.description, play.icon = "play", "play"

    play.observe(al_presionar, names="value")
    return play, deslizador, salida


def contador(desde=0, hasta=255, ms=200):
    """Miralos contar solos, del 0 al 255."""
    play, deslizador, salida = _contador(desde, hasta, ms)
    display(widgets.VBox([widgets.HBox([play, deslizador]), salida]))
