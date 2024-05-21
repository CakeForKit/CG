import time
from matplotlib import pyplot as plt
import numpy as np
from PyQt5.QtGui import QImage
from algos import canonic_eq, param_eq, brezenhem, alg_midpoint
from Point import *

CANVAS_WIDTH = 5000
CANVAS_HEIGHT = 5000
NUMBER_OF_RUNS = 200
MAX_RADIUS = 3000
RB_RA = 0.5
STEP = 300
NS_TO_MKS = 1e-6


def time_comparison(circle=True):
    def newCanvas():
        return QImage(CANVAS_WIDTH, CANVAS_HEIGHT, QImage.Format_ARGB32)

    canvas = newCanvas()
    color = QColor(0, 0, 0)
    time_list = []

    xc = round(CANVAS_WIDTH // 2)
    yc = round(CANVAS_HEIGHT // 2)
    center = Point(xc, yc)

    for algos in [canonic_eq, param_eq, alg_midpoint, brezenhem]:
        time_start = [0] * (MAX_RADIUS // STEP)
        time_end   = [0] * (MAX_RADIUS // STEP)
        # count_loop = []

        for _ in range(NUMBER_OF_RUNS):
            ra = STEP
            rb = STEP * RB_RA

            # count = algos(ra, rb, center, canvas, color, False, count_loop=SHOW_LOOPS)
            # count_loop.append(count)

            for j in range(MAX_RADIUS // STEP):
                if circle:
                    time_start[j] += time.time_ns()
                    algos(ra, ra, center, canvas, color, False)
                    time_end[j] += time.time_ns()
                else:
                    time_start[j] += time.time_ns()
                    algos(ra, rb, center, canvas, color, False)
                    time_end[j] += time.time_ns()


                    rb += STEP * RB_RA

                ra += STEP

            canvas = newCanvas()

        size = len(time_start)
        res_time = list(NS_TO_MKS * (time_end[i] - time_start[i]) / (NUMBER_OF_RUNS - 2) for i in range(size))
        time_list.append(res_time)

        # count_loop_list.append(list(count_loop[i] for i in range(size)))

    radius_arr = list(i for i in range(STEP, MAX_RADIUS + STEP, STEP))

    if circle:
        return radius_arr, time_list
    else:
        return radius_arr, time_list
    # figure = "окружности"
    # if not circle:
    #     figure = "эллипса"
    #
    # plt.figure(figsize = (17, 11))
    # plt.rcParams['font.size'] = '20'
    # title = f"Замеры времени для построения {figure}"
    # if not circle:
    #     title += f' rb/ra = {RB_RA}.\n'
    # else:
    #     title += f'.\n'
    # plt.title(title)
    #
    # plt.plot(radius_arr, time_list[0], label='Каноническое уравнение')
    # plt.plot(radius_arr, time_list[1], label='Параметрическое уравнение')
    # plt.plot(radius_arr, time_list[2], label='Алгоритм средней точки')
    # plt.plot(radius_arr, time_list[3], label='Алгоритм Брезенхема')
    #
    # plt.xticks(np.arange(STEP, MAX_RADIUS + STEP, STEP))
    # plt.legend()
    # plt.xlabel("Длина радиуса")
    # plt.ylabel("Время, с")
    #
    # plt.show()


def ellipse_graph_show(radius_arr, time_list):
    figure = "эллипса"
    title = f"Замеры времени для построения {figure}"
    title += f' rb/ra = {RB_RA}.\n'

    plt.figure(figsize=(17, 11))
    plt.rcParams['font.size'] = '20'
    plt.title(title)

    plt.plot(radius_arr, time_list[0], label='Каноническое уравнение')
    plt.plot(radius_arr, time_list[1], label='Параметрическое уравнение')
    plt.plot(radius_arr, time_list[2], label='Алгоритм средней точки')
    plt.plot(radius_arr, time_list[3], label='Алгоритм Брезенхема')

    plt.xticks(np.arange(STEP, MAX_RADIUS + STEP, STEP))
    plt.legend()
    plt.xlabel("Длина радиуса")
    plt.ylabel("Время, мкс")

    plt.show()


def circle_graph_show(radius_arr, time_list):
    figure = "окружности"
    title = f"Замеры времени для построения {figure}"
    title += f'.\n'

    plt.figure(figsize=(17, 11))
    plt.rcParams['font.size'] = '20'
    plt.title(title)

    plt.plot(radius_arr, time_list[0], label='Каноническое уравнение')
    plt.plot(radius_arr, time_list[1], label='Параметрическое уравнение')
    plt.plot(radius_arr, time_list[2], label='Алгоритм средней точки')
    plt.plot(radius_arr, time_list[3], label='Алгоритм Брезенхема')

    plt.xticks(np.arange(STEP, MAX_RADIUS + STEP, STEP))
    plt.legend()
    plt.xlabel("Длина радиуса")
    plt.ylabel("Время, мкс")

    plt.show()