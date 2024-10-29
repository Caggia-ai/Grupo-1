import random

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
