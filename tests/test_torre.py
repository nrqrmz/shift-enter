import matplotlib.pyplot as plt

from shift_enter import torre


def test_la_torre_tiene_nueve_capas():
    assert len(torre.LAS_CAPAS) == 9


def test_la_torre_empieza_en_la_arena_y_acaba_en_el_alumno():
    assert torre.LAS_CAPAS[0][0] == "Arena y electricidad"
    assert torre.LAS_CAPAS[-1][0] == "Esta celda"


def test_dibujar_pinta_un_rectangulo_por_capa():
    eje = torre.dibujar()
    assert len(eje.patches) == 9
    plt.close("all")


def test_la_torre_no_usa_simbolos_de_parrafo():
    for nombre, detalle in torre.LAS_CAPAS:
        assert "§" not in nombre
        assert "§" not in detalle


def test_la_torre_nombra_las_compuertas_como_se_llaman_de_verdad():
    detalles = " ".join(detalle for _, detalle in torre.LAS_CAPAS)
    assert "NOT, AND, OR" in detalles


def test_la_torre_manda_al_alumno_a_las_partes_por_su_nombre():
    detalles = " ".join(detalle for _, detalle in torre.LAS_CAPAS)
    assert "parte 5" in detalles
    assert "parte 4" in detalles


def test_comparar_velocidad_devuelve_dos_tiempos():
    tuyo, de_python = torre._comparar_velocidad(veces=5)
    assert tuyo > 0
    assert de_python > 0


def test_el_sumador_a_mano_es_mas_lento_que_el_de_python():
    tuyo, de_python = torre._comparar_velocidad(veces=20)
    assert tuyo > de_python


def test_comparar_velocidad_no_devuelve_nada():
    # Si devolviera los tiempos, la celda de la notebook los imprimiria como
    # tupla cruda debajo de la comparacion que lee el alumno.
    assert torre.comparar_velocidad(veces=5) is None
