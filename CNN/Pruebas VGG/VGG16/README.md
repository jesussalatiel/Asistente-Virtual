#PreImage
Este archivo es encargado de detectar rostros en una imagen para despues ser pasados por la Red Neuronal
con un tamaño de imagen de 224 x 224. Estas imagenes son almacenadas en la carpeta "Output".

#VGG16 (OxfordNet)
Este archivo contiene la arquitectura VGG16 que es encargada de procesar la imagen para posteriormente hacer una prediccion y obtener 
los descriptores profundos de cada imagen que posteriormente seran analizados con diversos metodos:
- [Similitud de Coseno](https://es.wikipedia.org/wiki/Similitud_coseno)
-- La cual es una funcion trigonometrica que proporciona un valor igual a 1 si el angulo comprendido es cero, es decir si ambos valores apuntan a un mismo lugar. Cualquier ángulo existente entre los vectores, el coseno arrojaria un valor inferior a uno.

- [Distancia Eucladiana](https://www.ecured.cu/Distancia_eucl%C3%ADdea)
-- Sirve para definir la distancia entre dos puntos en otros tipos de espacios de tres o mas dimensiones.
(Tiene defectos) :
- El primero de ellos es que la uclidea es una distancia sensible a las unidades de medida de las variables: las diferencias entre las variables medidas con los valores altos contribuiran en mucha mayor medida que las diferencias entre los valores de las variables con valores bajos. Como consecuencia, los cambios de escala determinaran, tambien, cambios en la distancia entre los individuos.
- El segundo inconveniente es que si las variables utilizadas estan correlacionadas, estas variables nos daran una informacion, en gran medida redundante.

#Conv Filter Visualization para OxfordNet
El archivo es encargado de mostrar visualmente los filtros de cada capa que son guardados en una imagen.

