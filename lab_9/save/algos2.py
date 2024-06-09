from Clipper import *
from Figure import *
from errs import *
from numpy import sign, matrix


def round(x):
    return int(x + 0.5)


def get_vect(dot_start, dot_end):
    return [dot_end[0] - dot_start[0], dot_end[1] - dot_start[1]]


def get_vect_mul(fvector, svector):
    return fvector[0] * svector[1] - fvector[1] * svector[0]


# проверка на выпуклость через векторное произведение
def is_polygon_convexity(cl: Clipper):
    clipper = cl.get_list_of_lists()
    if len(clipper) < 3:
        return False

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

    if sign < 0:
        cl

    return True


def visibility(point, begin, end):
    tmp1 = (point[0] - begin[0]) * (end[1] - begin[1])
    tmp2 = (point[1] - begin[1]) * (end[0] - begin[0])
    res = tmp1 - tmp2

    if -1e-7 < res < 1e-7:
        res = 0
    return sign(res)


def check_lines_crossing(begin1, end1, begin2, end2):
    vis1 = visibility(begin1, begin2, end2)
    vis2 = visibility(end1, begin2, end2)

    if (vis1 < 0 and vis2 > 0) or (vis1 > 0 and vis2 < 0):
        return True
    else:
        return False


def get_cross_point(begin1, end1, begin2, end2):
    coef = []
    coef.append([end1[0] - begin1[0], begin2[0] - end2[0]])
    coef.append([end1[1] - begin1[1], begin2[1] - end2[1]])

    rights = []
    rights.append([begin2[0] - begin1[0]])
    rights.append([begin2[1] - begin1[1]])

    coef_tmp = matrix(coef)
    coef_tmp = coef_tmp.I
    coef = [[coef_tmp.item(0), coef_tmp.item(1)], [coef_tmp.item(2), coef_tmp.item(3)]]

    coef_tmp = matrix(coef)
    param = coef_tmp.__mul__(rights)

    x, y = begin1[0] + (end1[0] - begin1[0]) * param.item(0), begin1[1] + (end1[1] - begin1[1]) * param.item(0)

    return [x, y]


def cut_sutherland_hodgman(polygon, clipper):
    p = polygon
    q = []
    w = clipper

    np = len(p)
    nq = 0
    nw = len(w)

    s = []
    f = []
    for i in range(nw - 1):
        nq = 0
        q = []
        for j in range(np):
            if j != 0:
                is_crossing = check_lines_crossing(s, p[j], w[i], w[i + 1])
                if is_crossing == True:
                    q.append(get_cross_point(s, p[j], w[i], w[i + 1]))
                    nq += 1
                else:
                    if visibility(s, w[i], w[i + 1]) == 0:
                        q.append(s)
                        nq += 1
                    elif visibility(p[j], w[i], w[i + 1]) == 0:
                        q.append(s)
                        nq += 1
            else:
                f = p[j]
            s = p[j]
            if visibility(s, w[i], w[i + 1]) > 0:
                continue
            q.append(s)
            nq += 1
        if nq == 0:
            continue
        is_crossing = check_lines_crossing(s, f, w[i], w[i + 1])
        if is_crossing == False:
            p = q
            np = nq
            continue
        q.append(get_cross_point(s, f, w[i], w[i + 1]))
        nq += 1
        p = q
        np = nq

    return p, np


def cut(qp, figure: Figure, clipper: Clipper, visible_color: QColor):
    qp.setPen(QPen(visible_color))
    fl = figure.get_list_of_lists()
    cl = clipper.get_list_of_lists()
    print(f'figure = {fl}')
    print(f'clipper = {cl}')
    p, np = cut_sutherland_hodgman(fl, cl)

    print(f'figure = {fl}')
    print(f'clipper = {cl}')
    for i in range(np):
        qp.drawLine(round(p[i - 1][0]), round(p[i - 1][1]), round(p[i][0]), round(p[i][1]))
