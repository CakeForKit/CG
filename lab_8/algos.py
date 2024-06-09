from structs import *
from errs import *


def round(x):
    return int(x + 0.5)


def get_parallel_line(line: Line, dy):
    x1, y1 = line.p1.get_xy()
    x2, y2 = line.p2.get_xy()

    if x2 == x1:
        p1 = Point(x1 + dy, y1)
        p2 = Point(x1 + dy, y2)
        return Line(p1, p2, line.color)

    k = (y2 - y1) / (x2 - x1)

    def find_parallel(x1, y1, k, x2):
        return round(k * (x2 - x1) + y1)

    p1 = Point(x1, y1 + dy)
    p2 = Point(x2, find_parallel(x1, y1 + dy, k, x2))
    return Line(p1, p2, line.color)


def scalar_mul(fvector, svector):
    return fvector[0] * svector[0] + fvector[1] * svector[1]


def get_vect(p1, p2):
    return [p2.x - p1.x, p2.y - p1.y]


def get_vect_mul(fvector, svector):
    return fvector[0] * svector[1] - fvector[1] * svector[0]


# проверка на выпуклость через векторное произведение
def is_polygon_convexity(clipper: Clipper):
    vect1 = get_vect(clipper[0], clipper[1])
    vect2 = get_vect(clipper[1], clipper[2])

    sign = None
    if get_vect_mul(vect1, vect2) > 0:
        sign = 1
    else:
        sign = -1

    for i in range(len(clipper)):
        vecti = get_vect(clipper[i - 2], clipper[i - 1])
        vectj = get_vect(clipper[i - 1], clipper[i])

        if sign * get_vect_mul(vecti, vectj) < 0:
            return False

    return True


def get_normal(dot1, dot2, dot3):
    vector = get_vect(dot1, dot2)

    if vector[1]:
        normal = [1, - vector[0] / vector[1]]
    else:
        normal = [0, 1]

    if scalar_mul(get_vect(dot2, dot3), normal) < 0:
        normal[0] = - normal[0]
        normal[1] = - normal[1]

    return normal


def cut_cyrus_beck(qp, line: Line, clipper: Clipper):
    t_beg = 0
    t_end = 1

    dot1 = line.p1
    dot2 = line.p2

    d = [dot2.x - dot1.x, dot2.y - dot1.y]  # директриса

    for i in range(-2, len(clipper) - 2):
        normal = get_normal(clipper[i], clipper[i + 1], clipper[i + 2])

        w = [dot1.x - clipper[i].x,
             dot1.y - clipper[i].y]

        d_scalar = scalar_mul(d, normal)
        w_scalar = scalar_mul(w, normal)

        if d_scalar == 0:
            if w_scalar < 0:
                return
            else:
                continue

        t = - w_scalar / d_scalar

        if d_scalar > 0:
            if t <= 1:
                t_beg = max(t_beg, t)
            else:
                return

        elif d_scalar < 0:
            if t >= 0:
                t_end = min(t_end, t)
            else:
                return

        if t_beg > t_end:
            break

    if t_beg <= t_end:
        dot1_res = [round(dot1.x + d[0] * t_beg), round(dot1.y + d[1] * t_beg)]
        dot2_res = [round(dot1.x + d[0] * t_end), round(dot1.y + d[1] * t_end)]

        qp.drawLine(*dot1_res, *dot2_res)


def cut_lines_cyrus_beck(qp, lines: Lines, visible_color: QColor, clipper: Clipper):
    qp.setPen(QPen(visible_color))
    for line in lines:
        cut_cyrus_beck(qp, line, clipper)
