import sys
from PyQt5 import *
from PyQt5.uic import *
from pyqtgraph import QtGui
from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
import funciones as f


# variables


class DescargaDatos(QtGui.QDialog):

    def __init__(self):
        super(DescargaDatos, self).__init__()

        self.ui = loadUi('interfaz/descarga_datos.ui', self)

        fecha = QtCore.QDate.currentDate()
        self.ui.fecha_termino_edit.setDate(fecha)
        self.datos_Button.clicked.connect(self.enviar_datos)
        self.ui.magnitud_edit.setText("5")

    def enviar_datos(self):

        temp_var = self.ui.fecha_inicio_edit.date()
        fecha_inicio = temp_var.toPyDate()

        temp_var = self.ui.fecha_termino_edit.date()
        fecha_termino = temp_var.toPyDate()

        magnitud = int(self.ui.magnitud_edit.text())

        self.ui.evento_comboBox.addItem("prueba")
        datos = f.pedir_datos(fecha_inicio, fecha_termino, magnitud)
        print(datos)
        for element in datos:
            self.ui.evento_comboBox.addItem(element)


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = loadUi('interfaz/main_windows.ui', self)
        self.descargar_Button.clicked.connect(self.executeDescargaDatos)
        self.cargar_Button.clicked.connect(self.openFileNameDialog)

    def executeDescargaDatos(self):
        descarga_datos_windows = DescargaDatos()
        descarga_datos_windows.exec_()

    def openFileNameDialog(self):
        options = QtGui.QFileDialog.Options()
        options |= QtGui.QFileDialog.DontUseNativeDialog
        fileName, _ = QtGui.QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)


app = QtGui.QApplication(sys.argv)
widget = MainWindow()
widget.show()
sys.exit(app.exec_())
