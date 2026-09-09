"""Las tres reglas con las que se construye todo lo demas, y el sumador.

Esto es plomeria a proposito. La notebook es de descubrimiento: el alumno
todavia no ha visto una funcion, asi que arma el sumador con el dedo sobre
los widgets de este modulo, no escribiendo estas lineas.
"""

import matplotlib.pyplot as plt

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
