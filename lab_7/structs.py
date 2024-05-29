from PyQt5.QtGui import QColor, QPen


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
    def __init__(self, p1: Point, p2: Point, color:QColor):
        self.x_left, self.x_right = sorted([p1.x, p2.x])
        self.y_top, self.y_bottom = sorted([p1.y, p2.y])
        self.color = color

    def width(self):
        return self.x_right - self.x_left

    def height(self):
        return self.y_bottom - self.y_top

    def draw(self, qp):
        qp.setPen(QPen(self.color, 1))
        qp.drawRect(self.x_left, self.y_top, self.width(), self.height())

    def get_data_text(self):
        return f'x_left=    {self.x_left}\n' \
               f'x_right=   {self.x_right}\n' \
               f'y_top=     {self.y_top}\n' \
               f'y_bottom=  {self.y_bottom}\n'

    def __str__(self):
        return f'Clipper(xl={self.x_left}, xr={self.x_right}, yb={self.y_bottom}, yt={self.y_top})'
