from shift_enter import paleta


def test_la_paleta_tiene_los_cuatro_colores():
    assert paleta.ENCENDIDO == "#f5c518"
    assert paleta.APAGADO == "#2b2b2b"
    assert paleta.BORDE == "#8a8a8a"
    assert paleta.TENUE == "0.45"


def test_la_paleta_trae_una_secuencia_para_las_ondas():
    assert len(paleta.COLORES_ONDA) >= 3
    assert all(color.startswith("#") for color in paleta.COLORES_ONDA)
    assert paleta.ENCENDIDO not in paleta.COLORES_ONDA


def test_aplicar_estilo_deja_matplotlib_sin_cuadricula():
    import matplotlib.pyplot as plt

    plt.rcParams["axes.grid"] = True
    paleta.aplicar_estilo()
    assert plt.rcParams["axes.grid"] is False
    assert plt.rcParams["font.size"] == 12
