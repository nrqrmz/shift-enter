"""Interruptores: dibujados, y prendibles con el dedo."""

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
            f"<div style='color:#777'>{partes or 'ningun interruptor prendido'}</div>")


def tablero(valor_inicial=0):
    """Ocho interruptores que prendes con el dedo."""
    botones = [widgets.ToggleButton(value=v, description=str(valor),
                                    layout=widgets.Layout(width="60px"))
               for v, valor in zip(a_binario(valor_inicial), TABLA_DE_VALORES)]
    marcador = widgets.HTML()

    def actualizar(_=None):
        marcador.value = _marcador([b.value for b in botones])

    for boton in botones:
        boton.observe(actualizar, names="value")
    actualizar()
    # Un cuadro fijo antes del widget: el estado de los widgets no se guarda,
    # asi que sin esto la celda se ve vacia para quien lee en GitHub.
    dibujar(a_binario(valor_inicial), etiquetas=TABLA_DE_VALORES, mostrar_bool=False,
            titulo=f"empieza en {valor_inicial}")
    display(widgets.VBox([widgets.HBox(botones), marcador]))
    return botones, marcador


def contador(desde=0, hasta=255, ms=200):
    """El boton de play contando en binario."""
    reproductor = widgets.Play(value=desde, min=desde, max=hasta, interval=ms)
    deslizador = widgets.IntSlider(value=desde, min=desde, max=hasta, description="numero")
    widgets.link((reproductor, "value"), (deslizador, "value"))
    salida = widgets.HTML()

    def pintar(cambio):
        n = cambio["new"]
        salida.value = (f"{como_html(a_binario(n), TABLA_DE_VALORES)}"
                        f"<div style='font-size:40px;font-weight:bold'>{n}</div>")

    deslizador.observe(pintar, names="value")
    pintar({"new": desde})
    dibujar(a_binario(desde), etiquetas=TABLA_DE_VALORES, mostrar_bool=False,
            titulo=f"empieza en {desde}")
    display(widgets.VBox([widgets.HBox([reproductor, deslizador]), salida]))
    return reproductor, deslizador, salida
