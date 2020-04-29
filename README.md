# IDRiD
# Análisis de lesiones causadas por retinopatía diabética.


La retinopatía diabética (RD) es la complicación microvascular más común (50%) que puede presentarse en todos los tipos de diabetes mellitus (DM).

El objetivo de este proyecto se trata de obtener una segmentación automatizada de la retinopatía diabética y del edema macular diabético, a través de la evaluación de imágenes del fondo de la retina, de forma que, la detección de alguna anomalía se pueda hacer de forma eficaz, y por consiguiente, la determinación de estadio de dicha enfermedad.

No cabe duda de que, para desarrollar correctamente un algoritmo eficaz, es necesario un conjunto de imágenes de la retina diverso y representativo. En este caso, se va a trabajar con una base de datos de una población india, IDRiD (Indian Diabetic Retinopathy Image Dataset), la cual cuenta con 81 imágenes de la retina, de las cuales 54 serán utilizadas para el entrenamiento del programa, y 27 para testificar. En estas imágenes, se recogen lesiones típicas de la retinopatía diabética y estructuras retinianas normales anotadas a nivel de píxeles [2].

Cabe destacar que la RD comienza en muchas ocasiones con cambios en los capilares de la retina, y es por ello, que se ha decidido segmentar de las imágenes de la base de datos mencionada anteriormente, los vasos sanguíneos, las hemorragias y los exudados [4]. Además, la DM también está relacionada con un mal drenaje del humor acuoso provocando que el líquido se acumule en el interior del ojo, y generando una subida de tensión ocular (glaucoma). Esto da lugar a fallos en el nervio óptico, y es por ello que también se ha decidido segmentar el disco óptico de las imágenes [4][5].

A continuación, se muestran las segmentaciones obtenidas.

![vasos sanguíneos](https://github.com/ireneraven/IDRiD/blob/master/vasos_sanguineos.png) 

![Microaneurismas](https://github.com/ireneraven/IDRiD/blob/master/Microaneurismas.png) 


![Disco_optico](https://github.com/ireneraven/IDRiD/blob/master/Disco_optico.png) 


![Glaucoma](https://github.com/ireneraven/IDRiD/blob/master/Glaucoma.png) 


![Hemorragias](https://github.com/ireneraven/IDRiD/blob/master/Hemorragias.png) 

Posteriormente, dado que el fin que se desea obtener en nuestro caso con la red neuronal, es una correcta segmentación de las áreas de las imágenes que se desean detectar, ya que se corresponden con anomalías, la máquina deberá dividir la imagen dada en diferentes segmentos. Las sutilezas de las imágenes médicas son bastante complejas y a veces incluso desafiantes para los médicos capacitados. Una máquina que pueda entender estos matices e identificar las áreas necesarias puede tener un profundo impacto en la atención médica. Es por ello, que se ha decidido utilizar la red neuronal Unet, ya que esta fue diseñada especialmente para la segmentación de imágenes médicas [11]. 

A continuación, se muestra una imagen en la que se ve reflejada la arquitectura de la UNet.

![UNett](https://github.com/ireneraven/IDRiD/blob/master/UNet.png)


Por último, puesto que en la base de datos de este proyecto están también disponibles las máscaras realizadas por expertos de cuatro de las estructuras que se han segmentado, con ayuda de una herramienta estadística, Dice-coefficient, se compararán las máscaras segmentados por nosotros con las mencionadas previamente.

A continuación, se muestra un ejemplo con las imágenes de los exudados. Con la máscara realizada por expertos (roja) y la máscara realizada por nosotros (blanca) se aplica el algoritmo de Dice-coefficient y se obtiene un 0,7124 de similitud.

![Dice-coefficient](https://github.com/ireneraven/IDRiD/blob/master/Dice-coefficient.JPG)


