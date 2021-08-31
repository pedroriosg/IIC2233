"""
Módulo principal del servidor
"""
from servidor import Servidor

if __name__ == "__main__":

    SERVIDOR = Servidor()

    try:
        while True:
            input("Presione Ctrl+C para cerrar el servidor...")
    except KeyboardInterrupt:
        print("Cerrando servidor...")
