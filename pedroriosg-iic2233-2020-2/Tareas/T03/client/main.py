"""
Módulo principal del cliente
"""
import sys
from PyQt5.QtWidgets import QApplication
from cliente import Cliente

if __name__ == "__main__":

    APP = QApplication([])
    # Se instancia el Cliente.
    CLIENTE = Cliente()

    # Se inicia la app de PyQt.
    ret = APP.exec_()
    sys.exit(ret)
