import os, shutil

#Name Classes

#Generate Data File
original_dataset_dir = './train/train/'
base_dir = './data/'
os.makedirs(base_dir, exist_ok=True)

#Create Main Directories 
train_dir = os.path.join(base_dir, 'train')
os.makedirs(train_dir, exist_ok= True)

validation_dir = os.path.join(base_dir,'validation')
os.makedirs(validation_dir, exist_ok=True)

test_dir = os.path.join(base_dir, 'test')
os.makedirs(test_dir, exist_ok=True)

#Create Classes (Dogs and Cats)
train_dogs_dir = os.path.join(train_dir, 'dogs')
os.makedirs(train_dogs_dir, exist_ok=True)
train_cats_dir = os.path.join(train_dir, 'cats')
os.makedirs(train_cats_dir, exist_ok=True)

validate_cats_dir = os.path.join(validation_dir, 'cats')
os.makedirs(validate_cats_dir, exist_ok=True)
validate_dogs_dir = os.path.join(validation_dir, 'dogs')
os.makedirs(validate_dogs_dir, exist_ok=True)

test_cats_dir = os.path.join(test_dir, 'cats')
os.makedirs(test_cats_dir, exist_ok=True)
test_dogs_dir = os.path.join(test_dir, 'dogs')
os.makedirs(test_dogs_dir, exist_ok=True)


#Copy 1000 cats images to train_cats_dir
images_name = [ 'cat.{}.jpg'.format(i) for i in range (1000) ]
for name in images_name:
    #./train/train/cat.0.jpg
    src = os.path.join(original_dataset_dir, name)
    #./data/train/cats/cat.0.jpg
    dts = os.path.join(train_cats_dir, name)
    #Move images
    shutil.copyfile(src, dts)

#Copy 500 cats images to validation_cats_dir
images_name = ['cat.{}.jpg'.format(i) for i in range(500)]
for name in images_name:
    src = os.path.join(original_dataset_dir, name)
    dts = os.path.join(validate_cats_dir, name)
    shutil.copyfile(src, dts)

#Copy 500 cats images to test_cats_dir
images_name = ['cat.{}.jpg'.format(i) for i in range(500)]
for name in images_name:
    src = os.path.join(original_dataset_dir, name)
    dts = os.path.join(test_cats_dir, name)
    shutil.copyfile(src, dts)

#Copy 1000 dogs images to train_dogs_dir
images_name = ['dog.{}.jpg'.format(i) for i in range(1000)]
for name in images_name:
    src = os.path.join(original_dataset_dir, name)
    dts = os.path.join(train_dogs_dir, name)
    shutil.copyfile(src, dts)

#Copy 500 dogs images to validation_dogs_dir
image_name = ['dog.{}.jpg'.format(i) for i  in range(500)]
for name in image_name:
    src = os.path.join(original_dataset_dir, name)
    dts = os.path.join(validate_dogs_dir, name)
    shutil.copyfile(src, dts)

#Copy 500 dogs images to test_dogs_dir
image_name = ['dog.{}.jpg'.format(i) for i in range(500)]
for name in image_name:
    src = os.path.join(original_dataset_dir, name)
    dts = os.path.join(test_dogs_dir, name)
    shutil.copyfile(src, dts)

#Check Data Set
print('Imagenes de entrenamiento: {}, {}'.format('Gatos', len(os.listdir(train_cats_dir))))
print('Imagenes de validación: {}, {}'.format('Gatos', len(os.listdir(validate_cats_dir))))
print('Imagenes de test: {}, {}'.format('Gatos', len(os.listdir(test_cats_dir))))

print('Imagenes de entrenamiento: {}, {}'.format('Perros', len(os.listdir(train_dogs_dir))))
print('Imagenes de validación: {}, {}'.format('Perros', len(os.listdir(validate_dogs_dir))))
print('Imagenes de test: {}, {}'.format('Perros', len(os.listdir(test_dogs_dir))))


