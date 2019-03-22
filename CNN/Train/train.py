import tensorflow as tf
#from sklearn.metrics import confusion_matrix, classification_report
from keras.callbacks import ModelCheckpoint
import keras.backend as K
from keras import losses
from keras.initializers import glorot_uniform
from keras.utils import plot_model
from keras.utils.vis_utils import model_to_dot
from keras.applications.imagenet_utils import preprocess_input
from keras.utils.data_utils import get_file
from keras.utils import layer_utils, np_utils
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from keras.preprocessing import image
from keras.models import Sequential, Model, load_model
from keras.layers import Flatten, Input, Add, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, AveragePooling2D, MaxPooling2D, GlobalMaxPooling2D, Dropout
from keras import layers
import pickle
import pandas as pd
#import seaborn as sn
import cv2
#from IPython.display import SVG
import numpy as np
from scipy import misc
from PIL import Image
import glob
import matplotlib.pyplot as plt
import scipy.misc
from matplotlib.pyplot import imshow
from keras.datasets import cifar100
from keras.applications import vgg16


(x_train_original, y_train_original), (x_test_original,
                                       y_test_original) = cifar100.load_data(label_mode='fine')


y_train = np_utils.to_categorical(y_train_original, 100)
y_test = np_utils.to_categorical(y_test_original, 100)


x_train = x_train_original/255
x_test = x_test_original/255

K.set_image_data_format('channels_last')
K.set_learning_phase(1)

#imgplot = plt.imshow(x_train_original[3])
#plt.show()


def resize_data(data):
    data_upscaled = np.zeros((data.shape[0], 48, 48, 3))
    for i, img in enumerate(data):
        large_img = cv2.resize(img, dsize=(
            48, 48), interpolation=cv2.INTER_CUBIC)
        data_upscaled[i] = large_img

    return data_upscaled


x_train_resized = resize_data(x_train_original)
x_test_resized = resize_data(x_test_original)
x_train_resized = x_train_resized / 255
x_test_resized = x_test_resized / 255


def create_vgg16():
  model = vgg16.VGG16(include_top=True, weights=None, input_tensor=None,
                      input_shape=(48, 48, 3), pooling=None, classes=100)

  return model


vgg16_model = create_vgg16()
vgg16_model.compile(loss='categorical_crossentropy',
                    optimizer='sgd', metrics=['acc', 'mse'])


vgg16_model.summary()


vgg16 = vgg16_model.fit(x=x_train_resized, y=y_train, batch_size=32, epochs=10,
                        verbose=1, validation_data=(x_test_resized, y_test), shuffle=True)

#Guardamos los pesos
vgg16_model.save_weights('pesos.h5')

#Presentamos metricas obtenidas del entrenamiento  y validacion
plt.figure(0)
plt.plot(vgg16.history['acc'], 'r')
plt.plot(vgg16.history['val_acc'], 'g')
plt.xticks(np.arange(0, 11, 2.0))
plt.rcParams['figure.figsize'] = (8, 6)
plt.xlabel("Num of Epochs")
plt.ylabel("Accuracy")
plt.title("Training Accuracy vs Validation Accuracy")
plt.legend(['train', 'validation'])

plt.figure(1)
plt.plot(vgg16.history['loss'], 'r')
plt.plot(vgg16.history['val_loss'], 'g')
plt.xticks(np.arange(0, 11, 2.0))
plt.rcParams['figure.figsize'] = (8, 6)
plt.xlabel("Num of Epochs")
plt.ylabel("Loss")
plt.title("Training Loss vs Validation Loss")
plt.legend(['train', 'validation'])

plt.show()
