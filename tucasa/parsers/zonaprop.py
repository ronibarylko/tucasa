from collections import defaultdict
import math
import warnings
from typing import List
import logging

import bs4
import requests

RESULTADOS_POR_PAGINA = 20


class Propiedad(object):
    """
    Parser de propiedades de ZonaProp
    """

    def __init__(self, url: str, local: bool = False):
        self.logger = logging.getLogger(__name__)
        if not local:
            response = requests.get(url).text
        else:
            self.logger.debug(f"Cargando archivo {url}")
            response = open(url).read()
        self.url = url
        self.soup = bs4.BeautifulSoup(response, 'html.parser')
        if not self._es_propiedad:
            warnings.warn(f"{url} no parece ser una propiedad.", UserWarning)

        def quitar_m2(entrada: str) -> int:
            indice = entrada.find("m²")
            valor = entrada[:indice]
            valor = int(valor)
            return valor

        def antiguedad(entrada: str) -> int:
            if entrada == "A estrenar":
                anios = 0
            else:
                anios = int(entrada)
            return anios

        # Esto no parece muy lindo, porque es un lambda a la función identidad
        # que no existe como builtin.
        self._procesar_valor = defaultdict(lambda: lambda x: x)
        self._procesar_valor['Ambientes'] = lambda x: int(x)
        self._procesar_valor['Baños'] = lambda x: int(x)
        self._procesar_valor['Dormitorios'] = lambda x: int(x)
        self._procesar_valor['Superficie total'] = quitar_m2
        self._procesar_valor['Superficie cubierta'] = quitar_m2
        self._procesar_valor['Antigüedad'] = antiguedad

        self._procesar_clave = defaultdict(lambda: lambda x: x)
        self._procesar_clave['Baño'] = lambda x: x + "s"
        self._procesar_clave['Ambiente'] = lambda x: x + "s"
        self._procesar_clave['Dormitorio'] = lambda x: x + "s"

        self._informacion = {}

    @property
    def _es_propiedad(self) -> bool:
        es_propiedad = self.soup.body['id'].upper() == 'PROPERTY'
        return es_propiedad

    @property
    def informacion(self) -> dict:
        datos = self.soup.findAll('li', {'class': 'icon-feature'})
        _informacion = {}
        for dato in datos:
            clave = dato.span.text
            clave = self._procesar_clave[clave](clave)
            valor = self._procesar_valor[clave](dato.b.text)
            _informacion[clave] = valor
        alquiler = self._alquiler()
        _informacion["Alquiler"] = alquiler
        expensas = self._expensas()
        _informacion["Expensas"] = expensas
        titulo = self.soup.find('h2', {'class': 'title-location'})
        direccion_limpia = ' '.join(titulo.b.text.split())
        # Quitar la información del barrio que a veces viene duplicada
        direccion_limpia = direccion_limpia.split(',')[0]
        sin_direccion = titulo.text.split(',')[1:]
        sin_espacios = [_.strip() for _ in sin_direccion]
        ubicacion = ', '.join(sin_espacios)
        _informacion["URL"] = self.url
        _informacion["Direccion"] = direccion_limpia
        _informacion['Ubicacion'] = ubicacion
        descripcion = self.soup.find('div', {'id': 'verDatosDescripcion'})
        _informacion["Descripcion"] = descripcion.text
        caracteristicas = {}
        general_section = self.soup.findAll(
            'section',
            {'class': 'general-section article-section'})
        for sec in general_section:
            clave = sec.div.text.strip()
            esta_lista = sec.findAll('li')
            estas_caracteristicas = tuple(_.text.strip() for _ in esta_lista)
            caracteristicas[clave] = estas_caracteristicas
        _informacion["Caracteristicas"] = caracteristicas
        return _informacion

    def _expensas(self) -> int:
        expensas = self.soup.find('div', {'class': 'block-expensas block-row'})
        if expensas is not None:
            expensas = expensas.span.text
            if '$' in expensas:
                expensas = expensas.replace(".", "")
                expensas = expensas.replace("$", "")
                expensas = int(expensas)
        return expensas

    def _alquiler(self) -> int:
        precios = self.soup.findAll("div", {"class": "block-price block-row"})
        alquiler = None
        for p in precios:
            texto = p.find("div", {"class": "price-operation"}).text
            if texto.upper() == 'ALQUILER':
                alquiler = p.find('div', {'class': 'price-items'}).span.text
                # TODO: Analizar caso de múltiple moneda. Por ahora sólo
                # obtenemos los que están en $
                if "$" in alquiler:
                    alquiler = alquiler.replace("$", "")
                    alquiler = alquiler.replace(".", "")
                    alquiler = int(alquiler)
                else:
                    alquiler = None
        return alquiler

    # No me gusta mucho esto, pero no se me ocurre otra forma de acceso rápido.
    # ¿con casefold? Tampoco quiero heredar de `dict`
    @property
    def ambientes(self) -> int:
        return self.informacion["Ambientes"]

    @property
    def antiguedad(self) -> int:
        return self.informacion["Antigüedad"]

    @property
    def superficie_total(self) -> int:
        return self.informacion["Superficie total"]

    @property
    def superficie_cubierta(self) -> int:
        return self.informacion["Superficie cubierta"]

    @property
    def banios(self) -> int:
        return self.informacion["Baños"]

    @property
    def dormitorios(self) -> int:
        return self.informacion["Dormitorios"]

    @property
    def disposicion(self) -> int:
        return self.informacion["Disposición"]

    @property
    def orientacion(self) -> int:
        return self.informacion["Orientación"]

    @property
    def estado(self) -> int:
        return self.informacion["Estado del inmueble"]

    @property
    def luminosidad(self) -> int:
        return self.informacion["Luminosidad"]

    @property
    def alquiler(self) -> int:
        return self.informacion["Alquiler"]

    @property
    def expensas(self) -> int:
        return self.informacion["Expensas"]

    @property
    def direccion(self) -> str:
        return self.informacion["Direccion"]

    @property
    def ubicacion(self) -> str:
        return self.informacion["Ubicacion"]

    @property
    def descripcion(self) -> str:
        return self.informacion["Descripcion"]

    @property
    def contacto(self):
        # TODO: Extraer contacto (necesita cargar JS seguramente)
        raise NotImplementedError

    @property
    def caracteristicas(self) -> dict:
        return self.informacion["Caracteristicas"]

    @property
    def ubicacion_mapa(self):
        # TODO: Extraer ubicación desde el mapa
        raise NotImplementedError


