from Point import Point, Pixel, INTENSE_MAX
import math as m


def round(n):
    return int(n + 0.5)


def symmetric_part_circle_1_8(center, points1_8):
    xc, yc = center.x, center.y
    points = list()
    for p in points1_8:
        tmp = [Point(p.x, p.y)]
        tmp += [Point(i.y - yc + xc, i.x - xc + yc) for i in tmp]
        tmp += [Point(-i.x + 2 * xc, i.y) for i in tmp]
        tmp += [Point(i.x, -i.y + 2 * yc) for i in tmp]
        points.extend(tmp)
    return points


def symmetric_part_ellipse_1_4(center, points1_4):
    xc, yc = center.x, center.y
    points = list()
    for p in points1_4:
        tmp = [Point(p.x, p.y)]
        tmp += [Point(-i.x + 2 * xc, i.y) for i in tmp]
        tmp += [Point(i.x, -i.y + 2 * yc) for i in tmp]
        points.extend(tmp)
    return points


def canonic_eq(ra, rb, center: Point):
    if ra == rb:
        return canonic_eq_circle(ra, center)
    else:
        return canonic_eq_ellipse(ra, rb, center)


def param_eq(ra, rb, center: Point):
    if ra == rb:
        return param_eq_circle(ra, center)
    else:
        return param_eq_ellipse(ra, rb, center)


def brezenhem(ra, rb, center: Point):
    if ra == rb:
        return brezenhem_circle(ra, center)
    else:
        return brezenhem_ellipse(ra, rb, center)


def alg_midpoint(ra, rb, center: Point):
    if ra == rb:
        return alg_midpoint_circle(ra, center)
    else:
        return alg_midpoint_ellipse(ra, rb, center)


def lib(ra, rb, center: Point):
    print(f'lib: ')
    return []


# Каноническое уравнение окружности
# (x - xc) ** 2 + (y - yc) ** 2 = R**2
# y = +- sqrt(R**2 - (x - xc)**2) + yc
def canonic_eq_circle(r, center: Point):
    print(f'canonic_eq_circle: r={r}, center={center}')
    xc = center.x
    yc = center.y
    r2 = r ** 2
    points1_8 = list()
    # build 1/8 points
    for x in range(xc, round(xc + r / m.sqrt(2)) + 1):
        y = round(m.sqrt(r2 - (x - xc) ** 2)) + yc
        points1_8.append(Point(x, y))
    points = symmetric_part_circle_1_8(center, points1_8)
    return points


# Каноническое уравнение Эллипса
# (x - xc) ** 2 / (a ** 2) + (y - yc) ** 2 / (b ** 2) = 1
# b**2 * (x - xc)**2 + a**2 * (y - yc)**2 = a**2 * b**2
def canonic_eq_ellipse(ra, rb, center: Point):
    print(f'canonic_eq_ellips: ra={ra} rb={rb}, center={center}')
    xc, yc = center.x, center.y
    ra2, rb2 = ra ** 2, rb ** 2

    border_x = xc + round(ra2 / m.sqrt(ra2 + rb2))
    border_y = yc + round(rb2 / m.sqrt(ra2 + rb2))

    points1_4 = list()
    for x in range(xc, border_x + 1):
        y = m.sqrt(ra2 * rb2 - (x - xc) ** 2 * rb2) / ra + yc
        points1_4.append(Point(x, round(y)))

    for y in range(border_y, yc - 1, -1):
        x = m.sqrt(ra2 * rb2 - (y - yc) ** 2 * ra2) / rb + xc
        points1_4.append(Point(round(x), y))

    # print('\n'.join([f'{i.x}, {i.y}' for i in points1_4]))
    points = symmetric_part_ellipse_1_4(center, points1_4)
    return points


# Параметрическое уравнение окружности
# x = r * cos(angle) + xc
# y = r * sin(angle) + yc
def param_eq_circle(r, center: Point):
    print(f'param_eq_circle: r={r}, center={center}')
    xc, yc = center.x, center.y
    step = 1 / r

    points1_8 = list()
    angle_rad = 0
    while angle_rad <= m.pi / 4:
        x = r * m.cos(angle_rad) + xc
        y = r * m.sin(angle_rad) + yc
        points1_8.append(Point(round(x), round(y)))

        angle_rad += step

    points = symmetric_part_circle_1_8(center, points1_8)
    return points


# Параметрическое уравнение Эллипса
# x = r * cos(angle) + xc
# y = r * sin(angle) + yc
def param_eq_ellipse(ra, rb, center: Point):
    print(f'param_eq_ellipse: ra={ra} rb={rb}, center={center}')
    xc, yc = center.x, center.y
    step = 1 / max(ra, rb)

    points1_4 = list()
    angle_rad = 0
    while angle_rad <= m.pi / 2:
        x = ra * m.cos(angle_rad) + xc
        y = rb * m.sin(angle_rad) + yc
        points1_4.append(Point(round(x), round(y)))

        angle_rad += step

    points = symmetric_part_ellipse_1_4(center, points1_4)
    return points


def brezenhem_circle(r, center: Point):
    print(f'brezenhem_circle: ')
    points = list()
    for x in range(100, 200):
        for y in range(100, 200):
            points.append(Point(x, y))

    return points


def brezenhem_ellipse(ra, rb, center: Point):
    print(f'brezenhem_ellipse: ')
    points = list()
    for x in range(100, 200):
        for y in range(100, 200):
            points.append(Point(x, y))

    return points


def alg_midpoint_circle(r, center: Point):
    print(f'alg_midpoint_circle: ')
    points = list()
    for x in range(100, 200):
        for y in range(100, 200):
            points.append(Point(x, y))

    return points


def alg_midpoint_ellipse(ra, rb, center: Point):
    print(f'alg_midpoint_ellipse: ')
    points = list()
    for x in range(100, 200):
        for y in range(100, 200):
            points.append(Point(x, y))

    return points


if __name__ == '__main__':
    pass
