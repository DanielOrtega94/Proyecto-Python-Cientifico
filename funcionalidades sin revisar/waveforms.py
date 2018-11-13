
# coding: utf-8

# In[ ]:


# extraer muchos datos, con amplia cobertura azimutal
import obspy
from obspy.clients.fdsn.mass_downloader import CircularDomain,     Restrictions, MassDownloader
# este es el tiempo del evento MW 8.2 de Fiji
origin_time = obspy.UTCDateTime(2018, 8, 19, 0, 19, 40)

# Circular domain around the epicenter. This will download all data between
# 70 and 90 degrees distance from the epicenter. This module also offers
# rectangular and global domains. More complex domains can be defined by
# inheriting from the Domain class.
domain = CircularDomain(latitude=-18.1125, longitude=-178.1536,
                        minradius=64.0, maxradius=180.0)

restrictions = Restrictions(
    # Get data from 5 minutes before the event to one hour after the
    # event. This defines the temporal bounds of the waveform data.
    starttime=origin_time - 60,
    endtime=origin_time + 3600,
    # You might not want to deal with gaps in the data. If this setting is
    # True, any trace with a gap/overlap will be discarded.
    reject_channels_with_gaps=True,
    # And you might only want waveforms that have data for at least 95 % of
    # the requested time span. Any trace that is shorter than 95 % of the
    # desired total duration will be discarded.
    minimum_length=0.95,
    # No two stations should be closer than 10 km to each other. This is
    # useful to for example filter out stations that are part of different
    # networks but at the same physical station. Settings this option to
    # zero or None will disable that filtering.
    minimum_interstation_distance_in_m=10E3,
    # Only HH or BH channels. If a station has HH channels, those will be
    # downloaded, otherwise the BH. Nothing will be downloaded if it has
    # neither. You can add more/less patterns if you like.
    #channel_priorities=["HH[Z]", "BH[Z]"],
    # Location codes are arbitrary and there is no rule as to which
    # location is best. Same logic as for the previous setting.
    #location_priorities=["", "00", "10"]
    sanitize=True,
    location="00",
    channel="BHZ")


# No specified providers will result in all known ones being queried.
# queremos datos de IRIS asi que ponemos IRIS jeje
mdl = MassDownloader(providers=['IRIS'])
# The data will be downloaded to the ``./waveforms/`` and ``./stations/``
# folders with automatically chosen file names.
mdl.download(domain, restrictions, mseed_storage="waveformsfiji",
             stationxml_storage="stationsfiji")


# In[1]:

# leer los sismogramas bajados, removerles la respuesta del instrumento, filtrarlos y
# obtener su distancia y azimuth
import obspy
from obspy import read, read_inventory
from obspy.geodetics.base import calc_vincenty_inverse, locations2degrees
from obspy.taup.tau import TauPyModel
import os

