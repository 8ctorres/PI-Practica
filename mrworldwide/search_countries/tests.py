from django.test import TestCase, Client
from search_countries.views import *

# Create your tests here.
class SearchCountriesTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_badname(self):
        resp = self.c.get("/search/", {"search_country" : "Asgard"})
        self.assertEquals(resp.status_code, 404)

    def test_badcode(self):
        resp = self.c.get("/search/", {"search_country": "ZZZ"})
        self.assertEquals(resp.status_code, 404)

    def test_ok(self):
        resp = self.c.get("/search/", {"search_country": "Nepal"})
        self.assertEquals(resp.status_code, 200)
