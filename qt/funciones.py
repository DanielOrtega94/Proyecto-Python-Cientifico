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
from obspy.clients.syngine import Client

# funcion encargada de retonar el nombre de los datos, que se encuentran
# disponibles a descargar, datos una fecha de inicio, una fecha de termino
# y una magnitud


def pedir_datos(csv, t1, t2):
    soluciones_fechas = csv[t1 < csv.fecha_evento]
    soluciones_fechas = soluciones_fechas[soluciones_fechas.fecha_evento < t2]
    soluciones_fechas["lat_cmt"] = np.around(
        soluciones_fechas["lat_cmt"], decimals=2)
    soluciones_fechas["lon_cmt"] = np.around(
        soluciones_fechas["lon_cmt"], decimals=2)
    return soluciones_fechas


def descargar_datos(cat, radiomin, radiomax):
    client = Client("IRIS")
    nombre_evento = cat["region"].values[0]
    fecha_evento = cat["fecha_evento"].values[0]
    magnitud = cat["Mw_cmt"].values[0]
    nombre_evento = str(nombre_evento + " " +
                        str(fecha_evento) + " " + str(magnitud)) # + str(canal)
    lat_e = float(cat["lat_cmt"])
    lon_e = float(cat["lon_cmt"])
    time = cat["tiempo_cmt"].values[0]
    time = str(fecha_evento) + "T" + time
    time = UTCDateTime(time)
    depth = float(cat["depth_cmt"])
    # print(nombre_evento,lat_e,lon_e,time,depth)
    radiomin = 50.0
    radiomax = 90.0
    domain = CircularDomain(latitude=lat_e, longitude=lon_e,
                            minradius=radiomin, maxradius=radiomax)
    mdl = MassDownloader(providers=["IRIS"])
    restrictions = Restrictions(starttime=time - 60, endtime=time + 3600,
                                chunklength_in_sec=86400, location="00", channel="BHZ", reject_channels_with_gaps=True,
                                minimum_length=0.95, minimum_interstation_distance_in_m=1000.0,
                                sanitize=True)
    ruta = os.getcwd()
    rutas = "datos/"
    informacion = ruta + "/" + rutas + nombre_evento
    n_carpeta_w = nombre_evento + "/waveforms"
    n_carpeta_s = nombre_evento + "/stations"

    informacion = informacion.replace("/", "\\")
    try:
        os.mkdir(informacion)
        os.chdir(informacion)
        archivo = open("info.txt", "w")
        archivo.write(str(cat["id_evento"].values[0]) + "\n")
        archivo.close()
        os.chdir("..")
        try:
            mdl.download(domain, restrictions, mseed_storage=n_carpeta_w,
                     stationxml_storage=n_carpeta_s)
        except:
            return 0
    except:
        return -100
        

# intentamos cargar el directorio de las waveforms, si falla se muestra un
# mensaje


def cargar_waveforms(directorio,fallas):
    # cargamos las carpetas asi, pero luego en la interfaz sera automatico
    ruta_w = directorio
    os.chdir(directorio)
    archivos = sorted(os.listdir(directorio))
    for estacion in fallas:
        for wave in archivos:
            lista = estacion.get_contents()['channels'][0].split(".")
            nombre =  lista[0] +"."+lista[1]
            if(wave.count(nombre)):
                archivos.remove(wave)
    waveforms = []
    for element in archivos:
        waveforms.append(read(element))
    
    return waveforms
    # except:
    # print("AAAAAAAAAAA")


# intentamos cargar el directorio de las estaciones, si falla se muestra un
# mensjae
def cargar_stations(directorio,ceseve,ruta_info):
    estaciones = []
    fallas = []
    bulk = []
    os.chdir(directorio)
    XML = os.listdir(directorio)
    XML = sorted(XML)
    ruta_info = ruta_info + "/info.txt"
    archivo =  open(ruta_info)
    archivos = []
    for element in archivo:
        archivos.append(element.strip())
    ceseve= ceseve[ceseve["id_evento"] == archivos[0]]
    time = UTCDateTime(str(ceseve["fecha_evento"].values[0])+"T"+ceseve["tiempo_cmt"].values[0])
    for resp in XML:
        # print(resp)
        inv = read_inventory(resp)
        bandera = True
        i = 0
        for element in inv.get_response(inv.get_contents()["channels"][0], time).__dict__['response_stages']:
            if (type(element) is obspy.core.inventory.response.ResponseStage):
                i += 1
            if(i > 1):
                bandera = False
        if(bandera):
            estaciones.append(inv)
            bulk.append([inv.get_contents()['channels'][0].split('.')[0],inv.get_contents()['channels'][0].split('.')[1]])
        else:
            fallas.append(inv)
    return estaciones, bulk,fallas


