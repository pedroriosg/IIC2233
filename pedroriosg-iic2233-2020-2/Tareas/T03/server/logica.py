import json
from faker import Faker
from jugadores import Jugador
from catan import Catan
from random import choice


class Logica:

    def __init__(self, parent):

        self.parent = parent
        self.leer_parametros_json()

        # Intanciamos el Catan
        self.catan = Catan(self)

        self.lista_jugadores = []
        self.colores = ["rojo", "verde", "azul", "violeta"]
        self.cantidad_clientes = 0

    def crear_jugador(self, numero, socket):
        # Creamos el Jugador y asociamos el socekt correspondiente
        nombre = self.lista_nombres[numero]
        jugador = Jugador(self, nombre, socket)
        self.lista_jugadores.append(jugador)
        # Asignamos color al jugador
        color = choice(self.colores)
        self.asignar_color(jugador, color)
        self.colores.remove(color)
        self.parent.enviar({"comando": "armar_sala", "numero_jugadores":
                            self.n_jugadores}, jugador.socket_jugador)
        self.parent.enviar({"comando": "labels_propios_juego",
                            "info": jugador.enviar_informacion()}, jugador.socket_jugador)
        self.parent.enviar_a_todos({"comando": "actualizar_jugadores", "nombres_jugadores":
                                    [i.nombre for i in self.lista_jugadores]})

        return jugador

    def asignar_color(self, jugador, color):
        jugador.color = color

    def crear_nombres(self, numero_jugadores):
        # Este método crea numero_jugadpres nombres
        fake = Faker()
        self.lista_nombres = []
        for _ in range(numero_jugadores):
            existe = False
            while not existe:
                fake_nombre = fake.name()
                if fake_nombre not in self.lista_nombres:
                    self.lista_nombres.append(fake_nombre)
                    existe = True

    def comenzar_partida(self):
        # Una vez conectado el último jugador:
        # Definimos turnos
        # Enviamos nombres para intercambio
        self.parent.log("Servidor", "Comenzando Partida", "-")
        self.envio_nombres_intercambio()
        self.catan.definir_turnos()
        self.enviar_otros_labels()
        self.parent.enviar_a_todos({"comando": "comenzar_partida",
                                    "hexagonos": self.catan.mapa.envio_hexagonos(),
                                    "pos_nodos": self.catan.mapa.posicion_nodos})
        self.parent.enviar_a_todos({"comando": "crear_labels_choza_camino",
                                    "chozas": self.catan.mapa.envio_nodos(),
                                    "caminos": self.catan.mapa.envio_caminos()})

    def envio_nombres_intercambio(self):
        for jugador in self.lista_jugadores:
            self.parent.enviar({"comando": "nombres_intercambio",
                                "info": jugador.crear_nombres_otros()},
                               jugador.socket_jugador)

    def enviar_otros_labels(self):
        # Envía Labels de otros jugadores al usuario
        for jugador in self.lista_jugadores:
            self.parent.enviar({"comando": "labels_otros_juego",
                                "info": jugador.enviar_informacion_otros()},
                               jugador.socket_jugador)

    def manejar_mensaje(self, mensaje, jugador, lista_jugadores):
        try:
            comando = mensaje["comando"]
        except KeyError:
            return []

        lista_respuestas = []
        if comando == "lanzar_dado":
            dados = self.catan.lanzar_dado(jugador)
            respuesta = {"comando": "dps_lanzar",
                         "dados": dados}
            tup = ("grupal", respuesta)
            lista_respuestas.append(tup)
        elif comando == "pasar_turno":
            self.catan.pasar_turno()
        elif comando == "verificar_choza":
            resultado = self.catan.verificar(mensaje["identificacion_choza"])
            respuesta = {"comando": "choza_verificada",
                         "resultado": resultado,
                         "identificacion": mensaje["identificacion_choza"]}
            tup = ("grupal", respuesta)
            lista_respuestas.append(tup)
            self.catan.actualizar_a_todos()
        elif comando == "verificar_camino":
            resultado = self.catan.verificar_camino(mensaje["identificacion_camino"])
            respuesta = {"comando": "camino_verificado",
                         "resultado": resultado,
                         "identificacion": mensaje["identificacion_camino"]}
            tup = ("grupal", respuesta)
            lista_respuestas.append(tup)
            self.catan.actualizar_a_todos()
        elif comando == "comprar_carta":
            tipo = self.catan.sacar_carta(jugador)
            respuesta = {"comando": "venta_carta",
                         "tipo_carta": tipo}
            tup = ("individual", respuesta)
            lista_respuestas.append(tup)
        elif comando == "rpta_monopolio":
            self.catan.obtener_monopolio(jugador, mensaje["materia"])
            respuesta = {"comando": "dps_monopolio"}
            self.catan.actualizar_a_todos()
        elif comando == "querer_intercambiar":
            self.catan.verificar_intercambio(jugador, mensaje)
        elif comando == "resultado_solicitud":
            self.catan.oficializar_intercambio(jugador, mensaje)
        return lista_respuestas

    def leer_parametros_json(self):
        # Acá leemos el archivo JSON
        with open("parametros.json", "rb") as file:
            self.parametros = json.load(file)
            self.asignar_parametros(self.parametros)

    def asignar_parametros(self, parametros):
        self.host = parametros["HOST"]
        self.port = parametros["PORT"]
        self.n_jugadores = parametros["CANTIDAD_JUGADORES_PARTIDA"]


if __name__ == "__main__":
    logica = Logica()
    logica.leer_parametros_json()
