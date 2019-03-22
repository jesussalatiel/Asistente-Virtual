from Vistas.vista_administracion import * 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import Vistas.database as db
import Vistas.logica_modificar_admin as modificarRoot
import Vistas.logica_agenda as agenda

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
            #QtWidgets.QMainWindow.__init__(self)
            super().__init__()
            #Cargamos los componentes correpondientes de la vista administrador
            self.setupUi(self)
            self.show()
            self.pushButton.clicked.connect(self.modifyRegister)
            self.pushButton_2.clicked.connect(self.deleteRegister)
            self.pushButton_3.clicked.connect(self.notifyRegister)
            self.pushButton_4.clicked.connect(self.sendRegister)
            self.formatTable()

    def formatTable(self):
        #Titulo de la ventana
        self.setWindowTitle("Ventana de Administrador")
        #Nombre de los botones
        self.pushButton.setText('Modificar')
        self.pushButton_2.setText('Eliminar')
        self.pushButton_3.setText('Notificar')
        self.pushButton_4.setText('C.Notificacion')
        
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
                i, 3, QtWidgets.QTableWidgetItem(str('Password')))
        #Cerramos la conexion a la base de datos
        db.closeConection()

    def getID(self, propiedad=0 ):
        try:
            id = self.tableWidget.selectedItems()
            return(id[propiedad].text())
        except:
            return None
            #Lanzamos excepcion en caso de que el usuario no seleccione ningun elemento de la tabla
            #Abrimos de nuevo la ventana
            #self.show()
            #Mandamos un mensaje de error
            #QMessageBox.warning(self, "Notificacion de error",
             #                   "Ningun campo seleccionado")
            

    def modifyRegister(self):
        if self.getID(0) == None:
                QMessageBox.warning(self, "Notificacion de error",
                                 "Ningun campo seleccionado")
        else:
            self.next = modificarRoot.adminModificar(self.getID(0))

    def deleteRegister(self):
        buttonReply = QMessageBox.warning(
            self, 'Eliminacion de Registro', "Esta seguro de eliminar el registro\n{}".format(self.getID(1)), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            if (db.deleteRoot(self.getID(0))== True):
                QMessageBox.information(self, 'Eliminacion de Recordatorio ',
                                        'Eliminacion Exitosa')
                #Recargamos la tabla para ver los cambios de la eliminacion
                self.formatTable()

    def notifyRegister(self):
        print('Notificar {}'.format(self.getID(1)))

    def sendRegister(self):
        print('Abrir Agenda {}'.format(self.getID()))
        self.next = agenda.agenda()

def admnistration():
    #Instancia de la ventana
    return MainWindow()


def startAdministration():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
