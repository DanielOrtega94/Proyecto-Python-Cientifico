import obspy
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader
import os
import funciones as f


t1 = obspy.UTCDateTime("2018-08-18T00:00:00")
t2 = obspy.UTCDateTime("2018-08-21T00:00:00")
magnitud = 5
