from PyQt5.QtGui import QPen, QColor
from PyQt5.QtGui import QPixmap
from errs import *
from Point import *
from Figure import *


# class Line:
#     def __init__(self, p1: Point, p2: Point, color: QColor):
#         self.p1 = p1
#         self.p2 = p2
#         self.color = color
#
#     def draw(self, qp):
#         qp.setPen(QPen(self.color, 1))
#         qp.drawLine(*self.p1.get_xy(), *self.p2.get_xy())
#
#     def get_data_text(self):
#         return f'{self.p1} - {self.p2}'
#
#     def __str__(self):
#         return f'({self.p1}--{self.p2}, clr={self.color.getRgb()})'
#
#     def __repr__(self):
#         return f'Line{self}'
#
#
# class Lines:
#     def __init__(self):
#         self.lines = list()
#
#     def add_line(self, line: Line):
#         self.lines.append(line)
#
#     def clear(self):
#         self.lines = []
#
#     def draw(self, qp):
#         for line in self.lines:
#             line.draw(qp)
#
#     def get_data_text(self):
#         text = ''
#         for line in self.lines:
#             text += line.get_data_text() + '\n'
#         return text
#
#     def __str__(self):
#         return f'{self.lines}'
#
#     def __len__(self):
#         return len(self.lines)
#
#     def __getitem__(self, i):
#         return self.lines[i]


class Clipper(Figure):
    def __init__(self, color: QColor):
        super().__init__(color)

    def is_point_in_clipper(self, p: Point):
        return p in self.points

    def __str__(self):
        if self.closed:
            return f'Clipper(closed): {self.points}'
        else:
            return f'Clipper(not closed): {self.points}'

