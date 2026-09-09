# Rediseño de «La piedra que aprendió a contar» — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sacar toda la plomería de la notebook a un paquete `shift_enter` instalable y reescribir la notebook con la torre volteada, de modo que un alumno de 12 a 14 años le dé play y el output lo capture.

**Architecture:** Un paquete de Python con seis módulos de plomería, instalado en Colab con una línea escondida en la celda de forma. La notebook se reconstruye con un script generador que vive en `herramientas/` durante el trabajo y se borra al final. El orden de las secciones se invierte: el alumno abre su nombre, su foto y su música por dentro, y solo entonces baja al interruptor y construye el sumador.

**Tech Stack:** Python 3.10 o superior, numpy, matplotlib, plotly, Pillow, ipywidgets, pytest, nbclient, nbformat.

**Spec:** `docs/superpowers/specs/2026-09-09-la-piedra-que-aprendio-a-contar-rediseno-design.md`

## Global Constraints

- **Todo en español**, incluidos identificadores, docstrings y comentarios.
- **Ninguna dependencia nueva.** Colab ya trae `numpy`, `pandas`, `matplotlib`, `seaborn`, `plotly`, `requests`, `Pillow` e `ipywidgets`. No se agrega nada fuera de esa lista.
- **`plotly` aparece exactamente una vez en toda la notebook:** la foto que se recorre con el mouse. Todo lo demás es matplotlib movido con `ipywidgets`.
- **Ninguna celda visible de la notebook contiene código de graficación.** Toda figura sale de una función del paquete.
- **El paquete es plomería y nada más.** `correr`, `NO`, `Y`, `O`, `XOR`, `medio_sumador`, `sumador_completo` y `sumar` se escriben a mano en celdas visibles y nunca entran al paquete.
- **Todo el archivo habla `True` y `False`,** incluidas las listas de bits. Solo los dibujos y los `print` los pintan como 1 y 0.
- **`sumar` devuelve interruptores, no un número.**
- **El nombre de importación es `shift_enter`.** El repo se sigue llamando `shift-enter`.
- **Ancho fijo de ocho interruptores.** Un número que no quepa levanta `NoCabe` con un mensaje en español, nunca revienta con un error de Python.
- **Las salidas se comiten a propósito** para que la notebook se lea en GitHub. Después de cada cambio hay que re-ejecutar con `nbclient` y confirmar que ninguna celda quedó con salida de error.

**Precondiciones que dependen del autor, no del código:**

- El repo `github.com/nrqrmz/shift-enter` tiene que ser **público** antes de que la línea de instalación sirva para un alumno.
- Hay que **unificar la rama**. El repo local está en `master`, el README apunta a `main`. Las tareas de abajo no dependen del resultado, pero la línea de instalación de la Tarea 9 sí.

---

### Task 1: Esqueleto del paquete y la paleta

**Files:**
- Create: `pyproject.toml`
- Create: `shift_enter/__init__.py`
- Create: `shift_enter/paleta.py`
- Test: `tests/test_paleta.py`

**Interfaces:**
- Consumes: nada.
- Produces: el paquete importable `shift_enter`; `shift_enter.paleta.ENCENDIDO`, `APAGADO`, `BORDE`, `TENUE` como cadenas de color, y `aplicar_estilo() -> None`.

- [ ] **Step 1: Escribe la prueba que falla**

```python
# tests/test_paleta.py
from shift_enter import paleta


def test_la_paleta_tiene_los_cuatro_colores():
    assert paleta.ENCENDIDO == "#f5c518"
    assert paleta.APAGADO == "#2b2b2b"
    assert paleta.BORDE == "#8a8a8a"
    assert paleta.TENUE == "0.45"


def test_aplicar_estilo_deja_matplotlib_sin_cuadricula():
    import matplotlib.pyplot as plt

    plt.rcParams["axes.grid"] = True
    paleta.aplicar_estilo()
    assert plt.rcParams["axes.grid"] is False
    assert plt.rcParams["font.size"] == 12
```

- [ ] **Step 2: Corre la prueba y confirma que falla**

Run: `python3 -m pytest tests/test_paleta.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'shift_enter'`

- [ ] **Step 3: Escribe el `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "shift-enter"
version = "0.1.0"
description = "La plomeria de las notebooks de shift-enter"
requires-python = ">=3.10"
dependencies = [
    "numpy",
    "matplotlib",
    "plotly",
    "pillow",
    "ipywidgets",
]

[tool.setuptools.packages.find]
include = ["shift_enter*"]

[tool.setuptools.package-data]
shift_enter = ["datos/*"]
```

- [ ] **Step 4: Escribe el paquete**

```python
# shift_enter/__init__.py
"""La plomeria de las notebooks de shift-enter.

Aqui vive todo lo que dibuja, mide o formatea. Lo que se ensena
se escribe a mano en las celdas visibles de cada notebook.
"""

__version__ = "0.1.0"
```

```python
# shift_enter/paleta.py
"""Los colores del taller y el estilo de las figuras."""

import matplotlib.pyplot as plt

ENCENDIDO = "#f5c518"
APAGADO = "#2b2b2b"
BORDE = "#8a8a8a"
TENUE = "0.45"


def aplicar_estilo():
    """Deja matplotlib listo para toda la notebook."""
    plt.rcParams["figure.figsize"] = (8, 4)
    plt.rcParams["font.size"] = 12
    plt.rcParams["axes.grid"] = False
```

- [ ] **Step 5: Instala el paquete en modo editable**

Run: `python3 -m pip install -e .`
Expected: `Successfully installed shift-enter-0.1.0`

- [ ] **Step 6: Corre la prueba y confirma que pasa**

Run: `python3 -m pytest tests/test_paleta.py -v`
Expected: 2 passed

- [ ] **Step 7: Comitea**

```bash
git add pyproject.toml shift_enter/__init__.py shift_enter/paleta.py tests/test_paleta.py
git commit -m "feat: esqueleto del paquete shift_enter y la paleta"
```

---

### Task 2: El módulo `binario`

**Files:**
- Create: `shift_enter/binario.py`
- Test: `tests/test_binario.py`

**Interfaces:**
- Consumes: nada.
- Produces: `TABLA_DE_VALORES: list[int]` de ocho enteros; `NoCabe(ValueError)`; `a_binario(n: int, ancho: int = 8) -> list[bool]`; `a_decimal(bits) -> int` que acepta booleanos o unos y ceros.

- [ ] **Step 1: Escribe la prueba que falla**

```python
# tests/test_binario.py
import pytest

from shift_enter.binario import TABLA_DE_VALORES, NoCabe, a_binario, a_decimal


def test_a_binario_y_a_decimal_son_inversas_en_todo_el_rango():
    for n in range(256):
        assert a_decimal(a_binario(n)) == n


def test_a_binario_devuelve_booleanos():
    bits = a_binario(5)
    assert bits == [False, False, False, False, False, True, False, True]
    assert all(isinstance(bit, bool) for bit in bits)


def test_a_binario_respeta_el_ancho():
    assert a_binario(3, ancho=4) == [False, False, True, True]


def test_a_binario_avisa_cuando_no_cabe():
    with pytest.raises(NoCabe, match="9 interruptores"):
        a_binario(256)


def test_a_binario_avisa_con_negativos():
    with pytest.raises(NoCabe, match="negativo"):
        a_binario(-1)


def test_a_decimal_acepta_unos_y_ceros():
    assert a_decimal([1, 0, 1]) == 5


def test_tabla_de_valores():
    assert TABLA_DE_VALORES == [128, 64, 32, 16, 8, 4, 2, 1]
```

- [ ] **Step 2: Corre la prueba y confirma que falla**

Run: `python3 -m pytest tests/test_binario.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'shift_enter.binario'`

- [ ] **Step 3: Escribe la implementación**

```python
# shift_enter/binario.py
"""De numeros a interruptores y de vuelta."""

TABLA_DE_VALORES = [128, 64, 32, 16, 8, 4, 2, 1]


class NoCabe(ValueError):
    """El numero necesita mas interruptores de los que hay."""


def a_binario(n, ancho=8):
    """Recibe un numero. Devuelve una lista de True y False, uno por interruptor."""
    if n < 0:
        raise NoCabe(f"{n} es negativo, y en un interruptor no hay donde poner el signo menos.")
    if n >= 2 ** ancho:
        raise NoCabe(f"{n} necesita {n.bit_length()} interruptores y solo tienes {ancho}.")
    return [bool((n >> (ancho - 1 - i)) & 1) for i in range(ancho)]


def a_decimal(bits):
    """Recibe interruptores. Devuelve cuanto valen leidos como numero."""
    valor = 0
    for bit in bits:
        valor = valor * 2 + int(bool(bit))
    return valor
```

- [ ] **Step 4: Corre la prueba y confirma que pasa**

Run: `python3 -m pytest tests/test_binario.py -v`
Expected: 7 passed

- [ ] **Step 5: Comitea**

```bash
git add shift_enter/binario.py tests/test_binario.py
git commit -m "feat: modulo binario con aviso cuando el numero no cabe"
```

---

### Task 3: Los interruptores dibujados

**Files:**
- Create: `shift_enter/interruptores.py`
- Test: `tests/test_interruptores.py`

**Interfaces:**
- Consumes: `shift_enter.paleta.ENCENDIDO/APAGADO/BORDE/TENUE`; `shift_enter.binario.TABLA_DE_VALORES`, `a_binario`, `a_decimal`, `NoCabe`.
- Produces: `simbolo(estado) -> str`; `dibujar(bits, etiquetas=None, titulo=None, mostrar_bool=True, ax=None) -> matplotlib.axes.Axes`; `tabla_de_verdad(nombre, compuerta, entradas=2) -> matplotlib.figure.Figure`; `dibujar_palabra(texto) -> None`.

