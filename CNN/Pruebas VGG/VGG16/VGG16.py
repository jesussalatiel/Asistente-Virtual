

from keras.models import Model, Sequential
from keras.layers import Input, Convolution2D, ZeroPadding2D, MaxPooling2D, Flatten, Dense, Dropout, Activation
from PIL import Image
import numpy as np
from keras.preprocessing.image import load_img, save_img, img_to_array
from keras.applications.imagenet_utils import preprocess_input
from keras.preprocessing import image
import matplotlib.pyplot as plt


size_width, size_height= (224, 224)
weights = './weights_mat_to_keras.h5'

def preprocess_image(image_path):
    #Procedemos a tratar las imagenes como vector
    #Cargamos la imagen y establecemos un tamaño de entrada
    img = load_img(image_path, target_size=(size_width, size_height))
    #Convertimos la imagen en array
    img = img_to_array(img)
    #Se agrega una nueva columna al vector de imagen
    img = np.expand_dims(img, axis=0)
    #Adecuamos la imagen al formato que requiere el modelo
    img = preprocess_input(img)
    return img

def loadVggFaceModel():
    #Aplicamos transferencia de aprendizaje segun http://www.robots.ox.ac.uk/~vgg/publications/2015/Parkhi15/parkhi15.pdf tabla 3
    model = Sequential()
    #Tamaño de la imagen 224x244 x 3 que es el RGB
    model.add(ZeroPadding2D((1,1),input_shape=(size_width, size_height, 3)))

    #Bloque 1
    model.add(Convolution2D(64, (3, 3), activation = 'relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(64, (3,3), activation= 'relu'))
    model.add(MaxPooling2D((2, 2), strides=(2,2)))

    #Bloque 2
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(128,(3,3),activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(128, (3,3), activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    #Bloque 3
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, (3,3),activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(256, (3,3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(256, (3,3), activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    #Bloque 4
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, (3,3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, (3,3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, (3,3), activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    #Bloque 5
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, (3,3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, (3,3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, (3,3), activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    #Bloque 6
    model.add(Convolution2D(4096, (7,7), activation='relu', name = 'fc1'))
    model.add(Dropout(0.5))
    model.add(Convolution2D(4096, (1,1), activation='relu', name = 'fc2'))
    model.add(Dropout(0.5))
    model.add(Convolution2D(2622, (1,1)))
    model.add(Flatten())
    model.add(Activation('softmax'))
    #Ingresamos los datos al modelo
    vgg_face_descriptor = Model(inputs = model.layers[0].input, outputs = model.layers[-2].output)
    
    vgg_face_descriptor.load_weights(weights)
    

    return vgg_face_descriptor


def findCosineSimilarity(source_representation, test_representation):
    a = np.matmul(np.transpose(source_representation), test_representation)
    b = np.sum(np.multiply(source_representation, source_representation))
    c = np.sum(np.multiply(test_representation, test_representation))
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))


def findEuclideanDistance(source_representation, test_representation):
    euclidean_distance = source_representation - test_representation
    euclidean_distance = np.sum(np.multiply(
        euclidean_distance, euclidean_distance))
    euclidean_distance = np.sqrt(euclidean_distance)
    return euclidean_distance

epsilon = 0.40
model = loadVggFaceModel()
model.summary()


def verifyFace(path_img_1, path_img_2):  

    data_1 = preprocess_image(path_img_1)
    data_2 = preprocess_image(path_img_2)

    img_1 = model.predict(data_1)[0, :]
    img_2 = model.predict(data_2)[0, :]


    cosine_similarity = findCosineSimilarity(img_1, img_2)
    euclidean_distance = findEuclideanDistance(img_1, img_2)

    print('Similitud de Coseno: {} \nDistancia Eucladiana: {}'.format(cosine_similarity, euclidean_distance))

    f = plt.figure()
    f.add_subplot(1, 2, 1)
    
    plt.imshow(image.load_img(path_img_1))
    plt.xticks([])
    plt.yticks([])
    f.add_subplot(1, 2, 2)
    plt.imshow(image.load_img(path_img_2))
    plt.xticks([])
    plt.yticks([])
    

    if round(cosine_similarity, 2) < epsilon:
        plt.title('Es la misma persona')
        #plt.show(block=True)
        return('Es la misma persona')
    else:
        plt.title('No es la misma persona')
        #plt.show(block=True)
        return('No es la misma persona')





#Muestras mas representantivas
img_1 = './Test/Adam_Sandler_0001.jpg'
img_2 = './Test/Adam_Sandler_0004.jpg'
print(verifyFace(img_1, img_2))

img_1 = './Output/Adam_Sandler_0001.jpg'
img_2 = './Output/Adam_Sandler_0004.jpg'
print(verifyFace(img_1, img_2))



