import math
import warnings

import googlemaps
import pandas as pd


class Distancias(object):
    def __init__(self, archivo: str, key: str = ""):
        self.dataframe = pd.read_csv(archivo)
        self.archivo = archivo
        self.key = key
        try:
            self.gmaps = googlemaps.Client(key=key)
        except ValueError:
            self.gmaps = None

    def tiempo(self, origen: str, destino: str, modo: str = "*",
               buscar=True) -> float:
        origen = self._normalizar_direccion(origen)
        destino = self._normalizar_direccion(destino)
        mascara_origen = self._mascara_direccion("Origen", origen)
        mascara_destino = self._mascara_direccion("Destino", destino)
        mascara_modo = self._mascara_modo(modo)
        mascara = mascara_origen & mascara_destino & mascara_modo
        resultado = self.dataframe[mascara]["Tiempo"]
        if len(resultado) == 0:
            if buscar:
                if self.gmaps is None:
                    self.gmaps = googlemaps.Client(key=self.key)
                tiempo = self._buscar(origen, destino, modo)
                self._agregar(origen, destino, modo, tiempo)
                return tiempo
            else:
                msg = (f"No encontré el viaje desde {origen} hasta {destino} "
                       f"con modo {modo} en mi base de datos")
                raise IndexError(msg)
        elif len(resultado) == 1:
            return resultado.item()
        else:
            msg = (f"Hay {len(resultado)} entradas para el viaje desde "
                   f"{origen} hasta {destino} con modo {modo}. Promediando.")
            warnings.warn(msg, UserWarning)
            return resultado.mean()

    def _mascara_direccion(self, columna, direccion):
        mascara = self.dataframe[columna] == direccion
        return mascara

    def _mascara_modo(self, modo):
        if modo == '*':
            mascara = pd.Series([True] * len(self.dataframe))
        else:
            mascara = self.dataframe["Modo"] == modo
        return mascara

    def _buscar(self, origen, destino, modo):
        ciudad = ", Buenos Aires, Argentina"
        origen_completo = origen + ciudad
        destino_completo = destino + ciudad
        # TODO: Este hack es medio bobo para la fecha.
        recorrido = self.gmaps.directions(origen_completo, destino_completo,
                                          modo, departure_time=pd.Timestamp("2020-06-03 09:22"))
        return math.ceil(recorrido[0]['legs'][0]['duration']['value'] / 60)

    def _agregar(self, origen, destino, modo, tiempo):
        para_agregar = {"Origen": origen, "Destino": destino, "Modo": modo,
                        "Tiempo": tiempo}
        self.dataframe = self.dataframe.append(para_agregar,
                                               ignore_index=True)

    def guardar(self, archivo_salida=None):
        if archivo_salida is None:
            archivo_salida = self.archivo
        self.dataframe.to_csv(archivo_salida, index=False)

    @staticmethod
    def _normalizar_direccion(direccion):
        direccion = Distancias._normalizar_conector(direccion)
        direccion = Distancias._normalizar_altura(direccion)
        return direccion

    @staticmethod
    def _normalizar_altura(direccion):
        # Redondear altura (si existe)
        direccion = direccion.split(" ")
        altura = direccion[-1]
        try:
            print(altura)
            print(int(altura))
            altura = int(altura)
            altura = altura // 100 * 100 + 1
            direccion[-1] = str(altura)
        except ValueError:
            pass
        direccion = " ".join(direccion)
        return direccion

    @staticmethod
    def _normalizar_conector(direccion):
        # Remover ' al ' de la altura
        direccion = direccion.replace(" al ", " ")
        return direccion
