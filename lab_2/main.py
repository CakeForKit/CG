import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QWidget)
from paint import CanvasWidget

DEBUG = True

class InfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('info.ui', self)
        self.setGeometry(1000, 500, 1000, 800)

        self.ok_pbtn.clicked.connect(self.close_window)

    def close_window(self):
        self.hide()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.setGeometry(100, 100, 2000, 2000 - 700)

        # холст
        self.canvas = CanvasWidget(self)
        self.stackedWidget.addWidget(self.canvas)
        self.stackedWidget.setCurrentWidget(self.canvas)
        ##

        # кнопки
        self.shift_btn.clicked.connect(self.shift_picture)
        self.rotate_btn.clicked.connect(self.rotate_picture)
        self.scaling_btn.clicked.connect(self.scaling_picture)
        self.step_back_btn.clicked.connect(self.canvas.step_back)
        self.reset_btn.clicked.connect(self.canvas.reset)

        self.cx_dsp.valueChanged.connect(self.canvas.update)
        self.cy_dsp.valueChanged.connect(self.canvas.update)
        ##

        # меню
        self.info_widget = InfoWidget()
        self.info_qm.aboutToShow.connect(self.show_info)
        self.exit_pbtn.aboutToShow.connect(self.exit)
        ##

    def shift_picture(self):
        dx, dy = self.dx_dsp.value(), self.dy_dsp.value()
        self.canvas.shift(dx, dy)

    def rotate_picture(self):
        cx, cy = self.cx_dsp.value(), self.cy_dsp.value()
        angle = self.angle_dsp.value()
        self.canvas.rotate(cx, cy, angle)

    def scaling_picture(self):
        cx, cy = self.cx_dsp.value(), self.cy_dsp.value()
        kx, ky = self.kx_dsp.value(), self.ky_dsp.value()

        if kx == 0 or ky == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка данных")
            msg.setInformativeText('При данных значениях масштабируемая фигура превратится '
                                   'либо в точку, либо в прямую')
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        self.canvas.scaling(cx, cy, kx, ky)

    def show_info(self):
        print('show')
        self.info_widget.show()

    def exit(self):
        sys.exit(0)


def exept_hooks(cls, exeption, trades):
    sys.__excepthook__(cls, exeption, trades)


if __name__ == '__main__':
    sys.excepthook = exept_hooks
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
