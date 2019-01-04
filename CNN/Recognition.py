from keras.models import Model, Sequential
from keras.layers import Input, Convolution2D, ZeroPadding2D, MaxPooling2D, Flatten, Dense,Dropout, Activation
from PIL import Image
import numpy as np
from keras.preprocessing.image import load_img, save_img, img_to_array
from keras.applications.imagenet_utils import preprocess_input
from keras.preprocessing import image
import matplotlib.pyplot as plt
from keras.models import model_from_json
import tensorflow as tf
import keras
import cv2 
from os import listdir
import cv2, imutils, os, time, shutil, time
#import Vistas.interfaz_admin as admin
import Vistas.cliente as cliente
import datetime
import Vistas.logica_cliente as cli
#------------------------------------------------------------------------------------------
#################Configuracion del CPU-GPU
config = tf.ConfigProto( device_count = {'GPU': 1 , 'CPU': 56} )
sess = tf.Session(config=config) 
keras.backend.set_session(sess)
#------------------------------------------------------------------------------------------
##############################################################################################
#########################PARAMETROS GENERALES DEL PROGRAMA####################################
#Titulo de la ventana de OpenCV
title_windows = 'Identificacion de Rostros'
#Cargamos clasificador de caras frontales
face_cascade = cv2.CascadeClassifier('./CNN/Assets/haarcascade_frontalface_default.xml')
#Seleccionamos el tamaño de la imagen de entrada
size_height, size_width = 224, 224 
#Cargamos la bases de datos de imagenes
#En esta ubicacion se alojan las imagenes que se quieren reconocer con extension jpg
database_images = './CNN/database/Usuarios_Registrados/'
#Color de la linea que es mostrada en OpenCV
color = (0,255,0)
#Ruta de pesos https://drive.google.com/file/d/1CPSeum3HpopfomUEK1gybeuIVoeJT_Eo/view
weights = './CNN/Assets/vgg_face_weights.h5'
##Instancia de la camara 
camara = cv2.VideoCapture(0)
################################################################################################
url = 'http://127.0.0.1:8081/'
################################################################################################
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
    model.add(Convolution2D(4096, (7,7), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Convolution2D(4096, (1,1), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Convolution2D(2622, (1,1)))
    model.add(Flatten())
    model.add(Activation('softmax'))
    #Ingresamos los datos al modelo
    vgg_face_descriptor = Model(inputs = model.layers[0].input, outputs = model.layers[-2].output)
    #Cargamos pesos ya pre-entrenado
    model.load_weights(weights)
    #vgg_face_descriptor.load_weights(weights)
    
    return vgg_face_descriptor

def findSimilarity(source_image, representation):
    #Utilizamos Distancia del coseno para detectar las similitudes entre vectores
    #https://sefiks.com/2018/08/13/cosine-similarity-in-machine-learning/
    a = np.matmul(np.transpose(source_image), representation)
    b = np.sum(np.multiply(source_image, source_image))
    c = np.sum(np.multiply(representation, representation))

    return 1 - (a / (np.sqrt(b)*(np.sqrt(c))))


#Cargamos el modelo 
model = loadVggFaceModel()
#Variable donde se van a cargar los datos de las imagenes
array_images = dict()

#Procedemos a tratar los nombres de la imagenes
for file in listdir(database_images):
    #Dividimos el nombre de la imagen de su extension
    images, extension = file.split(".")
    path = database_images+'%s.jpg' % (images)
    array_images[images]= model.predict(preprocess_image(path))[0,:] 
    

print("Servicio Iniciado.")
exit = True
name =''
user = 0
list_access  = []
while(exit):
    #Empezamos la lectura de video
    _, img = camara.read()
    #Detectamos solo caras frontales
    faces = face_cascade.detectMultiScale(img, 1.5, 5)
    #Pintamos las caras detectadas
   
    for (x,y,w,h) in faces:       
        #Dibijamos un rectangulo para mostrar la cara
        cv2.rectangle(img,(x,y),(x+w, y+h), color, 2) 
        #Seleccionamos las posiciones de la cara encerrada en el rectangulo
        detected_face = img[int(y):int(y+h), int(x):int(x+w)]
        ##Guardamos el rostro detectado con nuevas medidas
        detected_face = cv2.resize(detected_face, (size_width, size_height))
        #Convertimos la imagen a matriz
        img_pixels = image.img_to_array(detected_face).astype(np.float32)
        #Unimos la matriz 
        img_pixels = np.expand_dims(img_pixels, axis= 0)
        # Hacemos una prediccion 
        captured_reprentation = model.predict(img_pixels)[0,:]
        found = 0 #Variable para guardar los caras identificadas   
        acierto = 0.0 
        for i in array_images:
            #Renombramos a 'i' con la variable que contiene el nombre de la persona
            image_name = i.split('_')[0]
            representation = array_images[i]
            #Metodo encargado de encontrar las similitudes con el metodo de distancia del coseno
            similarity = findSimilarity(representation, captured_reprentation)
            #Evaluamos el porcentaje de similitud 
            acierto=(round(similarity,2))
            if(acierto < 0.27): # Si es menor que 0.27 es cara detectada y procedemos a dibijar el nombre y porcentaje de la similitud 
                acierto_str = str(abs(round(similarity,2)-100))+ ' %'
                print('Es {} en {} %'.format(image_name,abs(round(similarity,2)-100)))
                cv2.putText(img,acierto_str,(int(x+w-190), int(y-10)), cv2.FONT_HERSHEY_SIMPLEX, 1,color, 2)
                cv2.putText(img,image_name,(int(x+w-140), int(y-40)), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                found = 1
                user = 0 
                list_access.append(abs(round(similarity,2)-100))                
                break    
        #Variables para obtener la fecha 
        date = datetime.datetime.now()
        name = str(date).split('.')[1]
        #Verificamos los rostros presentes en la imagen
        if len(faces) > 2:
            print('Se detectaron {} rostros.'.format(len(faces)))
            database_images = './CNN/database/Usuarios_Desconocidos/muchas_{}.jpg'.format(name)
            user = 0
            del list_access[:] 
            cv2.imwrite(database_images, img)
        #Comparamos la lista para crear un promedio de la cara detectada y permitir el acceso
        if found== 1: 
            if len(list_access) > 5:
               if (sum(list_access) // len(list_access)) > 95:  
                   print('Desplegar panel de control') 
                   
        #Si no es detectada algun rostro aumentamos contador y volvemos a relizar el proceso para comprobar que en verdad no es usuario registrado 
        # y pueda ser tratado como invitado       
        if found == 0:
            user += 1
            print("{}. Desconocido".format(user))
            cv2.putText(img,'Invitado',((x+w-170), (y-10)), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            if user == 10: 
                database_images = './CNN/database/Usuarios_Desconocidos/{}.jpg'.format(name)
                cv2.imwrite(database_images, detected_face)
                user = 0
                
                cli.startCliente(database_images)
                del list_access[:] 
                
                
    #Titulo de la ventana     
    cv2.imshow(title_windows, img)
    #Si es presionado la tecla 'q' sales del programa
    if cv2.waitKey(1) & 0xFF == ord('q'): 
     #if exit === 'q':
       break

#Liberar Memoria
camara.release()
cv2.destroyAllWindows()