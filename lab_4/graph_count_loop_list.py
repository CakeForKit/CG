from graph_time_measure import *


def graph_loops():
    def newCanvas():
        return QImage(CANVAS_WIDTH, CANVAS_HEIGHT, QImage.Format_ARGB32)

    canvas = newCanvas()
    color = QColor(0, 0, 0)
    xc = round(CANVAS_WIDTH // 2)
    yc = round(CANVAS_HEIGHT // 2)
    center = Point(xc, yc)

    count_loop_list = []
    count_loop = []

    for algos in [canonic_eq, param_eq, alg_midpoint, brezenhem]:
        ra = STEP
        rb = STEP * RB_RA

        # count = algos(ra, rb, center, canvas, color, False, count_loop=SHOW_LOOPS)
        # count_loop.append(count)

        for j in range(MAX_RADIUS // STEP):
            count = algos(ra, rb, center, canvas, color, False, count_loop=True)
            count_loop.append(count)

            rb += STEP * RB_RA
            ra += STEP

            canvas = newCanvas()
        count_loop_list.append(count_loop)
        print(count_loop, algos.__name__)
        count_loop = []

    radius_arr = list(i for i in range(STEP, MAX_RADIUS + STEP, STEP))

    title = f"Замеры количества заходов в цикл для эллипса"
    title += f' rb/ra = {RB_RA}.\n'

    plt.figure(figsize=(9, 7))
    plt.rcParams['font.size'] = '15'
    plt.title(title)

    plt.plot(radius_arr, count_loop_list[0], label='Каноническое уравнение')
    plt.plot(radius_arr, count_loop_list[1], label='Параметрическое уравнение')
    plt.plot(radius_arr, count_loop_list[2], label='Алгоритм средней точки')
    plt.plot(radius_arr, count_loop_list[3], label='Алгоритм Брезенхема')

    plt.xticks(np.arange(STEP, MAX_RADIUS + STEP, STEP))
    plt.legend()
    plt.xlabel("Длина радиуса")
    plt.ylabel("Количество")

    plt.show()

if __name__ == '__main__':
    graph_loops()