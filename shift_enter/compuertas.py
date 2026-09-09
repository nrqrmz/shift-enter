"""Las tres reglas con las que se construye todo lo demas, y el sumador.

Esto es plomeria a proposito. La notebook es de descubrimiento: el alumno
todavia no ha visto una funcion, asi que arma el sumador con el dedo sobre
los widgets de este modulo, no escribiendo estas lineas.
"""

import ipywidgets as widgets
import matplotlib.pyplot as plt
from IPython.display import display

from .binario import a_binario
from .paleta import APAGADO, BORDE, ENCENDIDO, TENUE

PRENDIDO = True
APAGADO_LOGICO = False


def NOT(a):
    """Prendido cuando la entrada esta apagada."""
    return not a


def AND(a, b):
    """Prendido solo cuando las dos entradas estan prendidas."""
    return bool(a) and bool(b)


def OR(a, b):
    """Prendido cuando al menos una entrada esta prendida."""
    return bool(a) or bool(b)


def XOR(a, b):
    """Prendido solo si a y b son DISTINTOS.

    No es una pieza nueva: es NOT, AND y OR acomodadas de cierta forma.
    """
    return OR(AND(a, NOT(b)),
              AND(NOT(a), b))


def medio_sumador(a, b):
    """Suma dos interruptores. Devuelve (suma, llevo)."""
    return XOR(a, b), AND(a, b)


def sumador_completo(a, b, llevo_que_entra):
    """Suma dos interruptores mas el llevo de la columna anterior."""
    suma_parcial, acarreo_1 = medio_sumador(a, b)
    suma_final, acarreo_2 = medio_sumador(suma_parcial, llevo_que_entra)
    return suma_final, OR(acarreo_1, acarreo_2)


def sumar(a, b, ancho=8):
    """Ocho sumadores completos en fila. Devuelve la lista de bits."""
    bits_a = a_binario(a, ancho)
    bits_b = a_binario(b, ancho)
    resultado = []
    llevo = APAGADO_LOGICO

    for i in reversed(range(ancho)):
        suma, llevo = sumador_completo(bits_a[i], bits_b[i], llevo)
        resultado.insert(0, suma)

    return resultado


def _casos(entradas):
    if entradas == 1:
        return [(a,) for a in (False, True)], ["a"]
    return [(a, b) for a in (False, True) for b in (False, True)], ["a", "b"]


def _tabla_de_verdad(nombre, compuerta, entradas=2, resaltar=None, ax=None):
    """Todo lo que puede pasar con una compuerta. Version interna."""
    casos, encabezados = _casos(entradas)
    salida_x = len(encabezados) * 0.85 + 0.75

    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(salida_x + 1.3, 0.85 * len(casos) + 1.2))

    for j, h in enumerate(encabezados):
        ax.text(j * 0.85, 0.85, h, ha="center", fontsize=12, color="0.35")
    ax.text(salida_x, 0.85, nombre, ha="center", fontsize=12, weight="bold")

    for fila, caso in enumerate(casos):
        y = -fila
        vigente = resaltar is not None and tuple(bool(v) for v in resaltar) == caso
        grosor = 3.2 if vigente else 1.4
        for j, v in enumerate(caso):
            ax.add_patch(plt.Circle((j * 0.85, y), 0.28, zorder=2, linewidth=grosor,
                                    facecolor=ENCENDIDO if v else APAGADO,
                                    edgecolor=BORDE))
        ax.text(salida_x - 0.75, y, "→", ha="center", va="center",
                fontsize=15, color=TENUE)
        s = compuerta(*caso)
        ax.add_patch(plt.Circle((salida_x, y), 0.28, zorder=2, linewidth=grosor,
                                facecolor=ENCENDIDO if s else APAGADO,
                                edgecolor=BORDE))

    ax.set_xlim(-0.55, salida_x + 0.55)
    ax.set_ylim(-len(casos) + 0.1, 1.25)
    ax.set_aspect("equal")
    ax.axis("off")
    if propia:
        plt.tight_layout()
    return ax


def tabla_de_verdad(nombre, compuerta, entradas=2, resaltar=None):
    """Todo lo que puede pasar con una compuerta, dibujado."""
    _tabla_de_verdad(nombre, compuerta, entradas, resaltar)
    plt.show()


def _panel_compuertas(a, b):
    """Las tres tablas de verdad, con el renglon vigente iluminado."""
    figura, ejes = plt.subplots(1, 3, figsize=(11, 4.2))
    _tabla_de_verdad("NOT", NOT, entradas=1, resaltar=(a,), ax=ejes[0])
    _tabla_de_verdad("AND", AND, resaltar=(a, b), ax=ejes[1])
    _tabla_de_verdad("OR", OR, resaltar=(a, b), ax=ejes[2])
    plt.tight_layout()
    return figura


