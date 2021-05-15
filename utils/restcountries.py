import pandas as pd
import numpy as np
import requests as rq

# Código para construir un DataFrame con la información de los 250 países
# del API Restcountries

# Al final no usé la librería python porque creo que es más sencillo
# meter directamente el JSON en Pandas para crear las Series

base_url = "https://restcountries.eu/rest/v2/"

def stringListToString(inputlist):
    ret = ""
    for item in inputlist:
        ret = ret + str(item) + ", "

    return ret[0:-2]

def jsonToSeries(pais):
    # Identificamos la Serie correspondiente a cada país por su código ISO de 3 caracteres
    # Así es sencillo luego usarlos en la api del worldbank porque usa los mismos códigos
    serie_pais = pd.Series(data=pais, name=pais['alpha3Code'])
    serie_pais.drop("alpha3Code", inplace=True)

    #El TLD viene como una lista de un solo elemento
    #Solo hay un par de regiones que tienen 2 TLDs. Para esas almacenamos solo el primero
    serie_pais.topLevelDomain = serie_pais.topLevelDomain[0]

    #Solo hay 3 regiones que tienen más de un prefijo telefónico
    #Para esas, almacenamos un string en lugar de una string list
    serie_pais.callingCodes = stringListToString(serie_pais.callingCodes)

    #De las monedas en curso nos quedamos solo con el nombre de la principal
    serie_pais.currencies = serie_pais.currencies[0]['name']

    #De los idiomas nos quedamos solo con el nombre, y los guardamos como
    #un solo string
    serie_pais.languages = stringListToString([x['name'] for x in serie_pais.languages])

    #Las traducciones las vamos a ignorar ya que añaden complicación al DataFrame innecesariamente
    serie_pais.drop("translations", inplace=True)

    #De los bloques regionales igual, nos quedamos solo con los nombres como un string
    serie_pais.regionalBlocs = stringListToString(x['name'] for x in serie_pais.regionalBlocs)

    return serie_pais

def get_countries_by_name(name):
    resp = rq.get(base_url+"name/"+name)

    if (resp.status_code > 400):
        raise Exception("Error getting data from the API")

    return pd.concat([jsonToSeries(pais) for pais in resp.json()], axis=1).transpose()

def get_all_countries():
    resp = rq.get(base_url+"all")

    if (resp.status_code > 400):
        raise Exception("Error getting data from the API")

    return pd.concat([jsonToSeries(pais) for pais in resp.json()], axis=1).transpose()
