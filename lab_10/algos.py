import numpy as np
from canvas import Canvas
from transfom import transform, get_scale_param_and_mid


# Подпрограмма вычисляет пересечение с горизонтом.
# Вычисляет пересечение 2х отрезков прямых
def Intersection(x1, y1, x2, y2, arr):
    dx = x2 - x1
    dyc = y2 - y1
    dyp = arr[x2] - arr[x1]
    if dx == 0:
        xi = x2
        yi = arr[x2]
        return xi, yi
    if y1 == arr[x1] and y2 == arr[x2]:
        return x1, y1
    m = dyc / dx
    xi = x1 - round(dx * (y1 - arr[x1]) / (dyc - dyp))
    yi = round((xi - x1) * m + y1)
    return xi, yi


# Подпрограмма, определяющая видимость точки по отношению к верхнему и нижнему горизонту
# 0 - невидима.
# 1 - выше верхнего.
# -1 - ниже нижнего.
def Visible(x, y, top, bottom):
    # Если точка, ниже нижнего горизонта (или на нем). То она видима.
    if y <= bottom[x]:
        return -1
    # Если точка выше верхнего горизонта (или на нем). То она видима.
    if y >= top[x]:
        return 1
    return 0


# Подпрограмма заполнения массивов плавающих горизонтов между x1 и x2
# На основе линейной интерполяции.
def Horizon(x1, y1, x2, y2, top, bottom):
    if x2 - x1 == 0:    # Проверка вертикальности наклона.
        top[x2] = max(top[x2], y2)
        bottom[x2] = min(bottom[x2], y2)
        return
    # Вычисляем наклон.
    m = (y2 - y1) / (x2 - x1)
    # Движемся по x с шагом 1, чтобы заполнить
    # Массивы от x1 до x2.
    for x in range(x1, x2 + 1):
        y = round(m * (x - x1) + y1)
        top[x] = max(top[x], y)
        bottom[x] = min(bottom[x], y)


# Функция обработки и обновления точек бокового рёбра
def Side(x, y, x_edge, y_edge, canvas: Canvas, top, bottom):
    if (x_edge != -1):
        # Если кривая не первая
        # canvas.draw_line(x_edge, y_edge, x, y)
        Horizon(x_edge, y_edge, x, y, top, bottom)
    x_edge = x
    y_edge = y
    return x_edge, y_edge


