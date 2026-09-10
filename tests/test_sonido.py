import numpy as np
import pytest

from shift_enter import paleta, sonido


def test_la_onda_dura_lo_que_le_pides():
    assert len(sonido.onda(440, segundos=2.0)) == sonido.MUESTREO * 2


def test_la_onda_tiene_la_frecuencia_pedida():
    arreglo = sonido.onda(440, segundos=1.0)
    espectro = np.abs(np.fft.rfft(arreglo))
    pico = np.fft.rfftfreq(len(arreglo), 1 / sonido.MUESTREO)[espectro.argmax()]
    assert abs(pico - 440) < 2


def test_al_doble_de_velocidad_dura_la_mitad():
    arreglo = sonido.onda(440, segundos=1.0)
    assert len(sonido.a_velocidad(arreglo, 2)) == len(arreglo) // 2


def test_al_reves_invierte():
    arreglo = np.array([1.0, 2.0, 3.0])
    assert list(sonido.al_reves(arreglo)) == [3.0, 2.0, 1.0]


def test_la_melodia_dura_una_nota_por_letra():
    melodia = sonido.melodia_del_nombre("Ada", segundos_por_letra=0.1)
    assert len(melodia) == 3 * int(sonido.MUESTREO * 0.1)


def test_la_melodia_de_un_texto_vacio_no_revienta():
    assert len(sonido.melodia_del_nombre("")) >= 1


def test_dibujar_onda_pinta_una_linea_por_onda():
    figura = sonido._dibujar_onda([sonido.onda(440, 0.1), sonido.onda(880, 0.1)],
                                  etiquetas=["la", "la agudo"])
    assert len(figura.data) == 2


def test_dibujar_onda_nombra_cada_onda_con_su_etiqueta():
    figura = sonido._dibujar_onda([sonido.onda(440, 0.1), sonido.onda(880, 0.1)],
                                  etiquetas=["la", "la agudo"])
    assert [traza.name for traza in figura.data] == ["la", "la agudo"]


def test_dibujar_onda_recorta_a_las_muestras_pedidas():
    figura = sonido._dibujar_onda(sonido.onda(440, 1.0), muestras=120)
    assert len(figura.data[0].x) == 120


def test_dibujar_onda_mide_el_eje_en_segundos():
    figura = sonido._dibujar_onda(sonido.onda(440, 1.0), muestras=120)
    assert figura.data[0].x[1] == pytest.approx(1 / sonido.MUESTREO)


def test_la_ultima_onda_resalta_sobre_las_que_la_forman():
    # La ultima de la lista es el resultado: en el acorde, la suma. Tiene que
    # dominar el dibujo en vez de perderse entre sus propios sumandos.
    do, mi = sonido.onda(261.63, 0.1), sonido.onda(329.63, 0.1)
    figura = sonido._dibujar_onda([do, mi, do + mi],
                                  etiquetas=["do", "mi", "los dos sumados"])
    suma = figura.data[-1]
    assert suma.line.color == paleta.ENCENDIDO
    assert suma.line.width > figura.data[0].line.width


def test_dibujar_onda_lee_las_cuatro_ondas_de_un_solo_jalon():
    # El pago de la seccion: el mouse en un instante muestra los valores de
    # todas las ondas a la vez, y ahi se ve que los sumandos dan el resultado.
    figura = sonido._dibujar_onda([sonido.onda(440, 0.1), sonido.onda(880, 0.1)],
                                  etiquetas=["la", "la agudo"])
    assert figura.layout.hovermode == "x unified"


def test_deslizador_de_tono_no_deja_cuadro_fijo_antes_del_widget(monkeypatch):
    llamadas = []
    monkeypatch.setattr(sonido, "dibujar_onda", lambda *a, **k: llamadas.append((a, k)))
    monkeypatch.setattr(sonido, "reproducir", lambda *a, **k: None)
    sonido.deslizador_de_tono()
    assert len(llamadas) == 0
