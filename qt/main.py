import os
from PyQt5 import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.uic import *
from pyqtgraph import QtGui
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
import funciones as f
# import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# plt.use("Qt5Agg")
from matplotlib import rcParams
from matplotlib.figure import Figure
rcParams['font.size'] = 9
import numpy as np
import pandas as pd
import random
import sys
import shutil
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
        os.chdir(ruta_principal)
        self.ui = loadUi('interfaz/descarga_datos.ui', self)
        ultimo = soluciones_cmt.shape[0] - 1
        # dejamos un valor predeterminado, que corresponde a la fecha actual
        self.ui.fecha_inicio_edit.setDate(soluciones_cmt['fecha_evento'][0])
        self.ui.fecha_termino_edit.setDate(
            soluciones_cmt['fecha_evento'][ultimo])
        # al pinchar el boton se ejecuta el meotodos
        self.datos_Button.clicked.connect(self.enviar_datos)
        self.ui.magnitud_edit.setText("7")
        self.ui.radiomin_Edit.setText("50")
        self.ui.radiomax_lineEdit.setText("90")
        self.ui.start_time_lineEdit.setText("60")
        self.ui.end_time_lineEdit.setText("3600")
        self.ui.dist_esta_lineEdit.setText("1000")

    

        # transformamos los strings a fechas

        # print(type(self.soluciones['fecha_evento']))
        # print(type(self.soluciones['fecha_evento'][0].dt.date))

    # realizamos una llamada al metodo descargar_datos datos, cuando se
    # seleeciona un elemento en la lista, previamente cargados por
    # enviar_datos
    def print_info(self):
        numero = self.ui.descargar_listWidget.row(
            self.ui.descargar_listWidget.currentItem()) 
        numero  = self.a_mostrar[numero]
        # try:s
        # print(self.a_mostrar[numero])
        resultados = soluciones_cmt[soluciones_cmt["Unnamed: 0"] == numero]
        codigo= f.descargar_datos(resultados,self.radiomin,self.radiomax,self.start_time,self.end_time,self.dist_esta)
        if (codigo == -100):
            QtGui.QMessageBox.information(self, "Error", "Datos descargados anteriormente")
        else:
            QtGui.QMessageBox.information(self, "Exito", "Datos descargados exitosamente")
        # except:
        # QtGui.QMessageBox.information(
        # self, " ", "No se encontraron registros para los datos
        # seleccionados")

        self.done(0)

    # llamamos al metodo enviar_datos, para descargar la informacion asociado
    # a los datos y cargarlos en una lista, para luego poder ser seleecionados
    def enviar_datos(self):
        self.ui.descargar_listWidget.clear()
        temp_var = self.ui.fecha_inicio_edit.date()
        fecha_inicio = temp_var.toPyDate()
        temp_var = self.ui.fecha_termino_edit.date()
        fecha_termino = temp_var.toPyDate()
        magnitud = int(self.ui.magnitud_edit.text())
        self.radiomin = int(self.ui.radiomin_Edit.text())
        self.radiomax = int(self.ui.radiomax_lineEdit.text())
        self.start_time = int(self.ui.start_time_lineEdit.text())
        self.end_time = int(self.ui.end_time_lineEdit.text())
        self.dist_esta = int(self.ui.dist_esta_lineEdit.text())


        self.datos = f.pedir_datos(soluciones_cmt, fecha_inicio, fecha_termino,magnitud)
        if(len(self.datos) == 0):
            QtGui.QMessageBox.information(self, "Error", "Busqueda no ha arrojado resultados")
        self.a_mostrar = []
        for i, region, mw, lat, lon in zip(self.datos["Unnamed: 0"], self.datos["region"], self.datos["Mw_cmt"], self.datos["lat_cmt"], self.datos["lon_cmt"]):
            mw = np.around(mw, 2)
            string = str(region) + "  Mw: " + str(mw)
            self.a_mostrar.append(i)
            self.ui.descargar_listWidget.addItem(string)
        self.ui.descargar_listWidget.currentItemChanged.connect(self.print_info)
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
            string = element[0].__dict__["stats"].network + \
                " " + element[0].__dict__["stats"].station
            self.ui.indice_listWidget.addItem(string)
        self.seleccionar_Button.clicked.connect(self.print_info)

    # funcion que retona el numero seleccionado, en la lista
    def print_info(self):
        self.numero = self.ui.indice_listWidget.row(
            self.ui.indice_listWidget.currentItem())
        self.done(self.numero)




