import sys
import os
import random
import parametros as p

from math import floor
from time import sleep, time
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import pyqtSignal, QThread, QTimer, QRect
from PyQt5.QtGui import QPixmap


class Flecha(QThread):

    def __init__(self, flecha, orientacion, tipo, qrect):
        super().__init__()
        self.flecha = flecha
        self.orientacion = orientacion
        self.tipo = tipo
        self.valida = None
        self.caja_intersecto = None
        self.tocada = None
        self.hielo = False
        self.en_limite = True
        if orientacion == p.RIGHT_ARROW:
            self.x = 190
            self.caja_intersecto = qrect[3]
        elif orientacion == p.LEFT_ARROW:
            self.x = 40
            self.caja_intersecto = qrect[0]
        elif orientacion == p.UP_ARROW:
            self.x = 90
            self.caja_intersecto = qrect[1]
        elif orientacion == p.DOWN_ARROW:
            self.x = 140
            self.caja_intersecto = qrect[2]
        self.y = 170

    def run(self):
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.movimiento)
        self.timer.start()
        self.timer_1 = QTimer()
        self.timer_1.setInterval(1)
        self.timer_1.timeout.connect(self.intersecto)
        self.timer_1.start()

    def movimiento(self):

        if self.tipo != "D" and not self.hielo:
            mov = self.y + p.VELOCIDAD_FLECHA
            self.flecha.move(self.x, mov)
            self.y = mov
        elif self.tipo == "D" and not self.hielo:
            mov = self.y + p.VELOCIDAD_FLECHA * p.RAPIDEZ_FLECHA_DORADA
            self.flecha.move(self.x, mov)
            self.y = mov

        if self.tipo != "D" and self.hielo:
            mov = self.y + p.VELOCIDAD_FLECHA * 0.5
            self.flecha.move(self.x, mov)
            self.y = mov
        elif self.tipo == "D" and self.hielo:
            mov = self.y + p.VELOCIDAD_FLECHA * p.RAPIDEZ_FLECHA_DORADA * 0.5
            self.flecha.move(self.x, mov)
            self.y = mov

        if self.y > 680 and self.tocada is None:
            self.flecha.hide()
            self.tocada = False
        
        if self.y > 700:
            self.timer.stop()

    def intersecto(self):

        if self.flecha.geometry().intersects(self.caja_intersecto.geometry()):
            self.valida = True
        else:
            self.valida = False