- [ ] **Step 1: Escribe la prueba que falla**

```python
# tests/test_interruptores.py
import matplotlib
matplotlib.use("Agg")

from shift_enter import interruptores
from shift_enter.binario import TABLA_DE_VALORES


def test_simbolo_distingue_prendido_de_apagado():
    assert interruptores.simbolo(True) == "●"
    assert interruptores.simbolo(False) == "○"
    assert interruptores.simbolo(1) == "●"


def test_dibujar_acepta_un_solo_interruptor():
    eje = interruptores.dibujar(True)
    assert eje is not None


def test_dibujar_pinta_un_circulo_por_bit():
    eje = interruptores.dibujar([True, False, True], etiquetas=[4, 2, 1])
    assert len(eje.patches) == 3


def test_tabla_de_verdad_de_una_entrada_tiene_dos_casos():
    figura = interruptores.tabla_de_verdad("NO", lambda a: not a, entradas=1)
    ejes = figura.axes[0]
    assert len(ejes.patches) == 4  # dos entradas y dos salidas


def test_dibujar_palabra_no_revienta_con_un_emoji():
    interruptores.dibujar_palabra("A\U0001faa8")


def test_la_tabla_de_valores_sigue_siendo_de_ocho():
    assert len(TABLA_DE_VALORES) == 8
```

- [ ] **Step 2: Corre la prueba y confirma que falla**

Run: `python3 -m pytest tests/test_interruptores.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'shift_enter.interruptores'`

- [ ] **Step 3: Escribe la implementación**

```python
# shift_enter/interruptores.py
"""Interruptores: dibujados, y prendibles con el dedo."""

import matplotlib.pyplot as plt

from .binario import TABLA_DE_VALORES, NoCabe, a_binario
from .paleta import APAGADO, BORDE, ENCENDIDO, TENUE

PRENDIDO = "●"
APAGADO_SIMBOLO = "○"


def simbolo(estado):
    """Un interruptor, en texto. Acepta True/False o 1/0."""
    return PRENDIDO if estado else APAGADO_SIMBOLO


def dibujar(bits, etiquetas=None, titulo=None, mostrar_bool=True, ax=None):
    """Dibuja uno o varios interruptores como focos."""
    if not isinstance(bits, (list, tuple)):
        bits = [bits]
    bits = [int(bool(b)) for b in bits]
    n = len(bits)

    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(1.05 * n + 0.6, 2.4 if mostrar_bool else 2.0))

    for i, b in enumerate(bits):
        ax.add_patch(plt.Circle((i, 0), 0.36, zorder=2, linewidth=1.6,
                                facecolor=ENCENDIDO if b else APAGADO, edgecolor=BORDE))
        ax.text(i, -0.72, str(b), ha="center", va="center",
                fontsize=15, weight="bold", family="monospace")
        if mostrar_bool:
            ax.text(i, -1.10, "True" if b else "False", ha="center", va="center",
                    fontsize=9, color=TENUE, family="monospace")
        if etiquetas is not None:
            ax.text(i, 0.68, str(etiquetas[i]), ha="center", va="center",
                    fontsize=10, color="0.35")

    ax.set_xlim(-0.7, n - 0.3)
    ax.set_ylim(-1.45 if mostrar_bool else -1.1, 1.0)
    ax.set_aspect("equal")
    ax.axis("off")
    if titulo:
        ax.set_title(titulo, fontsize=13, pad=10)
    if propia:
        plt.tight_layout()
        plt.show()
    return ax


def tabla_de_verdad(nombre, compuerta, entradas=2):
    """Todo lo que puede pasar con una compuerta, dibujado."""
    if entradas == 1:
        casos = [(a,) for a in (False, True)]
        encabezados = ["a"]
    else:
        casos = [(a, b) for a in (False, True) for b in (False, True)]
        encabezados = ["a", "b"]

    salida_x = len(encabezados) * 0.85 + 0.75
    figura, ax = plt.subplots(figsize=(salida_x + 1.3, 0.85 * len(casos) + 1.2))

    for j, h in enumerate(encabezados):
        ax.text(j * 0.85, 0.85, h, ha="center", fontsize=12, color="0.35")
    ax.text(salida_x, 0.85, nombre, ha="center", fontsize=12, weight="bold")

    for fila, caso in enumerate(casos):
        y = -fila
        for j, v in enumerate(caso):
            ax.add_patch(plt.Circle((j * 0.85, y), 0.28, zorder=2, linewidth=1.4,
                                    facecolor=ENCENDIDO if v else APAGADO, edgecolor=BORDE))
        ax.text(salida_x - 0.75, y, "→", ha="center", va="center",
                fontsize=15, color=TENUE)
        s = compuerta(*caso)
        ax.add_patch(plt.Circle((salida_x, y), 0.28, zorder=2, linewidth=1.4,
                                facecolor=ENCENDIDO if s else APAGADO, edgecolor=BORDE))

    ax.set_xlim(-0.55, salida_x + 0.55)
    ax.set_ylim(-len(casos) + 0.1, 1.25)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    plt.show()
    return figura


def dibujar_palabra(texto):
    """Cada letra de un texto, en ocho interruptores."""
    for letra in texto:
        numero = ord(letra)
        try:
            bits = a_binario(numero)
        except NoCabe as no_cabe:
            print(f"   {letra}  →  {numero}   {no_cabe}")
            continue
        dibujar(bits, etiquetas=TABLA_DE_VALORES, mostrar_bool=False,
                titulo=f"{letra}   →   {numero}")
```

- [ ] **Step 4: Corre la prueba y confirma que pasa**

Run: `python3 -m pytest tests/test_interruptores.py -v`
Expected: 6 passed

- [ ] **Step 5: Comitea**

```bash
git add shift_enter/interruptores.py tests/test_interruptores.py
git commit -m "feat: interruptores dibujados y tabla de verdad"
```

---

### Task 4: Los interruptores que se prenden con el dedo

**Files:**
- Modify: `shift_enter/interruptores.py`
- Test: `tests/test_tablero.py`

**Interfaces:**
- Consumes: lo de la Tarea 3, más `shift_enter.binario.a_decimal`.
- Produces: `como_html(bits, etiquetas=None) -> str`; `tablero(valor_inicial=0) -> tuple[list, ipywidgets.HTML]` que devuelve los ocho botones y el marcador; `contador(desde=0, hasta=255, ms=200) -> tuple[Play, IntSlider, HTML]`.

`como_html` existe porque redibujar matplotlib doscientas cincuenta y seis veces seguidas se arrastra en Colab. Los juguetes vivos son HTML, que se actualiza al instante. Las figuras que tienen que leerse en GitHub siguen siendo matplotlib.

- [ ] **Step 1: Escribe la prueba que falla**

```python
# tests/test_tablero.py
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
    botones, marcador = interruptores.tablero(valor_inicial=5)
    assert len(botones) == 8
    assert [b.value for b in botones] == [False, False, False, False, False, True, False, True]
    assert "5" in marcador.value


def test_el_tablero_reacciona_cuando_prendes_uno():
    botones, marcador = interruptores.tablero(valor_inicial=0)
    botones[0].value = True          # la columna de 128
    assert "128" in marcador.value


def test_el_contador_va_de_cero_a_doscientos_cincuenta_y_cinco():
    reproductor, deslizador, salida = interruptores.contador()
    assert reproductor.min == 0 and reproductor.max == 255
    deslizador.value = 255
    assert "255" in salida.value


def test_los_juguetes_dejan_un_cuadro_fijo_antes_del_widget(monkeypatch):
    dibujados = []
    monkeypatch.setattr(interruptores, "dibujar",
                        lambda *a, **k: dibujados.append(a))
    interruptores.tablero(valor_inicial=5)
    interruptores.contador()
    assert len(dibujados) == 2
```

- [ ] **Step 2: Corre la prueba y confirma que falla**

Run: `python3 -m pytest tests/test_tablero.py -v`
Expected: FAIL con `AttributeError: module 'shift_enter.interruptores' has no attribute 'como_html'`

- [ ] **Step 3: Agrega la implementación al final de `shift_enter/interruptores.py`**

```python
import ipywidgets as widgets
from IPython.display import display

from .binario import a_decimal

ENCENDIDO_HTML = ENCENDIDO
APAGADO_HTML = APAGADO


def como_html(bits, etiquetas=None):
    """Los interruptores como circulos de HTML. Se actualiza al instante."""
    piezas = []
    for i, bit in enumerate(bits):
        color = ENCENDIDO_HTML if bit else APAGADO_HTML
        etiqueta = "" if etiquetas is None else str(etiquetas[i])
        piezas.append(
            f"<div style='display:inline-block;text-align:center;margin:0 6px'>"
            f"<div style='font-size:11px;color:#777'>{etiqueta}</div>"
            f"<div style='width:38px;height:38px;border-radius:50%;"
            f"background:{color};border:2px solid {BORDE}'></div>"
            f"<div style='font-family:monospace;font-weight:bold'>{int(bool(bit))}</div>"
            f"</div>"
        )
    return "<div>" + "".join(piezas) + "</div>"


def _marcador(bits):
    numero = a_decimal(bits)
    partes = " + ".join(str(v) for b, v in zip(bits, TABLA_DE_VALORES) if b)
    return (f"{como_html(bits, TABLA_DE_VALORES)}"
            f"<div style='font-size:40px;font-weight:bold;margin-top:8px'>{numero}</div>"
            f"<div style='color:#777'>{partes or 'ningun interruptor prendido'}</div>")


def tablero(valor_inicial=0):
    """Ocho interruptores que prendes con el dedo."""
    botones = [widgets.ToggleButton(value=v, description=str(valor),
                                    layout=widgets.Layout(width="60px"))
               for v, valor in zip(a_binario(valor_inicial), TABLA_DE_VALORES)]
    marcador = widgets.HTML()

    def actualizar(_=None):
        marcador.value = _marcador([b.value for b in botones])

    for boton in botones:
        boton.observe(actualizar, names="value")
    actualizar()
    # Un cuadro fijo antes del widget: el estado de los widgets no se guarda,
    # asi que sin esto la celda se ve vacia para quien lee en GitHub.
    dibujar(a_binario(valor_inicial), etiquetas=TABLA_DE_VALORES, mostrar_bool=False,
            titulo=f"empieza en {valor_inicial}")
    display(widgets.VBox([widgets.HBox(botones), marcador]))
    return botones, marcador


def contador(desde=0, hasta=255, ms=200):
    """El boton de play contando en binario."""
    reproductor = widgets.Play(value=desde, min=desde, max=hasta, interval=ms)
    deslizador = widgets.IntSlider(value=desde, min=desde, max=hasta, description="numero")
    widgets.link((reproductor, "value"), (deslizador, "value"))
    salida = widgets.HTML()

    def pintar(cambio):
        n = cambio["new"]
        salida.value = (f"{como_html(a_binario(n), TABLA_DE_VALORES)}"
                        f"<div style='font-size:40px;font-weight:bold'>{n}</div>")

    deslizador.observe(pintar, names="value")
    pintar({"new": desde})
    dibujar(a_binario(desde), etiquetas=TABLA_DE_VALORES, mostrar_bool=False,
            titulo=f"empieza en {desde}")
    display(widgets.VBox([widgets.HBox([reproductor, deslizador]), salida]))
    return reproductor, deslizador, salida
```

