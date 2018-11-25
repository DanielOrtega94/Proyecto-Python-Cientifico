import obspy
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader
import os
import funciones as f

'''
t1 = obspy.UTCDateTime("2018-08-18T00:00:00")
t2 = obspy.UTCDateTime("2018-08-21T00:00:00")
magnitud = 5

datos = f.pedir_datos(t1, t2, magnitud)

for element in datos:
    print(element["event_descriptions"][0].text,element.preferred_magnitude()["mag"])
    #print(element.__dict__)
'''
directorio = "D:/Daniel/Documents/GitHub/Proyecto-Python/qt/datos/CENTRAL EAST PACIFIC RISE2018-11-12/waveforms"

archivos = f.cargar_waveforms(directorio)
print(type(archivos))
# for element in archivos:
# 	print(element)
print(archivos[0].__dict__["stats"].network,archivos[0].__dict__["stats"].station)


#print(archivos[0].__dict__.network,archivos[0].__dict__['station'])
