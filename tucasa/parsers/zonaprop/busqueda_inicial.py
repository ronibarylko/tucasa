import math

from tucasa.parsers.zonaprop.navegacion_zona_prop import NavegacionZonaProp

RESULTADOS_POR_PAGINA = 20


class BusquedaInicial(NavegacionZonaProp):

    @classmethod
    def buscar_en(cls, url):
        return cls(url)

    def cantidad_de_resultados(self) -> int:
        titulo = self.response.find('h1', {'class': 'list-result-title'})
        cantidad = titulo.text.split(" ")[0].replace('.', '')
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

    def cantidad_de_paginas(self) -> int:
        return math.ceil(self.cantidad_de_resultados() / RESULTADOS_POR_PAGINA)