- [ ] **Step 4: Corre la prueba y confirma que pasa**

Run: `python3 -m pytest tests/test_tablero.py -v`
Expected: 6 passed

- [ ] **Step 5: Comitea**

```bash
git add shift_enter/interruptores.py tests/test_tablero.py
git commit -m "feat: tablero de interruptores y contador con boton de play"
```

---

### Task 5: El disco cifrador

**Files:**
- Create: `shift_enter/cifra.py`
- Test: `tests/test_cifra.py`

**Interfaces:**
- Consumes: `shift_enter.paleta.ENCENDIDO`, `TENUE`.
- Produces: `ALFABETO: str`; `MENSAJE_RETO: str` igual a `"QF%UNJIWF%^F%HZJSYF"`; `DESPLAZAMIENTO_RETO: int` igual a `5`; `disco(mensaje, desplazamiento, ax=None) -> matplotlib.axes.Axes`; `deslizador_disco(mensaje) -> None`.

El alumno escribe `correr` a mano en la notebook con `ord` y `chr`, sin dar vuelta al alfabeto. Por eso el espacio se convierte en `%` y eso es parte de la lección: el espacio también es un número. `disco` dibuja el alfabeto corrido solo como metáfora visual; el mensaje que se descifra abajo usa la misma aritmética que escribió el alumno.

- [ ] **Step 1: Escribe la prueba que falla**

```python
# tests/test_cifra.py
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
```

- [ ] **Step 2: Corre la prueba y confirma que falla**

Run: `python3 -m pytest tests/test_cifra.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'shift_enter.cifra'`

- [ ] **Step 3: Escribe la implementación**

```python
# shift_enter/cifra.py
"""El disco cifrador de Julio Cesar."""

import ipywidgets as widgets
import matplotlib.pyplot as plt
from ipywidgets import interact

from .paleta import ENCENDIDO, TENUE

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DESPLAZAMIENTO_RETO = 5
MENSAJE_RETO = "QF%UNJIWF%^F%HZJSYF"


def _corrido(texto, cuanto):
    return "".join(chr(ord(letra) + cuanto) for letra in texto)


def disco(mensaje, desplazamiento, ax=None):
    """Las dos tiras del alfabeto y el mensaje descifrandose."""
    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(13, 3.4))

    abajo = ALFABETO[desplazamiento % 26:] + ALFABETO[:desplazamiento % 26]
    for i, (arriba_letra, abajo_letra) in enumerate(zip(ALFABETO, abajo)):
        ax.text(i, 1.0, arriba_letra, ha="center", va="center",
                fontsize=13, family="monospace", color=TENUE)
        ax.text(i, 0.45, abajo_letra, ha="center", va="center",
                fontsize=13, family="monospace", weight="bold")
    ax.text(-1.6, 1.0, "cifrado", ha="right", va="center", fontsize=10, color=TENUE)
    ax.text(-1.6, 0.45, "de verdad", ha="right", va="center", fontsize=10, color=TENUE)

    ax.text(12.5, -0.55, _corrido(mensaje, -desplazamiento), ha="center", va="center",
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
    """Arrastra el desplazamiento y mira el mensaje volverse espanol."""

    @interact(desplazamiento=widgets.IntSlider(min=0, max=25, value=0,
                                               description="corrimiento"))
    def _(desplazamiento):
        disco(mensaje, desplazamiento)
```

- [ ] **Step 4: Corre la prueba y confirma que pasa**

Run: `python3 -m pytest tests/test_cifra.py -v`
Expected: 4 passed

- [ ] **Step 5: Comitea**

```bash
git add shift_enter/cifra.py tests/test_cifra.py
git commit -m "feat: disco cifrador con deslizador y mensaje del reto"
```

---

### Task 6: El módulo `sonido`

**Files:**
- Create: `shift_enter/sonido.py`
- Test: `tests/test_sonido.py`

**Interfaces:**
- Consumes: nada del paquete.
- Produces: `MUESTREO: int` igual a `22050`; `onda(hz, segundos=2.0) -> np.ndarray`; `reproducir(arreglo) -> None`; `dibujar_onda(ondas, etiquetas=None, muestras=300) -> matplotlib.axes.Axes`; `melodia_del_nombre(texto, segundos_por_letra=0.35) -> np.ndarray`; `a_velocidad(arreglo, factor) -> np.ndarray`; `al_reves(arreglo) -> np.ndarray`; `deslizador_de_tono() -> None`.

- [ ] **Step 1: Escribe la prueba que falla**

```python
# tests/test_sonido.py
import matplotlib
matplotlib.use("Agg")
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
```

- [ ] **Step 2: Corre la prueba y confirma que falla**

Run: `python3 -m pytest tests/test_sonido.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'shift_enter.sonido'`

- [ ] **Step 3: Escribe la implementación**

```python
# shift_enter/sonido.py
"""Sonido: una lista de numeros que se puede escuchar."""

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Audio, display
from ipywidgets import interact

MUESTREO = 22050


def onda(hz, segundos=2.0):
    """Una onda pura de la frecuencia que pidas."""
    t = np.linspace(0, segundos, int(MUESTREO * segundos), endpoint=False)
    return np.sin(2 * np.pi * hz * t)


def reproducir(arreglo):
    """Pone el reproductor de audio debajo de la celda."""
    display(Audio(arreglo, rate=MUESTREO))


def a_velocidad(arreglo, factor):
    """Mas rapido o mas lento: se toman menos o mas muestras."""
    indices = np.arange(0, len(arreglo), factor)
    return np.interp(indices, np.arange(len(arreglo)), arreglo)


def al_reves(arreglo):
    """La misma lista de numeros, leida del final al principio."""
    return np.asarray(arreglo)[::-1]


def melodia_del_nombre(texto, segundos_por_letra=0.35):
    """Cada letra es un numero, cada numero es una nota."""
    if not texto:
        return np.zeros(1)
    notas = [onda(110 * 2 ** ((ord(letra) % 24) / 12), segundos_por_letra)
             for letra in texto]
    return np.concatenate(notas)


def dibujar_onda(ondas, etiquetas=None, muestras=300, ax=None):
    """Un sonido, visto de muy cerca."""
    if not isinstance(ondas, (list, tuple)):
        ondas = [ondas]
    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(11, 2.5))
    for i, arreglo in enumerate(ondas):
        etiqueta = None if etiquetas is None else etiquetas[i]
        ax.plot(np.arange(min(muestras, len(arreglo))) / MUESTREO,
                arreglo[:muestras], linewidth=1.5, label=etiqueta)
    if etiquetas is not None:
        ax.legend(loc="upper right", fontsize=9)
    ax.set_xlabel("segundos")
    if propia:
        plt.tight_layout()
        plt.show()
    return ax


def deslizador_de_tono():
    """Arrastra los hertz y escucha el cambio."""

    @interact(hz=widgets.IntSlider(min=110, max=1760, step=10, value=440,
                                   description="Hz"))
    def _(hz):
        print(f"   Cambiaste un solo numero: {hz}")
        reproducir(onda(hz))
```

- [ ] **Step 4: Corre la prueba y confirma que pasa**

Run: `python3 -m pytest tests/test_sonido.py -v`
Expected: 7 passed

- [ ] **Step 5: Comitea**

```bash
git add shift_enter/sonido.py tests/test_sonido.py
git commit -m "feat: modulo sonido con melodia del nombre, velocidad y reversa"
```

---

### Task 7: La imagen de respaldo y las funciones sin widget

**Files:**
- Create: `shift_enter/datos/leibniz.jpg`
- Create: `shift_enter/imagen.py`
- Test: `tests/test_imagen.py`

**Interfaces:**
- Consumes: nada del paquete.
- Produces: `de_respaldo() -> np.ndarray` en gris, `dtype=uint8`; `desde_texto(dibujo: str) -> np.ndarray`; `mostrar(arreglo, titulo=None, ax=None) -> matplotlib.axes.Axes`; `mas_brillo(arreglo, cuanto) -> np.ndarray`.

La foto viaja dentro del paquete. Hoy se baja de Wikimedia en una celda visible y si Wikimedia falla se cae media notebook.

- [ ] **Step 1: Baja la foto una sola vez y guárdala en el paquete**

