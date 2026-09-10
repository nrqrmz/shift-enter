import json
from pathlib import Path

import pytest

NOTEBOOK = Path(__file__).resolve().parents[1] / "la-piedra-que-aprendio-a-contar.ipynb"
PAQUETE_COMPUERTAS = Path(__file__).resolve().parents[1] / "shift_enter" / "compuertas.py"
GRAFICACION = ("plt.", "px.", "matplotlib", "plotly", "sns.", "fig,")
PROHIBIDAS = ("basura", "corrimiento", "desplazamiento", "inútil",
              "aburrido", "§")


@pytest.fixture(scope="module")
def celdas():
    return json.loads(NOTEBOOK.read_text(encoding="utf-8"))["cells"]


def visibles(celdas):
    return [(i, celda) for i, celda in enumerate(celdas)
            if celda["cell_type"] == "code"
            and celda.get("metadata", {}).get("cellView") != "form"]


def test_ninguna_celda_quedo_con_error(celdas):
    con_error = [i for i, celda in enumerate(celdas)
                 if any(salida.get("output_type") == "error"
                        for salida in celda.get("outputs", []))]
    assert con_error == []


def test_la_primera_celda_de_codigo_es_de_forma(celdas):
    primera = next(celda for celda in celdas if celda["cell_type"] == "code")
    assert primera.get("metadata", {}).get("cellView") == "form"
    assert "".join(primera["source"]).startswith("#@title")


def test_ninguna_celda_visible_dibuja(celdas):
    ofensivas = [(i, marca) for i, celda in visibles(celdas)
                 for marca in GRAFICACION if marca in "".join(celda["source"])]
    assert ofensivas == []


def test_ninguna_celda_visible_importa(celdas):
    ofensivas = [i for i, celda in visibles(celdas)
                 if "import " in "".join(celda["source"])]
    assert ofensivas == []


def test_ninguna_celda_visible_define_una_funcion(celdas):
    # La notebook es de descubrimiento: el alumno todavia no ha visto una
    # funcion, asi que arma el sumador con el dedo sobre los widgets del
    # paquete. Todo 'def' vive en shift_enter.
    ofensivas = [i for i, celda in visibles(celdas)
                 if "def " in "".join(celda["source"])]
    assert ofensivas == []


def test_solo_la_celda_que_califica_conserva_un_if(celdas):
    # Unica excepcion autorizada: ahi ver el codigo es lo que hace que la
    # prueba contra el + de Python valga como prueba y no como afirmacion.
    con_if = [i for i, celda in visibles(celdas)
              if "if " in "".join(celda["source"])]
    assert len(con_if) == 1
    assert "aciertos" in "".join(celdas[con_if[0]]["source"])


def test_las_compuertas_viven_en_el_paquete():
    fuente = (PAQUETE_COMPUERTAS).read_text(encoding="utf-8")
    for firma in ("def NOT(", "def AND(", "def OR(", "def XOR(",
                  "def medio_sumador(", "def sumador_completo(", "def sumar("):
        assert firma in fuente


def test_la_notebook_no_usa_vocabulario_retirado():
    # Sobre el archivo completo, no solo las celdas: el bloque de estado de
    # los widgets en metadata guarda las etiquetas de los deslizadores, y ahi
    # sobrevivia "corrimiento" de la ejecucion vieja.
    crudo = NOTEBOOK.read_text(encoding="utf-8")
    ofensivas = [palabra for palabra in PROHIBIDAS if palabra in crudo]
    assert ofensivas == []


def test_el_paquete_no_usa_vocabulario_retirado():
    paquete = Path(__file__).resolve().parents[1] / "shift_enter"
    fuente = "\n".join(archivo.read_text(encoding="utf-8")
                       for archivo in sorted(paquete.rglob("*.py")))
    ofensivas = [palabra for palabra in PROHIBIDAS if palabra in fuente]
    assert ofensivas == []


def test_ninguna_salida_carga_plotly_entero(celdas):
    # Cada figura de plotly quiere guardar una copia completa de plotly.js
    # dentro del archivo: casi cinco megas por celda que en GitHub no dibujan
    # nada, porque alla el JavaScript se elimina. La figura viaja en el
    # payload "application/vnd.plotly.v1+json", que si se renderiza en Colab,
    # Jupyter y nbviewer. Despues de re-ejecutar hay que volver a quitarlas.
    ofensivas = [i for i, celda in enumerate(celdas)
                 for salida in celda.get("outputs", [])
                 if "plotly" in "".join(salida.get("data", {})
                                        .get("text/html", "")).lower()]
    assert ofensivas == []
