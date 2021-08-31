# Actividad Bonus IIC2233 2020-2

import pyrematch as re

# -------------------------------------------------------------------
# DEFINIR AQUI LOS PATRONES PARA CONSTRUIR CADA EXPRESION REGULAR
# NO CAMBIAR LOS NOMBRES DE LAS VARIABLES
PATRON1 = r"== !n{\w+( \w+)?+( \w+)?} ==\n"
PATRON2 = r"=== !n{\w+( \w+)?+( \w+)?} ===\n"
PATRON3 = r"==== !n{\w+( \w+)?+( \W?+\w+\W?+\w+\W?+)?} ====\n"
PATRON4 = r"== !n{\w+( \w+)?+( \w+)?} =="
PATRON5 = ""
PATRON6 = ""


# -------------------------------------------------------------------
# Complete a continuación el código de cada consulta.
# Cada consulta recibe el patrón correspondiente para construir la expresión
# regular, y el texto sobre el cual se aplicará.
# Cada consulta debe retornar una lista de tuplas, donde cada tupla contiene
# el match encontrado, su posición de inicio y su posición de término.


# CONSULTA 1

def consulta1(texto, patron):
    lista_final = []
    regex = re.compile(patron)
    for match in regex.finditer(texto):
        tupla = []
        name = match.group("n")
        posiciones = match.span("n")
        tupla.append(name)
        tupla.append(posiciones[0])
        tupla.append(posiciones[1])
        lista_final.append(tuple(tupla))
    lista_final.reverse()
    return lista_final


# CONSULTA 2

def consulta2(texto, patron):
    lista_final = []
    regex = re.compile(patron)
    for match in regex.finditer(texto):
        tupla = []
        name = match.group("n")
        posiciones = match.span("n")
        tupla.append(name)
        tupla.append(posiciones[0])
        tupla.append(posiciones[1])
        lista_final.append(tuple(tupla))
    lista_final.reverse()
    return lista_final


# CONSULTA 3

def consulta3(texto, patron):
    lista_final = []
    regex = re.compile(patron)
    for match in regex.finditer(texto):
        tupla = []
        name = match.group("n")
        posiciones = match.span("n")
        tupla.append(name)
        tupla.append(posiciones[0])
        tupla.append(posiciones[1])
        lista_final.append(tuple(tupla))
    lista_final.reverse()
    return lista_final


# CONSULTA 4

def consulta4(texto, patron):
    lista_final = []
    regex = re.compile(patron)
    for match in regex.finditer(texto):
        tupla = []
        name = match.group("n")
        posiciones = match.span("n")
        tupla.append(name)
        tupla.append(posiciones[0])
        tupla.append(posiciones[1])
        lista_final.append(tuple(tupla))
    print(lista_final)
    lista_final.reverse()
    return lista_final


# CONSULTA 5

def consulta5(texto, patron):
    pass


# CONSULTA 6

def consulta6(texto, patron):
    pass
