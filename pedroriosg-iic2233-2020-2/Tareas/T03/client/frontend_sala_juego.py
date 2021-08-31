import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal
from drag_and_drop import Construccion, Choza, Camino
from frontend_monopolio import Monopolio
from frontend_intercambio import Intercambio
from frontend_solicitud_intercambio import SolicitudIntercambio
from frontend_fin_partida import FinPartida

path = os.path.join("sala_juego.ui")
window_name, base_class = uic.loadUiType(path)


class SalaJuego(window_name, base_class):

    lanzar_dado_signal = pyqtSignal(dict)
    pasar_turno_signal = pyqtSignal(dict)
    comprar_signal = pyqtSignal(dict)
    verificar_construccion_choza_signal = pyqtSignal(dict)
    verificar_construccion_camino_signal = pyqtSignal(dict)
    enviar_monopolio_signal = pyqtSignal(dict)
    enviar_intercambio_signal = pyqtSignal(dict)
    resultado_solicitud_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.monopolio = Monopolio(self)
        self.intercambio = Intercambio(self)
        self.solicitud_intercambio = SolicitudIntercambio(self)
        self.fin = FinPartida(self)
        self.rgb = {"rojo": "(195, 0, 0)", "verde": "(40, 163, 84)",
                    "azul": "(3, 3, 231)", "violeta": "(189, 0, 216)"}
        self.mi_nombre = None
        self.mi_color = None
        self.pos_nodos = None
        self.dragueables = []
        self.estadisticas_personales = []
        self.estadisticas_otros = []
        self.dados = []
        self.boton_lanzar.clicked.connect(self.lanzar_dado)
        self.boton_pasar.clicked.connect(self.pasar_turno)
        self.boton_comprar.clicked.connect(self.comprar)
        self.boton_negociar.clicked.connect(self.negociar)

    def crear_hexagonos(self, tupla):
        # nodos_clave para posicionar los nodos
        nodos_clave = {"0": "0", "2": "1", "5": "2", "7": "3", "9": "4",
                       "11": "5", "15": "6", "17": "7", "19": "8", "21": "9"}
        # hexagonos nos da la informacion de cada hexágono
        # {_id: [numero_ficha, materia_prima]}
        hexagonos = tupla[0]
        # pos_nodos nos da la informacion de cada nodo
        # {_id: [x, y}
        pos_nodos = tupla[1]
        self.pos_nodos = pos_nodos
        ancho = pos_nodos["5"][0] - pos_nodos["4"][0]
        alto = pos_nodos["9"][1] - pos_nodos["0"][1]
        for nodo in nodos_clave:
            hexa = nodos_clave[nodo]
            pos_x = pos_nodos[nodo][0]
            pos_y = pos_nodos[nodo][1]
            self.label_hex = QLabel(self)
            self.label_hex.setGeometry(pos_x - (ancho / 4), pos_y, ancho, alto)
            ruta_hex = os.path.join("sprites", "Materias_primas",
                                    f"hexagono_{hexagonos[hexa][1]}.png")
            self.label_hex.setScaledContents(True)
            pixeles_hex = QPixmap(ruta_hex)
            self.label_hex.setPixmap(pixeles_hex)
            self.label_hex.show()

        for nodo in nodos_clave:
            hexa = nodos_clave[nodo]
            pos_x = pos_nodos[nodo][0]
            pos_y = pos_nodos[nodo][1]
            self.label_num = QLabel(self)
            self.label_num.setGeometry(pos_x + (ancho / 32), pos_y + (alto / 4),
                                       alto / 2, alto / 2)
            ruta_num = os.path.join("sprites", "Materias_primas", "ficha_numero.png")
            self.label_num.setScaledContents(True)
            pixeles_num = QPixmap(ruta_num)
            self.label_num.setPixmap(pixeles_num)
            self.label_num.show()
            self.label_num_2 = QLabel(f"{hexagonos[hexa][0]}", self)
            self.label_num_2.setGeometry(pos_x + (ancho / 32), pos_y + (alto / 4),
                                         alto / 2, alto / 2)
            self.label_num_2.setFont(QFont("Courier New", 24))
            if hexagonos[hexa][0] != 6 and hexagonos[hexa][0] != 8:
                self.label_num_2.setStyleSheet("color: rgb(0, 0, 0)")
            else:
                self.label_num_2.setStyleSheet("color: rgb(255, 0, 0)")
            self.label_num_2.setAlignment(Qt.AlignCenter)
            self.label_num_2.show()

    def crear_labels_personal(self, informacion):
        # Creamos QLabel para su nombre
        self.mi_nombre = informacion["nombre"]
        self.mi_color = informacion["color"]
        self.label_nombre = QLabel(f"{informacion['nombre']} (TÚ)", self)
        self.label_nombre.setGeometry(840, 660, 241, 30)
        self.label_nombre.setFont(QFont("Courier New", 16))
        self.label_nombre.setStyleSheet(f"color: rgb{self.rgb[informacion['color']]}")
        self.label_nombre.setAlignment(Qt.AlignCenter)
        self.label_nombre.show()
        # Creamos QLabel (Dropeable) para Choza
        if informacion["color"] == "rojo":
            ruta_choza = os.path.join("sprites", "Construcciones", "choza_roja.png")
        else:
            ruta_choza = os.path.join("sprites", "Construcciones",
                                      f"choza_{informacion['color']}.png")
        self.label_choza_drop = Construccion(self, ruta_choza, informacion['color'], "choza",
                                             informacion['turno'])
        self.label_choza_drop.setGeometry(463, 733, 25, 25)
        self.dragueables.append(self.label_choza_drop)
        # Creamos QLabel (Dropeable) para Camino
        ruta_camino = os.path.join("sprites", "Construcciones",
                                   f"camino_{informacion['color']}_0.png")
        self.label_camino_drop = Construccion(self, ruta_camino, informacion['color'], "camino",
                                              informacion['turno'])
        self.label_camino_drop.setGeometry(543, 738, 45, 15)
        self.dragueables.append(self.label_camino_drop)
        # Creamos QLabel para Cartas y Puntos
        lista = ["arcilla", "madera", "trigo", "cartas", "puntos"]
        x = 120
        y = 726
        posiciones = {1: 130, 2: 130, 3: 540, 4: 130, 5: 0}
        contador = 0
        for elemento in lista:
            self.numero = QLabel(f"{informacion[elemento]}", self)
            self.numero.setGeometry(x, y, 35, 30)
            self.numero.setFont(QFont("Courier New", 18))
            self.numero.show()
            contador += 1
            x += posiciones[contador]
            self.estadisticas_personales.append(self.numero)

    def crear_labels_otros(self, informacion):

        # Crearemos primero los nombres y string puntos
        x_nombre = 840
        y_nombre = 90
        x_v = 920
        y_v = 110
        for jugador in informacion:
            self.label_n = QLabel(f"{jugador['nombre']}", self)
            self.label_n.setGeometry(x_nombre, y_nombre, 241, 30)
            self.label_n.setFont(QFont("Courier New", 14))
            self.label_n.setStyleSheet(f"color: rgb{self.rgb[jugador['color']]}")
            self.label_n.setAlignment(Qt.AlignCenter)
            self.label_n.show()
            self.label_v = QLabel("PUNTOS:", self)
            self.label_v.setGeometry(x_v, y_v, 61, 30)
            self.label_v.setFont(QFont("Courier New", 13))
            self.label_v.show()
            y_nombre += 160
            y_v += 160
        # Ahora posicionaremos las fotos de materias primas
        materias = ["arcilla", "madera", "trigo"]
        x = 860
        y = 150
        for materia in materias:
            lista_materias = []
            y_m = 210
            for _ in range(len(informacion)):
                self.label_f = QLabel(self)
                self.label_f.setGeometry(x, y, 35, 50)
                ruta_f = os.path.join("sprites", "Materias_primas", f"carta_{materia}.png")
                self.label_f.setScaledContents(True)
                pixeles_f = QPixmap(ruta_f)
                self.label_f.setPixmap(pixeles_f)
                self.label_f.show()
                y += 160
                self.label_p = QLabel(f"{informacion[_][materia]}", self)
                self.label_p.setGeometry(x, y_m, 35, 30)
                self.label_p.setFont(QFont("Courier New", 18))
                self.label_p.setAlignment(Qt.AlignCenter)
                self.label_p.show()
                lista_materias.append(self.label_p)
                y_m += 160
            self.estadisticas_otros.append(lista_materias)
            y = 150
            x += 80

        # Ahora crearemos los puntos de victoria de cada jugador
        x = 980
        y = 115
        puntos_victoria = []
        for _ in range(len(informacion)):
            self.label_pv = QLabel(self)
            self.label_pv = QLabel(f"{informacion[_]['puntos']}", self)
            self.label_pv.setGeometry(x, y, 35, 21)
            self.label_pv.setFont(QFont("Courier New", 13))
            self.label_pv.setAlignment(Qt.AlignCenter)
            self.label_pv.show()
            puntos_victoria.append(self.label_pv)
            y += 160
        self.estadisticas_otros.append(puntos_victoria)

    def crear_labels_chozas_caminos(self, informacion):
        self.chozas = []
        # Creamos las CHOZAS
        for nodo in informacion[0]:
            posicion = self.pos_nodos[nodo]
            self.label_choza = Choza(self, nodo, informacion[0][nodo], posicion)
            self.chozas.append(self.label_choza)
        pos = {"01": [150, 70], "23": [450, 70], "910": [150, 240], "1112": [450, 240],
               "1920": [150, 410], "2122": [450, 410], "2930": [150, 585],
               "3132": [450, 585], "56": [300, 155], "78": [600, 155], "1516": [300, 325],
               "1718": [600, 325], "2526": [300, 500], "2728": [600, 500], "04": [80, 100],
               "15": [230, 100], "26": [380, 100], "37": [530, 100], "49": [80, 180],
               "510": [230, 180], "611": [380, 180], "712": [530, 180], "813": [680, 180],
               "914": [80, 270], "1015": [230, 270], "1116": [380, 270], "1217": [530, 270],
               "1318": [680, 270], "1419": [80, 350], "1520": [230, 350], "1621": [380, 350],
               "1722": [530, 350], "1823": [680, 350], "1924": [80, 440], "2025": [230, 440],
               "2126": [380, 440], "2227": [530, 440], "2328": [680, 440], "2429": [80, 520],
               "2530": [230, 530], "2631": [380, 520], "2732": [530, 530]}
        self.caminos = []
        for ide in pos:
            info = informacion[1][ide]
            self.label = Camino(self, ide, info[1], info[0], pos[ide])
            self.caminos.append(self.label)

    def cambiar_turno(self, info):
        # Cambia Label del Jugador
        nombre = info[0]
        color = info[1]
        self.label_turno_jugador.setText(nombre)
        self.label_turno_jugador.setStyleSheet(f"color: rgb{self.rgb[color]}")
        self.label_turno_jugador.setAlignment(Qt.AlignCenter)

    def mi_turno(self):
        self.boton_lanzar.setEnabled(True)
        self.boton_negociar.setEnabled(True)
        self.boton_comprar.setEnabled(True)
        for dragueable in self.dragueables:
            dragueable.turno = True

    def pasar_turno(self):
        msg = {"comando": "pasar_turno"}
        self.pasar_turno_signal.emit(msg)
        self.boton_lanzar.setEnabled(False)
        self.boton_pasar.setEnabled(False)
        self.boton_negociar.setEnabled(False)
        self.boton_comprar.setEnabled(False)
        for dragueable in self.dragueables:
            dragueable.turno = False

    def lanzar_dado(self):
        msg = {"comando": "lanzar_dado"}
        self.lanzar_dado_signal.emit(msg)
        self.boton_lanzar.setEnabled(False)
        self.boton_pasar.setEnabled(True)

    def comprar(self):
        msg = {"comando": "comprar_carta"}
        self.comprar_signal.emit(msg)

    def actualizar_labels_personal(self, informacion):
        # Actualizamos QLabel para Cartas y Puntos
        lista = ["arcilla", "madera", "trigo", "cartas", "puntos"]
        contador = 0
        for label in self.estadisticas_personales:
            label.setText(f"{informacion[lista[contador]]}")
            contador += 1

    def actualizar_labels_otros(self, informacion):
        lista = ["arcilla", "madera", "trigo", "puntos"]
        contador = 0
        for lis in self.estadisticas_otros:
            contador_jug = 0
            for label in lis:
                label.setText(f"{informacion[contador_jug][lista[contador]]}")
                contador_jug += 1
            contador += 1

    def actualizar_dados(self, informacion):
        numeros = {0: informacion[0], 1: informacion[1]}
        pos = {0: 669, 1: 749}
        for _ in self.dados:
            _.hide()
        for _ in range(2):
            self.label_dado = QLabel(self)
            self.label_dado.setGeometry(pos[_], 630, 51, 51)
            ruta_dado = os.path.join("sprites", "Dados",
                                     f"dado_{str(numeros[_])}.png")
            self.label_dado.setScaledContents(True)
            pixeles_dado = QPixmap(ruta_dado)
            self.label_dado.setPixmap(pixeles_dado)
            self.label_dado.show()
            self.dados.append(self.label_dado)

    def actualizar_choza(self, informacion):
        if informacion[0]:
            for choza in self.chozas:
                if choza._id == informacion[1][0]:
                    choza.setear_color(informacion[1][1])

    def warning(self, resultado):
        if not resultado:
            msg = QMessageBox()
            msg.setWindowTitle("CHOZA INCORRECTA")
            msg.setText("¡NO PUEDES CONSTRUIR EN ESE LUGAR!")
            msg.exec_()

    def actualizar_camino(self, informacion):
        if informacion[0]:
            for camino in self.caminos:
                if camino._id == informacion[1][0]:
                    camino.setear_color(informacion[1][1])

    def manejar_carta(self, carta):
        if carta == "victoria":
            msg = QMessageBox()
            msg.setText("¡PUNTO DE VICTORIA PARA TI!")
            msg.exec_()
        elif carta == "monopolio":
            self.monopolio.show()
        else:
            msg = QMessageBox()
            msg.setText("¡NO PUEDES COMPRAR CARTAS!")
            msg.exec_()

    def setear_nombres_intercmabio(self, nombres):
        self.intercambio.setear_nombres(nombres)

    def negociar(self):
        self.intercambio.show()

    def solicitud_de_intercambio(self, mensaje):
        self.solicitud_intercambio.setear_labels(mensaje)
        self.solicitud_intercambio.show()

    def intercambio_no_apto(self):
        msg = QMessageBox()
        msg.setText("¡INTERCAMBIO NO APTO!")
        msg.exec_()

    def intercambio_final(self, msg):
        final = ""
        if msg == "exitoso":
            final = "¡INTERCAMBIO EXITOSO!"
        elif msg == "fracasado":
            final = "¡INTERCAMBIO FRACASAD0!"
        msg = QMessageBox()
        msg.setText(final)
        msg.exec_()

    def nombres_fin_partida(self, nombres):
        self.fin.setear_nombres(nombres)

    def resultados_partida(self, resultado):
        self.fin.setear_resultados(resultado)

    def actualizar_label_carretera(self, info):
        self.label_carretera.setText(info[0])
        self.label_carretera.setStyleSheet(f"color: rgb{self.rgb[info[1]]}")
        self.label_carretera.setAlignment(Qt.AlignCenter)

    def empate_carretera(self):
        self.label_carretera.setText("NADIE")
        self.label_carretera.setStyleSheet("color: rgb(0, 0, 0)")
        self.label_carretera.setAlignment(Qt.AlignCenter)


if __name__ == '__main__':
    app = QApplication([])
    sala_juego = SalaJuego()
    sala_juego.show()
    sys.exit(app.exec_())
