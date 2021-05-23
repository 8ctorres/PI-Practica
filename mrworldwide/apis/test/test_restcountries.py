import unittest
from django.test import TestCase
import pandas as pd
import numpy as np
import restcountries

class RestCountriesTest(TestCase):

    # Test consistente en hacer una petición a la API, extraer los datos
    # de un país cualquiera (para el caso, Italia y Canada), y comprobar
    # que los resultados son los esperados
    def test_get_info(self):
        allcountries = get_all_countries()
        italy = allcountries.loc['ITA']
        self.assertEquals(italy.countryName, "Italy")
        self.assertEquals(italy.region, "Europe")
        self.assertEquals(italy.alpha2Code, "IT")
        self.assertEquals(italy.capital, "Rome")
        canada = allcountries.loc['CAN']
        self.assertEquals(canada.countryName, "Canada")
        self.assertEquals(canada.region, "Americas")
        self.assertEquals(canada.alpha2Code, "CA")
        self.assertEquals(canada.capital, "Ottawa")

    # Test consistente en intentar extraer información de un país que no existe
    @unittest.expectedFailure
    def test_get_mordor(self):
        allcountries = get_all_countries()
        mordor = allcountries.loc['Mordor']
