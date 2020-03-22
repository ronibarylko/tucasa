import os
import unittest

from tucasa.parsers import zonaprop

url_departamento = ("https://www.zonaprop.com.ar/propiedades/sensacional-"
                    "vista-a-parque-rivadavia.-amoblado.-45628502.html")
url_listado = ("https://www.zonaprop.com.ar/departamentos-alquiler-"
               "belgrano-caballito-2-ambientes.html")
url_listado2 = ("https://www.zonaprop.com.ar/departamentos-alquiler-palermo"
                "-2-ambientes-15000-20000-pesos.html")
directorio = os.path.dirname(__file__)
descarga_departamento = os.path.join(directorio,
                                     "../resources/departamento.html")
descarga_departamento2 = os.path.join(directorio,
                                      "../resources/departamento2.html")
descarga_departamento3 = os.path.join(directorio,
                                      "../resources/departamento3.html")
descarga_departamento4 = os.path.join(directorio,
                                      "../resources/departamento4.html")
descarga_listado = os.path.join(directorio, "../resources/listado.html")
descarga_listado2 = os.path.join(directorio, "../resources/listado2.html")


class TestPropiedad(unittest.TestCase):
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

    def test_antiguedad_3(self):
        propiedad = zonaprop.Propiedad(descarga_departamento3, True)
        antiguedad = propiedad.antiguedad
        self.assertEqual(antiguedad, 0)

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

    def test_expensas_4(self):
        propiedad = zonaprop.Propiedad(descarga_departamento4, True)
        expensas = propiedad.expensas
        self.assertIsNone(expensas)

    def test_direccion_1(self):
        propiedad = zonaprop.Propiedad(descarga_departamento, True)
        direccion = propiedad.direccion
        self.assertEqual(direccion, "Doblas al 100")

    def test_direccion_2(self):
        propiedad = zonaprop.Propiedad(descarga_departamento2, True)
        direccion = propiedad.direccion
        self.assertEqual(direccion, "Ciudad de la Paz")

    def test_direccion_3(self):
        propiedad = zonaprop.Propiedad(descarga_departamento3, True)
        direccion = propiedad.direccion
        self.assertEqual(direccion, "Teodoro Garcia al 2100")

    def test_ubicacion_1(self):
        propiedad = zonaprop.Propiedad(descarga_departamento, True)
        ubicacion = propiedad.ubicacion
        self.assertEqual(ubicacion, "Caballito, Capital Federal")

    def test_ubicacion_2(self):
        propiedad = zonaprop.Propiedad(descarga_departamento2, True)
        ubicacion = propiedad.ubicacion
        self.assertEqual(ubicacion, "Belgrano, Capital Federal")

    def test_ubicacion_3(self):
        propiedad = zonaprop.Propiedad(descarga_departamento3, True)
        ubicacion = propiedad.ubicacion
        self.assertEqual(ubicacion, "Belgrano, Capital Federal")

    def test_descripcion_1(self):
        propiedad = zonaprop.Propiedad(descarga_departamento, True)
        descripcion = propiedad.descripcion
        self.assertTrue(descripcion.startswith("Departamento de categoría con impresionante vista al Parque"))
        self.assertTrue(descripcion.endswith("Vivanco Negocios Inmobiliarios desde Sumaprop."))

    def test_descripcion_2(self):
        propiedad = zonaprop.Propiedad(descarga_departamento2, True)
        descripcion = propiedad.descripcion
        self.assertTrue(descripcion.startswith("54 metros cuadrados con balcón en edificio"))
        self.assertTrue(descripcion.endswith("EN EL EDIFICIO Cristina Ver datos 8444 ofic Ver datos"))

    def test_descripcion_3(self):
        propiedad = zonaprop.Propiedad(descarga_departamento3, True)
        descripcion = propiedad.descripcion
        self.assertTrue(descripcion.startswith("Hermoso piso en alquiler en pleno Belgrano"))
        self.assertTrue(descripcion.endswith("SEGUINOS EN FACEBOOK"))

    def test_contacto(self):
        propiedad = zonaprop.Propiedad(descarga_departamento, True)
        with self.assertRaises(NotImplementedError):
            propiedad.contacto()

    def test_caracteristicas_1(self):
        propiedad = zonaprop.Propiedad(descarga_departamento, True)
        caracteristicas = propiedad.caracteristicas
        self.assertIn("Características generales", caracteristicas.keys())
        self.assertIn("Servicios", caracteristicas.keys())
        self.assertIn("Ambientes", caracteristicas.keys())
        self.assertIn("Características", caracteristicas.keys())

    def test_caracteristicas_2(self):
        propiedad = zonaprop.Propiedad(descarga_departamento2, True)
        caracteristicas = propiedad.caracteristicas
        self.assertIn("Características generales", caracteristicas.keys())
        self.assertIn("Servicios", caracteristicas.keys())
        self.assertIn("Ambientes", caracteristicas.keys())
        self.assertNotIn("Características", caracteristicas.keys())

    def test_caracteristicas_3(self):
        propiedad = zonaprop.Propiedad(descarga_departamento3, True)
        caracteristicas = propiedad.caracteristicas
        self.assertIn("Características generales", caracteristicas.keys())
        self.assertIn("Servicios", caracteristicas.keys())
        self.assertIn("Ambientes", caracteristicas.keys())
        self.assertIn("Características", caracteristicas.keys())

    def test_ubicacion_mapa(self):
        propiedad = zonaprop.Propiedad(descarga_departamento, True)
        with self.assertRaises(NotImplementedError):
            propiedad.ubicacion_mapa()


