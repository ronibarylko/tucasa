import logging

import click
import pandas as pd
from tqdm import tqdm

from tucasa.parsers import zonaprop


@click.command()
@click.argument('url')
@click.option('-o', '--output-file', 'archivo_salida',
              default='resultados.csv', show_default=True)
def main(url, archivo_salida):
    busqueda = zonaprop.ResultadoBusqueda(url)
    resultados = busqueda.cantidad_de_resultados
    paginas = busqueda.cantidad_de_paginas
    print(f"Encontré {resultados} resultados en {paginas} páginas.")
    propiedades = []
    for n in tqdm(range(1, paginas + 1), desc='Página'):
        url_pagina = busqueda.listado_pagina(n)
        logging.debug(f"Parseando página {url_pagina}")
        listado = zonaprop.Listado(url_pagina)
        for url in tqdm(listado.propiedades_url, desc='Propiedad',
                        leave=False):
            logging.debug(f"Parseando propiedad {url}")
            propiedad = zonaprop.Propiedad(url)
            propiedades.append(propiedad)
    info = []
    for i, p in enumerate(propiedades):
        info.append(p.informacion)
    df = pd.DataFrame(info)
    df.to_csv(archivo_salida)


if __name__ == '__main__':
    main()
