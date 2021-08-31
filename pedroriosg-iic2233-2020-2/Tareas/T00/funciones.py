from random import randint
from string import ascii_uppercase as letras
import tablero

# Acá funciones clave para el programa
# No están las bombas especiales


def menu_inicio():
    validacion = True
    # La funcion imprime la visual del menú y pide input
    while validacion:
        print(" \n***** Menú de Inicio *****")
        print(" \nSelecciona una opción:\n ")
        print("[0] Iniciar una partida")
        print("[1] Ver Ranking de puntajes")
        print("[2] Salir del programa\n ")
        option = input("Indique su opción (0, 1 o 2): ")
        if option == "0" or option == "1" or option == "2":
            validacion = False
            return int(option)
        else:
            print("\nSeleccione una opción válida.")


def ranking_de_puntajes():
    # Abrimos el archivo
    with open("puntajes.txt", "rt") as archivo:
        informacion = archivo.readlines()
    # Si no hay inscritos
    if len(informacion) == 0:
        print("\nNo existen puntajes registrados")
        return 0
    # Verificamos que la primera linea no esté vacía
    if len(informacion) != 0:
        if informacion[0] == "\n":
            informacion = informacion[1:]
    # Limpiamos la información
    rankings = list()
    for linea in informacion:
        puntaje_personal = linea.strip().split(",")
        puntaje_personal[1] = int(puntaje_personal[1])
        rankings.append(puntaje_personal)
    # Acá en caso de que el jugador sea el primero en inscribirse
    # Ordenamos la lista, invertimos
    rankings.sort(key=lambda x: x[1])
    rankings.reverse()
    rankings = rankings[:5]
    # Mostramos el menú
    validacion = True
    while validacion:
        contador = 1
        print(" \n***** Ranking de Puntajes *****\n ")
        for numero in rankings:
            print(f"{contador}) {numero[0]}: {numero[1]} Ptos")
            contador += 1
        print(" \n[0] Volver\n ")
        option = input("Indique su opción (0): ")
        if option == "0":
            validacion = False
            return int(option)
        else:
            print("\nSelecciona una opción válida.")


def restricciones_apodo(apodo):
    es_valido = False
    # Revisaremos si el apodo es válido
    if len(apodo) >= 5 and apodo.isalnum():
        es_valido = True
    return es_valido


def apodo_invalido():
    validacion = True
    print(" \n***** Apodo ingresado inválido *****")
    print(" \n***** Debes ingresar un apodo alfanumérico *****")
    print(" \n***** El apodo debe tener al menos 5 caracteres *****")
    while validacion:
        print(" \nSelecciona una opción:\n")
        print("[0] Ingresar apodo nuevamente")
        print("[1] Volver al Menú de Inicio\n ")
        option = input("Indique su opción (0 o 1): ")
        if option == "0" or option == "1":
            validacion = False
            return int(option)
        else:
            print("\nSelecciona una opción válida.")


def coordenadas_tablero():
    print(" \n***** Seleccione el tamaño del mapa *****\n ")
    es_valido = False
    while not es_valido:
        fil = input("Ingrese Nº Filas [3 - 15]: ")
        col = input("Ingrese Nº Columnas [3 - 15]: ")
        if fil.isnumeric() and col.isnumeric():
            if int(fil) >= 3 and int(fil) <= 15 and int(col) >= 3 and int(col) <= 15:
                es_valido = True
            else:
                print("")
                print(" \n***** Tablero inválido *****")
                print(" \n***** Debes ingresar dimensiones válidas *****\n ")
        else:
            print("")
            print(" \n***** Tablero inválido *****")
            print(" \n***** Debes ingresar dimensiones válidas *****\n ")
    return es_valido, int(fil), int(col)


def crear_mapa(fil, col):
    tablero = []
    filas = []
    for fila in range(0, fil):
        for columna in range(0, col):
            filas.append(" ")
        tablero.append(filas)
        filas = []
    return tablero


def posicionamiento_barcos(tab_rival, tab_propio, num_barcos, filas, columnas):
    # Posicionando barcos rivales
    tablero_rival = tab_rival
    ejecucion_rival = True
    contador_barcos_rival = 0
    while ejecucion_rival:
        coordenadas_rival = (randint(0, filas - 1), randint(0, columnas - 1))
        if tablero_rival[coordenadas_rival[0]][coordenadas_rival[1]] == " ":
            tablero_rival[coordenadas_rival[0]][coordenadas_rival[1]] = "B"
            contador_barcos_rival += 1
        if contador_barcos_rival == num_barcos:
            ejecucion_rival = False
    # Posicionando barcos propios
    tablero_propio = tab_propio
    ejecucion_propio = True
    contador_barcos_propio = 0
    while ejecucion_propio:
        coordenadas_propio = (randint(0, filas - 1), randint(0, columnas - 1))
        if tablero_propio[coordenadas_propio[0]][coordenadas_propio[1]] == " ":
            tablero_propio[coordenadas_propio[0]][coordenadas_propio[1]] = "B"
            contador_barcos_propio += 1
        if contador_barcos_propio == num_barcos:
            ejecucion_propio = False
    return tablero_rival, tablero_propio


def menu_de_juego(tab_rival, tab_propio):
    print(" \n***** Menú de Juego *****\n ")
    tablero.print_tablero(tab_rival, tab_propio)
    print(" \n[0] Rendirse")
    print("[1] Lanzar una bomba")
    print("[2] Salir del programa\n ")
    option = input("Ingresa tu elección: ")
    if option == "0" or option == "1" or option == "2":
        return int(option)
    else:
        print("\nIngrese una opción válida.")


