from PyQt5.QtGui import QImage, QPainter, QPixmap, QPen, QColor, QFont, qRgba
from PyQt5.QtWidgets import QSizePolicy

from algos import lib, INTENSE_MAX
from figure import FigureLine, FigureSpec
from Point import Point


DEBUG = True


class Canvas:
    def __init__(self, label, background_color):
        self.label = label
        self.width = label.size().width()
        self.height = label.size().height()
        self.background_color = background_color
        self.img = QImage(self.width, self.height, QImage.Format_ARGB32)

        self.figures = list()

        self.update()

    def update(self):
        print(f'update canvas: {self}')
        self.update_img_elem()
        self.draw_background()
        self.draw_ruler()
        self.redraw_all_figures()
        # self.tmp()

    def tmp(self):
        rb, gb, bb = self.background_color.red(), self.background_color.green(), self.background_color.blue()
        rl, gl, bl = 0, 0, 0
        intense = 50
        rn = int(rl + (rb - rl) * (1 - intense / INTENSE_MAX))
        gn = int(gl + (gb - gl) * (1 - intense / INTENSE_MAX))
        bn = int(bl + (bb - bl) * (1 - intense / INTENSE_MAX))
        color = QColor(rn, gn, bn)
        for i in range(100, 610):
            # color.setAlpha(m)
            # m += 2
            for j in range(100, 300):
                self.img.setPixelColor(i, j, color)
                # print(self.img.pixelColor(i, j).alpha())

    def draw_figure(self, fig):
        # print(f'draw_figure - {fig}:')
        if fig.algorithm == lib:
            qp = QPainter(self.img)
            qp.setPen(QPen(fig.color, 1))
            if fig.__class__ == FigureLine:
                qp.drawLine(fig.p1.x, fig.p1.y, fig.p2.x, fig.p2.y)
            else:
                # print(f'need_lines = {fig.need_lines}')
                for line in fig.need_lines:
                    qp.drawLine(line.p1.x, line.p1.y, line.p2.x, line.p2.y)
        else:
            for p in fig.points:
                color = p.pixel_color(fig.color, self.background_color)
                self.img.setPixelColor(p.x, p.y, color)
            # if fig.__class__ == FigureSpec:
            #     print(f'need_lines = {fig.need_lines}')

    def redraw_all_figures(self):
        for fig in self.figures:
            self.draw_figure(fig)
        print(self.figures)
        # if len(self.figures) >= 2:
        #     for i in range(len(self.figures[0].points)):
        #         if self.figures[0].points[i] != self.figures[1].points[i]:
        #             print(self.figures[0].points[i], self.figures[1].points[i])

    def add_figure(self, fig):
        self.figures.append(fig)
        self.draw_figure(fig)

    def update_img_elem(self):
        self.width = self.label.size().width()
        self.height = self.label.size().height()
        self.img = QImage(self.width, self.height, QImage.Format_RGB32)

    def set_background_color(self, color):
        print(f'set_background_color: {color.name()}')
        self.background_color = color
        self.update()

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

    def __str__(self):
        figs = ''
        for f in self.figures:
            figs += str(f) + '\n\t'
        return f"Canvas({self.width}, {self.height}, " \
               f"background={self.background_color.name()})\n" \
               f"figures={figs}"

    # def set_pixel(self):
    #     self.img.setPixel()