def FloatHorizon(x_min, x_max, x_step, z_min, z_max, z_step, canvas: Canvas, func, angles):
    scale_param, mid = get_scale_param_and_mid(x_min, x_max, x_step, func, z_min, z_max, z_step, angles, canvas.width, canvas.height)
    print('width, height: ', canvas.width, canvas.height)
    print(f'scale_param = {scale_param}')

    x_left, y_left = -1, -1
    x_right, y_right = -1, -1

    # Инициализируем начальными значениями массивы горизонтов.
    top = [0] * canvas.width  # Верхний.
    bottom = [canvas.height] * canvas.width  # Нижний.

    for z in np.arange(z_max, z_min, -z_step):
        # инициализация предыдущих значений по x и y
        x_prev = x_min
        y_prev = func(x_min, z)
        # использование видового преобразования
        x_prev, y_prev = transform(x_prev, y_prev, z, angles, scale_param, mid, canvas.width, canvas.height)

        flag_prev = Visible(x_prev, y_prev, top, bottom)
        #
        x_left, y_left = Side(x_prev, y_prev, x_left, y_left, canvas, top, bottom)
        for x in np.arange(x_min, x_max, x_step):
            y_curr = func(x, z)
            x_curr, y_curr = transform(x, y_curr, z, angles, scale_param, mid, canvas.width, canvas.height)
            # Проверка видимости текущей точки.
            flag_curr = Visible(x_curr, y_curr, top, bottom)
            # Равенство флагов означает, что обе точки находятся
            # Либо выше верхнего горизонта, либо ниже нижнего,
            # Либо обе невидимы.
            if flag_curr == flag_prev:
                # Если текущая вершина выше верхнего горизонта или ниже нижнего (Предыдущая такая же)
                if flag_curr != 0:
                    # Значит отображаем отрезок от предыдущей до текущей.
                    canvas.draw_line(x_prev, y_prev, x_curr, y_curr)
                    # заполненяем массив плавающих горизонтов между x_prev и x_curr
                    Horizon(x_prev, y_prev, x_curr, y_curr, top, bottom)
                    # canvas.draw_line(x_prev, top[x_prev], x_curr, top[x_curr], True)  ####################
                # flag_curr == 0 означает, что и flag_prev == 0,
                # А значит часть от flag_curr до flag_prev невидима. Ничего не делаем.
            else:
                # Если видимость изменилась. Вычисляем пересечение.
                if flag_curr == 0:  # curr точка видима
                    if flag_prev == 1:
                        # Сегмент "входит" в верхний горизонт. Ищем пересечение с верхним горизонтом.
                        xi, yi = Intersection(x_prev, y_prev, x_curr, y_curr, top)
                    else:  # flag_prev == -1 (flag_prev нулю (0) не может быть равен, т.к. мы обработали это выше).
                        # Сегмент "входит" в нижний горизонт. Ищем пересечение с нижним горизонтом.
                        xi, yi = Intersection(x_prev, y_prev, x_curr, y_curr, bottom)
                    # Отображаем сегмент, от предыдущей точки, до пересечения.
                    canvas.draw_line(x_prev, y_prev, xi, yi)
                    Horizon(x_prev, y_prev, xi, yi, top, bottom)
                else:
                    if flag_curr == 1:
                        if flag_prev == 0:
                            # Сегмент "выходит" из верхнего горизонта. Ищем пересечение с верхним горизонтом.
                            xi, yi = Intersection(x_prev, y_prev, x_curr, y_curr, top)
                            # Отображаем сегмент от пересечения до текущей точки.
                            canvas.draw_line(xi, yi, x_curr, y_curr)
                            Horizon(xi, yi, x_curr, y_curr, top, bottom)
                        else:  # flag_prev == -1
                            # Сегмент начинается с точки, ниже нижнего горизонта
                            # И заканчивается в точке выше верхнего горизонта.
                            # Нужно искать 2 пересечения.
                            # Первое пересечение с нижним горизонтом.
                            xi, yi = Intersection(x_prev, y_prev, x_curr, y_curr, bottom)
                            # Отображаем сегмент от предыдущей то пересечения.
                            canvas.draw_line(x_prev, y_prev, xi, yi)
                            Horizon(x_prev, y_prev, xi, yi, top, bottom)
                            # Второе пересечение с верхним горизонтом.
                            xi, yi = Intersection(x_prev, y_prev, x_curr, y_curr, top)
                            # Отображаем сегмент от пересечения до текущей.
                            canvas.draw_line(xi, yi, x_curr, y_curr)
                            Horizon(xi, yi, x_curr, y_curr, top, bottom)
                    else:  # flag_curr == -1
                        if flag_prev == 0:
                            # Сегмент "выходит" из нижнего горизонта.
                            # Ищем пересечение с нижним горизонтом.
                            xi, yi = Intersection(x_prev, y_prev, x_curr, y_curr, bottom)
                            canvas.draw_line(xi, yi, x_curr, y_curr)
                            Horizon(xi, yi, x_curr, y_curr, top, bottom)
                        else:
                            # Сегмент начинается с точки, выше верхнего горизонта
                            # И заканчивается в точке ниже нижнего горизонта.
                            # Нужно искать 2 пересечения.
                            # Первое пересечение с верхним горизонтом.
                            xi, yi = Intersection(x_prev, y_prev, x_curr, y_curr, top)
                            # Отображаем сегмент от предыдущей до пересечения.
                            canvas.draw_line(x_prev, y_prev, xi, yi)
                            Horizon(x_prev, y_prev, xi, yi, top, bottom)
                            # Ищем второе пересечение с нижним горизонтом.
                            xi, yi = Intersection(x_prev, y_prev, x_curr, y_curr, bottom)
                            # Отображаем сегмент от пересечения до текущей.
                            canvas.draw_line(xi, yi, x_curr, y_curr)
                            Horizon(xi, yi, x_curr, y_curr, top, bottom)
            x_prev, y_prev = x_curr, y_curr
            flag_prev = flag_curr

        x_right, y_right = Side(x_prev, y_prev, x_right, y_right, canvas, top, bottom)



