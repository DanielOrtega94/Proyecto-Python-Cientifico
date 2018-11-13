import obspy
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader
import os


def pedir_datos(t1, t2, magnitud):
    client = Client("IRIS")
    #t1 = obspy.UTCDateTime("2018-08-18T00:00:00")
    #t2 = obspy.UTCDateTime("2018-08-21T00:00:00")
    #magnitud = 7
    cat = client.get_events(starttime=t1, endtime=t2, minmagnitude=magnitud)
    return cat


def descargar_datos():
    client = Client("IRIS")
    #t1 = obspy.UTCDateTime("2018-08-18T00:00:00")
    #t2 = obspy.UTCDateTime("2018-08-21T00:00:00")
    #magnitud = 7
    cat = client.get_events(starttime=t1, endtime=t2, minmagnitude=magnitud)
    i = 0
    for elemento in cat:
        print(i, elemento)
        i += 1
    numero = int(input("seleccion un evento"))
    evento = cat[numero]
    nombre_evento = evento.event_descriptions[0].text

# lista
    origen = cat[numero].origins

    nombre_evento = nombre_evento + \
        str(origen[0].time.year) + "-" + \
        str(origen[0].time.month) + "-" + str(origen[0].time.day)

    lat_e = origen[0].latitude
    lon_e = origen[0].longitude
    time = origen[0].time
    depth = origen[0].depth
    radiomin = 50.0
    radiomax = 90.0

    domain = CircularDomain(latitude=lat_e, longitude=lon_e,
                            minradius=radiomin, maxradius=radiomax)
    mdl = MassDownloader(providers=["IRIS"])

    restrictions = Restrictions(starttime=time - 60, endtime=time + 3600, chunklength_in_sec=86400, location="00", channel="BHZ", reject_channels_with_gaps=True, minimum_length=0.95, minimum_interstation_distance_in_m=1000.0,
                                sanitize=True)

    ruta = os.getcwd()

    rutas = "datos/"
    informacion = ruta + "/" + rutas + nombre_evento
    n_carpeta_w = nombre_evento + "/waveforms"
    n_carpeta_s = nombre_evento + "/stations"

    informacion = informacion.replace("/", "\\")
    os.mkdir(informacion)
    os.chdir(informacion)
    archivo = open("info.txt", "w")
    archivo.write(str(lat_e) + "\n")
    archivo.write(str(lon_e) + "\n")
    archivo.write(str(time) + "\n")
    archivo.close()
    os.chdir("..")
    mdl.download(domain, restrictions, mseed_storage=n_carpeta_w,
                 stationxml_storage=n_carpeta_s)


def abrir(self):
    # Mensaje de advertencia
    msg = QtGui.QMessageBox()  # mensajes de advertencia
    # carga el archivo
    #archivo = QFileDialog.getOpenFileName(None, 'Open file', '.')
    # Se verifica que se cargue de manera correcta la imagen
    try:
        print(archivo)
        #foto = QtGui.QImage(archivo)
        #msg.setText('Archivo cargado correctamente')
        #foto = Image.open(archivo)
        #self.original = foto
        # Tamaño del cuadro de la interfaz
        #self.size = (self.ui.cuadro.width(), self.ui.cuadro.height())
        # Evita que la imagen cambie su tamaño
        #foto.thumbnail(self.size, Image.ANTIALIAS)
        #foto = ImageQt.ImageQt(foto)
        # Se visualiza la imagen
        # self.ui.cuadro.setPixmap(QtGui.QPixmap.fromImage(foto))
        # "self.bandera" Indicador de que la imagen se encuentra en escala de grises o no
        # Se inicializa en 0
        self.bandera = 0
        # En el caso que no cargue de manera correcta
    except:
        msg.setText("Archivo no seleccionado")
        msg.setIcon(QtGui.QMessageBox.Critical)

        # Histograma de la imagen original
        #im_histo = self.original.histogram()
        #self.ui.PlotWidget.axes.plot(range(len(im_histo)), im_histo)
        # self.ui.PlotWidget.draw()
        # Cuadros de aviso
    msg.setWindowTitle("Aviso")
    msg.setStandardButtons(QtGui.QMessageBox.Ok)
    msg.exec_()
