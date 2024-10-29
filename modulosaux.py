
def detectarRepetidos(legajo,lista):
    return legajo in lista


def escribirDocumento(lista):
    with open("Credenciales.txt","wt") as archivo:
        for credencial in lista:
            archivo.write(credencial+"\n")

def sumaListaRecursiva(lista):
    if len(lista)==0:
        return 0
    else:
        return lista[0]+sumaListaRecursiva(lista[1:])
