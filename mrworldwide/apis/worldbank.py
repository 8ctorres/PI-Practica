"""
   Código para extraer datos del API de Worldbank y cargarlos en estructuras de datos de Pandas
"""

# # https://datahelpdesk.worldbank.org/knowledgebase/topics/1255


import pandas as pd
import numpy as np
import requests as rq
from apis.exceptions import APIRequestException

indicators_url = "http://api.worldbank.org/v2/indicator"
countries_url = "http://api.worldbank.org/v2/country"
topics_url = "http://api.worldbank.org/v2/topic"

# Devueve un dataframe con información sobre los distintos temas que trata
# el índice es el "id" del tema, y los atributos son el nombre y una descripción

def get_topics_list():
    resp = rq.get(topics_url+"?format=json&per_page=100")

    if resp.status_code > 400:
       raise APIRequestException("HTTP Error")

    try:
        jsondata = resp.json()[1] #Dejo la primera entrada porque es información de paginación
    except ValueError:
        raise APIRequestException("JSON Decode failed")

    series_temas = [(pd.Series(data=tema, name=tema['id']).drop("id")) for tema in jsondata]

    dataframe_temas = pd.concat(series_temas, axis=1).transpose()
    dataframe_temas.index.name = "id"
    dataframe_temas.columns = ["topicName", "description"]

    return dataframe_temas


# Devuelve un dataframe con los IDs, nombres y descripciones de todos los indicadores de un tema
# Se espera que se pase el ID del tema (obtenido a través de la anterior función)
def get_indicators_from_topic(topic):
    resp = rq.get(topics_url+"/"+topic+"/indicator"+"?format=json&per_page=20000")

    if resp.status_code > 400:
        raise APIRequestException("HTTP Error")

    try:
        jsondata = resp.json()[1]
    except ValueError:
        raise APIRequestException("JSON Decode failed")

    series_indics = []

    for indic in jsondata:
        # Creamos la serie y ponemos el ID como nombre de la serie
        serie = pd.Series(data=indic, name=indic['id']).drop("id")

        # Renombramos a indicatorName para evitar confusiones
        serie.rename(index={'name': 'indicatorName'}, inplace=True)

        # Sacamos los "topics" ya que no van a hacernos falta
        # (ya sabíamos el topic para pedir el indicador)
        serie.drop("topics", inplace=True)

        # Separamos el "source" que es un diccionario en sus campos "sourceID" y "SourceName"
        tsourceID = serie.source['id']
        tsourceName = serie.source['value']
        serie.drop("source", inplace=True)

        # Y reindexamos para tenerla ordenada
        serie = serie.reindex(
            pd.Index(data=
                     ["name", "unit", "sourceID",
                      "sourceName", "sourceNote", "sourceOrganization"]))

        serie.sourceID = tsourceID
        serie.sourceName = tsourceName

        # La añadimos a la lista

        series_indics.append(serie)

    # Montamos el DataFrame
    dataframe_indicadores = pd.concat(series_indics, axis=1).transpose()
    dataframe_indicadores.index.name = "indicatorID"

    return dataframe_indicadores


# Esta función devuelve un dataframe con los valores asociados al indicador en el país indicados,
# organizados de forma que cada columna del dataframe corresponde a un período de tiempo.
# Los nombres de las columnas indican el periodo al que se refiere (p.e: 2018, 2019, 2020...)
# Las filas dependen del indicador en cuestión, pero hay siempre una fila "value" que tiene
# el valor en crudo

def get_indicator(country, indicator):
    resp = rq.get(countries_url+"/"+country+"/indicator/"+indicator+"?format=json&per_page=500")

    if resp.status_code > 400:
        raise APIRequestException("HTTP Error")

    try:
        jsondata = resp.json()[1]
    except ValueError:
        raise APIRequestException("JSON Decode failed")

    jsondata.reverse() # La API los entrega de más reciente a más antiguo

    series_inds = []

    for year in jsondata:
        serie_ind = pd.Series(data=year, name=year['date']).drop("date")

        #WIP: Desgranamos Indicador y Country, que son diccionarios, en sus dos componentes

        tindicator_id = serie_ind.indicator['id']
        tindicator_name = serie_ind.indicator['value']

        tcountry_id = serie_ind.country['id']
        tcountry_name = serie_ind.country['value']

        serie_ind.drop("indicator", inplace=True)
        serie_ind.drop("country", inplace=True)

        serie_ind = serie_ind.reindex(
            pd.Index(["indicatorId", "indicatorName", "countryId", "countryName",
                                     "countryiso3code", "value", "unit", "obs_status", "decimal"]))

        serie_ind.indicatorId = tindicator_id
        serie_ind.indicatorName = tindicator_name
        serie_ind.countryId = tcountry_id
        serie_ind.countryName = tcountry_name

        series_inds.append(serie_ind)

    dataframe_ind = pd.concat(series_inds, axis=1).transpose()
    # Convertimos el índice a serie temporal para poder tratarlo
    # más fácilmente luego
    dataframe_ind.index = pd.to_datetime(dataframe_ind.index)
    dataframe_ind.index.name = "Periodo"

    return dataframe_ind
