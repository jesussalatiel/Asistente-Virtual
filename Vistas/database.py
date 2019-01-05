import pymongo
import base64
import datetime
from bson.objectid import ObjectId
import os

#Conexion a la base de datos
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#Seleccion de la base de datos
database = myclient['asistente']
#Seleccion de la tabla o archivo donde seran almacenados los registros
tabla_notas = database['notas_simples']
tabla_audio = database['audio_notas']


def saveNota(name, email, nota, imagen):
    try:
        with open(imagen,'rb') as imageFile:
            nota_simple = {
                'name_invitado': name,
                'email':email,
                'tipo': 'Nota Simple',
                'nota':nota,
                'date': (str(datetime.datetime.now()).split('.')[0]),
                'name_img':str(imagen.split('/')[4]),
                'path_img':imagen,
                'bin_imagen' : base64.b64encode(imageFile.read())
            }
        res = tabla_notas.insert_one(nota_simple)
        return res.inserted_id
    except:
        return False
  
def saveAudio(name, email, nota, audio, imagen):
    try:
        with open(imagen,'rb') as imageFile:
            nota_voz = {
              'name_invitado': name,
              'email':email,
              'tipo': 'Nota de Voz y/o Texto', 
              'nota':nota,
              'date': (str(datetime.datetime.now()).split('.')[0]),
              'path_nota_voz':audio,
              'name_img':str(imagen.split('/')[4]),
              'path_img':imagen,
              'bin_imagen' : base64.b64encode(imageFile.read())
            }
        res = tabla_audio.insert_one(nota_voz)
        return res.inserted_id  
    except:
        return False

#Metodo para buscar imagen por "id" en la base de datos        
def findImageId(id):
    #Variable para almacenar los datos decodificados de la imagen
    decoder_img = '' 
    #Ruta donde se gurdara temporalmente la imagen
    path = './Vistas/Invitados/tmp/'
    #Nombre de la imagen temporal
    filename = '{}some_image.jpg'.format(path)
    #Verificamos que exista la ruta de la carpeta si no procedemos a crearla
    os.makedirs(path, exist_ok=True)
    #Hacemos una busqueda por todo el JSON buscando por id y decodificamos la imagen perteneciente a este
    for id in tabla_notas.find({"_id": ObjectId(id)}):
        #Decodificamos la imagen
        decoder_img = base64.b64decode(id['bin_imagen'])
    #Procedemos a guardar la imagen en la ruta especificada
    with open(filename, 'wb') as f:
        #Escribimos que la imagen en la carpeta
        f.write(decoder_img)
#Metodo para eliminar notas
def deleteData(id):
    #Retonamos 1 si se elimino el elemento correctamente
    return tabla_notas.delete_one({'_id': ObjectId(id)}).deleted_count

#Metodo encargado de ontener la informacion especifica de este usuario       
def dataInvitado(id):
    #Guardamos los datos en una lista para tener un mejor control de los datos
    information = list()
    #Hacemos una busqueda en el JSON para obtener los datos del invitado 
    for data in tabla_notas.find({"_id": ObjectId(id)}):
        information.append(data['name_invitado'])
        information.append(data['email'])
        information.append(data['nota'])
        information.append(data['date'])
    #Retornamos los todos los datos almacenados anteriormente 
    return(information[:])

#Metodo para obtener todos los registros del archivo Notas Simples y ser mostrados en la tabla del archivo logica administrador
def findAllNote():
    return tabla_notas.find()

#Metodo para enlistar los campos clave del JSON
def keysList():
    #Creamos una lista en la que seran guardados los campos que obtengamos del JSON
    newlist = list()
    for keys in tabla_notas.find():
        for i in keys.keys():
            newlist.append(i)
    #Retornamos solo los campos del JSON 
    return newlist  

#Metodo para cerrar la conexion a la base de datos
def closeConection():
    return myclient.close()
