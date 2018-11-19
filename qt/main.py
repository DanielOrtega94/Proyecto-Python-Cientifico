import sys
from PyQt5 import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.uic import *
from pyqtgraph import QtGui
from PyQt5.QtCore import QObject, pyqtSignal
# from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
import funciones as f
# import matplotlib as plt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# plt.use("Qt5Agg")
from matplotlib import rcParams
from matplotlib.figure import Figure
rcParams['font.size'] = 9
import numpy as np
import random
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

# variables


# definimos una clase para crear una nueva ventana de dialogo
class DescargaDatos(QtGui.QDialog):
    # constructor de la clase en el, seleccionamos la interfaz a que deseamos
    # que sea mostrada, luego debemos conectar los elementos de las interfazs
    # a los metodos

    def __init__(self):
        super(DescargaDatos, self).__init__()
        self.ui = loadUi('interfaz/descarga_datos.ui', self)
        fecha = QtCore.QDate.currentDate()
        # dejamos un valor predeterminado, que corresponde a la fecha actual
        self.ui.fecha_termino_edit.setDate(fecha)
        self.ui.fecha_inicio_edit.setDate(fecha)
        # al pinchar el boton se ejecuta el meotodos
        self.datos_Button.clicked.connect(self.enviar_datos)
        # deja un valor predeterminado que corresponde a 5
        self.ui.magnitud_edit.setText("5")

    # realizamos una llamada al metodo descargar_datos datos, cuando se
    # seleeciona un elemento en la lista, previamente cargados por
    # enviar_datos
    def print_info(self):
        numero = self.ui.descargar_listWidget.row(
            self.ui.descargar_listWidget.currentItem())
        try:
            f.descargar_datos(self.datos, numero)
            QtGui.QMessageBox.information(
                self, " ", "Datos descargados exitosamente")
        except:
            QtGui.QMessageBox.information(
                self, " ", "No se encontraron registros para los datos seleccionados")

        self.done(0)

    # llamamos al metodo enviar_datos, para descargar la informacion asociado
    # a los datos y cargarlos en una lista, para luego poder ser seleecionados
    def enviar_datos(self):
        temp_var = self.ui.fecha_inicio_edit.date()
        fecha_inicio = temp_var.toPyDate()
        temp_var = self.ui.fecha_termino_edit.date()
        fecha_termino = temp_var.toPyDate()
        magnitud = int(self.ui.magnitud_edit.text())
        self.datos = f.pedir_datos(fecha_inicio, fecha_termino, magnitud)
        print(self.datos)
        for element in self.datos:
            string = element["event_descriptions"][0].text + \
                " " + str(element.preferred_magnitude()["mag"])
            self.ui.descargar_listWidget.addItem(string)
        self.ui.descargar_listWidget.currentItemChanged.connect(
            self.print_info)
        # clickeado = self.ui.descargar_listWidget.itemClicked.connect(self.ui.descargar_listWidget.listClicked)
        # print(clickeado)


# Ventana de dialogo para seleccionar el evento que queremos graficar
class SeleccionarDatos(QtGui.QDialog):

    # cargamos lista de datos, cargados en el programa, para luego ser
    # retornado el indice escogido, para ser graficado en la interfaz
    # principal del programa
    def __init__(self, waveforms):
        super(SeleccionarDatos, self).__init__()
        self.ui = loadUi('interfaz/seleccionar.ui', self)
        self.waveforms = waveforms
        for element in self.waveforms:
            string = element.__dict__["stats"].network + \
                " " + element.__dict__["stats"].station
            self.ui.indice_listWidget.addItem(string)
        self.seleccionar_Button.clicked.connect(self.print_info)

    # funcion que retona el numero seleccionado, en la lista
    def print_info(self):
        self.numero = self.ui.indice_listWidget.row(
            self.ui.indice_listWidget.currentItem())
        self.done(self.numero)

# ventana principal de la aplicacion se define los metodos y el espacio
# para realizar graficos