class RemoverRespuesta(QtGui.QDialog):

    def __init__(self,wavefoms,stations):
        super(RemoverRespuesta, self).__init__()
        output = ["DISP","VEL","ACC"]
        self.ui = loadUi('interfaz/remover_respuesta.ui', self)
        self.waveforms = wavefoms
        self.estaciones = stations
        self.ui.prefilter_lineEdit.setText("0.001, 0.005, 10, 20")
        self.ui.output_comboBox.addItems(output)
        self.ui.calcular_pushButton.clicked.connect(self.llamada_funcion)

    def llamada_funcion(self):
        prefilter = str(self.ui.prefilter_lineEdit.text()).split(",")
        pre_filter = []
        for element in prefilter:
            pre_filter.append(float(element))
        self.output = str(self.ui.output_comboBox.currentText())
        self.waveforms = f.remover_respuesta(self.waveforms,self.estaciones,pre_filter,self.output)
        self.done(0)



class Periodo(QtGui.QDialog):

    def __init__(self,wavefoms):
        super(Periodo, self).__init__()
        self.ui = loadUi('interfaz/periodo.ui', self)
        self.ui.frecuencias_lineEdit.setText("0.2")
        self.ui.lowpass_radioButton.setChecked(True)
        self.waveforms = wavefoms
        self.ui.calcular_pushButton.clicked.connect(self.llamada_funcion)

    def llamada_funcion(self):
        if(self.ui.lowpass_radioButton.isChecked()):
            tipo = "lowpass"
            frecu = float(self.ui.frecuencias_lineEdit.text())
        elif(self.ui.highpass_radioButton.isChecked()):
            tipo = "highpass"
            frecu = float(self.ui.frecuencias_lineEdit.text())
        elif(self.ui.bandpass_radioButton.isChecked()):
            tipo = "bandpass"
            frecuen = str(self.ui.frecuencias_lineEdit.text()).split(",")
            frecu = []
            for element in frecuen:
                frecu.append(float(element))
        self.waveforms = f.filtro(tipo,self.waveforms,frecu)
        self.done(0)

class SismogramaSintetico(QtGui.QDialog):


    def __init__(self,ruta_info,bulk,output):
        super(SismogramaSintetico, self).__init__()
        self.ui = loadUi('interfaz/sismograma_sintetico.ui', self)
        self.ui.calcular_pushButton.clicked.connect(self.llamada_funcion)
        self.ui.starttime_lineEdit.setText("30")
        self.ui.endtime_lineEdit.setText("30")
        self.ruta_info =ruta_info
        self.bulk=bulk
        self.output=output

    def llamada_funcion(self):
        self.start = str(self.ui.starttime_lineEdit.text())
        self.end = str(self.ui.endtime_lineEdit.text())
        self.sismograma_sintetico,self.parametros_sinteticos = f.generar_sintetico(self.ruta_info,soluciones_cmt,self.bulk,self.output,self.start,self.end)
        self.done(0)


