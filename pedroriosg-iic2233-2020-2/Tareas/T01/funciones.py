from delegaciones import IEEEsparta, DCCrotona
from deportistas import Deportistas


def datos_deportistas():
    # Retorna un diccionario y lista con los deportistas intanciados

    # Abrimos el archivo
    with open("deportistas.csv", "rt") as archivo:
        informacion = archivo.readlines()

    # Limpiamos la informacion
    deportistas = list()
    for linea in informacion:
        deportista = linea.strip().split(",")
        deportistas.append(deportista)
    header = deportistas[0]
    deportistas = deportistas[1:]
    # Leemos el header
    dic_header = dict()
    contador = 0
    for atributo in header:
        name = atributo.strip()
        dic_header[name] = contador
        contador += 1
    # Instanciamos los deportistas
    lista_deportistas = list()
    for instancia in deportistas:
        nombre = instancia[dic_header["nombre"]].strip()
        flexibildad = int(instancia[dic_header["flexibilidad"]].strip())
        moral = int(instancia[dic_header["moral"]].strip())
        precio = int(instancia[dic_header["precio"]].strip())
        velocidad = int(instancia[dic_header["velocidad"]].strip())
        lesionado = instancia[dic_header["lesionado"]].strip()
        if lesionado == "False":
            lesionado = False
        else:
            lesionado = True
        resistencia = int(instancia[dic_header["resistencia"]].strip())
        lista_deportistas.append(Deportistas(nombre, flexibildad, moral,
                                             precio, velocidad, lesionado,
                                             resistencia))
    # Armamos el diccionario
    diccionario_deportista = dict()
    for deportista in lista_deportistas:
        diccionario_deportista[deportista.nombre] = deportista

    return lista_deportistas, diccionario_deportista


def instanciar_delegaciones(entrenador, enemigo, eleccion,
                            diccionario_deportista):
    # Abrimos el archivo
    with open("delegaciones.csv", "rt") as archivo:
        informacion = archivo.readlines()

    # Limpiamos la informacion
    delegaciones = list()
    for linea in informacion:
        delegacion = linea.strip().split(",")
        delegaciones.append(delegacion)
    header = delegaciones[0]
    delegaciones = delegaciones[1:]
    dict_header = dict()
    contador = 0
    for atributo in header:
        dict_header[atributo] = contador
        contador += 1
    for clase in delegaciones:
        if clase[dict_header["Delegacion"]] == "IEEEsparta":
            # Info IEEEspartanos
            esparta_moral = float(clase[dict_header["Moral"]])
            esparta_nombre = clase[dict_header["Delegacion"]]
            esparta_equipo = clase[dict_header["Equipo"]].split(";")
            deportistas_esparta = list()
            for nombre in esparta_equipo:
                deportistas_esparta.append(diccionario_deportista[nombre])
                del diccionario_deportista[nombre]
            esparta_medalla = int(clase[dict_header["Medallas"]])
            esparta_dinero = int(clase[dict_header["Dinero"]])
        elif clase[dict_header["Delegacion"]] == "DCCrotona":
            # Info DCCrotona
            crotona_moral = float(clase[dict_header["Moral"]])
            crotona_nombre = clase[dict_header["Delegacion"]]
            crotona_equipo = clase[dict_header["Equipo"]].split(";")
            deportistas_crotona = list()
            for nombre in crotona_equipo:
                deportistas_crotona.append(diccionario_deportista[nombre])
                del diccionario_deportista[nombre]
            crotona_medalla = int(clase[dict_header["Medallas"]])
            crotona_dinero = int(clase[dict_header["Dinero"]])

    # Instanciamos segun elección
    if eleccion == "1":
        delegacion = IEEEsparta(esparta_nombre, entrenador,
                                deportistas_esparta,
                                esparta_medalla, esparta_moral, esparta_dinero)
        enemigo = DCCrotona(crotona_nombre, enemigo, deportistas_crotona,
                            crotona_medalla, crotona_moral, crotona_dinero)
    else:
        enemigo = IEEEsparta(esparta_nombre, enemigo, deportistas_esparta,
                             esparta_medalla, esparta_moral, esparta_dinero)
        delegacion = DCCrotona(crotona_nombre, entrenador, deportistas_crotona,
                               crotona_medalla, crotona_moral, crotona_dinero)

    return delegacion, enemigo