```bash
mkdir -p shift_enter/datos
python3 -c "
from io import BytesIO
import requests
from PIL import Image
url = ('https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/'
       'Christoph_Bernhard_Francke_-_Bildnis_des_Philosophen_Leibniz_%28ca._1695%29.jpg/'
       '500px-Christoph_Bernhard_Francke_-_Bildnis_des_Philosophen_Leibniz_%28ca._1695%29.jpg')
r = requests.get(url, headers={'User-Agent': 'shift-enter (notebook educativa)'})
r.raise_for_status()
Image.open(BytesIO(r.content)).convert('L').save('shift_enter/datos/leibniz.jpg', quality=85)
print('guardada')
"
ls -la shift_enter/datos/leibniz.jpg
```

Expected: el archivo existe y pesa menos de 100 KB.

- [ ] **Step 2: Escribe la prueba que falla**

```python
# tests/test_imagen.py
import matplotlib
matplotlib.use("Agg")
import numpy as np

from shift_enter import imagen


def test_la_foto_de_respaldo_viene_en_el_paquete():
    foto = imagen.de_respaldo()
    assert foto.ndim == 2
    assert foto.dtype == np.uint8
    assert foto.shape[0] > 100 and foto.shape[1] > 100


def test_desde_texto_convierte_gatos_en_negro():
    dibujo = """
    .#.
    ###
    """
    tabla = imagen.desde_texto(dibujo)
    assert tabla.shape == (2, 3)
    assert tabla[0, 0] == 255
    assert tabla[0, 1] == 0
    assert list(tabla[1]) == [0, 0, 0]


def test_desde_texto_rellena_las_filas_cortas():
    tabla = imagen.desde_texto("##\n#")
    assert tabla.shape == (2, 2)
    assert tabla[1, 1] == 255


def test_mas_brillo_no_se_pasa_de_255():
    tabla = np.array([[200, 10]], dtype=np.uint8)
    assert list(imagen.mas_brillo(tabla, 100)[0]) == [255, 110]


def test_mas_brillo_no_baja_de_cero():
    tabla = np.array([[200, 10]], dtype=np.uint8)
    assert list(imagen.mas_brillo(tabla, -100)[0]) == [100, 0]


def test_mostrar_pinta_la_imagen():
    eje = imagen.mostrar(imagen.desde_texto("#."), titulo="prueba")
    assert len(eje.images) == 1
```

- [ ] **Step 3: Corre la prueba y confirma que falla**

Run: `python3 -m pytest tests/test_imagen.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'shift_enter.imagen'`

- [ ] **Step 4: Escribe la implementación**

```python
# shift_enter/imagen.py
"""Una imagen es una tabla de numeros."""

from importlib import resources

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def de_respaldo():
    """La foto de Leibniz, empacada dentro del paquete."""
    with resources.files("shift_enter.datos").joinpath("leibniz.jpg").open("rb") as archivo:
        return np.array(Image.open(archivo).convert("L"), dtype=np.uint8)


def desde_texto(dibujo):
    """Convierte un texto de puntos y gatos en una tabla de numeros."""
    filas = [linea.strip() for linea in dibujo.strip().splitlines()]
    ancho = max(len(fila) for fila in filas)
    return np.array([[0 if letra == "#" else 255 for letra in fila.ljust(ancho, ".")]
                     for fila in filas], dtype=np.uint8)


def mas_brillo(arreglo, cuanto):
    """Sumarle un numero a cada pixel, sin salirse de 0 y 255."""
    return np.clip(arreglo.astype(int) + cuanto, 0, 255).astype(np.uint8)


def mostrar(arreglo, titulo=None, ax=None):
    """La imagen, sin ejes ni adornos."""
    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(5, 6))
    ax.imshow(arreglo, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    ax.axis("off")
    if titulo:
        ax.set_title(titulo)
    if propia:
        plt.tight_layout()
        plt.show()
    return ax
```

- [ ] **Step 5: Corre la prueba y confirma que pasa**

Run: `python3 -m pytest tests/test_imagen.py -v`
Expected: 6 passed

- [ ] **Step 6: Comitea**

```bash
git add shift_enter/datos/leibniz.jpg shift_enter/imagen.py tests/test_imagen.py
git commit -m "feat: foto de respaldo empacada y funciones de imagen"
```

---

### Task 8: La foto que se recorre con el mouse, y los deslizadores

**Files:**
- Modify: `shift_enter/imagen.py`
- Test: `tests/test_imagen_widgets.py`

**Interfaces:**
- Consumes: lo de la Tarea 7.
- Produces: `mostrar_con_numeros(arreglo, titulo=None) -> plotly.graph_objects.Figure`; `selector() -> ipywidgets.FileUpload`; `actual() -> np.ndarray`; `olvidar() -> None`; `deslizador_brillo(arreglo) -> None`; `mezclador_color() -> None`.

Esta es la única celda de toda la notebook que usa plotly. Ahí la interacción es la lección: el alumno pasa el mouse y lee el número de cada pixel, y se acerca con dos dedos.

`selector` usa el widget de subir archivo y no `files.upload()` de Colab, porque ese último se queda esperando para siempre cuando la notebook corre sola con `nbclient`. Mientras el alumno no suba nada, `actual()` devuelve la foto de respaldo y la sección funciona completa.

- [ ] **Step 1: Escribe la prueba que falla**

```python
# tests/test_imagen_widgets.py
import matplotlib
matplotlib.use("Agg")
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
    figura = imagen.mostrar_con_numeros(imagen.desde_texto("#."))
    assert figura.data[0].type == "heatmap"


def test_mostrar_con_numeros_ensena_el_valor_al_pasar_el_mouse():
    figura = imagen.mostrar_con_numeros(imagen.desde_texto("#."))
    assert "%{z}" in figura.data[0].hovertemplate


def test_el_selector_acepta_imagenes():
    subir = imagen.selector()
    assert subir.accept == "image/*"
    assert subir.multiple is False
```

- [ ] **Step 2: Corre la prueba y confirma que falla**

Run: `python3 -m pytest tests/test_imagen_widgets.py -v`
Expected: FAIL con `AttributeError: module 'shift_enter.imagen' has no attribute 'olvidar'`

- [ ] **Step 3: Agrega la implementación al final de `shift_enter/imagen.py`**

```python
from io import BytesIO

import ipywidgets as widgets
import plotly.express as px
from IPython.display import display
from ipywidgets import interact

_SUBIDA = {"arreglo": None}


def _recordar(arreglo):
    _SUBIDA["arreglo"] = arreglo


def olvidar():
    """Vuelve a la foto de respaldo."""
    _SUBIDA["arreglo"] = None


def actual():
    """La foto del alumno si ya subio una, o la de respaldo."""
    return _SUBIDA["arreglo"] if _SUBIDA["arreglo"] is not None else de_respaldo()


def selector():
    """El boton para subir tu propia foto. No bloquea si nadie sube nada."""
    subir = widgets.FileUpload(accept="image/*", multiple=False,
                               description="sube tu foto")
    aviso = widgets.HTML("Mientras no subas nada, trabajas con la foto de respaldo.")

    def recibir(cambio):
        archivos = cambio["new"]
        if not archivos:
            return
        crudo = (archivos[0]["content"] if isinstance(archivos, (list, tuple))
                 else list(archivos.values())[0]["content"])
        _recordar(np.array(Image.open(BytesIO(bytes(crudo))).convert("L"), dtype=np.uint8))
        aviso.value = "Listo. Vuelve a correr las celdas de abajo y va a salir tu cara."

    subir.observe(recibir, names="value")
    display(widgets.VBox([subir, aviso]))
    return subir


def mostrar_con_numeros(arreglo, titulo=None):
    """La foto por dentro. Pasa el mouse y lee el numero de cada pixel."""
    figura = px.imshow(arreglo, color_continuous_scale="gray", zmin=0, zmax=255,
                       title=titulo)
    figura.update_traces(
        hovertemplate="fila %{y}, columna %{x}<br><b>%{z}</b><extra></extra>")
    figura.update_layout(coloraxis_showscale=False, dragmode="zoom",
                         margin=dict(l=10, r=10, t=45, b=10))
    figura.show()
    return figura


def deslizador_brillo(arreglo):
    """Sumale un numero a cada pixel y mira que pasa."""

    @interact(brillo=widgets.IntSlider(min=-150, max=150, value=0, description="+"))
    def _(brillo):
        mostrar(mas_brillo(arreglo, brillo), titulo=f"foto + ({brillo})")


def mezclador_color():
    """Cualquier color del mundo, con tres numeros."""

    @interact(rojo=widgets.IntSlider(min=0, max=255, value=200, description="rojo"),
              verde=widgets.IntSlider(min=0, max=255, value=90, description="verde"),
              azul=widgets.IntSlider(min=0, max=255, value=30, description="azul"))
    def _(rojo, verde, azul):
        _, eje = plt.subplots(figsize=(4, 2.4))
        eje.add_patch(plt.Rectangle((0, 0), 1, 1,
                                    facecolor=(rojo / 255, verde / 255, azul / 255)))
        eje.set_xlim(0, 1)
        eje.set_ylim(0, 1)
        eje.axis("off")
        eje.set_title(f"[{rojo}, {verde}, {azul}]", family="monospace")
        plt.tight_layout()
        plt.show()
```

- [ ] **Step 4: Corre la prueba y confirma que pasa**

Run: `python3 -m pytest tests/test_imagen_widgets.py -v`
Expected: 5 passed

- [ ] **Step 5: Corre todas las pruebas del paquete**

Run: `python3 -m pytest tests/ -v`
Expected: 43 passed

- [ ] **Step 6: Comitea**

```bash
git add shift_enter/imagen.py tests/test_imagen_widgets.py
git commit -m "feat: foto propia, foto por dentro con plotly y mezclador de color"
```