class MainWindow(QtGui.QMainWindow):

    # asociamos eventos a apretar los botones, que corresponden a llamadas de
    # funciones
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = loadUi('interfaz/main_windows.ui', self)
        self.m = PlotCanvas(self, width=5, height=4)
        self.m.setGeometry(QtCore.QRect(60, 50, 501, 471))
        self.descargar_Button.clicked.connect(self.executeDescargaDatos)
        self.cargar_estaciones_Button.clicked.connect(self.path_estaciones)
        self.cargar_waveforms_Button.clicked.connect(self.path_waveforms)
        self.remover_respuesta_Button.clicked.connect(self.remover_respuesta)
        self.filtrar_ondap_Button.clicked.connect(self.remover_respuesta)
        self.graficar_Button.clicked.connect(self.executeSeleccionarDatos)
        self.waveforms = ""
        self.estaciones = ""

        # metodo que llama a un instancia de DescargaDatos, y muestra la
        # pantalla, la ejecuccion del metodo exec_(), permite retonar valores
        # de los dialogos
    def executeDescargaDatos(self):
        descarga_datos_windows = DescargaDatos()
        descarga_datos_windows.exec_()
        # pasar datos de un dialog a otro
        # print(descarga_datos_windows.magnitud_edit.text())

        # metodo que llama a un instancia de SeleccionarDatos, y muestra la
        # pantalla, la ejecuccion del metodo exec_(), permite retonar valores
        # de los dialogos
    def executeSeleccionarDatos(self):
        if (type(self.waveforms) is not type(" ")):
            seleccionar_datos_windows = SeleccionarDatos(self.waveforms)
            seleccionar_datos_windows.exec_()
            # recibimos valor de qdialog
            self.indice_array = seleccionar_datos_windows.numero
            self.graficar(self.indice_array)
            self.m.plot(self.waveforms[0])
        else:
            QtGui.QMessageBox.information(
                self, "Error ", "Seleecione carpeta waveforms")

    # cargamos una interfaz, para seleccionar el una carpeta, donde se
    # encuentran almacenadas las estaciones, para luego ser cargadas
    def path_estaciones(self):
        self.file_estaciones = str(QtGui.QFileDialog.getExistingDirectory(
            self, "Seleccione estaciones"))
        if self.file_estaciones:
            self.estaciones = f.cargar_stations(self.file_estaciones)
            # print(self.estaciones)
            if(np.size(self.estaciones) == 0):
                QtGui.QMessageBox.information(
                    self, "Error ", "Seleecione carpeta estaciones")
            else:
                QtGui.QMessageBox.information(
                    self, "Exito", "Archivos cargados correctamente")

   # cargamos una interfaz, para seleccionar el una carpeta, donde se
   # encuentran almacenadas las waveforms para luego ser cargadas
    def path_waveforms(self):
        self.file_waveforms = str(QtGui.QFileDialog.getExistingDirectory(
            self, "Seleccione waveforms"))
        if self.file_waveforms:
            # print(self.file_estaciones)
            self.waveforms = f.cargar_waveforms(self.file_waveforms)
            # print(self.waveforms)
            if(np.size(self.waveforms) == 0):
                QtGui.QMessageBox.information(
                    self, "Error ", "Seleecione carpeta waveforms")
            else:
                QtGui.QMessageBox.information(
                    self, "Exito", "Archivos cargados correctamente")

        # funcion que realiza los checks necesarios para llamar al metodo
        # remover_respuesta, si existen archivos cargados, nos permite llamar a
        # la funcion, de otra manera, nos indicara que debemos cargar los
        # archivos
    def remover_respuesta(self):
        if(type(self.waveforms) is type(" ") or type(self.estaciones) is type(" ")):
            QtGui.QMessageBox.information(
                self, "Error ", "Primero cargue los datos")
        else:
            f.remover_respuesta(self.file_waveforms,
                                self.estaciones, self.waveforms)
            QtGui.QMessageBox.information(
                self, "Exito", "Operacion realizada correctamente")
        # funcion que realiza los checks necesarios para llamar al metodo
        # periodo_P, si existen archivos cargados, nos permite llamar a
        # la funcion, de otra manera, nos indicara que debemos cargar los
        # archivos

    def periodo_P(self):
        # print(self.file_waveforms, self.estaciones)
        if(type(self.waveforms) is type(" ") or type(self.estaciones) is type(" ")):
            QtGui.QMessageBox.information(
                self, "Error ", "Primero cargue los datos")
        else:
            f.filtro_periodo_P(self.file_waveforms,
                               self.estaciones, self.waveforms)
            QtGui.QMessageBox.information(
                self, "Exito", "Operacion realizada correctamente")

        # funcion que realiza los checks necesarios para llamar al metodo
        # graficar, si existen archivos cargados, nos permite llamar a
        # la funcion y se actualiza el grafico, de otra manera, nos indicara que debemos cargar los
        # archivos
    def graficar(self, numero):
        if(type(self.waveforms) is type(" ")):
            QtGui.QMessageBox.information(
                self, "Error ", "Primero cargue los datos")
        else:
            self.m.plot(self.waveforms[numero])
            QtGui.QMessageBox.information(
                self, " ", "Datos graficos exitosamente")


# clase definida, para definir un lugar donde se pueda graficar en la interfaz
class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(
            self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    # funcion para actualizar el grafico, ademas si se quieren definir
    # distintos estilos de graficos se puede modificar aqui, agregando o
    # eliminando parametros
    def plot(self, st):
        tr = st
        print(tr)
        ax = self.figure.add_subplot(111)
        ax.plot(tr.times("matplotlib"), tr.data, "b-")
        ax.xaxis_date()
        self.figure.autofmt_xdate()
        self.draw()


# llama a la ejecuccion de la ventana principal dando inicio a la aplicaicon
app = QtGui.QApplication(sys.argv)
widget = MainWindow()
widget.show()
sys.exit(app.exec_())
