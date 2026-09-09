"""Deja la suite muda y ciega: nada de ventanas, nada de pestañas.

Esto corre antes que cualquier modulo de prueba. Sin esto, dos cosas se
escapan del proceso de pytest hacia el mundo real:

- matplotlib, sin backend explicito, intenta abrir una ventana grafica
  (TkAgg u otro backend interactivo) en cuanto algun test importa pyplot.
- plotly, fuera de un kernel de Jupyter, resuelve su renderer por omision
  a "browser": cada figura.show() abre una pestaña nueva del navegador.

"plotly_mimetype" emite un payload de display para IPython, que no hace
nada en absoluto fuera de un kernel, asi que .show() queda inerte aqui sin
tocar mostrar_con_numeros ni el renderer que fija la propia celda de forma
de la notebook para Colab.

No borrar esto: sin las dos lineas de abajo, correr `pytest` vuelve a
abrirle una ventana y un navegador al que lo corra.
"""

import matplotlib
matplotlib.use("Agg")

import plotly.io as pio
pio.renderers.default = "plotly_mimetype"