def _probador():
    """Construye el probador de compuertas. Version interna."""
    a = widgets.ToggleButton(value=False, description="a",
                             layout=widgets.Layout(width="70px"))
    b = widgets.ToggleButton(value=False, description="b",
                             layout=widgets.Layout(width="70px"))
    salida = widgets.Output()

    def pintar(_=None):
        with salida:
            salida.clear_output(wait=True)
            _panel_compuertas(a.value, b.value)
            plt.show()

    a.observe(pintar, names="value")
    b.observe(pintar, names="value")
    pintar()
    return a, b, salida


def probador():
    """Prende los dos interruptores y mira las tres compuertas a la vez."""
    a, b, salida = _probador()
    display(widgets.VBox([widgets.HBox([a, b]), salida]))


def _cable(ax, puntos, vivo):
    """Un cable. Encendido si esta conduciendo, apagado si no."""
    xs = [p[0] for p in puntos]
    ys = [p[1] for p in puntos]
    ax.plot(xs, ys, linewidth=2.6 if vivo else 1.6,
            color=ENCENDIDO if vivo else BORDE, zorder=1,
            solid_capstyle="round")


def _caja(ax, x, y, texto, vivo):
    """Una compuerta, dibujada como caja rotulada."""
    ax.add_patch(plt.Rectangle((x - 0.62, y - 0.42), 1.24, 0.84, zorder=2,
                               linewidth=1.8, facecolor="white",
                               edgecolor=ENCENDIDO if vivo else BORDE))
    ax.text(x, y, texto, ha="center", va="center", zorder=3,
            fontsize=11, weight="bold", family="monospace")


def _foco(ax, x, y, valor, etiqueta):
    """Un interruptor con su rotulo y su cero o su uno."""
    ax.add_patch(plt.Circle((x, y), 0.3, zorder=3, linewidth=1.6,
                            facecolor=ENCENDIDO if valor else APAGADO,
                            edgecolor=BORDE))
    ax.text(x, y + 0.55, etiqueta, ha="center", va="center",
            fontsize=11, color=TENUE)
    ax.text(x, y - 0.62, str(int(bool(valor))), ha="center", va="center",
            fontsize=12, weight="bold", family="monospace")


def _dibujar_xor(a, b, ax=None):
    """El cableado del XOR, con la corriente encendida por donde pasa."""
    a, b = bool(a), bool(b)
    no_a, no_b = NOT(a), NOT(b)
    arriba = AND(a, no_b)
    abajo = AND(no_a, b)
    salida = OR(arriba, abajo)

    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(10, 4.6))

    _foco(ax, 0, 3.2, a, "a")
    _foco(ax, 0, 0.4, b, "b")

    _caja(ax, 2.2, 1.0, "NOT", no_b)
    _caja(ax, 2.2, 2.6, "NOT", no_a)
    _caja(ax, 4.6, 3.2, "AND", arriba)
    _caja(ax, 4.6, 0.4, "AND", abajo)
    _caja(ax, 7.0, 1.8, "OR", salida)

    _cable(ax, [(0.3, 3.2), (3.98, 3.2)], a)
    _cable(ax, [(0.3, 0.4), (1.2, 0.4), (1.2, 1.0), (1.58, 1.0)], b)
    _cable(ax, [(2.82, 1.0), (3.4, 1.0), (3.4, 2.95), (3.98, 2.95)], no_b)
    _cable(ax, [(0.3, 3.2), (1.2, 3.2), (1.2, 2.6), (1.58, 2.6)], a)
    _cable(ax, [(2.82, 2.6), (3.4, 2.6), (3.4, 0.65), (3.98, 0.65)], no_a)
    _cable(ax, [(0.3, 0.4), (3.98, 0.4)], b)
    _cable(ax, [(5.22, 3.2), (5.9, 3.2), (5.9, 2.0), (6.38, 2.0)], arriba)
    _cable(ax, [(5.22, 0.4), (5.9, 0.4), (5.9, 1.6), (6.38, 1.6)], abajo)
    _cable(ax, [(7.62, 1.8), (8.6, 1.8)], salida)

    _foco(ax, 8.9, 1.8, salida, "XOR")

    ax.set_xlim(-0.9, 9.9)
    ax.set_ylim(-0.9, 4.2)
    ax.set_aspect("equal")
    ax.axis("off")
    if propia:
        plt.tight_layout()
    return ax


def _diagrama_xor():
    """Construye el diagrama vivo del XOR. Version interna."""
    a = widgets.ToggleButton(value=False, description="a",
                             layout=widgets.Layout(width="70px"))
    b = widgets.ToggleButton(value=False, description="b",
                             layout=widgets.Layout(width="70px"))
    salida = widgets.Output()

    def pintar(_=None):
        with salida:
            salida.clear_output(wait=True)
            _dibujar_xor(a.value, b.value)
            plt.show()

    a.observe(pintar, names="value")
    b.observe(pintar, names="value")
    pintar()
    return a, b, salida


def diagrama_xor():
    """Mueve los interruptores y mira por donde pasa la corriente."""
    a, b, salida = _diagrama_xor()
    display(widgets.VBox([widgets.HBox([a, b]), salida]))
