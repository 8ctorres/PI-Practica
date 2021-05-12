"""
    Código básico para ir extrayendo datos de AQICN y cargándolos en estructuras de Pandas
    La idea es que luego esto lo copiemos ya dentro del proyecto de Django cuando tengamos
    claro el sitio donde copiarlo

"""

import pandas as pd
import numpy as np
import requests as rq

base_url = "https://api.waqi.info/"
token = "b7818feb850f1306340bd0465824027131b20af8"

# Obtener los datos de una o varias ciudades
# Esta función acepta una lista de ciudades (strings)
# y devuelve un DataFrame que contiene los datos de polución
# del aire disponibles para esas ciudades

def get_feed_ciudades(ciudades):
    series_ciudades = []
    for ciudad in ciudades:
        series_ciudades.append(get_feed_ciudad(ciudad))

    dataframe_ciudades = pd.concat(series_ciudades, axis=1)
    dataframe_ciudades.columns = ciudades

    return dataframe

def get_feed_ciudad(ciudad):
    resp = rq.get(base_url+"feed/"+ciudad+"/?token="+token)

    if resp.json()['status'] != "ok":
        raise Exception("API Request failed")

    datos_ciudad = resp.json()['data']['iaqi']

    serie_ciudad = pd.Series(datos_ciudad).apply(lambda x: x['v'])
    serie_ciudad.name = ciudad

    return serie_ciudad


def get_datos_coords(lat=None, lon=None):
    if lat is None or lon is None:
        raise ValueError("No se indicaron coordenadas")

    resp = rq.get(base_url+"feed/geo:"+str(lat)+";"+str(lon)+"/?token="+token)
    jsondata = resp.json()

    if jsondata['status'] != "ok":
        raise Exception("API Request failed")

    datos_loc = jsondata['data']['iaqi']
    nombre_loc = jsondata['data']['city']['name']

    serie = pd.Series(datos_loc).apply(lambda x: x['v'])
    serie.name = nombre_loc

    return serie

