from Vistas.vista_modificar_admin import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
            #QtWidgets.QMainWindow.__init__(self)
            super().__init__()
            #Cargamos los componentes correpondientes de la vista administrador
            self.setupUi(self)
            self.show()


def adminModificar():
    #Instancia de la ventana
    return MainWindow()


def startModificarAdministration():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
