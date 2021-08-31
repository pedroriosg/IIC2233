import parametros as p
from abc import ABC, abstractmethod


class Deportes(ABC):

    def __init__(self):
        self.implemento = None
        self.riesgo = None

    def validez_competencia(self, j_delegacion, j_enemigo, delegacion, enemigo):
        validez = True
        empate = False
        dele_gandora = None
        dele_perdedora = None
        j_ganador = None
        j_perdedor = None
        if self.implemento:
            if delegacion.implementos_deportivos <= p.NIVEL_IMPLEMENTOS \
             and enemigo.implementos_deportivos <= p.NIVEL_IMPLEMENTOS:
                empate = True
                validez = False
                print("Ambas delegaciones sin implementos para competir")
            elif delegacion.implementos_deportivos <= p.NIVEL_IMPLEMENTOS \
                    and j_enemigo.lesionado:
                empate = True
                validez = False
                print("Delegacion sin implementos y enemigo lesionado")
            elif enemigo.implementos_deportivos <= p.NIVEL_IMPLEMENTOS \
                    and j_delegacion.lesionado:
                empate = True
                validez = False
                print("Delegacion enemiga sin implementos y jugador lesionado")
            elif j_delegacion.lesionado and j_enemigo.lesionado:
                empate = True
                validez = False
                print("Ambos jugadores lesionados")
            elif delegacion.implementos_deportivos <= p.NIVEL_IMPLEMENTOS:
                dele_gandora = enemigo
                dele_perdedora = delegacion
                j_ganador = j_enemigo
                j_perdedor = j_delegacion
                validez = False
                print("Delegacion sin implementos")
            elif j_delegacion.lesionado:
                dele_gandora = enemigo
                dele_perdedora = delegacion
                j_ganador = j_enemigo
                j_perdedor = j_delegacion
                validez = False
                print("Jugador lesionado")
            elif enemigo.implementos_deportivos <= p.NIVEL_IMPLEMENTOS:
                dele_gandora = delegacion
                dele_perdedora = enemigo
                j_ganador = j_delegacion
                j_perdedor = j_enemigo
                validez = False
                print("Delegacion enemiga sin implementos")
            elif j_enemigo.lesionado:
                dele_gandora = delegacion
                dele_perdedora = enemigo
                j_ganador = j_delegacion
                j_perdedor = j_enemigo
                validez = False
                print("Jugador enemigo lesionado")
        else:
            if j_delegacion.lesionado and j_enemigo.lesionado:
                empate = True
                validez = False
                print("Ambos jugadores lesionados")
            elif j_delegacion.lesionado:
                dele_gandora = enemigo
                dele_perdedora = delegacion
                j_ganador = j_enemigo
                j_perdedor = j_delegacion
                validez = False
                print("Jugador lesionado")
            elif j_enemigo.lesionado:
                dele_gandora = delegacion
                dele_perdedora = enemigo
                j_ganador = j_delegacion
                j_perdedor = j_enemigo
                validez = False
                print("Jugador enemigo lesionado")

        return validez, empate, dele_gandora, dele_perdedora, j_ganador, j_perdedor

    @abstractmethod
    def calcular_ganador():
        pass


class Atletismo(Deportes):

    def __init__(self):
        self.implemento = False
        self.riesgo = p.RIESGO_LEISON_ATLETISMO

    def calcular_ganador(self, j_delegacion, j_enemigo, delegacion, enemigo):
        empate = False
        dele_ganadora = None
        dele_perdedora = None
        j_ganador = None
        j_perdedor = None
        puntaje_delegacion = max(p.PUNTAJE_MINIMO,
                                 p.PONDERADOR_VELOCIDAD_ATLETISMO * j_delegacion.velocidad +
                                 p.PONDERADOR_RESISTENCIA_ATLETISMO * j_delegacion.resistencia +
                                 p.PONDERADOR_MORAL_ATLETISMO * j_delegacion.moral)
        puntaje_enemigo = max(p.PUNTAJE_MINIMO,
                              p.PONDERADOR_VELOCIDAD_ATLETISMO * j_enemigo.velocidad +
                              p.PONDERADOR_RESISTENCIA_ATLETISMO * j_enemigo.resistencia +
                              p.PONDERADOR_MORAL_ATLETISMO * j_enemigo.moral)
        if puntaje_delegacion > puntaje_enemigo:
            print("Ganaste la competencia de Atletismo compitiendo!")
            dele_ganadora = delegacion
            dele_perdedora = enemigo
            j_ganador = j_delegacion
            j_perdedor = j_enemigo
        elif puntaje_enemigo < puntaje_delegacion:
            print("Perdiste la competencia de Atletismo compitiendo!")
            dele_ganadora = enemigo
            dele_perdedora = delegacion
            j_ganador = j_enemigo
            j_perdedor = j_delegacion
        else:
            print("Empate compitiendo!")
            empate = True
        return empate, dele_ganadora, dele_perdedora, j_ganador, j_perdedor


