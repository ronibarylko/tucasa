import logging

import pandas as pd

from tucasa import direcciones


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
propiedades = pd.read_csv("data/resultados.csv", index_col=0)
destinos = pd.read_csv("data/destinos.csv", index_col=0)
distancias = direcciones.Distancias("data/bd_distancias.csv")
for etiqueta in destinos["Etiqueta"]:
    propiedades[etiqueta] = 0
for i, origen in enumerate(propiedades["Direccion"]):
    for viaje in destinos.iterrows():
        destino = viaje[1]["Destino"]
        modo = viaje[1]["Modo"]
        etiqueta = viaje[1]["Etiqueta"]
        tiempo = distancias.tiempo(origen, destino, modo)
        logger.info((f"Modo: {modo}, Origen: {origen}, Destino: {destino}"
                     f", Etiqueta: {etiqueta}"))
        propiedades[etiqueta].iloc[i] = tiempo
# Actualizar las distancias con las nuevas calculadas
distancias.guardar("data/bd_distancias.csv")
propiedades.to_csv("data/resultados_con_distancias.csv")
