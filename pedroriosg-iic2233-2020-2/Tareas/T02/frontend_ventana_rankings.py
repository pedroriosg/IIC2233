import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal

window_name, base_class = uic.loadUiType("designer_rankings.ui")


class VentanaRanking(window_name, base_class):

    senal_abrir_ventana_ranking = pyqtSignal()
    senal_volver_a_inicio = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.senal_abrir_ventana_ranking.connect(self.show)
        self.boton_ranking_volver.clicked.connect(self.vovler_a_inicio)

    def vovler_a_inicio(self):
        self.hide()
        self.senal_volver_a_inicio.emit()
    
    def actualizar_labels(self, lista):
        labels = {0: self.primer_lugar,
                  1: self.segundo_lugar,
                  2: self.tercer_lugar,
                  3: self.cuarto_lugar,
                  4: self.quinto_lugar}
        
        for i in range(0, len(lista)):
            labels[i].setText(f"{i + 1}. {lista[i][0]}: {lista[i][1]} Ptos.")

if __name__ == '__main__':
    app = QApplication([])
    ventana_ranking = VentanaRanking()
    ventana_ranking.show()
    sys.exit(app.exec_())
