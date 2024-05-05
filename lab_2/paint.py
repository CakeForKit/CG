from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QFont, QBrush, QFontMetrics
from PyQt5.QtCore import Qt, QPoint
import math as m
from geometry import *


SHOW_JUST_FIGURE = False
MAX_COORD_X = 5
MIN_COORD_X = -MAX_COORD_X
A, B, C, R = 1, 1, 1, 1

DEBUG = True


class CanvasWidget(QWidget):
    def __init__(self, parant):
        super().__init__()
        self.parant = parant
        self.window_width = self.width()
        self.window_height = self.height()

        self.parant.figure_params_le.setText(f'A = {A} B = {B} C = {C} R = {R}')
        self.grid_step = 0.5
        self.scale_figure_points = 100
        self.text_height = 25

        self.center = (1, 1)
        self.center_figure = (1, 1)
        self.circle = list()
        self.hyperbole = list()
        self.figure = list()
        self.set_start_circle_points()
        self.set_start_hyperbole_points()

        self.steps_back_data = list() # [[func, list_args_to_func] ...]

    def shift(self, dx, dy):
        self.center_figure = shift(dx, dy, [self.center_figure])[0]
        # print(self.center_figure)
        self.figure = shift(dx, dy, self.figure)
        self.circle = shift(dx, dy, self.circle)
        self.hyperbole = shift(dx, dy, self.hyperbole)
        self.steps_back_data.append([self.shift, [-dx, -dy]])

        self.update()
        
    def rotate(self, cx, cy, angle):
        self.center_figure = rotate(cx, cy, angle, [self.center_figure])[0]
        self.figure = rotate(cx, cy, angle, self.figure)
        self.circle = rotate(cx, cy, angle, self.circle)
        self.hyperbole = rotate(cx, cy, angle, self.hyperbole)
        self.steps_back_data.append([self.rotate, [cx, cy, -angle]])

        self.update()

    def scaling(self, cx, cy, kx, ky):
        self.center_figure = scaling(cx, cy, kx, ky, [self.center_figure])[0]
        self.figure = scaling(cx, cy, kx, ky, self.figure)
        self.circle = scaling(cx, cy, kx, ky, self.circle)
        self.hyperbole = scaling(cx, cy, kx, ky, self.hyperbole)
        self.steps_back_data.append([self.scaling, [cx, cy, 1 / kx, 1 / ky]])

        self.update()

    def step_back(self):
        if len(self.steps_back_data) > 0:
            func, args = self.steps_back_data[-1]
            func(*args)
            del self.steps_back_data[-1]
            del self.steps_back_data[-1]
            self.update()

    def translate_to_computer_system(self, x, y, debug=False):
        save_x, save_y = x, y
        # to positive
        x += -MIN_COORD_X
        max_coord_y = (MAX_COORD_X - MIN_COORD_X) * self.window_height / self.window_width / 2
        min_coord_y = -max_coord_y
        y += -min_coord_y
        # scale
        scale_x = self.window_width / (MAX_COORD_X - MIN_COORD_X)
        scale_y = self.window_height / (max_coord_y - min_coord_y)
        x = round(x * scale_x)
        y = round(y * scale_y)
        # reverse y
        y = self.window_height - y

        if debug:
            print(f'translate_to_computer_system: {(save_x, save_y)} -> {(x, y)}')
        # if x < 0 or y < 0:
        #     raise Exception('my error: translate_to_computer_system')

        return x, y

    def set_pen(self, qp, width=1, color=Qt.black):
        pen = QPen()
        pen.setWidth(width)
        pen.setColor(color)
        qp.setPen(pen)

    def draw_axis_and_grid(self, qp, debug=DEBUG):
        qp.setPen(QPen(Qt.black, 2))
        # self.set_pen(qp, 2, Qt.black)
        font = QFont()
        font.setPixelSize(self.text_height)
        qp.setFont(font)

        # axis
        center_x, center_y = self.translate_to_computer_system(0, 0)
        qp.drawLine(0, center_y, self.window_width, center_y)
        qp.drawLine(center_x, 0, center_x, self.window_height)
        dx, dy = -QFontMetrics(font).width('0') - 3, self.text_height + 1
        qp.drawText(center_x + dx, center_y + dy, '0')

        # grid
        self.set_pen(qp, 1, Qt.black)
        x = self.grid_step
        end_field = False
        while not end_field:
            cs_x = self.translate_to_computer_system(x, 0)[0]
            minus_cs_x = self.translate_to_computer_system(-x, 0)[0]
            if 0 <= cs_x <= self.window_width:
                qp.drawLine(cs_x, 0, cs_x, self.window_height)
                dx, dy = -QFontMetrics(font).width(str(x)) - 3, self.text_height + 1
                qp.drawText(cs_x + dx, center_y + dy, str(x))

                qp.drawLine(minus_cs_x, 0, minus_cs_x, self.window_height)
                dx, dy = -QFontMetrics(font).width(str(-x)) - 3, self.text_height + 1
                qp.drawText(minus_cs_x + dx, center_y + dy, str(-x))

                x += self.grid_step
            else:
                end_field = True

        y = self.grid_step
        end_field = False
        while not end_field:
            cs_y = self.translate_to_computer_system(0, y)[1]
            minus_cs_y = self.translate_to_computer_system(0, -y)[1]
            if 0 <= cs_y <= self.window_height:
                qp.drawLine(0, cs_y, self.window_width, cs_y)
                dx, dy = -QFontMetrics(font).width(str(y)) - 3, self.text_height + 1
                qp.drawText(center_x + dx, cs_y + dy, str(y))

                qp.drawLine(0, minus_cs_y, self.window_width, minus_cs_y)
                dx, dy = -QFontMetrics(font).width(str(-y)) - 3, self.text_height + 1
                qp.drawText(center_x + dx, minus_cs_y + dy, str(-y))

                y += self.grid_step
            else:
                end_field = True

    def reset(self):
        print('RESET')
        self.set_start_circle_points()
        self.set_start_hyperbole_points()
        self.set_start_figure_points()
        self.steps_back_data = list()
        self.update()

    def set_start_circle_points(self):
        self.circle = build_start_circle(A, B, R, self.scale_figure_points)

    def set_start_hyperbole_points(self):
        self.hyperbole = build_start_hyperbole(C, self.scale_figure_points, MAX_COORD_X)

    def set_start_figure_points(self):
        if len(self.circle) == 0:
            self.set_start_circle_points()
        if len(self.hyperbole) == 0:
            self.set_start_hyperbole_points()
        self.figure = get_start_filling_figure(self.hyperbole, self.circle, A, B, R, C)
        self.center_figure = (1.0, 1.0)

    def paint_circle(self, qp):
        if len(self.circle) == 0:
            self.set_start_circle_points()
        circle_points = list(map(lambda x: QPoint(*self.translate_to_computer_system(*x)), self.circle))
        qp.drawPolyline(*circle_points, circle_points[0])

    def paint_hyperbole(self, qp):
        if len(self.hyperbole) == 0:
            self.set_start_hyperbole_points()
        hyperbole_points = list(map(lambda x: QPoint(*self.translate_to_computer_system(*x)), self.hyperbole))
        qp.drawPolyline(*hyperbole_points)

    def paint_full_figure(self, qp):
        if len(self.figure) == 0:
            self.set_start_figure_points()
        if len(self.figure) != 0:
            figure_points = list(map(lambda x: QPoint(*self.translate_to_computer_system(*x)), self.figure))
            qp.setBrush(QBrush(Qt.red, Qt.CrossPattern))
            qp.drawPolygon(*figure_points)

    def draw_center(self, qp, x, y):
        center_coord = (x, y)
        # center_coord = (self.parant.cx_dsp.value(), self.parant.cy_dsp.value())
        self.center = self.translate_to_computer_system(*center_coord)
        self.set_pen(qp, width=9, color=Qt.red)
        qp.drawPoint(self.center[0], self.center[1])

        self.set_pen(qp, width=3, color=Qt.black)
        font = QFont()
        font.setPixelSize(self.text_height)
        qp.setFont(font)
        dx, dy = -QFontMetrics(font).width('0') - 3, self.text_height + 1
        qp.drawText(self.center[0] + dx, self.center[1] + dy, f'({center_coord[0]:.2f}, {center_coord[1]:.2f})')

    def paintEvent(self, event):
        self.window_width = self.width()
        self.window_height = self.height()
        # if DEBUG:
        #     print(f'(self.window_width, self.window_height) = {(self.window_width, self.window_height)}')

        qp = QPainter(self)
        qp.begin(self)

        # делаем белый фон
        qp.setBrush(Qt.white)
        qp.drawRect(self.rect())
        #

        # рисуем сетку
        self.draw_axis_and_grid(qp, debug=False)

        # центр вращения
        center = self.parant.cx_dsp.value(), self.parant.cy_dsp.value()
        self.draw_center(qp, *center)

        # центр фигуры
        self.draw_center(qp, *self.center_figure)
        # self.set_pen(qp, width=9, color=Qt.black)
        # qp.drawPoint(*self.translate_to_computer_system(*self.center_figure))

        # start figures
        self.set_pen(qp, width=3, color=Qt.blue)
        if not SHOW_JUST_FIGURE:
            self.paint_circle(qp)
            self.paint_hyperbole(qp)
        self.paint_full_figure(qp)


        qp.end()