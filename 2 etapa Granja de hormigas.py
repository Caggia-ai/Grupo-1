import random
from modulosaux import detectarRepetidos, escribirDocumento, sumaListaRecursiva
from moduloporcentaje import porcentajessemanal, porcentajeVendedor, fporcentajes

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

def repartirTrabajadores(lista, sedes):
    try:
        with open("Sedes.txt", "wt") as documentoSedes:
            listaconSedes=[[sede] for sede in sedes] 
            asignadas=random.sample(lista,len(sedes)) 
            for i in range(len(sedes)):                   
                listaconSedes[i].append(asignadas[i])         
            for credencial in asignadas:
                lista.remove(credencial)                   
            while lista:
                sedeRandom=random.choice(sedes)                     
                indiceSede=sedes.index(sedeRandom)                  
                credencialRandom=random.choice(lista)               
                listaconSedes[indiceSede].append(credencialRandom)     
                lista.remove(credencialRandom)                      
            for sede in listaconSedes:                                 
                documentoSedes.write(str(sede)+"\n")
    except OSError as msg:
        print("ERROR DE ARCHIVO:", msg)

def calcularDatosSedes(precio):
    try:
        with open("Importe total por sede.txt", "wt") as archSalida2, open("Ventas Semanales.txt", "rt") as documentoSemanal, open("Sedes.txt", "rt") as documentoSedes:
            ventas = {}
            for linea in documentoSemanal:
                partes = linea.strip().strip("[]").split(",")
                credencial = partes[0].strip()
                totalMes = int(partes[-1].strip())
                ventas[credencial] = totalMes

            sedes = {}
            for linea in documentoSedes:
                partes = linea.strip().strip("[]").split(",")
                sede = partes[0].strip()
                credenciales = [cred.strip() for cred in partes[1:]]
                sedes[sede] = credenciales

            for sede, vendedores in sedes.items():
                totalPeceras = sum(ventas[vendedor] for vendedor in vendedores if vendedor in ventas)
                archSalida2.write(f"{sede}= Total de ventas: {totalPeceras * precio}$\n")

            archSalida2.write("\n{Sedes:\n")
            for sede, vendedores in sedes.items():
                totalVendedores = len(vendedores)
                totalPeceras = sum(ventas[vendedor] for vendedor in vendedores if vendedor in ventas)
                dineroGenerado = totalPeceras * precio
                sededic = {}
                sededic[sede] = {
                    "Vendedores": totalVendedores,
                    "Peceras vendidas": totalPeceras,
                    "Dinero generado": f"{dineroGenerado}$"
                }
                archSalida2.write(str(sededic) + "\n")
            archSalida2.write("}\n")

    except OSError as msg:
        print("ERROR DE ARCHIVO:", msg)

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
