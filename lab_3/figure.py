from Point import Point, rotate
import math as m


class FigureLine:
    def __init__(self, p1: Point, p2: Point, algorithm, color):
        self.p1 = p1
        self.p2 = p2
        self.algorithm = algorithm
        self.color = color
        self.points = self.get_points_to_draw()

        # print(self)

    def get_points_to_draw(self):
        return self.algorithm(self.p1, self.p2)

    def __str__(self):
        return f'FigureLine({self.p1}, {self.p2}, {self.algorithm.__name__}, color={self.color.name()})'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2


class FigureSpec:
    def __init__(self, lenline, angle, center, algorithm, color):
        self.lenline = lenline
        self.angle = angle
        self.center = center
        self.algorithm = algorithm
        self.color = color
        self.need_lines = []
        self.points = self.get_points_to_draw()

    def get_need_lines(self, printing=False):
        if printing: print('\nget_need_lines:')
        need_lines = list()
        grad_angle = 0
        while grad_angle < 360:
            x = self.lenline * m.cos(m.radians(grad_angle)) + self.center.x
            y = self.lenline * m.sin(-m.radians(grad_angle)) + self.center.y
            p = Point(round(x), round(y))
            if printing: print(f'grad={grad_angle} {p}')

            line = FigureLine(self.center, p, self.algorithm, self.color)
            need_lines.append(line)

            grad_angle += self.angle % 360

        return need_lines

    def get_points_to_draw(self):
        self.need_lines = self.get_need_lines()
        # print(f'get_points_to_draw: need_lines={self.need_lines}')
        points = list()
        for line in self.need_lines:
            points.extend(line.points)
        return points

    # def get_points_to_draw(self):
    #     points = list()
    #     grad_angle = 0
    #     while grad_angle < 360:
    #         x = self.lenline * m.cos(m.radians(grad_angle)) + self.center.x
    #         y = self.lenline * m.sin(-m.radians(grad_angle)) + self.center.y
    #         p = Point(round(x), round(y))
    #
    #         pts = FigureLine(self.center, p, self.algorithm, self.color).points
    #         points.extend(pts)
    #
    #         grad_angle += self.angle % 360
    #     return points

    def __str__(self):
        return f'FigureSpec(len={self.lenline}, angle={self.angle}, {self.algorithm.__name__}, color={self.color.name()})'

    def __repr__(self):
        return self.__str__()
