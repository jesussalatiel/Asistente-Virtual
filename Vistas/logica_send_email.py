from Vistas.vista_email import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import Vistas.database as db

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, id_invitado):
            super().__init__()
            
            #Cargamos los componentes correpondientes de la vista administrador
            self.setupUi(self)
            self.show()
            self._id_invitado = id_invitado
            self.buildEmail()
            #Evento del boton ver
            self.pushButton.clicked.connect(self.sendEmail)
            self.pushButton_2.clicked.connect(self.cancel)

    def buildEmail(self):
        #Titulo de la ventana
        data =  db.dataInvitado(self._id_invitado)
        self.setWindowTitle("Enviar correo a {}".format(data[0]))

    def sendEmail(self):
        print('Enviar correo')

    def cancel(self):
        print('Cancelar')

def windowsEmail(id):
    return MainWindow(id)

def startAdministration(id):
    app = QtWidgets.QApplication([])
    window = MainWindow(id)
    window.show()
    app.exec_()



