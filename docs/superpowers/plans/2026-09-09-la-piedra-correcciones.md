# Correcciones de La piedra que aprendió a contar — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Aplicar las dieciséis correcciones que Enrique levantó al correr la
notebook en Colab: dos bugs con causa raíz, el cambio a Colab como único
blanco, la reescritura de la parte cinco sin código a la vista, y la auditoría
de tono.

**Architecture:** Todo el código de funciones que hoy vive en celdas visibles se
muda al paquete `shift_enter`. Nace `shift_enter/compuertas.py`, que concentra
las compuertas, el sumador y cuatro widgets nuevos con los que el alumno arma el
sumador con el dedo en vez de escribirlo. Las tareas van paquete primero,
notebook después, porque las celdas llaman al paquete y no al revés.

**Tech Stack:** Python 3.10+, numpy, matplotlib, plotly, Pillow, ipywidgets,
pytest, nbformat, nbclient. Todo preinstalado en Google Colab.

**Spec:** `docs/superpowers/specs/2026-09-09-la-piedra-correcciones-design.md`

## Global Constraints

- **Todo en español**, incluidos identificadores, docstrings y comentarios. Los
  nombres de las compuertas son la única excepción: `NOT`, `AND`, `OR`, `XOR`
  van en inglés porque así se llaman los conceptos reales.
- **Español de México.** Prohibidas en la notebook y en el paquete: `basura`,
  `corrimiento`, `desplazamiento`, `inútil`, `aburrido`, `§`.
- **Cero dependencias nuevas.** Solo lo que Colab preinstala.
- **En la notebook no queda ningún `def`.** Ningún `if` tampoco, salvo la celda
  de calificación de la Tarea 13, que es la única excepción autorizada.
- **Ninguna celda visible dibuja ni importa.** `plt.`, `px.`, `matplotlib`,
  `plotly`, `sns.`, `fig,` e `import ` solo pueden aparecer en la celda de forma
  del taller. `tests/test_notebook.py` ya lo vigila y se queda vigilándolo.
- **Colab es el único blanco.** No se diseña para que la notebook se lea en
  GitHub sin ejecutarla. Ningún widget dibuja un cuadro fijo antes de sí mismo.
- **La notebook se re-ejecuta con `nbclient`, nunca con `jupyter nbconvert`**,
  que está roto en este entorno. El procedimiento exacto está en `CLAUDE.md`.
- **`CLAUDE.md` está en el `.gitignore`.** Nunca se agrega a un commit.
- Cada tarea termina con `pytest` en verde antes de commitear.

---

### Task 1: Retirar el guardián viejo

`tests/test_notebook.py` afirma hoy lo contrario de lo que este plan
construye: que `def NO(`, `def XOR(`, `def sumar(` y sus hermanas viven en
celdas visibles y jamás aparecen en el paquete. En cuanto la Tarea 2 cree
`compuertas.py`, esos tres tests se ponen rojos. Se retiran ahora, antes de
tocar nada, y el guardián nuevo, que afirma la regla contraria, se escribe
hasta la Tarea 15, cuando la notebook ya cumpla.

**Files:**
- Modify: `tests/test_notebook.py`
- Modify: `tests/conftest.py`

**Interfaces:**
- Consumes: nada.
- Produces: `tests/test_notebook.py` conserva `test_ninguna_celda_quedo_con_error`,
  `test_la_primera_celda_de_codigo_es_de_forma`,
  `test_ninguna_celda_visible_dibuja`, `test_ninguna_celda_visible_importa` y el
  helper `visibles(celdas)`. La constante `CONCEPTO` desaparece.

- [ ] **Step 1: Confirmar que la suite está verde antes de tocar nada**

Run: `pytest -q`
Expected: PASS, sin fallos.

- [ ] **Step 2: Borrar los tres tests que codifican la regla vieja**

Borra de `tests/test_notebook.py` la constante `CONCEPTO` y estos tres tests
completos, con sus cuerpos:

- `test_el_concepto_nunca_migra_al_paquete`
- `test_toda_funcion_de_concepto_que_ya_existe_vive_en_celda_visible`
- `test_toda_firma_de_concepto_vive_en_una_celda_visible`

Borra también la constante `PAQUETE`, que solo usaba el primero de ellos.

No toques los otros cuatro tests ni el helper `visibles`.

- [ ] **Step 3: Actualizar el docstring de conftest**

`tests/conftest.py` explica que fija `plotly_mimetype` en parte por "el
renderer que fija la propia celda de forma de la notebook para Colab". Esa
línea del taller desaparece en la Tarea 11. Sustituye ese párrafo por:

```python
"""Deja la suite muda y ciega: nada de ventanas, nada de pestañas.

Esto corre antes que cualquier modulo de prueba. Sin esto, dos cosas se
escapan del proceso de pytest hacia el mundo real:

- matplotlib, sin backend explicito, intenta abrir una ventana grafica
  (TkAgg u otro backend interactivo) en cuanto algun test importa pyplot.
- plotly, fuera de un kernel de Jupyter, resuelve su renderer por omision
  a "browser": cada figura.show() abre una pestaña nueva del navegador.

"plotly_mimetype" emite un payload de display para IPython, que no hace
nada en absoluto fuera de un kernel, asi que .show() queda inerte aqui.
Dentro de Colab no aplica nada de esto: alla plotly detecta el entorno solo
y la notebook ya no le impone ningun renderer.

No borrar esto: sin las dos lineas de abajo, correr `pytest` vuelve a
abrirle una ventana y un navegador al que lo corra.
"""
```

- [ ] **Step 4: Correr la suite**

Run: `pytest -q`
Expected: PASS. Deben quedar tres tests menos que en el paso 1.

- [ ] **Step 5: Commit**

```bash
git add tests/test_notebook.py tests/conftest.py
git commit -m "test: retira el guardian que exigia el concepto en celda visible"
```

---

### Task 2: `shift_enter/compuertas.py`, la lógica

Las compuertas, el sumador y la tabla de verdad. Sin widgets todavía.
`tabla_de_verdad` se muda desde `interruptores.py` y gana el parámetro
`resaltar`, que los widgets de las tareas siguientes necesitan para iluminar el
renglón vigente.

**Files:**
- Create: `shift_enter/compuertas.py`
- Create: `tests/test_compuertas.py`
- Modify: `shift_enter/interruptores.py` (borrar `_tabla_de_verdad` y `tabla_de_verdad`)
- Modify: `tests/test_interruptores.py` (mover sus dos tests de tabla de verdad)

**Interfaces:**
- Consumes: `shift_enter.binario.a_binario`, `shift_enter.paleta.ENCENDIDO`,
  `APAGADO`, `BORDE`, `TENUE`.
- Produces:
  - `NOT(a) -> bool`, `AND(a, b) -> bool`, `OR(a, b) -> bool`, `XOR(a, b) -> bool`
  - `medio_sumador(a, b) -> (bool, bool)` como `(suma, llevo)`
  - `sumador_completo(a, b, llevo_que_entra) -> (bool, bool)` como `(suma, llevo)`
  - `sumar(a, b, ancho=8) -> list[bool]`, ocho bits, el más significativo primero
  - `_tabla_de_verdad(nombre, compuerta, entradas=2, resaltar=None, ax=None) -> Axes`
  - `tabla_de_verdad(nombre, compuerta, entradas=2, resaltar=None) -> None`
  - `PRENDIDO = True`, `APAGADO_LOGICO = False`

- [ ] **Step 1: Escribir las pruebas que fallan**

Crea `tests/test_compuertas.py`:

```python
from shift_enter import compuertas
from shift_enter.binario import a_decimal


def test_not_invierte():
    assert compuertas.NOT(False) is True
    assert compuertas.NOT(True) is False


def test_and_solo_se_prende_con_los_dos():
    assert compuertas.AND(True, True) is True
    assert compuertas.AND(True, False) is False
    assert compuertas.AND(False, True) is False
    assert compuertas.AND(False, False) is False


def test_or_se_prende_con_cualquiera():
    assert compuertas.OR(True, True) is True
    assert compuertas.OR(True, False) is True
    assert compuertas.OR(False, True) is True
    assert compuertas.OR(False, False) is False


def test_xor_se_prende_solo_con_distintos():
    assert compuertas.XOR(True, False) is True
    assert compuertas.XOR(False, True) is True
    assert compuertas.XOR(True, True) is False
    assert compuertas.XOR(False, False) is False


def test_las_compuertas_devuelven_booleanos_de_verdad():
    # 'and' y 'or' de Python devuelven el operando, no un booleano.
    assert compuertas.AND(1, 0) is False
    assert compuertas.OR(0, 2) is True


def test_el_medio_sumador_lleva_uno_solo_cuando_los_dos_estan_prendidos():
    assert compuertas.medio_sumador(False, False) == (False, False)
    assert compuertas.medio_sumador(True, False) == (True, False)
    assert compuertas.medio_sumador(False, True) == (True, False)
    assert compuertas.medio_sumador(True, True) == (False, True)


def test_el_sumador_completo_suma_tres_interruptores():
    assert compuertas.sumador_completo(True, True, True) == (True, True)
    assert compuertas.sumador_completo(True, True, False) == (False, True)
    assert compuertas.sumador_completo(True, False, True) == (False, True)
    assert compuertas.sumador_completo(False, False, False) == (False, False)


def test_sumar_acierta_las_dieciseis_mil_sumas():
    aciertos = sum(1 for a in range(128) for b in range(128)
                   if a_decimal(compuertas.sumar(a, b)) == a + b)
    assert aciertos == 128 * 128


def test_sumar_devuelve_ocho_interruptores():
    assert len(compuertas.sumar(13, 29)) == 8


def test_sumar_se_desborda_en_doscientos_cincuenta_y_seis():
    assert a_decimal(compuertas.sumar(255, 1)) == 0


def test_tabla_de_verdad_de_una_entrada_tiene_dos_casos():
    eje = compuertas._tabla_de_verdad("NOT", compuertas.NOT, entradas=1)
    assert len(eje.patches) == 4  # dos entradas y dos salidas


def test_tabla_de_verdad_de_dos_entradas_tiene_cuatro_casos():
    eje = compuertas._tabla_de_verdad("AND", compuertas.AND)
    assert len(eje.patches) == 12  # ocho entradas y cuatro salidas


def test_tabla_de_verdad_resalta_el_renglon_vigente():
    eje = compuertas._tabla_de_verdad("AND", compuertas.AND, resaltar=(True, True))
    resaltados = [p for p in eje.patches if getattr(p, "get_linewidth", None)
                  and p.get_linewidth() > 2]
    assert resaltados != []


def test_tabla_de_verdad_sin_resaltar_no_resalta_nada():
    eje = compuertas._tabla_de_verdad("AND", compuertas.AND)
    resaltados = [p for p in eje.patches if getattr(p, "get_linewidth", None)
                  and p.get_linewidth() > 2]
    assert resaltados == []


def test_tabla_de_verdad_publica_no_devuelve_nada():
    assert compuertas.tabla_de_verdad("NOT", compuertas.NOT, entradas=1) is None
```

- [ ] **Step 2: Correr para verificar que fallan**

Run: `pytest tests/test_compuertas.py -q`
Expected: FAIL con `ModuleNotFoundError: No module named 'shift_enter.compuertas'`.

