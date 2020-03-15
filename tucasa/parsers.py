import bs4
import requests

class ZonaProp(object):
  """
  Parser para la información que surge de ZonaProp
  """
  def __init__(self):
    pass

  def es_propiedad(self, url: str) -> bool:
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    es_propiedad = soup.body['id'].upper() == 'PROPERTY'
    return es_propiedad
