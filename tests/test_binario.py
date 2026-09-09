import pytest

from shift_enter.binario import TABLA_DE_VALORES, NoCabe, a_binario, a_decimal


def test_a_binario_y_a_decimal_son_inversas_en_todo_el_rango():
    for n in range(256):
        assert a_decimal(a_binario(n)) == n


def test_a_binario_devuelve_booleanos():
    bits = a_binario(5)
    assert bits == [False, False, False, False, False, True, False, True]
    assert all(isinstance(bit, bool) for bit in bits)


def test_a_binario_respeta_el_ancho():
    assert a_binario(3, ancho=4) == [False, False, True, True]


def test_a_binario_avisa_cuando_no_cabe():
    with pytest.raises(NoCabe, match="9 interruptores"):
        a_binario(256)


def test_a_binario_avisa_con_negativos():
    with pytest.raises(NoCabe, match="negativo"):
        a_binario(-1)


def test_a_decimal_acepta_unos_y_ceros():
    assert a_decimal([1, 0, 1]) == 5


def test_tabla_de_valores():
    assert TABLA_DE_VALORES == [128, 64, 32, 16, 8, 4, 2, 1]
