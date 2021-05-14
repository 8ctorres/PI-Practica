import unittest
from django.test import TestCase

class AQICNTest(TestCase):
    # Test consistente en leer los datos de la ciudad de Bilbao. Como
    # no sabemos de antemano cuales van a ser los datos, solo podemos
    # comprobar que no son nulos, que son del tipo correcto, y que tienen
    # sentido (i.e. no son negativos, NaN...)
    def test_bilbao():
        aire_bilbao = get_feed_ciudad("Bilbao")
        self.assertEquals(aire_bilbao.name, "Bilbao")
        self.assertEquals(type(aire_bilbao.no2), numpy.float64)
        self.assertTrue(aire_bilbao.o3 > 0)
