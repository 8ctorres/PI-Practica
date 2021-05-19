import unittest
from django.test import TestCase

class WorldBankTest(TestCase):

    def setUp(self):
        self.alltopics = get_topics_list()


    # Test consistente en comprobar que los temas se sacan correctamente
    def get_topics_test(self):
        self.assertEquals(self.alltopics.loc['4'].topicName, "Education")
        self.assertEquals(self.alltopics.loc['11'].topicName, "Poverty")

    # Test consistente en sacar un identificador de la API, para luego poder
    # hacer consultas en base a ese indicador
    def get_indicator_test(self):
        education_indicators = get_indicators_from_topic("4")
        self.illiteracy_ind = education_indicators.loc["UIS.LP.AG15T99"]
        self.assertEquals(illiteracy_ind.topicName,
                          'Adult illiterate population, 15+ years, both sexes (number)')

    # Test consistente en sacar el dato concreto de un país en un año concreto,
    # de un indicador concreto. Usamos un dato antiguo porque suponemos que no va a cambiar
    def get_value_test(self):
        spain_illiteracy = get_indicator("esp", illiteracy_ind.name)
        self.assertEquals(spain_illiteracy.loc['2008'].value, 931368)
