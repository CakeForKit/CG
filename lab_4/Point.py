from math import cos, sin
from PyQt5.QtGui import QColor

INTENSE_MAX = 100


def rotate(p, angle_rad, center):
    x = p.x
    new_x = round(center.x + (x - center.x) * cos(angle_rad) + (p.y - center.y) * sin(angle_rad))
    new_y = round(center.y - (x - center.x) * sin(angle_rad) + (p.y - center.y) * cos(angle_rad))
    return Point(new_x, new_y)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Pixel(Point):
    def __init__(self, x, y, intensity=INTENSE_MAX):
        super().__init__(x, y)
        self.intensity = intensity

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'Pixel({self.x}, {self.y}, {self.intensity})'

    def pixel_color(self, self_color, back_color):
        rb, gb, bb = back_color.red(), back_color.green(), back_color.blue()
        rl, gl, bl = self_color.red(), self_color.green(), self_color.blue()
        rn = int(rl + (rb - rl) * (1 - self.intensity / INTENSE_MAX))
        gn = int(gl + (gb - gl) * (1 - self.intensity / INTENSE_MAX))
        bn = int(bl + (bb - bl) * (1 - self.intensity / INTENSE_MAX))
        color = QColor(rn, gn, bn)
        return color

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y  # and self.intensity == other.intensity
