from Vistas.vista_modificar_invitado import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import Vistas.database as db
import Vistas.logica_conocidos 

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, id_invitado):
            #QtWidgets.QMainWindow.__init__(self)
            super().__init__()
            #Cargamos los componentes correpondientes de la vista administrador
            self.setupUi(self)
            self._id_invitado = id_invitado
            self.show()
            self.pushButton.clicked.connect(self.modifyKnow)
            self.pushButton_2.clicked.connect(self.cancel)
            self.buildWindows()
            self.status = False
            
    #Construimos la ventana principal de la ventana modificacion
    def buildWindows(self):
        self.setWindowTitle('Modificacion de Usuario')
        data = db.dataKnownId(self._id_invitado)
        self.lineEdit.setText(data['name'])
        self.lineEdit_2.setText(data['email']) 
            
    #Metodo para modificar los datos de usuarios
    def modifyKnow(self):
        #Mensaje de confirmacion para atualizar registro
        if (len(self.lineEdit.text()) <= 0 or len(self.lineEdit_2.text()) <= 0):
            QMessageBox.warning(self, "Campos Vacios",
                                "Faltan campos por completar")
        else:        
            buttonReply = QMessageBox.warning(
                self, 'Modificacion de Usuario', "Esta seguro de modificar el usuario", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                if (db.updateUserId(self._id_invitado, self.lineEdit.text(), self.lineEdit_2.text())) == True:
                    #Cerramos la ventana de actualizar
                    self.close()
                    #Imprimimos mensaje de actualizacion exitosa
                    QMessageBox.information(self, 'Modificacion de Usuario ',
                                            'Operacion Exitosa')
            
    #Cerrar Ventana
    def cancel(self):
        self.close() 
        #Regresamos a la ventana anterior
        self.next = Vistas.logica_conocidos.known()
    
    #Control del evento cerrar que es mostrado en la ventana
    def closeEvent(self, event):
        self.cancel()
        
#Instancia de la ventana para abrir en otra vista
def modifyKnown(id_invitado):
    return MainWindow(id_invitado)

#Ejecucion de todos los Widgets de la ventana
def startModifyKnown(id_invitado):
    app = QtWidgets.QApplication([])
    window = MainWindow(id_invitado)
    window.show()
    app.exec_()
