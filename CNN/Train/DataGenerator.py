from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import numpy as np
from keras.applications.imagenet_utils import preprocess_input
#Este es el metodo de generar diversas vistas de la imagen para crear un set de datos mas extenso
datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    #Propiedades extras
    rotation_range=40,
    width_shift_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

img = load_img('./cat.0.jpg')  # this is a PIL image
x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
# this is a Numpy array with shape (1, 3, 150, 150)
x = x.reshape((1,) + x.shape)

# the .flow() command below generates batches of randomly transformed images
# and saves the results to the `preview/` directory
i = 0

#Guardamos las imagenes en una carpeta llamada "preview" con el nombre "imagen " y la extension ".jpg" 
for batch in datagen.flow(x, batch_size=1,
                          save_to_dir='preview', save_prefix='imagen', save_format='jpg'):
    i += 1
    if i > 20:
        break


def preprocess_image(image_path):
    #Procedemos a tratar las imagenes como vector
    #Cargamos la imagen y establecemos un tamaño de entrada
    img = load_img(image_path, target_size=(224, 224))
    #Convertimos la imagen en array
    img = img_to_array(img)
    #Se agrega una nueva columna al vector de imagen
    img = np.expand_dims(img, axis=0)
    #Adecuamos la imagen al formato que requiere el modelo
    img = preprocess_input(img)
    return img


preprocess_image('./cat.0.jpg')
