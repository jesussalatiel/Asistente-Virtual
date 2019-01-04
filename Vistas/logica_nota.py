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
        

        #self.label.setText("Haz clic en el botón")
        #self.pushButton.setText("Presióname")
        #self.pushButton.clicked.connect(self.actualizar)
        #self.label.setText("<html><head/><body><p><img src={}></p></body></html>".format(path))
    
    #Metodo encargado de construir la interfaz de nota
    def buildNota(self):
        #Hacemos una consulta a la base de datos para obtener la informacion del invitado
        data_invitado = db.dataInvitado(self._invitado)
        #Ingresamos el id de invitado para obtener su imagen
        self.idInvitado(self._invitado)
        #Path temporal para guardar la imagen del invitado
        self.path = './Vistas/Invitados/'
        #Ruta completa del invitado
        self.image = self.path+'tmp/{}'.format('some_image.jpg')
        #Ingresamos su imagen en un label para ser mostrado por pantalla
        self.label.setText(
            "<html><head/><body><p><img src={}></p></body></html>".format(self.image))
        #Datos basicos del usuario
        self.label_2.setText('Nombre: {}'.format(data_invitado[0]))
        self.setWindowTitle('Visita de {}'.format(data_invitado[0]))
        self.label_3.setText('Visito: {}'.format(data_invitado[3]))
        self.label_4.setText('Email: {}'.format(data_invitado[1]))
        self.textEdit.setText(data_invitado[2])
        
    
    def actualizar(self):
        self.label.setText("¡Acabas de hacer clic en el botón!")

    def closeEvent(self, event):
        #Eliminamos la carpeta temporal
        shutil.rmtree(self.path)
    
    #Metodo encargado de buscar la imagen 
    def idInvitado(self, id):
        #Buscamos la imagen y la insertamos en la vista de nota
        return db.findImageId(id)
           
def Second(id):
    return MainWindow(id)


