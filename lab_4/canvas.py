from PyQt5.QtGui import QImage, QPainter, QPixmap, QPen, QColor, QFont, qRgba
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QSizePolicy

from algos import lib
from figure import FigureCircle, FigureCircleSpec, FigureEllipse, FigureEllipseSpec
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

    def draw_figure(self, fig):
        # print(f'draw_figure - {fig}:')
        if fig.algorithm == lib:
            qp = QPainter(self.img)
            qp.setPen(QPen(fig.color, 1))
            if fig.__class__ == FigureCircle:
                qp.drawEllipse(QPoint(fig.center.x, fig.center.y), fig.r, fig.r)
            elif fig.__class__ == FigureEllipse:
                qp.drawEllipse(QPoint(fig.center.x, fig.center.y), fig.ra, fig.rb)
            elif fig.__class__ == FigureCircleSpec:
                # print(f'need_lines = {fig.need_lines}')
                for circle in fig.need_circles:
                    qp.drawEllipse(QPoint(circle.center.x, circle.center.y), circle.r, circle.r)
            else:
                for ellipse in fig.need_ellipse:
                    qp.drawEllipse(QPoint(ellipse.center.x, ellipse.center.y), ellipse.ra, ellipse.rb)
        else:
            for p in fig.points:
                color = fig.color
                self.img.setPixelColor(p.x, p.y, color)
            # if fig.__class__ == FigureSpec:
            #     print(f'need_lines = {fig.need_lines}')

    def redraw_all_figures(self):
        for fig in self.figures:
            self.draw_figure(fig)
        # print(self.figures)

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

