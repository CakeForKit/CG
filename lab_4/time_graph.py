from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtGui import QColor, QPainter, QPen
from Point import Point
from figure import FigureSpec
from algos import dda, brez_int, brez_float, brez_smooth, wu, lib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import time

LENGTH = 1000
ANGLE = 10
NSEC_IN_SEC = 1e9


def get_time_algos(algos):
    ts = time.time_ns()
    FigureSpec(LENGTH, ANGLE, Point(LENGTH, LENGTH), algos, QColor(0, 0, 0))
    te = time.time_ns()

    return te - ts


class TimeGraphWidget(FigureCanvasQTAgg):
    def __init__(self, label):
        super().__init__()
        self.label = label
        self.setGeometry(200, 200, 2000, 1200)

        self.fig = Figure(figsize=(9, 7), dpi=200)
        super(TimeGraphWidget, self).__init__(self.fig)

        self.show_graph()

    def show_graph(self):
        algos = [dda, brez_int, brez_float, brez_smooth, wu]
        x = [f.__name__ for f in algos]
        x = ['ЦДА', 'Брезенхем с\nцелочисленными\nданными', 'Брезенхем с\nдействительными\nданными',
             'Брезенхем с\nустранением\nступенчатости', 'Ву']
        xnum = list(range(1, len(algos) + 1))
        y = [get_time_algos(f) / NSEC_IN_SEC for f in algos]
        print(f'x = {x}')
        print(f'y = {y}')

        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.bar(x=xnum, height=y, width=0.6)
        self.ax.set_xticks(xnum, labels=x)
        self.ax.set_ylabel('Секунды')
        self.ax.set_title('Исследование времени работы алгоритмов построения')
        self.draw()
        # bargraph = pg.BarGraphItem(x=xnum, height=y, width=0.6)
        # self.plot_graph.addItem(bargraph)