class TestListado(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parser_listado_true(self):
        listado = zonaprop.Listado(url_listado)
        prop = listado._es_listado
        self.assertTrue(prop)

    def test_parser_listado_false(self):
        with self.assertWarns(UserWarning):
            listado = zonaprop.Listado(url_departamento)
        prop = listado._es_listado
        self.assertFalse(prop)

    def test_parser_listado_local_true(self):
        listado = zonaprop.Listado(descarga_listado, True)
        prop = listado._es_listado
        self.assertTrue(prop)

    def test_parser_listado_local_false(self):
        with self.assertWarns(UserWarning):
            listado = zonaprop.Listado(descarga_departamento, True)
        prop = listado._es_listado
        self.assertFalse(prop)

    def test_lista_propiedades(self):
        listado = zonaprop.Listado(descarga_listado, True)
        propiedades = listado._propiedades_div
        self.assertEqual(len(propiedades), 15)

    def test_lista_propiedades_2(self):
        listado = zonaprop.Listado(descarga_listado2, True)
        propiedades = listado._propiedades_div
        self.assertEqual(len(propiedades), 20)

    def test_propiedad_desde_div_1(self):
        listado = zonaprop.Listado(url_listado)
        propiedades = listado._propiedades_div
        listado._propiedad_desde_div(propiedades[0])

    def test_propiedad_desde_div_2(self):
        listado = zonaprop.Listado(url_listado2)
        propiedades = listado._propiedades_div
        listado._propiedad_desde_div(propiedades[0])

    def test_todas_propiedades_desde_div_1(self):
        listado = zonaprop.Listado(url_listado)
        propiedades = listado._propiedades_div
        for p in propiedades:
            listado._propiedad_desde_div(p)

    def test_todas_propiedades_desde_div_2(self):
        listado = zonaprop.Listado(url_listado2)
        propiedades = listado._propiedades_div
        for p in propiedades:
            listado._propiedad_desde_div(p)


class TestResultadoBusqueda(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_busqueda_true(self):
        busqueda = zonaprop.ResultadoBusqueda(url_listado)
        busq = busqueda._es_busqueda
        self.assertTrue(busq)

    def test_busqueda_true_2(self):
        busqueda = zonaprop.ResultadoBusqueda(url_listado2)
        busq = busqueda._es_busqueda
        self.assertTrue(busq)

    def test_busqueda_false(self):
        with self.assertWarns(UserWarning):
            busqueda = zonaprop.ResultadoBusqueda(url_departamento)
        busq = busqueda._es_busqueda
        self.assertFalse(busq)

    def test_busqueda_local_true(self):
        with self.assertWarns(UserWarning):
            busqueda = zonaprop.ResultadoBusqueda(descarga_listado, local=True)
        busq = busqueda._es_busqueda
        self.assertTrue(busq)

    def test_busqueda_local_false(self):
        with self.assertWarns(UserWarning):
            busqueda = zonaprop.ResultadoBusqueda(descarga_departamento, local=True)
        busq = busqueda._es_busqueda
        self.assertFalse(busq)

    def test_cantidad_de_resultados(self):
        with self.assertWarns(UserWarning):
            busqueda = zonaprop.ResultadoBusqueda(descarga_listado, local=True)
        self.assertEqual(busqueda.cantidad_de_resultados, 1412)

    def test_cantidad_de_resultados_2(self):
        with self.assertWarns(UserWarning):
            busqueda = zonaprop.ResultadoBusqueda(descarga_listado2, local=True)
        self.assertEqual(busqueda.cantidad_de_resultados, 121)

    def test_cantidad_de_paginas(self):
        with self.assertWarns(UserWarning):
            busqueda = zonaprop.ResultadoBusqueda(descarga_listado, local=True)
        self.assertEqual(busqueda.cantidad_de_paginas, 71)

    def test_cantidad_de_paginas_2(self):
        with self.assertWarns(UserWarning):
            busqueda = zonaprop.ResultadoBusqueda(descarga_listado2, local=True)
        self.assertEqual(busqueda.cantidad_de_paginas, 7)

    def test_devolver_listado_1(self):
        busqueda = zonaprop.ResultadoBusqueda(url_listado)
        url_pagina1 = busqueda.listado_pagina(1)
        correcto = ("https://www.zonaprop.com.ar/departamentos-alquiler-"
                    "belgrano-caballito-2-ambientes-pagina-1.html")
        self.assertEqual(url_pagina1, correcto)

    def test_devolver_todos(self):
        busqueda = zonaprop.ResultadoBusqueda(url_listado)
        correcto = ("https://www.zonaprop.com.ar/departamentos-alquiler-"
                    "belgrano-caballito-2-ambientes-pagina-{n}.html")
        for n in range(1, busqueda.cantidad_de_paginas + 1):
            url_pagina = busqueda.listado_pagina(n)
            self.assertEqual(correcto.format(n=n), url_pagina)
