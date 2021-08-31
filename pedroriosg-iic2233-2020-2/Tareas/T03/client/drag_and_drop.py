import os
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtCore import QMimeData, Qt


class Choza(QLabel):

    def __init__(self, parent, _id, color, coordenadas):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setScaledContents(True)
        self.setGeometry(coordenadas[0] - 12.5, coordenadas[1] - 12.5,
                         25, 25)
        self.color = color
        self.parent = parent
        self._id = _id
        self.disponible = True
        if self.color is not None:
            self.setear_color(self.color)
        else:
            self.show()

    def dragEnterEvent(self, event):
        if self.disponible:
            if event.mimeData().hasImage():
                print("event accepted")
                event.accept()
            else:
                print("event rejected")
                event.ignore()

    def dropEvent(self, event):
        fuente = event.source()
        self.color = fuente.color
        tipo = fuente.tipo
        if tipo == "choza":
            msg = {"comando": "verificar_choza", "identificacion_choza":
                   [self._id, self.color]}
            self.parent.verificar_construccion_choza_signal.emit(msg)

    def setear_color(self, color):
        self.color = color
        if self.color == "rojo":
            self.color = "roja"
        ruta = os.path.join("sprites", "Construcciones", f"choza_{self.color}.png")
        pixeles_choza = QPixmap(ruta)
        self.setPixmap(pixeles_choza)
        self.disponible = False
        self.show()


class Camino(QLabel):

    def __init__(self, parent, _id, orientacion, color, coordenadas):
        super().__init__(parent)
        self.parent = parent
        self.setAcceptDrops(True)
        self.setScaledContents(True)
        self.coordenadas = coordenadas
        self.color = color
        self._id = _id
        self.orientacion = orientacion
        self.disponible = True
        self.definir_geometria()
        if self.color is not None:
            self.setear_color(self.color)
        else:
            self.show()

    def dragEnterEvent(self, event):
        if self.disponible:
            if event.mimeData().hasImage():
                print("event accepted")
                event.accept()
            else:
                print("event rejected")
                event.ignore()

    def dropEvent(self, event):
        fuente = event.source()
        self.color = fuente.color
        tipo = fuente.tipo
        if tipo == "camino":
            msg = {"comando": "verificar_camino", "identificacion_camino":
                   [self._id, self.color]}
            self.parent.verificar_construccion_camino_signal.emit(msg)

    def definir_geometria(self):
        geometrias = {"0": [50, 17], "60": [40, 52], "120": [40, 52]}
        x = self.coordenadas[0]
        y = self.coordenadas[1]
        # Para Label 120
        self.setGeometry(x, y, geometrias[self.orientacion][0],
                         geometrias[self.orientacion][1])

    def setear_color(self, color):
        self.color = color
        ruta = os.path.join("sprites", "Construcciones",
                            f"camino_{self.color}_{self.orientacion}.png")
        pixeles_camino = QPixmap(ruta)
        self.setPixmap(pixeles_camino)
        self.show()
        self.disponible = False


class Construccion(QLabel):

    def __init__(self, parent, image, color, tipo, turno):
        super(QLabel, self).__init__(parent)
        self.setScaledContents(True)
        self.setPixmap(QPixmap(image))
        self.show()
        self.tipo = tipo
        self.color = color
        self.turno = False

    def mousePressEvent(self, event):
        if self.turno:
            if event.button() == Qt.LeftButton:
                self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if self.turno:
            if not (event.buttons() & Qt.LeftButton):
                return
            if (event.pos() - self.drag_start_position).manhattanLength() \
               < QApplication.startDragDistance():
                return

            drag = QDrag(self)
            mimedata = QMimeData()
            mimedata.setText(self.text())
            mimedata.setImageData(self.pixmap().toImage())

            drag.setMimeData(mimedata)
            pixmap = QPixmap(self.size())
            painter = QPainter(pixmap)
            painter.drawPixmap(self.rect(), self.grab())
            painter.end()
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())
            drag.exec_(Qt.CopyAction | Qt.MoveAction)
