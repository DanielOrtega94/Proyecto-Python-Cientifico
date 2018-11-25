import folium
import os
import webbrowser

from obspy import UTCDateTime
from obspy import read
from obspy import read_inventory
import funciones as f


m = folium.Map(tiles='Stamen Terrain',
               zoom_start=0.5, min_zoom=2)
# zoom_start=2, location=[-45.57299,-72.08139])


directorio = "D:/Daniel/Documents/GitHub/Proyecto-Python/qt/datos/VENEZUELA2018-11-24/stations"
directorio_anterior = "D:/Daniel/Documents/GitHub/Proyecto-Python/qt/datos/VENEZUELA2018-11-24/"
directorio_wave = "D:/Daniel/Documents/GitHub/Proyecto-Python/qt/datos/VENEZUELA2018-11-24/waveforms"
archivos = f.cargar_stations(directorio)
os.chdir(directorio)

archivo = open(directorio_anterior + "info.txt")
array = []
for element in archivo:
    array.append(element.replace("\n", ""))
lat_e = float(array[0])
lon_e = float(array[1])
folium.Marker(location=[lat_e, lon_e], popup='Lugar Evento',
              icon=folium.Icon(color='red', icon='info-sign')).add_to(m)

# icon = folium.features.CustomIcon(icon_url,icon_size=(14, 14))
for resp in archivos:
    # print(resp)
    inv = read_inventory(str(resp))
    nombre = resp.replace(".xml", "")
    latitud = inv[0][0].__dict__["_latitude"]
    longitud = inv[0][0].__dict__["_longitude"]
    folium.Marker(location=[latitud, longitud], popup=nombre).add_to(m)
    # folium.LayerControl(collapsed=False).add_to(m)
    # inv.plot()
    # print(nombre, latitud, longitud)
    m.add_child(folium.LatLngPopup())

os.chdir(directorio_anterior)
m.save('index.html')
webbrowser.open("index.html")
