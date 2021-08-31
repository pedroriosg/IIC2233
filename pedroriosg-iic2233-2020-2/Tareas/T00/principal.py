import funciones
import funciones_2
import tablero

# Main (código principal)

ejecucion_general = True

while ejecucion_general:
    ejecucion_apodo = True
    # Se muestra el menu principal
    opcion_menu_inicio = funciones.menu_inicio()
    if opcion_menu_inicio == 2:  # Acá se acaba el programa
        ejecucion_general = False
    elif opcion_menu_inicio == 1:  # Acá se muestra el Ranking
        funciones.ranking_de_puntajes()
        pass
    elif opcion_menu_inicio == 0:
        while ejecucion_apodo:
            ejecucion_tablero = True
            apodo = input(" \nIngrese Apodo: ")
            # Revisamos si el apodo es válido
            if funciones.restricciones_apodo(apodo):
                ejecucion_apodo = False
                # Funcion crear
                while ejecucion_tablero:
                    validacion_tablero, filas_tablero, columnas_tablero = \
                        funciones.coordenadas_tablero()
                    if validacion_tablero:
                        ejecucion_tablero = False
                        # Creación de mapas
                        mapa_oponente = funciones.crear_mapa(filas_tablero,
                                                             columnas_tablero)
                        mapa_jugador = funciones.crear_mapa(filas_tablero,
                                                            columnas_tablero)
                        # Posicionamiento de barcos
                        num_barcos, radio = funciones.abrir_parametros()
                        tablero_rival, tablero_propio = funciones.posicionamiento_barcos(mapa_oponente, mapa_jugador, num_barcos, filas_tablero, columnas_tablero)
                        # Implementar menú de juego
                        enemigos_descubiertos = 0
                        aliados_descubiertos = 0
                        bomba_cruz = True
                        bomba_x = True
                        bomba_diamante = True
                        # Acá juega el jugador principal
                        condicion_termino = True
                        while condicion_termino:
                            ejecucion_menu_de_juego = True
                            while ejecucion_menu_de_juego:
                                opcion_menu_juego = funciones.menu_de_juego(tablero_rival,
                                                                            tablero_propio)
                                if opcion_menu_juego == 1:
                                    # Seleccionamos la opcion de la bomba
                                    opcion_bomba = funciones.seleccion_bombas(bomba_cruz, bomba_x, bomba_diamante)
                                    # Pedimos coordenadas
                                    col, fil = funciones.seleccion_coordenadas(tablero_rival, filas_tablero, columnas_tablero)
                                    # Opciones de bombas
                                    if opcion_bomba == 0:
                                        tablero_rival, enemigos_descubiertos, repite = funciones.bomba_regular(tablero_rival, fil, col, enemigos_descubiertos)
                                    elif opcion_bomba == 1:
                                        bomba_cruz = False
                                        bomba_x = False
                                        bomba_diamante = False
                                        print("\nIMPORTANTE: Desde ahora solo puedes usar la Bomba Regular\n")
                                        tablero_rival, enemigos_descubiertos, repite = funciones_2.bomba_cruz(tablero_rival, radio, fil, col, enemigos_descubiertos)
                                    elif opcion_bomba == 2:
                                        bomba_cruz = False
                                        bomba_x = False
                                        bomba_diamante = False
                                        print("\nIMPORTANTE: Desde ahora solo puedes usar la Bomba Regular\n")
                                        tablero_rival, enemigos_descubiertos, repite = funciones_2.bomba_x(tablero_rival, radio, fil, col, enemigos_descubiertos)
                                    elif opcion_bomba == 3:
                                        bomba_cruz = False
                                        bomba_x = False
                                        bomba_diamante = False
                                        print("\nIMPORTANTE: Desde ahora solo puedes usar la Bomba Regular\n")
                                        tablero_rival, enemigos_descubiertos, repite = funciones_2.bomba_diamante(tablero_rival, radio, fil, col, enemigos_descubiertos)
                                    if not repite:
                                        ejecucion_menu_de_juego = False
                                        print("Disparo al agua!\n")
                                    else:
                                        print("Tocado!\n")
                                    tablero.print_tablero(tablero_rival, tablero_propio)
                                    condicion_termino = funciones.condicion_termino(enemigos_descubiertos, aliados_descubiertos, num_barcos)
                                    if not condicion_termino:
                                        ejecucion_menu_de_juego = False
                                        # Calcular puntaje
                                        puntaje_final_1 = funciones.calcular_puntaje(filas_tablero, columnas_tablero, num_barcos, enemigos_descubiertos, aliados_descubiertos)
                                        print(f"\nJuego Finalizado. Has ganado con {puntaje_final_1} Ptos!")
                                        # Inscribimos puntaje
                                        funciones.inscribir_puntaje(apodo, puntaje_final_1)
                                        # Se acaba el programa ?
                                elif opcion_menu_juego == 2:
                                    # Finaliza el programa
                                    ejecucion_menu_de_juego = False
                                    condicion_termino = False
                                    ejecucion_general = False
                                    print("\nHas abandonado el juego.\n")
                                elif opcion_menu_juego == 0:
                                    ejecucion_menu_de_juego = False
                                    condicion_termino = False
                                    # Calcular puntaje
                                    puntaje_0 = funciones.calcular_puntaje(filas_tablero, columnas_tablero, num_barcos, enemigos_descubiertos, aliados_descubiertos)
                                    print(" \nTe has rendido. Has perdido la partida!")
                                    print(f"Tu puntaje fue de {puntaje_0} Ptos")
                                    # Inscribimos puntaje
                                    funciones.inscribir_puntaje(apodo, puntaje_0)
                            # Juega el oponente
                            if condicion_termino:
                                tablero_propio, aliados_descubiertos = funciones.jugada_oponente(tablero_rival, tablero_propio, filas_tablero, columnas_tablero, aliados_descubiertos)
                                ejecucion_menu_de_juego = True
                                condicion_termino = funciones.condicion_termino(enemigos_descubiertos, aliados_descubiertos, num_barcos)
                                if not condicion_termino:
                                    # Calcular puntaje
                                    puntaje_final_2 = funciones.calcular_puntaje(filas_tablero, columnas_tablero, num_barcos, enemigos_descubiertos, aliados_descubiertos)
                                    print(f"\nJuego Finalizado. Has perdido con {puntaje_final_2} Ptos!")
                                    ejecucion_menu_de_juego = False
                                    # Inscribimos puntaje
                                    funciones.inscribir_puntaje(apodo, puntaje_final_2)
                                    # Se acaba el programa
            # Apodo inválido
            else:
                opcion_menu_invalido = funciones.apodo_invalido()
                if opcion_menu_invalido == 0:
                    pass
                else:
                    ejecucion_apodo = False
