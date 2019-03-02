#Cargamos la base de datos en donde se encuentra registrados los usuarios
import Vistas.database as db
#Decodificamos las imageness
db.decodeKnown()
db.decodeAdministration()
#Iniciamos el reconocimiento e identificacion de rostros
import CNN.Recognition as rec

