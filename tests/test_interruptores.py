import warnings

import matplotlib.pyplot as plt

from shift_enter import interruptores
from shift_enter.binario import TABLA_DE_VALORES


def test_simbolo_distingue_prendido_de_apagado():
    assert interruptores.simbolo(True) == "●"
    assert interruptores.simbolo(False) == "○"
    assert interruptores.simbolo(1) == "●"


def test_dibujar_acepta_un_solo_interruptor():
    eje = interruptores.dibujar(True)
    assert eje is not None
    plt.close("all")


def test_dibujar_pinta_un_circulo_por_bit():
    eje = interruptores.dibujar([True, False, True], etiquetas=[4, 2, 1])
    assert len(eje.patches) == 3
    plt.close("all")


def test_dibujar_palabra_deja_todas_las_letras_en_una_sola_figura():
    eje = interruptores.dibujar_palabra("Fernanda")
    # Ocho letras por ocho interruptores cada una.
    assert len(eje.patches) == 8 * 8
    plt.close("all")


def test_dibujar_palabra_rotula_cada_letra_con_su_numero():
    eje = interruptores.dibujar_palabra("Ab")
    textos = [t.get_text() for t in eje.texts]
    assert "A   →   65" in textos
    assert "b   →   98" in textos
    plt.close("all")


def test_dibujar_palabra_no_revienta_con_un_emoji():
    eje = interruptores.dibujar_palabra("A\U0001faa8")
    textos = [t.get_text() for t in eje.texts]
    assert any("no cabe" in t or "interruptores" in t for t in textos)
    plt.close("all")


def test_dibujar_palabra_no_manda_a_la_fuente_un_caracter_sin_glifo():
    figura, eje = plt.subplots()
    interruptores.dibujar_palabra("A\U0001faa8", ax=eje)
    textos = [t.get_text() for t in eje.texts]
    assert not any("\U0001faa8" in texto for texto in textos)
    assert any("interruptores" in texto for texto in textos)
    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)
        figura.canvas.draw()
    plt.close("all")


def test_la_tabla_de_valores_sigue_siendo_de_ocho():
    assert len(TABLA_DE_VALORES) == 8