---

### Task 9: El andamio de la notebook, el guardián y la portada

**Files:**
- Create: `herramientas/construir_notebook.py`
- Create: `tests/test_notebook.py`
- Modify: `la-piedra-que-aprendio-a-contar.ipynb`

**Interfaces:**
- Consumes: todo el paquete.
- Produces: `herramientas/construir_notebook.py` con `md(texto)`, `codigo(fuente)`, `forma(fuente)` y `construir(ruta)`. Cada tarea de sección de aquí en adelante agrega una función `seccion_N()` y su llamada, en orden, antes de `construir()`.

El constructor es un andamio, no un producto. La notebook sigue siendo el entregable. La Tarea 16 borra `herramientas/`.

- [ ] **Step 1: Respalda la notebook actual**

```bash
cp la-piedra-que-aprendio-a-contar.ipynb /tmp/piedra-respaldo.ipynb
```

- [ ] **Step 2: Escribe el guardián, que va a fallar**

```python
# tests/test_notebook.py
import json
from pathlib import Path

import pytest

NOTEBOOK = Path(__file__).resolve().parents[1] / "la-piedra-que-aprendio-a-contar.ipynb"
GRAFICACION = ("plt.", "px.", "matplotlib", "plotly", "sns.", "fig,")
CONCEPTO = ("def correr(", "def NO(", "def Y(", "def O(", "def XOR(",
            "def medio_sumador(", "def sumador_completo(", "def sumar(")


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


def test_el_alumno_escribe_el_concepto_a_mano(celdas):
    fuente = "\n".join("".join(celda["source"]) for _, celda in visibles(celdas))
    assert [firma for firma in CONCEPTO if firma not in fuente] == []
```

- [ ] **Step 3: Corre el guardián y confirma que falla**

Run: `python3 -m pytest tests/test_notebook.py -v`
Expected: FAIL. `test_ninguna_celda_visible_dibuja` reporta las diez celdas visibles con matplotlib de la notebook vieja.

- [ ] **Step 4: Escribe el constructor con la portada y la celda de forma**

```python
# herramientas/construir_notebook.py
"""Construye la-piedra-que-aprendio-a-contar.ipynb desde cero.

Andamio, no producto. La notebook es el entregable. Este archivo se
borra cuando el rediseno queda terminado.
"""

import nbformat as nbf

CELDAS = []


def md(texto):
    CELDAS.append(nbf.v4.new_markdown_cell(texto.strip("\n")))


def codigo(fuente):
    CELDAS.append(nbf.v4.new_code_cell(fuente.strip("\n")))


def forma(fuente):
    celda = nbf.v4.new_code_cell(fuente.strip("\n"))
    celda.metadata["cellView"] = "form"
    CELDAS.append(celda)


def portada():
    md("# 🪨 La piedra que aprendió a contar")
    md("Una computadora es arena.")
    md("Arena a la que le enseñamos a contar.")
    md("""
## 🎯 La promesa

**Hoy vas a abrir tu nombre, tu foto y tu música por dentro, y vas a descubrir
que las tres son la misma cosa: números.**

Y al final vas a construir con tus manos la pieza de la computadora que suma
esos números, sin escribir ni una sola vez el signo `+`.
""")
    md("""
### Cómo se usa

Presiona **`Shift + Enter`** en cada celda, **de arriba abajo y en orden**. Cada
sección usa lo que construiste en la anterior.

Cambia los números. Rompe las cosas. Vuelve a correr. No puedes descomponer nada.
""")
    forma('''
#@title 🔧 Prepara el taller  { display-mode: "form" }
# Corre esta celda y olvidala. Es el escenario, no la obra.
import importlib.util
import subprocess
import sys

if importlib.util.find_spec("shift_enter") is None:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                    "git+https://github.com/nrqrmz/shift-enter"], check=True)

from shift_enter import cifra, imagen, interruptores, paleta, sonido
from shift_enter.binario import TABLA_DE_VALORES, a_binario, a_decimal
from shift_enter.interruptores import simbolo

paleta.aplicar_estilo()
print("Listo. La piedra esta encendida.")
''')
    md("**Corre esa celda antes que nada.** Trae las herramientas. Es el escenario, no la obra.")


def construir(ruta="la-piedra-que-aprendio-a-contar.ipynb"):
    cuaderno = nbf.v4.new_notebook(cells=CELDAS)
    cuaderno.metadata.update({
        "colab": {"provenance": [], "toc_visible": True},
        "kernelspec": {"display_name": "Python 3 (ipykernel)",
                       "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12.9",
                          "file_extension": ".py", "mimetype": "text/x-python",
                          "nbconvert_exporter": "python",
                          "pygments_lexer": "ipython3",
                          "codemirror_mode": {"name": "ipython", "version": 3}},
    })
    nbf.write(cuaderno, ruta)
    print(f"escritas {len(CELDAS)} celdas en {ruta}")


if __name__ == "__main__":
    portada()
    construir()
```

- [ ] **Step 5: Reconstruye la notebook**

Run: `python3 herramientas/construir_notebook.py`
Expected: `escritas 7 celdas en la-piedra-que-aprendio-a-contar.ipynb`

- [ ] **Step 6: Ejecútala y guarda las salidas**

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

Expected: termina sin levantar excepción.

- [ ] **Step 7: Corre el guardián y confirma que pasa**

Run: `python3 -m pytest tests/test_notebook.py -v`
Expected: 5 passed. `test_el_alumno_escribe_el_concepto_a_mano` pasa por vacuidad mientras no haya celdas visibles, y se vuelve exigente en la Tarea 14.

- [ ] **Step 8: Comitea**

```bash
git add herramientas/construir_notebook.py tests/test_notebook.py la-piedra-que-aprendio-a-contar.ipynb
git commit -m "feat: andamio de construccion, guardian de la notebook y portada nueva"
```

---

### Task 10: §1 · Tu nombre

**Files:**
- Modify: `herramientas/construir_notebook.py`
- Modify: `la-piedra-que-aprendio-a-contar.ipynb`

**Interfaces:**
- Consumes: `sonido.melodia_del_nombre`, `sonido.reproducir`, `cifra.deslizador_disco`, `cifra.MENSAJE_RETO`.
- Produces: la variable `mi_nombre` y la función `correr`, que las secciones 3 y 5 dan por definidas.

- [ ] **Step 1: Agrega la sección al constructor, antes de `construir`**

```python
def seccion_nombre():
    md("""
---

# 1 · Tu nombre ya está adentro

Escribe tu nombre. Está guardado en esta computadora ahorita mismo.

No como letras. Aquí adentro no hay letras. Solo hay números.
""")
    codigo('''
mi_nombre = "Ada"    # ← pon el tuyo

for letra in mi_nombre:
    print(letra, "→", ord(letra))
''')
    md("""
Ese número no es un apodo ni una traducción. **Es** la letra. Es lo único que
hay de tu nombre dentro de la máquina.

Y si tu nombre es una lista de números, entonces se puede escuchar.
""")
    codigo('''
sonido.reproducir(sonido.melodia_del_nombre(mi_nombre))
''')
    md("""
### 🔧 Prueba tú

Si una letra es un número, súmale 3 y mira qué sale.
""")
    codigo('''
def correr(texto, cuanto):
    salida = ""
    for letra in texto:
        salida = salida + chr(ord(letra) + cuanto)
    return salida


secreto = correr(mi_nombre, 3)
print("   cifrado:   ", secreto)
print("   descifrado:", correr(secreto, -3))
''')
    md("""
Julio César mandaba sus órdenes militares así, hace dos mil años. Le sumaba un
número a cada letra y sus enemigos veían basura.

Tú lo acabas de hacer con una suma.
""")
    md("""
### 🎯 El reto

Aquí hay un mensaje cifrado. Nadie te va a decir con qué número.

Arrastra el corrimiento hasta que el mensaje se vuelva español.
""")
    codigo('''
cifra.deslizador_disco(cifra.MENSAJE_RETO)
''')
    md("""
### 🤔 Para pensar

El espacio también se convirtió en otro símbolo cuando corriste las letras.

¿Por qué? ¿Qué número crees que es un espacio?
""")
```

Y cambia el bloque final a:

```python
if __name__ == "__main__":
    portada()
    seccion_nombre()
    construir()
```

- [ ] **Step 2: Reconstruye**

Run: `python3 herramientas/construir_notebook.py`
Expected: `escritas 17 celdas`

- [ ] **Step 3: Ejecuta la notebook**

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

Expected: termina sin excepción.

- [ ] **Step 4: Corre el guardián**

Run: `python3 -m pytest tests/test_notebook.py -v`
Expected: 5 passed

- [ ] **Step 5: Comitea**

```bash
git add herramientas/construir_notebook.py la-piedra-que-aprendio-a-contar.ipynb
git commit -m "feat: seccion 1, tu nombre por dentro y el reto del disco cifrador"
```

---

### Task 11: §2 · Tu foto

**Files:**
- Modify: `herramientas/construir_notebook.py`
- Modify: `la-piedra-que-aprendio-a-contar.ipynb`

**Interfaces:**
- Consumes: `imagen.desde_texto`, `imagen.mostrar`, `imagen.selector`, `imagen.actual`, `imagen.mostrar_con_numeros`, `imagen.deslizador_brillo`, `imagen.mezclador_color`.
- Produces: la variable `mi_dibujo`.

- [ ] **Step 1: Agrega la sección al constructor**

```python
def seccion_foto():
    md("""
---

# 2 · Tu foto es una tabla de números

Tu nombre era una lista. Una imagen es una tabla: un número por cada punto de
la pantalla.

Empieza al revés. En vez de abrir una foto, dibuja una escribiendo. Cada `#` es
un punto negro y cada `.` uno blanco.
""")
    codigo('''
mi_dibujo = """
..####..
.#....#.
#.#..#.#
#......#
#.#..#.#
#..##..#
.#....#.
..####..
"""

imagen.mostrar(imagen.desde_texto(mi_dibujo), titulo="lo que escribiste")
''')
    md("""
