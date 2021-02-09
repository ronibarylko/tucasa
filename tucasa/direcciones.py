import math
import logging

import googlemaps
import pandas as pd


class Distancias(object):

    def __init__(self, archivo: str, key: str = ""):
        self.logger = logging.getLogger(__name__)
        try:
            self.dataframe = pd.read_csv(archivo)
        except FileNotFoundError:
            columnas = ["Origen", "Destino", "Modo", "Horario", "Tiempo"]
            self.dataframe = pd.DataFrame(columns=columnas)
        self.archivo = archivo
        self.key = key
        try:
            self.gmaps = googlemaps.Client(key=key)
        except ValueError:
            self.gmaps = None

    def tiempo(self, origen: str, destino: str, modo: str = "*",
               buscar=True) -> float:
        self.logger.debug(f"Viaje {origen} -> {destino} con modo {modo}")
        origen = self._normalizar_direccion(origen)
        destino = self._normalizar_direccion(destino)
        mascara_origen = self._mascara_direccion("Origen", origen)
        mascara_destino = self._mascara_direccion("Destino", destino)
        mascara_modo = self._mascara_modo(modo)
        mascara = mascara_origen & mascara_destino & mascara_modo
        resultado = self.dataframe[mascara]["Tiempo"]
        if len(resultado) == 0:
            self.logger.debug(f"No encontrado. Buscando en internet")
            if buscar:
                if self.gmaps is None:
                    self.gmaps = googlemaps.Client(key=self.key)
                tiempo = self._buscar(origen, destino, modo)
                self._agregar(origen, destino, modo, tiempo)
                return tiempo
            else:
                msg = (f"No encontré el viaje desde {origen} hasta {destino} "
                       f"con modo {modo} en mi base de datos y `buscar` no"
                       f"está habilitado")
                raise IndexError(msg)
        elif len(resultado) == 1:
            self.logger.debug(f"Encontrado en base de datos local")
            return resultado.item()
        else:
            msg = (f"Viaje {origen} -> {destino} con modo {modo} "
                   f"tiene {len(resultado)} entradas. Promediando.")
            self.logger.warning(msg)
            return resultado.mean()

    def _mascara_direccion(self, columna: str, direccion: str) -> pd.Series:
        # TODO: Hacer una búsqueda `casefold`
        mascara = self.dataframe[columna] == direccion
        return mascara

    def _mascara_modo(self, modo: str) -> pd.Series:
        if modo == '*':
            mascara = pd.Series([True] * len(self.dataframe))
        else:
            mascara = self.dataframe["Modo"] == modo
        return mascara

    def _buscar(self, origen: str, destino: str, modo: str) -> int:
        ciudad = ", Buenos Aires, Argentina"
        origen_completo = origen + ciudad
        destino_completo = destino + ciudad
        # TODO: Este hack es medio bobo para la fecha.
        recorrido = self.gmaps.directions(origen_completo, destino_completo,
                                          modo, departure_time=pd.Timestamp("2020-06-03 09:22"))
        return math.ceil(recorrido[0]['legs'][0]['duration']['value'] / 60)

    def _agregar(self, origen: str, destino: str, modo: str, tiempo: int) -> None:
        para_agregar = {"Origen": origen, "Destino": destino, "Modo": modo,
                        "Tiempo": tiempo}
        self.dataframe = self.dataframe.append(para_agregar,
                                               ignore_index=True)

    def guardar(self, archivo_salida: str = None) -> None:
        if archivo_salida is None:
            archivo_salida = self.archivo
        self.dataframe.to_csv(archivo_salida, index=False)

    def _normalizar_direccion(self, direccion: str) -> str:
        # TODO: Guardar las direcciones con mayúsculas en la primera letra
        direccion_nueva = self._normalizar_conector(direccion)
        direccion_nueva = self._normalizar_altura(direccion_nueva)
        self.logger.debug(f"Normalizando {direccion} -> {direccion_nueva}")
        return direccion_nueva

    @staticmethod
    def _normalizar_altura(direccion: str) -> str:
        # Redondear altura (si existe)
        direccion = direccion.split(" ")
        altura = direccion[-1]
        try:
            altura = int(altura)
            altura = altura // 100 * 100 + 1
            direccion[-1] = str(altura)
        except ValueError:
            pass
        direccion = " ".join(direccion)
        return direccion

    @staticmethod
    def _normalizar_conector(direccion: str) -> str:
        # Remover ' al ' de la altura
        direccion = direccion.replace(" al ", " ")
        return direccion
