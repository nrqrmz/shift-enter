import threading
import time

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
    play, deslizador, salida = interruptores._contador()
    assert deslizador.min == 0 and deslizador.max == 255
    deslizador.value = 255
    assert "255" in salida.value


def test_el_deslizador_del_contador_es_ancho():
    play, deslizador, salida = interruptores._contador()
    assert deslizador.layout.width == "620px"


def test_el_contador_trae_un_solo_boton_de_play():
    play, deslizador, salida = interruptores._contador()
    assert play.description == "play"
    assert play.value is False


def test_el_boton_dice_pausa_mientras_corre():
    play, deslizador, salida = interruptores._contador(ms=20)
    play.value = True
    try:
        assert play.description == "pausa"
    finally:
        play.value = False
    assert play.description == "play"

    for _ in range(100):
        vivos = [hilo for hilo in threading.enumerate()
                 if hilo.name == interruptores.HILO_DEL_CONTADOR and hilo.is_alive()]
        if not vivos:
            break
        time.sleep(0.02)
    assert vivos == []


def test_el_contador_da_la_vuelta_al_llegar_al_tope():
    assert interruptores._siguiente(254, 0, 255) == 255
    assert interruptores._siguiente(255, 0, 255) == 0
    assert interruptores._siguiente(0, 0, 255) == 1


def test_al_presionar_play_varias_veces_no_se_acumulan_hilos():
    # Un doble clic dejaba dos hilos avanzando el mismo deslizador.
    play, deslizador, salida = interruptores._contador(ms=20)
    for _ in range(5):
        play.value = True
        play.value = False

    for _ in range(100):
        vivos = [hilo for hilo in threading.enumerate()
                 if hilo.name == interruptores.HILO_DEL_CONTADOR and hilo.is_alive()]
        if not vivos:
            break
        time.sleep(0.02)

    assert vivos == []


def test_solo_un_hilo_avanza_mientras_el_play_esta_prendido():
    play, deslizador, salida = interruptores._contador(ms=20)
    play.value = True
    play.value = False
    play.value = True
    time.sleep(0.1)
    try:
        vivos = [hilo for hilo in threading.enumerate()
                 if hilo.name == interruptores.HILO_DEL_CONTADOR and hilo.is_alive()]
        assert len(vivos) == 1
    finally:
        play.value = False


def test_tablero_devuelve_none():
    resultado = interruptores.tablero(valor_inicial=0)
    assert resultado is None


def test_contador_devuelve_none():
    resultado = interruptores.contador()
    assert resultado is None


def test_los_juguetes_no_dejan_cuadro_fijo_antes_del_widget(monkeypatch):
    # Colab es el unico blanco: la celda se corre siempre, asi que ya no hay
    # que dibujar nada para quien la lea sin ejecutarla.
    dibujados = []
    monkeypatch.setattr(interruptores, "dibujar",
                        lambda *a, **k: dibujados.append(a))
    interruptores.tablero(valor_inicial=5)
    interruptores.contador()
    assert dibujados == []
