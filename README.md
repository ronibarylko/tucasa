# Crawler de Departamentos

Esta herramienta es, en realidad, de uso personal para simplificarme la búsqueda de departamentos. Una vez que uno hace la búsqueda con los criterios que quiere en una buscador (en este caso, zonaprop) aparecen UN MONTÓN de links, difíciles de seguir, de recopilar, etcétera. El propósito es simplificar esa iinformación y su análisis.

## Obtener información

Obtener departamentos de acuerdo a ciertos criterios (barrios, ambientes, etcétera) con la interfaz de páginas web (por ahora sólo zonaprop) y guardarlos en bases de datos locales.

Por ahora la búsqueda se hace en zonaprop para obtener el link. En la carpeta `bin` se encuentra el archivo `obtener_departamentos.py`, que se ejecuta con una dirección de búsqueda de zonaprop y guarda toda la información en un `.csv`, por ejemplo:

```
$ python obtener_departamentos.py https://www.zonaprop.com.ar/departamentos-alquiler-palermo-belgrano-recoleta-caballito-almagro-colegiales-villa-crespo-3-ambientes-publicado-hace-menos-de-45-dias-menos-30000-pesos.html
```

(la dirección de búsqueda es la que crea zonaprop con los filtros de la interfaz web).

## Análisis

Lo más importante, al menos para mí, es analizar el tiempo que me iba a llevar trasladarme a mi lugar de trabajo. Así que también hay un buscador de Google Maps que dice el tiempo de viaje, en varios medios de transporte, desde la dirección de cada departamento a una serie de destinos de interés. Además, guarda esos resultados en un csv local, para no hacer demasiadas consultas a la API de google.

En este repositorio hay un ejemplo que pone todas las distancias entre los destinos ficticios de interés en `bin/data/destinos.csv` y los departamentos que salieron de la búsqueda anterior, `bin/data/resultados.csv`. Si ejecutan el script `direcciones.py` en la carpeta `bin/`:

```
$ python direcciones.py
```

va a crear el archivo `data/resultados_con_distancias.csv` que recopila esa información. La búsqueda de direcciones está en la base de datos local; para hacer búsquedas distintas hay que usar una API key de Google Maps personal.

Una vez que están esos datos, con distancias incluidas, se pueden agregar funciones de costo (por ejemplo, ¿cuánto vale estar 5 minutos más cerca del trabajo con un medio de transporte que usan sólo 2 veces por semana?) para normalizar toda la información y encontrar LA FUNCIÓN DE COSTO IDEAL PARA EL DEPARTAMENTO IDEAL. OK, quizás exagero; pero seguramente ayude a filtrar, de los 100 y pico de departamentos que aparecen, los 10/15 más importantes para cada une.