class DinamicaFlechas(QThread):

    senal_hielo = pyqtSignal()
    senal_volver_hielo = pyqtSignal()
    senal_actualizar_etiqueta_combo = pyqtSignal(tuple)
    senal_actualizar_aprobacion = pyqtSignal(int)
    senal_limpiar_todo = pyqtSignal(tuple)  # implementaaaar
    senal_termino_ronda = pyqtSignal()
    senal_eviar_info_ronda = pyqtSignal(tuple)
    senal_setear_dinero = pyqtSignal(int)
    senal_termino_urgente = pyqtSignal(tuple)
    senal_paso_correcto = pyqtSignal(list)
    senal_terminar_sin_jugar = pyqtSignal()
    senal_resetear_barras_combos = pyqtSignal()
    senal_cheatcode_niv = pyqtSignal()
    senal_abrir_tienda = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.acumulado = 0
        self.dinero = p.DINERO_INICIAL
        self.jugando = False

    def inicio_dinamica(self):

        self.jugando = True
        self.lista_flechas = []
        self.pasos = []
        self.combo = p.COMBO_INICIAL
        self.combo_mayor = p.COMBO_INICIAL
        self.pausa = False
        self.timer_combo = QTimer()
        self.timer_combo.setInterval(1)
        self.timer_combo.timeout.connect(self.kombo)
        self.timer_combo.start()
        self.cantidad_flechas = {"N": 0, "x2": 0, "D": 0, "H": 0}
        self.timer_hielo = QTimer()
        self.timer_fin_hielo = QTimer()
        self.timer_fin_hielo.setSingleShot(True)
        self.timer_hielo.setInterval(1)
        self.timer_hielo.timeout.connect(self.activar_hielo)
        self.pasos_totales = 0
        self.pasos_correctos = 0
        self.pasos_incorrectos = 0
        self.valor_aprobacion = 100  # Fijo
        self.porcentaje = 100  # Variante
        self.timer_termino = QTimer()
        self.timer_termino.setInterval(1000)
        self.timer_termino.timeout.connect(self.revisar_termino)

    def correr_flecha(self, flecha):

        self.lista_flechas.append(flecha)
        flecha.run()
        self.timer_termino.start()

    def agregar_paso(self, paso):
        self.pasos.append(paso)
        self.pasos_totales += 1

    def parar_flechas(self):

        try:
            if not self.pausa:
                for arrow in self.lista_flechas:
                    arrow.timer.stop()
                self.pausa = True
            else:
                for arrow in self.lista_flechas:
                    arrow.timer.start()
                self.pausa = False
        except AttributeError:
            pass

    def comprobar_flecha(self, orientacion):

        entra = False

        for arrow in self.lista_flechas:
            if arrow.valida and arrow.orientacion == orientacion:
                print("ATRAPADA")
                entra = True
                arrow.tocada = True
                arrow.flecha.hide()
                self.sumar_flecha(arrow)
                # Si es Hielo, detener velocidad
                if arrow.tipo == "H":
                    self.senal_hielo.emit()
                    self.timer_hielo.start()
                    self.timer_fin_hielo.setInterval(p.PONDERADOR_HIELO * 1000
                                                     * self.tempo[self.dificultad])
                    self.timer_fin_hielo.timeout.connect(self.vovler_hielo)
                    self.timer_fin_hielo.start()

        if not entra:
            print("HOLA")
            self.flecha_invalida()

    def sumar_flecha(self, flecha):

        self.cantidad_flechas[flecha.tipo] += 1
        print(self.cantidad_flechas)

    def puntaje_final(self):
        resultado = (self.cantidad_flechas["N"]
                     + p.PONDERADOR_X2 * self.cantidad_flechas["x2"]
                     + p.PONDERADOR_DORADA * self.cantidad_flechas["D"]
                     + self.cantidad_flechas["H"])

        max_combo = self.combo_mayor

        final = max_combo * resultado * p.PUNTOS_FLECHA

        return final

    def activar_hielo(self):
        for flecha in self.lista_flechas:
            flecha.hielo = True

    def vovler_hielo(self):
        self.timer_hielo.stop()
        for flecha in self.lista_flechas:
            flecha.hielo = False

    def recibir_tempo(self, info):
        self.tempo = info[0]
        self.dificultad = info[1]

    def kombo(self):
        for paso in self.pasos:
            contar_verdaderas = 0
            for tecla in paso:
                if tecla.tocada == False:
                    try:
                        self.pasos.remove(paso)
                    except ValueError:
                        pass
                    self.combo = p.RESETEO_COMBO
                    self.pasos_incorrectos += 1
                elif tecla.tocada:
                    contar_verdaderas += 1
                    if contar_verdaderas == len(paso):
                        self.combo += p.AUMENTO_COMBO
                        self.pasos_correctos += 1
                        self.senal_paso_correcto.emit(paso)
                        try:
                            self.pasos.remove(paso)
                        except ValueError:
                            pass
                        if self.combo > self.combo_mayor:
                            self.combo_mayor = self.combo

        info_combos = (self.combo, self.combo_mayor)
        self.senal_actualizar_etiqueta_combo.emit(info_combos)
        self.aprobacion()

    def flecha_invalida(self):

        if self.combo > self.combo_mayor:
            self.combo_mayor = self.combo

        self.combo = p.RESETEO_COMBO
        self.pasos_incorrectos += 1

        info_combos_2 = (self.combo, self.combo_mayor)
        self.senal_actualizar_etiqueta_combo.emit(info_combos_2)

    def aprobacion(self):

        if self.pasos_totales == 0:
            pasos_totales = 1
        else:
            pasos_totales = self.pasos_totales

        porcentaje = max(0, floor(p.APROBACION_FORMULA * (self.pasos_correctos
                         - self.pasos_incorrectos) / pasos_totales))

        self.porcentaje = porcentaje
        self.senal_actualizar_aprobacion.emit(porcentaje)

    def revisar_termino(self):
        finish = True
        for flecha in self.lista_flechas:
            if flecha.y < 690:
                finish = False

        if finish:
            self.timer_termino.stop()
            self.senal_termino_ronda.emit()
            puntaje = self.puntaje_final()
            self.acumulado += puntaje
            self.dinero += puntaje
            tupla = (puntaje, self.acumulado, self.combo_mayor,
                     self.pasos_incorrectos, self.porcentaje)
            self.senal_eviar_info_ronda.emit(tupla)
            self.setear_dinero()
            self.senal_abrir_tienda.emit()
            self.timer_combo.stop()
            for arrow in self.lista_flechas:
                arrow.flecha.hide()

    def setear_dinero(self):
        self.senal_setear_dinero.emit(self.dinero)

    def resetear_dinero_y_acumulado(self):
        self.acumulado = 0
        self.dinero = p.DINERO_INICIAL
        self.combo_mayor = p.COMBO_INICIAL

    def salir_urgente(self):
        if self.jugando:
            self.timer_termino.stop()
            puntaje = self.puntaje_final()
            self.acumulado += puntaje
            self.dinero += puntaje
            tupla = (puntaje, self.acumulado, self.combo_mayor,
                     self.pasos_incorrectos, self.porcentaje)
            self.setear_dinero()
            self.senal_termino_urgente.emit(tupla)
        else:
            self.senal_terminar_sin_jugar.emit()
        self.senal_resetear_barras_combos.emit() 
        self.senal_abrir_tienda.emit()
        self.timer_combo.stop()
        for arrow in self.lista_flechas:
            arrow.flecha.hide()

    def restar_valor_penguin(self, valor):
        self.dinero -= valor
        self.setear_dinero()

    def cheatcode_mon(self):
        self.dinero += p.DINERO_TRAMPA
        print("Haciendo Trampa")

    def parar_timer_combo(self):
        self.timer_combo.stop()
    
    def cheatcode_niv(self):
        self.senal_cheatcode_niv.emit()
        for arrow in self.lista_flechas:
            arrow.flecha.hide()
        self.timer_termino.stop()
        self.senal_termino_ronda.emit()
        puntaje = self.puntaje_final()
        print(puntaje)
        self.acumulado += puntaje
        self.dinero += puntaje
        tupla = (puntaje, self.acumulado, self.combo_mayor,
                 self.pasos_incorrectos, self.porcentaje)
        self.senal_eviar_info_ronda.emit(tupla)
        self.setear_dinero()
        self.senal_abrir_tienda.emit()
        self.timer_combo.stop()