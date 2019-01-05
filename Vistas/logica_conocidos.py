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
            self.pushButton.clicked.connect(self.convertToAdmin)
            self.pushButton_2.clicked.connect(self.deleteKnown)


    def windowsKnown(self):
        #Titulo de la ventana
        self.setWindowTitle("Ventana de Conocidos")
        self.pushButton.setText('Convertir')
        self.pushButton_2.setText('Eliminar')
        self.pushButton_3.setText('3')
        self.pushButton_4.setText('4')
        self.fillTable()
    
    def fillTable(self):
        #Especificamos columnas y filas que tendra la tabla
        columnas = 3
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
        for i, data in enumerate(db.dataKnown()):            
            #Aumentamos las filas segun la cantidad de registros
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(
                i, 0, QtWidgets.QTableWidgetItem(str(data['_id'])))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(data['name'])))
            self.tableWidget.setItem(
                i, 2, QtWidgets.QTableWidgetItem(str(data['id_anterior'])))
        #Cerramos la conexion a la base de datos
        db.closeConection()

    def convertToAdmin(self):
        try:
            #Seleccionamos solo el id del elemento seleccionado
            id = self.tableWidget.selectedItems()
            seleccion = db.saveAdministrator(id[0].text())
            #Preguntamos si realmente quiere convertir el usuario en administrados
            buttonReply = QMessageBox.warning(
                self, 'Convertir en Administrador', "Esta seguro de convertir en administrador", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                #Aseguramos que la operacion se realice con exito
                if seleccion == True:
                    QMessageBox.information(self, 'Convertir en Administrador ',
                                            'Operacion realizada con exito.')
                    #Actualizamos la tabla
                    self.fillTable()
        except:
            #self.show()
            #Mandamos un mensaje de error
            QMessageBox.warning(self, "Notificacion de error",
                                "Ningun campo seleccionado")

    def deleteKnown(self):
        try:
            #Seleccionamos solo el id del elemento seleccionado
            id = self.tableWidget.selectedItems()
            print(id[0].text())
        except:
            print("Error")
#Instancia de la ventana para abrir en otra vista
def known():
    return MainWindow()

#Ejecucion de todos los Widgets de la ventana 
def startKnown():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
