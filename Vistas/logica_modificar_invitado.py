from Vistas.vista_modificar_invitado import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import Vistas.database as db


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, id_invitado):
            #QtWidgets.QMainWindow.__init__(self)
            super().__init__()
            #Cargamos los componentes correpondientes de la vista administrador
            self.setupUi(self)
            self.show()

#Instancia de la ventana para abrir en otra vista
def modifyKnown(id_invitado):
    return MainWindow(id_invitado)

#Ejecucion de todos los Widgets de la ventana
def startModifyKnown(id_invitado):
    app = QtWidgets.QApplication([])
    window = MainWindow(id_invitado)
    window.show()
    app.exec_()