Cámbiale los puntos y los gatos. Dibuja lo tuyo y vuelve a correr la celda.

Los números no representan el dibujo. Los números **son** el dibujo.
""")
    md("""
### 🔧 Ahora la tuya

Sube una foto tuya. Si no quieres, no subas nada: el taller trae una de
repuesto y todo lo de abajo funciona igual.
""")
    codigo('''
imagen.selector()
''')
    md("""
Aquí está por dentro. **Pasa el mouse por encima** y vas a ver el número de cada
pixel. Acércate con dos dedos hasta que los puntos se vuelvan cuadrados.
""")
    codigo('''
imagen.mostrar_con_numeros(imagen.actual(), titulo="pasa el mouse por encima")
''')
    md("""
Si una foto es una tabla de números, entonces **editar una foto es hacer
aritmética**. Nada más.

Arrastra y mírala aclararse. Le estás sumando el mismo número a cada pixel.
""")
    codigo('''
imagen.deslizador_brillo(imagen.actual())
''')
    md("""
### El color son tres números

Hasta aquí todo fue gris, que es un número por punto. El color son tres:
cuánto rojo, cuánto verde y cuánto azul.

Con esos tres cabe cualquier color que hayas visto en una pantalla. Búscate uno.
""")
    codigo('''
imagen.mezclador_color()
''')
```

Y agrega `seccion_foto()` a la llamada final, después de `seccion_nombre()`.

- [ ] **Step 2: Reconstruye**

Run: `python3 herramientas/construir_notebook.py`
Expected: `escritas 28 celdas`

- [ ] **Step 3: Ejecuta la notebook**

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

Expected: termina sin excepción. La celda del selector no bloquea porque nadie sube nada.

- [ ] **Step 4: Corre el guardián**

Run: `python3 -m pytest tests/test_notebook.py -v`
Expected: 5 passed

- [ ] **Step 5: Comitea**

```bash
git add herramientas/construir_notebook.py la-piedra-que-aprendio-a-contar.ipynb
git commit -m "feat: seccion 2, dibujar escribiendo y la foto propia por dentro"
```

---

### Task 12: §3 · Tu música

**Files:**
- Modify: `herramientas/construir_notebook.py`
- Modify: `la-piedra-que-aprendio-a-contar.ipynb`

**Interfaces:**
- Consumes: `sonido.onda`, `dibujar_onda`, `reproducir`, `deslizador_de_tono`, `a_velocidad`, `al_reves`, `melodia_del_nombre`, y `mi_nombre` de la §1.
- Produces: la variable `la`, que no usa ninguna sección posterior.

- [ ] **Step 1: Agrega la sección al constructor**

```python
def seccion_musica():
    md("""
---

# 3 · Tu música es una lista de números

Un sonido es aire que empuja y jala tu tímpano. Si mides cuánto empuja, muchísimas
veces por segundo, te queda una lista de números.

Aquí está una, vista de muy cerca. Y escuchada.
""")
    codigo('''
la = sonido.onda(440)

sonido.dibujar_onda(la)
sonido.reproducir(la)
''')
    md("""
### 🔧 Prueba tú

Un solo número decide qué nota es. Arrástralo.
""")
    codigo('''
sonido.deslizador_de_tono()
''')
    md("""
### Y ahora rómpelo

Si el sonido es una lista, se le puede hacer lo que sea a una lista. Toma menos
números y sale más rápido. Léela del final al principio y sale al revés.
""")
    codigo('''
sonido.reproducir(sonido.a_velocidad(la, 2))
sonido.reproducir(sonido.al_reves(sonido.melodia_del_nombre(mi_nombre)))
''')
    md("""
### Y ahora súmalos

Tres sonidos. Súmalos como sumarías tres números.
""")
    codigo('''
do  = sonido.onda(261.63)
mi  = sonido.onda(329.63)
sol = sonido.onda(392.00)

acorde = do + mi + sol

sonido.dibujar_onda([do, mi, sol, acorde],
                    etiquetas=["do", "mi", "sol", "los tres sumados"],
                    muestras=600)
sonido.reproducir(acorde)
''')
    md("""
### Lo que llevas

Eso es un acorde de do mayor. No lo compusiste: lo **sumaste**.

Tu nombre, tu cara y ese acorde entraron a la máquina y se convirtieron en lo
mismo: listas de números.

Y a los tres les hiciste exactamente la misma cosa para cambiarlos. Le sumaste 3
a cada letra. Le sumaste 70 a cada pixel. Sumaste tres ondas.

Por eso una sola máquina puede tocar música, editar fotos y guardar mensajes. No
tiene tres talentos. Tiene uno.
""")
```

Y agrega `seccion_musica()` a la llamada final.

- [ ] **Step 2: Reconstruye**

Run: `python3 herramientas/construir_notebook.py`
Expected: `escritas 37 celdas`

- [ ] **Step 3: Ejecuta la notebook**

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

Expected: termina sin excepción.

- [ ] **Step 4: Corre el guardián**

Run: `python3 -m pytest tests/test_notebook.py -v`
Expected: 5 passed

- [ ] **Step 5: Comitea**

```bash
git add herramientas/construir_notebook.py la-piedra-que-aprendio-a-contar.ipynb
git commit -m "feat: seccion 3, la musica como lista de numeros"
```

---

### Task 13: §4 · ¿Y cómo cabe eso en una piedra?

**Files:**
- Modify: `herramientas/construir_notebook.py`
- Modify: `la-piedra-que-aprendio-a-contar.ipynb`

**Interfaces:**
- Consumes: `interruptores.tablero`, `contador`, `dibujar_palabra`, `dibujar`; `a_binario`; `TABLA_DE_VALORES`; `mi_nombre` de la §1.
- Produces: las variables `prendido` y `apagado`, que la §5 usa en las tres compuertas.

Aquí recién aparece el interruptor, como respuesta a una pregunta que el alumno ya se está haciendo. Y aquí se recoge el nombre de la §1, ahora en interruptores.

**Desviación del spec.** El spec ponía el desbordamiento en esta sección, con el contador cayendo de 255 a 0. `widgets.Play` se detiene en su máximo y no da la vuelta, y la caída solo tiene sentido cuando existe algo que suma. Por eso el desbordamiento se mueve a la §5, justo después de `sumar(255, 1)`, donde el alumno ve los ocho interruptores apagarse. Aquí queda el límite, que es 255 y ni uno más.

- [ ] **Step 1: Agrega la sección al constructor**

```python
def seccion_piedra():
    md("""
---

# 4 · ¿Y cómo cabe todo eso en una piedra?

Toma un puñado de arena de playa. Es dióxido de silicio.

Derrítela. Purifícala hasta que de cada mil millones de átomos solo uno sea de
otra cosa. Te queda un cristal gris, aburrido, que no hace absolutamente nada.

Ahora graba en su superficie algo diminuto, miles de veces más delgado que un
cabello, que hace **una sola cosa**: deja pasar la electricidad, o no la deja.

Eso es un **transistor**. Un interruptor sin partes móviles.

En el aparato donde estás leyendo esto hay varios **miles de millones**. Ninguno
sabe sumar. Ninguno sabe leer. Solo están prendidos o apagados.
""")
    codigo('''
prendido = True    # este es un valor booleano
apagado  = False   # este es un valor booleano

print("Para la maquina no se llaman 'prendido' y 'apagado'. Se llaman 1 y 0.")
print("Y no es un apodo. Compruebalo:")
print()
print("   True  == 1   →", True == 1)
print("   False == 0   →", False == 0)
''')
    md("""
### Ocho interruptores

Un interruptor solo tiene dos estados, así que solo puede guardar 0 o 1. Con
ocho ya cabe cualquier número hasta 255.

El truco es que cada columna vale **el doble** que su vecina de la derecha. En
el sistema que ya usas cada columna vale diez veces más, y es diez solo porque
tenemos diez dedos. Por nada más.

**Préndelos con el dedo** y mira qué número sale.
""")
    codigo('''
interruptores.tablero(valor_inicial=42)
''')
    md("""
### Dale play

Ahora míralos contar solos, del 0 al 255. **Mira las columnas, no el número.**
""")
    codigo('''
interruptores.contador()
''')
    md("""
El interruptor de la derecha se prende y se apaga en cada número. El siguiente,
cada dos. El siguiente, cada cuatro.

Cada uno va exactamente al doble de lento que su vecino de la derecha. Eso es
todo lo que significa contar en binario.

En 1679 Gottfried Leibniz escribió esto en un papel, sin computadoras y sin
electricidad. Le pareció bello y ya. Fue un juguete inútil durante doscientos
setenta años, hasta que alguien conectó unos interruptores y descubrió que el
juguete era exactamente lo que la máquina necesitaba.
""")
    md("""
### Tu nombre, otra vez

En la §1 tu nombre era una lista de números. Así es como está guardado de verdad.
""")
    codigo('''
interruptores.dibujar_palabra(mi_nombre)
''')
    md("""
### Donde se acaban

Con ocho interruptores el número más grande que existe es este. No hay uno más.
""")
    codigo('''
interruptores.dibujar(a_binario(255), etiquetas=TABLA_DE_VALORES,
                      mostrar_bool=False, titulo="el mas grande que cabe")
''')
    md("""
### 🤔 Para pensar

