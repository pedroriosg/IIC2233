import json
import socket
import threading
from logica import Logica
from time import sleep


class Servidor:

    def __init__(self, log_activo=True):

        # Nos va a permitir imprimir
        self.log_activo = log_activo
        self.log("Usuario", "Evento", "Detalles")
        self.log(20 * "-", 30 * "-", 20 * "-")

        # Creamos la lógica del juego
        self.logica = Logica(self)

        # HOST Y PORT
        self.host = self.logica.host
        self.port = self.logica.port

        # Cantidad de Jugadores
        self.n_jugadores = self.logica.n_jugadores

        # Creamos esa cantidad de nombres
        self.logica.crear_nombres(self.n_jugadores)

        # Lista que almacena Jugadores
        self.lista_jugadores = []

        # Creamos socket (IPv4, TCP)
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.log("Servidor", "Inicialización", "-")

        # Establecemos la conexión
        self.socket_servidor.bind((self.host, self.port))
        # Escuchamos
        self.socket_servidor.listen()
        self.log("Servidor", "Escuchando", f"{self.host} : {self.port}")
        self.aceptar_clientes()
        self.log("Servidor",  "Aceptando conexiones", "-")

    def log(self, cliente, evento, detalle):
        if self.log_activo:
            print(f"{cliente:20s}|{evento:30s}|{detalle: >s}")

    def aceptar_clientes(self):
        # Acá aceptamos n_jugadores clientes
        self.aceptar = True
        while True:
            while self.aceptar:
                socket_cliente, address_cliente = self.socket_servidor.accept()

                # Creamos el Jugador y asociamos el socekt correspondiente
                # cantidad_clientes, permite elegir el nombre del jugador
                jugador = self.logica.crear_jugador(self.logica.cantidad_clientes, socket_cliente)
                self.log(jugador.nombre, "Se conecta", "-")
                self.log(jugador.nombre, "Ingresa a Sala Espera", "-")

                # Creamos e iniciamos Thread que escucha al cliente
                thread_escuchar_jugador = threading.Thread(target=self.escuchar_cliente,
                                                           args=(jugador, ), daemon=True)
                thread_escuchar_jugador.start()
                self.logica.cantidad_clientes += 1

                # Revisamos condición para aceptar clientes
                if self.logica.cantidad_clientes == self.logica.n_jugadores:
                    self.log("Servidor", "Sala llena", "Inciaremos partida")
                    sleep(2)
                    self.logica.comenzar_partida()
                    self.aceptar = False

            while not self.aceptar:
                socket_cliente, address_cliente = self.socket_servidor.accept()
                self.log("SIN NOMBRE", "Conectarse", "Error")
                self.enviar({"comando": "espacio_no_disponible"}, socket_cliente)

    def escuchar_cliente(self, jugador):
        try:
            while True:
                mensaje = self.recibir(jugador.socket_jugador)
                self.log(jugador.nombre, mensaje["comando"], "-")
                lista_respuestas = self.logica.manejar_mensaje(mensaje, jugador,
                                                               self.logica.lista_jugadores)

                self.enviar_lista_respuestas(jugador, lista_respuestas)

        except ConnectionError:
            self.log(f"Error: conexión con {jugador} fue reseteada")

    def enviar_lista_respuestas(self, jugador, lista_respuestas):
        """Envía las respuestas a los clientes respectivos.

        Argumentos:
            jugador (Jugador): El jugador actual del cual se recibió el mensaje inicial
            lista_respuestas (lista de tuplas): Las respuestas a enviar retornadas por
              manejar_mensaje, clasificadas en una tupla según su destino
        """
        for tup in lista_respuestas:
            msg = tup[1]
            if tup[0] == "grupal":
                self.enviar_a_todos(msg)
            elif tup[0] == "individual":
                self.enviar(msg, jugador.socket_jugador)

    def enviar(self, mensaje, socket_cliente):
        """Envía un mensaje a un cliente.

        Argumentos:
            mensaje (dict): Contiene la información a enviar. Debe ser serializable.
            socket_cliente (socket): El socket objetivo al cual enviar el mensaje.
        """
        # Completar
        msg = self.codificar_mensaje(mensaje)
        largo_msg = len(msg).to_bytes(4, byteorder='big')
        bytes_leidos = bytearray()
        a_enviar = bytearray(largo_msg)
        contador = 1
        posicion = 0
        cero = 0
        while len(bytes_leidos) < len(msg):
            numero = contador.to_bytes(4, byteorder="little")
            tamaño = min(60, len(msg) - len(bytes_leidos))
            chunk = msg[posicion: posicion + tamaño]
            posicion += tamaño
            a_enviar += numero
            a_enviar += chunk
            bytes_leidos += chunk
            contador += 1
            if tamaño != 60:
                final = cero.to_bytes(60 - tamaño, byteorder="little")
                a_enviar += final

        socket_cliente.sendall(a_enviar)

    def recibir(self, socket_cliente):
        """Recibe un mensaje del cliente.

        Recibe el mensaje, lo decodifica usando el protocolo establecido,
        y lo des-serializa (via decodificar_mensaje).

        Argumentos:
            socket_cliente (socket): El socket del cliente del cual recibir.

        Retorna:
            dict: contiene el mensaje, después de ser decodificado.
        """
        # Completar
        largo_mensaje_bytes = socket_cliente.recv(4)
        largo_mensaje = int.from_bytes(largo_mensaje_bytes, byteorder='big')
        bytes_leidos = bytearray()
        parte_entera = largo_mensaje // 60
        for _ in range(parte_entera):
            numero = socket_cliente.recv(4)
            respuesta = socket_cliente.recv(60)
            bytes_leidos += respuesta
        if (largo_mensaje % 60) != 0:
            number = socket_cliente.recv(4)
            response = socket_cliente.recv(largo_mensaje % 60)
            sobran = socket_cliente.recv(60 - (largo_mensaje % 60))
            bytes_leidos += response

        mensaje = self.decodificar_mensaje(bytes_leidos)

        return mensaje

    def enviar_a_todos(self, mensaje):
        """Envía mensaje a todos los usuarios conectados.

        Argumentos:
            mensaje (dict): Contiene la información a enviar. Debe ser serializable.
        """
        for jugador in self.logica.lista_jugadores:
            try:
                self.enviar(mensaje, jugador.socket_jugador)
            except ConnectionError:
                # self.eliminar_cliente(jugador)
                pass

    @staticmethod
    def codificar_mensaje(mensaje):
        """Codifica y serializa un mensaje usando JSON.

        Argumentos:
            mensaje (dict): Contiene llaves de strings, con información útil a enviar a cliente.
              Los valores del diccionario deben ser serializables.

        Retorna:
            bytes: El mensaje serializado
        """
        try:
            # Creamos el objeto JSON
            json_mensaje = json.dumps(mensaje)
            # Codificamos el objeto JSON
            bytes_mensaje = json_mensaje.encode()

            return bytes_mensaje

        except json.JSONDecodeError:
            print("No se pudo codificar el mensaje")
            return b""

    @staticmethod
    def decodificar_mensaje(bytes_mensaje):
        """Decodifica y des-serializa bytes usando JSON.

        Argumentos:
            bytes_mensaje (bytes): Representa el mensaje serializado. Debe ser des-serializable
                y decodificable.

        Retorna:
            dict: El mensaje des-serializado, en su forma original.
        """
        try:
            mensaje = json.loads(bytes_mensaje)
            return mensaje
        except json.JSONDecodeError:
            print("No se pudo decodificar el mensaje")
            return dict()
