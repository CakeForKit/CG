from PyQt5.QtGui import QImage, QPainter, QPen, QColor
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QLabel

from figure import *
from structs import *
from canvas import Canvas
from algos import *

DEBUG = False
TEST = 2




if __name__ == '__main__':
    DEBUG = True
    lbl = QLabel()
    width, height = 2000, 2000
    canvas = Canvas(lbl, QColor(0, 0, 0), QColor(0, 0, 0))

    # треугольник
    if TEST == 1:
        ps = [Point(10, 10), Point(5, 15), Point(20, 30)]
        fig = OpenFigure()
        for p in ps:
            fig.add_point(p)
        fig = Figure(fig)
        alg_fill_solid_areas_ordered_list_CAP(canvas, [fig])

    # ребра вертикальные, горизонтальные и под маленьким углом
    elif TEST == 2:
        ps = [Point(10, 10), Point(15, 15), Point(10, 15), Point(30, 14), Point(30, 15)]
        fig = OpenFigure()
        for p in ps:
            fig.add_point(p)
        fig = Figure(fig)
        alg_fill_solid_areas_ordered_list_CAP(canvas, [fig])

