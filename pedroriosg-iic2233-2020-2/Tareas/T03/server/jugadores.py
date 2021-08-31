from random import choice


class Jugador:

    def __init__(self, parent, nombre, socket, log_activo=True):
        self.parent = parent
        self.log_activo = log_activo
        self.nombre = nombre
        self.socket_jugador = socket
        self.color = None
        self.arcilla = 0
        self.madera = 0
        self.trigo = 0
        self.puntos_victoria = self.parent.parametros["CHOZAS_INICIALES"] \
            + self.parent.parametros["CAMINOS_INICIALES"]
        self.cartas = 0
        self.turno = False
        self.carreteras = []
        self.largo_max_camino = 0

    def log(self, cliente, evento, detalle):
        if self.log_activo:
            print(f"{cliente:20s}|{evento:30s}|{detalle: >s}")

    def enviar_informacion(self):
        informacion = {"nombre": self.nombre, "color": self.color,
                       "arcilla": self.arcilla, "madera": self.madera,
                       "trigo": self.trigo, "puntos": self.puntos_victoria + self.cartas,
                       "cartas": self.cartas, "turno": self.turno}
        return informacion

    def enviar_informacion_otros(self):
        # Genera informacion de los demás jugadores
        info_final = []
        for jugador in self.parent.lista_jugadores:
            if jugador.nombre != self.nombre:
                info_personal = jugador.enviar_informacion()
                info_final.append(info_personal)
        return info_final

    def sumar_materia(self, materia):
        if materia == "arcilla":
            self.arcilla += self.parent.parametros["GANANCIA_MATERIA_PRIMA"]
        elif materia == "madera":
            self.madera += self.parent.parametros["GANANCIA_MATERIA_PRIMA"]
        elif materia == "trigo":
            self.trigo += self.parent.parametros["GANANCIA_MATERIA_PRIMA"]
        self.log(self.nombre, "Recibiendo Recursos",
                 f"{self.parent.parametros['GANANCIA_MATERIA_PRIMA']} {materia}")

    def construir_choza(self):
        if self.arcilla >= self.parent.parametros["CANTIDAD_ARCILLA_CHOZA"] and \
            self.madera >= self.parent.parametros["CANTIDAD_MADERA_CHOZA"] and \
                self.trigo >= self.parent.parametros["CANTIDAD_TRIGO_CHOZA"]:

            self.arcilla -= self.parent.parametros["CANTIDAD_ARCILLA_CHOZA"]
            self.madera -= self.parent.parametros["CANTIDAD_MADERA_CHOZA"]
            self.trigo -= self.parent.parametros["CANTIDAD_TRIGO_CHOZA"]
            self.puntos_victoria += 1
            return True
        else:
            return False

    def construir_camino(self):
        if self.arcilla >= self.parent.parametros["CANTIDAD_ARCILLA_CARRETERA"] and \
         self.madera >= self.parent.parametros["CANTIDAD_MADERA_CARRETERA"]:
            self.arcilla -= self.parent.parametros["CANTIDAD_ARCILLA_CARRETERA"]
            self.madera -= self.parent.parametros["CANTIDAD_MADERA_CARRETERA"]
            self.puntos_victoria += 1
            return True
        else:
            return False

    def verificar_carta(self):
        a = self.parent.parametros["CANTIDAD_ARCILLA_CARTA_DESARROLLO"]
        b = self.parent.parametros["CANTIDAD_MADERA_CARTA_DESARROLLO"]
        c = self.parent.parametros["CANTIDAD_TRIGO_CARTA_DESARROLLO"]
        if self.arcilla >= a and self.madera >= b and self.trigo >= c:
            self.arcilla -= a
            self.madera -= b
            self.trigo -= c
            return True
        else:
            return False

    def devolver_mitad_cartas(self):
        diccionario = {"arcilla": self.arcilla, "madera": self.madera,
                       "trigo": self.trigo}
        suma = self.arcilla + self.madera + self.trigo
        iteracion = round(suma/2)
        contador = 0
        if suma >= 8:
            while contador < iteracion:
                lista = ["arcilla", "madera", "trigo"]
                carta = choice(lista)
                if diccionario[carta] != 0:
                    diccionario[carta] -= 1
                    contador += 1
            self.arcilla = diccionario["arcilla"]
            self.madera = diccionario["madera"]
            self.trigo = diccionario["trigo"]

    def crear_nombres_otros(self):
        nombres = []
        for jugador in self.parent.lista_jugadores:
            if jugador.nombre != self.nombre:
                nombres.append(jugador.nombre)
        return nombres

    def realizar_intercambio(self, mensaje):
        materia = ["arcilla", "madera", "trigo"]
        restar = mensaje["materia_ofrecida"]
        if materia[restar] == "arcilla":
            self.arcilla -= mensaje["cantidad_ofrecida"]
        elif materia[restar] == "madera":
            self.madera -= mensaje["cantidad_ofrecida"]
        elif materia[restar] == "trigo":
            self.trigo -= mensaje["cantidad_ofrecida"]
        sumar = mensaje["materia_pedida"]
        if materia[sumar] == "arcilla":
            self.arcilla += mensaje["cantidad_pedida"]
        elif materia[sumar] == "madera":
            self.madera += mensaje["cantidad_pedida"]
        elif materia[sumar] == "trigo":
            self.trigo += mensaje["cantidad_pedida"]

    def calcular_carretera(self):
        carretera = 1
        visitados = []
        limite = 0
        while limite < 2:
            for camino in self.carreteras:
                for nodo in camino.nodos_que_conecta:
                    existe = self.ver_si_camino_conecta(nodo, camino, visitados)
                    if camino not in visitados:
                        visitados.append(camino)
                    if not existe:
                        limite += 1
                    else:
                        carretera += 1
        if carretera > self.largo_max_camino:
            self.largo_max_camino = carretera

        return self.largo_max_camino

    def ver_si_camino_conecta(self, nodo, camino, visitados):
        conecta = False
        for cam in self.carreteras:
            if (nodo in cam.nodos_que_conecta) and (cam != camino) and (cam not in visitados):
                conecta = True

        return conecta
