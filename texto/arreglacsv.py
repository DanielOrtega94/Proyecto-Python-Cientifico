

file = open("cmt.csv")
salida = open("cmt1.txt", 'w')
i = 0
texto = ""
for linea in file:

    if(i == 2):
        texto = texto.replace("\n", "")
        salida.write(texto+'\n')
        texto = ""
        i = 0
    texto += linea
    i += 1
