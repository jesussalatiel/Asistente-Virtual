import cv2
import numpy as np
import os, time
from random import choice
import pymongo
import base64
import shutil

video = cv2.VideoCapture(0)
face_casacade = cv2.CascadeClassifier('./CNN/Assets/haarcascade_frontalface_default.xml')
clock = 1
base_dir = './CNN/database/'
data_file = os.path.join(base_dir, 'PhotosAdmin/')
os.makedirs(data_file, exist_ok= True)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
database = myclient['asistente']
root = database['Administradores']

if video.isOpened() == False:
    print("No existe alguna camara conectada")
else:
    name = str(input('Ingresa tu nombre: '))
    email = str(input('Ingresa tu email: '))
    

    for seconds in range(clock):
        print('Tienes {} de {} segundos para ponerte chulo !'.format(seconds, clock))
        time.sleep(1)

    for i in range(0, 10):
        _, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_casacade.detectMultiScale(gray, 1.5, 5)

        for (x, y, w, h) in face:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
            detect_face = frame[int(y):int(y+h), int(x):int(x+w)]
            detected_face = cv2.resize(detect_face, (224, 224))
            cv2.imwrite(
                '{}{}.jpg'.format(data_file, i), detected_face)

        cv2.imshow("Sonrie", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


image = choice(os.listdir(data_file))
image = os.path.join(data_file,image)


with open(image, 'rb') as imageFile:
    query = {
        'name': name,
        'image': base64.b64encode(imageFile.read()),
        'email': email,
        'id_anterior': str('null')
 }
#Realizamos el registro
res = root.insert_one(query)

if len(str(res.inserted_id)) > 5:
    shutil.rmtree(data_file)
    print('Registro: {}'.format(res.inserted_id))

video.release()
cv2.destroyAllWindows()
