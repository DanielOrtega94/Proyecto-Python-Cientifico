import folium
import matplotlib.pyplot as plt
import numpy as np
import obspy
import os
import os
import pandas as pd
import webbrowser

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from matplotlib import pylab
# from mpl_toolkits.basemap import Basemap
from obspy import UTCDateTime
from obspy import read
from obspy import read_inventory
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.mass_downloader import CircularDomain
from obspy.clients.fdsn.mass_downloader import MassDownloader
from obspy.clients.fdsn.mass_downloader import Restrictions
from obspy.clients.syngine import Client
from obspy.imaging.beachball import beach

# funcion encargada de retonar el nombre de los datos, que se encuentran
# disponibles a descargar, datos una fecha de inicio, una fecha de termino
# y una magnitud


def pedir_datos(csv, t1, t2,magnitud):
    soluciones_fechas = csv[t1 < csv.fecha_evento]
    soluciones_fechas = soluciones_fechas[soluciones_fechas.fecha_evento < t2]
    soluciones_fechas = soluciones_fechas[soluciones_fechas.Mw_cmt>= magnitud]
    soluciones_fechas["lat_cmt"] = np.around(
        soluciones_fechas["lat_cmt"], decimals=2)
    soluciones_fechas["lon_cmt"] = np.around(
        soluciones_fechas["lon_cmt"], decimals=2)
    return soluciones_fechas


