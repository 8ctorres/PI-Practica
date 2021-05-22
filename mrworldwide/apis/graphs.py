from apis import worldbank as wb, aqicn as aq, restcountries as rc
from apis.exceptions import APIRequestException
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

## Caso de uso de ordenar los top N países por un indicador
## Por defecto es el top 10, el máximo son 200

def top_n_indicador(ind, n=10):
    # Saco la información de todos los países del mundo
    allcountries = rc.get_all_countries()
    # Me quedo con una lista de los alpha3code, para consultar worldbank
    codes = allcountries.index.to_list()
    # Para cada uno de los 250 países, obtengo el indicador en cuestión,
    # busco el último valor no nulo y lo meto en una Series
    serietodos = pd.Series(dtype="float64", name=ind)
    for code in codes:
        try:
            serieind = wb.get_indicator(code, ind).value
            valor = serieind[serieind.last_valid_index()]
            #Construyo una nueva Series con los nombres de los países como índice
            serietodos = serietodos.append(pd.Series(data={allcountries.loc[code].countryName: valor}))
        except APIRequestException: #TODO resolver los problemas con el import de la exception
            #Un error significa que el país no estaba en WorldBank
            #Puede pasar ya que Restcountries también contempla regiones administrativas
            #que formalmente no son países
            #Simplemente ignoramos y seguimos
            continue;

    # Me quedo con los N top países
    serietop = serietodos.nlargest(n, keep="all")
    return serietop

def graph_topn(ind, n=10, filename=None):
    # Peticion a la API
    serietop = top_n_indicador(ind, n)

    # Construyo el gráfico
    graf = serietop.plot.bar()

    # Si es el caso, lo guardo
    if filename is not None:
        plt.savefig(filename)

    # Devuelvo la serie para poder reutilizarla si fuera necesario
    return serietop










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