# removemos la respuesta del instrumentos a los sismogramas
def remover_respuesta(st,inv):
    pre_filt = [0.001, 0.005, 10, 20]
    # output = ["DISP","VEL","ACC"]
    # unidad = uno de los output escogidos 
    for wave,inventory in zip(st,inv):
        wave=wave.remove_response(inventory=inventory, pre_filt=pre_filt, output="VEL", plot=False)
        wave.taper
        wave.detrend("constant")
        wave.detrend("linear")
    return st #,unidad

# remmovemos el periodo P a los simogramas
def filtro(tipo, st):
    corners = 2
    if(tipo == "lowpass"):
        st = st.filter('lowpass', freq=0.2, corners=2, zerophase=True)
    elif(tipo == "highpass"):
        st =  st.filter('highpass', freq=0.2, corners=2, zerophase=True)
    elif(tipo == "bandpass"):
        st =  st.filter('bandpass', freqmin=0.2,freqmax=2, corners=2, zerophase=True)
    return st 

def generar_sintetico(tipo,ruta_info,ceseve,bulk):
    ruta_info = ruta_info + "/info.txt"
    archivo =  open(ruta_info)
    archivos = []
    for element in archivo:
        archivos.append(element.strip())
    ceseve= ceseve[ceseve["id_evento"] == archivos[0]]
    client = Client()
    if(tipo == "basico"):
        sint_teo = client.get_waveforms_bulk(model='ak135f_5s',eventid=archivos[0],
            units='velocity',starttime="P-30",endtime="P+30",components = 'Z' ,bulk = bulk)


    elif(tipo == "custom"):
        tiempo_cmt = ceseve["tiempo_cmt"].values[0]
        lon_cmt = ceseve["lon_cmt"].values[0]
        lat_cmt = ceseve["lat_cmt"].values[0]
        depth_cmt = ceseve["depth_cmt"].values[0]
        exp_cmt  =ceseve["exp_cmt"].values[0]
        Mij_cmt = list(exp_cmt * 10E-7 *np.array([ ceseve["Mrr"].values[0],ceseve["Mtt"].values[0],ceseve["Mpp"].values[0],ceseve["Mrt"].values[0],ceseve["Mrp"].values[0],ceseve["Mtp"].values[0]]))
        st_sint_teo=client.get_waveforms_bulk(model='ak135f_5s',bulk=bulk,
                                   units='velocity',origintime=tiempo_cmt,starttime="P-0",endtime="P+60",
                                   sourcemomenttensor=Mij_cmt,components="Z",
                                   sourcelongitude=lon_cmt,sourcelatitude=lat_cmt,
                                   sourcedepthinmeters= depth_cmt*1000 )
    return sint_teo



# funcion que carga el mapa que se abre en navegador usando las librerias
# folium y branca
def mapa(directorio, icono):
    # creamos el mapa
    m = folium.Map(tiles='Stamen Terrain', zoom_start=0.5, min_zoom=2)
    # creamos el icono para identificar las estaciones
    fig_icono = folium.features.CustomIcon(icono, icon_size=(14, 14))

    # graficamos las estaciones
    XML = os.listdir(directorio)
    archivos = sorted(XML)
    # archivos = cargar_stations(directorio)
    os.chdir(directorio)
    for resp in archivos:
        # print(resp)
        inv = read_inventory(str(resp))
        nombre = resp.replace(".xml", "")
        latitud = inv[0][0].__dict__["_latitude"]
        longitud = inv[0][0].__dict__["_longitude"]
        nombres = [nombre,latitud,longitud]
        # marker = folium.map.Marker([latitud, longitud], icon=fig_icono,popup=nombre)
        # m.add_children(marker)
        folium.Marker(location=[latitud, longitud],
                      popup=nombres).add_to(m)#nombre
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

def filtro():
    print("folium.Marker")
