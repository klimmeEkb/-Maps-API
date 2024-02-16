import os
import sys
import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
import pathlib
import os
import os.path


class MapFounderApi(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.abspath("design.ui"), self)
        self.i = 0.0
        self.button.clicked.connect(self.map_finding)
        self.initUI()

    def getImage(self, coords1, coords2, mash, i):
        if (float(coords1) < 86 and float(coords2) < 86 and float(mash) <= 90 and float(i) + float(mash) >= 0 and float(mash) <= 90 and float(i) + float(mash) <= 90):
            map_request = f"https://static-maps.yandex.ru/1.x/?ll={coords1},{coords2}&spn=0.01,{str(float(mash) + float(i))}&l=map"
            response = requests.get(map_request)
            if not response:
                print("Ошибка выполнения запроса:")
                print(map_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)    
            self.map_file = os.path.abspath("map.png")
            with open(self.map_file, "wb") as file:
                file.write(response.content)
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.setWindowTitle('Большая задача по Maps API')
        self.image = QLabel(self)
        self.image.move(100, 375)
        self.image.resize(400, 400)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space or event.key() == Qt.Key_Enter:
            self.map_finding()
            self.i = 0
        if event.key() == Qt.Key_PageUp:
            self.i -= 0.5
            self.map_finding()
        if event.key() == Qt.Key_PageDown:
            self.i += 0.5
            self.map_finding()

    def map_finding(self):
        self.getImage(self.coords1.text().strip(), self.coords2.text().strip(), self.mash.text().strip(), self.i)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapFounderApi()
    ex.show()
    sys.exit(app.exec())
