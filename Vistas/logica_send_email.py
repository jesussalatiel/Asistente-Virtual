from Vistas.vista_email import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import Vistas.database as db
import smtplib
import smtplib
from email.mime.text import MIMEText


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, id_invitado):
            super().__init__()
            #Contraseñas
            self._id_invitado = id_invitado
            self.email_administrator = ''
            self.password_administrator = ''
            self.email_from = 'Asistente Virtual'
            #Comprobamos conexion
            try:
                self.mailServer = smtplib.SMTP('smtp.gmail.com', 587)
                self.mailServer.ehlo()
                self.mailServer.starttls()
                self.mailServer.ehlo()
                self.mailServer.login(self.email_administrator, self.password_administrator)
                #Titulo de la ventana
                data = db.dataInvitado(self._id_invitado)
                self.setWindowTitle("Enviar correo a {}".format(data[0]))
                #Cargamos los componentes correpondientes de la vista administrador
                self.setupUi(self)
                self.show()
                #Evento del boton ver
                self.pushButton.clicked.connect(self.btnSendEmail)
                self.pushButton_2.clicked.connect(self.cancel)
            except:
                QMessageBox.warning(self, 'Envio de Email ', 'No existe conexion a internet.')
                
                


    def buildEmail(self,text, destinatario):
        # Construimos el mensaje simple
        id = db.dataInvitado(self._id_invitado)
        self.mensaje = MIMEText("""{}\nNumero de contestacion: {}""".format(text, id[3]))
        self.mensaje['From'] = self.email_from
        self.mensaje['To'] = destinatario
        self.mensaje['Subject'] = "Mensaje del Administrador"
        return self.mensaje
    
    def prepareEmail(self,mensaje, email_destinatario):
        # Envio del mensaje
        self.mailServer.sendmail(self.email_administrator,
                        email_destinatario,
                        mensaje.as_string())
        return True
    
    def sendEmail(self, texto, email_destinatario):
        status =self.prepareEmail(self.buildEmail(texto, email_destinatario), email_destinatario)
        return status

    def btnSendEmail(self):
        name = db.dataInvitado(self._id_invitado)
        if (len(self.plainTextEdit.toPlainText()) >= 1 or (len(self.lineEdit.text()) >= 5)):
            buttonReply = QMessageBox.information(
                self, 'Envio de Email', "Esta seguro de enviar el correo", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                if (self.sendEmail(self.plainTextEdit.toPlainText(), str(name[1]))) == True:
                    QMessageBox.information(self, 'Envio de Email','Se envio el correo con exito !')
                    self.close()
        else:
            QMessageBox.warning(self, 'Envio de Email ',
                                    'Faltan campos por completar')
        
    def cancel(self):
        self.close()

def windowsEmail(id):
    return MainWindow(id)

def startAdministration(id):
    app = QtWidgets.QApplication([])
    window = MainWindow(id)
    window.show()
    app.exec_()