- [ ] **Step 3: Escribir el módulo**

Crea `shift_enter/compuertas.py`:

```python
"""Las tres reglas con las que se construye todo lo demas, y el sumador.

Esto es plomeria a proposito. La notebook es de descubrimiento: el alumno
todavia no ha visto una funcion, asi que arma el sumador con el dedo sobre
los widgets de este modulo, no escribiendo estas lineas.
"""

import matplotlib.pyplot as plt

from .binario import a_binario
from .paleta import APAGADO, BORDE, ENCENDIDO, TENUE

PRENDIDO = True
APAGADO_LOGICO = False


def NOT(a):
    """Prendido cuando la entrada esta apagada."""
    return not a


def AND(a, b):
    """Prendido solo cuando las dos entradas estan prendidas."""
    return bool(a) and bool(b)


def OR(a, b):
    """Prendido cuando al menos una entrada esta prendida."""
    return bool(a) or bool(b)


def XOR(a, b):
    """Prendido solo si a y b son DISTINTOS.

    No es una pieza nueva: es NOT, AND y OR acomodadas de cierta forma.
    """
    return OR(AND(a, NOT(b)),
              AND(NOT(a), b))


def medio_sumador(a, b):
    """Suma dos interruptores. Devuelve (suma, llevo)."""
    return XOR(a, b), AND(a, b)


def sumador_completo(a, b, llevo_que_entra):
    """Suma dos interruptores mas el llevo de la columna anterior."""
    suma_parcial, acarreo_1 = medio_sumador(a, b)
    suma_final, acarreo_2 = medio_sumador(suma_parcial, llevo_que_entra)
    return suma_final, OR(acarreo_1, acarreo_2)


def sumar(a, b, ancho=8):
    """Ocho sumadores completos en fila. Devuelve la lista de bits."""
    bits_a = a_binario(a, ancho)
    bits_b = a_binario(b, ancho)
    resultado = []
    llevo = APAGADO_LOGICO

    for i in reversed(range(ancho)):
        suma, llevo = sumador_completo(bits_a[i], bits_b[i], llevo)
        resultado.insert(0, suma)

    return resultado


def _casos(entradas):
    if entradas == 1:
        return [(a,) for a in (False, True)], ["a"]
    return [(a, b) for a in (False, True) for b in (False, True)], ["a", "b"]


def _tabla_de_verdad(nombre, compuerta, entradas=2, resaltar=None, ax=None):
    """Todo lo que puede pasar con una compuerta. Version interna."""
    casos, encabezados = _casos(entradas)
    salida_x = len(encabezados) * 0.85 + 0.75

    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(salida_x + 1.3, 0.85 * len(casos) + 1.2))

    for j, h in enumerate(encabezados):
        ax.text(j * 0.85, 0.85, h, ha="center", fontsize=12, color="0.35")
    ax.text(salida_x, 0.85, nombre, ha="center", fontsize=12, weight="bold")

    for fila, caso in enumerate(casos):
        y = -fila
        vigente = resaltar is not None and tuple(bool(v) for v in resaltar) == caso
        grosor = 3.2 if vigente else 1.4
        for j, v in enumerate(caso):
            ax.add_patch(plt.Circle((j * 0.85, y), 0.28, zorder=2, linewidth=grosor,
                                    facecolor=ENCENDIDO if v else APAGADO,
                                    edgecolor=BORDE))
        ax.text(salida_x - 0.75, y, "→", ha="center", va="center",
                fontsize=15, color=TENUE)
        s = compuerta(*caso)
        ax.add_patch(plt.Circle((salida_x, y), 0.28, zorder=2, linewidth=grosor,
                                facecolor=ENCENDIDO if s else APAGADO,
                                edgecolor=BORDE))

    ax.set_xlim(-0.55, salida_x + 0.55)
    ax.set_ylim(-len(casos) + 0.1, 1.25)
    ax.set_aspect("equal")
    ax.axis("off")
    if propia:
        plt.tight_layout()
    return ax


def tabla_de_verdad(nombre, compuerta, entradas=2, resaltar=None):
    """Todo lo que puede pasar con una compuerta, dibujado."""
    _tabla_de_verdad(nombre, compuerta, entradas, resaltar)
    plt.show()
```

- [ ] **Step 4: Correr las pruebas nuevas**

Run: `pytest tests/test_compuertas.py -q`
Expected: PASS, quince tests.

- [ ] **Step 5: Sacar la tabla de verdad de `interruptores.py`**

Borra de `shift_enter/interruptores.py` las funciones `_tabla_de_verdad` y
`tabla_de_verdad` completas. Borra de `tests/test_interruptores.py` los dos
tests que las usan: `test_tabla_de_verdad_de_una_entrada_tiene_dos_casos` y
`test_tabla_de_verdad_no_devuelve_nada`.

`interruptores.py` conserva sus imports de `paleta` y de `binario`, que sus
otras funciones siguen usando.

- [ ] **Step 6: Correr la suite completa**

Run: `pytest -q`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add shift_enter/compuertas.py tests/test_compuertas.py \
        shift_enter/interruptores.py tests/test_interruptores.py
git commit -m "feat: compuertas NOT, AND, OR, XOR y el sumador, en el paquete"
```

---

### Task 3: El probador de compuertas

Dos interruptores que el alumno prende con el dedo, y las tres tablas de verdad
iluminando el renglón que está viviendo. Sustituye a las tres celdas de `if`
que hoy tiene la parte cinco.

**Files:**
- Modify: `shift_enter/compuertas.py`
- Modify: `tests/test_compuertas.py`

**Interfaces:**
- Consumes: `_tabla_de_verdad`, `NOT`, `AND`, `OR` de la Tarea 2.
- Produces:
  - `_panel_compuertas(a, b) -> Figure`, con tres ejes
  - `_probador() -> (ToggleButton, ToggleButton, Output)`
  - `probador() -> None`

- [ ] **Step 1: Escribir las pruebas que fallan**

Agrega al final de `tests/test_compuertas.py`:

```python
def test_el_panel_tiene_una_tabla_por_compuerta():
    figura = compuertas._panel_compuertas(True, False)
    assert len(figura.axes) == 3


def test_el_probador_arranca_con_los_dos_apagados():
    a, b, salida = compuertas._probador()
    assert a.value is False
    assert b.value is False


def test_el_probador_rotula_sus_dos_interruptores():
    a, b, salida = compuertas._probador()
    assert a.description == "a"
    assert b.description == "b"


def test_el_probador_repinta_cuando_prendes_uno(monkeypatch):
    pintados = []
    monkeypatch.setattr(compuertas, "_panel_compuertas",
                        lambda *a, **k: pintados.append(a))
    a, b, salida = compuertas._probador()
    de_arranque = len(pintados)
    a.value = True
    assert len(pintados) == de_arranque + 1
    assert pintados[-1] == (True, False)


def test_probador_no_devuelve_nada():
    assert compuertas.probador() is None
```

- [ ] **Step 2: Correr para verificar que fallan**

Run: `pytest tests/test_compuertas.py -q -k "panel or probador"`
Expected: FAIL con `AttributeError: module 'shift_enter.compuertas' has no attribute '_panel_compuertas'`.

- [ ] **Step 3: Implementar**

Agrega a los imports de `shift_enter/compuertas.py`:

```python
import ipywidgets as widgets
from IPython.display import display
```

Y al final del módulo:

```python
def _panel_compuertas(a, b):
    """Las tres tablas de verdad, con el renglon vigente iluminado."""
    figura, ejes = plt.subplots(1, 3, figsize=(11, 4.2))
    _tabla_de_verdad("NOT", NOT, entradas=1, resaltar=(a,), ax=ejes[0])
    _tabla_de_verdad("AND", AND, resaltar=(a, b), ax=ejes[1])
    _tabla_de_verdad("OR", OR, resaltar=(a, b), ax=ejes[2])
    plt.tight_layout()
    return figura


def _probador():
    """Construye el probador de compuertas. Version interna."""
    a = widgets.ToggleButton(value=False, description="a",
                             layout=widgets.Layout(width="70px"))
    b = widgets.ToggleButton(value=False, description="b",
                             layout=widgets.Layout(width="70px"))
    salida = widgets.Output()

    def pintar(_=None):
        with salida:
            salida.clear_output(wait=True)
            _panel_compuertas(a.value, b.value)
            plt.show()

    a.observe(pintar, names="value")
    b.observe(pintar, names="value")
    pintar()
    return a, b, salida


def probador():
    """Prende los dos interruptores y mira las tres compuertas a la vez."""
    a, b, salida = _probador()
    display(widgets.VBox([widgets.HBox([a, b]), salida]))
```

- [ ] **Step 4: Correr las pruebas**

Run: `pytest tests/test_compuertas.py -q`
Expected: PASS, veinte tests.

- [ ] **Step 5: Commit**

```bash
git add shift_enter/compuertas.py tests/test_compuertas.py
git commit -m "feat: el probador de compuertas, con el renglon vigente iluminado"
```

---

### Task 4: El diagrama del XOR

El remate de la parte cinco es que XOR no es una pieza nueva. Hoy ese remate
vive en tres líneas de código que ya nadie va a ver. Lo reemplaza un diagrama
del cableado donde los cables que están conduciendo se encienden.

**Files:**
- Modify: `shift_enter/compuertas.py`
- Modify: `tests/test_compuertas.py`

**Interfaces:**
- Consumes: `NOT`, `AND`, `OR`, `XOR`, `ENCENDIDO`, `APAGADO`, `BORDE` de la Tarea 2.
- Produces:
  - `_dibujar_xor(a, b, ax=None) -> Axes`
  - `_diagrama_xor() -> (ToggleButton, ToggleButton, Output)`
  - `diagrama_xor() -> None`

- [ ] **Step 1: Escribir las pruebas que fallan**

Agrega al final de `tests/test_compuertas.py`:

```python
from shift_enter.paleta import ENCENDIDO


def _cables_encendidos(eje):
    return [linea for linea in eje.lines
            if linea.get_color() == ENCENDIDO]


def test_con_todo_apagado_ningun_cable_conduce():
    eje = compuertas._dibujar_xor(False, False)
    assert _cables_encendidos(eje) == []


def test_con_entradas_distintas_algun_cable_conduce():
    eje = compuertas._dibujar_xor(True, False)
    assert _cables_encendidos(eje) != []


def test_el_diagrama_rotula_la_salida_con_el_valor_del_xor():
    for a in (False, True):
        for b in (False, True):
            eje = compuertas._dibujar_xor(a, b)
            textos = [t.get_text() for t in eje.texts]
            assert "XOR" in textos
            assert str(int(compuertas.XOR(a, b))) in textos


def test_el_diagrama_xor_repinta_cuando_prendes_uno(monkeypatch):
    pintados = []
    monkeypatch.setattr(compuertas, "_dibujar_xor",
                        lambda *a, **k: pintados.append(a))
    a, b, salida = compuertas._diagrama_xor()
    de_arranque = len(pintados)
    b.value = True
    assert len(pintados) == de_arranque + 1
    assert pintados[-1] == (False, True)


def test_diagrama_xor_no_devuelve_nada():
    assert compuertas.diagrama_xor() is None
