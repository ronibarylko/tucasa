import logging
from concurrent.futures.thread import ThreadPoolExecutor
from tqdm import tqdm
from tucasa.parsers.zonaprop import ObtenerPropiedad


class ObtenerPropiedadesConcurrente:

    def __init__(self, listado):
        self._listado_propiedades = listado.propiedades_url()
        self._thread_pool = ThreadPoolExecutor(max_workers=len(self._listado_propiedades))

    def obtener(self):
        def obtener_propiedad(_url):
            try:
                return ObtenerPropiedad(_url).propiedad()
            except Exception as e:
                print("No pude hacerlo con {} por {} \n".format(url, e))

        futures_props = []
        for url in tqdm(self._listado_propiedades, desc='Propiedad', leave=False):
            logging.debug(f"Parseando propiedad {url}")
            futures_props.append(self._thread_pool.submit(obtener_propiedad, url))
        return [fut.result() for fut in futures_props if fut.result()]
