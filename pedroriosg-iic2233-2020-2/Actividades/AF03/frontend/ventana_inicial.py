import os
from PyQt5.QtWidgets import (
    QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap


class VentanaInicial(QWidget):

    senal_comparar_codigo = pyqtSignal(str)
    senal_abrir_menu_principal = pyqtSignal()

    def __init__(self, ancho, alto, ruta_logo):
        """Es el init de la ventana del menú de inicio. Puedes ignorarlo."""
        super().__init__()
        self.size = (ancho, alto)
        self.resize(ancho, alto)
        self.init_gui(ruta_logo)

    def init_gui(self, ruta_logo):
        # Completar
        self.setWindowTitle("Ventana Inicial DCCrew")
        # Label Imagen
        self.imagen = QLabel(self)
        pixeles = QPixmap(ruta_logo)
        self.imagen.setPixmap(pixeles)
        self.imagen.setScaledContents(True)
        self.imagen.setGeometry(0, 0, self.size[0], self.size[1])

        # Label Texto
        self.texto = QLabel("Ingrese código de su partida:", self)

        # Cuadro Texto
        self.input_codigo = QLineEdit("", self)

        # Boton
        self.boton = QPushButton("&Ingresar")
        self.boton.clicked.connect(self.comparar_codigo)

        # Layout
        hboxm = QHBoxLayout()
        hboxm.addWidget(self.texto)
        hboxm.addWidget(self.input_codigo)
        vbox = QVBoxLayout()
        vbox.addWidget(self.imagen)
        vbox.addLayout(hboxm)
        vbox.addWidget(self.boton)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        self.setLayout(hbox)

    def comparar_codigo(self):
        """Método que emite la señal para comparar el código. Puedes ignorarlo.
        Recuerda que el QLineEdit debe llamarse 'input_codigo'"""
        codigo = self.input_codigo.text()
        self.senal_comparar_codigo.emit(codigo)

    def recibir_comparacion(self, son_iguales):
        """Método que recibe el resultado de la comparación. Puedes ignorarlo.
        Recuerda que el QLineEdit debe llamarse 'input_codigo'"""
        if not son_iguales:
            self.input_codigo.clear()
            self.input_codigo.setPlaceholderText("¡Inválido! Debe ser un código existente.")
        else:
            self.hide()
            self.senal_abrir_menu_principal.emit()
