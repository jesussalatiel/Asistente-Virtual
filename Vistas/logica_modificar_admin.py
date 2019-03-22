from Vistas.vista_modificar_admin import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, id):
            #QtWidgets.QMainWindow.__init__(self)
            super().__init__()
            self.id_root = id
            #Cargamos los componentes correpondientes de la vista administrador
            self.setupUi(self)
            self.buildWindows()
            self.pushButton.clicked.connect(self.modifyRoot)
            self.pushButton_2.clicked.connect(self.cancelRoot)
            self.pushButton_3.clicked.connect(self.saveRoot)
            self.show()

    def buildWindows(self):
        self.label.setText('<html><head/><body><p><img src={}></p></body></html>'.format('./a.jpg'))
        self.setWindowTitle("Modificar Administrador")
        self.pushButton.setText('Cambiar')
        self.pushButton_2.setText('Cancelar')
        self.pushButton_3.setText('Guardar')
        

    def modifyRoot(self):
        print('Modificar')

    def cancelRoot(self):
        print('Cancelar')

    def saveRoot(self):
        print(self.lineEdit.text())
        print(self.lineEdit_2.text())
        print(self.lineEdit_3.text())
    

def adminModificar(id_root=0):
    #Instancia de la ventana
    return MainWindow(id_root)


def startModificarAdministration():
    app = QtWidgets.QApplication([])
    window = MainWindow(0)
    window.show()
    app.exec_()
