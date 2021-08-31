import random
import os
import parametros as p
from time import sleep
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QUrl
from PyQt5.QtMultimedia import QSound


class BackVentanaInicio(QObject):
    "Este es el backend del menú de inicio."

    senal_resultado_verificacion = pyqtSignal(tuple)
    senal_enviar_lista_a_ordenar = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def verificar_usuario(self, usuario):
        if usuario.isalnum():
            self.senal_resultado_verificacion.emit((True, usuario))
        else:
            self.senal_resultado_verificacion.emit((False, usuario))

    def crear_txt(self):
        self.archivo = open("resultados.txt", "w")
        self.archivo.close()

    def agregar_usuario_txt(self, tupla):
        nombre = tupla[0]
        puntaje = tupla[1]
        self.archivo = open("resultados.txt", "a")
        self.archivo.write(f"{nombre},{puntaje}\n")
        self.archivo.close()

    def enviar_archivo(self):
        informacion = self.nombres_puntajes_a_lista()
        self.senal_enviar_lista_a_ordenar.emit(informacion)

    def nombres_puntajes_a_lista(self):
        jugadores = []
        # Abrimos el archivo
        with open("resultados.txt", "rt") as archivo:
            informacion = archivo.readlines()

        # Limpiamos informacion
        for linea in informacion:
            jugador = linea.strip().split(",")
            jugadores.append(jugador)

        for n in jugadores:
            n[1] = int(n[1])

        return jugadores