class Natacion(Deportes):

    def __init__(self):
        self.implemento = False
        self.riesgo = p.RIESGO_LESION_NATACION

    def calcular_ganador(self, j_delegacion, j_enemigo, delegacion, enemigo):
        empate = False
        dele_ganadora = None
        dele_perdedora = None
        j_ganador = None
        j_perdedor = None
        puntaje_delegacion = max(p.PUNTAJE_MINIMO,
                                 p.PONDERADOR_VELOCIDAD_NATACION * j_delegacion.velocidad +
                                 p.PONDERADOR_RESISTENCIA_NATACION * j_delegacion.resistencia +
                                 p.PONDERADOR_FLEXIBILIDAD_NATACION * j_delegacion.flexibilidad)
        puntaje_enemigo = max(p.PUNTAJE_MINIMO,
                              p.PONDERADOR_VELOCIDAD_NATACION * j_enemigo.velocidad +
                              p.PONDERADOR_RESISTENCIA_NATACION * j_enemigo.resistencia +
                              p.PONDERADOR_FLEXIBILIDAD_NATACION * j_enemigo.flexibilidad)
        if puntaje_delegacion > puntaje_enemigo:
            print("Ganaste la competencia de Natacion compitiendo!")
            dele_ganadora = delegacion
            dele_perdedora = enemigo
            j_ganador = j_delegacion
            j_perdedor = j_enemigo
        elif puntaje_enemigo < puntaje_delegacion:
            print("Perdiste la competencia de Natacion compitiendo!")
            dele_ganadora = enemigo
            dele_perdedora = delegacion
            j_ganador = j_enemigo
            j_perdedor = j_delegacion
        else:
            print("Empate compitiendo!")
            empate = True
        return empate, dele_ganadora, dele_perdedora, j_ganador, j_perdedor


class Gimnasia(Deportes):

    def __init__(self):
        self.implemento = True
        self.riesgo = p.RIESGO_LESION_GIMNASIA

    def calcular_ganador(self, j_delegacion, j_enemigo, delegacion, enemigo):
        empate = False
        dele_ganadora = None
        dele_perdedora = None
        j_ganador = None
        j_perdedor = None
        puntaje_delegacion = max(p.PUNTAJE_MINIMO,
                                 p.PONDERADOR_FLEXIBILIDAD_GIMNASIA * j_delegacion.flexibilidad +
                                 p.PONDERADOR_RESISTENCIA_GIMNASIA * j_delegacion.resistencia +
                                 p.PONDERADOR_MORAL_GIMNASIA * j_delegacion.moral)
        puntaje_enemigo = max(p.PUNTAJE_MINIMO,
                              p.PONDERADOR_FLEXIBILIDAD_GIMNASIA * j_enemigo.flexibilidad +
                              p.PONDERADOR_RESISTENCIA_GIMNASIA * j_enemigo.resistencia +
                              p.PONDERADOR_MORAL_GIMNASIA * j_enemigo.moral)
        if puntaje_delegacion > puntaje_enemigo:
            print("Ganaste la competencia de Gimnasia compitiendo!")
            dele_ganadora = delegacion
            dele_perdedora = enemigo
            j_ganador = j_delegacion
            j_perdedor = j_enemigo
        elif puntaje_enemigo < puntaje_delegacion:
            print("Perdiste la competencia de Gimnasia compitiendo!")
            dele_ganadora = enemigo
            dele_perdedora = delegacion
            j_ganador = j_enemigo
            j_perdedor = j_delegacion
        else:
            print("Empate compitiendo!")
            empate = True
        return empate, dele_ganadora, dele_perdedora, j_ganador, j_perdedor


class Ciclismo(Deportes):

    def __init__(self):
        self.implemento = True
        self.riesgo = p.RIESGO_LESION_CICLISMO

    def calcular_ganador(self, j_delegacion, j_enemigo, delegacion, enemigo):
        empate = False
        dele_ganadora = None
        dele_perdedora = None
        j_ganador = None
        j_perdedor = None
        puntaje_delegacion = max(p.PUNTAJE_MINIMO,
                                 p.PONDERADOR_VELOCIDAD_CICLISMO * j_delegacion.velocidad +
                                 p.PONDERADOR_RESISTENCIA_CICLISMO * j_delegacion.resistencia +
                                 p.PONDERADOR_FLEXIBILIDAD_CICLISMO * j_delegacion.flexibilidad)
        puntaje_enemigo = max(p.PUNTAJE_MINIMO,
                              p.PONDERADOR_VELOCIDAD_CICLISMO * j_enemigo.velocidad +
                              p.PONDERADOR_RESISTENCIA_CICLISMO * j_enemigo.resistencia +
                              p.PONDERADOR_FLEXIBILIDAD_CICLISMO * j_enemigo.flexibilidad)
        if puntaje_delegacion > puntaje_enemigo:
            print("Ganaste la competencia de Ciclismo compitiendo!")
            dele_ganadora = delegacion
            dele_perdedora = enemigo
            j_ganador = j_delegacion
            j_perdedor = j_enemigo
        elif puntaje_enemigo < puntaje_delegacion:
            print("Perdiste la competencia de Ciclismo compitiendo!")
            dele_ganadora = enemigo
            dele_perdedora = delegacion
            j_ganador = j_enemigo
            j_perdedor = j_delegacion
        else:
            print("Empate compitiendo!")
            empate = True
        return empate, dele_ganadora, dele_perdedora, j_ganador, j_perdedor
