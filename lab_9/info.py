from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class InfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('info.ui', self)
        self.setGeometry(1000, 500, 1000, 800)

        self.ok_pbtn.clicked.connect(self.close_window)

    def close_window(self):
        self.hide()
