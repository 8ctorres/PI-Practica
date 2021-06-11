from apis import worldbank as wb, restcountries as rc
from apis.exceptions import APIRequestException
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

## Caso de uso de ordenar los top N países por un indicador
## Por defecto es el top 10, el máximo son 200
def get_ind_global(ind):
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
            try:
                valor = serieind[serieind.last_valid_index()]
            except KeyError:
                # No hay un last valid index porque no hay datos
                raise APIRequestException("No data for this country")
            #Construyo una nueva Series con los nombres de los países como índice
            serietodos = serietodos.append(pd.Series(data={code: valor}))
        except APIRequestException:
            #Un error significa que el país no estaba en WorldBank
            #Puede pasar ya que Restcountries también contempla regiones administrativas
            #que formalmente no son países
            #Simplemente ignoramos y seguimos
            continue;
    return serietodos

def top_n_indicador(ind, n=10):
    # Me quedo con los N top países
    return get_ind_global(ind).nlargest(n, keep="all")

def graph_topn(ind, n=10, filename=None):
    # Peticion a la API
    serietop = top_n_indicador(ind, n)

    # Construyo el gráfico
    graf = serietop.plot.bar(figsize=(10,8))

    # Si es el caso, lo guardo
    if filename is not None:
        plt.savefig(filename)

    # Devuelvo la serie para poder reutilizarla si fuera necesario
    return serietop


# Dado un indicador y un par de países, saca un gráfico comparando
# la relación entre los dos. El parámetro "tipo" indica si va a ser
# un gráfico de líneas ("l") o de dispersión de puntos ("d")
def graph_comparacion(ind, pais1, pais2, filename=None, tipo="l"):
    # Hacemos la consulta del indicador a la API de Worldbank, y nos quedamos con
    # una serie temporal con los valores en crudo (columna "value")
    # Y descartamos los valores nulos
    ind1 = wb.get_indicator(pais1, ind).value.dropna()
    # Le damos un nombre a la Serie
    ind1.name = pais1

    ind2 = wb.get_indicator(pais2, ind).value.dropna()
    ind2.name = pais2

    df = pd.concat([ind1, ind2], axis=1)

    if tipo=="d":
        df.plot.scatter(x=ind1.name, y=ind1.name, figsize=(10,8))
    elif tipo=="l":
        df.plot(figsize=(10,8))
    else:
        raise TypeError("Unknown type: "+tipo)

    if filename is not None:
        plt.savefig(filename)

    return df


def graph_1dataXcountries(ind, paises, filename=None):
    # Construimos el dataframe con todos los países
    data = [wb.get_indicator(pais, ind) for pais in paises]
    series = []

    for ind in data:
        serie = ind.value.dropna()
        serie.name = ind.countryName.iloc[0]
        series.append(serie)

    df = pd.concat(series, axis=1)

    df.plot(figsize=(10,8))

    # Guardamos
    if filename is not None:
        plt.savefig(filename)

    # Devolvemos el dataframe
    return df

def graph_Xdata1country(inds, pais, filename=None):
    data = [wb.get_indicator(pais, ind) for ind in inds]
    series = []

    for ind in data:
        serie = ind.value.dropna()
        serie.name = ind.indicatorName.iloc[0]
        series.append(serie)

    df = pd.concat(series, axis=1)

    #TODO: Mirar el tema de hacerlos en varias escalas para evitar que uno opaque a los otros
    df.plot(figsize=(10,8))

    if filename is not None:
        plt.savefig(filename)
    return df

def graph_histograma(ind, filename=None):
    indglobal = get_ind_global(ind)
    indglobal.plot.hist(figsize=(10,8), bins=16)

    if filename is not None:
        plt.savefig(filename)

    return indglobal
