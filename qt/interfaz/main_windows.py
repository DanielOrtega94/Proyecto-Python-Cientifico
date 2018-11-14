# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_windows.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(590, 40, 160, 151))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.descargar_Button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.descargar_Button.setObjectName("descargar_Button")
        self.verticalLayout.addWidget(self.descargar_Button)
        self.cargar_estaciones_Button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cargar_estaciones_Button.setObjectName("cargar_estaciones_Button")
        self.verticalLayout.addWidget(self.cargar_estaciones_Button)
        self.cargar_waveforms_Button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cargar_waveforms_Button.setObjectName("cargar_waveforms_Button")
        self.verticalLayout.addWidget(self.cargar_waveforms_Button)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(600, 250, 160, 80))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.remover_respuesta_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.remover_respuesta_Button.setObjectName("remover_respuesta_Button")
        self.verticalLayout_2.addWidget(self.remover_respuesta_Button)
        self.filtrar_ondap_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.filtrar_ondap_Button.setObjectName("filtrar_ondap_Button")
        self.verticalLayout_2.addWidget(self.filtrar_ondap_Button)
        self.graficar_Button = QtWidgets.QPushButton(self.centralwidget)
        self.graficar_Button.setGeometry(QtCore.QRect(620, 420, 75, 23))
        self.graficar_Button.setObjectName("graficar_Button")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(590, 10, 121, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(580, 210, 121, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(580, 360, 121, 31))
        self.label_3.setObjectName("label_3")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(60, 50, 501, 471))
        self.graphicsView.setObjectName("graphicsView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.descargar_Button.setText(_translate("MainWindow", "Descargar Datos"))
        self.cargar_estaciones_Button.setText(_translate("MainWindow", "Cargar Estaciones"))
        self.cargar_waveforms_Button.setText(_translate("MainWindow", "Cargar Waveforms"))
        self.remover_respuesta_Button.setText(_translate("MainWindow", "Remover Respuesta"))
        self.filtrar_ondap_Button.setText(_translate("MainWindow", "Filtrar para Onda P"))
        self.graficar_Button.setText(_translate("MainWindow", "Graficar"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">Datos:</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">Análisis:</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">Gráficos:</span></p></body></html>"))