```

- [ ] **Step 2: Correr para verificar que fallan**

Run: `pytest tests/test_compuertas.py -q -k "xor and (cable or diagrama or rotula)"`
Expected: FAIL con `AttributeError: module 'shift_enter.compuertas' has no attribute '_dibujar_xor'`.

- [ ] **Step 3: Implementar**

Agrega al final de `shift_enter/compuertas.py`:

```python
def _cable(ax, puntos, vivo):
    """Un cable. Encendido si esta conduciendo, apagado si no."""
    xs = [p[0] for p in puntos]
    ys = [p[1] for p in puntos]
    ax.plot(xs, ys, linewidth=2.6 if vivo else 1.6,
            color=ENCENDIDO if vivo else BORDE, zorder=1,
            solid_capstyle="round")


def _caja(ax, x, y, texto, vivo):
    """Una compuerta, dibujada como caja rotulada."""
    ax.add_patch(plt.Rectangle((x - 0.62, y - 0.42), 1.24, 0.84, zorder=2,
                               linewidth=1.8, facecolor="white",
                               edgecolor=ENCENDIDO if vivo else BORDE))
    ax.text(x, y, texto, ha="center", va="center", zorder=3,
            fontsize=11, weight="bold", family="monospace")


def _foco(ax, x, y, valor, etiqueta):
    """Un interruptor con su rotulo y su cero o su uno."""
    ax.add_patch(plt.Circle((x, y), 0.3, zorder=3, linewidth=1.6,
                            facecolor=ENCENDIDO if valor else APAGADO,
                            edgecolor=BORDE))
    ax.text(x, y + 0.55, etiqueta, ha="center", va="center",
            fontsize=11, color=TENUE)
    ax.text(x, y - 0.62, str(int(bool(valor))), ha="center", va="center",
            fontsize=12, weight="bold", family="monospace")


def _dibujar_xor(a, b, ax=None):
    """El cableado del XOR, con la corriente encendida por donde pasa."""
    a, b = bool(a), bool(b)
    no_a, no_b = NOT(a), NOT(b)
    arriba = AND(a, no_b)
    abajo = AND(no_a, b)
    salida = OR(arriba, abajo)

    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(10, 4.6))

    _foco(ax, 0, 3.2, a, "a")
    _foco(ax, 0, 0.4, b, "b")

    _caja(ax, 2.2, 1.0, "NOT", no_b)
    _caja(ax, 2.2, 2.6, "NOT", no_a)
    _caja(ax, 4.6, 3.2, "AND", arriba)
    _caja(ax, 4.6, 0.4, "AND", abajo)
    _caja(ax, 7.0, 1.8, "OR", salida)

    _cable(ax, [(0.3, 3.2), (3.98, 3.2)], a)
    _cable(ax, [(0.3, 0.4), (1.2, 0.4), (1.2, 1.0), (1.58, 1.0)], b)
    _cable(ax, [(2.82, 1.0), (3.4, 1.0), (3.4, 2.95), (3.98, 2.95)], no_b)
    _cable(ax, [(0.3, 3.2), (1.2, 3.2), (1.2, 2.6), (1.58, 2.6)], a)
    _cable(ax, [(2.82, 2.6), (3.4, 2.6), (3.4, 0.65), (3.98, 0.65)], no_a)
    _cable(ax, [(0.3, 0.4), (3.98, 0.4)], b)
    _cable(ax, [(5.22, 3.2), (5.9, 3.2), (5.9, 2.0), (6.38, 2.0)], arriba)
    _cable(ax, [(5.22, 0.4), (5.9, 0.4), (5.9, 1.6), (6.38, 1.6)], abajo)
    _cable(ax, [(7.62, 1.8), (8.6, 1.8)], salida)

    _foco(ax, 8.9, 1.8, salida, "XOR")

    ax.set_xlim(-0.9, 9.9)
    ax.set_ylim(-0.9, 4.2)
    ax.set_aspect("equal")
    ax.axis("off")
    if propia:
        plt.tight_layout()
    return ax


def _diagrama_xor():
    """Construye el diagrama vivo del XOR. Version interna."""
    a = widgets.ToggleButton(value=False, description="a",
                             layout=widgets.Layout(width="70px"))
    b = widgets.ToggleButton(value=False, description="b",
                             layout=widgets.Layout(width="70px"))
    salida = widgets.Output()

    def pintar(_=None):
        with salida:
            salida.clear_output(wait=True)
            _dibujar_xor(a.value, b.value)
            plt.show()

    a.observe(pintar, names="value")
    b.observe(pintar, names="value")
    pintar()
    return a, b, salida


def diagrama_xor():
    """Mueve los interruptores y mira por donde pasa la corriente."""
    a, b, salida = _diagrama_xor()
    display(widgets.VBox([widgets.HBox([a, b]), salida]))
```

- [ ] **Step 4: Correr las pruebas**

Run: `pytest tests/test_compuertas.py -q`
Expected: PASS, veintiséis tests.

- [ ] **Step 5: Mirar el dibujo una vez, con ojos**

Los tests confirman que los cables se encienden, no que el diagrama se
entienda. Genera los cuatro casos y ábrelos:

```bash
python3 - <<'PY'
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shift_enter import compuertas
for a in (False, True):
    for b in (False, True):
        compuertas._dibujar_xor(a, b)
        plt.savefig(f"/tmp/xor_{int(a)}{int(b)}.png", dpi=110)
        plt.close("all")
print("/tmp/xor_00.png /tmp/xor_01.png /tmp/xor_10.png /tmp/xor_11.png")
PY
```

Confirma que ningún cable se encima con otro, que las cajas no se traslapan, y
que en los casos 01 y 10 se ve un camino continuo encendido de la entrada a la
salida. Si algo se encima, ajusta las coordenadas de `_dibujar_xor` y repite.

- [ ] **Step 6: Commit**

```bash
git add shift_enter/compuertas.py tests/test_compuertas.py
git commit -m "feat: el diagrama vivo del XOR, con la corriente encendida"
```

---

### Task 5: El medio sumador vivo

Dos interruptores, dos focos de salida rotulados suma y llevo, y el cableado de
XOR y AND a la vista.

**Files:**
- Modify: `shift_enter/compuertas.py`
- Modify: `tests/test_compuertas.py`

**Interfaces:**
- Consumes: `medio_sumador`, `_cable`, `_caja`, `_foco` de las Tareas 2 y 4.
- Produces:
  - `_dibujar_medio_sumador(a, b, ax=None) -> Axes`
  - `_medio_sumador_vivo() -> (ToggleButton, ToggleButton, Output)`
  - `medio_sumador_vivo() -> None`

- [ ] **Step 1: Escribir las pruebas que fallan**

Agrega al final de `tests/test_compuertas.py`:

```python
def test_el_medio_sumador_vivo_rotula_suma_y_llevo():
    eje = compuertas._dibujar_medio_sumador(True, True)
    textos = [t.get_text() for t in eje.texts]
    assert "suma" in textos
    assert "llevo" in textos


def test_con_los_dos_prendidos_el_llevo_conduce_y_la_suma_no():
    eje = compuertas._dibujar_medio_sumador(True, True)
    encendidos = [linea for linea in eje.lines
                  if linea.get_color() == ENCENDIDO]
    # El cable del llevo sale del AND; el de la suma sale del XOR y esta apagado.
    assert encendidos != []
    textos = [t.get_text() for t in eje.texts]
    assert textos.count("0") >= 1   # la suma vale cero
    assert textos.count("1") >= 1   # el llevo vale uno


def test_el_medio_sumador_vivo_repinta(monkeypatch):
    pintados = []
    monkeypatch.setattr(compuertas, "_dibujar_medio_sumador",
                        lambda *a, **k: pintados.append(a))
    a, b, salida = compuertas._medio_sumador_vivo()
    de_arranque = len(pintados)
    a.value = True
    assert len(pintados) == de_arranque + 1


def test_medio_sumador_vivo_no_devuelve_nada():
    assert compuertas.medio_sumador_vivo() is None
```

- [ ] **Step 2: Correr para verificar que fallan**

Run: `pytest tests/test_compuertas.py -q -k "medio_sumador_vivo or rotula_suma or llevo_conduce"`
Expected: FAIL con `AttributeError: ... has no attribute '_dibujar_medio_sumador'`.

- [ ] **Step 3: Implementar**

Agrega al final de `shift_enter/compuertas.py`:

```python
def _dibujar_medio_sumador(a, b, ax=None):
    """Dos interruptores entran, salen la suma y el llevo."""
    a, b = bool(a), bool(b)
    suma, llevo = medio_sumador(a, b)

    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(8.4, 4.2))

    _foco(ax, 0, 2.8, a, "a")
    _foco(ax, 0, 0.6, b, "b")

    _caja(ax, 3.0, 2.8, "XOR", suma)
    _caja(ax, 3.0, 0.6, "AND", llevo)

    _cable(ax, [(0.3, 2.8), (2.38, 2.8)], a)
    _cable(ax, [(0.3, 0.6), (1.4, 0.6), (1.4, 2.55), (2.38, 2.55)], b)
    _cable(ax, [(0.3, 2.8), (1.0, 2.8), (1.0, 0.85), (2.38, 0.85)], a)
    _cable(ax, [(0.3, 0.6), (2.38, 0.6)], b)
    _cable(ax, [(3.62, 2.8), (5.1, 2.8)], suma)
    _cable(ax, [(3.62, 0.6), (5.1, 0.6)], llevo)

    _foco(ax, 5.4, 2.8, suma, "suma")
    _foco(ax, 5.4, 0.6, llevo, "llevo")

    ax.set_xlim(-0.9, 6.4)
    ax.set_ylim(-0.9, 3.8)
    ax.set_aspect("equal")
    ax.axis("off")
    if propia:
        plt.tight_layout()
    return ax


def _medio_sumador_vivo():
    """Construye el medio sumador vivo. Version interna."""
    a = widgets.ToggleButton(value=False, description="a",
                             layout=widgets.Layout(width="70px"))
    b = widgets.ToggleButton(value=False, description="b",
                             layout=widgets.Layout(width="70px"))
    salida = widgets.Output()

    def pintar(_=None):
        with salida:
            salida.clear_output(wait=True)
            _dibujar_medio_sumador(a.value, b.value)
            plt.show()

    a.observe(pintar, names="value")
    b.observe(pintar, names="value")
    pintar()
    return a, b, salida


def medio_sumador_vivo():
    """Las cuatro sumas que existen, una por una, con el dedo."""
    a, b, salida = _medio_sumador_vivo()
    display(widgets.VBox([widgets.HBox([a, b]), salida]))
```

- [ ] **Step 4: Correr las pruebas**

Run: `pytest tests/test_compuertas.py -q`
Expected: PASS, treinta tests.

- [ ] **Step 5: Mirar el dibujo**

```bash
python3 - <<'PY'
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shift_enter import compuertas
for a in (False, True):
    for b in (False, True):
        compuertas._dibujar_medio_sumador(a, b)
        plt.savefig(f"/tmp/medio_{int(a)}{int(b)}.png", dpi=110)
        plt.close("all")
