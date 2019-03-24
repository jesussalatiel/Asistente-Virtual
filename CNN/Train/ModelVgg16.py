import os, random, shutil
import matplotlib.pyplot as plt
import numpy as np
from keras.preprocessing import image
from keras.applications import VGG16
from keras.preprocessing.image import ImageDataGenerator
from keras import models
from keras import layers
from keras import optimizers
import matplotlib.pyplot as plt
import tensorflow as tf
import keras
from keras.layers import Input, Convolution2D, ZeroPadding2D, MaxPooling2D, Flatten, Dense, Dropout, Activation

config = tf.ConfigProto(device_count={'GPU': 1, 'CPU': 56})
sess = tf.Session(config=config)
keras.backend.set_session(sess)


#Base Variables
base_dir = './data/'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')
test_dir = os.path.join(base_dir, 'test')

train_cats_dir = os.path.join(train_dir, 'cats')
train_dogs_dir = os.path.join(train_dir, 'dogs') 

test_cats_dir = os.path.join(test_dir, 'cats') 
test_dogs_dir = os.path.join(test_dir, 'dogs')

#Default imppit size for VGG16
img_width, img_height = 224, 224 
train_size, validate_size, test_size = 2000, 1000, 1000
v_batch_size = 32
epoch = 100

#Show pictures
def showPictures(path):
    #Get random image
    random_img = random.choice(os.listdir(path))
    img_path = os.path.join(path, random_img)
    #Preprocess picture for show on windows 
    img = image.load_img(img_path, target_size=(img_width, img_height))
    img_tensor = image.img_to_array(img)
    img_tensor /= 255.
    plt.imshow(img_tensor) 
    plt.show()
'''
for i in range(0, 2):
    showPictures(train_cats_dir)
    showPictures(train_dogs_dir)
'''
#Instantiate convolutional base
conv_base = VGG16(weights= 'imagenet', include_top= False, input_shape= (img_width, img_height, 3))
#Check architecture
conv_base.summary()



#Extract features
datagen = ImageDataGenerator(rescale=1./255)

def extract_features(directory, sample_count):
    features = np.zeros(shape =(sample_count, 7, 7, 512))
    labels = np.zeros(shape = (sample_count))
    
    #Preprocess data
    generator = datagen.flow_from_directory(
        directory,
        target_size=(img_width, img_height),
        batch_size=v_batch_size,
        class_mode='binary'
    )

    #Pass data through convolutional base
    i = 0
    for inputs_batch, labels_batch in generator:
        features_batch = conv_base.predict(inputs_batch)
        features[i * v_batch_size: (i + 1) * v_batch_size] = features_batch
        labels[i * v_batch_size: (i + 1) * v_batch_size] = labels_batch
        i += 1
        if i * v_batch_size >= sample_count:
            break

    return features, labels

train_features, train_labels = extract_features(train_dir, train_size)
validation_features, validation_labels = extract_features(validation_dir, validate_size)
test_feature, test_labels = extract_features(test_dir, test_size)


#Define model
model = models.Sequential()
model.add(ZeroPadding2D((1, 1), input_shape=(img_width, img_height, 3)))
model.add(Convolution2D(64, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1, 1)))
model.add(Convolution2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2), strides=(2, 2)))
model.summary()

# Compile model
model.compile(optimizer=optimizers.Adam(),
              loss='binary_crossentropy',
              metrics=['acc'])

'''
# Train model
history = model.fit(train_features, train_labels,
                    epochs=100,
                    batch_size=v_batch_size,
                    validation_data=(validation_features, validation_labels))

# Save model
model.save('../Assets/dogs_cat_gap.h5')
#Plot results
acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc)+1)

plt.plot(epochs, acc, 'bo', label='Training accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()
'''

# Define function to visualize predictions
def visualize_predictions(classifier, n_cases):
    for i in range(0, n_cases):
        path = random.choice([test_cats_dir, test_dogs_dir])

        # Get picture
        random_img = random.choice(os.listdir(path))
        img_path = os.path.join(path, random_img)
        img = image.load_img(img_path, target_size=(img_width, img_height))
        # Image data encoded as integers in the 0–255 range
        img_tensor = image.img_to_array(img)
        img_tensor /= 255.  # Normalize to [0,1] for plt.imshow application

        # Extract features
        features = conv_base.predict(
            img_tensor.reshape(1, img_width, img_height, 3))

        # Make prediction
        try:
            prediction = classifier.predict(features)
        except:
            prediction = classifier.predict(features.reshape(1, 7 * 7 * 512))

        # Show picture
        plt.imshow(img_tensor)
        plt.show()

        # Write prediction
        if prediction < 0.5:
            print('Cat')
        else:
            print('Dog')





# Visualize predictions
visualize_predictions(model, 5)
