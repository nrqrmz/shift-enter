import matplotlib
matplotlib.use("Agg")
import numpy as np

from shift_enter import imagen


def test_la_foto_de_respaldo_viene_en_el_paquete():
    foto = imagen.de_respaldo()
    assert foto.ndim == 2
    assert foto.dtype == np.uint8
    assert foto.shape[0] > 100 and foto.shape[1] > 100


def test_desde_texto_convierte_gatos_en_negro():
    dibujo = """
    .#.
    ###
    """
    tabla = imagen.desde_texto(dibujo)
    assert tabla.shape == (2, 3)
    assert tabla[0, 0] == 255
    assert tabla[0, 1] == 0
    assert list(tabla[1]) == [0, 0, 0]


def test_desde_texto_rellena_las_filas_cortas():
    tabla = imagen.desde_texto("##\n#")
    assert tabla.shape == (2, 2)
    assert tabla[1, 1] == 255


def test_mas_brillo_no_se_pasa_de_255():
    tabla = np.array([[200, 10]], dtype=np.uint8)
    assert list(imagen.mas_brillo(tabla, 100)[0]) == [255, 110]


def test_mas_brillo_no_baja_de_cero():
    tabla = np.array([[200, 10]], dtype=np.uint8)
    assert list(imagen.mas_brillo(tabla, -100)[0]) == [100, 0]


def test_mostrar_pinta_la_imagen():
    eje = imagen.mostrar(imagen.desde_texto("#."), titulo="prueba")
    assert len(eje.images) == 1
