from Vistas.vista_administrador import *
from PyQt5 import QtCore, QtGui, QtWidgets
import Vistas.database as db
import Vistas.logica_nota as verNota
from PyQt5.QtWidgets import QMessageBox


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        #QtWidgets.QMainWindow.__init__(self)
        super().__init__()
        #Cargamos los componentes correpondientes de la vista administrador
        self.setupUi(self)
        self.show()
        #Creamos el formato de la tabla
        self.formatTable()
        #Evento del boton ver
        self.pushButton.clicked.connect(self.tableItemChanged)

    def formatTable(self):
        #Titulo de la ventana
        self.setWindowTitle("Ventana de Administrador")
        #Especificamos columnas y filas que tendra la tabla
        columnas = 8
        #Bloqueamos la fila para que no pueda ser editada por el usuario
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        #Metodos para seleccionar la fila completa
        self.tableWidget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        # Usar seleccion simple, una fila a la vez
        self.tableWidget.setSelectionMode(QtWidgets.QTableWidget.SingleSelection)
        #Especificamos el numero de columnas
        self.tableWidget.setColumnCount(columnas)
        #Iniciamos filas en 0
        self.tableWidget.setRowCount(0)    
        #Iteramos en los datos para mostrar los registros de cada columna 
        for i, data in enumerate(db.findAllNote()):
            #Aumentamos las filas segun la cantidad de registros
            self.tableWidget.insertRow(i)
            #Imprimimos los datos de cada columna
            for x in range(columnas):
                self.tableWidget.setItem(i, x, QtWidgets.QTableWidgetItem(str(data[db.keysList()[x]])))
        #Cerramos la conexion a la base de datos
        db.closeConection()
        
    #Metodo encargado de obtener el id del campo seleccionado en la tabla       
    def tableItemChanged(self):
        #Seleccionamos solo el id del elemento seleccionado
        id = self.tableWidget.selectedItems()
        self.close()
        #Pasamos el id de la nota que se desea ver a la segunda ventana llamada "Second" y hacemos visible la ventana de Nota
        self.next = verNota.secondWindows(id[0].text())
        
        
#Instanciamos la aplicacion para que podamos avanzar y atrazar en las ventanas
def other():
    #Instancia de la ventana
    return MainWindow()


def startAdmin():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


