
from obspy import UTCDateTime
import pandas as pd
import os
# elegir primera fecha de todas
fecha = "2018/01/01 "
# la ultima fecha es:
fecha_last = "2018/01/31"
UTCfecha = UTCDateTime(fecha)
fechas = []
time_cmt = []
lat_cmt = []
lon_cmt = []
depth_cmt = []
name_cmt = []
exp_cmt = []
Mrr = []
Mtt = []
Mpp = []
Mrt = []
Mrp = []
Mtp = []
Err = []
Ett = []
Epp = []
Ert = []
Erp = []
Etp = []
mo = []
strike1 = []
dip1 = []
rake1 = []
strike2 = []
dip2 = []
rake2 = []

# donde se guardara toda la data
data_evento = []
archivo = 'enero-2018.txt'
nombre = 'cmt' + archivo.replace(".txt", "") + ".csv"
df = pd.DataFrame()
# fechas.append(fecha)
while UTCfecha != UTCDateTime(fecha_last) + 3600 * 24:
    # print(fecha)
    # este numero es la n-esima linea que estamos leyendo
    number = 1
    # este numero es el c-esimo evento extraido del dia
    c = 0
    # en esta lista guardamos el indice de la linea que tiene el evento c-esimo
    indices = []

    with open(archivo) as fileobject:
        for line in fileobject:
            if line[5:15] == fecha:
                c += 1
                indices.append(number)

            number += 1

    # print(indices)
    # print(c)
    # si hay indices, es por que hay eventos en tal dia, por lo tanto podemos
    # seguir
    if len(indices) > 0:
        counter = 0
        eventos = []
        with open(archivo) as fileobject:
            for line in fileobject:
                counter += 1
                # para sacar las 5 lineas de informacion de cada evento
                if counter >= indices[0] and counter < indices[-1] + 5:
                    # array con 5*n lineas, donde n es el numero de eventos
                    eventos.append(line)

        for i in range(int(len(eventos) / 5)):

            evento = eventos[5 * i:5 * (i + 1)]
            fecha_evento = fecha
            
            fechas.append(fecha_evento)
            fil1 = evento[0]
            fil2 = evento[1]
            fil3 = evento[2]
            fil4 = evento[3]
            fil5 = evento[4]
            # relevante fila 1 :
            time_cmt.append(fil1[16:26].replace(" ", ""))
            lat_cmt.append(fil1[27:33].replace(" ", ""))
            lon_cmt.append(fil1[34:41].replace(" ", ""))
            depth_cmt.append(fil1[42:47].replace(" ", ""))
            # relevante fila 2:
            name_cmt.append(fil2[0:16].replace(" ", ""))
            # relevante fila 3: nada jeje
            # relevante fila 4:
            data4 = fil4.split(" ")
            data4 = [x for x in data4 if x]
            exp_cmt.append(data4[0])
            Mrr.append(data4[1])
            Err.append(data4[2])
            Mtt.append(data4[3])
            Ett.append(data4[4])
            Mpp.append(data4[5])
            Epp.append(data4[6])
            Mrt.append(data4[7])
            Ert.append(data4[8])
            Mrp.append(data4[9])
            Erp.append(data4[10])
            Mtp.append(data4[11])
            Etp.append(float(data4[12].replace("\n", "")))
            # relevante fila 5:
            data5 = fil5.split(" ")
            data5 = [x for x in data5 if x]
            mo.append(data5[10])
            strike1.append(data5[11])
            dip1.append(data5[12])
            rake1.append(data5[13])
            strike2.append(data5[14])
            dip2.append(data5[15])
            rake2.append(float(data5[16].replace("\n", "")))

    UTCfecha += 3600 * 24
    fecha = str(UTCfecha).replace('-', '/').split('T')[0]


datos = pd.DataFrame({'fecha_evento': fechas, 'tiempo_cmt': time_cmt, 'lat_cmt': lat_cmt, 'lon_cmt': lon_cmt, 'depth_cmt': depth_cmt, 'id_evento': name_cmt, 'exp_cmt': exp_cmt, 'Mrr': Mrr, 'Mtt': Mtt, 'Mpp': Mpp,
                      'Mrt': Mrt, 'Mrp': Mrp, 'Mtp': Mtp, 'Err': Err, 'Ett': Ett, 'Epp': Epp,
                      'Ert': Ert, 'Erp': Erp, 'Etp': Etp,
                      'momento_sismico': mo, 'strike_1': strike1, 'dip_1': dip1,
                      'rake_1': rake1, 'strike_2': strike2, 'dip_2': dip2, 'rake_2': rake2})

datos.to_csv(nombre, mode='a')