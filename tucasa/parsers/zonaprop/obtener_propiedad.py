import re

from tucasa.parsers.zonaprop.navegacion_zona_prop import NavegacionZonaProp
from tucasa.propiedad import Propiedad


class ObtenerPropiedad(NavegacionZonaProp):
    """
    Parser de propiedades de ZonaProp
    """

    def __init__(self, url: str, local: bool = False):
        super().__init__(url, local)

        self._procesar_valor = {'ambiente': lambda x: int(x[:x.find("Ambientes")]),
                                'bano': lambda x: int(x[:x.find("Baño")]),
                                'dormitorio': lambda x: int(x[:x.find("Dormitorio")]),
                                'stotal': lambda x: int(x[:x.find("m²")]),
                                'scubierta': lambda x: int(x[:x.find("m²")]),
                                'antiguedad': lambda x: 0 if "A estrenar" in x else int(x[:x.find("Antigüedad")])}

        self._propiedad = self._crear_propiedad()

    def es_mi_navegacion_esperada(self) -> bool:
        return self.response.body['id'].upper() == 'PROPERTY'

    def propiedad(self):
        return self._propiedad

    def _crear_propiedad(self):
        titulo = self.response.find('h2', {'class': 'title-location'})
        _informacion = {"alquiler": self._alquiler(),
                        "expensas": self._expensas(),
                        "url": self.url,
                        "direccion": self._direccion(titulo),
                        "ubicacion": self._ubicacion(titulo),
                        "descripcion": self._descripcion()
                        }

        datos = self.response.findAll('li', {'class': 'icon-feature'})
        for dato in datos:
            clave = self._dato2clave(dato)
            if clave in self._procesar_valor:
                _informacion[self._dato2clave(dato)] = self._procesar_valor[self._dato2clave(dato)](dato.text)

        _informacion["caracteristicas"] = self._caracteristicas()

        if self._es_departamento(_informacion):
            _informacion["scubierta"] = _informacion["stotal"]

        return Propiedad(**_informacion)

    def _es_departamento(self, _informacion):
        return not _informacion.get("scubierta")

    def _dato2clave(self, dato):
        return dato.find("i").attrs["class"][0].split("icon-")[1]

    def _caracteristicas(self):
        caracteristicas = {}
        general_section = self.response.findAll(
            'section',
            {'class': 'general-section article-section'})
        for sec in general_section:
            clave = sec.div.text.strip()
            estas_caracteristicas = tuple(w.text.strip() for w in (sec.findAll('li')))
            caracteristicas[clave] = estas_caracteristicas
        return caracteristicas

    def _descripcion(self):
        return self.response.find('div', {'id': 'reactDescription'}).text

    def _ubicacion(self, titulo):
        return ', '.join([w.strip() for w in (titulo.text.split(',')[1:])])

    def _direccion(self, titulo):
        return ' '.join(titulo.text.split()).split(',')[0]

    def _expensas(self) -> int:
        expensas = self.response.find('div', {'class': 'block-expensas block-row'})
        if expensas is not None:
            expensas = expensas.span.text
            if '$' in expensas:
                expensas = expensas.replace(".", "")
                expensas = expensas.replace("$", "")
                expensas = int(expensas)
        return expensas

    def _alquiler(self) -> int:
        precios = self.response.findAll("div", {"class": "block-price block-row"})
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
