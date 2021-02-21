class Propiedad:

    def __init__(self, ambiente, stotal, scubierta, bano, dormitorio, alquiler, expensas, direccion,
                 ubicacion, descripcion, caracteristicas, diccionario, url, antiguedad=None):
        self._ambientes = ambiente
        self._antiguedad = antiguedad
        self._superficie_total = stotal
        self._superficie_cubierta = scubierta
        self._banios = bano
        self._dormitorios = dormitorio
        self._alquiler = alquiler
        self._expensas = expensas
        self._direccion = direccion
        self._ubicacion = ubicacion
        self._descripcion = descripcion
        self._caracteristicas = caracteristicas
        self._url = url
        self._diccionario = diccionario #TODORONI esto pa printear, puede cambiarse

    def diccionario(self):
        return self._diccionario

    def ambientes(self) -> int:
        return self._ambientes

    def antiguedad(self) -> int:
        return self._antiguedad

    def superficie_total(self) -> int:
        return self._superficie_total

    def superficie_cubierta(self) -> int:
        return self._superficie_cubierta

    def banios(self) -> int:
        return self._banios

    def dormitorios(self) -> int:
        return self._dormitorios

    def alquiler(self) -> int:
        return self._alquiler

    def expensas(self) -> int:
        return self._expensas

    def direccion(self) -> str:
        return self._direccion

    def ubicacion(self) -> str:
        return self._ubicacion

    def descripcion(self) -> str:
        return self._descripcion

    def contacto(self):
        # TODO: Extraer contacto (necesita cargar JS seguramente)
        raise NotImplementedError

    def caracteristicas(self) -> dict:
        return self._caracteristicas

    def ubicacion_mapa(self):
        # TODO: Extraer ubicación desde el mapa
        raise NotImplementedError
