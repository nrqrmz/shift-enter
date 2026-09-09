from pathlib import Path

import matplotlib.pyplot as plt

from shift_enter import cifra


def test_correr_le_suma_el_salto_a_cada_letra():
    assert cifra.correr("ABC", 1) == "BCD"
    assert cifra.correr("BCD", -1) == "ABC"


def test_correr_ida_y_vuelta_regresa_al_original():
    assert cifra.correr(cifra.correr("Fernanda", 7), -7) == "Fernanda"


def test_el_mensaje_del_reto_se_descifra_con_su_salto():
    assert cifra.correr(cifra.MENSAJE_RETO, -cifra.SALTO_RETO) == "LA PIEDRA YA CUENTA"


def test_el_mensaje_del_reto_es_imprimible():
    assert all(32 <= ord(letra) < 127 for letra in cifra.MENSAJE_RETO)


def test_el_alfabeto_tiene_veintiseis_letras():
    assert len(cifra.ALFABETO) == 26


def test_imprimible_sustituye_los_caracteres_de_control():
    # El espacio cifrado es '%', y en el salto 17 cae en el caracter 20,
    # que no tiene dibujo en la fuente. Ese es el bug del glyph 20.
    assert cifra._imprimible(chr(20)) == "▯"
    assert cifra._imprimible("A" + chr(20) + "B") == "A▯B"


def test_imprimible_deja_pasar_lo_que_si_se_dibuja():
    assert cifra._imprimible("LA PIEDRA YA CUENTA") == "LA PIEDRA YA CUENTA"


def test_ningun_salto_manda_caracteres_sin_dibujo_a_la_figura():
    for salto in range(26):
        eje = cifra.disco(cifra.MENSAJE_RETO, salto)
        for texto in eje.texts:
            assert all(ord(letra) >= 32 for letra in texto.get_text())
        plt.close("all")   # sin esto matplotlib avisa a las veinte figuras


def test_el_disco_dibuja_las_dos_tiras_y_el_mensaje():
    eje = cifra.disco("QF%UNJIWF", 5)
    textos = [t.get_text() for t in eje.texts]
    assert "LA PIEDRA" in textos
    assert "A" in textos
    plt.close("all")


def test_el_disco_escribe_el_salto_en_la_figura():
    eje = cifra.disco(cifra.MENSAJE_RETO, 17)
    textos = [t.get_text() for t in eje.texts]
    assert "salto: 17" in textos
    plt.close("all")


def test_el_deslizador_se_llama_salto_y_es_ancho():
    deslizador = cifra._deslizador_de_salto()
    assert deslizador.description == "salto"
    assert deslizador.min == 0 and deslizador.max == 25
    assert deslizador.layout.width == "620px"


def test_deslizador_disco_no_deja_cuadro_fijo_antes_del_widget(monkeypatch):
    llamadas = []
    monkeypatch.setattr(cifra, "disco", lambda *a, **k: llamadas.append((a, k)))
    cifra.deslizador_disco("QF%UNJIWF")
    # Una sola llamada: el render inicial de @interact. Colab es el unico
    # blanco, asi que ya no se dibuja un cuadro fijo para quien lee sin correr.
    assert len(llamadas) == 1


def test_en_la_fuente_no_queda_vocabulario_de_espana():
    fuente = Path(cifra.__file__).read_text(encoding="utf-8")
    for prohibida in ("corrimiento", "desplazamiento"):
        assert prohibida not in fuente