# ventana principal de la aplicacion se define los metodos y el espacio
# para realizar graficos
class MainWindow(QtGui.QMainWindow):

    # asociamos eventos a apretar los botones, que corresponden a llamadas de
    # funciones
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = loadUi('interfaz/main_windows.ui', self)
        # self.m = PlotCanvas(self, width=5, height=4)
        # self.m.setGeometry(QtCore.QRect(60, 50, 501, 471))
        self.descargar_Button.clicked.connect(self.executeDescargaDatos)
        self.graficar_Button.clicked.connect(self.graficar)
        self.remover_respuesta_Button.clicked.connect(self.executeRemoverRespuesta)
        self.filtrar_ondap_Button.clicked.connect(self.executePeriodo)
        self.sismograma_pushButton.clicked.connect(self.executeSismogramaSintetico)
        self.cargar_estaciones_Button.clicked.connect(self.carga_datos)
        self.mapa_Button.clicked.connect(self.graficar_mapa)
        self.limpiar_datos_pushButton.clicked.connect(self.limpiar_valores)
        self.guardar_cambios_pushButton.clicked.connect(self.guardar_trabajo)
        self.sintetico_pushButton.clicked.connect(self.guardar_sintetico)
        self.cargar_waveforms_Button.clicked.connect(self.cargar_waveforms)
        self.cargar_sintetico_Button.clicked.connect(self.cargar_sintetico)
        self.basemap_pushButton.clicked.connect(self.graficar_basemap)
        self.graficar_sintetico_Button.clicked.connect(self.graficar_sintetico)
        # self.cargar_waveforms_Button.clicked.connect(self.graficar_basemap)
        self.waveforms = ""
        self.estaciones = ""

    def graficar_basemap(self):
        f.mapa_basemap(soluciones_cmt,self.file_estaciones)
        print("asd")

    def graficar(self):
        try:
            c=0 
            ruta = str(QtGui.QFileDialog.getExistingDirectory(self, "Seleccione directorio para guardar sismograma"))
            # ruta = self.file_estaciones+"/graficos_normales/"
            os.mkdir(ruta)
            os.chdir(ruta)

            for traza in self.waveforms:
                traza = traza[0]
                fig = plt.figure()
                ax = fig.add_subplot(1, 1, 1)
                ax.plot(traza.times('matplotlib'),traza.data , 'r' , label = 'sis obs')
                plt.title('Formas de onda observadas estacion  ' +traza.id  )
                ax.xaxis_date()
                fig.autofmt_xdate()
                print(ruta)
                plt.savefig(ruta+traza.id+'.'+'{:04}'.format(c+1)+'.png')
                plt.close()
                c+=1
        except:
            QtGui.QMessageBox.information(self, "Error ", "Algo inesperado ha sucedido")


    def graficar_sintetico(self):
        try:
            c=0 
            ruta = str(QtGui.QFileDialog.getExistingDirectory(self, "Seleccione directorio para guardar sismograma"))
            # ruta = self.file_estaciones+"/graficos_sinteticos/"

            os.mkdir(ruta)
            os.chdir(ruta)
            for traza in self.sismograma_sintetico:
                traza = traza
                fig = plt.figure()
                ax = fig.add_subplot(1, 1, 1)
                ax.plot(traza.times('matplotlib'),traza.data , 'r' , label = 'sis obs')
                plt.title('Formas de onda observadas estacion  ' +traza.id  )
                ax.xaxis_date()
                fig.autofmt_xdate()
                print(ruta)
                plt.savefig(ruta+traza.id+'.'+'{:04}'.format(c+1)+'.png')
                plt.close()
                c+=1
        except:
            QtGui.QMessageBox.information(self, "Error ", "Algo inesperado ha sucedido")


    def executeDescargaDatos(self):
        os.chdir(ruta_principal)
        descarga_datos_windows = DescargaDatos()
        descarga_datos_windows.exec_()
        # pasar datos de un dialog a otro
        # print(descarga_datos_windows.magnitud_edit.text())

        # metodo que llama a un instancia de SeleccionarDatos, y muestra la
        # pantalla, la ejecuccion del metodo exec_(), permite retonar valores
        # de los dialogos
    def executeSeleccionarDatos(self):
        # try:
        os.chdir(ruta_principal)
        seleccionar_datos_windows = SeleccionarDatos(self.waveforms)
        seleccionar_datos_windows.exec_()
            # recibimos valor de qdialog
        self.indice_array = seleccionar_datos_windows.numero
        string = self.waveforms[self.indice_array][0].__dict__["stats"].network + \
                " " + self.waveforms[self.indice_array][0].__dict__["stats"].station
        # self.graficar(self.indice_array)
        tr = self.waveforms[self.indice_array][0]
        plt
        ax = self.figure.add_subplot(111)
        ax.plot(tr.times("matplotlib"), tr.data, "b-")
        # ax.tittle(nombre)
        ax.xaxis_date()
        self.figure.autofmt_xdate()
        self.draw()
        plt.show()
        QtGui.QMessageBox.information(self, "Exito ", "Graficado Correctamente")

        # self.m.plot(self.waveforms[self.indice_array],string)
        
        # except:
        #     QtGui.QMessageBox.information(
        #         self, "Error ", "Error al intentar graficar los datos")

    def executeRemoverRespuesta(self):

        try:
            os.chdir(ruta_principal)
            remover_respuesta_windows = RemoverRespuesta(self.waveforms,self.estaciones)
            remover_respuesta_windows.exec_()
            self.waveforms = remover_respuesta_windows.waveforms
            self.output = remover_respuesta_windows.output
            QtGui.QMessageBox.information(self, "Exito", "Operacion realizada correctamente")
        except:
            QtGui.QMessageBox.information(self, "Error ", "Algo inesperado ha sucedido")

    def executePeriodo(self):
        try:
            os.chdir(ruta_principal)
            periodo_windows = Periodo(self.waveforms)
            periodo_windows.exec_()
            self.waveforms = periodo_windows.waveforms
            QtGui.QMessageBox.information(self, "Exito", "Operacion realizada correctamente")
        except:
            QtGui.QMessageBox.information(self, "Error ", "Algo inesperado ha sucedido")

    def executeSismogramaSintetico(self):
        try:
            os.chdir(ruta_principal)
            sismograma_windows = SismogramaSintetico(self.file_estaciones,self.bulk,self.output)
            sismograma_windows.exec_()
            self.sismograma_sintetico = sismograma_windows.sismograma_sintetico
            self.parametros_sinteticos = sismograma_windows.parametros_sinteticos
            self.tiempo_inicio = sismograma_windows.sismograma_sintetico
            self.tiempo_termino = sismograma_windows.sismograma_sintetico
            QtGui.QMessageBox.information(self, "Exito", "Operacion realizada correctamente")
        except:
            QtGui.QMessageBox.information(self, "Error ", "Debe ejecutar remover respuesta primero")


    def guardar_trabajo(self):
        ruta_guardar = str(QtGui.QFileDialog.getExistingDirectory(self, "Seleccione estaciones"))
        try:
            f.guardar_trabajo(self.waveforms, self.file_estaciones,ruta_principal,ruta_guardar)
            QtGui.QMessageBox.information(self, "Exito ", "Datos guardados correctamente")     
        except:
            QtGui.QMessageBox.information(self, "Exito ", "Algo inesperado ha sucedido")
            # print("sadfasdf")

    def  guardar_sintetico(self):
        ruta_guardar = str(QtGui.QFileDialog.getExistingDirectory(self, "Seleccione directorio para guardar sismograma"))
        try:
            f.guardar_trabajo_sintetico(self.sismograma_sintetico, self.file_estaciones,ruta_principal,ruta_guardar)
            print(ruta_guardar)
            os.chdir(ruta_guardar)
            archivo = open("info.txt","w")
            for element in self.parametros_sinteticos:
                archivo.write(element+'\n')
            archivo.close()
            QtGui.QMessageBox.information(self, "Exito ", "Datos guardados correctamente")     
        except:
            QtGui.QMessageBox.information(self, "Error", "Algo inesperado ha sucedido")

    def limpiar_valores(self):
        self.waveforms = " "
        self.estaciones = " "
        self.file_estaciones = ""
        self.estaciones = ""
        self.file_waveforms = ""
        self.waveforms = ""
        self.bulk = ""
        self.sismograma_windows = ""
        QtGui.QMessageBox.information(self, "Exito ", "Datos limpiados correctamente")
   

        # metodo que llama a un instancia de DescargaDatos, y muestra la
        # pantalla, la ejecuccion del metodo exec_(), permite retonar valores
        # de los dialogos
    

    def carga_datos(self):
        os.chdir(ruta_principal)
        self.file_estaciones = str(QtGui.QFileDialog.getExistingDirectory(
            self, "Seleccione carpeta datos"))
        self.estaciones,self.bulk,self.fallas,self.waveforms = f.carga_datos(self.file_estaciones,soluciones_cmt)
        if(np.size(self.estaciones) == 0 or np.size(self.waveforms) == 0):
            QtGui.QMessageBox.information(self, "Error ", "Algo inesperado ha sucedido")
        else:
            QtGui.QMessageBox.information(self, "Exito", "Archivos cargados correctamente")

    def cargar_waveforms(self):
        os.chdir(ruta_principal)
        try:
            ruta_wave = str(QtGui.QFileDialog.getExistingDirectory(self, "Seleccione carpeta con waveforms modificados"))
            # print(ruta_wave)
            self.waveforms = cargar_waveforms(ruta_wave,self.fallas)
        except:
            QtGui.QMessageBox.information(self, "Error ", "Algo inesperado ha sucedido")


    def cargar_sintetico(self):
        os.chdir(ruta_principal)
        try:
            ruta_wave = str(QtGui.QFileDialog.getExistingDirectory(self, "Seleccione carpeta con waveforms modificados"))
            # print(ruta_wave)
            self.waveforms = cargar_sintetico(ruta_wave)
        except:
            QtGui.QMessageBox.information(self, "Error ", "Algo inesperado ha sucedido")


        # funcion que realiza los checks necesarios para llamar al metodo
        # remover_respuesta, si existen archivos cargados, nos permite llamar a
        # la funcion, de otra manera, nos indicara que debemos cargar los
        # archivos

        # funcion que realiza los checks necesarios para llamar al metodo
        # periodo_P, si existen archivos cargados, nos permite llamar a
        # la funcion, de otra manera, nos indicara que debemos cargar los
        # archivos

    def periodo(self):
        # print(self.file_waveforms, self.estaciones)
        if(type(self.waveforms) is type(" ") or type(self.estaciones) is type(" ")):
            QtGui.QMessageBox.information(
                self, "Error ", "Primero cargue los datos")
        else:
            tipo = "bandpass"
            self.waveforms = f.filtro(tipo,self.waveforms)
            QtGui.QMessageBox.information(
                self, "Exito", "Operacion realizada correctamente")

        # funcion que realiza los checks necesarios para llamar al metodo
        # graficar, si existen archivos cargados, nos permite llamar a
        # la funcion y se actualiza el grafico, de otra manera, nos indicara que debemos cargar los
        # archivos
    # def graficar(self, numero):
    #             # if(type(self.waveforms) is type(" ")):
    #     # try:
    #     print(type(self.waveforms[numero]))
    #     self.m.plot(self.waveforms[numero])
    #         # QtGui.QMessageBox.information(
    #             # self, " ", "Datos graficos exitosamente")
    #     # except:
    #     #     QtGui.QMessageBox.information(
    #     #         self, "Error ", "Primero cargue los datos")


    def graficar_mapa(self):
        # ruta = os.getcwd() + "/interfaz/estaciones.png"
        if self.file_estaciones:
            f.mapa(self.estaciones,soluciones_cmt,self.file_estaciones)
        else:
            QtGui.QMessageBox.information(
                self, "Error ", "Cargue waveforms y stations del evento")


# llama a la ejecuccion de la ventana principal dando inicio a la aplicaicon
ruta_principal = os.getcwd()
ruta_soluciones = ruta_principal + "/datos/cmt.csv"
soluciones_cmt = pd.read_csv(ruta_soluciones, low_memory=False)
soluciones_cmt['fecha_evento'] = pd.to_datetime(soluciones_cmt['fecha_evento'])
soluciones_cmt['fecha_evento'] = soluciones_cmt['fecha_evento'].dt.date
app = QtGui.QApplication(sys.argv)
widget = MainWindow()
widget.show()
sys.exit(app.exec_())