origin_time = obspy.UTCDateTime(2018, 8, 19, 0, 19, 40)  # el tiempo del origen
epic = [-17.77, -177.80]  # epicentro del terremoto (CMT HARVARD)
source_depth = 558.6
# leemos todas las formas de onda bajadas con read
st = read("waveformsfiji/*.mseed")
# cargamos una lista con todos los datos de estaciones
XML = os.listdir("stationsfiji")
# datos ordenados alfabéticamente... la fcn de arriba no lo hace
XML = sorted(XML)
c = 0
# print(XML)
# un filtro para frecuencias muy altas y bajas
pre_filt = [0.001, 0.005, 10, 20]
dist = []
az = []
baz = []
canal = []
great_circle = []
arrivals = []
taup = TauPyModel()
for resp in XML:
    print(resp)  # para cachar donde pueda cagar el script
    # leemos la info del instrumento
    inv = read_inventory("stationsfiji/" + str(resp))
    datachannel = inv.get_contents()
    channel = datachannel['channels']  # extraer el canal correspondiente
    # sacamos las coordenadas del canal  para t=tfiji
    datacoor = inv.get_coordinates(channel[0], origin_time)
    coords = [datacoor['latitude'], datacoor[
        'longitude'], datacoor['local_depth']]
    # CALCULAR DISTANCIA Y AZIMUTHS EVENTO-ESTACION
    [disti, azi, bazi] = calc_vincenty_inverse(
        epic[0], epic[1], coords[0], coords[1])
    greatcirc = locations2degrees(epic[0], epic[1], coords[0], coords[1])
    # Arriv=taup.get_travel_times(source_depth_in_km=source_depth,distance_in_degree=greatcirc,phase_list=['P'],\
    #                      receiver_depth_in_km=coords[2])
    # arrivals.append(Arriv)

    # lol=TauPyModel.get_travel_times(source_depth_in_km=141,distance_in_degree=44,phase_list='P',receiver_depth_in_km=0.0)

    # guardar todo en listas (quizá  en pandas se vería mejor?)
    dist.append(disti)
    az.append(azi)
    baz.append(bazi)
    canal.append(channel[0])
    # remover respuesta del instrumento
    st[c].remove_response(inventory=inv, pre_filt=pre_filt,
                          output="VEL", plot=False)
    # aplicar un lowpass
    st[c].filter('lowpass', freq=0.2, corners=2, zerophase=True)
    c += 1


# In[70]:


# ahora creamos los sismogramas sintéticos
import obspy
from obspy.clients.syngine import Client
client = Client()
cmtsol = "GCMT:201808190019A"  # solucion cmt del evento
origin_time = obspy.UTCDateTime(2018, 8, 19, 0, 19, 40)  # el tiempo del origen
# definimos la variable sint, no se como hacerlo correr en el loop abajo
# de otra manera
tiniciales = []
tfinales = []
sint = client.get_waveforms(model='ak135f_5s', network='BK', station='CMB', eventid=cmtsol,
                                  locationcode='00', units='velocity', starttime="P-30", endtime="P+30")
tiniciales.append(sint[-1].stats.starttime)
tfinales.append(sint[-1].stats.endtime)
trsint = sint[0]
for elemento in XML[1:]:
    print(elemento)
    aux = elemento.split('.')
    network = aux[0]
    estacion = aux[1]

    # ignoramos los sismogramas que no llegue la Onda P "en teoría"
    try:
        sint += client.get_waveforms(model='ak135f_5s', network=network, station=estacion, eventid=cmtsol,
                                     units='velocity', starttime="P-30", endtime="P+30", locationcode='00')
        tiniciales.append(sint[-1].stats.starttime)
        tfinales.append(sint[-1].stats.endtime)

    except:
        pass


trsint = sint[0:-1:3]
print(trsint)


# In[108]:
# hay estaciones bajadas a las cuales no les llega la onda P (teoricamente),
# esta parte es para encontrar las estaciones a las cuales le llega, y
# usarlas despues

netsyn = []
stasyn = []
netreal = []
stareal = []
for elemento in trsint:
    netsyn.append(elemento.stats.network)
    stasyn.append(elemento.stats.station)
# print(st[0].stats.st)
for elemento in st:
    netreal.append(elemento.stats.network)
    stareal.append(elemento.stats.station)
# print(len(netreal))
print(stasyn)
print("xd\n")
print(stareal)
stfinal = []
# obtenemos los indices de las estaciones útiles
for i in range(len(trsint)):
    for j in range(len(st)):
        if stareal[j] == stasyn[i]:
            stfinal.append(j)

print(stfinal)
print("xd\n")
print(stasyn)


# In[190]:


from obspy import Stream, Trace
from operator import itemgetter

sismosreales = Stream()
azimutsreales = []
distanciasreales = []
print(sismosreales)
for i in range(len(stfinal)):
    sismosreales.append(st[stfinal[i]])
    azimutsreales.append(az[stfinal[i]])
    distanciasreales.append(dist[stfinal[i]])

print(sismosreales)
print(trsint)


