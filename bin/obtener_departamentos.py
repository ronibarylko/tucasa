import logging

import click
import pandas as pd
from tqdm import tqdm

from tucasa.obtener_propiedades_concurrente import ObtenerPropiedadesConcurrente
from tucasa.parsers.zonaprop import RecorrerListado, BusquedaInicial


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


def obtener_propiedades(paginas, respuesta):
    propiedades = []
    for n in tqdm(range(1, paginas + 1), desc='Página'):
        url_pagina = respuesta.listado_pagina(n)
        logging.debug(f"Parseando página {url_pagina}")
        listado = RecorrerListado(url_pagina)
        propiedades = propiedades + ObtenerPropiedadesConcurrente(listado).obtener()

    return propiedades


if __name__ == '__main__':
    main()
