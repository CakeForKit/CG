import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from info import InfoWidget
from canvas import Canvas
from structs import *
from figure import *
from errs import Errors_my, BaseErr


NS_TO_MS = 1e3 # 1e-3
# from main_window import Ui_MainWindow

import time
DEBUG = True

COLORS = {
    'black': QColor(0, 0, 0),
    'white': QColor(255, 255, 255),
    'yellow': QColor(255, 255, 102),
    'red': QColor(255, 101, 101),
    'blue': QColor(106, 243, 255),
    'green': QColor(93, 186, 0)
}


class MainWindow(QMainWindow):  # , Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # self.setupUi(self)
        uic.loadUi('main_window.ui', self)
        width, height = 2500, 1200
        self.setGeometry(50, 50, width, height)

        self.openfigure = OpenFigure()

        self.background_color = COLORS['white']
        self.line_color = COLORS['black']
        self.canvas = Canvas(self.canvas_lbl, self.line_color, self.background_color)
        self.change_line_color(self.line_color)

        self.color_btns_clicked()
        self.clear_canvas_btn.clicked.connect(self.clear_canvas)
        self.add_point_btn.clicked.connect(self.add_point_by_btn)
        self.close_figure_btn.clicked.connect(self.close_figure)
        self.fill_figures_btn.clicked.connect(self.fill_figures)

        # меню
        self.info_widget = InfoWidget()
        self.info_qm.aboutToShow.connect(self.show_info)
        self.exit_pbtn.aboutToShow.connect(self.exit)
        ##
        self.update()

        # self.add_point(100, 100)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            x, y = event.x(), event.y()
            rect_lbl = self.canvas_lbl.geometry()
            if rect_lbl.contains(x, y):
                mb = self.menubar.geometry()
                x -= rect_lbl.x()
                y -= rect_lbl.y() + mb.height()
                print(f"EVENT ==== ({x, y}) --- ({rect_lbl.topLeft().x(), rect_lbl.topLeft().y()})")
                event.accept()

                self.add_point(x, y)

    def update(self) -> None:
        print('update main_window')

        self.canvas.update()
        self.openfigure.draw(self.canvas)

        pmp = QPixmap.fromImage(self.canvas.img)
        self.canvas_lbl.setPixmap(pmp)

        self.print_figures_data()
        QApplication.processEvents()

    def fill_figures(self):
        self.canvas.colour = self.line_color
        self.canvas.fill_new_figures()
        delay = self.choose_delay()
        time = self.canvas.fill_all_figures(delay)

        self.canvas.update()

        if time == -1:
            self.time_le.setText(f'-')
        else:
            self.time_le.setText(f'{time * NS_TO_MS:.1f}')
        # self.openfigure.draw(self.canvas)
        # pmp = QPixmap.fromImage(self.canvas.img)
        # self.canvas_lbl.setPixmap(pmp)


    def add_point(self, x, y):
        p = Point(x, y)
        if p in self.openfigure.points:
            errm = Errors_my(ErrPointExistInFigure.text())
            errm.show()
            return
        self.openfigure.add_point(p)
        # self.update()
        self.openfigure.draw(self.canvas)
        self.print_figures_data()

    def add_point_by_btn(self):
        x = self.x_sp.value()
        y = self.y_sp.value()
        self.add_point(x, y)

    def close_figure(self):
        if not self.openfigure.can_close():
            errm = Errors_my(ErrCanNotCloseFigure.text())
            errm.show()
            return

        cf = Figure(self.openfigure)
        self.openfigure = OpenFigure()
        self.canvas.add_figure(cf)
        self.update()

    def print_figures_data(self):
        text = self.canvas.get_text_figures_data()
        text += f'{" " * 6}OpenFigure{" " * 6}\n' + self.openfigure.get_text_points()
        self.points_textEdit.setPlainText(text)

    def choose_delay(self):
        if self.delay_rbn.isChecked():
            print("with delay")
            return True
        else:
            print('NO delay')
            return False

    def color_btns_clicked(self):
        self.black_line_btn.clicked.connect(self.change_line_color_to_black)
        self.yellow_line_btn.clicked.connect(self.change_line_color_to_yellow)
        self.red_line_btn.clicked.connect(self.change_line_color_to_red)
        self.blue_line_btn.clicked.connect(self.change_line_color_to_blue)
        self.green_line_btn.clicked.connect(self.change_line_color_to_green)

    def change_line_color(self, color):
        print(f'change_line_color to {color.getRgb()}')
        self.color_line_show.setStyleSheet(f"background-color: {color.name()}")
        self.line_color = color
        # self.update()

    def change_line_color_to_black(self):
        self.change_line_color(COLORS['black'])

    def change_line_color_to_yellow(self):
        self.change_line_color(COLORS['yellow'])

    def change_line_color_to_red(self):
        self.change_line_color(COLORS['red'])

    def change_line_color_to_blue(self):
        self.change_line_color(COLORS['blue'])

    def change_line_color_to_green(self):
        self.change_line_color(COLORS['green'])

        print('cmp_time_ellipse')

    def clear_canvas(self):
        print('clear_canvas')
        self.openfigure = OpenFigure()
        self.canvas.clear_canvas()
        self.update()

    def show_info(self):
        print('show info')
        self.info_widget.show()

    def resizeEvent(self, event):
        self.update()

    def exit(self):
        sys.exit(0)


def exept_hooks(cls, exeption, trades):
    sys.__excepthook__(cls, exeption, trades)


if __name__ == '__main__':
    sys.excepthook = exept_hooks
    app = QApplication(sys.argv)
    main = MainWindow()
    main.update()
    main.show()
    sys.exit(app.exec())
