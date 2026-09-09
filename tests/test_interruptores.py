import matplotlib
matplotlib.use("Agg")

from shift_enter import interruptores
from shift_enter.binario import TABLA_DE_VALORES


def test_simbolo_distingue_prendido_de_apagado():
    assert interruptores.simbolo(True) == "●"
    assert interruptores.simbolo(False) == "○"
    assert interruptores.simbolo(1) == "●"


def test_dibujar_acepta_un_solo_interruptor():
    eje = interruptores.dibujar(True)
    assert eje is not None


def test_dibujar_pinta_un_circulo_por_bit():
    eje = interruptores.dibujar([True, False, True], etiquetas=[4, 2, 1])
    assert len(eje.patches) == 3


def test_tabla_de_verdad_de_una_entrada_tiene_dos_casos():
    figura = interruptores.tabla_de_verdad("NO", lambda a: not a, entradas=1)
    ejes = figura.axes[0]
    assert len(ejes.patches) == 4  # dos entradas y dos salidas


def test_dibujar_palabra_no_revienta_con_un_emoji():
    interruptores.dibujar_palabra("A\U0001faa8")


def test_la_tabla_de_valores_sigue_siendo_de_ocho():
    assert len(TABLA_DE_VALORES) == 8
