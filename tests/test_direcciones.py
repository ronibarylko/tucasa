import os
import unittest

import pandas as pd

from tucasa import direcciones

directorio = os.path.dirname(__file__)
base_de_datos = os.path.join(directorio,
                             "resources/bd_distancias.csv")
base_de_datos_salida = os.path.join(directorio,
                                    "resources/bd_distancias_salida.csv")
base_de_datos_no_existe = os.path.join(directorio,
                                       "resources/bd_distancias_no.csv")


class TestDirecciones(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_construccion(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        self.assertListEqual(list(distancia.dataframe.columns),
                             ["Origen", "Destino", "Modo", "Horario", "Tiempo"])

    def test_construccion_falla(self) -> None:
        with self.assertRaises(FileNotFoundError):
            direcciones.Distancias(base_de_datos_no_existe)

    def test_distancias_no_existe(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        origen = "Gorriti 440"
        destino = "El Salvador 5218"
        modo = "walking"
        with self.assertRaises(IndexError):
            distancia.tiempo(origen, destino, modo, buscar=False)

    def test_distancias_existe(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        origen = "Gorriti 4300"
        destino = "El Salvador 5218"
        modo = "walking"
        tiempo = distancia.tiempo(origen, destino, modo, buscar=False)
        self.assertEqual(20, tiempo)

    def test_distancia_multimodo(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        origen = "Gorriti 4000"
        destino = "El Salvador 5218"
        modo = "*"
        with self.assertWarns(UserWarning):
            tiempo = distancia.tiempo(origen, destino, modo, buscar=False)
        self.assertEqual(15.5, tiempo)

    def test_distancia_repetido(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        origen = "Gorriti 4000"
        destino = "El Salvador 5218"
        modo = "walking"
        with self.assertWarns(UserWarning):
            tiempo = distancia.tiempo(origen, destino, modo, buscar=False)
        self.assertEqual(17.5, tiempo)

    def test_mascara_origen_1(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        mascara = distancia._mascara_direccion("Origen", "Gorriti 4000")
        correcto = [True, False, True, False, True, False, False, False, True]
        self.assertListEqual(correcto, list(mascara))

    def test_mascara_origen_2(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        mascara = distancia._mascara_direccion("Origen", "Gorriti 4300")
        correcto = [False, True, False, False, False, False, False, False, False]
        self.assertListEqual(correcto, list(mascara))

    def test_mascara_origen_3(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        mascara = distancia._mascara_direccion("Origen", "Gorriti 4200")
        correcto = [False, False, False, True, False, True, False, True, False]
        self.assertListEqual(correcto, list(mascara))

    def test_mascara_origen_4(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        mascara = distancia._mascara_direccion("Origen", "Gorriti 4032")
        correcto = [False, False, False, False, False, False, True, False, False]
        self.assertListEqual(correcto, list(mascara))

    def test_mascara_origen_5(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        mascara = distancia._mascara_direccion("Origen", "Gorraiti 4032")
        correcto = [False, False, False, False, False, False, False, False, False]
        self.assertListEqual(correcto, list(mascara))

    def test_mascara_destino_1(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        mascara = distancia._mascara_direccion("Destino", "El Salvador 5218")
        correcto = [True, True, True, True, True, True, True, False, True]
        self.assertListEqual(correcto, list(mascara))

    def test_mascara_destino_2(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        mascara = distancia._mascara_direccion("Destino", "Otro 5218")
        correcto = [False, False, False, False, False, False, False, True, False]
        self.assertListEqual(correcto, list(mascara))

    def test_mascara_destino_3(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        mascara = distancia._mascara_direccion("Destino", "Otro 5a218")
        correcto = [False, False, False, False, False, False, False, False, False]
        self.assertListEqual(correcto, list(mascara))

    def test_mascara_modo_1(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        mascara = distancia._mascara_modo("walking")
        correcto = [True, True, False, False, False, False, True, True, True]
        self.assertListEqual(correcto, list(mascara))

    def test_mascara_modo_2(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        mascara = distancia._mascara_modo("bicycling")
        correcto = [False, False, True, True, False, False, False, False, False]
        self.assertListEqual(correcto, list(mascara))

    def test_distancias_no_existe_busca(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        origen = "Gorriti 440"
        destino = "El Salvador 5218"
        modo = "walking"
        with self.assertRaises(ValueError):
            distancia.tiempo(origen, destino, modo, buscar=True)

    def test_agregar_distancia(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        origen = "desde"
        destino = "hasta"
        modo = "walking"
        tiempo = 10
        largo_inicial = len(distancia.dataframe)
        distancia._agregar(origen, destino, modo, tiempo)
        largo_final = len(distancia.dataframe)
        ultima_fila = distancia.dataframe.iloc[-1, :]
        self.assertEqual(ultima_fila["Origen"], origen)
        self.assertEqual(ultima_fila["Destino"], destino)
        self.assertEqual(ultima_fila["Modo"], modo)
        self.assertEqual(ultima_fila["Tiempo"], tiempo)
        self.assertEqual(1, largo_final - largo_inicial)

    def test_guardar_1(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        actual = distancia.dataframe
        distancia.guardar()
        guardado = pd.read_csv(base_de_datos)
        pd.testing.assert_frame_equal(actual, guardado)

    def test_guardar_2(self) -> None:
        distancia = direcciones.Distancias(base_de_datos)
        origen = "desde"
        destino = "hasta"
        modo = "walking"
        tiempo = 10
        distancia._agregar(origen, destino, modo, tiempo)
        actual = distancia.dataframe
        distancia.guardar(base_de_datos_salida)
        guardado = pd.read_csv(base_de_datos_salida)
        pd.testing.assert_frame_equal(actual, guardado)
