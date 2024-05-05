import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox)
from PyQt5.QtGui import QColor, QPixmap
from info import InfoWidget
from canvas import Canvas
from algos import dda, brez_int, brez_float, brez_smooth, wu, lib
from figure import FigureLine, FigureSpec
from Point import Point
from errs import Errors_my
from time_graph import TimeGraphWidget
from step_graph import StepGraph
# from main_window import Ui_MainWindow

DEBUG = True

COLORS = {
    'black': QColor(0, 0, 0),
    'white': QColor(255, 255, 255),
    'red': QColor(255, 101, 101),
    'blue': QColor(106, 243, 255),
    'green': QColor(93, 186, 0)
}


class MainWindow(QMainWindow): # , Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # self.setupUi(self)
        uic.loadUi('main_window.ui', self)
        width, height = 2500, 1300
        self.setGeometry(100, 100, width, height)
        # self.setFixedSize(width, height)

        background_color = COLORS['white']
        self.line_color = COLORS['black']
        self.canvas = Canvas(self.canvas_lbl, background_color)
        self.change_line_color(self.line_color)

        # self.algos_btn_gp.buttonClicked.connect(self.choose_algos)
        self.color_btns_clicked()
        self.draw_line_btn.clicked.connect(self.draw_line)
        self.draw_spectr_btn.clicked.connect(self.draw_spectr)
        self.cmp_time_btn.clicked.connect(self.cmp_time)
        self.cmp_gradation_btn.clicked.connect(self.cmp_gradation)
        self.clear_canvas_btn.clicked.connect(self.clear_canvas)

        # меню
        self.info_widget = InfoWidget() # TODO
        self.info_qm.aboutToShow.connect(self.show_info)
        self.exit_pbtn.aboutToShow.connect(self.exit)
        ##
        self.update()

    def update(self) -> None:
        # TODO
        print('update main_window')
        # self.canvas = Canvas(self.canvas_lbl, self.background_color, self.line_color)
        self.canvas.update()
        pmp = QPixmap.fromImage(self.canvas.img)
        self.canvas_lbl.setPixmap(pmp)

    def draw_line(self):
        xbeg = self.x_beg_sb.value()
        ybeg = self.y_beg_sb.value()
        xend = self.x_end_sb.value()
        yend = self.y_end_sb.value()
        algos = self.choose_algos()
        print(f'draw_line  ({xbeg}, {ybeg}) - ({xend}, {yend}) algos: {algos}')

        fig = FigureLine(Point(xbeg, ybeg), Point(xend, yend), algos, self.line_color)
        self.canvas.add_figure(fig)

        # TODO

        self.update()

    def draw_spectr(self):
        length = self.length_sb.value()
        angle = self.angle_sb.value()
        if angle == 0:
            err = Errors_my('Угол поворота не может быть равен 0')
            err.show()
            return
        self.canvas.update()
        center = Point(self.canvas.width // 2, self.canvas.height // 2)
        algos = self.choose_algos()
        print(f'draw_spectr: len={length} angle={angle} center={center} algos={algos}')

        fig = FigureSpec(length, angle, center, algos, self.line_color)
        self.canvas.add_figure(fig)

        self.update()

    def choose_algos(self):
        if self.brezf_rb.isChecked():
            print('brezf_rb')
            algos = brez_float
        elif self.brezint_rb.isChecked():
            print('brezint_rb')
            algos = brez_int
        elif self.brezs_rb.isChecked():
            print('brezs_rb')
            algos = brez_smooth
        elif self.dda_rb.isChecked():
            print('dda_rb')
            algos = dda
        elif self.wu_rb.isChecked():
            print('wu_rb')
            algos = wu
        else:
            print('lib_rb')
            algos = lib

        return algos

    def color_btns_clicked(self):
        self.black_bg_btn.clicked.connect(self.change_background_color_to_black)
        self.white_bg_btn.clicked.connect(self.change_background_color_to_white)
        self.red_bg_btn.clicked.connect(self.change_background_color_to_red)
        self.blue_bg_btn.clicked.connect(self.change_background_color_to_blue)
        self.green_bg_btn.clicked.connect(self.change_background_color_to_green)

        self.black_line_btn.clicked.connect(self.change_line_color_to_black)
        self.white_line_btn.clicked.connect(self.change_line_color_to_white)
        self.red_line_btn.clicked.connect(self.change_line_color_to_red)
        self.blue_line_btn.clicked.connect(self.change_line_color_to_blue)
        self.green_line_btn.clicked.connect(self.change_line_color_to_green)

    def draw_background(self):
        self.canvas_lbl.setStyleSheet(f"background-color: {self.background_color.name()}")

    def change_background_color(self, color):
        self.canvas.set_background_color(color)
        # self.background_color = color
        self.update()

    def change_line_color(self, color):
        print(f'change_line_color to {color.getRgb()}')
        self.color_line_show.setStyleSheet(f"background-color: {color.name()}")
        self.line_color = color
        # self.line_color = color
        self.update()

    def change_background_color_to_black(self):
        self.change_background_color(COLORS['black'])

    def change_background_color_to_white(self):
        self.change_background_color(COLORS['white'])

    def change_background_color_to_red(self):
        self.change_background_color(COLORS['red'])

    def change_background_color_to_blue(self):
        self.change_background_color(COLORS['blue'])

    def change_background_color_to_green(self):
        self.change_background_color(COLORS['green'])

    def change_line_color_to_black(self):
        self.change_line_color(COLORS['black'])

    def change_line_color_to_white(self):
        self.change_line_color(COLORS['white'])

    def change_line_color_to_red(self):
        self.change_line_color(COLORS['red'])

    def change_line_color_to_blue(self):
        self.change_line_color(COLORS['blue'])

    def change_line_color_to_green(self):
        self.change_line_color(COLORS['green'])

    def cmp_time(self):
        print('cmp_time')
        self.time_graph = TimeGraphWidget(self.canvas_lbl)
        self.time_graph.show()

        # TODO

    def cmp_gradation(self):
        print('cmp_gradation')
        StepGraph()
        # TODO

    def clear_canvas(self):
        print('clear_canvas')
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
