import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from info import InfoWidget
from canvas import Canvas
from structs import *
from random import randint
from algos import simple_cut
from errs import Errors_my, BaseErr

NS_TO_MS = 1e3  # 1e-3

DEBUG = True

COLORS = {
    'purple': QColor(170, 85, 255),
    'black': QColor(0, 0, 0),
    'yellow': QColor(255, 255, 102),
    'red': QColor(255, 101, 101),
    'blue': QColor(0, 0, 255),
    'green': QColor(93, 186, 0)
}


class MainWindow(QMainWindow):  # , Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # self.setupUi(self)
        uic.loadUi('main_window.ui', self)
        width, height = 2500, 1500
        self.setGeometry(50, 50, width, height)

        self.background_color = QColor(255, 255, 255)
        self.clipper_color = COLORS['black']
        self.line_color = COLORS['red']
        self.res_color = COLORS['green']
        self.canvas = Canvas(self.canvas_lbl, self.background_color)

        self.change_clipper_color(self.clipper_color)
        self.change_line_color(self.line_color)
        self.change_res_color(self.res_color)

        self.color_btns_clicked()
        self.clear_canvas_btn.clicked.connect(self.clear_canvas)
        self.draw_clipper_btn.clicked.connect(self.new_clipper_by_btn)
        self.draw_line_btn.clicked.connect(self.draw_line_by_btn)
        self.draw_random_lines_btn.clicked.connect(self.draw_random_lines)
        self.cut_btn.clicked.connect(self.cut_lines)

        # меню
        self.info_widget = InfoWidget()
        self.info_qm.aboutToShow.connect(self.show_info)
        self.exit_pbtn.aboutToShow.connect(self.exit)
        ##

        self.points_for_line = []
        self.points_for_clipper = []

    def is_in_label(self, p):
        rect_lbl = self.canvas_lbl.geometry()
        if rect_lbl.contains(p.x, p.y):
            mb = self.menubar.geometry()
            p.x -= rect_lbl.x()
            p.y -= rect_lbl.y() + mb.height()

            return True
        return False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            p = Point(event.x(), event.y())
            if self.is_in_label(p):
                event.accept()
                if len(self.points_for_line) == 0:
                    self.points_for_line.append(p)
                else:
                    self.points_for_line.append(p)
                    self.add_draw_line(*self.points_for_line)
                    self.points_for_line = []
                # self.points_for_line = [p, p]
                # print(f'mousePressEvent: {self.points_for_line}')
                # self.canvas.redraw()
                # self.canvas.draw_line(Line(p, p, self.line_color))
        elif event.button() == Qt.RightButton:
            p = Point(event.x(), event.y())
            if self.is_in_label(p):
                event.accept()
                self.points_for_clipper = [p, p]
                print(f'mousePressEvent: {self.points_for_clipper}')
                # self.canvas.redraw()
                # self.canvas.new_clipper(*self.points_for_clipper, self.clipper_color)
                # self.canvas.draw_clipper()
                self.new_clipper(*self.points_for_clipper)

    def mouseMoveEvent(self, event):
        # if event.buttons() == Qt.LeftButton:
        #     p = Point(event.x(), event.y())
        #     if self.is_in_label(p):
        #         event.accept()
        #         self.points_for_line[1] = p
        #         print(f'mouseMoveEvent: {self.points_for_line}')
        #         self.canvas.redraw()
        #         self.canvas.draw_line(Line(*self.points_for_line, self.line_color))
        if event.buttons() == Qt.RightButton:
            p = Point(event.x(), event.y())
            if self.is_in_label(p):
                event.accept()
                self.points_for_clipper[1] = p
                # self.canvas.redraw()
                # self.canvas.new_clipper(*self.points_for_clipper, self.clipper_color)
                # self.canvas.draw_clipper()
                self.new_clipper(*self.points_for_clipper)
                print(f'mouseMoveEvent: {self.canvas.clipper}')

    def mouseReleaseEvent(self, event):
        # if event.button() == Qt.LeftButton:
        #     p = Point(event.x(), event.y())
        #     if self.is_in_label(p):
        #         event.accept()
        #         self.points_for_line[1] = p
        #         # print(f'mouseReleaseEvent: {self.points_for_line}')
        #         self.canvas.redraw()
        #         self.add_draw_line(*self.points_for_line)
        if event.button() == Qt.RightButton:
            p = Point(event.x(), event.y())
            if self.is_in_label(p):
                event.accept()
                self.points_for_clipper[1] = p
                # self.canvas.redraw()
                # self.canvas.new_clipper(*self.points_for_clipper, self.clipper_color)
                # self.canvas.draw_clipper()
                self.new_clipper(*self.points_for_clipper)
                print(f'mouseReleaseEvent: {self.canvas.clipper}')

    def cut_lines(self):
        simple_cut(self.canvas.qp, self.canvas.lines, self.res_color, self.canvas.clipper)
        self.canvas.import_img()

    def new_clipper_by_btn(self):
        x1 = self.clipper_x1_sp.value()
        y1 = self.clipper_y1_sp.value()
        x2 = self.clipper_x2_sp.value()
        y2 = self.clipper_y2_sp.value()
        self.new_clipper(Point(x1, y1), Point(x2, y2))

    def new_clipper(self, p1: Point, p2: Point):
        self.canvas.new_clipper(p1, p2, self.clipper_color)
        self.canvas.redraw()
        self.show_data_scene()

    def draw_line_by_btn(self):
        x1 = self.line_x1_sp.value()
        y1 = self.line_y1_sp.value()
        x2 = self.line_x2_sp.value()
        y2 = self.line_y2_sp.value()
        self.add_draw_line(Point(x1, y1), Point(x2, y2))

    def add_draw_line(self, p1: Point, p2: Point):
        self.canvas.add_draw_line(p1, p2, self.line_color)
        self.show_data_scene()

    def draw_random_lines(self):
        for i in range(5):
            x1 = randint(0, self.canvas.width)
            y1 = randint(0, self.canvas.height)
            x2 = randint(0, self.canvas.width)
            y2 = randint(0, self.canvas.height)
            self.add_draw_line(Point(x1, y1), Point(x2, y2))


    def show_data_scene(self):
        text = ''

        text += '----- Отсекатель -----\n'
        if self.canvas.clipper is None:
            text += '\n'
        else:
            text += self.canvas.clipper.get_data_text()

        text += '----- Отрезки -----\n'
        text += self.canvas.lines.get_data_text()

        self.data_scene_textEdit.setPlainText(text)

    def color_btns_clicked(self):
        self.purple_btn_line.clicked.connect(self.change_line_color_to_purple)
        self.black_btn_line.clicked.connect(self.change_line_color_to_black)
        self.yellow_btn_line.clicked.connect(self.change_line_color_to_yellow)
        self.red_btn_line.clicked.connect(self.change_line_color_to_red)
        self.blue_btn_line.clicked.connect(self.change_line_color_to_blue)
        self.green_btn_line.clicked.connect(self.change_line_color_to_green)

        self.purple_btn_clipper.clicked.connect(self.change_clipper_color_to_purple)
        self.black_btn_clipper.clicked.connect(self.change_clipper_color_to_black)
        self.yellow_btn_clipper.clicked.connect(self.change_clipper_color_to_yellow)
        self.red_btn_clipper.clicked.connect(self.change_clipper_color_to_red)
        self.blue_btn_clipper.clicked.connect(self.change_clipper_color_to_blue)
        self.green_btn_clipper.clicked.connect(self.change_clipper_color_to_green)

        self.purple_btn_res.clicked.connect(self.change_res_color_to_purple)
        self.black_btn_res.clicked.connect(self.change_res_color_to_black)
        self.yellow_btn_res.clicked.connect(self.change_res_color_to_yellow)
        self.red_btn_res.clicked.connect(self.change_res_color_to_red)
        self.blue_btn_res.clicked.connect(self.change_res_color_to_blue)
        self.green_btn_res.clicked.connect(self.change_res_color_to_green)

    def change_line_color(self, color):
        print(f'change_line_color to {color.getRgb()}')
        self.color_line_show.setStyleSheet(f"background-color: {color.name()}")
        self.line_color = color

    def change_line_color_to_purple(self):
        self.change_line_color(COLORS['purple'])

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

    def change_clipper_color(self, color):
        print(f'change_clipper_color to {color.getRgb()}')
        self.color_clipper_show.setStyleSheet(f"background-color: {color.name()}")
        self.clipper_color = color
        self.canvas.change_clipper_color(color)
        self.canvas.draw_clipper()

    def change_clipper_color_to_purple(self):
        self.change_clipper_color(COLORS['purple'])

    def change_clipper_color_to_black(self):
        self.change_clipper_color(COLORS['black'])

    def change_clipper_color_to_yellow(self):
        self.change_clipper_color(COLORS['yellow'])

    def change_clipper_color_to_red(self):
        self.change_clipper_color(COLORS['red'])

    def change_clipper_color_to_blue(self):
        self.change_clipper_color(COLORS['blue'])

    def change_clipper_color_to_green(self):
        self.change_clipper_color(COLORS['green'])

    def change_res_color(self, color):
        print(f'change_res_color to {color.getRgb()}')
        self.color_res_show.setStyleSheet(f"background-color: {color.name()}")
        self.res_color = color

    def change_res_color_to_purple(self):
        self.change_res_color(COLORS['purple'])

    def change_res_color_to_black(self):
        self.change_res_color(COLORS['black'])

    def change_res_color_to_yellow(self):
        self.change_res_color(COLORS['yellow'])

    def change_res_color_to_red(self):
        self.change_res_color(COLORS['red'])

    def change_res_color_to_blue(self):
        self.change_res_color(COLORS['blue'])

    def change_res_color_to_green(self):
        self.change_res_color(COLORS['green'])

    def clear_canvas(self):
        print('clear_canvas')
        self.canvas.clear_canvas()

    def show_info(self):
        print('show info')
        self.info_widget.show()

    # def resizeEvent(self, event):
    #     self.update()

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
