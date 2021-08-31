import sys
import os
import parametros as p
from time import sleep
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor, QImage
from PyQt5.QtCore import QMimeData, Qt, QTimer, QThread, QObject, pyqtSignal


class Espacio(QLabel):

    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.disponible = False
        self.color = None
        self.dinero = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            print("event accepted")
            event.accept()
        else:
            print("event rejected")
            event.ignore()

    def dropEvent(self, event):
        poder = True
        print(self.dinero)
        print(p.VALUE_PINGUIRIN)
        if self.dinero < p.VALUE_PINGUIRIN:
            self.setAcceptDrops(False)
            print("No puedes comprar")
            poder = False
        if event.mimeData().hasImage() and poder:
            self.setPixmap(QPixmap.fromImage(QImage(event.mimeData().imageData())))
            self.setAcceptDrops(False)
            self.disponible = True
            fuente = event.source()
            self.color = fuente.color

    def moverse(self, paso):
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.volver)
        if len(paso) == 1:
            for flecha in paso:
                orientacion = flecha.orientacion
                if orientacion == p.LEFT_ARROW:
                    ruta = os.path.join("sprites", f"pinguirin_{self.color}",
                                        f"{self.color}_izquierda.png")
                elif orientacion == p.RIGHT_ARROW:
                    ruta = os.path.join("sprites", f"pinguirin_{self.color}",
                                        f"{self.color}_derecha.png")
                elif orientacion == p.DOWN_ARROW:
                    ruta = os.path.join("sprites", f"pinguirin_{self.color}",
                                        f"{self.color}_arriba.png")
                elif orientacion == p.UP_ARROW:
                    ruta = os.path.join("sprites", f"pinguirin_{self.color}",
                                        f"{self.color}_abajo.png")

        elif len(paso) == 2:
            orientaciones = (paso[0].orientacion, paso[1].orientacion)
            if  p.LEFT_ARROW in orientaciones and p.UP_ARROW in orientaciones:
                ruta = os.path.join("sprites", f"pinguirin_{self.color}",
                                    f"{self.color}_arriba_izquierda.png")
            elif p.RIGHT_ARROW in orientaciones and p.UP_ARROW in orientaciones:
                ruta = os.path.join("sprites", f"pinguirin_{self.color}",
                                    f"{self.color}_arriba_derecha.png")
            elif p.LEFT_ARROW in orientaciones and p.DOWN_ARROW in orientaciones:
                ruta = os.path.join("sprites", f"pinguirin_{self.color}",
                                    f"{self.color}_abajo_izquierda.png")
            elif p.RIGHT_ARROW in orientaciones and p.DOWN_ARROW in orientaciones:
                ruta = os.path.join("sprites", f"pinguirin_{self.color}",
                                    f"{self.color}_abajo_derecha.png")

        elif len(paso) == 3:
            ruta = os.path.join("sprites", f"pinguirin_{self.color}",
                                f"{self.color}_tres_flechas.png")

        pixeles = QPixmap(ruta)
        self.setPixmap(pixeles)
        self.timer.start()

    def volver(self):
        original = os.path.join("sprites", f"pinguirin_{self.color}", f"{self.color}_neutro.png")
        pixeles = QPixmap(original)
        self.setPixmap(pixeles)


class Piguirin(QLabel):

    def __init__(self, parent, image, color):
        super(QLabel, self).__init__(parent)
        self.setPixmap(QPixmap(image))
        self.show()
        self.color = color
        self.tienda_open = True

    def mousePressEvent(self, event):
        if self.tienda_open:
            if event.button() == Qt.LeftButton:
                self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if self.tienda_open:
            if not (event.buttons() & Qt.LeftButton):
                return
            if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
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
