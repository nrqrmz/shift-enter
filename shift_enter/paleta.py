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
