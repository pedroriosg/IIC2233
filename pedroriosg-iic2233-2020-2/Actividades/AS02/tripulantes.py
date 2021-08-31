import random
import time
from threading import Thread, Event, Lock, Timer

from parametros import (PROB_IMPOSTOR, PROB_ARREGLAR_SABOTAJE,
                        TIEMPO_ENTRE_TAREAS, TIEMPO_TAREAS, TIEMPO_SABOTAJE,
                        TIEMPO_ENTRE_ACCIONES, TIEMPO_ESCONDITE)

from funciones import (elegir_accion_impostor, print_progreso, print_anuncio,
                       print_sabotaje, cargar_sabotajes, print_explosión)


class Tripulante(Thread):

    def __init__(self, color, tareas, evento_sabotaje, diccionario_tareas):
        # No modificar
        super().__init__(daemon=True)
        self.color = color
        self.tareas = tareas
        self.esta_vivo = True
        self.diccionario_tareas = diccionario_tareas
        self.evento_sabotaje = evento_sabotaje
        # Si quieres agregar lineas, hazlo desde aca

    def run(self):
        # Completar
        while self.esta_vivo and len(self.tareas) > 0:
            if not self.evento_sabotaje.is_set():
                self.hacer_tarea()
                time.sleep(TIEMPO_ENTRE_TAREAS)
            elif self.evento_sabotaje.is_set():
                probabilidad = random.uniform(0, 1)
                if PROB_ARREGLAR_SABOTAJE > probabilidad:
                    self.arreglar_sabotaje()
                time.sleep(TIEMPO_ENTRE_TAREAS)

    def hacer_tarea(self):
        # Completar
        tarea = random.choice(self.tareas)
        estado = self.diccionario_tareas[tarea]["realizado"]
        lock = self.diccionario_tareas[tarea]["lock"]
        with lock:
            tiempo_ejecucion = random.uniform(TIEMPO_TAREAS[0], TIEMPO_TAREAS[1])
            if not estado:
                for iteracion in range(5):
                    if self.esta_vivo:
                        print_progreso(self.color, f"Realizando {tarea}", 25 * iteracion)
                        time.sleep(tiempo_ejecucion / 5)
                    else:
                        print_anuncio(self.color, "Ha muerto")
                        break
                if self.esta_vivo:
                    self.tareas.remove(tarea)
                    self.diccionario_tareas[tarea]["realizado"] = True

    def arreglar_sabotaje(self):
        # Completar
        tiempo = random.uniform(TIEMPO_SABOTAJE[0], TIEMPO_SABOTAJE[1])
        print_anuncio(self.color, "Ha comenzado a reparar el sabotaje")
        for iteracion in range(4):
            if self.esta_vivo:
                print_progreso(self.color, f"Arreglando sabotaje", 33 * iteracion)
                time.sleep(tiempo / 4)
            else:
                print_anuncio(self.color, "Ha muerto")
                break
        if self.esta_vivo:
            self.evento_sabotaje.clear()
            print_anuncio(self.color, "Ha terminado de arreglar el sabotaje")


class Impostor(Tripulante):

    def __init__(self, color, tareas, evento_sabotaje, diccionario_tareas, tripulantes, evento_termino):
        # No modificar
        super().__init__(color, tareas, evento_sabotaje, diccionario_tareas)
        self.tripulantes = tripulantes
        self.evento_termino = evento_termino
        self.sabotajes = cargar_sabotajes()
        # Si quieres agregar lineas, hazlo desde aca

    def run(self):
        # Completar
        while len(self.tripulantes) > 0 or not self.evento_termino.is_set():
            accion = elegir_accion_impostor()
            if accion == "Matar":
                self.matar_jugador()
            elif accion == "Sabotear":
                self.sabotear()
            elif accion == "Esconderse":
                time.sleep(TIEMPO_ESCONDITE)
            time.sleep(TIEMPO_ENTRE_ACCIONES)

    def matar_jugador(self):
        # Completar
        if len(self.tripulantes) > 0:
            jugador = random.choice(self.tripulantes)
            jugador.esta_vivo = False
            self.tripulantes.remove(jugador)
            print_anuncio(jugador.color, f"Ha muerto. Quedan {len(self.tripulantes)} tripulantes vivos")

    def sabotear(self):
        # Completar
        if not self.evento_sabotaje.is_set():
            nombre_sabotaje = random.choice(self.sabotajes)
            tiempo = random.uniform(TIEMPO_SABOTAJE[0], TIEMPO_SABOTAJE[1])
            print_sabotaje(nombre_sabotaje)
            self.evento_sabotaje.set()
            t1 = Timer(tiempo, self.terminar_sabotaje)
            t1.start()

    def terminar_sabotaje(self):
        # Completar
        if self.evento_sabotaje.is_set():
            while len(self.tripulantes) > 0:
                self.matar_jugador()
            print_explosión()




if __name__ == "__main__":
    print("\n" + " INICIANDO PRUEBA DE TRIPULANTE ".center(80, "-") + "\n")
    # Se crea un diccionario de tareas y un evento sabotaje de ejemplos.
    ejemplo_tareas = {
            "Limpiar el filtro de oxigeno": {
                "lock": Lock(),
                "realizado": False,
                "nombre": "Limpiar el filtro de oxigeno"
            }, 
            "Botar la basura": {
                "lock": Lock(),
                "realizado": False,
                "nombre":  "Botar la basura"
            }
        }
    ejemplo_evento = Event()

    # Se intancia un tripulante de color ROJO
    rojo = Tripulante("Rojo", list(ejemplo_tareas.keys()), ejemplo_evento, ejemplo_tareas)

    rojo.start()

    time.sleep(5)
    # ==============================================================
    # Descomentar las siguientes lineas para probar el evento sabotaje.

    print(" HA COMENZADO UN SABOTAJE ".center(80, "*"))
    ejemplo_evento.set()

    rojo.join()

    print("\n-" + "="*80 + "\n")
    print(" PRUEBA DE TRIPULANTE TERMINADA ".center(80, "-"))
    if sum((0 if x["realizado"] else 1 for x in ejemplo_tareas.values())) > 0:
        print("El tripulante no logró completar todas sus tareas. ")
    elif ejemplo_evento.is_set():
        print("El tripulante no logró desactivar el sabotaje")
    else:
        print("El tripulante ha GANADO!!!")
