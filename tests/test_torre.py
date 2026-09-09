from shift_enter import torre


def test_la_torre_tiene_nueve_capas():
    assert len(torre.LAS_CAPAS) == 9


def test_la_torre_empieza_en_la_arena_y_acaba_en_el_alumno():
    assert torre.LAS_CAPAS[0][0] == "Arena y electricidad"
    assert torre.LAS_CAPAS[-1][0] == "Esta celda"


def test_dibujar_pinta_un_rectangulo_por_capa():
    eje = torre.dibujar()
    assert len(eje.patches) == 9
