#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 16:57:51 2018

@author: doctorcasa
"""

## con los datos ya obtenidos y procesados, solo falta  mostrar los resultados
from obspy import read
import obspy
import shutil
import numpy as np
st_reales=read('sismogramas_reales/*.mseed')
st_sintes=read('sismogramas_sinteticos/*.mseed')
print(st_reales)
print(st_sintes)
f=open('tiempos.txt')
lineas=f.read()
linea=lineas.split('\n')
linea.pop()
ID=[]; tinicio=[]; tfinal=[]; azimut=[]
for elemento in linea:
    lista=elemento.split(' ')
    ID.append(lista[0]); tinicio.append(lista[1]) ; tfinal.append(lista[2]); azimut.append(lista[3])   ;

azimutfloat=[]
for elemento in azimut:
    elemento='{:.5}'.format(elemento)
    aux=float(elemento)
    azimutfloat.append(aux)


azimut_orden=np.sort(azimutfloat)
azimut_index=np.argsort(azimutfloat)
    
#%% cortar los sismogramas
origin_time = obspy.UTCDateTime(2018, 8, 19, 0, 19, 40) ## el tiempo del origen)
samprate=4.0
npts=240
c=0
for traza in st_reales:
    traza.interpolate(sampling_rate=samprate,starttime=obspy.UTCDateTime(tinicio[c]),npts=npts)
    c+=1
    

#%% hallar la correlacion cruzada entre los sismogramas
from scipy import signal
from matplotlib import pylab
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import pylab
sism_lag=[]
c=0
for traza in st_reales:
    lageada=np.argmax(signal.correlate(traza.data,st_sintes[c].data))
    new_signal=np.roll(st_sintes[c].data,shift=int(np.ceil(lageada)))
    sism_lag.append(new_signal)
    c+=1

shutil.rmtree('grafs')
os.mkdir('grafs')

numbers=np.arange(1,len(st_reales)+1)
numbers_format=[]
for number in numbers:
    aux='{:04}'.format(number)
    numbers_format.append(aux)
    
    
    
#for i in range(len(st_reales)):
#    plt.figure()
#    plt.plot(st_reales[azimut_index[i]].times() , st_reales[azimut_index[i]].data , 'r' , label='sis_obs')
#    plt.plot(st_sintes[azimut_index[i]].times() , st_sintes[azimut_index[i]].data , 'k' , label='sis_teo')
#    plt.legend()
#    plt.title('Formas de Onda P  ' + st_reales[azimut_index[i]].id + \
#                  ' sismograma sintetico syngine con azimut '+str(azimut_orden[i]),fontsize=8)
#    pylab.savefig('grafs/'+numbers_format[i]+'.'+st_reales[azimut_index[i]].id+'.png')
#    plt.close()     


#for i in range(len(st_reales)):
#    plt.figure()
#    plt.plot( st_reales[i].times() , st_reales[i].data , 'r',label='sis_obs')
#    plt.plot( st_sintes[i].times() , st_sintes[i].data , 'b',label='sis_teo')
#    plt.legend()
#    plt.title('Formas de Onda P  ' + st_reales[i].id + ' sismograma sintetico syngine azimut '+azimutfloat[])
#    pylab.savefig('grafs/'+st_reales[i].id+'.png')
#    plt.close()
#plt.plot(st_reales[93].times(),st_reales[93].data,'r')
#plt.plot(st_sintes[0].times(),st_sintes[0],'g')
#plt.plot(st_sintes[93].times(),sism_lag[93].data,'b')

