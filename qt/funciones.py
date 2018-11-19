import obspy
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader
import os
from obspy import read, read_inventory, UTCDateTime
from obspy.geodetics.base import calc_vincenty_inverse, locations2degrees
from obspy.taup.tau import TauPyModel
from PyQt5 import QtCore, QtGui, QtWidgets


# funcion encargada de retonar el nombre de los datos, que se encuentran
# disponibles a descargar, datos una fecha de inicio, una fecha de termino
# y una magnitud
def pedir_datos(t1, t2, magnitud):
    client = Client("IRIS")
    cat = client.get_events(starttime=t1, endtime=t2, minmagnitude=magnitud)
    return cat

# dado un indice, y un array de waveforms, seleecionamos un evento para
# ser descargados, donde de los eventos, descargamos las estaciones y las
# waveforms, la descarga de los datos se realiza en carpetas
# diferenciables, para poder facilitar el posterior uso, y manipulacion de
# datos


def descargar_datos(cat, numero):
    client = Client("IRIS")
    evento = cat[numero]
    nombre_evento = evento.event_descriptions[0].text
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
    try:
        mdl.download(domain, restrictions, mseed_storage=n_carpeta_w,
                     stationxml_storage=n_carpeta_s)
    except:
        return 0

# intentamos cargar el directorio de las waveforms, si falla se muestra un
# mensaje
def cargar_waveforms(directorio):
        # cargamos las carpetas asi, pero luego en la interfaz sera automatico
    ruta_w = directorio
    ruta_w = ruta_w + "/*.mseed"
    # print(ruta_w)
    try:
        st = read(ruta_w)
        return st
    except:
        print("AAAAAAAAAAA")

# intentamos cargar el directorio de las estaciones, si falla se muestra un
# mensjae
def cargar_stations(directorio):
    ruta_w = directorio
    ruta_w = ruta_w
    XML = os.listdir(ruta_w)
    XML = sorted(XML)
    return XML


# removemos la respuesta del instrumentos a los sismogramas
def remover_respuesta(directorio, XML, st):
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

    directorio = directorio.replace("waveforms", "info.txt")
    archivo = open(directorio)
    array = []
    for element in archivo:
        array.append(element.replace("\n", ""))
    lat_e = float(array[0])
    lon_e = float(array[1])
    time = UTCDateTime(array[2])
    directorio = directorio.replace("info.txt", "stations")
    # print(directorio)
    os.chdir(directorio)

    for resp in XML:
        print(resp)
        inv = read_inventory(str(resp))
        datachannel = inv.get_contents()
        channel = datachannel['channels']
        datacoor = inv.get_coordinates(channel[0], time)
        coords = [datacoor['latitude'], datacoor[
            'longitude'], datacoor['local_depth']]
        [disti, azi, bazi] = calc_vincenty_inverse(
            lat_e, lon_e, coords[0], coords[1])
        greatcirc = locations2degrees(lat_e, lon_e, coords[0], coords[1])
        dist.append(disti)
        az.append(azi)
        baz.append(bazi)
        canal.append(channel[0])
        bandera = True
        i = 0
        for element in inv.get_response(inv.get_contents()["channels"][0], time).__dict__['response_stages']:
            if (type(element) is obspy.core.inventory.response.ResponseStage):
                i += 1
            if(i > 1):
                bandera = False
        if(bandera):
            st[c].remove_response(
                inventory=inv, pre_filt=pre_filt, output="VEL", plot=False)
        c += 1


# remmovemos el periodo P a los simogramas
def filtro_periodo_P(directorio, st):
    c = 0
    pre_filt = [0.001, 0.005, 10, 20]
    dist = []
    az = []
    baz = []
    canal = []
    great_circle = []
    arrivals = []
    taup = TauPyModel()
    os.chdir(ruta_w)
    directorio = directorio.replace("waveforms", "info.txt")
    archivo = open(directorio)
    array = []
    for element in archivo:
        array.append(element.replace("\n", ""))
    lat_e = float(array[0])
    lon_e = float(array[1])
    time = UTCDateTime(array[2])
    directorio = directorio.replace("info.txt", "stations")
    # print(directorio)
    os.chdir(directorio)

    for resp in XML:
        print(resp)
        inv = read_inventory(str(resp))
        datachannel = inv.get_contents()
        channel = datachannel['channels']
        datacoor = inv.get_coordinates(channel[0], time)
        coords = [datacoor['latitude'], datacoor[
            'longitude'], datacoor['local_depth']]
        [disti, azi, bazi] = calc_vincenty_inverse(
            lat_e, lon_e, coords[0], coords[1])
        greatcirc = locations2degrees(lat_e, lon_e, coords[0], coords[1])
        dist.append(disti)
        az.append(azi)
        baz.append(bazi)
        canal.append(channel[0])
        bandera = True
        i = 0
        for element in inv.get_response(inv.get_contents()["channels"][0], time).__dict__['response_stages']:
            if (type(element) is obspy.core.inventory.response.ResponseStage):
                i += 1
                if(i > 1):
                    bandera = False
        if(bandera):
            st[c].filter('lowpass', freq=0.2, corners=2, zerophase=True)
        c += 1
