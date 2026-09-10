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
    figura = imagen._mostrar_con_numeros(imagen.desde_texto("#."))
    assert figura.data[0].type == "heatmap"


def test_mostrar_con_numeros_ensena_el_valor_al_pasar_el_mouse():
    figura = imagen._mostrar_con_numeros(imagen.desde_texto("#."))
    assert "%{z}" in figura.data[0].hovertemplate


def test_mostrar_con_numeros_no_devuelve_nada():
    assert imagen.mostrar_con_numeros(imagen.desde_texto("#.")) is None


def test_el_selector_acepta_imagenes():
    subir = imagen.selector()
    assert subir.accept == "image/*"
    assert subir.multiple is False


def test_deslizador_brillo_no_deja_cuadro_fijo_antes_del_widget(monkeypatch):
    llamadas = []
    monkeypatch.setattr(imagen, "mostrar", lambda *a, **k: llamadas.append((a, k)))
    arreglo = imagen.desde_texto("#.")
    imagen.deslizador_brillo(arreglo)
    # Una sola llamada: el render inicial de @interact. Colab es el unico
    # blanco, asi que ya no se dibuja nada para quien lea sin ejecutar.
    assert len(llamadas) == 1


def test_mezclador_color_no_deja_cuadro_fijo_antes_del_widget(monkeypatch):
    llamadas = []
    monkeypatch.setattr(imagen, "_dibujar_muestra", lambda *a, **k: llamadas.append((a, k)))
    imagen.mezclador_color()
    assert len(llamadas) == 1
