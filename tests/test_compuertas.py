from shift_enter import compuertas
from shift_enter.binario import a_decimal


def test_not_invierte():
    assert compuertas.NOT(False) is True
    assert compuertas.NOT(True) is False


def test_and_solo_se_prende_con_los_dos():
    assert compuertas.AND(True, True) is True
    assert compuertas.AND(True, False) is False
    assert compuertas.AND(False, True) is False
    assert compuertas.AND(False, False) is False


def test_or_se_prende_con_cualquiera():
    assert compuertas.OR(True, True) is True
    assert compuertas.OR(True, False) is True
    assert compuertas.OR(False, True) is True
    assert compuertas.OR(False, False) is False


def test_xor_se_prende_solo_con_distintos():
    assert compuertas.XOR(True, False) is True
    assert compuertas.XOR(False, True) is True
    assert compuertas.XOR(True, True) is False
    assert compuertas.XOR(False, False) is False


def test_las_compuertas_devuelven_booleanos_de_verdad():
    # 'and' y 'or' de Python devuelven el operando, no un booleano.
    assert compuertas.AND(1, 0) is False
    assert compuertas.OR(0, 2) is True


def test_el_medio_sumador_lleva_uno_solo_cuando_los_dos_estan_prendidos():
    assert compuertas.medio_sumador(False, False) == (False, False)
    assert compuertas.medio_sumador(True, False) == (True, False)
    assert compuertas.medio_sumador(False, True) == (True, False)
    assert compuertas.medio_sumador(True, True) == (False, True)


def test_el_sumador_completo_suma_tres_interruptores():
    assert compuertas.sumador_completo(True, True, True) == (True, True)
    assert compuertas.sumador_completo(True, True, False) == (False, True)
    assert compuertas.sumador_completo(True, False, True) == (False, True)
    assert compuertas.sumador_completo(False, False, False) == (False, False)


def test_sumar_acierta_las_dieciseis_mil_sumas():
    aciertos = sum(1 for a in range(128) for b in range(128)
                   if a_decimal(compuertas.sumar(a, b)) == a + b)
    assert aciertos == 128 * 128


def test_sumar_devuelve_ocho_interruptores():
    assert len(compuertas.sumar(13, 29)) == 8


def test_sumar_se_desborda_en_doscientos_cincuenta_y_seis():
    assert a_decimal(compuertas.sumar(255, 1)) == 0


def test_tabla_de_verdad_de_una_entrada_tiene_dos_casos():
    eje = compuertas._tabla_de_verdad("NOT", compuertas.NOT, entradas=1)
    assert len(eje.patches) == 4  # dos entradas y dos salidas


def test_tabla_de_verdad_de_dos_entradas_tiene_cuatro_casos():
    eje = compuertas._tabla_de_verdad("AND", compuertas.AND)
    assert len(eje.patches) == 12  # ocho entradas y cuatro salidas


def test_tabla_de_verdad_resalta_el_renglon_vigente():
    eje = compuertas._tabla_de_verdad("AND", compuertas.AND, resaltar=(True, True))
    resaltados = [p for p in eje.patches if getattr(p, "get_linewidth", None)
                  and p.get_linewidth() > 2]
    assert resaltados != []


def test_tabla_de_verdad_sin_resaltar_no_resalta_nada():
    eje = compuertas._tabla_de_verdad("AND", compuertas.AND)
    resaltados = [p for p in eje.patches if getattr(p, "get_linewidth", None)
                  and p.get_linewidth() > 2]
    assert resaltados == []


def test_tabla_de_verdad_publica_no_devuelve_nada():
    assert compuertas.tabla_de_verdad("NOT", compuertas.NOT, entradas=1) is None
