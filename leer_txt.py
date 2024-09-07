import os

def abrir(nombre_archivo:str)->str:
    nombre_archivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre_archivo+'.txt')
    with open(nombre_archivo,"r")as file:
        lineas = file.readlines()
    
    texto_completo = "".join([linea.rstrip("\n") for linea in lineas])
        
    return texto_completo 