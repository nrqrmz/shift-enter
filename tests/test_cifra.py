import matplotlib
matplotlib.use("Agg")

from shift_enter import cifra


def correr(texto, cuanto):
    return "".join(chr(ord(letra) + cuanto) for letra in texto)


def test_el_mensaje_del_reto_se_descifra_con_su_desplazamiento():
    assert correr(cifra.MENSAJE_RETO, -cifra.DESPLAZAMIENTO_RETO) == "LA PIEDRA YA CUENTA"


def test_el_mensaje_del_reto_es_imprimible():
    assert all(32 <= ord(letra) < 127 for letra in cifra.MENSAJE_RETO)


def test_el_alfabeto_tiene_veintiseis_letras():
    assert len(cifra.ALFABETO) == 26


def test_el_disco_dibuja_las_dos_tiras_y_el_mensaje():
    eje = cifra.disco("QF%UNJIWF", 5)
    textos = [t.get_text() for t in eje.texts]
    assert "LA PIEDRA" in textos
    assert "A" in textos


def test_deslizador_disco_deja_un_cuadro_fijo_antes_del_widget(monkeypatch):
    llamadas = []
    monkeypatch.setattr(cifra, "disco", lambda *a, **k: llamadas.append((a, k)))
    cifra.deslizador_disco("QF%UNJIWF")
    # Dos llamadas: el cuadro fijo explicito y el render inicial de @interact
    # (que tambien dibuja con desplazamiento 0, el valor por defecto del
    # deslizador). Si se borra la linea del cuadro fijo, solo queda una.
    assert len(llamadas) == 2
    primera_args, primera_kwargs = llamadas[0]
    assert primera_args[:2] == ("QF%UNJIWF", 0) or (
        primera_args[:1] == ("QF%UNJIWF",) and primera_kwargs.get("desplazamiento") == 0
    )
