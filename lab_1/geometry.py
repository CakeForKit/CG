import math as m

DEBUG = False
EPS = 1e-5


# проверяет, является ли угол 123 = 90град
def if_90_grad(p1, p2, p3):
    # находим вектора
    v12 = (p1[0] - p2[0], p1[1] - p2[1])
    v32 = (p3[0] - p2[0], p3[1] - p2[1])

    # проверяем перпендикулярность угла 123 по скалярному произведению
    return v12[0] * v32[0] + v12[1] * v32[1] == 0


def find_x4_y4_in_rect(p1, p2, p3):
    if if_90_grad(p2, p1, p3):
        x4 = p3[0] + (p2[0] - p1[0])
        y4 = p3[1] + (p2[1] - p1[1])
    elif if_90_grad(p1, p2, p3):
        x4 = p1[0] + (p3[0] - p2[0])
        y4 = p1[1] + (p3[1] - p2[1])
    elif if_90_grad(p1, p3, p2):
        x4 = p1[0] + (p2[0] - p3[0])
        y4 = p1[1] + (p2[1] - p3[1])
    else:
        return None
    return x4, y4


def center_of_rect(rect_list):
    max_x = max(i[0] for i in rect_list)
    min_x = min(i[0] for i in rect_list)
    max_y = max(i[1] for i in rect_list)
    min_y = min(i[1] for i in rect_list)
    xy = [(max_x + min_x) / 2, (max_y + min_y) / 2]

    print(f'\ncenter_of_rect:\t rect: {rect_list}\ncenter: {xy}')
    return xy


# возвращает коэфиценты уравнени прямой - ax + by + c = 0
def line_abc(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    a = y2 - y1
    b = x1 - x2
    c = y1 * (x2 - x1) - x1 * (y2 - y1)
    return (a, b, c)


# возвращает коэфиценты ур биссектрисы внутреннего угла между прямыми 12 и 13
def bisectrix_abc(abc12, abc13, p2, p3):
    a12, b12, c12 = abc12
    a13, b13, c13 = abc13
    sqrt12 = m.sqrt(a12 ** 2 + b12 ** 2)
    sqrt13 = m.sqrt(a13 ** 2 + b13 ** 2)

    # ур со знаком плюс
    pa213 = a12 * sqrt13 - a13 * sqrt12
    pb213 = b12 * sqrt13 - b13 * sqrt12
    pc213 = c12 * sqrt13 - c13 * sqrt12
    # ур со знаком минус
    ma213 = a12 * sqrt13 + a13 * sqrt12
    mb213 = b12 * sqrt13 + b13 * sqrt12
    mc213 = c12 * sqrt13 + c13 * sqrt12

    # подставим точки 2 и 3 в уравнения биссектрис, если знаки будут разные то это биссектриса внутреннего угла
    x2, y2 = p2
    x3, y3 = p3
    if (pa213 * x2 + pb213 * y2 + pc213) * (pa213 * x3 + pb213 * y3 + pc213) < 0:
        return (pa213, pb213, pc213)
    else:
        return (ma213, mb213, mc213)


# возвращает координаты точки пересечения двух прямых по коэфицентам их уравнений
def point_intersection_lines(a1, b1, c1, a2, b2, c2):
    if (a1 == 0 and a2 == 0) or (b1 == 0 and b2 == 0):
        return None

    if (b1 != 0 and b2 != 0) and abs(a1 / b1 - a2 / b2) < EPS:
        return None

    if a2 == 0:
        y = -c2 / b2
        x = (-c1 - b1 * y) / a1
    elif a1 == 0:
        y = -c1 / b1
        x = (-c2 - b2 * y) / a2
    else:
        y = -(c1 - c2 * (a1 / a2)) / (b1 - b2 * (a1 / a2))
        x = (-c1 - b1 * y) / a1
    return [x, y]


def if_triangle(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    if x1 == x2 and x1 == x3:
        return False
    if x1 == x2 or x1 == x3:
        return True
    if abs((y2 - y1) / (x2 - x1) - (y3 - y1) / (x3 - x1)) < EPS:
        return False
    return True


# возвращает координаты точки пересечения биссектрис
def point_intersection_bisectrix(p1, p2, p3, debug_hear=False):
    if DEBUG or debug_hear:
        print(f'\nSTART point_intersection_bisectrix: 3 points: {p1}, {p2}, {p3}')
    # коэф уравнений прямых 12, 13, 23
    abc12 = line_abc(p1, p2)
    abc13 = line_abc(p1, p3)
    abc23 = line_abc(p2, p3)

    if DEBUG or debug_hear:
        print(f'a12, b12, c12: {abc12}')
        print(f'a13, b13, c13: {abc13}')
        print(f'a23, b23, c23: {abc23}')

    # коэф биссектрис углов 213, 123
    abc213 = bisectrix_abc(abc12, abc13, p2, p3)
    abc123 = bisectrix_abc(abc12, abc23, p1, p3)

    if DEBUG or debug_hear:
        print('abc213: ', abc213)
        print('abc123: ', abc123)

    # точка пересечения биссектрис
    xy = point_intersection_lines(*abc213, *abc123)

    if DEBUG or debug_hear:
        print(f'xy: {xy}')

    return xy


# возвращает угол в радианах между прямой 12 и осью OX
def angle_ox(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        return m.pi / 2

    k = (y2 - y1) / (x2 - x1)
    rad = m.atan(k)
    return rad


# принимает список прямоугольника и список точек
# возвращает кортеж из 3 точек прямоугольника, точку центра прямоугольника, и точку пересечения биссектрис и угол в градусах
def find_triangle(rect_list, arr, debug_hear=False):
    if DEBUG:
        print(f'find_triangle:\t rect_list: {rect_list}, arr: {arr}')
    if len(rect_list) < 4 or len(arr) < 3:
        raise Exception('ERR find_triangle PARAMETRS')
    min_angle = 360
    angle = 360
    bis_out = []
    points = tuple()

    center_rect = center_of_rect(rect_list)
    for i in range(len(arr)):
        p1 = arr[i]
        for j in range(i + 1, len(arr)):
            p2 = arr[j]
            for k in range(j + 1, len(arr)):
                p3 = arr[k]
                if if_triangle(p1, p2, p3):
                    bis = point_intersection_bisectrix(p1, p2, p3)
                    if not bis is None:
                        angle = angle_ox(center_rect, bis)

                        if DEBUG or debug_hear:
                            print(f'3 points: {(p1, p2, p3)}, angle: {m.degrees(angle)}')

                        if abs(angle) < abs(min_angle):
                            min_angle = angle
                            bis_out = bis
                            points = (p1, p2, p3)

    return points, bis_out, center_rect, m.degrees(min_angle)


