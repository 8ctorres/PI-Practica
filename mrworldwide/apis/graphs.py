import worldbank as wb
import restcountries as rc
import aqicn as aq
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Dada una lista de dataframes cuyo índice sea una serie temporal,
# muestra un gráfico comparando la progresión de todos los valores
# a lo largo del tiempo
def grafico_lineas(inds, filename=None):
    newdf = pd.concat(inds, axis=1)
    newdf.plot.line()
    if filename is not None:
        plt.savefig(filename)

# Dadas dos series, saca un gráfico
# de dispersión de las dos
def grafico_dispersion(xind, yind, filename=None):
    newdf = pd.concat([xind, yind], axis=1)
    newdf.plot.scatter(x=xind.name, y=yind.name)
    if filename is not None:
        plt.savefig(filename)


if __name__ == "__main__":
    esp = wb.get_indicator("esp", "ny.gdp.mktp.cd").value
    esp.name = "Spain"
    prt = wb.get_indicator("prt", "ny.gdp.mktp.cd").value
    prt.name = "Portugal"
