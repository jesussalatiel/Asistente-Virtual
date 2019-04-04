import cv2
import os
import matplotlib.pyplot as plt

face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
INPUT_FILE_IMAGES = './Test'
OUTPUT_FILE_IMAGES = 'Output'
os.makedirs(OUTPUT_FILE_IMAGES, exist_ok= True)

def preprocessImage(path, image, showImage):
    path = os.path.join(path, image)
    camara = cv2.imread(path)
    gray = cv2.cvtColor(camara, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor = 1.5,
        minNeighbors = 5
    )

    print('Detected {0} faces !'.format(len(faces)))

    if len(faces) == 0:
        print('La imagen: {0} tiene algún ruido.'.format(image))
    else:
        f = plt.figure()
        f.add_subplot(1, 3, 1)
        plt.title('Input')
        plt.imshow(camara)
        plt.xticks([])
        plt.yticks([])
    
        for(x, y, w, h) in faces:
            cv2.rectangle(camara, (x, y), (x + w, y + h), (0, 255, 0), 2)
            detected_face = camara[int(y):int(y+h), int(x):int(x+w)]
            detected_face = cv2.resize(detected_face, (224, 224))

            f.add_subplot(1, 3, 2)
            plt.title('Face Detection')
            plt.imshow(camara)
            plt.xticks([])
            plt.yticks([])

            f.add_subplot(1, 3,3)
            plt.title('Output')
            plt.imshow(detected_face)
            plt.xticks([])
            plt.yticks([])

            if showImage:
                plt.show()  
            path = os.path.join(OUTPUT_FILE_IMAGES, image)
            cv2.imwrite(path, detected_face)


for image in os.listdir(INPUT_FILE_IMAGES):
    preprocessImage(INPUT_FILE_IMAGES, image, True)
