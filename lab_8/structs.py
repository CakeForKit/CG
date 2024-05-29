from PyQt5.QtGui import QPen, QColor
from PyQt5.QtGui import QPixmap
from errs import *


def draw_edges(qp, edges, color):
    # color = QColor(0, 0, 0)
    qp.setPen(QPen(color, 1))

    for i in range(len(edges)):
        qp.drawLine(edges[i][0].x, edges[i][0].y, edges[i][1].x, edges[i][1].y)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_xy(self):
        return self.x, self.y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Line:
    def __init__(self, p1: Point, p2: Point, color: QColor):
        self.p1 = p1
        self.p2 = p2
        self.color = color

    def draw(self, qp):
        qp.setPen(QPen(self.color, 1))
        qp.drawLine(*self.p1.get_xy(), *self.p2.get_xy())

    def get_data_text(self):
        return f'{self.p1} - {self.p2}'

    def __str__(self):
        return f'({self.p1}--{self.p2}, clr={self.color.getRgb()})'

    def __repr__(self):
        return f'Line{self}'


class Lines:
    def __init__(self):
        self.lines = list()

    def add_line(self, line: Line):
        self.lines.append(line)

    def clear(self):
        self.lines = []

    def draw(self, qp):
        for line in self.lines:
            line.draw(qp)

    def get_data_text(self):
        text = ''
        for line in self.lines:
            text += line.get_data_text() + '\n'
        return text

    def __str__(self):
        return f'{self.lines}'

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, i):
        return self.lines[i]


class Clipper:
    def __init__(self, color: QColor):
        self.color = color
        self.points = list()
        self.closed = False

    def get_data_text(self):
        text = ''
        id = 1
        for p in self.points:
            line = f'{id}) X = {p.x}, Y = {p.y}\n'
            text += line
            id += 1
        return text

    def add_point(self, p):
        if self.closed:
            raise AddPointToCloseFigureErr
        self.points.append(p)

    def add_point_draw(self, p, canvas):
        if self.closed:
            raise AddPointToCloseFigureErr

        if len(self.points) > 0:
            qp = canvas.qp
            qp.setPen(QPen(self.color, 1))
            qp.drawLine(self.points[-1].x, self.points[-1].y, p.x, p.y)

            canvas.import_img()
        self.points.append(p)

    def can_close(self):
        return len(self.points) >= 3

    def is_closed(self):
        return self.closed

    def is_point_in_clipper(self, p: Point):
        return p in self.points

    def draw(self, qp):
        edges = []
        for i in range(1, len(self.points)):
            edges.append([self.points[i - 1], self.points[i]])
        draw_edges(qp, edges, self.color)

        if self.closed:
            draw_edges(qp, [[self.points[0], self.points[-1]]], self.color)


    def close(self):
        if self.can_close():
            self.closed = True
        else:
            raise ErrCanNotCloseFigure

    def __getitem__(self, i):
        return self.points[i]

    def __len__(self):
        return len(self.points)

    def __str__(self):
        if self.closed:
            return f'Clipper(closed): {self.points}'
        else:
            return f'Clipper(not closed): {self.points}'

    def __repr__(self):
        return self.__str__()