print("listo: /tmp/medio_*.png")
PY
```

Confirma que en el caso 11 la suma queda apagada y el llevo encendido, que es
justo lo que la prosa de la notebook va a afirmar.

- [ ] **Step 6: Commit**

```bash
git add shift_enter/compuertas.py tests/test_compuertas.py
git commit -m "feat: el medio sumador vivo, con sus focos de suma y llevo"
```

---

### Task 6: El sumador de ocho columnas

Aquí se cumple la promesa. Dos filas de ocho interruptores que el alumno prende
con el dedo, la fila del resultado abajo, y los llevos brincando de columna en
columna a la vista.

**Files:**
- Modify: `shift_enter/compuertas.py`
- Modify: `tests/test_compuertas.py`

**Interfaces:**
- Consumes: `sumador_completo`, `_foco`, `binario.TABLA_DE_VALORES`,
  `binario.a_decimal`.
- Produces:
  - `_llevos(bits_a, bits_b) -> (list[bool], list[bool])` como `(resultado, llevos)`,
    ambas de largo ocho, el bit más significativo primero. `llevos[i]` es el
    llevo que la columna `i` le manda a su vecina de la izquierda.
  - `_dibujar_sumador(bits_a, bits_b, ax=None) -> Axes`
  - `_sumador_vivo() -> (list[ToggleButton], list[ToggleButton], Output)`
  - `sumador_vivo(a=13, b=29) -> None`

- [ ] **Step 1: Escribir las pruebas que fallan**

Agrega al final de `tests/test_compuertas.py`:

```python
from shift_enter.binario import a_binario


def test_los_llevos_coinciden_con_el_resultado_de_sumar():
    for a, b in ((13, 29), (255, 1), (0, 0), (170, 85)):
        resultado, llevos = compuertas._llevos(a_binario(a), a_binario(b))
        assert resultado == compuertas.sumar(a, b)
        assert len(llevos) == 8


def test_sin_llevos_cuando_no_se_encima_nada():
    resultado, llevos = compuertas._llevos(a_binario(1), a_binario(2))
    assert llevos == [False] * 8


def test_el_llevo_se_propaga_de_derecha_a_izquierda():
    # 255 + 1 obliga a que las ocho columnas se pasen.
    resultado, llevos = compuertas._llevos(a_binario(255), a_binario(1))
    assert llevos == [True] * 8


def test_el_dibujo_del_sumador_ensena_los_tres_numeros():
    eje = compuertas._dibujar_sumador(a_binario(13), a_binario(29))
    textos = [t.get_text() for t in eje.texts]
    assert "13" in textos
    assert "29" in textos
    assert "42" in textos


def test_el_sumador_vivo_trae_dieciseis_interruptores():
    botones_a, botones_b, salida = compuertas._sumador_vivo()
    assert len(botones_a) == 8
    assert len(botones_b) == 8


def test_el_sumador_vivo_arranca_en_los_valores_pedidos():
    botones_a, botones_b, salida = compuertas._sumador_vivo(a=13, b=29)
    assert [b.value for b in botones_a] == a_binario(13)
    assert [b.value for b in botones_b] == a_binario(29)


def test_el_sumador_vivo_repinta_cuando_prendes_uno(monkeypatch):
    pintados = []
    monkeypatch.setattr(compuertas, "_dibujar_sumador",
                        lambda *a, **k: pintados.append(a))
    botones_a, botones_b, salida = compuertas._sumador_vivo(a=0, b=0)
    de_arranque = len(pintados)
    botones_a[0].value = True
    assert len(pintados) == de_arranque + 1


def test_sumador_vivo_no_devuelve_nada():
    assert compuertas.sumador_vivo() is None
```

- [ ] **Step 2: Correr para verificar que fallan**

Run: `pytest tests/test_compuertas.py -q -k "llevo or sumador_vivo or tres_numeros"`
Expected: FAIL con `AttributeError: ... has no attribute '_llevos'`.

- [ ] **Step 3: Implementar**

Agrega `from .binario import TABLA_DE_VALORES, a_binario, a_decimal` a los
imports de `shift_enter/compuertas.py`, reemplazando el `from .binario import
a_binario` que ya estaba. Luego agrega al final del módulo:

```python
def _llevos(bits_a, bits_b):
    """Suma columna por columna y guarda el llevo que sale de cada una."""
    resultado = [False] * 8
    llevos = [False] * 8
    llevo = APAGADO_LOGICO

    for i in reversed(range(8)):
        suma, llevo = sumador_completo(bits_a[i], bits_b[i], llevo)
        resultado[i] = suma
        llevos[i] = llevo

    return resultado, llevos


def _dibujar_sumador(bits_a, bits_b, ax=None):
    """Las ocho columnas, con el llevo brincando de una a otra."""
    resultado, llevos = _llevos(bits_a, bits_b)

    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(10.5, 5.2))

    filas = ((3.0, bits_a, str(a_decimal(bits_a))),
             (1.8, bits_b, str(a_decimal(bits_b))),
             (0.0, resultado, str(a_decimal(resultado))))

    for y, bits, numero in filas:
        for i, bit in enumerate(bits):
            ax.add_patch(plt.Circle((i, y), 0.32, zorder=3, linewidth=1.6,
                                    facecolor=ENCENDIDO if bit else APAGADO,
                                    edgecolor=BORDE))
        ax.text(8.6, y, numero, ha="left", va="center",
                fontsize=20, weight="bold", family="monospace")

    for i, valor in enumerate(TABLA_DE_VALORES):
        ax.text(i, 3.75, str(valor), ha="center", va="center",
                fontsize=9, color=TENUE)

    # El llevo que sale de la columna i entra a la columna i-1, a su izquierda.
    for i, llevo in enumerate(llevos):
        if i == 0:
            continue
        ax.annotate("", xy=(i - 1 + 0.34, 1.05), xytext=(i - 0.34, 0.75),
                    arrowprops=dict(arrowstyle="->", linewidth=2.2 if llevo else 1.2,
                                    color=ENCENDIDO if llevo else BORDE))

    ax.plot([-0.5, 7.5], [0.95, 0.95], linewidth=1.4, color=BORDE, zorder=1)
    ax.text(-1.0, 3.0, "a", ha="right", va="center", fontsize=12, color=TENUE)
    ax.text(-1.0, 1.8, "b", ha="right", va="center", fontsize=12, color=TENUE)
    ax.text(-1.0, 0.0, "suma", ha="right", va="center", fontsize=12, color=TENUE)

    ax.set_xlim(-2.2, 10.4)
    ax.set_ylim(-0.9, 4.2)
    ax.set_aspect("equal")
    ax.axis("off")
    if propia:
        plt.tight_layout()
    return ax


def _sumador_vivo(a=13, b=29):
    """Construye el sumador de ocho columnas. Version interna."""
    botones_a = [widgets.ToggleButton(value=v, description=str(valor),
                                      layout=widgets.Layout(width="58px"))
                 for v, valor in zip(a_binario(a), TABLA_DE_VALORES)]
    botones_b = [widgets.ToggleButton(value=v, description=str(valor),
                                      layout=widgets.Layout(width="58px"))
                 for v, valor in zip(a_binario(b), TABLA_DE_VALORES)]
    salida = widgets.Output()

    def pintar(_=None):
        with salida:
            salida.clear_output(wait=True)
            _dibujar_sumador([x.value for x in botones_a],
                             [x.value for x in botones_b])
            plt.show()

    for boton in botones_a + botones_b:
        boton.observe(pintar, names="value")
    pintar()
    return botones_a, botones_b, salida


def sumador_vivo(a=13, b=29):
    """Arma la suma con el dedo y mira el llevo brincar de columna en columna."""
    botones_a, botones_b, salida = _sumador_vivo(a, b)
    display(widgets.VBox([widgets.HBox(botones_a),
                          widgets.HBox(botones_b),
                          salida]))
```

- [ ] **Step 4: Correr las pruebas**

Run: `pytest tests/test_compuertas.py -q`
Expected: PASS, treinta y ocho tests.

- [ ] **Step 5: Mirar el dibujo**

```bash
python3 - <<'PY'
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shift_enter import compuertas
from shift_enter.binario import a_binario
for a, b in ((13, 29), (255, 1), (170, 85), (0, 0)):
    compuertas._dibujar_sumador(a_binario(a), a_binario(b))
    plt.savefig(f"/tmp/sumador_{a}_{b}.png", dpi=110)
    plt.close("all")
print("listo: /tmp/sumador_*.png")
PY
```

Confirma que en 255 más 1 las siete flechas de llevo están encendidas y la fila
de la suma está toda apagada, y que en 13 más 29 el resultado dice 42.

- [ ] **Step 6: Correr la suite completa**

Run: `pytest -q`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add shift_enter/compuertas.py tests/test_compuertas.py
git commit -m "feat: el sumador de ocho columnas que se arma con el dedo"
```

---

### Task 7: `cifra.py`, el salto y el carácter que no se dibuja

Tres cosas: `correr` se vuelve pública porque se muda desde la celda visible,
todo lo que se llamaba desplazamiento o corrimiento pasa a llamarse salto, y el
bug del glyph 20 se arregla en el dibujo.

**Files:**
- Modify: `shift_enter/cifra.py`
- Modify: `tests/test_cifra.py`

**Interfaces:**
- Consumes: `paleta.ENCENDIDO`, `paleta.TENUE`.
- Produces:
  - `correr(texto, salto) -> str`
  - `SALTO_RETO = 5`, `MENSAJE_RETO`, `ALFABETO` (sin cambios de valor)
  - `_imprimible(texto) -> str`
  - `disco(mensaje, salto, ax=None) -> Axes`
  - `deslizador_disco(mensaje) -> None`
  - `DESPLAZAMIENTO_RETO` y `_corrido` dejan de existir.

- [ ] **Step 1: Reescribir las pruebas**

Reemplaza `tests/test_cifra.py` entero:

```python
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


def test_el_disco_escribe_el_salto_en_la_figura():
    eje = cifra.disco(cifra.MENSAJE_RETO, 17)
    textos = [t.get_text() for t in eje.texts]
    assert "salto: 17" in textos


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
```

- [ ] **Step 2: Correr para verificar que fallan**

Run: `pytest tests/test_cifra.py -q`
Expected: FAIL con `AttributeError: module 'shift_enter.cifra' has no attribute 'correr'`.

- [ ] **Step 3: Reescribir el módulo**

Reemplaza `shift_enter/cifra.py` entero:

