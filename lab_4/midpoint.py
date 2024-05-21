from Point import *
import math as m


def mathround(n):
    return int(n + 0.5)


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


def alg_midpoint_ellipse(ra, rb, center: Point, canvas, color, draw, count_loop=False):
    xc, yc = center.get_xy()
    x, y = 0, mathround(rb)
    ra2 = ra * ra
    rb2 = rb * rb

    border_x = mathround(ra / m.sqrt(1 + rb2 / ra2))
    border_y = mathround(rb / m.sqrt(1 + ra2 / rb2))

    count = 0

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
        if count_loop:
            count += 1

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

        if count_loop:
            count += 1

    return count
