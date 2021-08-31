import os

from collections import deque
from cargar_archivos import cargar_aeropuertos, cargar_conexiones
from entidades import Aeropuerto, Conexion


UMBRAL = 40000


class RedesMundiales:

    def __init__(self):
        # Estructura donde se guardaran los aeropuertos
        # Cada llave es un id y el valor es una instancia de Aeropuerto
        self.aeropuertos = {}

    def agregar_aeropuerto(self, aeropuerto_id, nombre):
        # Agregar un aeropuerto a la estructura
        aeropuerto = Aeropuerto(aeropuerto_id, nombre)
        self.aeropuertos[aeropuerto_id] = aeropuerto

    def agregar_conexion(self, aeropuerto_id_partida, aeropuerto_id_llegada, infectados):
        # Crear la conexion de partida-llegada para el par de aeropuertos
        if aeropuerto_id_partida in self.aeropuertos and aeropuerto_id_llegada in self.aeropuertos:
            existe = False
            aeropuerto = self.aeropuertos[aeropuerto_id_partida]
            conexiones = aeropuerto.conexiones
            for conect in conexiones:
                if conect.aeropuerto_llegada_id == aeropuerto_id_llegada:
                    existe = True
            if not existe:
                conection = Conexion(aeropuerto_id_partida, aeropuerto_id_llegada, infectados)
                aeropuerto.conexiones.append(conection)

    def cargar_red(self, ruta_aeropuertos, ruta_conexiones):

        # Primero se crean todos los aeropuertos
        for aeropuerto_id, nombre in cargar_aeropuertos(ruta_aeropuertos):
            self.agregar_aeropuerto(aeropuerto_id, nombre)

        # Después generamos las conexiones
        for id_partida, id_salida, infectados in cargar_conexiones(ruta_conexiones):
            self.agregar_conexion(id_partida, id_salida, infectados)

    def eliminar_conexion(self, conexion):
        id_partida = conexion.aeropuerto_inicio_id
        id_llegada = conexion.aeropuerto_llegada_id
        aeropuerto_inicio = self.aeropuertos.get(id_partida)
        for c in aeropuerto_inicio.conexiones:
            if c.aeropuerto_llegada_id == id_llegada:
                aeropuerto_inicio.conexiones.remove(c)
                break

    def eliminar_aeropuerto(self, aeropuerto_id):
        if aeropuerto_id not in self.aeropuertos:
            raise ValueError(f"No puedes eliminar un aeropuerto que no existe ({aeropuerto_id})")
        if self.aeropuertos[aeropuerto_id].conexiones:
            raise ValueError(f"No puedes eliminar un aeropuerto con conexiones ({aeropuerto_id})")
        del self.aeropuertos[aeropuerto_id]

    def infectados_generados_desde_aeropuerto(self, aeropuerto_id):
        # Muestra la cantidad de infectados generados por un aeropuerto
        aeropuerto = self.aeropuertos[aeropuerto_id]
        totally = 0
        visitados = []
        # La cola de siempre, comienza desde el nodo inicio.
        queue = deque([aeropuerto_id])
        # Usamos BFS
        while len(queue) > 0:
            id_ = queue.popleft()
            # Detalle clave: si ya visitamos el nodo, no hacemos nada!
            if id_ in visitados:
                continue
            # Lo visitamos
            visitados.append(id_)
            # Agregamos los vecinos a la cola si es que no han sido visitados.
            for conexion in self.aeropuertos[id_].conexiones:
                totally += conexion.infectados
                nuevo_id = conexion.aeropuerto_llegada_id
                if nuevo_id not in visitados:
                    queue.append(nuevo_id)
        print(f"La cantidad estimada de infectados generados por el aeropuerto {aeropuerto.nombre} es de {totally}")
        return totally

    def verificar_candidatos(self, ruta_aeropuertos_candidatos, ruta_conexiones_candidatas):
        # Se revisa cada aeropuerto candidato con las agregars conexiones candidatas.
        # Se elimina el aeropuerto en caso de que este genere muchos infectados
        with open(ruta_aeropuertos_candidatos, "rt") as archivo:
            informacion = archivo.readlines()
        # Limpiamos la Informacion
        info_limpia = []
        for line in informacion:
            final = line.strip().split(",")
            info_limpia.append(final)
        # Instanciamos los aeropuertos
        for aero in info_limpia:
            self.agregar_aeropuerto(int(aero[0]), aero[1])
        with open(ruta_conexiones_candidatas, "rt") as archivo:
            informacion_2 = archivo.readlines()
        # Limpiamos la Informacion
        info_limpia_2 = []
        for line in informacion_2:
            final = line.strip().split(",")
            info_limpia_2.append(final)
        # Instanciamos las conexiones
        for conection in info_limpia_2:
            nodo_conexion = Conexion(int(conection[0]), int(conection[1]), int(conection[2]))
            self.agregar_conexion(int(conection[0]), int(conection[1]), int(conection[2]))
            infectados = self.infectados_generados_desde_aeropuerto(int(conection[0]))
            if infectados > UMBRAL:
                self.eliminar_conexion(nodo_conexion)
                print(f"La conexion {int(conection[0])} -> {int(conection[1])} rompe las reglas de seguridad")
                airport = self.aeropuertos[int(conection[0])]
                for conexion in airport.conexiones:
                    self.eliminar_conexion(conexion)
                self.eliminar_aeropuerto(int(conection[0]))
            else:
                pass





if __name__ == "__main__":
    # I: Construcción de la red
    # Instanciación de la red de aeropuertos
    redmundial = RedesMundiales()
    # Carga de datos (utiliza agregar_aeropuerto y agregar_conexion)
    redmundial.cargar_red(
        os.path.join("datos", "aeropuertos.txt"),
        os.path.join("datos", "conexiones.txt"),
    )

    # II: Consultas sobre la red
    # Verificar si conteo de infectados funciona
    # Para el aeropuerto 8 debería ser 2677
    redmundial.infectados_generados_desde_aeropuerto(8)
    # Para el aeropuerto 7 debería ser 10055
    redmundial.infectados_generados_desde_aeropuerto(7)
    # Para el aeropuerto 12 debería ser 30000
    redmundial.infectados_generados_desde_aeropuerto(4)

    # III: Simulación sobre la red
    # Utilizamos lo que hemos hecho para aplicar los cambios sobre la red
    redmundial.verificar_candidatos(
        os.path.join("datos", "aeropuertos_candidatos.txt"),
        os.path.join("datos", "conexiones_candidatas.txt"),
    )
