from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import QPoint
from Point import *
import math as m


def mathround(n):
    return int(n + 0.5)


def canonic_eq(ra, rb, center: Point, canvas, color, draw):
    if ra == rb:
        return canonic_eq_circle(ra, center, canvas, color, draw)
    else:
        return canonic_eq_ellipse(ra, rb, center, canvas, color, draw)


def param_eq(ra, rb, center: Point, canvas, color, draw):
    if ra == rb:
        return param_eq_circle(ra, center, canvas, color, draw)
    else:
        return param_eq_ellipse(ra, rb, center, canvas, color, draw)


def brezenhem(ra, rb, center: Point, canvas, color, draw):
    if ra == rb:
        return brezenhem_circle(ra, center, canvas, color, draw)
    else:
        return brezenhem_ellipse(ra, rb, center, canvas, color, draw)


def alg_midpoint(ra, rb, center: Point, canvas, color, draw):
    if ra == rb:
        return alg_midpoint_circle(ra, center, canvas, color, draw)
    else:
        return alg_midpoint_ellipse(ra, rb, center, canvas, color, draw)


def lib(ra, rb, center: Point, canvas, color, draw):
    qp = QPainter(canvas)
    qp.setPen(QPen(color, 1))
    qp.drawEllipse(QPoint(*center.get_xy()), ra, rb)


# Каноническое уравнение окружности
# (x - xc) ** 2 + (y - yc) ** 2 = R**2
# y = +- sqrt(R**2 - (x - xc)**2) + yc
def canonic_eq_circle(r, center: Point, canvas, color, draw):
    # print(f'canonic_eq_circle: r={r}, center={center}')
    xc = center.x
    yc = center.y
    r2 = r ** 2
    # build 1/8 points
    for x in range(xc, mathround(xc + r / m.sqrt(2)) + 1):
        y = mathround(m.sqrt(r2 - (x - xc) ** 2)) + yc
        if draw:
            draw_symmetric_1_8(Point(x, y), center, canvas, color)


# Каноническое уравнение Эллипса
# (x - xc) ** 2 / (a ** 2) + (y - yc) ** 2 / (b ** 2) = 1
# b**2 * (x - xc)**2 + a**2 * (y - yc)**2 = a**2 * b**2
def canonic_eq_ellipse(ra, rb, center: Point, canvas, color, draw):
    xc, yc = center.x, center.y
    ra2, rb2 = ra * ra, rb * rb

    border_x = mathround(xc + ra / m.sqrt(1 + rb2 / ra2))  # вывод на листочке
    border_y = mathround(yc + rb / m.sqrt(1 + ra2 / rb2))

    for x in range(mathround(xc), border_x + 1):
        y = yc + m.sqrt(ra2 * rb2 - (x - xc) ** 2 * rb2) / ra
        if draw:
            draw_symmetric_1_4(Point(x, mathround(y)), center, canvas, color)

    for y in range(border_y, mathround(yc) - 1, -1):
        x = xc + m.sqrt(ra2 * rb2 - (y - yc) ** 2 * ra2) / rb
        if draw:
            draw_symmetric_1_4(Point(mathround(x), y), center, canvas, color)


# Параметрическое уравнение окружности
# x = r * cos(angle) + xc
# y = r * sin(angle) + yc
def param_eq_circle(r, center: Point, canvas, color, draw):
    xc, yc = center.x, center.y
    step = 1 / r
    '''При достаточно большом радиусе кривизны 2 соседние т. кривой необходимо выбирать, 
    так чтобы значение угла(рад) образованного радиусами, 
    проведенными в рассматриваемые точки, было не менее 1/R (R - радиус кривизны кривой в выбранной точке)'''

    # points1_8 = list()
    angle_rad = 0
    while angle_rad <= m.pi / 4:
        x = mathround(r * m.cos(angle_rad)) + xc
        y = mathround(r * m.sin(angle_rad)) + yc
        if draw:
            draw_symmetric_1_8(Point(x, y), center, canvas, color)

        angle_rad += step



