import matplotlib
matplotlib.use("Agg")

from shift_enter import interruptores


def test_como_html_pinta_prendidos_y_apagados():
    html = interruptores.como_html([True, False])
    assert interruptores.ENCENDIDO_HTML in html
    assert interruptores.APAGADO_HTML in html


def test_como_html_muestra_las_etiquetas():
    html = interruptores.como_html([True], etiquetas=[128])
    assert "128" in html


def test_el_tablero_arranca_en_el_valor_pedido():
    botones, marcador = interruptores._tablero(valor_inicial=5)
    assert len(botones) == 8
    assert [b.value for b in botones] == [False, False, False, False, False, True, False, True]
    assert "5" in marcador.value


def test_el_tablero_reacciona_cuando_prendes_uno():
    botones, marcador = interruptores._tablero(valor_inicial=0)
    botones[0].value = True          # la columna de 128
    assert "128" in marcador.value


def test_el_contador_va_de_cero_a_doscientos_cincuenta_y_cinco():
    reproductor, deslizador, salida = interruptores._contador()
    assert reproductor.min == 0 and reproductor.max == 255
    deslizador.value = 255
    assert "255" in salida.value


def test_tablero_devuelve_none():
    resultado = interruptores.tablero(valor_inicial=0)
    assert resultado is None


def test_contador_devuelve_none():
    resultado = interruptores.contador()
    assert resultado is None


def test_los_juguetes_dejan_un_cuadro_fijo_antes_del_widget(monkeypatch):
    dibujados = []
    monkeypatch.setattr(interruptores, "dibujar",
                        lambda *a, **k: dibujados.append(a))
    interruptores.tablero(valor_inicial=5)
    interruptores.contador()
    assert len(dibujados) == 2
