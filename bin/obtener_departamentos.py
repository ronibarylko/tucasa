import logging
from concurrent.futures.thread import ThreadPoolExecutor

import click
import pandas as pd
from tqdm import tqdm

from tucasa.parsers.zonaprop import RecorrerListado, BusquedaInicial, ObtenerPropiedad


@click.command()
@click.argument('url')
@click.option('-o', '--output-file', 'archivo_salida', default='resultados.csv', show_default=True)
def main(url, archivo_salida):
    respuesta_inicial = BusquedaInicial.buscar_en(url)

    resultados = respuesta_inicial.cantidad_de_resultados()
    paginas = respuesta_inicial.cantidad_de_paginas()
    print(f"Encontré {resultados} resultados en {paginas} páginas.")

    propiedades_as_dict = [vars(p) for p in obtener_propiedades(paginas, respuesta_inicial)]
    df = pd.DataFrame(propiedades_as_dict)
    df.to_csv(archivo_salida, index=False)


class ObtenerPropiedadesConcurrentes:

    def __init__(self, listado):
        self._listado = listado
        self._thread_pool = ThreadPoolExecutor(max_workers=20)

    def procesar(self):
        def obtener_propiedad(_url):
            try:
                return ObtenerPropiedad(_url).propiedad()
            except Exception as e:
                print("No pude hacerlo con {} por {} \n".format(url, e))

        futures_props = []
        for url in tqdm(self._listado.propiedades_url(), desc='Propiedad', leave=False):
            logging.debug(f"Parseando propiedad {url}")
            futures_props.append(self._thread_pool.submit(obtener_propiedad, url))
        return [fut.result() for fut in futures_props if fut.result()]


def obtener_propiedades(paginas, respuesta):
    propiedades = []
    for n in tqdm(range(1, paginas + 1), desc='Página'):
        url_pagina = respuesta.listado_pagina(n)
        logging.debug(f"Parseando página {url_pagina}")
        listado = RecorrerListado(url_pagina)
        propiedades = propiedades + ObtenerPropiedadesConcurrentes(listado).procesar()

    return propiedades


if __name__ == '__main__':
    main()
