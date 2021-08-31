import random
import os
import parametros as p
from time import sleep
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QUrl


class BackVentanaResumen(QObject):

    senal_activa_boton_siguiente = pyqtSignal(tuple)
    senal_para_agregar_al_txt = pyqtSignal(tuple)
    senal_ocultar_ventana_juego = pyqtSignal()
    senal_mostrar_ventana_inicio = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.nivel = None
        self.aprobaste = None

    def recibir_dificultad_nombre(self, info):
        self.nivel = info[0]
        self.usuario = info[1]

    def ver_aprobacion(self, tupla):

        aprobacion = tupla[0]
        self.puntaje = tupla[1]

        if self.nivel == 0:
            if aprobacion >= p.APROBACION_PRINCIPIANTE:
                self.aprobaste = True
            else:
                self.aprobaste = False
        elif self.nivel == 1:
            if aprobacion >= p.APROBACION_AFICIONADO:
                self.aprobaste = True
            else:
                self.aprobaste = False
        elif self.nivel == 2:
            if aprobacion >= p.APROBACION_MAESTRO:
                self.aprobaste = True
            else:
                self.aprobaste = False

        tupla = (self.aprobaste, self.nivel)
        if self.aprobaste:
            self.senal_activa_boton_siguiente.emit(tupla)
        else:
            self.senal_activa_boton_siguiente.emit(tupla)

    def volver_inicio(self):
        tupla = (self.usuario, self.puntaje)
        self.senal_para_agregar_al_txt.emit(tupla)
  
    def salida_urgente(self, tupla):
        tupla = (self.usuario, tupla[1])
        self.senal_para_agregar_al_txt.emit(tupla)
        self.senal_ocultar_ventana_juego.emit()
        self.senal_mostrar_ventana_inicio.emit()

