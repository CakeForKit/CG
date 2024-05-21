from PyQt5.QtGui import QImage, QPainter, QPixmap, QPen, QColor, QFont, qRgba
from PyQt5.QtWidgets import QApplication
from algos import line_by_line_filling_algorithm_with_seed
import time
DEBUG = True

from structs import *
from figure import *


class Canvas:
    def __init__(self, label, background_color):    # colour, line_colour,
        self.label = label
        self.width = label.size().width()
        self.height = label.size().height()
        # self.line_colour = line_colour
        # self.colour = colour
        self.background_color = background_color
        self.img = QImage(self.width, self.height, QImage.Format_ARGB32)

        self.figures = list()
        # self.figures_filled = list()

        self.update()

    def update(self):
        print(f'update canvas: {self}')

    # def repaint_canvas(self, brush_colour):
    #     print('repaint_canvas')
    #     self.update_img_elem()
    #     self.draw_background()
    #     self.draw_ruler()
    #     self.redraw_all_figures()
    #     self.fill_all_figures(brush_colour, False)

    def draw_figure(self, fig):
        fig.draw(self)

    def redraw_all_figures(self):
        for fig in self.figures:
            self.draw_figure(fig)

    # def fill_new_figures(self):
    #     self.figures_filled = self.figures[:]

    def fill_all_figures(self, brush_colour, line_colour, seed_point, delay):
        time_alg = -1
        # if len(self.figures) > 0:
        time_start = time.time()
        line_by_line_filling_algorithm_with_seed(self, line_colour, brush_colour, seed_point, delay)
        time_end = time.time()

        if not delay:
            time_alg = time_end - time_start
        # self.redraw_all_figures()
        return time_alg

    def add_figure(self, fig):
        self.figures.append(fig)
        self.draw_figure(fig)

    def get_text_figures_data(self):
        text = ''
        for i, f in enumerate(self.figures):
            text += f'{" " * 6}Figure {i + 1}{" " * 6}\n'
            text += f.get_text_points()
            text += '\n'
        return text

    def update_img_elem(self):
        print(f'update_img_elem ({self.width}, {self.height})')
        self.width = self.label.size().width()
        self.height = self.label.size().height()
        self.img = QImage(self.width, self.height, QImage.Format_RGB32)

    def import_img(self):
        pmp = QPixmap.fromImage(self.img)
        self.label.setPixmap(pmp)
        QApplication.processEvents()

    def draw_seed_point(self, x, y, color: QColor):
        # light = 100
        # color_light = QColor(*list(map(lambda x: x + light if x + light <= 255 else 255, color.getRgb()[:-1])))
        # for yi in range(y - 1, y + 2):
        #     for xi in range(x - 1, x + 2):
        #         if self.x_in_canvas(xi) and self.y_in_canvas(yi):
        #             self.set_pixel_color(xi, yi, color_light)

        self.set_pixel_color(x, y, color)
        # print(f'draw_seed_point: {color.getRgb()} --> {color_light.getRgb()}')



    def set_pixel_color(self, x, y, color: QColor):
        self.img.setPixelColor(x, y, color)

    def get_pixel_color(self,x, y):
        return self.img.pixelColor(x, y)

    def x_in_canvas(self, x):
        return 0 <= x <= self.width

    def y_in_canvas(self, y):
        return 0 <= y <= self.height

    def draw_background(self):
        self.img.fill(self.background_color)

    def draw_ruler(self, step=100, pen=QPen(QColor(0, 0, 0), 1), font=QFont('MS Shell Dlg 2', 14)):
        print(f'draw_ruler')
        if self.background_color.name() == QColor(0, 0, 0).name():
            pen.setColor(QColor(255, 255, 255))
        else:
            pen.setColor(QColor(0, 0, 0))
        # OX
        qp = QPainter(self.img)
        qp.setPen(pen)
        qp.setFont(font)

        lenline = min(self.width, self.height) // 30
        for x in range(0, self.width, step):
            qp.drawLine(x, 0, x, lenline)
            qp.drawText(x, lenline, f'{x}')

        for y in range(0, self.height, step):
            qp.drawLine(0, y, lenline, y)
            qp.drawText(0, y, f'{y}')

    def clear_canvas(self):
        self.figures = []
        # self.figures_filled = list()
        self.update_img_elem()
        self.draw_background()
        self.draw_ruler()

    def __str__(self):
        figs = ''
        for f in self.figures:
            figs += str(f) + '\n\t'
        return f"Canvas({self.width}, {self.height}, " \
               f"background={self.background_color.name()})\n" \
               f"figures={figs}"

