def noRepetir(objetivo, lista):
    esta=False
    if objetivo in lista:
        esta=True
    return esta



def valoresCompletos(lista):
    largo=len(lista)
    for i in range(largo,-1):
        if lista[i]>9999 and lista[i]<100000:
            del lista[i]
    return lista

    
