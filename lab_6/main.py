import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from info import InfoWidget
from canvas import Canvas
from structs import *
from figure import *
from errs import Errors_my, BaseErr

NS_TO_MS = 1e3  # 1e-3

DEBUG = True

COLORS = {
    'black': QColor(236, 229, 255),
    'white': QColor(255, 255, 255),
    'yellow': QColor(255, 255, 102),
    'red': QColor(255, 101, 101),
    'blue': QColor(106, 243, 255),
    'green': QColor(93, 186, 0)
}

INV_COLORS = {
    'black': QColor(0, 0, 0),
    # 'white': QColor(255, 255, 255),
    'yellow': QColor(0, 0, 255),
    'red': QColor(90, 255, 140),
    'blue': QColor(255, 0, 0),
    'green': QColor(255, 0, 255),
}


# print(list(map(lambda x: x.getRgb(), INV_COLORS.values())))


class MainWindow(QMainWindow):  # , Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # self.setupUi(self)
        uic.loadUi('main_window.ui', self)
        width, height = 2500, 1500
        self.setGeometry(50, 50, width, height)

        self.background_color = COLORS['white']
        self.brush_color = COLORS['red']
        self.line_colour = INV_COLORS['black']
        self.canvas = Canvas(self.canvas_lbl, self.background_color)

        self.openfigure = OpenFigure(self.line_colour)
        self.change_brush_color(self.brush_color)
        self.change_line_color(self.line_colour)

        self.seed_point = list()

        self.color_btns_clicked()
        self.line_color_btns_clicked()
        self.clear_canvas_btn.clicked.connect(self.clear_canvas)
        self.add_point_btn.clicked.connect(self.add_point_by_btn)
        self.add_seed_btn.clicked.connect(self.add_seed_point_by_btn)
        self.close_figure_btn.clicked.connect(self.close_figure)
        self.fill_figures_btn.clicked.connect(self.fill_figures)

        # меню
        self.info_widget = InfoWidget()
        self.info_qm.aboutToShow.connect(self.show_info)
        self.exit_pbtn.aboutToShow.connect(self.exit)
        ##
        self.update()

        # self.add_point(100, 100)

    def is_in_label(self, p):
        rect_lbl = self.canvas_lbl.geometry()
        if rect_lbl.contains(p.x, p.y):
            mb = self.menubar.geometry()
            p.x -= rect_lbl.x()
            p.y -= rect_lbl.y() + mb.height()

            return True
        return False

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            p = Point(event.x(), event.y())
            if self.is_in_label(p):
                event.accept()
                self.add_point(*p.get_xy())
        elif event.buttons() == Qt.RightButton:
            p = Point(event.x(), event.y())
            if self.is_in_label(p):
                event.accept()
                self.add_seed_point(*p.get_xy())
        elif event.buttons() == Qt.MiddleButton:
            self.close_figure()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            p = Point(event.x(), event.y())
            if self.is_in_label(p):
                event.accept()
                self.add_point(*p.get_xy())

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.RightButton:
            self.fill_figures()

    def update(self) -> None:
        print('update main_window')

        self.canvas.update()
        # self.openfigure.draw(self.canvas)
        #
        self.canvas.import_img()
        self.print_figures_data()

    def fill_figures(self):
        # self.canvas.colour = self.brush_color
        # delay = self.choose_delay()
        # self.canvas.fill_all_figures(self.brush_color, self.line_colour, delay)
        if len(self.seed_point) == 0:
            errm = Errors_my(ErrNoSeedPoint.text())
            errm.show()
            return
        delay = self.choose_delay()
        time = self.canvas.fill_all_figures(self.brush_color, self.line_colour, self.seed_point.pop(), delay)

        # self.canvas.update()

        if time == -1:
            self.time_le.setText(f'-')
        else:
            self.time_le.setText(f'{time * NS_TO_MS:.1f}')
        # self.openfigure.draw(self.canvas)
        # pmp = QPixmap.fromImage(self.canvas.img)
        # self.canvas_lbl.setPixmap(pmp)

    def add_point(self, x, y):
        p = Point(x, y)
        if p in self.openfigure.points:
            errm = Errors_my(ErrPointExistInFigure.text())
            errm.show()
            return
        self.openfigure.add_point(p)
        # self.openfigure.add_point_draw(p, self.canvas)
        self.openfigure.draw(self.canvas)
        self.print_figures_data()

    def add_seed_point(self, x, y):
        p = Point(x, y)
        self.seed_point = [p]
        self.canvas.draw_seed_point(*p.get_xy(), self.brush_color)
        self.canvas.import_img()

    def add_seed_point_by_btn(self):
        x = self.x_sp.value()
        y = self.y_sp.value()
        self.add_seed_point(x, y)

    def add_point_by_btn(self):
        x = self.x_sp.value()
        y = self.y_sp.value()
        self.add_point(x, y)

    def close_figure(self):
        if not self.openfigure.can_close():
            errm = Errors_my(ErrCanNotCloseFigure.text())
            errm.show()
            return

        cf = Figure(self.openfigure, self.line_colour)
        self.openfigure = OpenFigure(self.line_colour)
        self.canvas.add_figure(cf)

        self.canvas.draw_figure(cf)
        self.print_figures_data()
        # self.update()

    def print_figures_data(self):
        text = self.canvas.get_text_figures_data()
        text += f'{" " * 6}OpenFigure{" " * 6}\n' + self.openfigure.get_text_points()
        self.points_textEdit.setPlainText(text)

    def choose_delay(self):
        if self.delay_rbn.isChecked():
            print("with delay")
            return True
        else:
            print('NO delay')
            return False

    def color_btns_clicked(self):
        self.black_brush_btn.clicked.connect(self.change_brush_color_to_black)
        self.yellow_brush_btn.clicked.connect(self.change_brush_color_to_yellow)
        self.red_brush_btn.clicked.connect(self.change_brush_color_to_red)
        self.blue_brush_btn.clicked.connect(self.change_brush_color_to_blue)
        self.green_brush_btn.clicked.connect(self.change_brush_color_to_green)

    def change_brush_color(self, color):
        print(f'change_brush_color to {color.getRgb()}')
        self.color_brush_show.setStyleSheet(f"background-color: {color.name()}")
        self.brush_color = color
        # self.update()

    def change_brush_color_to_black(self):
        self.change_brush_color(COLORS['black'])

    def change_brush_color_to_yellow(self):
        self.change_brush_color(COLORS['yellow'])

    def change_brush_color_to_red(self):
        self.change_brush_color(COLORS['red'])

    def change_brush_color_to_blue(self):
        self.change_brush_color(COLORS['blue'])

    def change_brush_color_to_green(self):
        self.change_brush_color(COLORS['green'])

    def line_color_btns_clicked(self):
        self.inv_black_line_btn.clicked.connect(self.change_line_color_to_black)
        self.inv_yellow_line_btn.clicked.connect(self.change_line_color_to_yellow)
        self.inv_red_line_btn.clicked.connect(self.change_line_color_to_red)
        self.inv_blue_line_btn.clicked.connect(self.change_line_color_to_blue)
        self.inv_green_line_btn.clicked.connect(self.change_line_color_to_green)

    def change_line_color(self, color):
        print(f'change_line_color to {color.getRgb()}')
        self.color_line_show.setStyleSheet(f"background-color: {color.name()}")
        self.line_colour = color
        self.openfigure.line_colour = color
        self.openfigure.draw(self.canvas)
        # self.update()

    def change_line_color_to_black(self):
        self.change_line_color(INV_COLORS['black'])

    def change_line_color_to_yellow(self):
        self.change_line_color(INV_COLORS['yellow'])

    def change_line_color_to_red(self):
        self.change_line_color(INV_COLORS['red'])

    def change_line_color_to_blue(self):
        self.change_line_color(INV_COLORS['blue'])

    def change_line_color_to_green(self):
        self.change_line_color(INV_COLORS['green'])

    def clear_canvas(self):
        print('clear_canvas')
        self.openfigure = OpenFigure(self.line_colour)
        self.canvas.clear_canvas()
        self.update()

    def show_info(self):
        print('show info')
        self.info_widget.show()

    def resizeEvent(self, event):
        self.update()

    def exit(self):
        sys.exit(0)


def exept_hooks(cls, exeption, trades):
    sys.__excepthook__(cls, exeption, trades)


if __name__ == '__main__':
    sys.excepthook = exept_hooks
    app = QApplication(sys.argv)
    main = MainWindow()
    main.update()
    main.show()
    sys.exit(app.exec())