```python
"""El disco cifrador de Julio Cesar."""

import ipywidgets as widgets
import matplotlib.pyplot as plt
from ipywidgets import interact

from .paleta import ENCENDIDO, TENUE

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SALTO_RETO = 5
MENSAJE_RETO = "QF%UNJIWF%^F%HZJSYF"

# El espacio cifrado es '%'. Al restarle ciertos saltos cae en caracteres de
# control, que la fuente no sabe dibujar y que hacen que matplotlib avise
# "Glyph 20 missing from font". El mensaje tiene que seguir corriendose
# completo, porque de ahi sale la pregunta que cierra la parte 1, asi que la
# correccion va aqui, al pintar.
SIN_DIBUJO = "▯"


def correr(texto, salto):
    """Le suma el salto al numero de cada letra."""
    return "".join(chr(ord(letra) + salto) for letra in texto)


def _imprimible(texto):
    """Cambia por un recuadro cualquier caracter que la fuente no dibuje."""
    return "".join(letra if 32 <= ord(letra) < 127 else SIN_DIBUJO
                   for letra in texto)


def _deslizador_de_salto():
    """El deslizador del salto, ancho y rotulado en espanol de Mexico."""
    return widgets.IntSlider(min=0, max=25, value=0, description="salto",
                             continuous_update=False,
                             layout=widgets.Layout(width="620px"))


def disco(mensaje, salto, ax=None):
    """Las dos tiras del alfabeto y el mensaje descifrandose."""
    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(13, 3.8))

    abajo = ALFABETO[salto % 26:] + ALFABETO[:salto % 26]
    for i, (arriba_letra, abajo_letra) in enumerate(zip(ALFABETO, abajo)):
        ax.text(i, 1.0, arriba_letra, ha="center", va="center",
                fontsize=13, family="monospace", color=TENUE)
        ax.text(i, 0.45, abajo_letra, ha="center", va="center",
                fontsize=13, family="monospace", weight="bold")
    ax.text(-1.6, 1.0, "cifrado", ha="right", va="center", fontsize=10, color=TENUE)
    ax.text(-1.6, 0.45, "de verdad", ha="right", va="center", fontsize=10, color=TENUE)

    ax.text(-1.6, -0.55, f"salto: {salto}", ha="right", va="center",
            fontsize=15, weight="bold", family="monospace")

    ax.text(12.5, -0.55, _imprimible(correr(mensaje, -salto)),
            ha="center", va="center",
            fontsize=22, family="monospace", weight="bold", color=ENCENDIDO,
            bbox=dict(facecolor="#2b2b2b", edgecolor="none", pad=10))

    ax.set_xlim(-6, 27)
    ax.set_ylim(-1.2, 1.5)
    ax.axis("off")
    if propia:
        plt.tight_layout()
        plt.show()
    return ax


def deslizador_disco(mensaje):
    """Arrastra el salto y mira el mensaje volverse espanol."""
    @interact(salto=_deslizador_de_salto())
    def _(salto):
        disco(mensaje, salto)
```

Nota sobre el test del salto en la figura: `disco` con `ax=None` llama a
`plt.show()`, y en la suite eso es inerte porque `conftest.py` fija el backend
Agg. El eje devuelto conserva sus textos.

- [ ] **Step 4: Correr las pruebas**

Run: `pytest tests/test_cifra.py -q`
Expected: PASS, trece tests.

- [ ] **Step 5: Confirmar que la advertencia de la fuente ya no sale**

Run:

```bash
python3 -W error::UserWarning - <<'PY'
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shift_enter import cifra
for salto in range(26):
    cifra.disco(cifra.MENSAJE_RETO, salto)
    plt.savefig("/dev/null")
    plt.close("all")
print("sin advertencias en los veintiseis saltos")
PY
```

Expected: imprime la línea final. Si truena con `UserWarning: Glyph ...
missing from font`, `_imprimible` no está cubriendo algún caso.

- [ ] **Step 6: Correr la suite completa**

Run: `pytest -q`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add shift_enter/cifra.py tests/test_cifra.py
git commit -m "fix: el disco cifrador deja de mandar caracteres sin dibujo a la fuente"
```

---

### Task 8: `interruptores.py`, los widgets sin gráfica

El tablero y el contador pierden su cuadro fijo. El contador gana un slider
ancho y un solo botón de play que se convierte en pausa. `dibujar_palabra` pasa
de una figura por letra a una sola figura de un renglón por letra, porque
Fernanda tiene ocho letras y hoy serían ocho pantallazos de scroll.

**Files:**
- Modify: `shift_enter/interruptores.py`
- Modify: `tests/test_tablero.py`
- Modify: `tests/test_interruptores.py`

**Interfaces:**
- Consumes: `binario.TABLA_DE_VALORES`, `binario.a_binario`, `binario.a_decimal`,
  `binario.NoCabe`.
- Produces:
  - `_siguiente(valor, desde, hasta) -> int`, que da la vuelta al llegar al tope
  - `_tablero(valor_inicial=0) -> (list[ToggleButton], HTML)` (sin cambio de firma)
  - `_contador(desde=0, hasta=255, ms=200) -> (ToggleButton, IntSlider, HTML)`.
    El primer elemento pasa de ser un `widgets.Play` a ser el botón de play.
  - `tablero(valor_inicial=0) -> None`, `contador(desde=0, hasta=255, ms=200) -> None`
  - `dibujar_palabra(texto) -> Axes`, ahora devuelve el eje único

- [ ] **Step 1: Reescribir las pruebas de los widgets**

En `tests/test_tablero.py`, reemplaza `test_el_contador_va_de_cero_a_doscientos_cincuenta_y_cinco`
y `test_los_juguetes_dejan_un_cuadro_fijo_antes_del_widget` por:

```python
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
    play, deslizador, salida = interruptores._contador(ms=5000)
    play.value = True
    try:
        assert play.description == "pausa"
    finally:
        play.value = False
    assert play.description == "play"


def test_el_contador_da_la_vuelta_al_llegar_al_tope():
    assert interruptores._siguiente(254, 0, 255) == 255
    assert interruptores._siguiente(255, 0, 255) == 0
    assert interruptores._siguiente(0, 0, 255) == 1


def test_los_juguetes_no_dejan_cuadro_fijo_antes_del_widget(monkeypatch):
    # Colab es el unico blanco: la celda se corre siempre, asi que ya no hay
    # que dibujar nada para quien la lea sin ejecutarla.
    dibujados = []
    monkeypatch.setattr(interruptores, "dibujar",
                        lambda *a, **k: dibujados.append(a))
    interruptores.tablero(valor_inicial=5)
    interruptores.contador()
    assert dibujados == []
```

En `tests/test_interruptores.py`, reemplaza
`test_dibujar_palabra_no_revienta_con_un_emoji` por:

```python
def test_dibujar_palabra_deja_todas_las_letras_en_una_sola_figura():
    eje = interruptores.dibujar_palabra("Fernanda")
    # Ocho letras por ocho interruptores cada una.
    assert len(eje.patches) == 8 * 8


def test_dibujar_palabra_rotula_cada_letra_con_su_numero():
    eje = interruptores.dibujar_palabra("Ab")
    textos = [t.get_text() for t in eje.texts]
    assert "A   →   65" in textos
    assert "b   →   98" in textos


def test_dibujar_palabra_no_revienta_con_un_emoji():
    eje = interruptores.dibujar_palabra("A\U0001faa8")
    textos = [t.get_text() for t in eje.texts]
    assert any("no cabe" in t or "interruptores" in t for t in textos)
```

- [ ] **Step 2: Correr para verificar que fallan**

Run: `pytest tests/test_tablero.py tests/test_interruptores.py -q`
Expected: FAIL con `AttributeError: ... has no attribute '_siguiente'` y con
`TypeError` en `dibujar_palabra`, que hoy devuelve `None`.

- [ ] **Step 3: Implementar**

En `shift_enter/interruptores.py`:

Agrega `import threading` y `import time` al inicio, junto a los imports que ya
están.

Reemplaza `dibujar_palabra` completa por:

```python
def dibujar_palabra(texto, ax=None):
    """Cada letra de un texto, en ocho interruptores, todas en una figura."""
    letras = list(texto)
    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(9.5, 0.95 * len(letras) + 0.8))

    for fila, letra in enumerate(letras):
        y = -fila
        numero = ord(letra)
        try:
            bits = a_binario(numero)
        except NoCabe as no_cabe:
            ax.text(0, y, f"{letra}  →  {numero}   {no_cabe}",
                    ha="left", va="center", fontsize=11, color=TENUE)
            continue
        ax.text(-1.2, y, f"{letra}   →   {numero}", ha="right", va="center",
                fontsize=12, family="monospace")
        for i, bit in enumerate(bits):
            ax.add_patch(plt.Circle((i, y), 0.33, zorder=2, linewidth=1.5,
                                    facecolor=ENCENDIDO if bit else APAGADO,
                                    edgecolor=BORDE))

    for i, valor in enumerate(TABLA_DE_VALORES):
        ax.text(i, 0.85, str(valor), ha="center", va="center",
                fontsize=9, color=TENUE)

    ax.set_xlim(-5.2, 7.7)
    ax.set_ylim(-len(letras) + 0.3, 1.3)
    ax.set_aspect("equal")
    ax.axis("off")
    if propia:
        plt.tight_layout()
        plt.show()
    return ax
```

Reemplaza `tablero` completa por:

```python
def tablero(valor_inicial=0):
    """Ocho interruptores que prendes con el dedo."""
    botones, marcador = _tablero(valor_inicial)
    display(widgets.VBox([widgets.HBox(botones), marcador]))
```

Reemplaza `_contador` y `contador` completas por:

```python
def _siguiente(valor, desde, hasta):
    """El numero que sigue, dando la vuelta al llegar al tope."""
    return desde if valor + 1 > hasta else valor + 1


def _contador(desde=0, hasta=255, ms=200):
    """Construye el contador con su boton de play. Version interna."""
    deslizador = widgets.IntSlider(value=desde, min=desde, max=hasta,
                                   description="número",
                                   layout=widgets.Layout(width="620px"))
    play = widgets.ToggleButton(value=False, description="play", icon="play",
                                layout=widgets.Layout(width="100px"))
    salida = widgets.HTML()

    def pintar(cambio):
        n = cambio["new"]
        salida.value = (f"{como_html(a_binario(n), TABLA_DE_VALORES)}"
                        f"<div style='font-size:40px;font-weight:bold'>{n}</div>")

    deslizador.observe(pintar, names="value")
    pintar({"new": desde})

    def avanzar():
        # ipywidgets no trae un boton de play solo: el suyo son tres botones
        # pegados. Este hilo es lo que lo sustituye. Es demonio, asi que no
        # deja al kernel colgado si alguien cierra la pestana con el play
        # prendido.
        while play.value:
            deslizador.value = _siguiente(deslizador.value, desde, hasta)
            time.sleep(ms / 1000)

    def al_presionar(cambio):
        if cambio["new"]:
            play.description, play.icon = "pausa", "pause"
            threading.Thread(target=avanzar, daemon=True).start()
        else:
            play.description, play.icon = "play", "play"

    play.observe(al_presionar, names="value")
    return play, deslizador, salida


def contador(desde=0, hasta=255, ms=200):
    """Miralos contar solos, del 0 al 255."""
    play, deslizador, salida = _contador(desde, hasta, ms)
    display(widgets.VBox([widgets.HBox([play, deslizador]), salida]))
```

- [ ] **Step 4: Correr las pruebas**

Run: `pytest tests/test_tablero.py tests/test_interruptores.py -q`
Expected: PASS.

- [ ] **Step 5: Confirmar que el hilo del play no deja nada colgado**

Run:

```bash
python3 - <<'PY'
import matplotlib, threading, time
matplotlib.use("Agg")
from shift_enter import interruptores
play, deslizador, salida = interruptores._contador(ms=20)
antes = deslizador.value
play.value = True
time.sleep(0.3)
play.value = False
time.sleep(0.1)
vivos = [h for h in threading.enumerate() if h is not threading.main_thread()]
print("avanzo:", deslizador.value != antes)
print("hilos vivos al soltar el play:", vivos)
PY
```

Expected: `avanzo: True` y una lista de hilos vacía.

- [ ] **Step 6: Correr la suite completa**

Run: `pytest -q`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add shift_enter/interruptores.py tests/test_tablero.py tests/test_interruptores.py
git commit -m "feat: los widgets sin grafica, con play propio y el nombre en una figura"
```

