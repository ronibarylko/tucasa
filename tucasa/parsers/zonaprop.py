import bs4
import requests
import warnings


class Propiedad(object):
    """
    Parser de propiedades de ZonaProp
    """

    def __init__(self, url: str, local=False):
        if not local:
            response = requests.get(url).text
        else:
            response = open(url).read()
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

        self._procesar_valor_conocidas = {}
        self._procesar_valor_conocidas['Ambientes'] = lambda x: int(x)
        self._procesar_valor_conocidas['Baños'] = lambda x: int(x)
        self._procesar_valor_conocidas['Dormitorios'] = lambda x: int(x)
        self._procesar_valor_conocidas['Superficie total'] = quitar_m2
        self._procesar_valor_conocidas['Superficie cubierta'] = quitar_m2
        self._procesar_valor_conocidas['Antigüedad'] = antiguedad

        self._procesar_clave_conocidas = {}
        self._procesar_clave_conocidas['Baño'] = lambda x: x + "s"
        self._procesar_clave_conocidas['Ambiente'] = lambda x: x + "s"
        self._procesar_clave_conocidas['Dormitorio'] = lambda x: x + "s"

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
            clave = self._procesar_clave(clave)(clave)
            valor = self._procesar_valor(clave)(dato.b.text)
            _informacion[clave] = valor
        alquiler = self.soup.find('div', {'class': 'price-items'})
        _informacion["Alquiler"] = alquiler.span.text
        expensas = self.soup.find('div', {'class': 'block-expensas block-row'})
        _informacion["Expensas"] = expensas.span.text
        titulo = self.soup.find('h2', {'class': 'title-location'})
        direccion_limpia = ' '.join(titulo.b.text.split())
        sin_direccion = titulo.text.split(',')[1:]
        sin_espacios = [_.strip() for _ in sin_direccion]
        ubicacion = ', '.join(sin_espacios)
        _informacion["Direccion"] = direccion_limpia
        _informacion['Ubicacion'] = ubicacion
        descripcion = self.soup.find('div', {'id': 'verDatosDescripcion'})
        _informacion["Descripcion"] = descripcion.text
        caracteristicas = {}
        general_section = self.soup.findAll('section', {'class': 'general-section article-section'})
        for sec in general_section:
            clave = sec.div.text.strip()
            esta_lista = sec.findAll('li')
            estas_caracteristicas = tuple(_.text.strip() for _ in esta_lista)
            caracteristicas[clave] = estas_caracteristicas
        _informacion["Caracteristicas"] = caracteristicas
        return _informacion

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
        #TODO: Extraer contacto (necesita cargar JS seguramente)
        raise NotImplementedError

    @property
    def caracteristicas(self):
        return self.informacion["Caracteristicas"]

    def _procesar_valor(self, clave):
        try:
            funcion = self._procesar_valor_conocidas[clave]
        except KeyError:
            funcion = lambda x: x
        return funcion

    def _procesar_clave(self, clave):
        try:
            funcion = self._procesar_clave_conocidas[clave]
        except KeyError:
            funcion = lambda x: x
        return funcion
