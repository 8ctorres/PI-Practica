from django.test import TestCase, Client
from compare_data.views import *

# Create your tests here.
class CompareDataTest(TestCase):

    def setUp(self):
        self.c = Client()

    def test_badtopic(self):
        resp = self.c.get("/compare_data/compare", {"choose_topic": "Patatas"})
        self.assertEquals(resp.status_code, 404)

    def test_badcountry(self):
        resp = self.c.get("/compare_data/result", {"compare_country1": "Brazil", "compare_country2" : "La Coru neno", "compare_indicator": "Population"})
        self.assertEquals(resp.status_code, 404)
        
    def test_badindicator(self):
        resp = self.c.get("/compare_data/result", {"compare_country1": "Brazil", "compare_country2" : "Germany", "compare_indicator": "Numero de koruños por metro cuadrado"})
        self.assertEquals(resp.status_code, 404)

    def test_funciona(self):
        resp = self.c.get("/compare_data/result", {"compare_country1": "Brazil", "compare_country2" : "Germany", "compare_indicator": "Population"})
        self.assertEquals(resp.status_code, 200)