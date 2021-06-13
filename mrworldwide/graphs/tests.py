from django.test import TestCase, Client
from graphs.views import *

# Create your tests here.
class OneDataXCountriesTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_badcountry(self):
        resp = self.c.get("/graphs/1dXc_result", {"graph_indicator1": "Population", "graph_country1": "Egypt", "graph_country2": "Ferrol", "graph_country3": "", "graph_country4": "", "graph_country5": ""})
        self.assertEquals(resp.status_code, 404)
        
        resp = self.c.get("/graphs/1dXc_result", {"graph_indicator1": "Population", "graph_country1": "Egypt", "graph_country2": "Germany", "graph_country3": "Madriz", "graph_country4": "", "graph_country5": ""})
        self.assertEquals(resp.status_code, 404)

        resp = self.c.get("/graphs/1dXc_result", {"graph_indicator1": "Population", "graph_country1": "Ferrol", "graph_country2": "Germany", "graph_country3": "France", "graph_country4": "", "graph_country5": ""})
        self.assertEquals(resp.status_code, 404)

        resp = self.c.get("/graphs/1dXc_result", {"graph_indicator1": "Population", "graph_country1": "Ferrol", "graph_country2": "acfqa23d", "graph_country3": "q34cwfra", "graph_country4": "", "graph_country5": ""})
        self.assertEquals(resp.status_code, 404)

    def test_badindicator(self):
        resp = self.c.get("/graphs/1dXc_result", {"graph_indicator1": "afsdf2w", "graph_country1": "Egypt", "graph_country2": "Germany", "graph_country3": "France", "graph_country4": "", "graph_country5": ""})
        self.assertEquals(resp.status_code, 404)

    def test_ok(self):
        resp = self.c.get("/graphs/1dXc_result", {"graph_indicator1": "Population", "graph_country1": "Egypt", "graph_country2": "Germany", "graph_country3": "France", "graph_country4": "", "graph_country5": ""})
        self.assertEquals(resp.status_code, 200)

class OneCountryXDataTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_badcountry(self):
        resp = self.c.get("/graphs/Xd1c_result", {"graph_country1" : "UKA", "graph_indicator1" : "Refugees by country", "graph_indicator2" : "Agricultural land", "graph_indicator3" : "Mortality rate under 5, per 1.000 births", "graph_indicator4" : "", "graph_indicator5" : ""})
        self.assertEquals(resp.status_code, 404)
    
    def test_badindicator(self):
        resp = self.c.get("/graphs/Xd1c_result", {"graph_country1" : "United Kingdom of Great Britain and Northern Ireland", "graph_indicator1" : "sfdaerg", "graph_indicator2" : "Agricultural land", "graph_indicator3" : "Mortality rate under 5, per 1.000 births", "graph_indicator4" : "", "graph_indicator5" : ""})
        self.assertEquals(resp.status_code, 404)

        resp = self.c.get("/graphs/Xd1c_result", {"graph_country1" : "United Kingdom of Great Britain and Northern Ireland", "graph_indicator1" : "Refugees by country", "graph_indicator2" : "arwecvaerv", "graph_indicator3" : "Mortality rate under 5, per 1.000 births", "graph_indicator4" : "", "graph_indicator5" : ""})
        self.assertEquals(resp.status_code, 404)

        resp = self.c.get("/graphs/Xd1c_result", {"graph_country1" : "United Kingdom of Great Britain and Northern Ireland", "graph_indicator1" : "Refugees by country", "graph_indicator2" : "Agricultural land", "graph_indicator3" : "3dvq24cfaerw", "graph_indicator4" : "", "graph_indicator5" : ""})
        self.assertEquals(resp.status_code, 404)

        resp = self.c.get("/graphs/Xd1c_result", {"graph_country1" : "United Kingdom of Great Britain and Northern Ireland", "graph_indicator1" : "Ravwefa we", "graph_indicator2" : "cvasecdawe", "graph_indicator3" : "dvaewrvaerfv", "graph_indicator4" : "", "graph_indicator5" : ""})
        self.assertEquals(resp.status_code, 404)
    
    def test_ok(self):
        resp = self.c.get("/graphs/Xd1c_result", {"graph_country1" : "United Kingdom of Great Britain and Northern Ireland", "graph_indicator1" : "Refugees by country", "graph_indicator2" : "Agricultural land", "graph_indicator3" : "Mortality rate under 5, per 1.000 births", "graph_indicator4" : "", "graph_indicator5" : ""})
        self.assertEquals(resp.status_code, 200)

class HistogramTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_badindicator(self):
        resp = self.c.get("/graphs/hist_result", {"graph_indicator1": "aevñkunsv"})
        self.assertEquals(resp.status_code, 404)

    def test_ok(self):
        resp = self.c.get("/graphs/hist_result", {"graph_indicator1": "Population"})
        self.assertEquals(resp.status_code, 200)