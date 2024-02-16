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
        self.button.clicked.connect(self.map_finding)
        self.initUI()

    def getImage(self, coords1, coords2, mash):
        if (float(coords1) < 86 and float(coords2) < 86):
            map_request = f"https://static-maps.yandex.ru/1.x/?ll={coords1},{coords2}&spn=0.01,{mash}&l=map"
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
        self.image.move(60, 330)
        self.image.resize(460, 460)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space or event.key() == Qt.Key_Enter:
            self.map_finding()

    def map_finding(self):
        self.getImage(self.coords1.text(), self.coords2.text(), self.mash.text())

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapFounderApi()
    ex.show()
    sys.exit(app.exec())
