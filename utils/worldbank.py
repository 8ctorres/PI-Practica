"""
   Código para extraer datos del API de Worldbank y cargarlos en estructuras de datos de Pandas
"""

# # https://datahelpdesk.worldbank.org/knowledgebase/topics/1255


import pandas as pd
import numpy as np
import requests as rq

indicators_url = "http://api.worldbank.org/v2/indicator"
countries_url = "http://api.worldbank.org/v2/country"


## Devuelve un dataframe con los nombres, IDs y descripciones de todos los indicadores disponibles para su consulta
def get_indicators_list():

    resp = rq.get(indicators_url+"?format=json&per_page=50000")

    if resp.status_code != 200:
        raise Exception("API Request Failed")


    jsondata = resp.json()[1] ## La primera de la entrada de la lista es la de paginación

    series_indicadores = []

    for indic in jsondata:
        series_indicadores.append(pd.Series(data=indic, name=indic['name']).drop("name"))

    dataframe_indicadores = pd.concat(series_indicadores, axis=1)

    return dataframe_indicadores


def get_country_indicator(country, indicator):

    resp = rq.get(countries_url+"/"+country+"/indicator/"+indicator+"?format=json&per_page=50000")

    if resp.status_code != 200:
        raise Exception("API Request Failed")

    jsondata = resp.json()[1]

