import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

path = os.path.join("intercambio.ui")
window_name, base_class = uic.loadUiType(path)


class Intercambio(window_name, base_class):

    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.boton_intercambiar.clicked.connect(self.intercambio)

    def intercambio(self):
        msg = {"comando": "querer_intercambiar",
               "materia_ofrecida": self.materia_ofrecida.currentIndex(),
               "cantidad_ofrecida": self.cantidad_ofrecida.value(),
               "materia_pedida": self.materia_pedida.currentIndex(),
               "cantidad_pedida": self.cantidad_pedida.value(),
               "jugador": self.pedir_jugador.currentText()}
        self.parent.enviar_intercambio_signal.emit(msg)
        self.hide()

    def setear_nombres(self, nombres):
        for name in nombres:
            self.pedir_jugador.addItem(name)


if __name__ == '__main__':
    app = QApplication([])
    intercambio = Intercambio()
    intercambio.show()
    sys.exit(app.exec_())
