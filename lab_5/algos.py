from PyQt5.QtGui import QImage, QPainter, QPen, QColor
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication

from figure import *
from structs import *
import time

DEBUG = False


def round(n):
    return int(n + 0.5)


def make_edges_list(figures):
    edges = list()
    for fig in figures:
        len_points_arr = len(fig)
        for i in range(len_points_arr):
            if i + 1 > len_points_arr - 1:
                edges.append([fig[-1], fig[0]])
            else:
                edges.append([fig[i], fig[i + 1]])

    return edges


def find_extrimum_Y_figures(figures):
    yMin = figures[0][0].y
    yMax = figures[0][0].y
    for fig in figures:
        for p in fig:
            if p.y > yMax:
                yMax = p.y
            if p.y < yMin:
                yMin = p.y
    return yMin, yMax


# {y: (x, dx, dy), ...}
def make_link_list(Ymin, Ymax):
    link_list = dict()
    for i in range(round(Ymax), round(Ymin), -1):
        link_list.update({i: list()})
    return link_list


def fill_y_group(y_groups, x_start, y_start, x_end, y_end):
    # delta_y > 0 всегда
    if y_start > y_end:
        x_end, x_start = x_start, x_end
        y_end, y_start = y_start, y_end

    delta_y = y_end - y_start
    if delta_y != 0:
        delta_x = -(x_end - x_start) / delta_y
        if y_end not in y_groups:
            y_groups[y_end] = [Node(x_end, delta_x, delta_y)]
        else:
            y_groups[y_end].append(Node(x_end, delta_x, delta_y))


def iterate_active_edges(active_edges):
    i = 0
    while i < len(active_edges):
        active_edges[i].x += active_edges[i].dx
        active_edges[i].dy -= 1
        if active_edges[i].dy < 1:
            active_edges.pop(i)
        else:
            i += 1


def add_active_edges(y_groups, active_edges, y):
    if y in y_groups:
        for y_group in y_groups.get(y):
            active_edges.append(y_group)
    active_edges.sort(key=lambda edge: edge.x)


def draw_act(qp, active_edges, y, colour):
    len_edge = len(active_edges)
    for i in range(0, len_edge, 2):
        try:
            p1, p2 = (round(active_edges[i].x), y), (round(active_edges[i + 1].x), y)
        except:
            p1, p2 = (round(active_edges[i].x), y), (round(active_edges[i - 1].x), y)

        qp.drawLine(*p1, *p2)
        if DEBUG:
            print(f'draw_act: {p1}, ({p2})')


def alg_fill_solid_areas_ordered_list_CAP(canvas_struct, figures, colour=QColor(0, 0, 0), delay=False):
    # canvas = canvas_struct.img
    qp = QPainter(canvas_struct.img)
    qp.setPen(QPen(colour, 1))

    edges = make_edges_list(figures)
    if DEBUG:
        print("Все рёбра всех фигур: (make_edges_list)")
        for edge in edges:
            print(edge)

    ymin, ymax = find_extrimum_Y_figures(figures)
    if DEBUG:   print(f'ymin, ymax = {ymin}, {ymax}')
    y_groups = make_link_list(ymin, ymax)
    for edge in edges:
        fill_y_group(y_groups, edge[0].x, edge[0].y, edge[1].x, edge[1].y)

    if DEBUG:
        print(f'make_link_list (y_groups)')
        for k, v in y_groups.items():
            print(f'{k}: {v}')
        # print(y_groups)

    y_end = ymax
    y_start = ymin
    active_edges = []
    while y_end > y_start:
        iterate_active_edges(active_edges)
        add_active_edges(y_groups, active_edges, y_end)

        if DEBUG:
            print("Len egde:", len(active_edges))
            e = 1
            for i in active_edges:
                print("   ", e, ")", i)
                e += 1
        draw_act(qp, active_edges, y_end, colour)
        y_end -= 1
        if delay:
            time.sleep(1e-20)
            pmp = QPixmap.fromImage(canvas_struct.img)
            canvas_struct.label.setPixmap(pmp)
            QApplication.processEvents()

    draw_edges(canvas_struct.img, edges)
