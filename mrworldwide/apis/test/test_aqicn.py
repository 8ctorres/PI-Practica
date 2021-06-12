import unittest
from django.test import TestCase
import numpy
from aqicn import get_datos_ciudad

class AQICNTest(TestCase):
    # Test consistente en leer los datos de la ciudad de Bilbao. Como
    # no sabemos de antemano cuales van a ser los datos, solo podemos
    # comprobar que no son nulos, que son del tipo correcto, y que tienen
    # sentido (i.e. no son negativos, NaN...)
    def test_bilbao(self):
        aire = get_datos_ciudad("Bilbao")
        self.assertEquals(type(aire.loc['Bilbao'].no2), numpy.float64)
        self.assertTrue(aire.loc['Bilbao'].o3 > 0)
