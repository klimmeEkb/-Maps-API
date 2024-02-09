import os
import sys
import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton

class Example(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("design.ui", self)
        #self.button.clicked.connect(self.map_finding)
        self.initUI()

    def getImage(self, coords1, coords2):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={coord1},{coords2}&spn=0.002,0.002&l=map"
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        else:
            self.pixmap = QPixmap(self.map_file)
            self.image = QLabel(self)
            self.image.move(120, 330)
            self.image.resize(460, 460)
            self.image.setPixmap(self.pixmap)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setWindowTitle('Большая задача по Maps API')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.map_finding()

    def map_finding(self):
        self.getImage(self.coords1.text(), self.coords2.text())

    def close(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
