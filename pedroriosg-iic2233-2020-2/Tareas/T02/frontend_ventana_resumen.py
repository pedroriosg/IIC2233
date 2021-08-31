import sys
import os
import random
import parametros as p

from time import sleep
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import pyqtSignal, QThread, QTimer, QRect
from PyQt5.QtGui import QPixmap
from backend_flechas import Flecha

window_name, base_class = uic.loadUiType("designer_resumen.ui")


class VentanaResumen(window_name, base_class):

    senal_abrir_ventana_resumen = pyqtSignal()
    senal_verificar_aprobacion = pyqtSignal(tuple) # ver que tal
    senal_volver_inicio = pyqtSignal()
    senal_resetear_combos_barras = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.senal_abrir_ventana_resumen.connect(self.show)
        self.boton_volver_inicio.clicked.connect(self.volver_inicio)
        self.boton_continuar_jugando.clicked.connect(self.continuar_jugando)

    def recibir_info_y_editar(self, informacion):
        puntaje_obtenido = informacion[0]
        acumulado = informacion[1]
        maximo_combo = informacion[2]
        pasos_fallados = informacion[3]
        aprobacion = informacion[4]

        self.puntaje.setText(f"{puntaje_obtenido}")
        self.puntaje_acumulado.setText(f"{acumulado}")
        self.maximo_combo.setText(f"{maximo_combo}")
        self.pasos_fallados.setText(f"{pasos_fallados}")
        self.aprobacion.setText(f"{aprobacion}")

        tupla = (aprobacion, acumulado)
        self.senal_verificar_aprobacion.emit(tupla)

    def activar_botones(self, info):
        bul = info[0]
        level = info[1]
        if bul:
            self.boton_continuar_jugando.setEnabled(bul)
            self.mensaje.setText(f"SIGUES JUGANDO")
        else:
            self.boton_volver_inicio.setEnabled(True)
            self.mensaje.setText(f"QUEDAS ELIMINADO DE DCCUMBIA")
        self.numero_ronda.setText(f"{level + 1}")

    def volver_inicio(self):
        self.hide()
        self.senal_volver_inicio.emit()
        self.senal_resetear_combos_barras.emit()
        self.boton_volver_inicio.setEnabled(False)

    def continuar_jugando(self):
        self.senal_resetear_combos_barras.emit()
        self.hide()
        self.boton_continuar_jugando.setEnabled(False)

if __name__ == '__main__':
    app = QApplication([])
    ventana_resumen = VentanaResumen()
    ventana_resumen.show()
    sys.exit(app.exec_())