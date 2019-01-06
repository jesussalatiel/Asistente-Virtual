import pymongo
import base64
import datetime
from bson.objectid import ObjectId
import os
import cv2


################### Parametros Genrales de BD ######################################
####################################################################################
#Conexion a la base de datos
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#Seleccion de la base de datos
database = myclient['asistente']
#Seleccion de la tabla o archivo donde seran almacenados los registros
table_notas = database['Notas']
invitado_conocido = database['Conocidos']
root = database['Administradores']
####################################################################################


#Metodo encargado de guardar las notas en la base de datos 
def safeData(name, email, nota, imagen, type, audio):     
    try:
        #Abrimos la imagen para poder codificarla a binario
        with open(imagen,'rb') as imageFile:
            #Creamos el JSON con los campos que contendra el archivo
            nota_simple = {
                'name_invitado': name,
                'email':email,
                'tipo': type,
                'nota':nota,
                'path_nota_voz': audio,
                'date': (str(datetime.datetime.now()).split('.')[0]),
                'name_img':str(imagen.split('/')[4]),                
                'path_img':imagen,
                'bin_imagen' : base64.b64encode(imageFile.read())
            }
        #Agregamos el objeto a la base de datos
        res = table_notas.insert_one(nota_simple)
        #Retornamos el id del objeto agregado
        return res.inserted_id
    except:
        #Retornamos False si ocurrio un problema en la codificacion de la imagen
        return False

#Metodo encargado de guardar todos los administradores del sistema
def saveAdministrator(id_invitado):    
    #Realizamos un recorrido en la base para obtener los parametros respectivos del ID del invitado para ser almacenados en administradores
    for invitado in invitado_conocido.find({'_id': ObjectId(id_invitado)}):
        #Creamos el JSON de insercion de datos que seran guardados en la base 
        query = {
            'name': invitado['name'],
            'image': invitado['image'],
            'email': invitado['email'],
            'id_anterior': invitado['id_anterior']
        }
        #Realizamos el registro
        res = root.insert_one(query)
        if len(str(res.inserted_id)) >= 4:
            #Enviamos True si todo salio bien
            return True if (invitado_conocido.delete_one({'_id': ObjectId(id_invitado)}).deleted_count) == 1 else False
    #Retornamos Falso si no se ingreso el registro
    return False
    

#Eliminamos a conocidos
def deleteKnown(id_invitado):
    return True if (invitado_conocido.delete_one({'_id': ObjectId(id_invitado)}).deleted_count) == 1 else False

#Metodo para guardar a Invitados
def safeInvitado(name, email, imagen, id_anterior):
    #Leemos la imagen para ser convertida a escala de grises
    image = cv2.imread(imagen)
    #Guardamos la imagen en escala de grises para el fucninamiento de la red neuronal
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Escribimos la imagen a escala de grises en su misma ruta y con el mismo nombre
    cv2.imwrite(imagen, gray)
    #Procedemos a convertir la imagen a binario para almacenarlo en la base de datos
    with open(imagen, 'rb') as imageFile:
        know = {
            'name': name,
            'email':email,
            'image': base64.b64encode(imageFile.read()),
            'id_anterior': id_anterior
        }
    #Insertamos al usuario en la tabla Invitado Conocido
    res = invitado_conocido.insert_one(know)
    #Retornamos el id del usuario registrado
    return str(res.inserted_id)

#Decodificamos todos los usuarios conocidos
def decodeKnown():
    #Establecemos los usuarios en la base de datos de la red neuronal
    path = './CNN/database/Usuarios_Registrados/'
    #Verificamos que exista la carpeta si no la creamos
    os.makedirs(path, exist_ok=True)
    #Hacemos una consulta a la base de datos para ver quienes son los usuarios registrados
    for known in invitado_conocido.find():        
        #Creamos el path de la imagen con su respectivo nombre
        path_image= (path+str(known['_id'])+'.jpg')
        #Abrimos memoria para que pueda escribir la imagen en el path seleccionada
        with open(path_image, 'wb') as f:
            #Escribimos la imagen decodificada en el path establecido
            img = base64.b64decode(known['image'])
            f.write(img)

def decodeAdministration():
    #Establecemos los usuarios en la base de datos de la red neuronal
    path = './CNN/database/Usuarios_Registrados/'
    #Verificamos que exista la carpeta si no la creamos
    os.makedirs(path, exist_ok=True)
    for administrador in root.find():
        path_image = (path+str(administrador['_id'])+'.jpg')
        with open(path_image, 'wb') as image:
            img = base64.b64decode(administrador['image'])
            image.write(img)

#Metodo para obtener todos los datos del usuario conocido
def dataKnown(): 
    return invitado_conocido.find().sort('name')
def dataRoot():
    return root.find()
    
def dataKnownId(id_invitado):
    for data in invitado_conocido.find({'_id': ObjectId(id_invitado)}):
        return data

def dataRootAll():
    return root.find().sort('name')
    
def dataKnownAll():
    return invitado_conocido.find()

def updateUserId(id_invitado, name, email):
    modify = {
        "$set":{
            'name':name,
            'email':email
        }
    }
    invitado_conocido.update_one({'_id': ObjectId(id_invitado)}, modify)
    return True 

#Verificar si exite el invitado en usuarios conocidos
def exitsInvitado(id):
    query = {'id_anterior':id}
    veces = 0
    verify = invitado_conocido.find({}, query)
    for exist in verify:
        if (exist['id_anterior']) in id:
            veces += 1
    if veces < 1:
        return False
        
    return True  

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
    for id in table_notas.find({"_id": ObjectId(id)}):
        #Decodificamos la imagen
        decoder_img = base64.b64decode(id['bin_imagen'])
    #Procedemos a guardar la imagen en la ruta especificada
    with open(filename, 'wb') as f:
        #Escribimos que la imagen en la carpeta
        f.write(decoder_img)


#Metodo para eliminar notas
def deleteData(id):
    #Retonamos 1 si se elimino el elemento correctamente
    return table_notas.delete_one({'_id': ObjectId(id)}).deleted_count


#Metodo encargado de ontener la informacion especifica de este usuario       
def dataInvitado(id):
    #Guardamos los datos en una lista para tener un mejor control de los datos
    information = list()
    #Hacemos una busqueda en el JSON para obtener los datos del invitado 
    for data in table_notas.find({"_id": ObjectId(id)}):
        information.append(data['name_invitado'])
        information.append(data['email'])
        information.append(data['nota'])
        information.append(str(data['_id']))
        information.append(data['date'])
        information.append(data['path_nota_voz'])
    #Retornamos los todos los datos almacenados anteriormente 
    return(information[:])


#Metodo para obtener todos los registros del archivo Notas Simples y ser mostrados en la tabla del archivo logica administrador
def findAllNote():
    return table_notas.find().sort("name_invitado")

#Metodo para enlistar los campos clave del JSON
def keysList():
    #Creamos una lista en la que seran guardados los campos que obtengamos del JSON
    newlist = list()
    for keys in table_notas.find():
        for i in keys.keys():
            newlist.append(i)
    #Retornamos solo los campos del JSON 
    return newlist  

#Metodo para cerrar la conexion a la base de datos
def closeConection():
    return myclient.close()
