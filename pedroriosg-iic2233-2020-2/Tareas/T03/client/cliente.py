import json
import threading
import socket
from controlador import Controlador


class Cliente:

    def __init__(self, log_activo=True):

        # Inicializar UI
        self.controlador = Controlador(self)

        self.host = self.controlador.host
        self.port = self.controlador.port

        self.log_activo = log_activo
        self.log("Usuario", "Evento", "Detalles")
        self.log(20 * "-", 30 * "-", 20 * "-")
        self.log("Cliente", "Inicialización", "-")

        # Creamos socket (IPv4, TCP)
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Conectarse con el servidor
            self.socket_cliente.connect((self.host, self.port))
            self.conectado = True
            self.log("Servidor", "Acepta conexion", "-")

            # Escuchar los mensajes del servidor
            thread = threading.Thread(target=self.escuchar_servidor, daemon=True)
            thread.start()

        except ConnectionError:
            print(f"No se pudo conectar a {self.host}:{self.port}")
            self.socket_cliente.close()

    def log(self, cliente, evento, detalle):
        if self.log_activo:
            print(f"{cliente:20s}|{evento:30s}|{detalle: >s}")

    def escuchar_servidor(self):
        try:
            # Completar
            while self.conectado:
                mensaje = self.recibir()
                self.log("Servidor", "Mensaje recibido", mensaje["comando"])
                self.controlador.manejar_mensaje(mensaje)
        except ConnectionError:
            print("Error de conexión con el servidor")
        finally:
            self.socket_cliente.close()

    def enviar(self, mensaje):
        """Envía un mensaje a un cliente.

        Argumentos:
            mensaje (dict): Contiene la información a enviar. Debe ser serializable.
            socket_cliente (socket): El socket objetivo al cual enviar el mensaje.
        """
        try:
            # Completar
            msg = self.codificar_mensaje(mensaje)
            largo_msg = len(msg).to_bytes(4, byteorder='big')
            bytes_leidos = bytearray()
            a_enviar = bytearray(largo_msg)
            cero = 0
            contador = 1
            posicion = 0
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

            self.socket_cliente.sendall(a_enviar)
            self.log("Cliente", mensaje['comando'], "-")

        except ConnectionError:
            self.socket_cliente.close()

    def recibir(self):
        """Recibe un mensaje del servidor.

        Recibe el mensaje, lo decodifica usando el protocolo establecido,
        y lo des-serializa (via decodificar_mensaje).

        Retorna:
            dict: contiene el mensaje, después de ser decodificado.
        """
        # Completar
        largo_mensaje_bytes = self.socket_cliente.recv(4)
        largo_mensaje = int.from_bytes(largo_mensaje_bytes, byteorder='big')
        bytes_leidos = bytearray()
        parte_entera = largo_mensaje // 60
        for _ in range(parte_entera):
            numero = self.socket_cliente.recv(4)
            respuesta = self.socket_cliente.recv(60)
            bytes_leidos += respuesta
        if (largo_mensaje % 60) != 0:
            number = self.socket_cliente.recv(4)
            response = self.socket_cliente.recv(largo_mensaje % 60)
            sobran = self.socket_cliente.recv(60 - (largo_mensaje % 60))
            bytes_leidos += response

        mensaje = self.decodificar_mensaje(bytes_leidos)
        return mensaje

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
            # Create JSON object
            json_mensaje = json.dumps(mensaje)
            # Encode JSON object
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
