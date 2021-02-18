from typing import List

from tucasa.parsers.zonaprop.navegacion_zona_prop import NavegacionZonaProp


class RecorrerListado(NavegacionZonaProp):
    """
    Parser de listado de propiedades de ZonaProp
    """

    def _propiedades_div(self) -> list:
        # TODO: Manejar los emprendimientos. Los estamos ignorando.
        container = self.response.find('div', {'class': 'list-card-container'})
        prop = container.findAll('div', {'data-posting-type': 'PROPERTY'})
        return prop

    def propiedades_url(self) -> List[str]:
        lista_url = []
        for div in self._propiedades_div():
            url = 'http://www.zonaprop.com.ar' + div['data-to-posting']
            lista_url.append(url)
        return lista_url
