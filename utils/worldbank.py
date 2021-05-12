"""
   Código para extraer datos del API de Worldbank y cargarlos en estructuras de datos de Pandas
"""

# # https://datahelpdesk.worldbank.org/knowledgebase/topics/1255


import pandas as pd
import numpy as np
import requests as rq

indicators_url = "http://api.worldbank.org/v2/indicator"
countries_url = "http://api.worldbank.org/v2/country"
topics_url = "http://api.worldbank.org/v2/topic"

def get_topics_list():

    resp = rq.get(topics_url+"?format=json&per_page=100")

    if resp.status_code != 200:
        raise Exception("API Request Failed")

    jsondata = resp.json()[1]

    series_temas = []

    for tema in jsondata:
        series_temas.append(pd.Series(data=tema, name=tema['value']).drop("value"))

    dataframe_temas = pd.concat(series_temas, axis=1)

    return dataframe_temas


## Devuelve un dataframe con los nombres, IDs y descripciones de todos los indicadores de un tema
## Se espera que se pase el ID del tema (obtenido a través de la anterior función)
def get_indicators_list(topic):

    resp = rq.get(topics_url+"/"+topic+"/indicator"+"?format=json&per_page=20000")

    if resp.status_code != 200:
        raise Exception("API Request Failed")


    jsondata = resp.json()[1] ## La primera de la entrada de la lista es la de paginación

    series_indicadores = []

    for indic in jsondata:
        series_indicadores.append(pd.Series(data=indic, name=indic['name']).drop("name"))

    dataframe_indicadores = pd.concat(series_indicadores, axis=1)

    return dataframe_indicadores


# Esta función devuelve un dataframe con los valores asociados al indicador en el país indicados,
# organizados de forma que cada columna del dataframe corresponde a un período de tiempo.
# Los nombres de las columnas indican el periodo al que se refiere (p.e: 2018, 2019, 2020...)
# Las filas dependen del indicador en cuestión, pero hay siempre una fila "value" que tiene
# el valor en crudo

def get_country_indicator(country, indicator):

    resp = rq.get(countries_url+"/"+country+"/indicator/"+indicator+"?format=json&per_page=500")

    if resp.status_code != 200:
        raise Exception("API Request Failed")

    jsondata = resp.json()[1]  ## La primera entrada de la lista es la información de paginación

    jsondata.reverse() # La API los entrega de más reciente a más antiguo, y prefiero tenerlos ordenados

    series_inds = []

    for year in jsondata:

        serie_ind = pd.Series(data=year, name=year['date']).drop("date")

        indicator_id = serie_ind.indicator['id']
        indicator_name = serie_ind.indicator['value']

        country_id = serie_ind.country['id']
        country_name = serie_ind.country['value']

        serie_ind.drop("indicator", inplace=True)
        serie_ind.drop("country", inplace=True)

        serie_ind.reindex (pd.Index(["indicator_id", "indicator_name", "country_id", "country_name",
                                     "countryiso3code", "value", "unit", "obs_status", "decimal"],
                                   dtype="object"))

        serie_ind.indicator_id = indicator_id
        serie_ind.indicator_name = indicator_name
        serie_ind.country_id = country_id
        serie_ind.country_name = country_name

        series_inds.append(serie_ind)


    dataframe_ind = pd.concat(series_inds, axis=1)

    return dataframe_ind
