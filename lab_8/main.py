import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from info import InfoWidget
from canvas import Canvas
from structs import *
from random import randint
from algos import cut_lines_cyrus_beck, get_parallel_line, is_polygon_convexity
from errs import Errors_my, BaseErr

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
        self.canvas = Canvas(self.canvas_lbl, self.clipper_color, self.background_color)

        self.change_clipper_color(self.clipper_color)
        self.change_line_color(self.line_color)
        self.change_res_color(self.res_color)

        self.color_btns_clicked()
        self.clear_canvas_btn.clicked.connect(self.clear_canvas)
        self.add_point_clipper_btn.clicked.connect(self.add_point_clipper_by_btn)
        self.close_clipper_btn.clicked.connect(self.close_clipper)
        self.draw_line_btn.clicked.connect(self.draw_line_by_btn)
        self.draw_parallel_lines_btn.clicked.connect(self.draw_parallel_lines)
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
        elif event.button() == Qt.RightButton:
            p = Point(event.x(), event.y())
            if self.is_in_label(p):
                event.accept()
                self.add_point_clipper(*p.get_xy())
        elif event.buttons() == Qt.MiddleButton:
            self.close_clipper()

    def cut_lines(self):
        if self.canvas.clipper.is_closed():
            if not is_polygon_convexity(self.canvas.clipper):
                errm = Errors_my(ConvexityErr.text())
                errm.show()
                return
            cut_lines_cyrus_beck(self.canvas.qp, self.canvas.lines, self.res_color, self.canvas.clipper)
            self.canvas.import_img()
        else:
            errm = Errors_my(CloseClipperErr.text())
            errm.show()
            return

    def add_point_clipper_by_btn(self):
        x = self.clipper_x_sp.value()
        y = self.clipper_y_sp.value()
        self.add_point_clipper(x, y)

    def add_point_clipper(self, x, y):
        if self.canvas.clipper.is_closed():
            self.canvas.clipper = Clipper(self.clipper_color)
            self.canvas.redraw()

        p = Point(x, y)
        if self.canvas.clipper.is_point_in_clipper(p):
            errm = Errors_my(ErrPointExistInFigure.text())
            errm.show()
            return
        self.canvas.clipper.add_point(p)
        self.canvas.draw_clipper()
        self.show_data_scene()

    def close_clipper(self):
        if not self.canvas.clipper.is_closed():
            if self.canvas.clipper.can_close():
                self.canvas.clipper.close()
                self.canvas.draw_clipper()
                self.show_data_scene()
            else:
                errm = Errors_my(ErrCanNotCloseFigure.text())
                errm.show()
                return

    def draw_line_by_btn(self):
        x1 = self.line_x1_sp.value()
        y1 = self.line_y1_sp.value()
        x2 = self.line_x2_sp.value()
        y2 = self.line_y2_sp.value()
        self.add_draw_line(Point(x1, y1), Point(x2, y2))

    def add_draw_line(self, p1: Point, p2: Point):
        self.canvas.add_draw_line(p1, p2, self.line_color)
        self.show_data_scene()

    def show_data_scene(self):
        text = ''

        text += '----- Отсекатель -----\n'
        if self.canvas.clipper.is_closed():
            text += 'замкнут\n'
        else:
            text += 'не замкнут\n'
        text += self.canvas.clipper.get_data_text()

        text += '----- Отрезки -----\n'
        text += self.canvas.lines.get_data_text()

        self.data_scene_textEdit.setPlainText(text)

    def draw_parallel_lines(self):
        if self.canvas.clipper.is_closed():
            dy = 300
            points = self.canvas.clipper.points

            for i in range(-1, len(points) - 1):
                print(i, points)
                clipper_line = Line(points[i], points[i + 1], self.line_color)

                dy = max((clipper_line.p1.y - clipper_line.p2.y) // 2, 30)
                for mul in [1, -1]:
                    line = get_parallel_line(clipper_line, mul * dy)
                    print(line)
                    self.add_draw_line(line.p1, line.p2)
        else:
            points = self.canvas.clipper.points

            for i in range(0, len(points) - 1):
                print(i, points)
                clipper_line = Line(points[i], points[i + 1], self.line_color)

                dy = max((clipper_line.p1.y - clipper_line.p2.y) // 2, 30)
                for mul in [1, -1]:
                    line = get_parallel_line(clipper_line, mul * dy)
                    print(line)
                    self.add_draw_line(line.p1, line.p2)




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
        self.show_data_scene()

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
