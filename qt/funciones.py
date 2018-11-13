import obspy
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader
import os
from obspy import read, read_inventory, UTCDateTime
from obspy.geodetics.base import calc_vincenty_inverse, locations2degrees
from obspy.taup.tau import TauPyModel


def pedir_datos(t1, t2, magnitud):
    client = Client("IRIS")
    #t1 = obspy.UTCDateTime("2018-08-18T00:00:00")
    #t2 = obspy.UTCDateTime("2018-08-21T00:00:00")
    #magnitud = 7
    cat = client.get_events(starttime=t1, endtime=t2, minmagnitude=magnitud)
    return cat


def descargar_datos(cat, numero):
    #t1 = obspy.UTCDateTime("2018-08-18T00:00:00")
    #t2 = obspy.UTCDateTime("2018-08-21T00:00:00")
    #magnitud = 7
    #cat = client.get_events(starttime=t1, endtime=t2, minmagnitude=magnitud)
    #i = 0
    # for elemento in cat:
    #    print(i, elemento)
    #    i += 1
    #numero = int(input("seleccion un evento"))
    client = Client("IRIS")
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


def cargar_estations(directorio):
        # cargamos las carpetas asi, pero luego en la interfaz sera automatico
    ruta_w = directorio
    ruta_w = ruta_w + "/*.mseed"
    print(ruta_w)
    st = read(ruta_w)
    return st


def remover_respuesta(directorio,st):
    XML = os.listdir(ruta_s)
    XML = sorted(XML)
    c = 0
    # un filtro para frecuencias muy altas y bajas
    pre_filt = [0.001, 0.005, 10, 20]
    dist = []
    az = []
    baz = []
    canal = []
    great_circle = []
    arrivals = []
    taup = TauPyModel()
    ruta_w = ruta_w.replace("waveforms","info.txt")
    archivo = open(ruta_w)
    array =[]
    for element in archivo:
        array.append(element.replace("\n",""))
    lat_e = float(array[0])
    lon_e = float(array[1])
    time = UTCDateTime(array[2])

def filto_perido_P(directorio,st):
    print("asdasd")
