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

  @property
  def _es_propiedad(self) -> bool:
    es_propiedad = self.soup.body['id'].upper() == 'PROPERTY'
    return es_propiedad
