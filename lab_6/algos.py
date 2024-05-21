from PyQt5.QtGui import QImage, QPainter, QPen, QColor
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication

from figure import *
from structs import *
from canvas import *
import time

DEBUG = False


def line_by_line_filling_algorithm_with_seed(canvas, border_colour: QColor, fill_colour: QColor,
                                             seed_point: Point, delay=False):
    print("fill_c = ", fill_colour.getRgb())
    print("border_c = ", border_colour.getRgb())

    stack = [seed_point]
    while stack:
        seed_pixel = stack.pop()
        x, y = seed_pixel.get_xy()
        canvas.set_pixel_color(x, y, fill_colour)
        tx, ty = x, y

        # заполняем интервал справа от затравки
        x += 1
        while (canvas.get_pixel_color(x, y) != border_colour and
               canvas.get_pixel_color(x, y) != fill_colour and x < canvas.width):
            canvas.set_pixel_color(x, y, fill_colour)
            x += 1
        xright = x - 1

        # заполняем интервал слева от затравки
        x = tx - 1
        while (canvas.get_pixel_color(x, y) != border_colour and
               canvas.get_pixel_color(x, y) != fill_colour and x >= 0):
            canvas.set_pixel_color(x, y, fill_colour)
            x -= 1
        xleft = x + 1

        # Проход по верхней строке
        x = xleft
        if ty < canvas.height:
            y = ty + 1

            while x <= xright:
                flag = False

                # идем до конца данного интервала по x
                # если при (xleft, y + 1) внутренняя часть то True
                # x = самый правый x в данной группе
                while (canvas.get_pixel_color(x, y) != border_colour and
                       canvas.get_pixel_color(x, y) != fill_colour and x <= xright):
                    flag = True
                    x += 1

                # Помещаем в стек крайний справа пиксель
                if flag:
                    # если это xright
                    if x == xright and canvas.get_pixel_color(x, y) != border_colour and \
                            canvas.get_pixel_color(x, y) != fill_colour:
                        if y < canvas.height:
                            stack.append(Point(x, y))
                    else:
                        if y < canvas.height:
                            stack.append(Point(x - 1, y))

                # Идем вправо по x если внутренний интервал был прерван
                x_in = x
                while (canvas.get_pixel_color(x, y) == fill_colour or
                       canvas.get_pixel_color(x, y) == border_colour) and x < xright:
                    x = x + 1

                if x == x_in:
                    x += 1

        # Проход по нижней строке
        x = xleft
        y = ty - 1

        while x <= xright:
            flag = False

            # ищем самый правый пиксель по x внутри интервала
            while canvas.get_pixel_color(x, y) != border_colour and \
                    canvas.get_pixel_color(x, y) != fill_colour and x <= xright:
                flag = True
                x += 1

            # Помещаем в стек крайний справа пиксель
            if flag:
                if x == xright and canvas.get_pixel_color(x, y) != border_colour and \
                        canvas.get_pixel_color(x, y) != fill_colour:
                    if y > 0:
                        stack.append(Point(x, y))
                else:
                    if y > 0:
                        stack.append(Point(x - 1, y))

                flag = False

            # Продолжаем проверку, если интервал был прерван
            # X = левый пиксель из следующего интервала
            x_in = x
            while (canvas.get_pixel_color(x, y) == fill_colour or
                   canvas.get_pixel_color(x, y) == border_colour) and x < xright:
                x = x + 1

            # если правее нет нового интервала
            if x == x_in:
                x += 1

        if delay:
            time.sleep(1e-20)
            canvas.import_img()

    canvas.import_img()
