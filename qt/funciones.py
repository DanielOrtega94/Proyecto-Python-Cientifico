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


def descargar_datos(cat,numero):
    #t1 = obspy.UTCDateTime("2018-08-18T00:00:00")
    #t2 = obspy.UTCDateTime("2018-08-21T00:00:00")
    #magnitud = 7
    #cat = client.get_events(starttime=t1, endtime=t2, minmagnitude=magnitud)
    #i = 0
    #for elemento in cat:
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


