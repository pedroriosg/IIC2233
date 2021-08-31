import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import pyqtSignal

window_name, base_class = uic.loadUiType("designer_inicio.ui")


class VentanaInicio(window_name, base_class):

    senal_verificar_usuario = pyqtSignal(str)
    senal_abrir_ventana_juego = pyqtSignal(str)
    senal_abrir_ventana_ranking = pyqtSignal()
    senal_abrir_ventana_inicio = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.boton_comenzar.clicked.connect(self.verificar_usuario)
        self.boton_ver_ranking.clicked.connect(self.ver_ranking)
        self.senal_abrir_ventana_inicio.connect(self.show)

    def verificar_usuario(self):
        "Método que emite la señal para comparar el código."
        usuario = self.nombre_usuario.text()
        self.senal_verificar_usuario.emit(usuario)

    def recibir_comparacion(self, info):

        alfanumerico = info[0]

        if not alfanumerico:
            self.nombre_usuario.clear()
            msg = QMessageBox()
            msg.setWindowTitle("USUARIO INVÁLIDO")
            msg.setText("¡Debe ser alphanumerico!")
            msg.exec_()
        else:
            self.hide()
            self.senal_abrir_ventana_juego.emit(info[1])

    def ver_ranking(self):
        self.hide()
        self.senal_abrir_ventana_ranking.emit()

    def limpiar_casilla(self):
        self.nombre_usuario.clear()


if __name__ == '__main__':
    app = QApplication([])
    ventana_inicio = VentanaInicio()
    ventana_inicio.show()
    sys.exit(app.exec_())