# Параметрическое уравнение Эллипса
# x = r * cos(angle) + xc
# y = r * sin(angle) + yc
def param_eq_ellipse(ra, rb, center: Point, canvas, color, draw):
    xc, yc = center.x, center.y
    if ra > rb:
        step = 1 / ra
    else:
        step = 1 / rb
    '''Т к вычисление радиуса кривизны ко всех точка трудоемко, 
    можно найти макс радиус кривизны и провести аппроксимацию на его основе'''

    # points1_4 = list()
    angle_rad = 0
    while angle_rad <= m.pi / 2:
        x = mathround(ra * m.cos(angle_rad)) + xc
        y = mathround(rb * m.sin(angle_rad)) + yc
        if draw:
            draw_symmetric_1_4(Point(x, y), center, canvas, color)

        angle_rad += step



def brezenhem_circle(r, center: Point, canvas, color, draw):
    # print(f'brezenhem_circle: ')
    xc, yc = center.get_xy()
    x, y = 0, r
    di = 2 * (1 - r)
    delta = 0

    while x <= y:
        if draw:
            draw_symmetric_1_8(Point(x + xc, mathround(y) + yc), center, canvas, color)

        dir = 2
        if di <= 0:
            delta = 2 * (di + y) - 1

            if delta < 0:
                dir = 1  # mh
            else:
                dir = 2  # md
        elif di > 0:
            delta = 2 * (di - x) - 1

            if delta < 0:
                dir = 2  # md
            else:
                dir = 3  # mv

        x += 1
        if dir == 1:  # mh
            di += 2 * x + 1
        elif dir == 2:  # md
            y -= 1
            di += 2 * x - 2 * y + 2
        else:
            y -= 1
            di += - 2 * y + 1


def brezenhem_ellipse(ra, rb, center: Point, canvas, color, draw):
    xc, yc = center.get_xy()
    x, y = 0, rb
    ra2 = ra * ra
    rb2 = rb * rb

    delta_i = rb2 - ra2 * (2 * y - 1)  #
    eps = 0

    while y >= 0:
        if draw:
            draw_symmetric_1_4(Point(x + xc, mathround(y) + yc), center, canvas, color)

        dir = 2
        if delta_i < 0:
            eps = 2 * delta_i + (2 * y + 2) * ra2

            if eps < 0:
                dir = 1
            else:
                dir = 2
        elif delta_i > 0:
            eps = 2 * delta_i + (- 2 * x + 2) * rb2
            if eps <= 0:
                dir = 2
            else:
                dir = 3
        else:
            dir = 2

        if dir == 1:
            x += 1
            delta_i += (2 * x + 1) * rb2 #+ rb2
        elif dir == 2:
            x += 1
            y -= 1
            delta_i += (2 * x + 1) * rb2 + (1 - 2 * y) * ra2
        else:
            y -= 1
            delta_i += (1 - 2 * y) * ra2

# d = f(x, y) = (x + 1)**2 + (y - 1/2)**2 - r**2
def alg_midpoint_circle(r, center: Point, canvas, color, draw):
    xc, yc = center.get_xy()
    x, y = 0, mathround(r)

    di = 5 / 4 - r  # = f(0, r)
    while y >= x:
        if draw:
            draw_symmetric_1_8(Point(x + xc, y + yc), center, canvas, color)

        if di < 0:
            di += 2 * x + 3
            x += 1
        else:
            di += 2 * x + 3 - 2 * y + 2
            x += 1
            y -= 1


def alg_midpoint_ellipse(ra, rb, center: Point, canvas, color, draw):
    xc, yc = center.get_xy()
    x, y = 0, mathround(rb)
    ra2 = ra * ra
    rb2 = rb * rb

    border_x = mathround(ra / m.sqrt(1 + rb2 / ra2))
    border_y = mathround(rb / m.sqrt(1 + ra2 / rb2))

    di = rb2 + ra2 * mathround(0.25 - rb)
    while x <= border_x:
        if draw:
            draw_symmetric_1_4(Point(x + xc, y + yc), center, canvas, color)

        if di < 0:
            di += rb2 * (2 * x + 3)
            x += 1
        else:
            di += rb2 * (2 * x + 3) + 2 * ra2 * (1 - y)
            x += 1
            y -= 1

    x, y = mathround(ra), 0
    di = ra2 + rb2 * mathround(0.25 - ra)

    while y <= border_y:
        if draw:
            draw_symmetric_1_4(Point(x + xc, y + yc), center, canvas, color)

        if di < 0:
            di += ra2 * (2 * y + 3)
            y += 1
        else:
            di += ra2 * (2 * y + 3) + 2 * rb2 * (1 - x)
            x -= 1
            y += 1


if __name__ == '__main__':
    pass
