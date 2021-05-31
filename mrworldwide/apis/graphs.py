from apis import worldbank as wb, restcountries as rc
from apis.exceptions import APIRequestException
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

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
            serietodos = serietodos.append(pd.Series(data={code: valor}))
        except APIRequestException:
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
        df.plot.scatter(x=ind1.name, y=ind1.name)
    else if tipo=="l":
        df.plot()
    else:
        raise TypeError("Unknown type: "+tipo)

    if filename is not None:
        plt.savefig(filename)

    return df


def graph_1dataXcountries(ind, paises, filename=None):
    # Construimos el dataframe con todos los países
    df = pd.concat([wb.get_indicator(pais, ind) for pais in paises], axis=1)

    # Dibujamos el gráfico
    df.plot()

    # Guardamos
    if filename is not None:
        plt.savefig(filename)

    # Devolvemos el dataframe
    return df

def graph_Xdata1country(inds, pais, filename=None):
    df = pd.concat([wb.get_indicator(pais, ind) for ind in inds], axis=1)
    df.plot
    if filename is not None:
        plt.savefig(filename)
    return df

#TODO: Histograma

# Funcion que recorre el directorio temporal donde están los JPGs antiguos de los gráfico
# y los va eliminando
# Se le pasa como parámetro la ruta al directorio a limpiar, y opcionalmente un lifetime
# como de antiguo tiene que ser un fichero para eliminarlo) en minutos. Por defecto son 15

def clear_old_graphs(path, lifetime=15):
    dir = os.scandir(path)
    for file in dir:
        #Comprobamos que sea una foto por seguridad, por si alguien se equivoca al llamar la función no cargarnos medio proyecto
        #Si la fecha de modificación es anterior a "lifetime" minutos desde ahora mismo, eliminarlo
        if file.is_file() and file.name.endswith(".jpg") and ((datetime.now().timestamp() - file.stat().st_mtime) > lifetime*60):
            os.remove(file)
