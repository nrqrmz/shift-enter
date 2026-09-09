"""De numeros a interruptores y de vuelta."""

TABLA_DE_VALORES = [128, 64, 32, 16, 8, 4, 2, 1]


class NoCabe(ValueError):
    """El numero necesita mas interruptores de los que hay."""


def a_binario(n, ancho=8):
    """Recibe un numero. Devuelve una lista de True y False, uno por interruptor."""
    if n < 0:
        raise NoCabe(f"{n} es negativo, y en un interruptor no hay dónde poner el signo menos.")
    if n >= 2 ** ancho:
        raise NoCabe(f"{n} necesita {n.bit_length()} interruptores y solo tienes {ancho}.")
    return [bool((n >> (ancho - 1 - i)) & 1) for i in range(ancho)]


def a_decimal(bits):
    """Recibe interruptores. Devuelve cuanto valen leidos como numero."""
    valor = 0
    for bit in bits:
        valor = valor * 2 | int(bool(bit))
    return valor
