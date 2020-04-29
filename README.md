# IDRiD
Análisis de lesiones causadas por retinopatía diabética.


La retinopatía diabética (RD) es la complicación microvascular más común (50%) que puede presentarse en todos los tipos de diabetes mellitus (DM).

El objetivo de este proyecto se trata de obtener una segmentación automatizada de la retinopatía diabética y del edema macular diabético, a través de la evaluación de imágenes del fondo de la retina, de forma que, la detección de alguna anomalía se pueda hacer de forma eficaz, y por consiguiente, la determinación de estadio de dicha enfermedad.

No cabe duda de que, para desarrollar correctamente un algoritmo eficaz, es necesario un conjunto de imágenes de la retina diverso y representativo. En este caso, se va a trabajar con una base de datos de una población india, IDRiD (Indian Diabetic Retinopathy Image Dataset), la cual cuenta con 81 imágenes de la retina, de las cuales 54 serán utilizadas para el entrenamiento del programa, y 27 para testificar. En estas imágenes, se recogen lesiones típicas de la retinopatía diabética y estructuras retinianas normales anotadas a nivel de píxeles [2].

Cabe destacar que la RD comienza en muchas ocasiones con cambios en los capilares de la retina, y es por ello, que se ha decidido segmentar de las imágenes de la base de datos mencionada anteriormente, los vasos sanguíneos, las hemorragias y los exudados [4]. Además, la DM también está relacionada con un mal drenaje del humor acuoso provocando que el líquido se acumule en el interior del ojo, y generando una subida de tensión ocular (glaucoma). Esto da lugar a fallos en el nervio óptico, y es por ello que también se ha decidido segmentar el disco óptico de las imágenes [4][5].

A continuación, se muestran las segmentaciones obtenidas.

