from structs import *


def round(x):
    return int(x + 0.5)


def find_point_code(p: Point, clipper: Clipper):
    code = [0, 0, 0, 0]

    if p.x < clipper.x_left:
        code[0] = 1
    elif p.x > clipper.x_right:
        code[1] = 1
    if p.y < clipper.y_top:
        code[2] = 1
    elif p.y > clipper.y_bottom:
        code[3] = 1

    return code


def code_mult(t1, t2):
    if len(t1) != 4 or len(t2) != 4:
        raise ValueError('Error point_code ')

    mult = 0
    for i in range(4):
        mult += t1[i] * t2[i]
    return mult


# return r, or -1 if line horisontal
def find_r(p1: Point, p2: Point, q: Point, clipper: Clipper, flag: list):
    left = clipper.x_left
    right = clipper.x_right
    bottom = clipper.y_top
    top = clipper.y_bottom

    m = float('inf')  # угол наклона отрезка
    # Если отрезок не вертикальный
    if p1.x != p2.x:
        m = (p2.y - p1.y) / (p2.x - p1.x)
        if q.x <= left:
            y = round(m * (left - q.x) + q.y)
            if bottom <= y <= top:
                return Point(left, y)  # пересечение с левым краем отсекателя
        if q.x >= right:
            y = round(m * (right - q.x) + q.y)
            if bottom <= y <= top:
                return Point(right, y)  # пересечение с правым краем отсекателя

    # проверка горизонтальности отрезка
    if m == 0:
        flag[0] = False
        return q

    # проверка пересечения с верхним краем
    if q.y >= top:
        x = round((top - q.y) / m + q.x)
        if left <= x <= right:
            return Point(x, top)
    # проверка пересечения с нижним краем
    if q.y <= bottom:
        x = round((bottom - q.y) / m + q.x)
        if left <= x <= right:
            return Point(x, bottom)

    flag[0] = False
    return q


def cut_line(line: Line, clipper: Clipper):
    flag_visibility = True  # признак видимости
    # r1 r2 - видиимые концевые точки

    # вычисление кодов концевых точек
    t1 = find_point_code(line.p1, clipper)
    t2 = find_point_code(line.p2, clipper)
    s1 = sum(t1)
    s2 = sum(t2)

    # print(line, t1, t2)

    # проверка полной видимости отрезка
    if s1 == 0 and s2 == 0:
        return (flag_visibility, line)  # весь отрезок видиим
    else:
        # проверка случая тривиальной невидимости
        if code_mult(t1, t2) != 0:
            flag_visibility = False
            return (flag_visibility, line)  # отрезок тривиально невидим
        else:
            i = 0
            # проверка попадания точки1 в отсекатель
            if s1 == 0:
                r1 = line.p1
                q = line.p2
                i = 1
            # проверка попадания точки2 в отсекатель
            elif s2 == 0:
                r1 = line.p2
                q = line.p1
                i = 1

            if i == 0:
                q = line.p1
                flag = [flag_visibility]
                r1 = find_r(line.p1, line.p2, q, clipper, flag)
                flag_visibility = flag[0]
                q = line.p2
            flag = [flag_visibility]
            r2 = find_r(line.p1, line.p2, q, clipper, flag)
            flag_visibility = flag[0]

    if flag_visibility:
        return (flag_visibility, Line(r1, r2, line.color))

    return (flag_visibility, line)


def simple_cut(qp, lines: Lines, visible_color: QColor, clipper: Clipper):
    save_pen = qp.pen()
    qp.setPen(visible_color)
    for i in range(len(lines)):
        vline = cut_line(lines[i], clipper)
        print(vline)
        if vline[0]:
            x1, y1 = vline[1].p1.get_xy()
            x2, y2 = vline[1].p2.get_xy()
            print(x1, y1, x2, y2)
            qp.drawLine(x1, y1, x2, y2)
    qp.setPen(save_pen)
