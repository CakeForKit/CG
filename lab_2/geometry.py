import math as m


# (x - a)**2 + (y - b)**2 = r**2
# x = a + r * cos(degrees)
# y = b + r * sin(degrees)
# return circle = [[x, y] ... ]
def build_start_circle(a, b, r, scale):
    circle = list()
    degrees = 0
    while degrees <= 2 * m.pi:
        circle.append([a + m.cos(degrees) * r, b + m.sin(degrees) * r])
        degrees += 1 / (r * scale)
    return circle


# y = c / x
# return hyperbole = [[x, y] ...]
def build_start_hyperbole(c, scale, max_x):
    hyperbole = list()
    x = 1 / scale
    while x <= max_x:
        hyperbole.append([x, c / x])
        x += 1 / scale

    return hyperbole


# (x + a)**2 + (y + b)**2 = r**2
# y = c / x
# return figure = [[x, y] ...]
def get_start_filling_figure(hyperbole_points, circle_points, a, b, r, c):
    figure = list()
    # часть гиперболы которая формирует фигуру
    figure.extend(list(filter(lambda point: (point[0] - a) ** 2 + (point[1] - b) ** 2 <= r ** 2
                                            and point[1] >= c / point[0], hyperbole_points)))
    # часть окружности которая формирует фигуру
    circle_part = list(filter(lambda point: (point[0] - a) ** 2 + (point[1] - b) ** 2 <= r ** 2
                                            and point[1] >= c / point[0], circle_points))
    if len(circle_part) > 0:
        ind_reverse = -1
        while circle_part[ind_reverse - 1][0] - circle_part[ind_reverse][0] < 0 and -ind_reverse < len(circle_part):
            ind_reverse -= 1
        ind_reverse += 1
        if -ind_reverse < len(circle_part):
            circle_part = circle_part[ind_reverse:] + circle_part[:ind_reverse]

        figure.extend(circle_part)

    return figure


# Сдвигает точки фигуры на dx dy
# return figure
def shift(dx, dy, figure):
    figure = list(map(lambda p: [p[0] + dx, p[1] + dy], figure))
    return figure


# Вращает точки фигуры на angle (в градусах), относительно точки cx, cy
# return figure
def rotate(cx, cy, angle, figure):
    rad_angle = m.radians(angle)
    for i in range(len(figure)):
        x, y = figure[i]
        x -= cx
        y -= cy
        new_x = x * m.cos(rad_angle) - y * m.sin(rad_angle)
        new_y = x * m.sin(rad_angle) + y * m.cos(rad_angle)
        figure[i] = [new_x + cx, new_y + cy]

    return figure


def scaling(cx, cy, kx, ky, figure):
    for i in range(len(figure)):
        x, y = figure[i]
        x -= cx
        y -= cy
        x *= kx
        y *= ky
        figure[i] = [x + cx, y + cy]

    return figure
