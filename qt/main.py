import sys
from PyQt5 import *
from PyQt5.uic import *
from pyqtgraph import QtGui
from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
import funciones as f
import numpy as np

# variables


class DescargaDatos(QtGui.QDialog):

    def __init__(self):
        super(DescargaDatos, self).__init__()

        self.ui = loadUi('interfaz/descarga_datos.ui', self)

        fecha = QtCore.QDate.currentDate()
        self.ui.fecha_termino_edit.setDate(fecha)
        self.ui.fecha_inicio_edit.setDate(fecha)

        self.datos_Button.clicked.connect(self.enviar_datos)
        self.ui.magnitud_edit.setText("5")

    def print_info(self):
        # print(self.ui.descargar_listWidget.currentItem().text())
        numero = self.ui.descargar_listWidget.row(
            self.ui.descargar_listWidget.currentItem())
        QtGui.QMessageBox.information(
            self, " ", "Datos descargados exitosamente")
        # f.descargar_datos(self.datos,numero)

    def enviar_datos(self):

        temp_var = self.ui.fecha_inicio_edit.date()
        fecha_inicio = temp_var.toPyDate()

        temp_var = self.ui.fecha_termino_edit.date()
        fecha_termino = temp_var.toPyDate()

        magnitud = int(self.ui.magnitud_edit.text())

        # self.ui.evento_comboBox.addItem("prueba")
        self.datos = f.pedir_datos(fecha_inicio, fecha_termino, magnitud)
        print(self.datos)
        # self.ui.evento_comboBox.addItem(element)
        for element in self.datos:
            string = element["event_descriptions"][0].text + \
                " " + str(element.preferred_magnitude()["mag"])
            self.ui.descargar_listWidget.addItem(string)

            #.currentRow()
        self.ui.descargar_listWidget.currentItemChanged.connect(
            self.print_info)
        #clickeado = self.ui.descargar_listWidget.itemClicked.connect(self.ui.descargar_listWidget.listClicked)
        # print(clickeado)


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = loadUi('interfaz/main_windows.ui', self)
        self.descargar_Button.clicked.connect(self.executeDescargaDatos)
        self.cargar_estaciones_Button.clicked.connect(self.path_estaciones)
        self.cargar_waveforms_Button.clicked.connect(self.path_waveforms)

        self.remover_respuesta_Button.clicked.connect(self.remover_respuesta)
        self.filtrar_ondap_Button.clicked.connect(self.remover_respuesta)

    def executeDescargaDatos(self):
        descarga_datos_windows = DescargaDatos()
        descarga_datos_windows.exec_()
        # pasar datos de un dialog a otro
        print(descarga_datos_windows.magnitud_edit.text())

    def path_estaciones(self):
        # xml
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

               # st
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

        # necesita waveforms
    def remover_respuesta(self):
        #print(self.file_waveforms, self.estaciones)
        try:
            f.remover_respuesta(self.file_waveforms,
                                self.estaciones, self.waveforms)
            QtGui.QMessageBox.information(
                self, "Exito", "Operacion realizada correctamente")
        except:
            QtGui.QMessageBox.information(
                self, "Error ", "Ha sucedido algo inesperado")

    def periodo_P():
        #print(self.file_waveforms, self.estaciones)
        try:
            f.filtro_periodo_P(self.file_waveforms,
                               self.estaciones, self.waveforms)
            QtGui.QMessageBox.information(
                self, "Exito", "Operacion realizada correctamente")
        except:
            QtGui.QMessageBox.information(
                self, "Error ", "Ha sucedido algo inesperado")

app = QtGui.QApplication(sys.argv)
widget = MainWindow()
widget.show()
sys.exit(app.exec_())
