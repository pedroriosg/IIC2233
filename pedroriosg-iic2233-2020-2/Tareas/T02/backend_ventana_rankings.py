import random
import os
import parametros as p
from time import sleep
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QUrl
from PyQt5.QtMultimedia import QSound


class BackVentanaRanking(QObject):

    senal_enviar_tops = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def recibir_y_analizar(self, archivo):
        # Ordenamos por ranking
        ranking = archivo
        print(ranking)
        ranking.sort(key=lambda x: x[1])
        ranking.reverse()
        ranking = ranking[:5]
        self.senal_enviar_tops.emit(ranking)
