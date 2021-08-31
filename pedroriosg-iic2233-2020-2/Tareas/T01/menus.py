def menu_inicio():
    print("\n***** Menú de Inicio *****")
    t = True
    while t:
        print("\nSelecciona una opción:")
        print("\n[1] Comenzar una nueva partida")
        print("[0] Salir del Programa\n")
        opcion = input("Indique opción: ")
        if opcion == "1" or opcion == "0":
            t = False
        else:
            print("\nOpción inválida. Ingrese nuevamente.\n")
    return opcion


def ingresar_datos():
    print("\n***** A continuación, ingresa nombres de usuario *****")
    print("\n***** Deben ser ambos alfanuméricos *****\n")
    t = True
    r = True
    while t:
        usuario = input("Nombre de usuario: ")
        usuario_rival = input("Nombre de rival: ")
        if usuario.isalnum() and usuario_rival.isalnum():
            t = False
        else:
            print("\nIngresa nombres válidos\n")
    print("\n***** A continuación, elige tu delegación *****\n")
    while r:
        print("Selecciona una opción:")
        print("\n[1] IEEEsparta")
        print("[2] DCCrotona\n")
        opcion = input("Indique su opción (1 ó 2): ")
        if opcion == "1" or opcion == "2":
            r = False
        else:
            print("\nOpción inválida. Ingrese nuevamente.\n")
    return usuario, usuario_rival, opcion


def menu_principal():
    print("\n***** Menú Principal *****")
    t = True
    while t:
        print("\nSelecciona una opción:")
        print("\n[1] Menú Entrenador")
        print("[2] Simular competencias")
        print("[3] Mostrar estado")
        print("[0] Salir del Programa")
        print("[-1] Volver al Menú anterior\n")
        opcion = input("Indique opción: ")
        lista_opciones = ["-1", "0", "1", "2", "3"]
        if opcion in lista_opciones:
            t = False
        else:
            print("\nOpción inválida. Ingrese nuevamente.\n")
    return opcion


def menu_entrenador():
    print("\n***** Menú Entrenador *****")
    t = True
    while t:
        print("\nSelecciona una opción:")
        print("\n[1] Fichar")
        print("[2] Entrenar")
        print("[3] Sanar")
        print("[4] Comprar Tecnología")
        print("[5] Usar Habilidad Especial")
        print("[0] Salir del Programa")
        print("[-1] Volver al Menú anterior\n")
        opcion = input("Indique opción: ")
        lista_opciones = ["-1", "0", "1", "2", "3", "4", "5"]
        if opcion in lista_opciones:
            t = False
        else:
            print("\nOpción inválida. Ingrese nuevamente.\n")
    return opcion


def simulacion_nueva():
    print("\n***** Simulacion Acabada *****\n")
    t = True
    while t:
        print("\nSelecciona una opción:")
        print("\n[1] Realizar una nueva simulacion")
        print("[0] Salir del programa\n")
        opcion = input("Indique opción: ")
        lista_opciones = ["0", "1"]
        if opcion in lista_opciones:
            t = False
        else:
            print("\nOpción inválida. Ingrese nuevamente.\n")
    return opcion
