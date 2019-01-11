from Vistas.vista_administracion import * 
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
            self.windowsAdministration()
            self.pushButton.clicked.connect(self.prueba)
            self.formatTable()

    def formatTable(self):
        #Titulo de la ventana
        self.setWindowTitle("Ventana de Administrador")
        #Nombre de los botones
        self.pushButton.setText('Modificar')
        self.pushButton_2.setText('Eliminar')
        self.pushButton_3.setText('Notificar')
        self.pushButton_4.setText('4')
        
        #Especificamos columnas y filas que tendra la tabla
        columnas = 5
        #Bloqueamos la fila para que no pueda ser editada por el usuario
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        #Metodos para seleccionar la fila completa
        self.tableWidget.setSelectionBehavior(
            QtWidgets.QTableWidget.SelectRows)
        # Usar seleccion simple, una fila a la vez
        self.tableWidget.setSelectionMode(
            QtWidgets.QTableWidget.SingleSelection)
        #Especificamos el numero de columnas
        self.tableWidget.setColumnCount(columnas)
        #Iniciamos filas en 0
        self.tableWidget.setRowCount(0)
        #Iteramos en los datos para mostrar los registros de cada columna

        for i, data in enumerate(db.dataRootAll()):
            #Aumentamos las filas segun la cantidad de registros
            self.tableWidget.insertRow(i)
            #Imprimimos los datos de cada columna
            self.tableWidget.setItem(
                i, 0, QtWidgets.QTableWidgetItem(str(data['_id'])))
            self.tableWidget.setItem(
                i, 1, QtWidgets.QTableWidgetItem(str(data['name'])))
            self.tableWidget.setItem(
                i, 2, QtWidgets.QTableWidgetItem(str(data['email'])))
            self.tableWidget.setItem(
                i, 3, QtWidgets.QTableWidgetItem(str(data['id_anterior'])))
        #Cerramos la conexion a la base de datos
        db.closeConection()

    def windowsAdministration(self):
        #Titulo de la ventana
        self.setWindowTitle("Ventana de Administracion")
        self.pushButton.setText('1')
        self.pushButton_2.setText('2')
        self.pushButton_3.setText('3')
        self.pushButton_4.setText('4')

    def prueba(self):
        print("pruebas")
        
def admnistration():
    #Instancia de la ventana
    return MainWindow()


def startAdministration():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
