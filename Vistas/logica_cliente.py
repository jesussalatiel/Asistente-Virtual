from Vistas.vista_cliente import *
import datetime
from PyQt5.QtCore import QTimer
import re
from PyQt5.QtWidgets import QMessageBox
from pynput import keyboard
import threading
import pyaudio
import wave
import Vistas.database as db 
import os

class Windows(QtWidgets.QMainWindow, Ui_MainWindow):

   def path_image(self, path):   
        self.label_2.setText("<html><head/><body><p><img src={}></p></body></html>".format(path))
        self.image = path
        
   
   def date(self):
        day = "Fecha: {}".format(str(datetime.datetime.now()).split('.')[0])
        self.label_3.setText(day)
        
   def cancel(self):
       self.close() 
          
   def save_data(self):
        name, email, note = self.lineEdit_2.text(), self.lineEdit_3.text(), self.textEdit.toPlainText()
        if  not name and not email:
          QMessageBox.warning(self, "Notificación de Mensaje", "Algun campo requerido no esta completo.")
        else:
          if (re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', email.lower())):
               if (self.start_speak == True): 
                    recibo = str(db.safeData(name, email, note, self.image, 'Audio', self.PATH +
                                             name+'_'+((str(self.image.split('/')[4]).split('.')[0])+'.mp3')))
                    self.saveAudio(str((self.image.split('/')[4]).split('.')[0]))
                    #Notificamos que el mensaje se guardo con exito
                    QMessageBox.information(
                        self, 'Notificacion de Mensaje  ', "El mensaje de voz se ha notificado con exito\nNumero de registro: {}\nMuchas Gracias!".format(recibo))
                    #Quitamos la pantalla de dejar mensaje, aveces por este comando Truena el programa debido a un bug del codigo de Qt
                    #self.statusBar().showMessage('Audio Guardado.')  
                    print('Audio Guardado') 
                    self.cancel()
               #Verificamos que el campo donde escriba el usuario tenga al menos 2 letras para notificar que es mensaje     
               elif (len(note) > 1):                    
                    recibo =(db.safeData(name, email, note, self.image, 'Text', None))
                    QMessageBox.information(
                        self, 'Notificacion de Mensaje  ', "El mensaje se ha notificado con exito\nNumero de registro: {}\nMuchas Gracias!".format(recibo))
                    self.cancel()
               elif(len(note)<=0) and self.start_speak == False:
                    QMessageBox.warning(self, "Notificación de Mensaje", "Faltan campos por rellenar.")
          else:
               QMessageBox.warning(self, "Correo Invalido", "Correo Electronico Invalido")
        
   
   def on_press(self, key):       
        try:
            if key == keyboard.Key.f1:
               self.i+=1
               self.start_speak = True
               #Notificamos que esta grabando un audio, aveces por este comando truena el programa debido a un bug del mismo QT
               #self.statusBar().showMessage('Grabando Audio.')
               print('Grabando Audio')
               #print('Frame: {}, status: {}'.format(self.i, self.start_speak))
               data = self.stream.read(self.CHUNK)
               self.frames.append(data)  
        except AttributeError:
            print('Se producio un error')
                
   def on_release(self, key):
        if key == keyboard.Key.esc:           
           return False

   def saveAudio(self,name):
       self.stream.stop_stream()
       self.stream.close()
       self.p.terminate()
       self.wf = wave.open(self.PATH+self.lineEdit_2.text()+'_'+name+'.mp3', 'wb')
       self.wf.setnchannels(self.CHANNELS)
       self.wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
       self.wf.setframerate(self.RATE)
       self.wf.writeframes(b''.join(self.frames))
       self.wf.close()
       self.start_speak = False

   def escuchar(self):
        try:
          with keyboard.Listener(on_press=self.on_press,  on_release=self.on_release) as self.listener:
               self.listener.join()       
        except:
             print()

   def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        #Armando la interfaz de usuario 
        #Establecemos la fecha en el formulario
        self.date()
        #Variables Globales
        self.start_speak = False
        self.icon = QtGui.QIcon()
        self.image = '' 
        ##Grabar
        self.CHUNK = 1500
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        #self.RECORD_SECONDS = 10
        self.PATH = './CNN/database/Usuarios_Audios/'
        os.makedirs(self.PATH, exist_ok=True)
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.stream = self.p.open(format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    frames_per_buffer=self.CHUNK)
        
        #Titulo de la ventana
        self.setWindowTitle("Bienvenido desea dejar su mensaje")
        self.textEdit.setPlaceholderText('Escriba su mensajes ó \nMantenga presionado f1 para grabar audio')
        ####Hilos para escuchar el evento de teclado
        hilo2 = threading.Thread(target = self.escuchar)
        self.i=0
        self.listener = None
        hilo2.start()
        #Activamos los eventos de los botones
        self.pushButton.clicked.connect(self.save_data)
        self.pushButton_2.clicked.connect(self.cancel)     
        
       

#Metodo de ejecucion del programa
def startCliente(image):
     app = QtWidgets.QApplication([])
     window = Windows()  
     window.path_image(image)      
     window.show()
     app.exec_()

#Metodo con el cual se ejecuta toda la clase y puede ser llamado por otras clases
def mainCliente(image):
     hilo1 = threading.Thread(target = startCliente(image))
     hilo1.start()
     
     
