from Point import Point
from algos import dda, brez_int, brez_float, brez_smooth, wu, lib
import matplotlib.pyplot as plt
import math as m

LENGTH = 1000


def StepGraph():
    # fig = plt.figure("Исследование ступенчатости алгоритмов построение.", figsize=(18, 10))
    grad_angle = 0
    step = 2
    p1 = Point(0, 0)
    p2 = Point(p1.x, p1.y + LENGTH)

    angles = []
    DDA_steps = []
    BrezenhemInteger_steps = []
    BrezenhemFloat_steps = []
    BrezenhemSmooth_steps = []
    VU_steps = []

    for j in range(90 // step):
        DDA_steps.append(dda(p1, p2, count_steps=True))
        BrezenhemInteger_steps.append(brez_int(p1, p2, count_steps=True))
        BrezenhemFloat_steps.append(brez_float(p1, p2, count_steps=True))
        BrezenhemSmooth_steps.append(brez_smooth(p1, p2, count_steps=True))
        VU_steps.append(wu(p1, p2, count_steps=True))

        x = LENGTH * m.cos(m.radians(grad_angle)) + p1.x
        y = LENGTH * m.sin(-m.radians(grad_angle)) + p1.y
        p2 = Point(round(x), round(y))
        angles.append(grad_angle)
        grad_angle += step

    plt.figure(figsize=(14, 8), dpi=200)
    # plt.subplots_adjust(left=0, right=0.1, top=0, bottom=0.1)
    plt.subplots_adjust(
        top=0.956,
        bottom=0.074,
        left=0.042,
        right=0.981,
        hspace=0.2,
        wspace=0.2
    )
    plt.subplot(2, 3, 1)
    plt.title("ЦДА")
    plt.plot(angles, DDA_steps)
    plt.xticks(list(range(0, 91, 5)))
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.subplot(2, 3, 2)
    plt.title("BУ")
    plt.plot(angles, VU_steps)
    plt.xticks(list(range(0, 91, 5)))
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.subplot(2, 3, 3)
    plt.title("Брензенхем с действительными коэффицентами")
    plt.plot(angles, BrezenhemFloat_steps)
    plt.xticks(list(range(0, 91, 5)))
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.subplot(2, 3, 4)
    plt.title("Брензенхем с целыми коэффицентами")
    plt.plot(angles, BrezenhemInteger_steps)
    plt.xticks(list(range(0, 91, 5)))
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.subplot(2, 3, 5)
    plt.title("Брензенхем с устр. ступенчатости")
    plt.plot(angles, BrezenhemSmooth_steps)
    plt.xticks(list(range(0, 91, 5)))
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.figure(figsize=(9, 7), dpi=200)
    plt.subplot(111)
    plt.plot(angles, DDA_steps, label='ЦДА')
    plt.plot(angles, BrezenhemInteger_steps, '--', label="Брензенхем с целыми коэффицентами")
    plt.plot(angles, BrezenhemFloat_steps, '.', label="Брензенхем с действительными коэффицентами")
    plt.plot(angles, BrezenhemSmooth_steps, '>', label="Брензенхем с устр\nступенчатости")
    plt.plot(angles, VU_steps, '-.', label="By")
    plt.title(f"Исследование ступенчатости.\n{LENGTH} - длина отрезка")
    plt.xticks(list(range(0, 91, 5)))
    plt.legend()
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.show()

