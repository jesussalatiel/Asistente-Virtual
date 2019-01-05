from Vistas.vista_nota import *
import Vistas.database as db
import shutil


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, id_invitado):
        super().__init__()
        self._invitado = id_invitado
        self.setupUi(self)
        self.show()
        self.buildNota()
        self.pushButton.clicked.connect(self.notificar)
        self.pushButton_2.clicked.connect(self.delete)
        self.pushButton_3.clicked.connect(self.play)

    # Metodo encargado de construir la interfaz de nota
    def buildNota(self):
        # Hacemos una consulta a la base de datos para obtener la informacion del invitado
        data_invitado = db.dataInvitado(self._invitado)
        # Ingresamos el id de invitado para obtener su imagen
        self.idInvitado(self._invitado)
        # Path temporal para guardar la imagen del invitado
        self.path = './Vistas/Invitados/'
        # Ruta completa del invitado
        self.image = self.path+'tmp/{}'.format('some_image.jpg')
        # Ingresamos su imagen en un label para ser mostrado por pantalla
        self.label.setText(
            "<html><head/><body><p><img src={}></p></body></html>".format(self.image))
        # Datos basicos del usuario
        self.label_2.setText('Nombre: {}'.format(data_invitado[0]))
        self.setWindowTitle('Visita de {}'.format(data_invitado[0]))
        self.label_3.setText('Visito: {}'.format(data_invitado[3]))
        self.label_4.setText('Email: {}'.format(data_invitado[1]))
        self.textEdit.setText(data_invitado[2])
        #Verificamos si el usuario dejo una nota de voz para desplegar el boton
        if data_invitado[4] == None:
            self.pushButton_3.setGeometry(0, 0, 0, 0)
            self.pushButton_3.setEnabled(False)
        
            
    def notificar(self):
        print("Notificar")

    def play(self):
        print("Reproducir nota")

    #Metodo encargado de eliminar las notas 
    def delete(self):
        if (db.deleteData(self._invitado)) == 1:
            print('Eliminado Exitosamente')    
        self.close()

    #Control del evento cerrar que es mostrado en la ventana
    def closeEvent(self, event):
        #Evento de cerrar en la pantalla
        self.closeAll()

    #Metodo encargado de liberar memoria al cerra las ventana
    def closeAll(self):
        # Eliminamos la carpeta temporal
        shutil.rmtree(self.path)
        self.close()
    
    # Metodo encargado de buscar la imagen
    def idInvitado(self, id):
        # Buscamos la imagen y la insertamos en la vista de nota
        return db.findImageId(id)

#Metodo inicial para ejecutar la segunda ventana llamada Nota
def secondWindows(id):
    #Retornamos una instancia de pantalla para poder utilizar sus objetos en otras clases
    return MainWindow(id)
