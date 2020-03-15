import unittest

from tucasa.parsers import zonaprop


url_departamento = ("https://www.zonaprop.com.ar/propiedades/sensacional-"
                    "vista-a-parque-rivadavia.-amoblado.-45628502.html")
url_listado = ("https://www.zonaprop.com.ar/departamentos-alquiler-"
               "belgrano-caballito-2-ambientes.html")


class TestZonaProp(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_parser_propiedad_true(self):
    departamento = zonaprop.Propiedad(url_departamento)
    prop = departamento._es_propiedad
    self.assertTrue(prop)

  def test_parser_propiedad_false(self):
    with self.assertWarns(UserWarning):
      propiedad = zonaprop.Propiedad(url_listado)
    prop = propiedad._es_propiedad
    self.assertFalse(prop)
