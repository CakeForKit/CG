from PyQt5.QtGui import QImage, QPainter, QPixmap, QPen, QColor, QFont, qRgba
from PyQt5.QtWidgets import QApplication
from algos import alg_fill_solid_areas_ordered_list_CAP
import time
DEBUG = True

from structs import *
from figure import *


class Canvas:
    def __init__(self, label, colour, background_color):
        self.label = label
        self.width = label.size().width()
        self.height = label.size().height()
        self.colour = colour
        self.background_color = background_color
        self.img = QImage(self.width, self.height, QImage.Format_ARGB32)

        self.figures = list()
        self.figures_filled = list()

        self.update()

    def update(self):
        print(f'update canvas: {self}')
        self.update_img_elem()
        self.draw_background()
        self.draw_ruler()
        self.redraw_all_figures()
        self.fill_all_figures(False)


    def draw_figure(self, fig):
        fig.draw(self)

    def redraw_all_figures(self):
        for fig in self.figures:
            self.draw_figure(fig)

    def fill_new_figures(self):
        # self.figures_filled = list()
        # self.update()
        self.figures_filled = self.figures[:]

    def fill_all_figures(self, delay):
        time_alg = -1
        if len(self.figures_filled) > 0:
            time_start = time.time()
            alg_fill_solid_areas_ordered_list_CAP(self, self.figures_filled, self.colour, delay)
            time_end = time.time()

            if not delay:
                time_alg = time_end - time_start
        self.redraw_all_figures()
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
        self.width = self.label.size().width()
        self.height = self.label.size().height()
        self.img = QImage(self.width, self.height, QImage.Format_RGB32)

    # def set_background_color(self, color):
    #     print(f'set_background_color: {color.name()}')
    #     self.background_color = color
    #     self.update()

    def draw_background(self):
        self.img.fill(self.background_color)

    def draw_ruler(self, step=100, pen=QPen(QColor(0, 0, 0), 1), font=QFont('MS Shell Dlg 2', 14)):
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
        self.figures_filled = list()

    def __str__(self):
        figs = ''
        for f in self.figures:
            figs += str(f) + '\n\t'
        return f"Canvas({self.width}, {self.height}, " \
               f"background={self.background_color.name()})\n" \
               f"figures={figs}"

