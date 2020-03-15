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

    self._procesar_valor_conocidas = {}
    self._procesar_valor_conocidas['Ambientes'] = lambda x: int(x)
    self._procesar_valor_conocidas['Baños'] = lambda x: int(x)
    self._procesar_valor_conocidas['Superficie total'] = quitar_m2
    self._procesar_valor_conocidas['Superficie cubierta'] = quitar_m2

    self._procesar_clave_conocidas = {}
    self._procesar_clave_conocidas['Baño'] = lambda x: x + "s"
    self._procesar_clave_conocidas['Ambiente'] = lambda x: x + "s"


    self._informacion = {}

  @property
  def _es_propiedad(self) -> bool:
    es_propiedad = self.soup.body['id'].upper() == 'PROPERTY'
    return es_propiedad

  @property
  def informacion(self) -> bool:
    datos = self.soup.findAll('li', {'class': 'icon-feature'})
    _informacion = {}
    for dato in datos:
      clave = dato.span.text
      clave = self._procesar_clave(clave)(clave)
      valor = self._procesar_valor(clave)(dato.b.text)
      _informacion[clave] = valor
    return _informacion

  @property
  def ambientes(self) -> int:
    return self.informacion["Ambientes"]

  @property
  def superficie_total(self) -> int:
    return self.informacion["Superficie total"]

  @property
  def superficie_cubierta(self) -> int:
    return self.informacion["Superficie cubierta"]

  @property
  def banios(self) -> int:
    return self.informacion["Baños"]

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
