import unittest
import os

from tucasa.parsers import zonaprop


url_departamento = ("https://www.zonaprop.com.ar/propiedades/sensacional-"
                    "vista-a-parque-rivadavia.-amoblado.-45628502.html")
url_listado = ("https://www.zonaprop.com.ar/departamentos-alquiler-"
               "belgrano-caballito-2-ambientes.html")

directorio = os.path.dirname(__file__)
descarga_departamento = os.path.join(directorio,
                                     "../resources/departamento.html")
descarga_departamento2 = os.path.join(directorio,
                                      "../resources/departamento2.html")
descarga_listado = os.path.join(directorio, "../resources/listado.html")


class TestZonaProp(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def atest_parser_propiedad_true(self):
    departamento = zonaprop.Propiedad(url_departamento)
    prop = departamento._es_propiedad
    self.assertTrue(prop)

  def atest_parser_propiedad_false(self):
    with self.assertWarns(UserWarning):
      propiedad = zonaprop.Propiedad(url_listado)
    prop = propiedad._es_propiedad
    self.assertFalse(prop)

  def test_parser_propiedad_local_true(self):
    departamento = zonaprop.Propiedad(descarga_departamento, True)
    prop = departamento._es_propiedad
    self.assertTrue(prop)

  def test_parser_propiedad_local_false(self):
    with self.assertWarns(UserWarning):
      propiedad = zonaprop.Propiedad(descarga_listado, True)
    prop = propiedad._es_propiedad
    self.assertFalse(prop)

  def test_ambientes_1(self):
    propiedad = zonaprop.Propiedad(descarga_departamento, True)
    ambientes = propiedad.ambientes
    self.assertEqual(ambientes, 4)

  def test_ambientes_2(self):
    propiedad = zonaprop.Propiedad(descarga_departamento2, True)
    ambientes = propiedad.ambientes
    self.assertEqual(ambientes, 2)

  def test_sup_cubierta_1(self):
    propiedad = zonaprop.Propiedad(descarga_departamento, True)
    sup_cubierta = propiedad.superficie_cubierta
    self.assertEqual(sup_cubierta, 138)

  def test_sup_cubierta_2(self):
    propiedad = zonaprop.Propiedad(descarga_departamento2, True)
    sup_cubierta = propiedad.superficie_cubierta
    self.assertEqual(sup_cubierta, 51)

  def test_sup_total_1(self):
    propiedad = zonaprop.Propiedad(descarga_departamento, True)
    sup_total = propiedad.superficie_total
    self.assertEqual(sup_total, 150)

  def test_sup_total_2(self):
    propiedad = zonaprop.Propiedad(descarga_departamento2, True)
    sup_total = propiedad.superficie_total
    self.assertEqual(sup_total, 54)

  def test_banios_1(self):
    propiedad = zonaprop.Propiedad(descarga_departamento, True)
    banios = propiedad.banios
    self.assertEqual(banios, 2)

  def test_banios_2(self):
    propiedad = zonaprop.Propiedad(descarga_departamento2, True)
    banios = propiedad.banios
    self.assertEqual(banios, 1)

  def test_dormitorios_1(self):
    propiedad = zonaprop.Propiedad(descarga_departamento, True)
    dormitorios = propiedad.dormitorios
    self.assertEqual(dormitorios, 3)

  def test_dormitorios_2(self):
    propiedad = zonaprop.Propiedad(descarga_departamento2, True)
    dormitorios = propiedad.dormitorios
    self.assertEqual(dormitorios, 1)

  def test_antiguedad_1(self):
    propiedad = zonaprop.Propiedad(descarga_departamento, True)
    antiguedad = propiedad.antiguedad
    self.assertEqual(antiguedad, 80)

  def test_antiguedad_2(self):
    propiedad = zonaprop.Propiedad(descarga_departamento2, True)
    antiguedad = propiedad.antiguedad
    self.assertEqual(antiguedad, 22)

  def test_disposicion_1(self):
    propiedad = zonaprop.Propiedad(descarga_departamento, True)
    disposicion = propiedad.disposicion
    self.assertEqual(disposicion, "Frente")

  def test_disposicion_2(self):
    propiedad = zonaprop.Propiedad(descarga_departamento2, True)
    disposicion = propiedad.disposicion
    self.assertEqual(disposicion, "Contrafrente")

  def test_orientacion_1(self):
    propiedad = zonaprop.Propiedad(descarga_departamento, True)
    orientacion = propiedad.orientacion
    self.assertEqual(orientacion, "O")

  def test_orientacion_2(self):
    propiedad = zonaprop.Propiedad(descarga_departamento2, True)
    orientacion = propiedad.orientacion
    self.assertEqual(orientacion, "NO")

  def test_estado_1(self):
    propiedad = zonaprop.Propiedad(descarga_departamento, True)
    estado = propiedad.estado
    self.assertEqual(estado, "Excelente")

  def test_estado_2(self):
    propiedad = zonaprop.Propiedad(descarga_departamento2, True)
    estado = propiedad.estado
    self.assertEqual(estado, "Excelente")

  def test_luminosidad_1(self):
    propiedad = zonaprop.Propiedad(descarga_departamento, True)
    luminosidad = propiedad.luminosidad
    self.assertEqual(luminosidad, "Muy luminoso")

  def test_luminosidad_2(self):
    propiedad = zonaprop.Propiedad(descarga_departamento2, True)
    luminosidad = propiedad.luminosidad
    self.assertEqual(luminosidad, "Muy luminoso")

  def test_alquiler_1(self):
    propiedad = zonaprop.Propiedad(descarga_departamento, True)
    alquiler = propiedad.alquiler
    self.assertEqual(alquiler, "USD 1.300")

  def test_alquiler_2(self):
    propiedad = zonaprop.Propiedad(descarga_departamento2, True)
    alquiler = propiedad.alquiler
    self.assertEqual(alquiler, "$ 26.000")

  def test_expensas_1(self):
    propiedad = zonaprop.Propiedad(descarga_departamento, True)
    expensas = propiedad.expensas
    self.assertEqual(expensas, "$ 6.400")

  def test_expensas_2(self):
    propiedad = zonaprop.Propiedad(descarga_departamento2, True)
    expensas = propiedad.expensas
    self.assertEqual(expensas, "$ 8.000")
