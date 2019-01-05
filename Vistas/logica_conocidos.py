from Vistas.vista_conocidos import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import Vistas.database as db

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
            #QtWidgets.QMainWindow.__init__(self)
            super().__init__()
            #Cargamos los componentes correpondientes de la vista administrador
            self.setupUi(self)
            self.show()
            self.windowsKnown()
            self.pushButton.clicked.connect(self.prueba)


    def windowsKnown(self):
        #Titulo de la ventana
        self.setWindowTitle("Ventana de Conocidos")
        self.pushButton.setText('1')
        self.pushButton_2.setText('2')
        self.pushButton_3.setText('3')
        self.pushButton_4.setText('4')
    
    def prueba(self):
        print("pruebas")

def known():
    #Instancia de la ventana
    return MainWindow()


def startKnown():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