---

### Task 9: Los cuadros fijos que quedan

`imagen.deslizador_brillo`, `imagen.mezclador_color` y
`sonido.deslizador_de_tono` siguen dibujando un cuadro fijo antes de su widget,
por la misma razón que ya no aplica.

**Files:**
- Modify: `shift_enter/imagen.py`
- Modify: `shift_enter/sonido.py`
- Modify: `tests/test_imagen_widgets.py`
- Modify: `tests/test_sonido.py`

**Interfaces:**
- Consumes: nada nuevo.
- Produces: las tres funciones conservan su firma y dejan de llamar al
  dibujante antes del `@interact`.

- [ ] **Step 1: Dar la vuelta a las pruebas**

En `tests/test_imagen_widgets.py`, reemplaza los dos últimos tests por:

```python
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
```

En `tests/test_sonido.py`, reemplaza
`test_deslizador_de_tono_deja_un_cuadro_fijo_antes_del_widget` por:

```python
def test_deslizador_de_tono_no_deja_cuadro_fijo_antes_del_widget(monkeypatch):
    llamadas = []
    monkeypatch.setattr(sonido, "dibujar_onda", lambda *a, **k: llamadas.append((a, k)))
    monkeypatch.setattr(sonido, "reproducir", lambda *a, **k: None)
    sonido.deslizador_de_tono()
    assert len(llamadas) == 0
```

Nota: `deslizador_de_tono` no dibuja dentro del `@interact`, solo reproduce, así
que al quitar su cuadro fijo quedan cero llamadas a `dibujar_onda`, no una.

- [ ] **Step 2: Correr para verificar que fallan**

Run: `pytest tests/test_imagen_widgets.py tests/test_sonido.py -q`
Expected: FAIL, tres tests, con `assert 2 == 1` y `assert 1 == 0`.

- [ ] **Step 3: Borrar los cuadros fijos**

En `shift_enter/imagen.py`, borra de `deslizador_brillo` el comentario de tres
líneas y la línea `mostrar(arreglo, titulo="foto + (0)")`. Borra de
`mezclador_color` el comentario de tres líneas y la línea
`_dibujar_muestra(200, 90, 30)`.

En `shift_enter/sonido.py`, borra de `deslizador_de_tono` el comentario de tres
líneas y la línea `dibujar_onda(onda(440), etiquetas=["440 Hz"])`.

- [ ] **Step 4: Correr las pruebas**

Run: `pytest -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add shift_enter/imagen.py shift_enter/sonido.py \
        tests/test_imagen_widgets.py tests/test_sonido.py
git commit -m "refactor: ningun widget dibuja un cuadro fijo antes de si mismo"
```

---

### Task 10: `torre.py`, sin símbolos de párrafo y con el cronómetro adentro

La torre nombra las secciones con `§`, que hay que quitar, y llama a las
compuertas NO, Y y O, que ahora se llaman NOT, AND y OR. Y se lleva el
cronómetro que hoy está escrito a mano en la celda de la parte seis, porque
medir es plomería.

**Files:**
- Modify: `shift_enter/torre.py`
- Modify: `tests/test_torre.py`

**Interfaces:**
- Consumes: `compuertas.sumar` de la Tarea 2.
- Produces:
  - `LAS_CAPAS`, misma forma, textos nuevos
  - `comparar_velocidad(a=13, b=29, veces=300) -> (float, float)` como
    `(segundos_del_tuyo, segundos_del_de_python)`
  - `dibujar(capas=None, ax=None) -> Axes` (sin cambios)

- [ ] **Step 1: Escribir las pruebas que fallan**

Agrega a `tests/test_torre.py`:

```python
def test_la_torre_no_usa_simbolos_de_parrafo():
    for nombre, detalle in torre.LAS_CAPAS:
        assert "§" not in nombre
        assert "§" not in detalle


def test_la_torre_nombra_las_compuertas_como_se_llaman_de_verdad():
    detalles = " ".join(detalle for _, detalle in torre.LAS_CAPAS)
    assert "NOT, AND, OR" in detalles


def test_la_torre_manda_al_alumno_a_las_partes_por_su_nombre():
    detalles = " ".join(detalle for _, detalle in torre.LAS_CAPAS)
    assert "parte 5" in detalles
    assert "parte 4" in detalles


def test_comparar_velocidad_devuelve_dos_tiempos():
    tuyo, de_python = torre.comparar_velocidad(veces=5)
    assert tuyo > 0
    assert de_python > 0


def test_el_sumador_a_mano_es_mas_lento_que_el_de_python():
    tuyo, de_python = torre.comparar_velocidad(veces=20)
    assert tuyo > de_python
```

- [ ] **Step 2: Correr para verificar que fallan**

Run: `pytest tests/test_torre.py -q`
Expected: FAIL con `assert '§' not in ...` y
`AttributeError: module 'shift_enter.torre' has no attribute 'comparar_velocidad'`.

- [ ] **Step 3: Implementar**

En `shift_enter/torre.py`, agrega `import time` al inicio y
`from .compuertas import sumar` debajo de los imports.

Reemplaza `LAS_CAPAS` por:

```python
LAS_CAPAS = [
    ("Arena y electricidad", "física. Aquí no hay ideas todavía"),
    ("Transistor", "un interruptor sin partes móviles"),
    ("Compuerta", "NOT, AND, OR        ← lo armaste en la parte 5"),
    ("Bit", "prendido o apagado  ← parte 4"),
    ("Byte", "ocho bits: un número, una letra, un pixel  ← partes 1, 2 y 4"),
    ("Sumador", "13 + 29 = 42        ← parte 5"),
    ("Instrucción", "lo único que el procesador entiende"),
    ("Python", "el + que usaste sin pensarlo"),
    ("Esta celda", "aquí estás tú"),
]
```

Y agrega al final del módulo:

```python
def comparar_velocidad(a=13, b=29, veces=300):
    """Cronometra el sumador de compuertas contra el + que trae Python."""
    inicio = time.perf_counter()
    for _ in range(veces):
        sumar(a, b)
    tuyo = (time.perf_counter() - inicio) / veces

    muchas = veces * 1000
    inicio = time.perf_counter()
    for _ in range(muchas):
        a + b
    de_python = (time.perf_counter() - inicio) / muchas

    print(f"   tu sumador:      {tuyo * 1e6:>10.1f} microsegundos")
    print(f"   el + de Python:  {de_python * 1e6:>10.4f} microsegundos")
    print()
    print(f"   El tuyo es unas {tuyo / de_python:,.0f} veces más lento.")
    return tuyo, de_python
```

- [ ] **Step 4: Correr las pruebas**

Run: `pytest tests/test_torre.py -q`
Expected: PASS.

- [ ] **Step 5: Barrer el paquete entero en busca de vocabulario prohibido**

Run:

```bash
grep -rn 'basura\|corrimiento\|desplazamiento\|inútil\|aburrido\|§' shift_enter/ || echo "el paquete esta limpio"
```

Expected: `el paquete esta limpio`.

- [ ] **Step 6: Correr la suite completa**

Run: `pytest -q`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add shift_enter/torre.py tests/test_torre.py
git commit -m "refactor: la torre sin simbolos de parrafo y con el cronometro adentro"
```

---

### Task 11: La notebook, taller y partes 1 a 3

De aquí en adelante se edita el JSON de la notebook con scripts, nunca a mano, y
se re-ejecuta hasta la Tarea 15. Guarda un respaldo antes de la primera
edición.

**Files:**
- Modify: `la-piedra-que-aprendio-a-contar.ipynb`

**Interfaces:**
- Consumes: `cifra.correr`, `cifra.MENSAJE_RETO`, `cifra.deslizador_disco` de la
  Tarea 7.
- Produces: la notebook con el taller sin `pio`, la parte 1 con Fernanda y el
  salto, la parte 2 con la carita de dieciséis por dieciséis, y la parte 3 con
  las unidades en el cierre.

- [ ] **Step 1: Respaldar y escribir el ayudante de edición**

```bash
cp la-piedra-que-aprendio-a-contar.ipynb /tmp/piedra-respaldo.ipynb
```

Crea `/tmp/editar.py`, que las tareas 11 a 14 van a importar:

```python
"""Ayudante para editar la notebook por contenido y no por indice.

Los indices se recorren en cuanto se agrega o se borra una celda, asi que
todas las ediciones buscan la celda por un fragmento unico de su texto.
"""

import nbformat

RUTA = "la-piedra-que-aprendio-a-contar.ipynb"


def abrir():
    return nbformat.read(RUTA, as_version=4)


def guardar(nb):
    nbformat.write(nb, RUTA)


def indice(nb, fragmento):
    """El indice de la unica celda que contiene el fragmento."""
    encontrados = [i for i, c in enumerate(nb.cells) if fragmento in c.source]
    if len(encontrados) != 1:
        raise SystemExit(f"{fragmento!r} aparece {len(encontrados)} veces, no una")
    return encontrados[0]


def reemplazar(nb, fragmento, texto_nuevo):
    """Cambia el contenido completo de la celda que contiene el fragmento."""
    nb.cells[indice(nb, fragmento)].source = texto_nuevo.strip("\n")


def borrar(nb, fragmento):
    del nb.cells[indice(nb, fragmento)]
```

- [ ] **Step 2: Editar el taller y las partes 1 a 3**

Corre este script desde la raíz del repo:

```bash
python3 - <<'PY'
import sys; sys.path.insert(0, "/tmp")
from editar import abrir, guardar, reemplazar, indice

nb = abrir()

# --- La promesa: el alumno ya no escribe el sumador, lo arma con el dedo ---
reemplazar(nb, "## 🎯 La promesa", """
## 🎯 La promesa

**Hoy vas a abrir tu nombre, tu foto y tu música por dentro, y vas a descubrir
que las tres son la misma cosa: números.**

Y al final vas a armar con el dedo, interruptor por interruptor, la pieza de la
computadora que suma esos números, sin que aparezca ni una sola vez el signo `+`.
""")

# --- El taller: fuera plotly.io y fuera time; entra compuertas ---
taller = nb.cells[indice(nb, "#@title 🔧 Prepara el taller")]
fuente = taller.source
fuente = fuente.replace("import subprocess\nimport sys\nimport time\n",
                        "import subprocess\nimport sys\n")
fuente = fuente.replace("\nimport plotly.io as pio\n", "\n")
fuente = fuente.replace(
    "from shift_enter import cifra, imagen, interruptores, paleta, sonido, torre",
    "from shift_enter import (cifra, compuertas, imagen, interruptores, paleta,\n"
    "                         sonido, torre)")
fuente = fuente.replace(
    "from shift_enter.binario import TABLA_DE_VALORES, a_binario, a_decimal\n"
    "from shift_enter.interruptores import simbolo\n",
    "from shift_enter.binario import TABLA_DE_VALORES, a_binario, a_decimal\n")
