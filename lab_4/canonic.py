from Point import *
import math as m


def mathround(n):
    return int(n + 0.5)


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
def canonic_eq_ellipse(ra, rb, center: Point, canvas, color, draw, count_loop=False):
    xc, yc = center.x, center.y
    ra2, rb2 = ra * ra, rb * rb

    border_x = mathround(xc + ra / m.sqrt(1 + rb2 / ra2))  # вывод на листочке
    border_y = mathround(yc + rb / m.sqrt(1 + ra2 / rb2))

    count = 0
    for x in range(mathround(xc), border_x + 1):
        y = yc + m.sqrt(ra2 * rb2 - (x - xc) ** 2 * rb2) / ra
        if draw:
            draw_symmetric_1_4(Point(x, mathround(y)), center, canvas, color)
        if count_loop:
            count += 1

    for y in range(border_y, mathround(yc) - 1, -1):
        x = xc + m.sqrt(ra2 * rb2 - (y - yc) ** 2 * ra2) / rb
        if draw:
            draw_symmetric_1_4(Point(mathround(x), y), center, canvas, color)
        if count_loop:
            count += 1
    # print(f'CANONIC count loop = {count}')

    return count