class Listado(object):
    """
    Parser de listado de propiedades de ZonaProp
    """

    def __init__(self, url: str, local=False):
        self.logger = logging.getLogger(__name__)
        if not local:
            response = requests.get(url).text
        else:
            self.logger.debug(f"Cargando archivo {url}")
            response = open(url).read()
        self.soup = bs4.BeautifulSoup(response, 'html.parser')
        if not self._es_listado:
            warnings.warn(f"{url} no parece ser un listado.", UserWarning)

    @property
    def _es_listado(self) -> bool:
        es_listado = self.soup.body['id'].upper() == 'BODY-LISTADO'
        return es_listado

    @property
    def _propiedades_div(self) -> list:
        # TODO: Manejar los emprendimientos. Los estamos ignorando.
        container = self.soup.find('div', {'class': 'list-card-container'})
        prop = container.findAll('div', {'data-posting-type': 'PROPERTY'})
        return prop

    @property
    def propiedades_url(self) -> List[str]:
        lista_url = []
        for div in self._propiedades_div:
            url = 'http://www.zonaprop.com.ar' + div['data-to-posting']
            lista_url.append(url)
        return lista_url


class ResultadoBusqueda(object):
    def __init__(self, url: str, local=False):
        self.logger = logging.getLogger(__name__)
        self.url = url
        if not local:
            response = requests.get(url).text
        else:
            self.logger.warning(("No están habilitadas todas las opciones"
                                 "para búsquedas descargadas"))
            self.logger.debug(f"Cargando archivo {url}")
            response = open(url).read()
        self.soup = bs4.BeautifulSoup(response, 'html.parser')
        if not self._es_busqueda:
            warnings.warn(f"{url} no parece ser una búsqueda.", UserWarning)

    @property
    def _es_busqueda(self):
        #TODORONI no puedo obtener "id" de body
        return True
        #es_busqueda = self.soup.body['id'].upper() == 'BODY-LISTADO'
        #return es_busqueda

    @property
    def cantidad_de_resultados(self) -> int:
        titulo = self.soup.find('h1', {'class': 'list-result-title'})
        cantidad = titulo.b.text.replace('.', '')
        cantidad = int(cantidad)
        return cantidad

    # TODO: Pythonizar este código: claramente tiene que ser un iterable
    # (ver uso en `obtener_departamentos.py`)
    def listado_pagina(self, n: int) -> str:
        """
        A partir de la url de la búsqueda, genera el listado de la página `n`.
        """
        url_pagina = self.url.replace('.html', f'-pagina-{n}.html')
        return url_pagina

    @property
    def cantidad_de_paginas(self) -> int:
        numero_de_paginas = math.ceil(self.cantidad_de_resultados / RESULTADOS_POR_PAGINA)
        return numero_de_paginas
