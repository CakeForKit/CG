from Clipper import *
from Figure import *
from errs import *
from numpy import sign, matrix

EPS = 1e-8

def round(x):
    return int(x + 0.5)


# def scalar_mul(fvector, svector):
#     return fvector[0] * svector[0] + fvector[1] * svector[1]

def get_vect(p1, p2):
    return [p2.x - p1.x, p2.y - p1.y]


def get_vect_mul(fvector, svector):
    return fvector[0] * svector[1] - fvector[1] * svector[0]


# проверка на выпуклость через векторное произведение
def is_polygon_convexity(clipper: Clipper):
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
        clipper.reverse()

    return True


# return
# < 0 - невидима
# ==0 - лежит на стороне
# >0 - видима
def visibility(point: Point, begp: Point, endp: Point):
    # определение видимости через вектороное произведение
    tmp1 = (point.x - begp.x) * (endp.y - begp.y)
    tmp2 = (point.y - begp.y) * (endp.x - begp.x)
    res = tmp1 - tmp2

    if -EPS < res < EPS:
        res = 0
    return sign(res)


def is_lines_crossing(begin1: Point, end1: Point, begin2: Point, end2: Point):
    vis1 = visibility(begin1, begin2, end2) # определеить видимость начальной точки ребра многоугольника
    vis2 = visibility(end1, begin2, end2)   # определеить видимость конечной точки ребра многоугольника

    if (vis1 < 0 and vis2 > 0) or (vis1 > 0 and vis2 < 0):
        return True
    else:
        return False


def get_cross_point(begin1: Point, end1: Point, begin2: Point, end2: Point):
    # вычисление точки пересечения 2х отрезков через параметрическое уравнение
    coef = []
    coef.append([end1.x - begin1.x, begin2.x - end2.x])
    coef.append([end1.y - begin1.y, begin2.y - end2.y])

    rights = []
    rights.append([begin2.x - begin1.x])
    rights.append([begin2.y - begin1.y])

    coef_tmp = matrix(coef)
    coef_tmp = coef_tmp.I
    coef = [[coef_tmp.item(0), coef_tmp.item(1)], [coef_tmp.item(2), coef_tmp.item(3)]]

    coef_tmp = matrix(coef)
    param = coef_tmp.__mul__(rights)

    x, y = begin1.x + (end1.x - begin1.x) * param.item(0), begin1.y + (end1.y - begin1.y) * param.item(0)

    return Point(x, y)


def cut_sutherland_hodgman(figure: Figure, clipper: Clipper):
    if not figure.is_closed() or not clipper.is_closed():
        return

    A_figure = figure
    res_B_figure = []
    C_clipper = clipper

    len_A_figure = len(A_figure)
    len_res_B_figure = 0
    len_C_clipper = len(C_clipper)

    s = []
    f = []
    for i in range(len_C_clipper - 1):  # цикл по всем границам отсекателя
        len_res_B_figure = 0
        res_B_figure = []
        for j in range(len_A_figure):  # цикл по всем границам отсекаемого многоугольника
            if j != 0:
                # 1
                # определить факт пересечения ребра S--Aj с текущей границей отсекателя Ci--Ci+1
                is_crossing = is_lines_crossing(s, A_figure[j], C_clipper[i], C_clipper[i + 1])
                if is_crossing:
                    # если пересечение есть, то находим точку пересечения и заносим ее в результат
                    res_B_figure.append(get_cross_point(s, A_figure[j], C_clipper[i], C_clipper[i + 1]))
                    len_res_B_figure += 1
            else:
                f = A_figure[j]     # особо обработать первую вершину многоугольника
# 2
            # изменить начальную точку ребра многоугольника
            s = A_figure[j]
            if visibility(s, C_clipper[i], C_clipper[i + 1]) >= 0:   # проверяем видимость конечной точки
                res_B_figure.append(s)
                len_res_B_figure += 1
# 3
        if len_res_B_figure == 0:
            return res_B_figure, len_res_B_figure

        # определить факт пересечения последним ребром многоугольника отсекателя
        is_crossing = is_lines_crossing(s, f, C_clipper[i], C_clipper[i + 1])
        if is_crossing:
            res_B_figure.append(get_cross_point(s, f, C_clipper[i], C_clipper[i + 1]))
            len_res_B_figure += 1

    return res_B_figure, len_res_B_figure


def cut(qp, figure: Figure, clipper: Clipper, visible_color: QColor):
    qp.setPen(QPen(visible_color))
    p, np = cut_sutherland_hodgman(figure, clipper)

    # print(f'figure = {figure}')
    # print(f'clipper = {clipper}')
    for i in range(np):
        qp.drawLine(round(p[i - 1].x), round(p[i - 1].y), round(p[i].x), round(p[i].y))
