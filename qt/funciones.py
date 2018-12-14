import folium
import obspy
import os
import webbrowser
import pandas as pd 
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from obspy import UTCDateTime
from obspy import read
from obspy import read_inventory
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.mass_downloader import CircularDomain
from obspy.clients.fdsn.mass_downloader import MassDownloader
from obspy.clients.fdsn.mass_downloader import Restrictions
from obspy.geodetics.base import calc_vincenty_inverse
from obspy.geodetics.base import locations2degrees
from obspy.taup.tau import TauPyModel

# funcion encargada de retonar el nombre de los datos, que se encuentran
# disponibles a descargar, datos una fecha de inicio, una fecha de termino
# y una magnitud

def pedir_datos(csv,t1,t2):
    soluciones_fechas = csv[t1 < csv.fecha_evento]
    soluciones_fechas = soluciones_fechas[soluciones_fechas.fecha_evento < t2]
    soluciones_fechas["lat_cmt"] = np.around(soluciones_fechas["lat_cmt"], decimals=2)
    soluciones_fechas["lon_cmt"] = np.around(soluciones_fechas["lon_cmt"], decimals=2)
    return soluciones_fechas


# def pedir_datos(t1, t2, magnitud):
#     client = Client("IRIS")
#     cat = client.get_events(starttime=t1, endtime=t2, minmagnitude=magnitud)
#     return cat

# dado un indice, y un array de waveforms, seleecionamos un evento para
# ser descargados, donde de los eventos, descargamos las estaciones y las
# waveforms, la descarga de los datos se realiza en carpetas
# diferenciables, para poder facilitar el posterior uso, y manipulacion de
# datos


def descargar_datos(cat):
    client = Client("IRIS")
    nombre_evento = cat["region"].values[0]
    fecha_evento = cat["fecha_evento"].values[0]
    nombre_evento = str(nombre_evento + str(fecha_evento))
    lat_e = float(cat["lat_cmt"])
    lon_e = float(cat["lon_cmt"])
    time = cat["tiempo_cmt"].values[0]
    print("f: ",fecha_evento)
    print("t: ",time)
    
    time = str(fecha_evento) +"T" + time
    print(time)
    time = UTCDateTime(time)
    depth = float(cat["depth_cmt"])
    # print(nombre_evento,lat_e,lon_e,time,depth)
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
    archivo.write(str(fecha_evento) + "\n")
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
    os.chdir(directorio)
    # print(directorio)

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


# funcion que carga el mapa que se abre en navegador usando las librerias
# folium y branca
def mapa(directorio, icono):
    # creamos el mapa
    m = folium.Map(tiles='Stamen Terrain', zoom_start=0.5, min_zoom=2)
    # creamos el icono para identificar las estaciones
    fig_icono = folium.features.CustomIcon(icono, icon_size=(14, 14))

    # graficamos las estaciones
    archivos = cargar_stations(directorio)
    os.chdir(directorio)
    for resp in archivos:
        print(resp)
        inv = read_inventory(str(resp))
        nombre = resp.replace(".xml", "")
        latitud = inv[0][0].__dict__["_latitude"]
        longitud = inv[0][0].__dict__["_longitude"]
        #
        # marker = folium.map.Marker([latitud, longitud], icon=fig_icono,popup=nombre)
        # m.add_children(marker)
        folium.Marker(location=[latitud, longitud],
                      popup=nombre).add_to(m)
        m.add_child(folium.LatLngPopup())

    # cargamos la informacion del terremoto
    directorio = directorio.replace("stations", "info.txt")
    archivo = open(directorio)
    array = []
    for element in archivo:
        array.append(element.replace("\n", ""))
    lat_e = float(array[0])
    lon_e = float(array[1])
    folium.Marker(location=[lat_e, lon_e], popup='Lugar Evento',
                  icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
    directorio = directorio.replace("info.txt", "")
    print(directorio)
    os.chdir(directorio)
    m.save('index.html')
    webbrowser.open("index.html")

    # leer
