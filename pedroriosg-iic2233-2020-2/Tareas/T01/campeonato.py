import funciones_bitacora as funciones
import parametros as p
from random import choice
from deportes import Atletismo, Natacion, Gimnasia, Ciclismo


class Campeonato():

    def __init__(self):
        self.dia_actual = p.DIA_INICIAL_COMPETENCIA
        self.medallero = {"IEEEsparta": 0, "DCCrotona": 0}
        self.medallas_esparta = {"Atletismo": 0, "Natacion": 0, "Gimnasia": 0, "Ciclismo": 0}
        self.medallas_crotona = {"Atletismo": 0, "Natacion": 0, "Gimnasia": 0, "Ciclismo": 0}

    def realizar_competencias(self, delegacion, enemigo):
        self.dia_actual += 1
        funciones.agregar_dia(self.dia_actual)
        print("\nComienza el día de competencia!!")
        print("\nTus jugadores disponibles son:\n")
        # Listas para contrincantes por deporte
        deportistas_atletismo = []
        deportistas_natacion = []
        deportistas_gimnasia = []
        deportistas_ciclismo = []
        lista_numeros = []
        print(f"NUMER0  NOMBRE DEPORTISTA{15 * ' '}VELOCIDAD   RESISTENCIA"
              "  FLEXIBILIDAD   MORAL  LESION\n")
        c = 0
        for d in delegacion.equipo:
            datos = [(d.nombre, d.velocidad, d.resistencia, d.flexibilidad,
                      d.moral, str(d.lesionado))]
            for n, v, r, f, m, l in datos:
                print(f"{c}{7 * ' '}{n:35s}{v: <3.0f}{11 * ' '}"
                      f"{r: <3.0f}{10 * ' '}{f: <3.0f}{8 * ' '}"
                      f"{m: <3.0f}{3 * ' '}{l:>s}")
                lista_numeros.append(str(c))
                c += 1
        t = True
        while t:
            op_atl = input("\nIngresa tu opción para Atletismo: ")
            op_nat = input("Ingresa tu opción para Natación: ")
            op_gim = input("Ingresa tu opción para Gimnasia: ")
            op_cic = input("Ingresa tu opción para Ciclismo: ")
            if op_atl in lista_numeros and op_nat in lista_numeros and op_gim \
               in lista_numeros and op_cic in lista_numeros:
                t = False
                # Agregamos Atletismo
                deportistas_atletismo.append(delegacion.equipo[int(op_atl)])
                rival_atl = choice(enemigo.equipo)
                deportistas_atletismo.append(rival_atl)
                # Agregamos Natacion
                deportistas_natacion.append(delegacion.equipo[int(op_nat)])
                rival_nat = choice(enemigo.equipo)
                deportistas_natacion.append(rival_nat)
                # Agregamos Gimnasia
                deportistas_gimnasia.append(delegacion.equipo[int(op_gim)])
                rival_gim = choice(enemigo.equipo)
                deportistas_gimnasia.append(rival_gim)
                # Agregamos Ciclismo
                deportistas_ciclismo.append(delegacion.equipo[int(op_cic)])
                rival_cic = choice(enemigo.equipo)
                deportistas_ciclismo.append(rival_cic)
            else:
                print("\nOpción no válida. Ingresa números existentes.")
        # Atletismo
        print(f"\nATLETISMO: {deportistas_atletismo[0].nombre} vs "
              f"{deportistas_atletismo[1].nombre}\n")  # Mostramos quienes compiten
        validez, empate, dele_ganadora, dele_perdedora, j_ganador, j_perdedor = \
            Atletismo().validez_competencia(deportistas_atletismo[0],
                                            deportistas_atletismo[1], delegacion, enemigo)
        if validez:  # Si el juego es válido, ahora pueden lesionarse
            deportistas_atletismo[0].lesionarse(Atletismo().riesgo)
            deportistas_atletismo[1].lesionarse(Atletismo().riesgo)
            # Chequeamos condiciones nuevamente
            validez, empate, dele_ganadora, dele_perdedora, j_ganador, j_perdedor = \
                Atletismo().validez_competencia(deportistas_atletismo[0],
                                                deportistas_atletismo[1], delegacion, enemigo)
        # Analizamos los valores retornados para bitácora y premiar
        if empate:
            funciones.agregar_bitacora("Atletismo", "EMPATE", "EMPATE")
        elif not validez:
            funciones.agregar_bitacora("Atletismo", dele_ganadora.nombre, j_ganador.nombre)
        else:
            empate, dele_ganadora, dele_perdedora, j_ganador, j_perdedor = \
                Atletismo().calcular_ganador(deportistas_atletismo[0],
                                             deportistas_atletismo[1], delegacion, enemigo)
            if empate:
                funciones.agregar_bitacora("Atletismo", "EMPATE", "EMPATE")
            else:
                funciones.agregar_bitacora("Atletismo", dele_ganadora.nombre, j_ganador.nombre)
        if not empate:
            self.premiar(dele_ganadora, dele_perdedora, j_ganador, j_perdedor, "Atletismo")
        # Natacion
        # Mostramos quienes compiten
        print(f"\nNATACION: {deportistas_natacion[0].nombre} vs {deportistas_natacion[1].nombre}\n")
        validez, empate, dele_ganadora, dele_perdedora, j_ganador, j_perdedor = \
            Natacion().validez_competencia(deportistas_natacion[0],
                                           deportistas_natacion[1], delegacion, enemigo)
        if validez:  # Si el juego es válido, ahora pueden lesionarse
            deportistas_natacion[0].lesionarse(Natacion().riesgo)
            deportistas_natacion[1].lesionarse(Natacion().riesgo)
            # Chequeamos condiciones nuevamente
            validez, empate, dele_ganadora, dele_perdedora, j_ganador, j_perdedor = \
                Natacion().validez_competencia(deportistas_natacion[0],
                                               deportistas_natacion[1], delegacion, enemigo)
        # Analizamos los valores retornados para bitácora y premiar
        if empate:
            funciones.agregar_bitacora("Natacion", "EMPATE", "EMPATE")
        elif not validez:
            funciones.agregar_bitacora("Natacion", dele_ganadora.nombre, j_ganador.nombre)
        else:
            empate, dele_ganadora, dele_perdedora, j_ganador, j_perdedor = \
                Natacion().calcular_ganador(deportistas_natacion[0],
                                            deportistas_natacion[1], delegacion, enemigo)
            if empate:
                funciones.agregar_bitacora("Natacion", "EMPATE", "EMPATE")
            else:
                funciones.agregar_bitacora("Natacion", dele_ganadora.nombre, j_ganador.nombre)
        if not empate:
            self.premiar(dele_ganadora, dele_perdedora, j_ganador, j_perdedor, "Natacion")
        # Gimnasia
        # Mostramos quienes compiten
        print(f"\nGIMNASIA: {deportistas_gimnasia[0].nombre} vs {deportistas_gimnasia[1].nombre}\n")
        validez, empate, dele_ganadora, dele_perdedora, j_ganador, j_perdedor = \
            Gimnasia().validez_competencia(deportistas_gimnasia[0],
                                           deportistas_gimnasia[1], delegacion, enemigo)
        if validez:  # Si el juego es válido, ahora pueden lesionarse
            deportistas_gimnasia[0].lesionarse(Gimnasia().riesgo)
            deportistas_gimnasia[1].lesionarse(Gimnasia().riesgo)
            # Chequeamos condiciones nuevamente
            validez, empate, dele_ganadora, dele_perdedora, j_ganador, j_perdedor = \
                Gimnasia().validez_competencia(deportistas_gimnasia[0],
                                               deportistas_gimnasia[1], delegacion, enemigo)
        # Analizamos los valores retornados para bitácora y premiar
        if empate:
            funciones.agregar_bitacora("Gimnasia", "EMPATE", "EMPATE")
        elif not validez:
            funciones.agregar_bitacora("Gimnasia", dele_ganadora.nombre, j_ganador.nombre)
        else:
            empate, dele_ganadora, dele_perdedora, j_ganador, j_perdedor = \
                Gimnasia().calcular_ganador(deportistas_gimnasia[0],
                                            deportistas_gimnasia[1], delegacion, enemigo)
            if empate:
                funciones.agregar_bitacora("Gimnasia", "EMPATE", "EMPATE")
            else:
                funciones.agregar_bitacora("Gimnasia", dele_ganadora.nombre, j_ganador.nombre)
        if not empate:
            self.premiar(dele_ganadora, dele_perdedora, j_ganador, j_perdedor, "Gimnasia")
        # Ciclismo
        # Mostramos quienes compiten
        print(f"\nCICLISMO: {deportistas_ciclismo[0].nombre} vs {deportistas_ciclismo[1].nombre}\n")
        validez, empate, dele_ganadora, dele_perdedora, j_ganador, j_perdedor = \
            Ciclismo().validez_competencia(deportistas_ciclismo[0],
                                           deportistas_ciclismo[1], delegacion, enemigo)
        if validez:  # Si el juego es válido, ahora pueden lesionarse
            deportistas_ciclismo[0].lesionarse(Ciclismo().riesgo)
            deportistas_ciclismo[1].lesionarse(Ciclismo().riesgo)
            # Chequeamos condiciones nuevamente
            validez, empate, dele_ganadora, dele_perdedora, j_ganador, j_perdedor = \
                Ciclismo().validez_competencia(deportistas_ciclismo[0],
                                               deportistas_ciclismo[1], delegacion, enemigo)
        # Analizamos los valores retornados para bitácora y premiar
        if empate:
            funciones.agregar_bitacora("Ciclismo", "EMPATE", "EMPATE")
        elif not validez:
            funciones.agregar_bitacora("Ciclismo", dele_ganadora.nombre, j_ganador.nombre)
        else:
            empate, dele_ganadora, dele_perdedora, j_ganador, j_perdedor = \
                Ciclismo().calcular_ganador(deportistas_ciclismo[0],
                                            deportistas_ciclismo[1], delegacion, enemigo)
            if empate:
                funciones.agregar_bitacora("Ciclismo", "EMPATE", "EMPATE")
            else:
                funciones.agregar_bitacora("Ciclismo", dele_ganadora.nombre, j_ganador.nombre)
        if not empate:
            self.premiar(dele_ganadora, dele_perdedora, j_ganador, j_perdedor, "Ciclismo")

        self.dia_actual += 1  # Se acaba el día de competencia

    def premiar(self, delegacion_ganadora, delegacion_perdedora,
                ganador, perdedor, prueba):
        delegacion_ganadora.dinero += p.DINERO_GANADOR
        delegacion_ganadora.exelencia_y_respeto += p.PREMIO_EXE_RESP_GANADOR
        delegacion_ganadora.medallas += 1
        self.medallero[delegacion_ganadora.nombre] += 1
        if delegacion_ganadora.nombre == "IEEEsparta":
            self.medallas_esparta[prueba] += 1
        else:
            self.medallas_crotona[prueba] += 1
        delegacion_perdedora.exelencia_y_respeto -= p.BAJA_EXE_RESP_PERDEDOR
        ganador.moral += p.PREMIO_MORAL_GANADOR
        if delegacion_ganadora == "DCCrotona":  # Si gana un Crotona, doble moral.
            ganador.moral += (p.PREMIO_MORAL_GANADOR * 2)
        perdedor.moral -= p.BAJA_MORAL_PERDEDOR
        if delegacion_perdedora == "IEEEsparta":
            perdedor.moral -= (p.BAJA_MORAL_PERDEDOR * 2)  # Si pierde Esparta, moral baja doble

    def moral_delegaciones(self, delegacion, enemigo):
        print("\n--- MORAL DELEGACIONES ---\n")
        # Moral Delegación
        suma = 0
        for deportista in delegacion.equipo:
            suma += deportista.moral
        moral_delegacion = suma / len(delegacion.equipo)
        delegacion.moral = moral_delegacion
        print(f"Moral {delegacion.nombre}: {moral_delegacion}")
        # Moral Enemigo
        total = 0
        for deportista in enemigo.equipo:
            total += deportista.moral
        moral_enemigo = total / len(enemigo.equipo)
        enemigo.moral = moral_enemigo
        print(f"Moral {enemigo.nombre}: {moral_enemigo}")

    def actualizar_moral(self, delegacion, enemigo):
        # Actualiza la moral sin print
        # Moral Delegación
        suma = 0
        for deportista in delegacion.equipo:
            suma += deportista.moral
        moral_delegacion = suma / len(delegacion.equipo)
        delegacion.moral = moral_delegacion
        # Moral Enemigo
        total = 0
        for deportista in enemigo.equipo:
            total += deportista.moral
        moral_enemigo = total / len(enemigo.equipo)
        enemigo.moral = moral_enemigo

    def mostrar_estado(self, delegacion, enemigo):
        print("")
        print(19 * " "+"ESTADO DE LAS DELEGACIONES Y DEPORTISTAS")
        print(80 * "-")
        print("\n" + delegacion.nombre)
        print(f"\nEntreador: {delegacion.entrenador}")
        print(f"Moral del equipo: {delegacion.moral}")
        print(f"Medallas: {delegacion.medallas}")
        print(f"Dinero: {delegacion.dinero}")
        print(f"\nExelencia y respeto: {delegacion.exelencia_y_respeto}")
        print(f"Implementos deportivos: {delegacion.implementos_deportivos}")
        print(f"Implementos médicos: {delegacion.implementos_medicos}")
        print("\nEquipo deportivo\n")
        print(f"NOMBRE DEPORTISTA{15 * ' '}VELOCIDAD   RESISTENCIA"
              "  FLEXIBILIDAD   LESION\n")
        for d in delegacion.equipo:
            datos = [(d.nombre, d.velocidad, d.resistencia, d.flexibilidad, str(d.lesionado))]
            for n, v, r, f, l in datos:
                print(f"{n:35s}{v: <3.0f}{11 * ' '}{r: <3.0f}{10 * ' '}{f: <3.0f}{7 * ' '}{l:>s}")
        print("\n" + 80 * ":")
        print("\n" + enemigo.nombre)
        print(f"\nEntreador: {enemigo.entrenador}")
        print(f"Moral del equipo: {enemigo.moral}")
        print(f"Medallas: {enemigo.medallas}")
        print(f"Dinero: {enemigo.dinero}")
        print(f"\nExelencia y respeto: {enemigo.exelencia_y_respeto}")
        print(f"Implementos deportivos: {enemigo.implementos_deportivos}")
        print(f"Implementos médicos: {enemigo.implementos_medicos}")
        print("\nEquipo deportivo\n")
        print(f"NOMBRE DEPORTISTA{15 * ' '}VELOCIDAD   RESISTENCIA"
              "  FLEXIBILIDAD   LESION\n")
        for d in enemigo.equipo:
            datos = [(d.nombre, d.velocidad, d.resistencia, d.flexibilidad, str(d.lesionado))]
            for n, v, r, f, l in datos:
                print(f"{n:35s}{v: <3.0f}{11 * ' '}{r: <3.0f}{10 * ' '}{f: <3.0f}{7 * ' '}{l:>s}")
        print("\n" + 80 * "-")
        print(f"\nDía: {self.dia_actual}: Entrenamiento")
        print("\nMedallero\n")
        print("Deporte       IEEEsparta      DCCrotona")
        print(f"Atletismo{8 * ' '}{self.medallas_esparta['Atletismo']}{16 * ' '}"
              f"{self.medallas_crotona['Atletismo']}")
        print(f"Natacion{9 * ' '}{self.medallas_esparta['Natacion']}{16 * ' '}"
              f"{self.medallas_crotona['Natacion']}")
        print(f"Gimnasia{9 * ' '}{self.medallas_esparta['Gimnasia']}{16 * ' '}"
              f"{self.medallas_crotona['Gimnasia']}")
        print(f"Ciclismo{9 * ' '}{self.medallas_esparta['Ciclismo']}{16 * ' '}"
              f"{self.medallas_crotona['Ciclismo']}")
        print("\n" + 80 * "-")
