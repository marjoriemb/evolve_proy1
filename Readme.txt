ANÁLISIS DE MOVILIDAD: VIAJES, FRANJAS HORARIAS Y GRUPOS DEMOGRÁFICOS

Este proyecto contiene el análisis y visualizaciones sobre patrones de movilidad urbana.
A partir de un dataset de viajes, se estudian relaciones entre estaciones, franjas horarias, sexo y grupos etarios,
generando gráficos y métricas que permiten comprender mejor el comportamiento de los usuarios.

Para la realización del mismo se tomaron los datos correspondientes al 2025, disponibles en la web
https://www.mibici.net/es/datos-abiertos/

El objetivo del mismo era dar respuestas a las siguientes interrogantes:
    1- Cuál es la relación entre la edad y el sexo en cuánto al uso de las bicicletas públicas
       de la cuidad de Guadalajara, MX

    2- Cuál es la duración del viaje promedio.

    3- Cuáles días de la semana se suele emplear más

    4- Cuáles son los trayectos más frecuentes

    5- En qué horario hay una mayor demanda del servicio.

CONTENIDO DEL PROYECTO

- data/
    original/
        Directorio en el que se deben colocar los archivos csv que se deben procesar

    cleared/
        Directorio en el que se colocará el archivo csv luego de realizarle la limpieza de los datos
        y ser preprocesado.

- output/
        Directorio en el que se generarán las imágenes que ayudarán a dar respuesta a las
        interrogantes planteadas

- src/
      analyzer/
        Módulo en el que se implementó la generación de las imágenes de apoyo

      preprocesador/
        Módulo en el que se implementó la limpieza y preprocesamiento de los datos

      main.py
        Archivo que contiene el programa principal

- requirements.txt
    Lista de dependencias necesarias para ejecutar el proyecto.

- README.txt
    Documento principal con instrucciones y contexto del proyecto.


OBJETIVOS DEL ANÁLISIS

- Identificar los pares de estaciones más utilizados mediante conteos no dirigidos (A–B = B–A).
- Visualizar conexiones mediante heatmaps optimizados.
- Analizar la distribución de viajes por franjas horarias de 3 horas.
- Comparar patrones según sexo y grupos etarios.
- Detectar horas punta y diferencias entre segmentos de la población.


PRINCIPALES ANÁLISIS INCLUIDOS

- Heatmap de conexiones entre estaciones:
  Agrupación no dirigida de pares A–B, filtrado por volumen mínimo y división en grupos.

- Top 10 pares de estaciones:
  Gráfico de barras con los pares más utilizados, barras en color azul uniforme.

- Análisis temporal por franjas de 3 horas:
  Extracción de hora desde Inicio_del_viaje y construcción de franjas 00–03, 03–06, ..., 21–24.

- Comparación por sexo:
  Distribución de viajes por franja y sexo, con leyenda personalizada.

- Comparación por grupos etarios:
  Partición utilizada: 0–17, 18–29, 30–44, 45–59, 60+.


LIMPIEZA DE LOS DATOS EN EL MÓDULO DE PREPROCESAMIENTO
* Se eliminaron las filas duplicadas
* Se eliminaron las filas con valores nulos
* Se eliminaron las entradas asociadas a los viajes de menos de 1 minuto
* Se eliminaron las entradas asociadas a los viajes cuyo origen o destino
  involucran estaciones que ya no se encuentran en servicio

Estadísticas de la limpieza de los datos
Viajes procesados: 4532032
Entradas duplicadas: 0
Filas con valores no válidos eliminadas: 41894
Filas con viajes marginal ( < 1 minuto) eliminadas: 116609
Filas eliminadas asociadas a estaciones que no están en servicio: 3386
Viajes obtenidos una vez realizado el preprocesamiento: 4370143

