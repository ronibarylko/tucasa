from collections import defaultdict

from tucasa.parsers.zonaprop.navegacion_zona_prop import NavegacionZonaProp


class Propiedad(NavegacionZonaProp):
    """
    Parser de propiedades de ZonaProp
    """

    def __init__(self, url: str, local: bool = False):
        super().__init__(url, local)
        self.id_esperado = 'PROPERTY'

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

    def es_mi_navegacion_esperada(self) -> bool:
        return self.response.body['id'].upper() == 'PROPERTY'

    @property
    def informacion(self) -> dict:
        datos = self.response.findAll('li', {'class': 'icon-feature'})
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
        titulo = self.response.find('h2', {'class': 'title-location'})
        direccion_limpia = ' '.join(titulo.b.text.split())
        # Quitar la información del barrio que a veces viene duplicada
        direccion_limpia = direccion_limpia.split(',')[0]
        sin_direccion = titulo.text.split(',')[1:]
        sin_espacios = [_.strip() for _ in sin_direccion]
        ubicacion = ', '.join(sin_espacios)
        _informacion["URL"] = self.url
        _informacion["Direccion"] = direccion_limpia
        _informacion['Ubicacion'] = ubicacion
        descripcion = self.response.find('div', {'id': 'verDatosDescripcion'})
        _informacion["Descripcion"] = descripcion.text
        caracteristicas = {}
        general_section = self.response.findAll(
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
