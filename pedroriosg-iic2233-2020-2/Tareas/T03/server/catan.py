from threading import Lock
from mapa import Mapa
from random import choice, randint, sample
from generador_de_cartas import sacar_cartas


class Catan():

    def __init__(self, parent, log_activo=True):
        self.parent = parent
        self.log_activo = log_activo
        self.mapa = Mapa(parent)
        self.turnos = []
        self.cambia_turnos = 0
        self.condicion = True
        self.jugador_carretera_mas_larga = None

        # Creamos Lock para poblar el mapa
        self.lock = Lock()

    def log(self, cliente, evento, detalle):
        if self.log_activo:
            print(f"{cliente:20s}|{evento:30s}|{detalle: >s}")

    def definir_turnos(self):
        jugadores = self.parent.lista_jugadores.copy()
        for _ in range(len(self.parent.lista_jugadores)):
            eleccion = choice(jugadores)
            self.turnos.append(eleccion)
            jugadores.remove(eleccion)
        self.log("Servidor", "Definiendo Turnos", str([i.nombre for i in self.turnos]))
        self.poblar_servidor()
        self.jugadas()

    def poblar_servidor(self):
        self.lock.acquire()
        # Funcion que elige chozas y caminos inicales para los jugadores
        for jugador in self.turnos:
            confirmados = 0
            while confirmados < self.parent.parametros["CHOZAS_INICIALES"]:
                nodo = choice(list(self.mapa.nodos_dict.values()))
                # Si está disponible
                if nodo.estado:
                    # Revisamos adyacentes
                    se_puede = True
                    for adyacente in nodo.nodos_adyacentes:
                        if not self.mapa.nodos_dict[adyacente].estado:
                            se_puede = False
                    if se_puede:
                        self.mapa.nodos_dict[nodo._id].ocupar_nodo(jugador)
                        confirmados += 1
                        self.log(jugador.nombre, "Nodo Ocupado", nodo._id)
            confirmados = 0
            while confirmados < self.parent.parametros["CAMINOS_INICIALES"]:
                lista_caminos = sample(self.mapa.caminos, len(self.mapa.caminos))
                for camino in lista_caminos:
                    for adyacente in camino.nodos_que_conecta:
                        if not self.mapa.nodos_dict[adyacente].estado and \
                           self.mapa.nodos_dict[adyacente].usuario == jugador and \
                           confirmados < self.parent.parametros["CAMINOS_INICIALES"]:
                            camino.ocupar_camino(jugador)
                            jugador.carreteras.append(camino)
                            self.log(jugador.nombre, "Camino Ocupado",
                                     str(camino.nodos_que_conecta))
                            confirmados += 1
                        else:
                            for road in self.mapa.caminos:
                                if adyacente in road.nodos_que_conecta:
                                    if road.usuario == jugador:
                                        for ocu in self.mapa.caminos:
                                            if ocu.nodos_que_conecta == camino.nodos_que_conecta \
                                             and confirmados < \
                                             self.parent.parametros["CAMINOS_INICIALES"] and \
                                             ocu.estado:
                                                ocu.ocupar_camino(jugador)
                                                jugador.carreteras.append(ocu)
                                                jugador.calcular_carretera()
                                                confirmados += 1
                                                self.log(jugador.nombre, "Camino Ocupado",
                                                         str(camino.nodos_que_conecta))
        self.lock.release()
        self.carretera_mas_larga()
        self.repartir_inicio()

    def jugadas(self):
        if self.condicion:
            juega = self.turnos[self.cambia_turnos]
            self.parent.parent.enviar_a_todos({"comando": "cambiar_turno",
                                               "nombre_jugador": juega.nombre,
                                               "color": juega.color})
            self.parent.parent.enviar({"comando": "mi_turno"}, juega.socket_jugador)
            self.log(juega.nombre, "Comenzando Turno", "-")

        else:
            self.fin_partida()

    def pasar_turno(self):
        self.cambia_turnos += 1
        if self.cambia_turnos == len(self.turnos):
            self.cambia_turnos = 0
        self.revisar_termino()
        self.jugadas()

    def revisar_termino(self):
        for jugador in self.parent.lista_jugadores:
            suma = jugador.puntos_victoria + jugador.cartas
            if suma >= self.parent.parametros["PUNTOS_PARA_VICTORIA"]:
                campeon = jugador
                self.condicion = False
                self.log(campeon.nombre, "Gana DCColonos", "-")

    def lanzar_dado(self, jugador):
        dados = [randint(1, 6) for _ in range(2)]
        suma = dados[0] + dados[1]
        self.parent.parent.log(jugador.nombre, "Lanzar dados", f"Resultado: {str(suma)}")
        self.repartir_suma(suma)
        return dados

    def repartir_suma(self, suma):
        for jugador in self.parent.lista_jugadores:
            for hexagono in self.mapa.hexagonos:
                if hexagono.numero == suma:
                    for nodo in hexagono.nodos:
                        if self.mapa.nodos_dict[nodo].usuario == jugador:
                            jugador.sumar_materia(hexagono.materia_prima)
        if suma == self.parent.parametros["FICHA_EXEPCION"]:
            for jugador in self.parent.lista_jugadores:
                jugador.devolver_mitad_cartas()

        self.actualizar_a_todos()

    def repartir_inicio(self):
        for jugador in self.parent.lista_jugadores:
            for hexagono in self.mapa.hexagonos:
                for nodo in hexagono.nodos:
                    if self.mapa.nodos_dict[nodo].usuario == jugador:
                        jugador.sumar_materia(hexagono.materia_prima)
        self.actualizar_a_todos()

    def actualizar_a_todos(self):
        for jugador in self.parent.lista_jugadores:
            self.parent.parent.enviar({"comando": "actualizar_todo",
                                       "info_personal": jugador.enviar_informacion(),
                                       "info_grupal": jugador.enviar_informacion_otros()},
                                      jugador.socket_jugador)

    def verificar(self, info_choza):
        se_puede = True
        ide = info_choza[0]
        color = info_choza[1]
        choza = self.mapa.nodos_dict[ide]
        for nodo in choza.nodos_adyacentes:
            if self.mapa.nodos_dict[nodo].color is not None:
                se_puede = False
        # Buscamos al jugador
        for jug in self.parent.lista_jugadores:
            if jug.color == color:
                jugador = jug
        # Revisemos las cartas del jugador
        if se_puede:
            resultado = jugador.construir_choza()
            se_puede = resultado
        if se_puede:
            self.mapa.nodos_dict[ide].ocupar_nodo(jugador)
            self.log(jugador.nombre, "Comprar Choza", f"Nodo: {ide}")
        self.parent.parent.enviar({"comando": "warning", "resultado": se_puede},
                                  jugador.socket_jugador)
        return se_puede

    def verificar_camino(self, info_camino):
        se_puede = False
        ide = info_camino[0]
        color = info_camino[1]
        for jug in self.parent.lista_jugadores:
            if jug.color == color:
                jugador = jug
        for camino in self.mapa.caminos:
            if camino._id == ide:
                for adyacente in camino.nodos_que_conecta:
                    if self.mapa.nodos_dict[adyacente].usuario == jugador:
                        se_puede = True
                    else:
                        for cami in self.mapa.caminos:
                            if adyacente in cami.nodos_que_conecta:
                                if cami.usuario == jugador:
                                    se_puede = True

        # Revisemos las cartas del jugador
        if se_puede:
            resultado = jugador.construir_camino()
            se_puede = resultado
        if se_puede:
            for camino in self.mapa.caminos:
                if camino._id == ide:
                    camino.ocupar_camino(jugador)
                    jugador.carreteras.append(camino)
                    jugador.calcular_carretera()
                    self.carretera_mas_larga()
            self.log(jugador.nombre, "Comprar Camino", f"Camino: {ide}")
        self.parent.parent.enviar({"comando": "warning", "resultado": se_puede},
                                  jugador.socket_jugador)
        return se_puede

    def sacar_carta(self, jugador):
        resultado = jugador.verificar_carta()
        if resultado:
            carta = sacar_cartas(1)
            tipo = carta[0][0]
            if tipo == "victoria":
                self.log(jugador.nombre, "Compra Punto de Victoria", "-")
                jugador.cartas += 1
                self.actualizar_a_todos()
            elif tipo == "monopolio":
                pass
            return tipo

    def obtener_monopolio(self, jugador, materia):
        suma = 0
        for jug in self.parent.lista_jugadores:
            if jug != jugador:
                if materia == "arcilla":
                    suma += jug.arcilla
                    jug.arcilla = 0
                elif materia == "madera":
                    suma += jug.madera
                    jug.madera = 0
                elif materia == "trigo":
                    suma += jug.trigo
                    jug.trigo = 0
        if materia == "arcilla":
            jugador.arcilla += suma
        elif materia == "madera":
            jugador.madera += suma
        elif materia == "trigo":
            jugador.trigo += suma
        self.log(jugador.nombre, "Obteniendo Monopolio", materia)

    def verificar_intercambio(self, jugador, mensaje):
        se_puede = True
        lista = ["arcilla", "madera", "trigo"]
        self.log(jugador.nombre, f"Solicita Intercambio a {mensaje['jugador']}",
                 f"{mensaje['cantidad_ofrecida']} {lista[mensaje['materia_ofrecida']]} \
                 a cambio de {mensaje['cantidad_pedida']} {lista[mensaje['materia_pedida']]}")
        # Obtenemos el jugador con quien queremos intercambiar
        for jug in self.parent.lista_jugadores:
            if jug.nombre == mensaje["jugador"]:
                player = jug
        # Vemos las cartas ahora | Quiere intercambiar
        materia_ofrecida = lista[mensaje["materia_ofrecida"]]
        materia_pedida = lista[mensaje["materia_pedida"]]
        if materia_ofrecida == "arcilla":
            if jugador.arcilla < mensaje["cantidad_ofrecida"]:
                se_puede = False
        elif materia_ofrecida == "madera":
            if jugador.madera < mensaje["cantidad_ofrecida"]:
                se_puede = False
        elif materia_ofrecida == "trigo":
            if jugador.trigo < mensaje["cantidad_ofrecida"]:
                se_puede = False
        if materia_pedida == "arcilla":
            if player.arcilla < mensaje["cantidad_pedida"]:
                se_puede = False
        elif materia_pedida == "madera":
            if player.madera < mensaje["cantidad_pedida"]:
                se_puede = False
        elif materia_pedida == "trigo":
            if player.trigo < mensaje["cantidad_pedida"]:
                se_puede = False
        if se_puede:
            self.parent.parent.enviar({"comando": "aceptar_intercambio",
                                      "info": mensaje,
                                       "nombre": jugador.nombre}, player.socket_jugador)
        else:
            self.parent.parent.enviar({"comando": "intercambio_no_apto"},
                                      jugador.socket_jugador)
        return se_puede

    def oficializar_intercambio(self, jugador, mensaje):
        solicitud = mensaje["resultado"]
        a = mensaje["info"]["info"]
        lista = ["arcilla", "madera", "trigo"]
        # Buscamos al jugador que ofrece
        for jug in self.parent.lista_jugadores:
            if jug.nombre == mensaje["info"]["nombre"]:
                player = jug
        if solicitud == "aceptada":
            # Buscamos al jugador que ofrece
            player.realizar_intercambio(mensaje["info"]["info"])
            new_info = {"comando": "querer_intercambiar", "materia_ofrecida": a["materia_pedida"],
                        "cantidad_ofrecida": a["cantidad_pedida"],
                        "materia_pedida": a["materia_ofrecida"],
                        "cantidad_pedida": a["cantidad_ofrecida"], "jugador": 'Taylor Mercer'}
            jugador.realizar_intercambio(new_info)
            self.parent.parent.enviar({"comando": "intercambio_final",
                                      "resultado": "exitoso"}, player.socket_jugador)
        else:
            self.parent.parent.enviar({"comando": "intercambio_final",
                                      "resultado": "fracasado"}, player.socket_jugador)
        self.log(jugador.nombre, f"Contesta Intercambio a {player.nombre} ({solicitud})",
                 f"{a['cantidad_ofrecida']} {lista[a['materia_ofrecida']]} \
                 a cambio de {a['cantidad_pedida']} {lista[a['materia_pedida']]}")
        self.actualizar_a_todos()

    def fin_partida(self):
        for jugador in self.parent.lista_jugadores:
            # Enviamos nombres a la sala de fin
            msg = {"comando": "nombre_fin", "info": jugador.nombre}
            self.parent.parent.enviar(msg, jugador.socket_jugador)

        resultados = []
        for jugador in self.parent.lista_jugadores:
            info_personal = (jugador.nombre, jugador.puntos_victoria)
            resultados.append(info_personal)
        mesg = {"comando": "resultados", "info": resultados}
        self.parent.parent.enviar_a_todos(mesg)

    def carretera_mas_larga(self):
        informacion = [[jugador, jugador.calcular_carretera()]
                       for jugador in self.parent.lista_jugadores]
        informacion.sort(key=lambda x: x[1])
        ultimo = informacion.pop()
        penultimo = informacion.pop()
        if ultimo[1] > penultimo[1]:
            self.log(ultimo[0].nombre, "Obtiene carretera más larga", f"Largo: {ultimo[1]}")
            self.restar_carretera_larga()
            self.jugador_carretera_mas_larga = ultimo[0]
            self.actualizar_carretera(ultimo[0])
            self.sumar_carretera_larga()
        else:
            self.parent.parent.enviar_a_todos({"comando": "empate_carretera"})
            self.restar_carretera_larga()
            self.jugador_carretera_mas_larga = None

        self.actualizar_a_todos()

    def actualizar_carretera(self, jugador):
        info = (jugador.nombre, jugador.color)
        self.parent.parent.enviar_a_todos({"comando": "carretera", "info": info})

    def restar_carretera_larga(self):
        if self.jugador_carretera_mas_larga is not None:
            self.jugador_carretera_mas_larga.puntos_victoria -= 2

    def sumar_carretera_larga(self):
        self.jugador_carretera_mas_larga.puntos_victoria += 2