fuente = fuente.replace(
    "\n# Sin esto, plotly incrusta su libreria entera (~15 MB) en cada figura.\n"
    "# Con esto solo se incrusta una vez por CDN: mimetype para Colab y\n"
    "# JupyterLab, connected como respaldo en HTML si algun dia dejan de leerlo.\n"
    "pio.renderers.default = \"plotly_mimetype+notebook_connected\"\n",
    "\n# Nada de fijar el renderer de plotly: Colab lo detecta solo, y ponerle\n"
    "# otro encima es lo que dejaba en blanco la foto por dentro.\n")
taller.source = fuente

# --- Parte 1 ---
reemplazar(nb, "# 1 · Tu nombre ya está adentro", """
---

# 1 · Tu nombre es una lista de números

Escribe tu nombre. Está guardado en esta computadora ahorita mismo.

No como letras. Aquí adentro no hay letras. Solo hay números.
""")

reemplazar(nb, 'mi_nombre = "Ada"', """
mi_nombre = "Fernanda"    # ← pon el tuyo

for letra in mi_nombre:
    print(letra, "→", ord(letra))
""")

reemplazar(nb, "Ese número no es un apodo", """
Ese número no es un apodo ni una traducción. **Es** la letra. Es lo único que
hay de tu nombre dentro de la máquina.

Puedes volver a esa celda cuando quieras, poner otro nombre y correr otra vez
de ahí para abajo. Todo lo que sigue se hace con el nombre que dejes escrito.

Y si tu nombre es una lista de números, entonces se puede escuchar.
""")

reemplazar(nb, "Ese `correr` de aquí abajo ya está completo", """
### 🔧 Prueba tú

Ahora súmale un número a cada letra de tu nombre y mira qué sale. El `salto` de
aquí abajo dice cuántos lugares se recorre cada letra. Cámbialo y vuelve a
correr la celda.
""")

reemplazar(nb, "def correr(texto, cuanto)", """
salto = 3    # ← cámbialo

secreto = cifra.correr(mi_nombre, salto)
print("   cifrado:   ", secreto)
print("   descifrado:", cifra.correr(secreto, -salto))
""")

reemplazar(nb, "sus enemigos veían basura", """
Julio César mandaba sus órdenes militares así, hace dos mil años. Le sumaba un
número a cada letra, y quien interceptaba el mensaje se quedaba viendo letras
que no decían nada.

Tú lo acabas de hacer con una suma.
""")

reemplazar(nb, "Arrastra el corrimiento", """
### 🎯 El reto

Aquí hay un mensaje cifrado. Nadie te va a decir con qué número.

Arrastra el salto hasta que el mensaje se vuelva español.
""")

# --- Parte 2: la carita de dieciseis por dieciseis ---
reemplazar(nb, "mi_dibujo = ", '''
mi_dibujo = """
.....######.....
...##......##...
..#..........#..
.#............#.
.#............#.
#....##..##....#
#....##..##....#
#....##..##....#
#..............#
#..............#
#..#........#..#
.#..#......#..#.
.#...######...#.
..#..........#..
...##......##...
.....######.....
"""

imagen.mostrar(imagen.desde_texto(mi_dibujo), titulo="lo que escribiste")
''')

# --- Parte 3: el cierre gana las unidades ---
reemplazar(nb, "Eso es un acorde de do mayor", """
### Lo que llevas

Eso es un acorde de do mayor. No lo compusiste: lo **sumaste**.

Tu nombre, tu cara y ese acorde entraron a la máquina y se convirtieron en lo
mismo: listas de números.

Y a los tres les hiciste exactamente la misma cosa para cambiarlos. Le sumaste
tres lugares del alfabeto a cada letra de tu nombre. Le sumaste setenta niveles
de luz a cada pixel de tu foto. Le sumaste dos ondas más a la primera onda.

Por eso una sola máquina puede tocar música, editar fotos y guardar mensajes. No
tiene tres talentos. Tiene uno.
""")

guardar(nb)
print("partes 1 a 3 editadas")
PY
```

- [ ] **Step 3: Confirmar que las ediciones entraron**

Run:

```bash
python3 - <<'PY'
import json
fuente = "\n".join("".join(c["source"]) for c in
                   json.load(open("la-piedra-que-aprendio-a-contar.ipynb",
                                  encoding="utf-8"))["cells"])
for debe_estar in ("Fernanda", "cifra.correr", "salto = 3",
                   "Tu nombre es una lista de números", "#....##..##....#",
                   "tres lugares del alfabeto", "compuertas"):
    assert debe_estar in fuente, debe_estar
# 'basura' y 'simbolo' viven todavia en la parte 5, que se reescribe en la
# Tarea 13. Aqui solo se verifica lo que esta tarea si tenia que retirar.
for no_debe in ('mi_nombre = "Ada"', "def correr(", "sus enemigos veían basura",
                "corrimiento", "pio.", "import time"):
    assert no_debe not in fuente, no_debe
print("partes 1 a 3 verificadas")
PY
```

Expected: `partes 1 a 3 verificadas`.

- [ ] **Step 4: Commit**

```bash
git add la-piedra-que-aprendio-a-contar.ipynb
git commit -m "feat: partes 1 a 3 con Fernanda, el salto y la carita de 16x16"
```

---

### Task 12: La notebook, parte 4

La apertura que hoy termina en que ninguno sabe sumar, el Leibniz que escribió
en un papel y el juguete inútil, la referencia con símbolo de párrafo.

**Files:**
- Modify: `la-piedra-que-aprendio-a-contar.ipynb`

**Interfaces:**
- Consumes: `interruptores.tablero`, `interruptores.contador`,
  `interruptores.dibujar_palabra` de la Tarea 8.
- Produces: la parte 4 con la apertura reescrita y sin vocabulario prohibido.

- [ ] **Step 1: Editar la parte 4**

```bash
python3 - <<'PY'
import sys; sys.path.insert(0, "/tmp")
from editar import abrir, guardar, reemplazar

nb = abrir()

reemplazar(nb, "Toma un puñado de arena de playa", """
---

# 4 · ¿Y cómo cabe todo eso en una piedra?

Toma un puñado de arena de playa. Es dióxido de silicio: lo mismo de lo que
está hecho el vidrio de una ventana.

Derrítela. Purifícala hasta que de cada mil millones de átomos solo uno sea de
otra cosa. Te queda un cristal gris que cabe en tu mano.

Ahora graba en su superficie algo miles de veces más delgado que un cabello,
que hace **una sola cosa**: deja pasar la electricidad, o no la deja.

Eso es un **transistor**. Un interruptor sin partes móviles, que se prende y se
apaga mil millones de veces por segundo y nunca se cansa.

En el aparato donde estás leyendo esto hay varios **miles de millones**. Cada
uno, por su cuenta, solo sabe estar prendido o apagado.

Juntos están corriendo esta página ahorita mismo.
""")

reemplazar(nb, "Fue un juguete inútil", """
El interruptor de la derecha se prende y se apaga en cada número. El siguiente,
cada dos. El siguiente, cada cuatro.

Cada uno va exactamente al doble de lento que su vecino de la derecha. Eso es
todo lo que significa contar en binario.

En 1679 Gottfried Leibniz lo escribió a mano, sin computadoras y sin
electricidad. Le pareció bello y ya. Fue un juguete sin ningún uso durante
doscientos setenta años, hasta que alguien conectó unos interruptores y
descubrió que el juguete era exactamente lo que la máquina necesitaba.
""")

reemplazar(nb, "En la §1 tu nombre era una lista", """
### Tu nombre, otra vez

En la parte 1 tu nombre era una lista de números. Así es como está guardado de
verdad.
""")

guardar(nb)
print("parte 4 editada")
PY
```

- [ ] **Step 2: Confirmar**

Run:

```bash
python3 - <<'PY'
import json
fuente = "\n".join("".join(c["source"]) for c in
                   json.load(open("la-piedra-que-aprendio-a-contar.ipynb",
                                  encoding="utf-8"))["cells"])
for debe_estar in ("nunca se cansa", "corriendo esta página",
                   "sin ningún uso", "lo escribió a mano", "En la parte 1"):
    assert debe_estar in fuente, debe_estar
for no_debe in ("aburrido", "absolutamente nada", "inútil", "§", "en un papel"):
    assert no_debe not in fuente, no_debe
print("parte 4 verificada")
PY
```

Expected: `parte 4 verificada`.

- [ ] **Step 3: Commit**

```bash
git add la-piedra-que-aprendio-a-contar.ipynb
git commit -m "feat: la parte 4 cierra en potencia y no en vacio"
```

---

### Task 13: La notebook, parte 5 completa

La sección se reescribe entera. Salen las cinco celdas de código con `def` y
entra la secuencia de widgets. Es la tarea más larga del plan.

**Files:**
- Modify: `la-piedra-que-aprendio-a-contar.ipynb`

**Interfaces:**
- Consumes: `compuertas.probador`, `compuertas.diagrama_xor`,
  `compuertas.medio_sumador_vivo`, `compuertas.sumador_vivo`,
  `compuertas.sumar` de las Tareas 2 a 6; `interruptores.dibujar` y
  `TABLA_DE_VALORES`.
- Produces: la parte 5 sin ningún `def`, con un solo `if` en la celda de
  calificación.

- [ ] **Step 1: Reemplazar la sección**

```bash
python3 - <<'PY'
import sys; sys.path.insert(0, "/tmp")
import nbformat
from editar import abrir, guardar, indice

nb = abrir()

desde = indice(nb, "# 5 · ¿Y quién suma allá abajo?")
hasta = indice(nb, "# 6 · Las capas")

md = nbformat.v4.new_markdown_cell
code = nbformat.v4.new_code_cell

