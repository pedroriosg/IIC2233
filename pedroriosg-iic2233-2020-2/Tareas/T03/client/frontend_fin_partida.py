import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

path = os.path.join("fin_partida.ui")
window_name, base_class = uic.loadUiType(path)


class FinPartida(window_name, base_class):

    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.nombre = None
        self.boton_sala_espera.clicked.connect(self.resetear)

    def setear_nombres(self, nombre):
        self.nombre = nombre

    def setear_resultados(self, informacion):
        informacion.sort(key=lambda x: x[1])
        informacion.reverse()
        if informacion[0][0] == self.nombre:
            self.msg_resultado.setText("¡¡ Has ganado !!")
        else:
            self.msg_resultado.setText("¡¡ Has perdido !!")
        self.msg_resultado.setFont(QFont("Courier New", 24))
        self.msg_resultado.setStyleSheet("color: rgb(255, 187, 0)")
        self.msg_resultado.setAlignment(Qt.AlignCenter)
        contador = 1
        x_n = 40
        y_n = 200
        x_p = 290
        for player in informacion:
            name = player[0]
            puntos = player[1]
            if name == self.nombre:
                self.label_nombre = QLabel(f"{contador}. {name} (Tú)", self)
            else:
                self.label_nombre = QLabel(f"{contador}. {name}", self)
            self.label_nombre.setGeometry(x_n, y_n, 220, 30)
            self.label_nombre.setFont(QFont("Courier New", 15))
            self.label_nombre.setStyleSheet("color: rgb(255, 187, 0)")
            self.label_puntos = QLabel(f"{puntos} ptos.", self)
            self.label_puntos.setGeometry(x_p, y_n, 100, 30)
            self.label_puntos.setFont(QFont("Courier New", 15))
            self.label_puntos.setStyleSheet("color: rgb(255, 187, 0)")
            y_n += 40
            contador += 1

        self.show()
        self.parent.hide()

    def resetear(self):
        self.hide()


if __name__ == '__main__':
    app = QApplication([])
    fin = FinPartida()
    fin.show()
    sys.exit(app.exec_())
