import obspy
from obspy import read, read_inventory, UTCDateTime
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
directorio = "D:/Daniel/Documents/GitHub/Proyecto-Python/qt/datos/VENEZUELA2018-11-24/stations"

archivos = f.cargar_stations(directorio)
os.chdir(directorio)
# print(type(archivos))
# print(archivos)

# for resp in archivos:
    
#     inv = read_inventory(str(resp))
#     nombre  = resp.replace(".xml","")
#     print(nombre)
#     print(inv[0][0].__dict__["_latitude"],inv[0][0].__dict__["_longitude"])

#     break


#####################################


# archivos = f.cargar_waveforms(directorio)
# print(archivos[0].__dict__)

# print(type(archivos))
# # for element in archivos:
# # 	print(element)
# print(archivos[0].__dict__["stats"].network,archivos[0].__dict__["stats"].station)


# print(archivos[0].__dict__.network,archivos[0].__dict__['station'])
