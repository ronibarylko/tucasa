import logging

import click
import pandas as pd
from tqdm import tqdm

from tucasa.parsers.zonaprop import Propiedad, Listado, BusquedaInicial


@click.command()
@click.argument('url')
@click.option('-o', '--output-file', 'archivo_salida', default='resultados.csv', show_default=True)
def main(url, archivo_salida):
    respuesta_inicial = BusquedaInicial.buscar_en(url)

    resultados = respuesta_inicial.cantidad_de_resultados()
    paginas = respuesta_inicial.cantidad_de_paginas()
    print(f"Encontré {resultados} resultados en {paginas} páginas.")

    propiedades = obtener_propiedades(paginas, respuesta_inicial)

    guardar_en_archivo(archivo_salida, propiedades)


def obtener_propiedades(paginas, respuesta):
    propiedades = []

    for n in tqdm(range(1, paginas + 1), desc='Página'):
        url_pagina = respuesta.listado_pagina(n)
        logging.debug(f"Parseando página {url_pagina}")
        listado = Listado(url_pagina)
        for url in tqdm(listado.propiedades_url(), desc='Propiedad', leave=False):
            logging.debug(f"Parseando propiedad {url}")
            propiedad = Propiedad(url)
            propiedades.append(propiedad)

    return propiedades


def guardar_en_archivo(archivo_salida, propiedades):
    info = [p.informacion for p in propiedades]
    df = pd.DataFrame(info)
    df.to_csv(archivo_salida)


if __name__ == '__main__':
    main()
