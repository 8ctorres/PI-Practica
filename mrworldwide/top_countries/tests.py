from django.test import TestCase, Client
from top_countries.views import *

# Create your tests here.
class TopCountriesTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_badindicator(self):
        resp = self.c.post("/top/", {"indicator": "alicerucnalwksef", "top": "15"})
        self.assertEquals(resp.status_code, 404)

    def test_toomany(self):
        resp = self.c.post("/top/", {"indicator": "Percentage of unemployment", "top": "23541"})
        self.assertEquals(resp.status_code, 400)

    def test_ok(self):
        resp = self.c.post("/top/", {"indicator": "Percentage of unemployment", "top": "15"})
        self.assertEquals(resp.status_code, 200)
