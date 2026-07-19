from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt6.QtCore import Qt
import os

class MapWidget(QLabel):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setFixedSize(400,200)

        dir=os.path.dirname(os.path.abspath(__file__))

        PATH=os.path.join(dir,"world_map.png")

        self.original_pixmap=QPixmap(PATH).scaled(400,200,Qt.AspectRatioMode.IgnoreAspectRatio,Qt.TransformationMode.SmoothTransformation)

        self.setPixmap(self.original_pixmap)

    def mark_location(self,lat,lon):

        canvas = self.original_pixmap.copy()
        painter=QPainter(canvas)

        x=int(((lon+180)*400)/360)-10

        y=int(((90-lat)*200)/180)+15

        painter.setBrush(QColor("red"))
        painter.setPen(QPen(Qt.GlobalColor.black,1))
        painter.drawEllipse(x-3,y-3,6,6)

        painter.end()
        self.setPixmap(canvas)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.map_display = MapWidget(self)
        self.setCentralWidget(self.map_display)

        self.map_display.mark_location(40.7,-74.0)


if __name__=="__main__":
    app=QApplication([])
    window=MainWindow()
    window.show()
    app.exec()