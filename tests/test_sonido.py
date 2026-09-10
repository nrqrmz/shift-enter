import matplotlib.pyplot as plt
import numpy as np

from shift_enter import sonido


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
    eje = sonido.dibujar_onda([sonido.onda(440, 0.1), sonido.onda(880, 0.1)],
                              etiquetas=["la", "la agudo"])
    assert len(eje.lines) == 2
    plt.close("all")


def test_deslizador_de_tono_no_deja_cuadro_fijo_antes_del_widget(monkeypatch):
    llamadas = []
    monkeypatch.setattr(sonido, "dibujar_onda", lambda *a, **k: llamadas.append((a, k)))
    monkeypatch.setattr(sonido, "reproducir", lambda *a, **k: None)
    sonido.deslizador_de_tono()
    assert len(llamadas) == 0
