#Caracteristicas Generales de la VGG16
[VGG Face Descriptor](http://www.robots.ox.ac.uk/~vgg/software/vgg_face/)
[Deep Face Recognition](http://www.robots.ox.ac.uk/~vgg/publications/2015/Parkhi15/poster.pdf)

La arquitectura VGG16 fue desarrollado por Deep Face Recognition, Visual Geometry Group 
usado para identificar 1000 clases de objetos de ImageNet. Tiene 16 capas entrenables con un
tamaño de imagen de 224 x 224. Fue entrenado con: 
[the dataset is to obtain a list of names of candidate identities](https://www.imdb.com/interfaces/)
Contiene Celebridades y figuras publicas, al igual que politicos y actores
fue entrenado con 500K identidades diferentes, resultando en una listas de
2.5K de Mujeres y 2.5K de Hombres
##Arquitectura del Modelo
- Convolucion + ReLU activations
- MaxPooling
- Softmax
  
## Entrenamiento 
  - 10 epocas
  - SGD learninig rate 0.25

##Verificación
- Distancia Eucladiana para verificacion de identidad
- Curva ROC
- [Youtube Faces(YTF):](https://www.cs.tau.ac.il/~wolf/ytfaces/)
  Contiene 13,233 imagenes con 5,749 identidades 
- [Labeled Faces in the Wild dataset (LFW):](http://vis-www.cs.umass.edu/lfw/)
Contiene 3,425 videos de 1,595 personas de Youtube

##Implementacion
- MATLAB  toolbox MatConvNet
- 4 NVIDIA Titan Black GPU con 6 GB de memoria dedicada