from Vistas.vista_nota import *
import Vistas.database as db
import shutil
import os
from PyQt5.QtWidgets import QMessageBox
import Vistas.logica_administrador

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, id_invitado):
        super().__init__()
        self._invitado = id_invitado
        self.setupUi(self)
        self.show()
        self.buildNota()
        self.pushButton.clicked.connect(self.recordar)
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
        self.setWindowTitle('Notificacion de {}'.format(data_invitado[0]))
        self.label_3.setText('Visito: {}'.format(data_invitado[3]))
        self.label_4.setText('Email: {}'.format(data_invitado[1]))
        self.textEdit.setText(data_invitado[2])
        #Verificamos si el usuario dejo una nota de voz para desplegar el boton
        if data_invitado[4] == None:
            self.pushButton_3.setGeometry(0, 0, 0, 0)
            self.pushButton_3.setEnabled(False)
        
        print(db.exitsInvitado(self._invitado))
        
    #Metodo encargado de recordar al usuario        
    def recordar(self):
        name_invitado = str(db.dataInvitado(self._invitado)[0]).upper()        
        if (db.safeInvitado(name_invitado, self.image)):
            QMessageBox.information(self, 'Alta de Invitado ',
                                    'Se reconocera al nuevo invitado por: {}'.format(name_invitado))
        else:
            QMessageBox.warning(self, "Usuario Existente",
                                "Ya existe un usuario con el mismo nombre.")
    
    #Metodo para reproducir la nota de voz
    def play(self):
        print("Reproducir nota")

    #Metodo encargado de eliminar las notas 
    def delete(self):
        buttonReply = QMessageBox.warning(self, 'Eliminacion de Registro', "Esta seguro de eliminar el registro", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            if (db.deleteData(self._invitado)) == 1:
                QMessageBox.information(self, 'Eliminacion de Recordatorio ',
                                    'Eliminacion Exitosa')
            self.next = Vistas.logica_administrador.other()
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
        self.next = Vistas.logica_administrador.other()
    
    # Metodo encargado de buscar la imagen
    def idInvitado(self, id):
        # Buscamos la imagen y la insertamos en la vista de nota
        return db.findImageId(id)

#Metodo inicial para ejecutar la segunda ventana llamada Nota
def secondWindows(id):
    #Retornamos una instancia de pantalla para poder utilizar sus objetos en otras clases
    return MainWindow(id)
