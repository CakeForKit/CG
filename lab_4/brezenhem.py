from Point import *
import math as m


def mathround(n):
    return int(n + 0.5)



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


def brezenhem_ellipse(ra, rb, center: Point, canvas, color, draw, count_loop=False):
    xc, yc = center.get_xy()
    x, y = 0, rb
    ra2 = ra * ra
    rb2 = rb * rb

    delta_i = rb2 - ra2 * (2 * y - 1)  #
    eps = 0

    count = 0
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

        if count_loop:
            count += 1
    return count
