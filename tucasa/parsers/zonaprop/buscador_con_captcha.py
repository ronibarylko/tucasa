from selenium import webdriver

from tucasa.parsers.zonaprop import BusquedaInicial


class BuscadorConCaptcha(BusquedaInicial):

    def response_url(self, local, url):
        driver = webdriver.Chrome()
        driver.get(url)
        return driver.page_source

    def cantidad_de_resultados(self) -> int:
        titulo = self.response.find('h1', {'class': 'list-result-title'})
        cantidad = titulo.text.split(" ")[0].replace('.', '')
        cantidad = int(cantidad)
        return cantidad

