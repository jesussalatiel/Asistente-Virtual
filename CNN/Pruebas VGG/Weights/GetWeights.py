'''
http://www.robots.ox.ac.uk/~vgg/software/vgg_face/
'''
from scipy.io import loadmat
from keras.models import Sequential, Model
from keras.layers import Input, Dense, Flatten, Dropout, Activation, Lambda, Permute, Reshape
from keras.layers import Convolution2D, ZeroPadding2D, MaxPooling2D
from keras import backend as K
from keras.preprocessing.image import load_img, img_to_array
import tarfile, wget, os
from keras.utils import plot_model

K.set_image_data_format('channels_last')
#Face detection and VGG Face descriptor source code and models (MatConvNet)
matconvnet = 'vgg_face_matconvnet'

#Verify if exists VGG FACE MODEL 
if os.path.exists(matconvnet):
    print('OK !')
elif os.path.exists('{}.tar.gz'.format(matconvnet)):
    file = ('{}.tar.gz'.format(matconvnet))
    tar = tarfile.open(file)
    tar.extractall()
else:
    DATA_FILE_VGG16_MAT = 'http://www.robots.ox.ac.uk/~vgg/software/vgg_face/src/{}.tar.gz'.format(matconvnet)
    wget.download(DATA_FILE_VGG16_MAT)
    file = ('{}.tar.gz'.format(matconvnet))
    tar = tarfile.open(file)
    tar.extractall()

data = loadmat('./{}/data/vgg_face.mat'.format(matconvnet), matlab_compatible=False, struct_as_record=False)
net = data['net'][0, 0]
l = net.layers
description = net.classes[0, 0].description

print('SUMMARY LAYERS AND WEIGHTS')
print('{} {}'.format(l.shape, description.shape))

print('{} {}'.format(l[0, 10][0, 0].type[0], l[0, 10][0, 0].name[0]))

print('{} {}'.format(l[0, 10][0, 0].weights[0, 0].shape,
                      l[0, 10][0, 0].weights[0, 1].shape))


def convblock(cdim, nb, bits=3):
    Layer = []

    for k in range(1, bits+1):
        convname = 'conv'+str(nb)+'_'+str(k)
        Layer.append(Convolution2D(cdim, kernel_size=(3, 3), padding='same', activation='relu', name=convname)) 
    Layer.append(MaxPooling2D((2, 2), strides=(2, 2)))

    return Layer

def vgg_face_blank():
        
    withDO = True 
    
    if True:
        model = Sequential()
        
        
        model.add( Permute((1,2,3), input_shape=(224, 224, 3)) ) 

        for l in convblock(64, 1, bits=2):
            model.add(l)

        for l in convblock(128, 2, bits=2):
            model.add(l)
        
        for l in convblock(256, 3, bits=3):
            model.add(l)
            
        for l in convblock(512, 4, bits=3):
            model.add(l)
            
        for l in convblock(512, 5, bits=3):
            model.add(l)
        
        
        model.add( Convolution2D(4096, kernel_size=(7, 7), activation='relu', name='fc6') )
        if withDO:
            model.add( Dropout(0.5) )
        
        model.add( Convolution2D(4096, kernel_size=(1, 1), activation='relu', name='fc7') )
        if withDO:
            model.add( Dropout(0.5) )
        
        model.add( Convolution2D(2622, kernel_size=(1, 1), activation='relu', name='fc8') )
        model.add( Flatten() )
        model.add( Activation('softmax') )
        
        return model
    
    else:
        raise ValueError('No implementado')
        
def weight_compare(kmodel):
    kerasnames = [lr.name for lr in kmodel.layers]

   
    prmt = (0, 1, 2, 3)

    for i in range(l.shape[1]):
        matname = l[0, i][0, 0].name[0]
        mattype = l[0, i][0, 0].type[0]
        if matname in kerasnames:
            kindex = kerasnames.index(matname)
            print(matname, mattype)
            print(l[0, i][0, 0].weights[0, 0].transpose(prmt).shape, l[0, i][0, 0].weights[0, 1].shape)
            print(kmodel.layers[kindex].get_weights()[0].shape, kmodel.layers[kindex].get_weights()[1].shape)
            print('------------------------------------------')
        else:
            print('MISSING : ', matname, mattype)
            print('------------------------------------------')

def copy_mat_to_keras(kmodel):
    
    kerasnames = [lr.name for lr in kmodel.layers]

   
    prmt = (0,1,2,3)

    for i in range(l.shape[1]):
        matname = l[0,i][0,0].name[0]
        if matname in kerasnames:
            kindex = kerasnames.index(matname)
            #print matname
            l_weights = l[0,i][0,0].weights[0,0]
            l_bias = l[0,i][0,0].weights[0,1]
            f_l_weights = l_weights.transpose(prmt)
           
            assert (f_l_weights.shape == kmodel.layers[kindex].get_weights()[0].shape)
            assert (l_bias.shape[1] == 1)
            assert (l_bias[:,0].shape == kmodel.layers[kindex].get_weights()[1].shape)
            assert (len(kmodel.layers[kindex].get_weights()) == 2)
            kmodel.layers[kindex].set_weights([f_l_weights, l_bias[:,0]])
            

#Instance Vgg_Face_Blank to FaceModel       
FaceModel = vgg_face_blank()
weight_compare(FaceModel)
copy_mat_to_keras(FaceModel)


#Save Weights
plot_model(FaceModel, to_file='model.png')
FaceModel.save_weights('./weights_mat_to_keras.h5')
print('Successful Weights !')

