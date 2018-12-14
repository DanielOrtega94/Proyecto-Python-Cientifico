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
        # cargamos los archivos con las soluciones
        ruta = os.getcwd()
        self.soluciones_cmt = ruta + "/datos/cmt.csv"
        self.soluciones = pd.read_csv(self.soluciones_cmt)
        # transformamos los strings a fechas
        self.soluciones['fecha_evento'] = pd.to_datetime(
            self.soluciones['fecha_evento'])
        self.soluciones['fecha_evento'] = self.soluciones[
            'fecha_evento'].dt.date

        # print(type(self.soluciones['fecha_evento']))
        # print(type(self.soluciones['fecha_evento'][0].dt.date))

    # realizamos una llamada al metodo descargar_datos datos, cuando se
    # seleeciona un elemento en la lista, previamente cargados por
    # enviar_datos
    def print_info(self):
        numero = self.ui.descargar_listWidget.row(
            self.ui.descargar_listWidget.currentItem())
        # try:
            # print(self.a_mostrar[numero])
        resultados=self.soluciones[self.soluciones["Unnamed: 0"] == numero]
        f.descargar_datos(resultados)
        QtGui.QMessageBox.information(
                self, " ", "Datos descargados exitosamente")
        # except:
            # QtGui.QMessageBox.information(
                # self, " ", "No se encontraron registros para los datos seleccionados")

        self.done(0)

    # llamamos al metodo enviar_datos, para descargar la informacion asociado
    # a los datos y cargarlos en una lista, para luego poder ser seleecionados
    def enviar_datos(self):
        temp_var = self.ui.fecha_inicio_edit.date()
        fecha_inicio = temp_var.toPyDate()
        temp_var = self.ui.fecha_termino_edit.date()
        fecha_termino = temp_var.toPyDate()
        magnitud = int(self.ui.magnitud_edit.text())

        self.datos = f.pedir_datos(
            self.soluciones, fecha_inicio, fecha_termino)
        # print(self.datos)
        self.a_mostrar = []
        # print(self.datos.columns)
        for i,region, mw, lat, lon in zip(self.datos["Unnamed: 0"],self.datos["region"], self.datos["Mw_cmt"], self.datos["lat_cmt"], self.datos["lon_cmt"]):
            mw = np.around(mw,2)
            string = str(i) + " " + str(region) + "  Mw: " + str(mw) 
            self.a_mostrar.append(i)
            self.ui.descargar_listWidget.addItem(string)
        self.ui.descargar_listWidget.currentItemChanged.connect(
            self.print_info)
        # clickeado = self.ui.descargar_listWidget.itemClicked.connect(self.ui.descargar_listWidget.listClicked)
        # print(clickeado)

