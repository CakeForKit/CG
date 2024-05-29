from PyQt5.QtGui import QImage, QPainter, QPixmap, QPen, QColor, QFont, qRgba
from PyQt5.QtWidgets import QApplication
import time
DEBUG = True

from structs import *


class Canvas:
    def __init__(self, label, clipper_color, background_color):    # colour, line_colour,
        self.label = label
        self.width = label.size().width()
        self.height = label.size().height()
        self.background_color = background_color
        self.img = QImage(self.width, self.height, QImage.Format_ARGB32)
        self.qp = QPainter(self.img)

        self.lines = Lines()
        self.clipper = Clipper(clipper_color)
        self.clear_canvas()

    def redraw(self):
        self.update_img_elem()
        self.draw_background()
        self.draw_ruler()
        self.draw_all_lines(False)
        self.draw_clipper(False)
        self.import_img()

    def draw_all_lines(self, import_img=True):
        # qp = QPainter(self.img)
        self.lines.draw(self.qp)
        if import_img:
            self.import_img()

    def draw_line(self, line, import_img=True):
        # qp = QPainter(self.img)
        line.draw(self.qp)
        if import_img:
            self.import_img()

    def add_draw_line(self, p1: Point, p2: Point, color: QColor):
        line = Line(p1, p2, color)
        self.lines.add_line(line)
        print(f'add_draw_line: lines: {self.lines}')
        self.draw_line(line)

    def add_point_clipper(self, p: Point):
        self.clipper.add_point(p)

    def change_clipper_color(self, color: QColor):
        self.clipper.color = color

    def draw_clipper(self, import_img=True):
        self.clipper.draw(self.qp)
        if import_img:
            self.import_img()

    def update_img_elem(self):
        # print(f'update_img_elem ({self.width}, {self.height})')
        self.width = self.label.size().width()
        self.height = self.label.size().height()
        self.qp.end()
        self.img = QImage(self.width, self.height, QImage.Format_RGB32)
        self.qp = QPainter(self.img)


    def import_img(self):
        pmp = QPixmap.fromImage(self.img)
        self.label.setPixmap(pmp)
        QApplication.processEvents()

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
        # print(f'draw_ruler')
        if self.background_color.name() == QColor(0, 0, 0).name():
            pen.setColor(QColor(255, 255, 255))
        else:
            pen.setColor(QColor(0, 0, 0))
        # OX
        # qp = QPainter(self.img)
        self.qp.setPen(pen)
        self.qp.setFont(font)

        lenline = min(self.width, self.height) // 30
        for x in range(0, self.width, step):
            self.qp.drawLine(x, 0, x, lenline)
            self.qp.drawText(x, lenline, f'{x}')

        for y in range(0, self.height, step):
            self.qp.drawLine(0, y, lenline, y)
            self.qp.drawText(0, y, f'{y}')

    def clear_canvas(self):
        self.update_img_elem()
        self.draw_background()
        self.draw_ruler()
        self.import_img()

        self.lines = Lines()
        self.clipper = Clipper(self.clipper.color)

    def __str__(self):
        return f"Canvas({self.width}, {self.height}, " \
               f"background={self.background_color.name()})\n"

