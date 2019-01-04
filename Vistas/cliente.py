import cv2
import os
from os import listdir
import datetime
x = datetime.datetime.now()
name = str(x).split('.')[1]

database_images = './Algoritmos/CNN/database/User_Unkonw/{}.jpg'.format(name)

def saveInvitado(img, modelo):
    cv2.imwrite(database_images, img)
    #deleteTrash(modelo)


def deleteTrash(modelo):    
    for file in listdir(database_images):
        #Dividimos el nombre de la imagen de su extension
        images, extension = file.split(".")
        path = database_images+images+'.'+extension
        print(path)
        imagen = cv2.imread(path)
        rostros = modelo.detectMultiScale(imagen, 1.3, 2)
        if rostros == ():
            os.remove(path)
            print('Validando datos.')