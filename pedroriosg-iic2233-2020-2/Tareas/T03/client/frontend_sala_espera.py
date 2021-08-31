import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

path = os.path.join("sala_espera.ui")
window_name, base_class = uic.loadUiType(path)


class SalaEspera(window_name, base_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def labels_segun_cantidad(self, cantidad):
        self.lista_labels = []
        x = 130
        y = 350
        W = 241
        H = 40
        for _ in range(cantidad):
            self.label = QLabel("Esperando", self)
            self.label.setGeometry(x, y, W, H)
            self.label.setFont(QFont("Courier New", 18))
            self.label.setStyleSheet("color: rgb(255, 187, 0)")
            self.label.setAlignment(Qt.AlignCenter)
            self.lista_labels.append(self.label)
            self.label.show()

            # Ahora actualizamos posicion para siguiente QLabel
            if x < 440:
                x += 310
            elif x >= 440:
                x = 130
                y = 430

    def actualizar_jugadores(self, jugadores):
        for i in range(0, len(jugadores)):
            self.lista_labels[i].setText(jugadores[i])


path_2 = os.path.join("sala_espera_warning.ui")
window_name_2, base_class_2 = uic.loadUiType(path_2)


class WarningWindow(window_name_2, base_class_2):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.boton_cerrar.clicked.connect(self.cerrar_ventana)

    def cerrar_ventana(self):
        self.close()

    def closeEvent(self, event):

        try:
            event.accept()
        except AttributeError:
            pass


if __name__ == '__main__':
    app = QApplication([])
    sala_espera = WarningWindow()
    sala_espera.show()
    sys.exit(app.exec_())
