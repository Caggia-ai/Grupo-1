
from modulosaux import porcentajes

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
