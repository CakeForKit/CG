from errs import *

from PyQt5.QtGui import QPainter, QPen, QColor

from PyQt5.QtGui import QPixmap

def draw_edges(canvas, edges, colour):
    # colour = QColor(0, 0, 0)
    qp = QPainter(canvas)
    qp.setPen(QPen(colour, 1))

    for i in range(len(edges)):
        qp.drawLine(edges[i][0].x, edges[i][0].y, edges[i][1].x, edges[i][1].y)


class OpenFigure:
    def __init__(self, line_colour):
        self.points = list()
        self.line_colour = line_colour

    def get_text_points(self):
        text = ''
        id = 1
        for p in self.points:
            line = f'{id}) X = {p.x}, Y = {p.y}\n'
            text += line
            id += 1
        return text

    def add_point(self, p):
        self.points.append(p)

    def add_point_draw(self, p, canvas):
        if len(self.points) > 0:
            qp = QPainter(canvas.img)
            qp.setPen(QPen(self.line_colour, 1))
            qp.drawLine(self.points[-1].x, self.points[-1].y, p.x, p.y)

            canvas.import_img()
        self.points.append(p)

    def can_close(self):
        return len(self.points) >= 3

    def draw(self, canvas):
        edges = []
        for i in range(1, len(self.points)):
            edges.append([self.points[i - 1], self.points[i]])
        draw_edges(canvas.img, edges, self.line_colour)

        canvas.import_img()

    def __getitem__(self, i):
        return self.points[i]

    def __len__(self):
        return len(self.points)

    def __str__(self):
        return f'OpenFigure: {self.points}'

    def __repr__(self):
        return self.__str__()


class Figure(OpenFigure):
    def __init__(self, openfigure: OpenFigure, line_colour):
        super().__init__(openfigure.line_colour)
        self.points = openfigure.points[:]
        self.line_colour = line_colour
        pass

    def draw(self, canvas):
        super().draw(canvas)
        draw_edges(canvas.img, [[self.points[0], self.points[-1]]], self.line_colour)

        pmp = QPixmap.fromImage(canvas.img)
        canvas.label.setPixmap(pmp)

    def get_text_points(self):
        text = super().get_text_points()
        return text

    def add_point(self, p):
        raise AddPointToCloseFigureErr

    def __str__(self):
        return f'Figure: {self.points}'

    def __repr__(self):
        return self.__str__()
