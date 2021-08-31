import menus
import funciones
import funciones_bitacora
import parametros as p
from campeonato import Campeonato

ejecucion_general = True
while ejecucion_general:
    # Acá se muestra el Menú de inicio
    habilidad_especial = True
    opcion_inicio = menus.menu_inicio()
    if opcion_inicio == "0":
        # Acá se finaliza el flujo del programa
        ejecucion_general = False
    else:
        nombre_usuario, nombre_enemigo, opcion_delegacion = menus.ingresar_datos()
        simluaciones = True
        while simluaciones:
            # Instanciamos todos los deportistas
            lista_deportistas, dic_deportistas = funciones.datos_deportistas()
            # Instanciamos las delegaciones segun los datos anteriores
            delegacion, enemigo = funciones.instanciar_delegaciones(nombre_usuario,
                                                                    nombre_enemigo,
                                                                    opcion_delegacion,
                                                                    dic_deportistas)
            ejecucion_principal = True
            # Creamos la bitácora del campeonato
            funciones_bitacora.crear_txt()
            # Se muestra el Menú Principal
            campeonato = Campeonato()
            # Comienza el día 1 de Campeonato
            campeonato.dia_actual += 1
            while ejecucion_principal:
                ejecucion_entrenador = True
                # Acá se muestra el Menú Principal
                opcion_prinicpal = menus.menu_principal()
                if opcion_prinicpal == "1":  # Opcion Menú Entrenador
                    # Mostramos Moral según enunciado
                    campeonato.moral_delegaciones(delegacion, enemigo)
                    while ejecucion_entrenador:
                        # Se muestra el Menú de Entrenador
                        opcion_entrenador = menus.menu_entrenador()
                        if opcion_entrenador == "1":  # Opcion Fichar
                            if delegacion.moral < p.MENOR_MORAL_PARA_FICHAR:
                                print("\nNo puedes fichar. Moral baja.")
                            else:
                                delegacion.fichar_deportistas(dic_deportistas)
                        elif opcion_entrenador == "2":  # Opcion Entrenar
                            if delegacion.dinero < p.COSTO_ENTRENAR_DEPORTISTA:
                                print("\nNo puedes entrenar. Dinero bajo.")
                            else:
                                delegacion.entrenar_deportistas()
                        elif opcion_entrenador == "3":  # Opcion Sanar
                            if delegacion.dinero < p.COSTO_SANAR_DEPORTISTA:
                                print("\nNo puedes sanar. Dinero bajo")
                            else:
                                delegacion.sanar_lesiones(delegacion)
                        elif opcion_entrenador == "4":  # Opcion Comprar Tecnología
                            if delegacion.dinero < p.COSTO_TECNOLOGIA:
                                print("\nNo puedes Comprar Tecnología")
                            else:
                                delegacion.comprar_tecnologia()
                        elif opcion_entrenador == "5":  # Opcion Habilidad Especial
                            if habilidad_especial and delegacion.dinero >= \
                             p.COSTO_HABILIDAD_ESPECIAL:
                                delegacion.habilidad_especial()
                                habilidad_especial = False
                            else:
                                print("\nNo puedes utilizar la habilidad especial")
                        elif opcion_entrenador == "-1":
                            ejecucion_entrenador = False
                        else:
                            ejecucion_entrenador = False
                            ejecucion_principal = False
                            ejecucion_general = False

                elif opcion_prinicpal == "2":  # Simulacion de competencias
                    if p.DIAS_COMPETENCIA > campeonato.dia_actual:
                        # Mostramos moral según enunciado
                        campeonato.moral_delegaciones(delegacion, enemigo)
                        campeonato.realizar_competencias(delegacion, enemigo)
                        if p.DIAS_COMPETENCIA <= campeonato.dia_actual:
                            print("\nEl campeonato ha finalizado\n")
                            print("Medallas delegación IEEEsparta:", campeonato.medallero["IEEEsparta"])
                            print("Medallas delegación DCCrotona:", campeonato.medallero["DCCrotona"])
                            if campeonato.medallero["IEEEsparta"] > campeonato.medallero["DCCrotona"]:
                                print("\nGanador: IEEEsparta")
                            elif campeonato.medallero["IEEEsparta"] < campeonato.medallero["DCCrotona"]:
                                print("\nGanador: DCCrotona")
                            else:
                                print("Ganador: EMPATE")
                            ejecucion_entrenador = False
                            ejecucion_principal = False
                            opcion_simulacion = menus.simulacion_nueva()
                            if opcion_simulacion == "1":
                                pass
                            else:
                                simluaciones = False
                                ejecucion_general = False
                elif opcion_prinicpal == "3":  # Mostrar estado
                    # Actualizamos la moral antes de mostrar el estado
                    campeonato.actualizar_moral(delegacion, enemigo)
                    campeonato.mostrar_estado(delegacion, enemigo)
                elif opcion_prinicpal == "0":
                    ejecucion_principal = False
                    simluaciones = False
                    ejecucion_general = False
                elif opcion_prinicpal == "-1":
                    ejecucion_principal = False
                    simluaciones = False