¿Por qué justo 255, y no 256? ¿Y cuántos números distintos caben en ocho
interruptores, contando el cero?
""")
```

Y agrega `seccion_piedra()` a la llamada final.

- [ ] **Step 2: Reconstruye**

Run: `python3 herramientas/construir_notebook.py`
Expected: `escritas 49 celdas`

- [ ] **Step 3: Ejecuta la notebook**

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

Expected: termina sin excepción.

- [ ] **Step 4: Corre el guardián**

Run: `python3 -m pytest tests/test_notebook.py -v`
Expected: 5 passed

- [ ] **Step 5: Comitea**

```bash
git add herramientas/construir_notebook.py la-piedra-que-aprendio-a-contar.ipynb
git commit -m "feat: seccion 4, el interruptor con tablero y contador con play"
```

---

### Task 14: §5 · ¿Y quién suma allá abajo? Nadie

**Files:**
- Modify: `herramientas/construir_notebook.py`
- Modify: `la-piedra-que-aprendio-a-contar.ipynb`

**Interfaces:**
- Consumes: `prendido` y `apagado` de la §4; `interruptores.tabla_de_verdad`, `dibujar`; `simbolo`; `a_binario`, `a_decimal`, `TABLA_DE_VALORES`.
- Produces: `NO`, `Y`, `O`, `XOR`, `medio_sumador`, `sumador_completo` y `sumar`, todas escritas a mano en celdas visibles. `sumar` devuelve una lista de `True` y `False`, no un número.

Esta es la tarea que hace exigente a `test_el_alumno_escribe_el_concepto_a_mano`. Ninguna de esas siete funciones puede mudarse al paquete.

- [ ] **Step 1: Agrega la sección al constructor**

```python
def seccion_sumador():
    md("""
---

# 5 · ¿Y quién suma allá abajo? Nadie

Todo lo que hiciste hoy fue sumar. Le sumaste 3 a cada letra. Le sumaste 70 a
cada pixel. Sumaste tres ondas y salió un acorde.

Y allá abajo, adentro de la piedra, no hay nadie que sepa sumar. Solo hay
interruptores.

Vamos a construir al que suma.
""")
    md("""
### Tres reglas

Un interruptor solo no sirve. Lo interesante empieza cuando conectas dos y
decides qué pasa con el de salida.

Hay tres formas de conectarlos que resultaron suficientes para construir el
mundo entero. Se llaman **compuertas**. Son tres `if`, y las escribes tú.
""")
    codigo('''
def NO(a):
    if a == apagado:
        return prendido
    else:
        return apagado

def Y(a, b):
    if a == prendido and b == prendido:
        return prendido
    else:
        return apagado

def O(a, b):
    if a == apagado and b == apagado:
        return apagado
    else:
        return prendido


interruptores.tabla_de_verdad("NO", NO, entradas=1)
interruptores.tabla_de_verdad("Y", Y)
interruptores.tabla_de_verdad("O", O)
''')
    md("""
Esas tablas son la definición completa de una compuerta. Ahí está *todo* lo que
puede pasar. No hay caso escondido.

Con esas tres se puede construir cualquier otra cosa que haga una computadora.
Cualquiera. Empecemos por una cuarta que se prende cuando los dos interruptores
son **distintos**.
""")
    codigo('''
def XOR(a, b):
    """Prendido solo si a y b son DISTINTOS.
    No es una pieza nueva: es NO, Y y O acomodadas de cierta forma."""
    return O( Y(a, NO(b)),
              Y(NO(a), b) )


interruptores.tabla_de_verdad("XOR", XOR)
''')
    md("""
### Las cuatro sumas que existen

Sumar un interruptor más un interruptor. Eso es todo lo que hay:

```
0 + 0 = 0
0 + 1 = 1
1 + 0 = 1
1 + 1 = 10     ← se pasa: escribe 0 y lleva 1
```

Mira la columna de la suma y la columna del llevo.
""")
    codigo('''
print("     a    b          suma   llevo")
print("   " + "─" * 32)
for a in (apagado, prendido):
    for b in (apagado, prendido):
        print(f"     {simbolo(a)}   {simbolo(b)}     →      {simbolo(XOR(a, b))}     {simbolo(Y(a, b))}")
''')
    md("""
La columna de la suma es **XOR**. La columna del llevo es **Y**.

Las dos piezas ya estaban en tu caja. Nadie las inventó para esto.
""")
    codigo('''
def medio_sumador(a, b):
    suma    = XOR(a, b)
    acarreo = Y(a, b)
    return suma, acarreo


def sumador_completo(a, b, llevo_que_entra):
    suma_parcial, acarreo_1 = medio_sumador(a, b)
    suma_final,   acarreo_2 = medio_sumador(suma_parcial, llevo_que_entra)
    return suma_final, O(acarreo_1, acarreo_2)
''')
    md("""
### Encadenarlos

Cuando sumas 47 + 38 a mano empiezas por la derecha, y lo que llevas cae en la
siguiente columna. Aquí pasa igual: cada columna recibe tres cosas, el bit de
arriba, el de abajo, y lo que le llegó de la columna anterior.

Ocho sumadores completos en fila, cada uno pasándole su llevo al siguiente. Eso
es, literalmente, una pieza que existe dentro de tu procesador.
""")
    codigo('''
def sumar(a, b, ancho=8):
    bits_a = a_binario(a, ancho)
    bits_b = a_binario(b, ancho)
    resultado = []
    llevo = apagado

    for i in reversed(range(ancho)):
        suma, llevo = sumador_completo(bits_a[i], bits_b[i], llevo)
        resultado.insert(0, suma)

    return resultado


interruptores.dibujar(sumar(13, 29), etiquetas=TABLA_DE_VALORES,
                      mostrar_bool=False, titulo="13 + 29")
''')
    codigo('''
print("Esos interruptores, leidos como numero:", a_decimal(sumar(13, 29)))
print()
print("Ese 42 salio de:")
print("   • ocho sumadores completos encadenados,")
print("   • cada uno hecho de dos medios sumadores y una compuerta O,")
print("   • cada medio sumador hecho de un XOR y un Y,")
print("   • el XOR hecho de NO, Y y O,")
print("   • y NO, Y y O son tres if.")
print()
print("En ningun punto de esa cadena aparece el signo +.")
print("Acabas de construir la parte de la computadora que suma. 🎯")
''')
    md("""
### ✅ Que se califique solo

Un sumador que acierta una vez pudo tener suerte. Que lo pruebe con **todas** las
sumas posibles de 0 a 127, y que se compare contra el `+` de Python.
""")
    codigo('''
aciertos = 0
for a in range(128):
    for b in range(128):
        if a_decimal(sumar(a, b)) == a + b:
            aciertos = aciertos + 1

print(f"✅ {aciertos:,} de 16,384 sumas correctas")
''')
    md("""
### 🔧 Adivina antes de correr

Con ocho interruptores no cabe nada mayor que 255.

¿Qué crees que va a pasar con `sumar(255, 1)`? Adivina, y luego corre la celda.
""")
    codigo('''
interruptores.dibujar(sumar(255, 1), etiquetas=TABLA_DE_VALORES,
                      mostrar_bool=False, titulo="255 + 1")
''')
    md("""
Todos apagados. Cero.

Eso se llama **desbordamiento**, y no es un detalle académico:

- En **Pac-Man**, el contador de niveles usaba ocho interruptores. Al llegar al
  nivel 256 se desbordó y media pantalla se convirtió en basura. Nadie pudo pasar
  de ahí durante años.
- En 1996 el cohete **Ariane 5** se autodestruyó 37 segundos después de despegar.
  Un número no cupo donde lo estaban metiendo. Costó 370 millones de dólares.

Tu sumador tiene exactamente el mismo límite que ellos. No porque esté mal hecho:
porque los interruptores se acaban.

### 🤔 Para pensar

