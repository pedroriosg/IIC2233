import sys
import os
import random
import parametros as p

from time import sleep
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QMessageBox
from PyQt5.QtCore import pyqtSignal, QThread, QTimer, QRect
from PyQt5.QtGui import QPixmap
from backend_flechas import Flecha
from drag_and_drop import Espacio, Piguirin

window_name, base_class = uic.loadUiType("designer_juego.ui")


class VentanaJuego(window_name, base_class):

    senal_abrir_ventana_juego = pyqtSignal()
    senal_armar_paso = pyqtSignal(tuple)
    senal_salir_juego = pyqtSignal()
    senal_reproducir_cancion = pyqtSignal(int)
    senal_pausa = pyqtSignal()
    senal_agregar_flecha = pyqtSignal(object)
    senal_agregar_paso = pyqtSignal(list)
    senal_verificar_flecha = pyqtSignal(int)
    senal_volver_color = pyqtSignal(int)
    senal_eviar_tempo = pyqtSignal(tuple)
    senal_restar_dinero_penguin = pyqtSignal(int)
    senal_mon = pyqtSignal()
    senal_niv = pyqtSignal()
    senal_cerrar_tienda = pyqtSignal()
    senal_close_event = pyqtSignal()
    senal_close_event_sin_comenzar = pyqtSignal()

    def __init__(self):

        super().__init__()
        self.setupUi(self)
        self.boton_comenzar_partida.clicked.connect(self.comenzar_partida)
        self.boton_salir_juego.clicked.connect(self.salir_juego)
        self.boton_pausar.clicked.connect(self.pausa)
        self.boton_pausar.setEnabled(False)
        self.qrec_intersecto = (self.captura_left, self.captura_up,
                                self.captura_down, self.captura_right)

        self.valor_dinero.setText(f"{p.DINERO_INICIAL}")
        self.valor_pinguirin.setText(f"{p.VALUE_PINGUIRIN}")
        self.mi_dinero = p.DINERO_INICIAL
        self.crear_label_pinguinos()
        self.crear_drag_penguin()

    def mostrar_y_recibir_usuario(self, nombre):
        self.usuario = nombre
        print(self.usuario)
        self.show()

    def crear_flecha(self, dificultad):

        self.dificultad = dificultad

        un_paso = []
        tipo = ((1, "N"), (3, "x2"), (2, "D"), (4, "H"))
        posicion = ((p.LEFT_ARROW, "left_", 40), (p.UP_ARROW, "up_", 90),
                    (p.DOWN_ARROW, "down_", 140), (p.RIGHT_ARROW, "right_", 190))
        paso = random.randint(1, self.dificultad + 1)

        probability = random.uniform(0, 1)
        if probability < p.PROB_FLECHA_NORMAL:
            tipo = (1, "N")
        elif probability < p.PROB_FLECHA_X2:
            tipo = (3, "x2")
        elif probability < p.PROB_FLECHA_DORADA:
            tipo = (2, "D")
        elif probability <= p.PROB_FLECHA_HIELO:
            tipo = (4, "H")

        for i in range(0, paso):
            self.flecha = QLabel(self)
            sentido = random.choice(posicion)
            self.flecha.setGeometry(sentido[2], 170, p.ALTO_FLECHA, p.ALTO_FLECHA)
            ruta = os.path.join("sprites", "flechas", f"{sentido[1]}{tipo[0]}")
            pix = QPixmap(ruta)
            self.flecha.setPixmap(pix)
            self.flecha.setScaledContents(True)
            self.flecha.show()
            flecha = Flecha(self.flecha, sentido[0], tipo[1], self.qrec_intersecto)
            self.senal_agregar_flecha.emit(flecha)
            un_paso.append(flecha)
        
        self.senal_agregar_paso.emit(un_paso)

    def comenzar_partida(self):

        # Guardamos teclas apretadas para cheatcode
        self.cheatcodes = ""
        self.comienza = False

        hay_penguin = self.revisar_pengui()
        if hay_penguin:
            self.comienza = True
            # Desactivamos botones
            self.boton_pausar.setEnabled(True)
            self.boton_cancion.setEnabled(False)
            self.boton_dificultad.setEnabled(False)
            self.boton_comenzar_partida.setEnabled(False)
            dificultad = self.boton_dificultad.currentIndex()
            self.setear_barra(dificultad)
            tupla = (dificultad, self.usuario)
            self.senal_armar_paso.emit(tupla)
            song_number = self.boton_cancion.currentIndex()
            self.senal_reproducir_cancion.emit(song_number)
            self.senal_cerrar_tienda.emit()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CONDICION DE INICIO")
            msg.setText("¡Debes tener pingüinos en la pista!")
            msg.exec_()

    def salir_juego(self):
    
        try:
            if self.comienza:
                self.limpiar_pista()
                self.hide()
                self.senal_salir_juego.emit()
            else:
                self.senal_close_event_sin_comenzar.emit()
                self.hide()
                self.limpiar_pista()
        except AttributeError:
            self.senal_close_event_sin_comenzar.emit()
            self.hide()
            self.limpiar_pista()
        self.comienza = False

    def pausa(self):
        self.senal_pausa.emit()

    def keyPressEvent(self, event):
        self.senal_verificar_flecha.emit(event.key())
        if event.key() == p.LEFT_ARROW:
            self.qrec_intersecto[0].setStyleSheet("background-color: rgb(0, 225, 132)")
        elif event.key() == p.DOWN_ARROW:
            self.qrec_intersecto[2].setStyleSheet("background-color: rgb(0, 225, 132)")
        elif event.key() == p.RIGHT_ARROW:
            self.qrec_intersecto[3].setStyleSheet("background-color: rgb(0, 225, 132)")
        elif event.key() == p.UP_ARROW:
            self.qrec_intersecto[1].setStyleSheet("background-color: rgb(0, 225, 132)")

        # Implementamos la opcion cheatcode
        self.cheatcodes += str(event.key())
        mon = str(p.LETRA_M) + str(p.LETRA_O) + str(p.LETRA_N)
        niv = str(p.LETRA_N) + str(p.LETRA_I) + str(p.LETRA_V)
        if mon in self.cheatcodes:
            self.senal_mon.emit()
            self.cheatcodes = ""
        elif niv in self.cheatcodes:
            self.senal_niv.emit()
            self.cheatcodes = ""

    def keyReleaseEvent(self, event):
        self.senal_volver_color.emit(event.key())
        if event.key() == p.LEFT_ARROW:
            self.qrec_intersecto[0].setStyleSheet("background-color: rgb(205, 225, 255)")
        elif event.key() == p.DOWN_ARROW:
            self.qrec_intersecto[2].setStyleSheet("background-color: rgb(205, 225, 255)")
        elif event.key() == p.RIGHT_ARROW:
            self.qrec_intersecto[3].setStyleSheet("background-color: rgb(205, 225, 255)")
        elif event.key() == p.UP_ARROW:
            self.qrec_intersecto[1].setStyleSheet("background-color: rgb(205, 225, 255)")

    def setear_barra(self, dificultad):
        self.tempo = {0: p.DURACION_CANCION_PRINCIPIANTE,
                 1: p.DURACION_CANCION_AFICIONADO,
                 2: p.DURACION_CANCION_MAESTRO}
        self.barra_progreso.setMaximum(self.tempo[dificultad])
        self.barra_progreso.setMinimum(0)
        self.barra_aprobacion.setMaximum(100)
        self.barra_aprobacion.setMinimum(0)
        self.barra_aprobacion.setValue(0)
        self.barra_progreso.setValue(0)
        self.valor_barra = 0 # Barra Progreso
        tupla = (self.tempo, dificultad)
        self.senal_eviar_tempo.emit(tupla)

    def actualizar_barra(self):
        self.valor_barra += 1
        self.barra_progreso.setValue(self.valor_barra)

    def actualizar_combos(self, info):
        combo_actual = info[0]
        combo_mayor = info[1]

        self.combo_actual.setText(f"x{combo_actual}")
        self.combo_mayor.setText(f"x{combo_mayor}")

    def actualizar_aprobacion(self, porcentaje):
        self.barra_aprobacion.setValue(porcentaje)

    def setear_dinero(self, dinero):
        self.mi_dinero = dinero
        self.valor_dinero.setText(f"{dinero}")

    def resetear_dinero(self):
        self.valor_dinero.setText(f"{p.DINERO_INICIAL}")
        self.mi_dinero = p.DINERO_INICIAL

    def esconder_ventana(self):
        self.hide()

    def crear_label_pinguinos(self):
        print("CREANDO PUNGUINOS")
        self.pinguinos_comprados = 0
        self.espacios_pinguinos = []
        x = 320
        y = 440
        amplitud = 70
        # Horizontales
        for _ in range(0, 3):
            for _ in range(0, 5):
                self.labelp = Espacio(self)
                self.labelp.setGeometry(x, y, 70, 70)
                self.labelp.setScaledContents(True)
                x += amplitud
                self.espacios_pinguinos.append(self.labelp)
            y += 70
            x = 320
        
        self.timer_compra = QTimer()
        self.timer_compra.setInterval(10)
        self.timer_compra.timeout.connect(self.comprar_pinguino)
        self.mi_dinero = p.DINERO_INICIAL
        self.timer_compra.start()

    def crear_drag_penguin(self):
        self.drags_penguin = []
        posiciones = {"morado": [890, 460], "rojo": [890, 369], "celeste": [770, 369],
                      "amarillo": [770, 460], "verde": [830, 560]}
        rutas = ["morado", "rojo", "celeste", "amarillo", "verde"]
        for color in rutas:
            ruta = os.path.join("sprites", f"pinguirin_{color}", f"{color}_neutro.png")
            pinguino = Piguirin(self, ruta, color)
            pinguino.setScaledContents(True)
            pinguino.setGeometry(posiciones[color][0], posiciones[color][1], 70, 70)
            self.drags_penguin.append(pinguino)

    def recibir_paso(self, paso):
        un_paso = paso
        for penguin in self.espacios_pinguinos:
            if penguin.disponible:
                penguin.moverse(un_paso)

    def revisar_pengui(self):
        se_puede = False
        for pinguino in self.espacios_pinguinos:
            if pinguino.disponible:
                se_puede = True
        
        return se_puede

    def comprar_pinguino(self):
        # Actualizamos dinero de los pinguinos
        for animal in self.espacios_pinguinos:
            animal.dinero = self.mi_dinero
        cantidad = 0
        for animal in self.espacios_pinguinos:
            if animal.disponible:
                cantidad += 1

        total = cantidad - self.pinguinos_comprados
        for _ in range(0, total):
            self.cambiar_dinero()
        
        self.pinguinos_comprados = cantidad

    def cambiar_dinero(self):
        # Cambiamos el dinero por comprar pingüino
        valor = p.VALUE_PINGUIRIN
        self.senal_restar_dinero_penguin.emit(valor)

    def limpiar_pista(self):
        self.timer_compra.stop()
        print("LIMPIANDOO")
        self.mi_dinero = p.DINERO_INICIAL
        for animal in self.espacios_pinguinos:
            animal.dinero = self.mi_dinero
            animal.disponible = False
            animal.setAcceptDrops(True)
            animal.clear()
        
        self.timer_compra = QTimer()
        self.timer_compra.setInterval(10)
        self.timer_compra.timeout.connect(self.comprar_pinguino)
        self.mi_dinero = p.DINERO_INICIAL
        self.timer_compra.start()

    def resetear_barras_combos(self):
        print("ENTRE")
        self.combo_actual.setText(f"x{0}")
        self.combo_mayor.setText(f"x{0}")
        self.barra_aprobacion.setValue(0)
        self.barra_progreso.setValue(0)

    def cerrar_tienda(self):
        for drag in self.drags_penguin:
            drag.tienda_open = False

    def abrir_tienda(self):
        for drag in self.drags_penguin:
            drag.tienda_open = True
        # Como se abre la pre - ronda, activamos botones
        self.boton_pausar.setEnabled(False)
        self.boton_cancion.setEnabled(True)
        self.boton_dificultad.setEnabled(True)
        self.boton_comenzar_partida.setEnabled(True)

    def closeEvent(self, event):
    
        try:
            if self.comienza:
                self.senal_close_event.emit()
                event.accept()
            else:
                self.senal_close_event_sin_comenzar.emit()
                event.accept()
            self.limpiar_pista()
        
        except AttributeError:
            event.accept()
            self.senal_close_event_sin_comenzar.emit()
            self.limpiar_pista()
        self.comienza = False


if __name__ == '__main__':
    app = QApplication([])
    ventana_juego = VentanaJuego()
    ventana_juego.show()
    sys.exit(app.exec_())
