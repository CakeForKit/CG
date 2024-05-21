from Point import *
import math as m


def mathround(n):
    return int(n + 0.5)


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
def param_eq_ellipse(ra, rb, center: Point, canvas, color, draw, count_loop=False):
    xc, yc = center.x, center.y
    if ra > rb:
        step = 1 / ra
    else:
        step = 1 / rb
    '''Т к вычисление радиуса кривизны ко всех точка трудоемко, 
    можно найти макс радиус кривизны и провести аппроксимацию на его основе'''

    count = 0

    # points1_4 = list()
    angle_rad = 0
    while angle_rad <= m.pi / 2:
        x = mathround(ra * m.cos(angle_rad)) + xc
        y = mathround(rb * m.sin(angle_rad)) + yc
        if draw:
            draw_symmetric_1_4(Point(x, y), center, canvas, color)

        angle_rad += step
        if count_loop:
            count += 1
    # print(f'PARAM count loop = {count}')
    return count