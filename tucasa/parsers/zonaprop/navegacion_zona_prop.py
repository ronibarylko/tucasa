import logging
import warnings

import bs4
from selenium import webdriver


class NavegacionZonaProp:

    def __init__(self, url: str, local=False):
        self.logger = logging.getLogger(__name__)
        self.url = url
        self.id_esperado = 'BODY-LISTADO'
        self.response = self.parsear_html(self.response_url(local, url))

        if not self.es_mi_navegacion_esperada():
            warnings.warn(f"{url} no parece ser una búsqueda.", UserWarning)

    def response_url(self, local, url):
        return self._hacer_get_o_cargar_local(local, url)

    def parsear_html(self, respuesta):
        return bs4.BeautifulSoup(respuesta, 'html.parser')

    def _hacer_get_o_cargar_local(self, local, url):
        if not local:
            driver = webdriver.Chrome()
            driver.get(url)
            return driver.page_source
        self.logger.warning(("No están habilitadas todas las opciones"
                             "para búsquedas descargadas"))
        self.logger.debug(f"Cargando archivo {url}")
        return open(url).read()

    def es_mi_navegacion_esperada(self) -> bool:
        return self.response.body['id'].upper() == self.id_esperado
