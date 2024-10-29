import random

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

def porcentajessemanal(ventasvendedor):
    semanasum = [0, 0, 0, 0]  
    for ventas in ventasvendedor.values():  
        for i in range(4): 
            semanasum[i] += ventas[i]
    total_ventas = sum(semanasum) 
    porcentajes = [((semana / total_ventas) * 100) for semana in semanasum] if total_ventas > 0 else 0  # Evitamos la división por cero
    
    # Escribimos los porcentajes en el archivo como un diccionario
    with open("Porcentaje Semanal.txt", "wt") as archivo2:
        diccionarioporcentaje = {f"Semana{i + 1}": f"{porcentaje:.2f}%" for i, porcentaje in enumerate(porcentajes)}
        archivo2.write(str(diccionarioporcentaje))

def repartirTrabajadores(lista, sedes):
    try:
        with open("Sedes.txt", "wt") as documentoSedes:
            listaconSedes=[[sede] for sede in sedes] # Permite ordenar las sedes en la lista sedes
            asignadas=random.sample(lista,len(sedes)) # Agarra la lista de credenciales y utiliza random sample para distribuirlas entre las sedes de manera que no se repitan y tambien sea equitativo
            for i in range(len(sedes)):                    #-----------------------------
                listaconSedes[i].append(asignadas[i])         #Se encarga de minimo llenar una credencial por sede
            for credencial in asignadas:
                lista.remove(credencial)                   # Borra credenciales para que no se repitan
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

def porcentajes(total, parte):
    if total > 0:
        return (parte/total) * 100
    return  0

def porcentajeVendedor():
    try:
        with open("Porcentaje por Vendedor.txt", "wt") as archSalida1, open("Sedes.txt", "rt") as documentoSedes, open("Ventas Semanales.txt", "rt") as documentoSemanal:
            ventas={}
            for linea in documentoSemanal:
                partes=linea.strip().strip("[]").split(",")
                credencial=partes[0]
                totalMes=int(partes[-1])  # El total del mes es el último valor
                ventas[credencial]=totalMes

            sedes={}
            for linea in documentoSedes:
                partes=linea.strip().strip("[]").split(",")
                sede=partes[0].strip()
                credencialesSede=[cred.strip() for cred in partes[1:]]
                sedes[sede]=credencialesSede
            
            resultado={}
            for sede,vendedores in sedes.items():
                totalSede=sum(ventas[cred] for cred in vendedores if cred in ventas)
                resultado[sede]={}
                for vendedor in vendedores:
                    if vendedor in ventas:
                        porcentaje=porcentajes(totalSede,ventas[vendedor])
                        resultado[sede][vendedor]=round(porcentaje, 2)

            # Guardar resultados en un archivo de salida
            for sede,vendedores in resultado.items():
                archSalida1.write(f"Sede: {sede}:\n")
                for vendedor,porcentaje in vendedores.items():
                    archSalida1.write(f"{'Vendedor'.rjust(15)} {vendedor}: {porcentaje:.2f}%\n")
                    
            archSalida1.write("\n 2do Diccionario: \n")
            dict_credenciales = {vendedor: round(porcentaje, 2) for sede, vendedores in resultado.items() for vendedor, porcentaje in vendedores.items()}
            archSalida1.write(str(dict_credenciales) + "\n")
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
