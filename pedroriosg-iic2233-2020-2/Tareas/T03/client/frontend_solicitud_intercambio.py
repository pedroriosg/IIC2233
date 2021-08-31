import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

path = os.path.join("solicitud_intercambio.ui")
window_name, base_class = uic.loadUiType(path)


class SolicitudIntercambio(window_name, base_class):

    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.mensaje = None
        self.parent = parent
        self.boton_aceptar_intercambio.clicked.connect(self.aceptar_solicitud)
        self.boton_rechazar_intercambio.clicked.connect(self.rechazar_solicitud)

    def aceptar_solicitud(self):
        msg = {"comando": "resultado_solicitud",
               "resultado": "aceptada",
               "info": self.mensaje}
        self.parent.resultado_solicitud_signal.emit(msg)
        self.hide()

    def rechazar_solicitud(self):
        msg = {"comando": "resultado_solicitud",
               "resultado": "rechazada",
               "info": self.mensaje}
        self.parent.resultado_solicitud_signal.emit(msg)
        self.hide()

    def setear_labels(self, nombres):

        self.mensaje = nombres

        materia = ["Arcilla", "Madera", "Trigo"]
        self.nombre_jugador.setText(nombres["nombre"])
        self.nombre_jugador.setAlignment(Qt.AlignCenter)
        m_ofrece = nombres["info"]["materia_ofrecida"]
        self.materia_ofrecida.setText(materia[m_ofrece])
        self.materia_ofrecida.setAlignment(Qt.AlignCenter)
        c_ofrece = nombres["info"]["cantidad_ofrecida"]
        self.cantidad_ofrecida.setText(str(c_ofrece))
        self.cantidad_ofrecida.setAlignment(Qt.AlignCenter)

        m_pide = nombres["info"]["materia_pedida"]
        self.materia_pedida.setText(materia[m_pide])
        self.materia_pedida.setAlignment(Qt.AlignCenter)
        c_pide = nombres["info"]["cantidad_pedida"]
        self.cantidad_pedida.setText(str(c_pide))
        self.cantidad_pedida.setAlignment(Qt.AlignCenter)


if __name__ == '__main__':
    app = QApplication([])
    solicitud = SolicitudIntercambio()
    solicitud.show()
    sys.exit(app.exec_())
