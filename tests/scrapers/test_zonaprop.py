import unittest

from tucasa.parsers import ZonaProp


url_departamento = ("https://www.zonaprop.com.ar/propiedades/sensacional-"
                    "vista-a-parque-rivadavia.-amoblado.-45628502.html")
url_listado = ("https://www.zonaprop.com.ar/departamentos-alquiler-"
               "belgrano-caballito-2-ambientes.html")


class TestZonaProp(unittest.TestCase):
  def setUp(self):
    self.parser = ZonaProp()

  def tearDown(self):
    pass

  def test_parser_propiedad_true(self):
    prop = self.parser.es_propiedad(url_departamento)
    self.assertTrue(prop)

  def test_parser_propiedad_false(self):
    prop = self.parser.es_propiedad(url_listado)
    self.assertFalse(prop)