def calcular_puntaje(fil, col, num_barcos, ene_descubiertos, ali_descubiertos):
    puntaje = (fil * col * num_barcos * (ene_descubiertos - ali_descubiertos))
    if puntaje > 0:
        return puntaje
    else:
        return 0


def abrir_parametros():
    # Abrimos el archivo
    with open("parametros.py", "rt") as archivo:
        informacion = archivo.readlines()
    # Limpiamos la información
    parametros = list()
    for linea in informacion:
        parametro = linea.strip().split(" = ")
        parametro[1] = int(parametro[1])
        parametros.append(parametro)
    return parametros[0][1], parametros[1][1]


def inscribir_puntaje(apodo, puntaje):
    inscripcion = "\n"+apodo+","+str(puntaje)
    archivo = open("puntajes.txt", "a")
    archivo.write(inscripcion)
    archivo.close()


def seleccion_bombas(bomba_cruz, bomba_x, bomba_diamante):
    ejecucion_seleccion = True
    print("\n***** Seleccione Tipo de Bomba *****\n")
    print("[0] Bomba Regular")
    print("[1] Bomba Cruz")
    print("[2] Bomba X")
    print("[3] Bomba Diamante\n")
    while ejecucion_seleccion:
        option = input("Seleccione Tipo de Bomba: ")
        if option == "0":
            return int(option)
        elif option == "1" and bomba_cruz:
            return int(option)
        elif option == "2" and bomba_x:
            return int(option)
        elif option == "3" and bomba_diamante:
            return int(option)
        else:
            print("\nBomba no disponible. Seleccione nuevamente Tipo de Bomba.\n")


def seleccion_coordenadas(tablero_rival, filas, columnas, letters=letras):
    # Creamos diccionario con asociaciones
    asociaciones = dict()
    contador = 0
    abc = letters[:columnas]
    for indice in abc:
        asociaciones[indice] = contador
        contador += 1
    ejecucion_coordenadas = True
    print("\n***** Selecciona coordenadas de disparo *****\n")
    while ejecucion_coordenadas:
        coordenadas = input("Ingrese coordenadas (Ejemplo: A5): ")
        if len(coordenadas) != 2 or coordenadas.isalpha() or coordenadas[0].isnumeric():
            print("\n***** Coordenadas ingresadas inválidas *****")
            print("\nPor favor respeta el formato. Ingrese nuevamente.\n")
        else:
            coordenadas = list(coordenadas)
            coordenadas[0] = coordenadas[0].upper()
            coordenadas[1] = int(coordenadas[1])
            if not coordenadas[0] in abc:
                print("\n***** Coordenadas ingresadas inválidas *****")
                print("\nLetra columna no disponible. Ingrese nueva coordenada.\n")
            elif coordenadas[1] >= filas:
                print("\n***** Coordenadas ingresadas inválidas *****")
                print("\nNúmero fila no disponible. Ingrese nueva coordenada.\n")
            else:
                posicion = tablero_rival[coordenadas[1]][asociaciones[coordenadas[0]]]
                if posicion != " " and posicion != "B":
                    print("\n***** Coordenadas ingresadas inválidas *****")
                    print("\nCoordenada ocupada. Ingrese nueva coordenada\n")
                else:
                    print(f"\nDisparaste a la coordenada {coordenadas[0] + str(coordenadas[1])}")
                    return asociaciones[coordenadas[0]], coordenadas[1]


def bomba_regular(tab_rival, fila, columna, descubiertos):
    repite = False
    apuntados = descubiertos
    tab_final = tab_rival
    posicion = tab_final[fila][columna]
    if posicion == " ":
        tab_final[fila][columna] = "X"
    elif posicion == "B":
        tab_final[fila][columna] = "F"
        apuntados += 1
        repite = True
    return tab_final, apuntados, repite


def jugada_oponente(tab_rival, tab_propio, filas, columnas, descubiertos,
                    letters=letras):
    # Creamos diccionario con asociaciones
    puntos = descubiertos
    asociaciones = dict()
    contador = 0
    abc = letters[:columnas]
    for indice in abc:
        asociaciones[contador] = indice
        contador += 1
    repite = True
    table_rival = tab_rival
    table_propio = tab_propio
    while repite:
        repite = False
        eleccion = True
        while eleccion:
            coordenada_fila = randint(0, filas - 1)
            coordenada_columna = randint(0, columnas - 1)
            posicion = table_propio[coordenada_fila][coordenada_columna]
            print_oponente = False
            if posicion == " ":
                eleccion = False
                print_oponente = True
                table_propio[coordenada_fila][coordenada_columna] = "X"
            elif posicion == "B":
                eleccion = False
                print_oponente = True
                table_propio[coordenada_fila][coordenada_columna] = "F"
                repite = True
                puntos += 1
            else:
                pass
            if print_oponente:
                print("\n¡Tu oponente ha disparado a la coordenada "
                      f"{asociaciones[coordenada_columna]}{coordenada_fila}! ")
                print("El tablero actual es:\n")
                tablero.print_tablero(table_rival, table_propio)
    return table_propio, puntos


def condicion_termino(puntos_rival, puntos_jugador, num_barcos):
    condicion = True
    if puntos_jugador == num_barcos or puntos_rival == num_barcos:
        condicion = False
    return condicion
