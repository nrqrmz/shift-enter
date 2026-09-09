import matplotlib
matplotlib.use("Agg")
import numpy as np

from shift_enter import imagen


def test_sin_subir_nada_la_actual_es_la_de_respaldo():
    imagen.olvidar()
    assert np.array_equal(imagen.actual(), imagen.de_respaldo())


def test_la_foto_subida_reemplaza_a_la_de_respaldo():
    imagen.olvidar()
    imagen._recordar(imagen.desde_texto("#."))
    assert imagen.actual().shape == (1, 2)
    imagen.olvidar()


def test_mostrar_con_numeros_devuelve_una_figura_de_plotly():
    figura = imagen.mostrar_con_numeros(imagen.desde_texto("#."))
    assert figura.data[0].type == "heatmap"


def test_mostrar_con_numeros_ensena_el_valor_al_pasar_el_mouse():
    figura = imagen.mostrar_con_numeros(imagen.desde_texto("#."))
    assert "%{z}" in figura.data[0].hovertemplate


def test_el_selector_acepta_imagenes():
    subir = imagen.selector()
    assert subir.accept == "image/*"
    assert subir.multiple is False


def test_deslizador_brillo_deja_un_cuadro_fijo_antes_del_widget(monkeypatch):
    llamadas = []
    monkeypatch.setattr(imagen, "mostrar", lambda *a, **k: llamadas.append((a, k)))
    arreglo = imagen.desde_texto("#.")
    imagen.deslizador_brillo(arreglo)
    # Dos llamadas: el cuadro fijo explicito y el render inicial de @interact
    # (que tambien dibuja con brillo 0, el valor por defecto del deslizador).
    # Si se borra la linea del cuadro fijo, solo queda una.
    assert len(llamadas) == 2


def test_mezclador_color_deja_un_cuadro_fijo_antes_del_widget(monkeypatch):
    llamadas = []
    monkeypatch.setattr(imagen, "_dibujar_muestra", lambda *a, **k: llamadas.append((a, k)))
    imagen.mezclador_color()
    # Dos llamadas: el cuadro fijo explicito y el render inicial de @interact
    # (que tambien dibuja con los valores por defecto de los deslizadores).
    # Si se borra la linea del cuadro fijo, solo queda una.
    assert len(llamadas) == 2