def descargar_datos(cat, radiomin, radiomax,start_time,end_time,dist_esta):
    nombre_evento = cat["region"].values[0]
    fecha_evento = cat["fecha_evento"].values[0]
    magnitud = cat["Mw_cmt"].values[0]
    nombre_evento = str(nombre_evento + " " +
                        str(fecha_evento) + " " + str(magnitud)) # + str(canal)
    lat_e = cat["lat_cmt"].values[0]
    lon_e = cat["lon_cmt"].values[0]
    time = cat["tiempo_cmt"].values[0]
    time = str(fecha_evento) + "T" + time
    time = UTCDateTime(time)
    depth = cat["depth_cmt"].values[0]
    print("nombre ",nombre_evento,"lat: ",lat_e,"lon: ",lon_e,"time ",time,"depth ",depth,"minradius ",radiomin,"maxradius", radiomax)
    # radiomin = 50.0
    # radiomax = 90.0
    client = Client("IRIS")
    domain = CircularDomain(latitude=lat_e, longitude=lon_e,
                            minradius=radiomin, maxradius=radiomax)
    mdl = MassDownloader(providers=["IRIS"])
    restrictions = Restrictions(starttime=time - start_time, endtime=time + end_time,
                                chunklength_in_sec=86400, location="00", channel="BHZ", reject_channels_with_gaps=True,
                                minimum_length=0.95, minimum_interstation_distance_in_m=dist_esta,
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
        # try:
        mdl.download(domain, restrictions, mseed_storage=n_carpeta_w,
                     stationxml_storage=n_carpeta_s)
        # except:
            # return 0
    except:
        return -100
        

# intentamos cargar el directorio de las waveforms, si falla se muestra un
# mensaje


def carga_datos(directorio,ceseve):
    try:
        os.chdir(directorio)
        ruta_wave = directorio + "/waveforms"
        ruta_station =  directorio + "/stations"
        estaciones,bulk,fallas= cargar_stations(ruta_station,ceseve,directorio)
        waveforms = cargar_waveforms(ruta_wave,fallas)
    except:
        return [],[],[],[]
    return estaciones,bulk,fallas,waveforms

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

def cargar_sintetico(ruta_wave):
    os.chdir(directorio)
    archivos = sorted(os.listdir(directorio))
    sintetico =[]
    for element in archivos:
        sintetico.append(read(element))
    return sintetico


# removemos la respuesta del instrumentos a los sismogramas
def remover_respuesta(st,inv,pre_filt,output_1):
    stream = []
    for wave,inventory in zip(st,inv):
        wave=wave.remove_response(inventory=inventory, pre_filt=pre_filt, output=output_1, plot=False)
        wave.taper
        wave.detrend("constant")
        wave.detrend("linear")
        stream.append(wave)
    return stream #,unidad

# remmovemos el periodo P a los simogramas
def filtro(tipo, st,freq_):
    corners = 2
    stream = []
    if(tipo == "lowpass"):
        for element in st:
            element = element.filter('lowpass', freq=freq_, corners=2, zerophase=True)
            stream.append(element)
        # st = st.filter('lowpass', freq=freq_, corners=2, zerophase=True)
    elif(tipo == "highpass"):
        # st =  st.filter('highpass', freq=freq_, corners=2, zerophase=True)
        for element in st:
            element = element.filter('highpass', freq=freq_, corners=2, zerophase=True)
            stream.append(element)
    elif(tipo == "bandpass"):
        for element in st:
            element =  element.filter('bandpass', freqmin=freq_[0],freqmax=freq_[1], corners=2, zerophase=True)
            stream.append(element)
        # st =  st.filter('bandpass', freqmin=freq_[0],freqmax=freq_[1], corners=2, zerophase=True)
    return stream 

def generar_sintetico(ruta_info,ceseve,bulk,output,start,end):
    ruta_info = ruta_info + "/info.txt"
    archivo =  open(ruta_info)
    archivos = []
    for element in archivo:
        archivos.append(element.strip())
    ceseve= ceseve[ceseve["id_evento"] == archivos[0]]
    client = Client()
    codigo = archivos[0]
    # print(codigo)
    codigo = "GCMT:" + codigo[1:]
    print(codigo)
    if(output == "VEL"):
        output = 'velocity'
    elif(output == "DISP"):
        output = "displacement"
    elif(output == "ACC"):
        output = "acceleration"
    sint_teo = client.get_waveforms_bulk(model='ak135f_5s',eventid=codigo,
            units=output,starttime="P-"+start,endtime="P+"+end,components = 'Z' ,bulk = bulk)
    parametros = ['ak135f_5s',archivos[0],"P-"+start,"P+"+end,output]
    return sint_teo,parametros



# funcion que carga el mapa que se abre en navegador usando las librerias
# folium y branca
def mapa(estaciones,ceseve,ruta_info):
    # creamos el mapa
    m = folium.Map(tiles='Stamen Terrain', zoom_start=0.5, min_zoom=2)
    # creamos el icono para identificar las estaciones
    # fig_icono = folium.features.CustomIcon(icono, icon_size=(14, 14))

    # graficamos las estaciones
    for estacion in estaciones:
        lista = estacion.get_contents()['channels'][0].split(".")
        nombre =  lista[0] +"."+lista[1]
        latitud = estacion[0][0].__dict__["_latitude"]
        longitud = estacion[0][0].__dict__["_longitude"]
        folium.Marker(location=[latitud, longitud],
                      popup=nombre).add_to(m)#nombre
        m.add_child(folium.LatLngPopup())

    # cargamos la informacion del terremoto
    directorio = ruta_info + "/info.txt"
    archivo =  open(directorio)
    archivos = []
    for element in archivo:
        archivos.append(element.strip())
    ceseve= ceseve[ceseve["id_evento"] == archivos[0]]
    lon_e = ceseve["lon_cmt"].values[0]
    lat_e = ceseve["lat_cmt"].values[0]
    folium.Marker(location=[lat_e, lon_e], popup='Lugar Evento',
                  icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
    os.chdir(ruta_info)
    m.save('index.html')
    webbrowser.open("index.html")

def guardar_trabajo_sintetico(streams,nombre,ruta_principal,ruta_guardar):
    nombre = nombre.replace(ruta_principal.replace("\\","/")+"/datos/","")
    # print(ruta_guardar)
    os.chdir(ruta_guardar)

    i = 0
    for stream in streams:
        nuevo= nombre+str(i)+ ".mseed"
        stream.write(nuevo)  
        i+=1


def guardar_trabajo(streams,nombre,ruta_principal,ruta_guardar):

    nombre = nombre.replace(ruta_principal.replace("\\","/")+"/datos/","")
    os.chdir(ruta_guardar)
    i = 0
    for stream in streams:
        nuevo= nombre+str(i)+ ".mseed"
        print(nuevo)
        stream.write(nuevo)  
        i+=1

def mapa_basemap(ceseve,ruta_info):
    ruta_info = ruta_info + "/info.txt"
    archivo =  open(directorio)
    archivos = []
    for element in archivo:
        archivos.append(element.strip())
    ceseve= ceseve[ceseve["id_evento"] == archivos[0]]
    lon_e = ceseve["lon_cmt"].values[0]
    lat_e = ceseve["lat_cmt"].values[0]
    Mrr = ceseve['Mrr'].values[0]
    Mtt = ceseve['Mtt'].values[0]
    Mpp = ceseve['Mpp'].values[0]
    Mrt = ceseve['Mrt'].values[0]
    Mrp = ceseve['Mrp'].values[0]
    Mtp = ceseve['Mtp'].values[0]
    m = Basemap(resolution='c',projection='cyl', area_thresh = 100.0)
    m.bluemarble()
    x,y=m(lon_e,lat_e)
    ax=plt.gca()
    focmec=[Mrr[i],Mtt[i],Mpp[i],Mrt[i],Mrp[i],Mtp[i]]   
    b = beach(focmec, xy=(x[i], y[i]), width=3, linewidth=1)
    b.set_zorder(10)
    ax.add_collection(b)
    plt.show()