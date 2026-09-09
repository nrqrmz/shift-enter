import json
from pathlib import Path

import pytest

NOTEBOOK = Path(__file__).resolve().parents[1] / "la-piedra-que-aprendio-a-contar.ipynb"
GRAFICACION = ("plt.", "px.", "matplotlib", "plotly", "sns.", "fig,")


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


