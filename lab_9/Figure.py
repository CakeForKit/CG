from PyQt5.QtGui import QColor, QPen
from errs import *
from Point import *

def draw_edges(qp, edges, color):
    # color = QColor(0, 0, 0)
    qp.setPen(QPen(color, 1))

    for i in range(len(edges)):
        qp.drawLine(edges[i][0].x, edges[i][0].y, edges[i][1].x, edges[i][1].y)


class Figure:
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

    def is_point_in_figure(self, p: Point):
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
            self.points.append(Point(*self.points[0].get_xy()))
        else:
            raise ErrCanNotCloseFigure

    def get_list_of_lists(self):
        res = list()
        for p in self.points:
            res.append(list(p.get_xy()))

        return res

    def reverse(self):
        self.points.reverse()

    def __getitem__(self, i):
        return self.points[i]

    def __len__(self):
        return len(self.points)

    def __str__(self):
        if self.closed:
            return f'Figure(closed): {self.points}'
        else:
            return f'Figure(not closed): {self.points}'

    def __repr__(self):
        return self.__str__()
    
    