Si un interruptor solo puede estar prendido o apagado, no hay dónde poner el
signo menos. ¿Cómo guardarías un número **negativo**?
""")
```

Y agrega `seccion_sumador()` a la llamada final.

- [ ] **Step 2: Reconstruye**

Run: `python3 herramientas/construir_notebook.py`
Expected: `escritas 66 celdas`

- [ ] **Step 3: Ejecuta la notebook**

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

Expected: termina sin excepción.

- [ ] **Step 4: Confirma a mano que el sumador acertó las 16,384**

```bash
python3 -c "
import json
celdas = json.load(open('la-piedra-que-aprendio-a-contar.ipynb', encoding='utf-8'))['cells']
texto = ''.join(''.join(s.get('text', '')) for c in celdas for s in c.get('outputs', [])
                if s.get('output_type') == 'stream')
assert '16,384 de 16,384' in texto, 'el sumador no acerto todas'
print('el sumador acerto las 16,384')
"
```

Expected: `el sumador acerto las 16,384`

- [ ] **Step 5: Corre el guardián**

Run: `python3 -m pytest tests/test_notebook.py -v`
Expected: 5 passed. `test_el_alumno_escribe_el_concepto_a_mano` ahora sí encuentra las siete firmas.

- [ ] **Step 6: Comitea**

```bash
git add herramientas/construir_notebook.py la-piedra-que-aprendio-a-contar.ipynb
git commit -m "feat: seccion 5, el sumador construido a mano sin un solo signo de mas"
```

---

### Task 15: §6 · La torre

**Files:**
- Create: `shift_enter/torre.py`
- Create: `tests/test_torre.py`
- Modify: `herramientas/construir_notebook.py`
- Modify: `la-piedra-que-aprendio-a-contar.ipynb`

**Interfaces:**
- Consumes: `sumar` de la §5.
- Produces: `shift_enter.torre.LAS_CAPAS: list[tuple[str, str]]` de nueve capas; `shift_enter.torre.dibujar(capas=None, ax=None) -> matplotlib.axes.Axes`.

El spec listaba seis módulos. Este es un séptimo: la torre es un diagrama y no cabe en ninguno de los otros seis sin ensuciarlos.

- [ ] **Step 1: Escribe la prueba que falla**

```python
# tests/test_torre.py
import matplotlib
matplotlib.use("Agg")

from shift_enter import torre


def test_la_torre_tiene_nueve_capas():
    assert len(torre.LAS_CAPAS) == 9


def test_la_torre_empieza_en_la_arena_y_acaba_en_el_alumno():
    assert torre.LAS_CAPAS[0][0] == "Arena y electricidad"
    assert torre.LAS_CAPAS[-1][0] == "Esta celda"


def test_dibujar_pinta_un_rectangulo_por_capa():
    eje = torre.dibujar()
    assert len(eje.patches) == 9
```

- [ ] **Step 2: Corre la prueba y confirma que falla**

Run: `python3 -m pytest tests/test_torre.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'shift_enter.torre'`

- [ ] **Step 3: Escribe el módulo**

```python
# shift_enter/torre.py
"""La torre de capas, de la arena hasta esta celda."""

import matplotlib.pyplot as plt

LAS_CAPAS = [
    ("Arena y electricidad", "fisica. Aqui no hay ideas todavia"),
    ("Transistor", "un interruptor sin partes moviles"),
    ("Compuerta", "NO, Y, O            ← lo construiste en §5"),
    ("Bit", "prendido o apagado  ← §4"),
    ("Byte", "ocho bits: un numero, una letra, un pixel  ← §1, §2 y §4"),
    ("Sumador", "13 + 29 = 42        ← §5"),
    ("Instruccion", "lo unico que el procesador entiende"),
    ("Python", "el + que usaste sin pensarlo"),
    ("Esta celda", "aqui estas tu"),
]


def dibujar(capas=None, ax=None):
    """La torre completa, de abajo hacia arriba."""
    capas = LAS_CAPAS if capas is None else capas
    propia = ax is None
    if propia:
        _, ax = plt.subplots(figsize=(11, 7))

    for i, (nombre, detalle) in enumerate(capas):
        tono = 0.94 - i * 0.055
        ax.add_patch(plt.Rectangle((0, i), 10, 0.86, facecolor=str(tono),
                                   edgecolor="white", linewidth=2))
        color = "black" if tono > 0.5 else "white"
        ax.text(0.25, i + 0.43, nombre, va="center", ha="left",
                fontsize=13, weight="bold", color=color)
        ax.text(3.6, i + 0.43, detalle, va="center", ha="left",
                fontsize=10.5, color=color)

    ax.set_xlim(0, 10)
    ax.set_ylim(-0.3, len(capas) + 0.2)
    ax.axis("off")
    ax.set_title("La torre", fontsize=15, pad=15)
    if propia:
        plt.tight_layout()
        plt.show()
    return ax
```

- [ ] **Step 4: Corre la prueba y confirma que pasa**

Run: `python3 -m pytest tests/test_torre.py -v`
Expected: 3 passed

- [ ] **Step 5: Agrega la sección al constructor**

```python
def seccion_torre():
    md("""
---

# 6 · Las capas

Tú escribiste `sumar` con compuertas. Python trae un `+` que ya venía hecho.

Hacen lo mismo. ¿Para qué existen los dos? Corre esto.
""")
    codigo('''
inicio = time.perf_counter()
for _ in range(300):
    sumar(13, 29)
tuyo = (time.perf_counter() - inicio) / 300

inicio = time.perf_counter()
for _ in range(300000):
    13 + 29
de_python = (time.perf_counter() - inicio) / 300000

print(f"   tu sumador:      {tuyo * 1e6:>10.1f} microsegundos")
print(f"   el + de Python:  {de_python * 1e6:>10.4f} microsegundos")
print()
print(f"   El tuyo es unas {tuyo / de_python:,.0f} veces mas lento.")
''')
    md("""
### Por qué

Tu sumador **simula** compuertas usando software, que a su vez corre sobre
compuertas de verdad grabadas en silicio, que hacen la misma operación miles de
millones de veces por segundo.

Construiste una computadora dentro de una computadora. Por eso es lenta, y por
eso valió la pena: pudiste verla por dentro.

El `+` de Python no es más listo que el tuyo. Solo está más abajo en la torre.
""")
    codigo('''
torre.dibujar()
''')
    md("""
### Lo que se aprende bajando

Cada capa de esa torre existe por una sola razón: **para que no tengas que pensar
en la de abajo**.

El que escribe un videojuego no piensa en transistores. El que diseña
transistores no piensa en videojuegos. Y así funciona todo, hasta el día que algo
se rompe y alguien tiene que saber bajar.

Hoy bajaste hasta el fondo. Abriste tu nombre, tu cara y tu música, tocaste el
interruptor, lo conectaste, le enseñaste a contar, le enseñaste a sumar, y
volviste a subir.

La piedra ya cuenta.
""")
    md("""
---

## 🤔 Y sin embargo

Tu sumador no ha hecho nada por su cuenta.

Se quedó ahí, quieto, esperando a que tú corrieras la celda. Sabe sumar, pero no
sabe **cuándo** sumar, ni **qué** sumar, ni qué hacer después.

Le falta algo que no es una compuerta ni un número:

> Una receta. Alguien que le diga qué hacer, y en qué orden.

Eso es la siguiente presentación: **la venida del proceso**.
""")
```

Y agrega `seccion_torre()` a la llamada final.

- [ ] **Step 6: Agrega `time` y `torre` a la celda de forma**

En `portada()`, dentro del bloque `forma(...)`, cambia las dos líneas de importación por estas tres:

```python
import time

from shift_enter import cifra, imagen, interruptores, paleta, sonido, torre
from shift_enter.binario import TABLA_DE_VALORES, a_binario, a_decimal
from shift_enter.interruptores import simbolo
```

`time` va en la celda de forma y no en una celda visible, porque el guardián prohíbe que una celda visible importe nada.

- [ ] **Step 7: Reconstruye**

Run: `python3 herramientas/construir_notebook.py`
Expected: `escritas 72 celdas`

- [ ] **Step 8: Ejecuta la notebook**

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

Expected: termina sin excepción.

- [ ] **Step 9: Corre el guardián**

Run: `python3 -m pytest tests/test_notebook.py -v`
Expected: 5 passed

- [ ] **Step 10: Comitea**

```bash
git add shift_enter/torre.py tests/test_torre.py herramientas/construir_notebook.py la-piedra-que-aprendio-a-contar.ipynb
git commit -m "feat: seccion 6, la torre y el cierre hacia la venida del proceso"
```

---

### Task 16: Verificación final y retiro del andamio

**Files:**
- Delete: `herramientas/construir_notebook.py`
- Modify: `la-piedra-que-aprendio-a-contar.ipynb`

**Interfaces:**
- Consumes: todo lo anterior.
- Produces: nada nuevo. Deja el repo con el paquete, sus pruebas, el guardián y la notebook ejecutada.

- [ ] **Step 1: Corre la suite completa**

Run: `python3 -m pytest tests/ -v`
Expected: 51 passed

- [ ] **Step 2: Re-ejecuta la notebook una última vez, desde cero**

```bash
python3 -c "
import nbformat
from nbclient import NotebookClient
p = 'la-piedra-que-aprendio-a-contar.ipynb'
nb = nbformat.read(p, as_version=4)
NotebookClient(nb, timeout=600, kernel_name='python3',
               resources={'metadata': {'path': '.'}}).execute()
nbformat.write(nb, p)
"
```

Expected: termina sin excepción.

- [ ] **Step 3: Confirma que ninguna celda quedó con error**

```bash
python3 -c "
import json
c = json.load(open('la-piedra-que-aprendio-a-contar.ipynb', encoding='utf-8'))['cells']
print([i for i, x in enumerate(c)
       if any(o.get('output_type') == 'error' for o in x.get('outputs', []))] or 'sin errores')
"
```

Expected: `sin errores`

- [ ] **Step 4: Confirma que el paquete se instala limpio desde cero**

```bash
python3 -m pip uninstall -y shift-enter
python3 -m pip install .
python3 -c "
from shift_enter import cifra, imagen, interruptores, paleta, sonido, torre
print('la foto de respaldo mide', imagen.de_respaldo().shape)
"
python3 -m pip install -e .
```

Expected: imprime las medidas de la foto. Esto prueba que `datos/leibniz.jpg` viaja dentro del paquete y no solo en el repo.

- [ ] **Step 5: Retira el andamio**

```bash
git rm -r herramientas
```

- [ ] **Step 6: Comitea**

```bash
git add -A
git commit -m "chore: retira el andamio de construccion y deja la notebook ejecutada"
```

- [ ] **Step 7: Reporta lo que queda pendiente del autor**

Estas tres cosas no las puede cerrar el código y hay que decírselas al autor:

1. **Hacer público el repo** `github.com/nrqrmz/shift-enter`. Mientras esté privado, la línea de instalación de la celda de forma falla para cualquier alumno.
2. **Unificar la rama.** El repo local está en `master` y el README apunta a `main`.
3. **Probarla con un chico de doce años.** Ninguna de las 51 pruebas mide lo único que importa, que es si se engancha.

---

## Notas de ejecución

- **Las tareas 1 a 8 y 15 son del paquete** y se pueden trabajar en paralelo si se
  respetan las interfaces declaradas. Las tareas 9 a 16 son secuenciales: cada
  sección de la notebook usa variables que definió la anterior.
- **`mi_nombre` viaja de la §1 a la §3 y a la §4.** `prendido` y `apagado` viajan
  de la §4 a la §5. Reordenar secciones rompe la notebook.
- **Si una celda falla, `nbclient` deja el archivo intacto.** Un script de edición
  mal escrito no. Respalda antes de reconstruir.
- **Los conteos de celdas de cada tarea son una verificación**, no un adorno. Si
  no coinciden, falta o sobra una celda.
