import pandas as pd
import numpy as np
import requests as rq

# Código para construir un DataFrame con la información de los 250 países
# del API Restcountries

# Al final no usé la librería python porque creo que es más sencillo
# meter directamente el JSON en Pandas para crear las Series

def stringListToString(inputlist):
    ret = ""
    for item in inputlist:
        ret = ret + str(item) + ", "

    return ret[0:-2]

def get_all_countries():
    resp = rq.get("https://restcountries.eu/rest/v2/all")

    if (resp.status_code > 400):
        raise Exception("Error getting data from the API")

    jsondata = resp.json()
    series_paises = []

    for pais in jsondata:
        serie_pais = pd.Series(data=pais, name=pais['name'])

        #Eliminamos el nombre como atributo porque es redundante
        serie_pais.drop("name", inplace=True)

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

        series_paises.append(serie_pais)

    dataframe_paises = pd.concat(series_paises, axis=1)

    return dataframe_paises
