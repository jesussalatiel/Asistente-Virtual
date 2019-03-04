# Asistente Virtual Basado en Vision por Computadora
Implementación de un sistema computacional que funcione como Asistente Virtual basado en Visión por Computadora, haciendo uso de tecnicas de Visión Artificial para adquirir procesar y analizar imagenes del mundo real. Ademas de implementar Redes Neuronales Convolucionales para el reconocimiento de rostros humanos esto para que el sistema pueda identificar a los usuarios propietarios y usuarios visitantes.


## Requisitos de Instalación
- Python 3
- MongoDB
## Descargar los pesos para que pueda funcionar el algoritmo
- [Pesos para la red](https://drive.google.com/file/d/1zX1yBsAhePVNwd0AZ_aikF548l-HFXoC/view?usp=sharing) 
## Proceso de Instalación para Desarrollo 
- Crear un entorno virtual de Python 3 en Windows 10.
```bash
 python -m venv asistente 
```
- Ya creado el entorno procedemos a movernos a la carpeta
```bash
cd asistente
```
- Procedemos a movernos a Scripts para activar el entorno
```bash
cd Scripts 
```
- Activamos el entorno virtual
```bash
activate 
```
- Procedemos a instalar todas las librerias necesarias para el desarrollo y ejecución del programa
```bash
pip install -r /path/requeriments.txt 
```
- Fin de proceso !!

## Ejecución del Software
- Ejecutamos el archivo principal 
```bash
python main.py
```
## Desarrollo de Interfaz Gráfica
[Web de Referencía para el desarrollo de interfaces gráficas con PyQt.](https://medium.com/@hektorprofe/primeros-pasos-en-pyqt-5-y-qt-designer-programas-gr%C3%A1ficos-con-python-6161fba46060)
## Desarrollo de Web (FrontEnd)
- Instalamos React
```bash
npm install -g create-react-app
```
- Nos posicionamos en la carpeta que contiene la parte gráfica de la web
```bash
cd Django-React/frontend/gui
```
- Iniciamos el servidor 
```bash
npm start
```
## Desarollo del Servidor (BackEnd)
- Nos posicionamos en la carpeta que contiene la parte del backend
```bash
cd Django-React/backend/src
```
- Iniciamos el servidor
```bash
python manage.py runserver
```
### Contraseñas del Django
```bash
localhost:8000/admin
```
- user: admin
- pass: admin

### Estoy en proceso de creación del bat para instalación automatico