import random
import os
import parametros as p
from time import sleep
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QUrl
from PyQt5.QtMultimedia import QSound
from backend_flechas import Flecha


class BackVentanaJuego(QObject):

    senal_pausa_tecla = pyqtSignal()
    senal_aparecer_flecha = pyqtSignal(int)
    senal_verificar_flecha = pyqtSignal(int)
    senal_tecla_invalida = pyqtSignal()
    senal_dificultad_nombre = pyqtSignal(tuple)
    senal_activa_dinamica_flecha = pyqtSignal()

    def __init__(self):
        super().__init__()

    def armar_paso(self, info):

        self.timer = QTimer()
        self.dificultad = info[0]
        self.usuario = info[1]
        self.senal_dificultad_nombre.emit((self.dificultad, self.usuario))
        self.pausa_paso = False
        self.senal_activa_dinamica_flecha.emit()
        self.sigo_jugando = True

        if self.dificultad == 0:
            self.timer.setInterval(p.PASO_PRINCIPIANTE)
            self.timer.timeout.connect(self.enviar_senal_flecha)
            self.timer.start()
        elif self.dificultad == 1:
            self.timer.setInterval(p.PASO_AFICIONADO)
            self.timer.timeout.connect(self.enviar_senal_flecha)
            self.timer.start()
        elif self.dificultad == 2:
            self.timer.setInterval(p.PASO_MAESTRO)
            self.timer.timeout.connect(self.enviar_senal_flecha)
            self.timer.start()

    def pausar_paso(self):
        try:
            if not self.pausa_paso:
                self.timer.stop()
                self.pausa_paso = True
            else:
                self.timer.start()
                self.pausa_paso = False
        
        except AttributeError:
            pass

    def enviar_senal_flecha(self):
        self.senal_aparecer_flecha.emit(self.dificultad)

    def reproducir_cancion(self, indice):

        self.duracion_song = {0: p.DURACION_CANCION_PRINCIPIANTE,
                             1: p.DURACION_CANCION_AFICIONADO,
                             2: p.DURACION_CANCION_MAESTRO}

        self.timer_cancion = QTimer()
        self.timer_cancion.setSingleShot(True)
        self.timer_cancion.setInterval(self.duracion_song[self.dificultad] * 1000)
        self.timer_cancion.timeout.connect(self.terminar_level)
        self.timer_cancion.start()
        self.song = None
        self.pausa_song = False

        if indice == 0:
            ruta = os.path.join("songs", "cancion_1.wav")
        elif indice == 1:
            ruta = os.path.join("songs", "cancion_2.wav")

        self.song = QSound(ruta)
        self.song.play()

    def pausar_cancion(self):
        try:
            if not self.pausa_song and self.pausa_paso:
                print("Entrando")
                self.song.stop()
                self.pausa_song = True
            else:
                # CORREGIR ESTOO, ENTRA CUANDO PONGO SALIR
                print("Entrando aca")
                self.song.play()
                self.pausa_song = False
        except AttributeError:
            pass

    def pausar_song_y_pasos_para_salir(self):
        self.song.stop()
        self.timer.stop()

    def verificar_tecla(self, tecla):
        teclas = [p.LEFT_ARROW, p.RIGHT_ARROW, p.UP_ARROW, p.DOWN_ARROW]
        if tecla == p.STOP_KEY:
            self.pausar_paso()
            self.pausar_cancion()
            self.senal_pausa_tecla.emit()
        elif tecla in teclas:
            self.senal_verificar_flecha.emit(tecla)
        else:
            # Cualquier flecha del teclado
            self.senal_tecla_invalida.emit()

    def terminar_level(self):
        self.timer.stop()

    def parar_cancion_nivel(self):
        self.song.stop()