nuevas = [
    md("""---

# 5 · ¿Y quién suma allá abajo? Nadie

Todo lo que hiciste hoy fue sumar. Le sumaste tres lugares del alfabeto a cada
letra de tu nombre. Le sumaste setenta niveles de luz a cada pixel de tu foto.
Sumaste tres ondas y salió un acorde.

Tres cosas que no se parecen en nada, y la misma operación en las tres.

Y allá abajo, adentro de la piedra, no hay nadie que sepa sumar. Solo hay
interruptores prendidos y apagados.

Así que alguien tuvo que enseñarles. Hoy te toca a ti."""),

    md("""### Tres reglas

Un interruptor solo no sirve de mucho. Lo interesante empieza cuando conectas
dos y decides qué pasa con el de salida.

Hay tres formas de conectarlos, y con esas tres se construyó el mundo entero.
Se llaman **compuertas**, y así se llaman de verdad, en cualquier libro y en
cualquier fábrica: **NOT**, **AND** y **OR**.

Préndelas y apágalas con el dedo. La tabla de cada una se ilumina en el renglón
que estás viviendo, y ahí está *todo* lo que puede pasar. No hay caso
escondido."""),

    code("compuertas.probador()"),

    md("""### Una cuarta que no es nueva

Con esas tres se puede construir cualquier otra cosa que haga una computadora.
Cualquiera.

Empecemos por una que se prende cuando los dos interruptores son **distintos**.
Se llama **XOR**, y no es una pieza nueva: es NOT, AND y OR conectadas de cierta
forma.

Mueve los interruptores y mira por dónde pasa la corriente."""),

    code("compuertas.diagrama_xor()"),

    md("""### Las cuatro sumas que existen

Sumar un interruptor más un interruptor. Eso es todo lo que hay:

```
0 + 0 = 0
0 + 1 = 1
1 + 0 = 1
1 + 1 = 10     ← se pasa: escribe 0 y lleva 1
```

Abajo hay dos focos de salida: uno para la suma y otro para el llevo. Recorre
los cuatro casos y fíjate en cuál se prende cada vez."""),

    code("compuertas.medio_sumador_vivo()"),

    md("""La columna de la suma resultó ser **XOR**. La columna del llevo resultó
ser **AND**.

Nadie inventó una pieza nueva para esto. Las dos ya estaban en tu caja."""),

    md("""### Ocho columnas en fila

Cuando sumas 47 más 38 a mano empiezas por la derecha, y lo que llevas cae en la
siguiente columna. Aquí pasa igual: cada columna recibe tres cosas, el
interruptor de arriba, el de abajo, y el llevo que le mandó su vecina de la
derecha.

Ocho columnas encadenadas. Préndelas con el dedo y mira el llevo brincar de una
a otra.

Esto que estás moviendo es, literalmente, una pieza que existe dentro de tu
procesador."""),

    code("compuertas.sumador_vivo()"),

    md("""### ✅ Que se califique solo

Un sumador que acierta una vez pudo tener suerte. Que lo pruebe con **todas** las
sumas posibles de 0 a 127, y que se compare contra el `+` de Python."""),

    code("""aciertos = 0
for a in range(128):
    for b in range(128):
        if a_decimal(compuertas.sumar(a, b)) == a + b:
            aciertos = aciertos + 1

print(f"✅ {aciertos:,} de 16,384 sumas correctas")"""),

    md("""Dieciséis mil trescientas ochenta y cuatro sumas, todas correctas, y en
ningún punto de la cadena aparece el signo `+`.

Ese resultado salió de ocho columnas encadenadas, cada una hecha de dos medios
sumadores y una compuerta OR, cada medio sumador hecho de un XOR y un AND, y el
XOR hecho de NOT, AND y OR.

Hasta abajo de todo no hay más que interruptores prendidos y apagados. 🎯"""),

    md("""### 🔧 Adivina antes de correr

Con ocho interruptores no cabe nada mayor que 255.

¿Qué crees que va a pasar con 255 más 1? Adivina, y luego corre la celda."""),

    code("""interruptores.dibujar(compuertas.sumar(255, 1), etiquetas=TABLA_DE_VALORES,
                      mostrar_bool=False, titulo="255 + 1")"""),

    md("""Todos apagados. Cero.

Eso se llama **desbordamiento**, y no es un detalle académico:

- En **Pac-Man**, el contador de niveles usaba ocho interruptores. Al llegar al
  nivel 256 se desbordó y media pantalla se llenó de símbolos revueltos. Nadie
  pudo pasar de ahí durante años.
- En 1996 el cohete **Ariane 5** se autodestruyó 37 segundos después de despegar.
  Un número no cupo donde lo estaban metiendo. Costó 370 millones de dólares.

Tu sumador tiene exactamente el mismo límite que ellos. No porque esté mal hecho:
porque los interruptores se acaban.

### 🤔 Para pensar

Si un interruptor solo puede estar prendido o apagado, no hay dónde poner el
signo menos. ¿Cómo guardarías un número **negativo**?"""),
]

nb.cells[desde:hasta] = nuevas
guardar(nb)
print(f"parte 5 reemplazada: {hasta - desde} celdas viejas por {len(nuevas)} nuevas")
PY
```

- [ ] **Step 2: Confirmar que no quedó código de funciones**

Run:

```bash
python3 - <<'PY'
import json
celdas = json.load(open("la-piedra-que-aprendio-a-contar.ipynb",
                        encoding="utf-8"))["cells"]
codigo = [(i, "".join(c["source"])) for i, c in enumerate(celdas)
          if c["cell_type"] == "code"
          and c.get("metadata", {}).get("cellView") != "form"]
con_def = [i for i, f in codigo if "def " in f]
con_if = [i for i, f in codigo if "if " in f]
assert con_def == [], f"quedaron def en las celdas {con_def}"
assert len(con_if) == 1, f"se esperaba un solo if, hay {len(con_if)}: {con_if}"
fuente = "\n".join(f for _, f in codigo)
for debe in ("compuertas.probador()", "compuertas.diagrama_xor()",
             "compuertas.medio_sumador_vivo()", "compuertas.sumador_vivo()",
             "compuertas.sumar(255, 1)"):
    assert debe in fuente, debe
# Lo que la Tarea 11 no podia verificar todavia: ambos vivian en la parte 5.
completa = "\n".join("".join(c["source"]) for c in celdas)
assert "simbolo" not in completa
assert "basura" not in completa
print("parte 5 verificada")
PY
```

Expected: `parte 5 verificada`.

- [ ] **Step 3: Commit**

```bash
git add la-piedra-que-aprendio-a-contar.ipynb
git commit -m "feat: la parte 5 se arma con el dedo, sin una linea de codigo a la vista"
```

---

### Task 14: La notebook, parte 6 y cierre

El cronómetro pasa a ser una llamada, y la prosa cambia construiste por armaste
para que siga diciendo la verdad.

**Files:**
- Modify: `la-piedra-que-aprendio-a-contar.ipynb`

**Interfaces:**
- Consumes: `torre.comparar_velocidad`, `torre.dibujar` de la Tarea 10.
- Produces: la parte 6 sin código de medición a la vista.

- [ ] **Step 1: Editar la parte 6**

```bash
python3 - <<'PY'
import sys; sys.path.insert(0, "/tmp")
from editar import abrir, guardar, reemplazar

nb = abrir()

reemplazar(nb, "# 6 · Las capas", """
---

# 6 · Las capas

Tú armaste un sumador con compuertas. Python trae un `+` que ya venía hecho.

Hacen lo mismo. ¿Para qué existen los dos? Corre esto.
""")

reemplazar(nb, "inicio = time.perf_counter()", "torre.comparar_velocidad()")

reemplazar(nb, "Construiste una computadora dentro de una computadora", """
### Por qué

Tu sumador **simula** compuertas usando software, que a su vez corre sobre
compuertas de verdad grabadas en silicio, que hacen la misma operación miles de
millones de veces por segundo.

Armaste una computadora dentro de una computadora. Por eso es lenta, y por eso
valió la pena: pudiste verla por dentro.

El `+` de Python no es más listo que el tuyo. Solo está más abajo en la torre.
""")

guardar(nb)
print("parte 6 editada")
PY
```

- [ ] **Step 2: Confirmar**

Run:

```bash
python3 - <<'PY'
import json
fuente = "\n".join("".join(c["source"]) for c in
                   json.load(open("la-piedra-que-aprendio-a-contar.ipynb",
                                  encoding="utf-8"))["cells"])
assert "torre.comparar_velocidad()" in fuente
assert "perf_counter" not in fuente
assert "Armaste una computadora" in fuente
print("parte 6 verificada")
PY
```

Expected: `parte 6 verificada`.

- [ ] **Step 3: Commit**

```bash
git add la-piedra-que-aprendio-a-contar.ipynb
git commit -m "feat: la parte 6 con el cronometro en el paquete"
```

---

### Task 15: El guardián nuevo, la re-ejecución y la verificación

La notebook ya cumple la regla nueva, así que ahora sí se puede escribir el
guardián que la exige. Después se re-ejecuta y se guardan los resultados.

**Files:**
- Modify: `tests/test_notebook.py`
- Modify: `la-piedra-que-aprendio-a-contar.ipynb`

**Interfaces:**
- Consumes: todo lo anterior.
- Produces: `tests/test_notebook.py` con cuatro tests nuevos que codifican la
  regla invertida, y la notebook re-ejecutada sin errores.

- [ ] **Step 1: Escribir el guardián nuevo**

Agrega a `tests/test_notebook.py`, después de los tests que quedaron:

```python
PROHIBIDAS = ("basura", "corrimiento", "desplazamiento", "inútil",
              "aburrido", "§")


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


def test_la_notebook_no_usa_vocabulario_retirado(celdas):
    fuente = "\n".join("".join(celda["source"]) for celda in celdas)
    ofensivas = [palabra for palabra in PROHIBIDAS if palabra in fuente]
    assert ofensivas == []
```

Y agrega arriba, junto a la constante `NOTEBOOK`:

```python
PAQUETE_COMPUERTAS = Path(__file__).resolve().parents[1] / "shift_enter" / "compuertas.py"
```

- [ ] **Step 2: Correr el guardián nuevo**

Run: `pytest tests/test_notebook.py -q`
Expected: PASS. `test_ninguna_celda_quedo_con_error` sigue pasando porque los
resultados guardados todavía son los viejos; la re-ejecución del paso siguiente
es la que los reemplaza.

- [ ] **Step 3: Re-ejecutar la notebook**

Run:

```bash
python3 -c "
import nbformat
from nbclient import NotebookClient
p = 'la-piedra-que-aprendio-a-contar.ipynb'
nb = nbformat.read(p, as_version=4)
NotebookClient(nb, timeout=300, kernel_name='python3',
               resources={'metadata': {'path': '.'}}).execute()
nbformat.write(nb, p)
"
```

Expected: termina sin excepción. Si truena, `nbclient` deja el archivo intacto:
arregla lo que reportó y vuelve a correr. El respaldo está en
`/tmp/piedra-respaldo.ipynb`.

- [ ] **Step 4: Confirmar que ninguna celda quedó con error**

Run:

```bash
python3 -c "
import json
c = json.load(open('la-piedra-que-aprendio-a-contar.ipynb', encoding='utf-8'))['cells']
print([i for i,x in enumerate(c)
       if any(o.get('output_type')=='error' for o in x.get('outputs', []))] or 'sin errores')
"
```

Expected: `sin errores`.

- [ ] **Step 5: Confirmar que la ejecución no dejó advertencias de fuente**

Run:

```bash
python3 - <<'PY'
import json
celdas = json.load(open("la-piedra-que-aprendio-a-contar.ipynb",
                        encoding="utf-8"))["cells"]
avisos = []
for i, celda in enumerate(celdas):
    for salida in celda.get("outputs", []):
        texto = "".join(salida.get("text", [])) if salida.get("name") else ""
        if "missing from font" in texto or "Glyph" in texto:
            avisos.append(i)
print(avisos or "sin advertencias de fuente")
PY
```

Expected: `sin advertencias de fuente`.

- [ ] **Step 6: Correr la suite completa**

Run: `pytest -q`
Expected: PASS, todo verde.

- [ ] **Step 7: Commit**

```bash
git add tests/test_notebook.py la-piedra-que-aprendio-a-contar.ipynb
git commit -m "test: el guardian ahora exige que el concepto no se escriba, y la notebook se regenera"
```

- [ ] **Step 8: Lo que solo Enrique puede verificar**

Estas tres cosas no se pueden probar aquí, porque no hay Colab en este entorno.
Pásaselas para que las corra:

1. Que la foto por dentro dibuja, con su hover mostrando el número de cada pixel
   y su zoom de dos dedos, tanto con la foto de respaldo como con una foto
   suya recién subida.
2. Que el botón de play del contador anima el slider, que dice pausa mientras
   corre, y que se detiene al volver a presionarlo.
3. Que ninguno de los cuatro widgets nuevos de la parte 5 parpadea de forma
   molesta al mover los interruptores.
