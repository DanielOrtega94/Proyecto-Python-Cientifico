import obspy
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader


client = Client("IRIS")
t1 = obspy.UTCDateTime("2018-08-18T00:00:00")
t2 = obspy.UTCDateTime("2018-08-21T00:00:00")
cat = client.get_events(starttime=t1, endtime=t2, minmagnitude=7)
i = 0
for elemento in cat:
    print(i, elemento)
    i += 1

numero = int(input("seleccion un evento"))

evento = cat[numero]
origen =  cat[numero].origins
print(type(origen))
# mdl = MassDownloader()


### cambiar de pantalla 