import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

path = os.path.join("monopolio.ui")
window_name, base_class = uic.loadUiType(path)


class Monopolio(window_name, base_class):

    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.boton_arcilla.clicked.connect(self.arcilla)
        self.boton_madera.clicked.connect(self.madera)
        self.boton_trigo.clicked.connect(self.trigo)

    def arcilla(self):
        msg = {"comando": "rpta_monopolio", "materia": "arcilla"}
        self.parent.enviar_monopolio_signal.emit(msg)
        self.hide()

    def madera(self):
        msg = {"comando": "rpta_monopolio", "materia": "madera"}
        self.parent.enviar_monopolio_signal.emit(msg)
        self.hide()

    def trigo(self):
        msg = {"comando": "rpta_monopolio", "materia": "trigo"}
        self.parent.enviar_monopolio_signal.emit(msg)
        self.hide()


if __name__ == '__main__':
    app = QApplication([])
    monopolio = Monopolio()
    monopolio.show()
    sys.exit(app.exec_())