# In[ ]:
# guardamos la data en formato mseed pq se esta pegando mucho esta wea
import numpy as np
import os
import shutil
with open('tiempos.txt', 'w') as out_file:
    for i in range(len(tiniciales) - 1):
        out_string = ""
        out_string += sismosreales[i].id
        out_string += " "
        out_string += str(tiniciales[i])
        out_string += " "
        out_string += str(tfinales[i])
        out_string += " "
        out_string += str(azimutsreales[i])
        out_string += "\n"
        out_file.write(out_string)

shutil.rmtree('sismogramas_reales')
shutil.rmtree('sismogramas_sinteticos')
os.mkdir('sismogramas_reales')
os.mkdir('sismogramas_sinteticos')
for traza in sismosreales:
    traza.write('sismogramas_reales/' + traza.stats.network +
                '.' + traza.stats.station + 'BHZ.mseed', format='MSEED')

for traza in trsint:
    traza.write('sismogramas_sinteticos/' + traza.stats.network +
                '.' + traza.stats.station + 'MXZ.mseed', format='MSEED')


# SOLO QUEDA PLOTEAR Y COMPARAR!
# crear los vectores tiempo que captan solo la onda P
# t_new1=np.arange(0,st_new[0].stats.npts/st_new[0].stats.sampling_rate,st_new[0].stats.delta)
# tnew=[]
# for traza in sismosreales:
#    taux=np.arange(0,traza.stats.npts/traza.stats.saompling_rate,traza.stats.delta)
#    tnew.append(taux)
#


# In[62]:
#
#
# aux=XML[1].split('.')
# D=sint[0:-1:3]
#
#
# In[174]:
#
#
# sismosreales[0]
#
#
# In[ ]:
#
#
#import obspy
#from obspy.geodetics.base import calc_vincenty_inverse
# print(inv)
#origin_time = obspy.UTCDateTime(2018, 8, 19, 0, 19, 40)
# event_coordinates=[-17.77,-177.80]
# datacont=inv.get_contents()
# channel=datacont['channels']
# print(data['channels'])
# staloc=[data['latitude'],data['longitude']] ## 34.666985,-116.177467
# [dist,az,baz]=calc_vincenty_inverse(event_coordinates[0],event_coordinates[1],staloc[0],staloc[1])
# print(dist);print(az);print(baz)
#
#
# In[100]:
#
#
# print(c)
# print(inv)
# print(st[218])
# st[c].remove_response(inventory=inv,pre_filt=pre_filt,output="VEL",plot=False)
# print(channel[0])
# datacoor=inv.get_coordinates(channel[0],origin_time)
# print(st[13],st[1])
#
#
# In[49]:
#
#
# try:
#    print ("Hello World")
# except:
#    print ("this is an error message")
#
#
# In[65]:
#
#
# ahora creamos los sismogramas sintéticos
#import obspy
#from obspy.clients.syngine import Client
# client=Client()
# cmtsol="GCMT:201808190019A" ## solucion cmt del evento
# origin_time = obspy.UTCDateTime(2018, 8, 19, 0, 19, 40) ## el tiempo del origen
# definimos la variable sint, no se como hacerlo correr en el loop abajo de otra manera
#tiniciales=[]; tfinales=[]
# sint=client.get_waveforms(model='ak135f_5s',network='BK',station='CMB',eventid=cmtsol,
#                                  locationcode='00',units='velocity',starttime="P-30",endtime="P+30")
# tiniciales.append(sint[-1].stats.starttime);tfinales.append(sint[-1].stats.endtime)
# trsint=sint[0]
# for elemento in XML[1:]:
#        print(elemento)
#        aux=elemento.split('.')
#        network=aux[0];estacion=aux[1]
#        try:
#            sint+=client.get_waveforms(model='ak135f_5s',network=network,station=estacion,eventid=cmtsol,
#                                   units='velocity',starttime="P-30",endtime="P+30",locationcode='00')
#        except:
#            pass
#        tiniciales.append(sint[0].stats.starttime);tfinales.append(sint[0].stats.endtime)
#
#
#
#
# trsint=sint[0:-1:3]
# print(trsint)
