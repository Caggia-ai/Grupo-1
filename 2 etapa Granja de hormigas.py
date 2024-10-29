import random
from modulosaux import detectarRepetidos, escribirDocumento, sumaListaRecursiva
from moduloporcentaje import porcentajessemanal, porcentajeVendedor, fporcentajes
from modulosedes import repartirTrabajadores, calcularDatosSedes

def ingresoCredenciales(lista):
    while True:
        try:
            credencial = input("Ingrese una credencial de 5 dígitos (-1 para finalizar): ")
            credencial=credencial.strip(" ")
            if credencial==str(-1):
                if len(lista)<6:
                    print(f"Debes ingresar minimo 6 credenciales. Usted cuenta unicamente con {len(lista)} credencial/es")
                    continue
                break
            if not credencial.isdigit():
                raise ValueError("La credencial debe ser un número.")
            if len(credencial)==5 and int(credencial)!= 0:
                repetido=detectarRepetidos(credencial, lista)
                if repetido:
                    print("Esta credencial ya fue registrada. Ingrese una nueva")
                else:
                    lista.append(credencial)
            else:
                print("Por favor ingrese una credencial de exactamente 5 dígitos.")
        except ValueError:
            print(f"Error de valor: la credencial debe ser un número.")
        except OSError as msg:
            print("ERROR DE ARCHIVO",msg)
    escribirDocumento(lista)

def ventas():
    ventasvendedor = {}
    try:
        with open("Ventas Semanales.txt", "wt") as documentoSemanal, open("Credenciales.txt", "rt") as documentoCredenciales:
            for linea in documentoCredenciales:
                credencial=linea.strip()
                semana=[random.randint(0, 20) for i in range(4)]
                totalMes=sumaListaRecursiva(semana)
                semana.append(totalMes)
                ventasvendedor[credencial] = semana[:4]  # Almacena solo las ventas de las 4 semanas
                semana.insert(0,credencial) #el primer elemento es la credencial
                documentoSemanal.write(str(semana)+"\n")
    except OSError as msg:
        print("ERROR DE ARCHIVO:", msg)
    return ventasvendedor

def main():
    COSTO=500
    listaCredenciales=[]
    listaSedes=["Quilmes","Sarandi","Wilde","Bernal","V.Dominico","Ezpeleta"]
    ingresoCredenciales(listaCredenciales)
    if listaCredenciales:
        repartirTrabajadores(listaCredenciales, listaSedes)
        ventas()
        porcentajeVendedor()
        calcularDatosSedes(COSTO)
        porcentajesemanal = ventas()
        porcentajessemanal(porcentajesemanal)
    else:
        print("No se ingresaron datos. No se puede realizar ningún informe")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
