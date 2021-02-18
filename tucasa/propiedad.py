class Propiedad:

    def __init__(self, ambientes, antiguedad, superficie_total, superficie_cubierta, banios, dormitorios, disposicion,
                 orientacion, estado, luminosidad, alquiler, expensas, direccion, ubicacion, descripcion,
                 caracteristicas):
        self._ambientes = ambientes
        self._antiguedad = antiguedad
        self._superficie_total = superficie_total
        self._superficie_cubierta = superficie_cubierta
        self._banios = banios
        self._dormitorios = dormitorios
        self._disposicion = disposicion
        self._orientacion = orientacion
        self._estado = estado
        self._luminosidad = luminosidad
        self._alquiler = alquiler
        self._expensas = expensas
        self._direccion = direccion
        self._ubicacion = ubicacion
        self._descripcion = descripcion
        self._caracteristicas = caracteristicas

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

    def disposicion(self) -> int:
        return self._disposicion

    def orientacion(self) -> int:
        return self._orientacion

    def estado(self) -> int:
        return self._estado

    def luminosidad(self) -> int:
        return self._luminosidad

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
