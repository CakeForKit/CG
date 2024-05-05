import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox)
from PyQt5.QtGui import QColor, QPixmap
from info import InfoWidget
from canvas import Canvas
from algos import (canonic_eq, param_eq, brezenhem, alg_midpoint, lib)
from figure import FigureCircle, FigureCircleSpec, FigureEllipse, FigureEllipseSpec, ERRS_FIGURE
from Point import Point
from errs import Errors_my
# from time_graph import TimeGraphWidget

# from main_window import Ui_MainWindow

DEBUG = True

COLORS = {
    'black': QColor(0, 0, 0),
    'white': QColor(255, 255, 255),
    'red': QColor(255, 101, 101),
    'blue': QColor(106, 243, 255),
    'green': QColor(93, 186, 0)
}


class MainWindow(QMainWindow):  # , Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # self.setupUi(self)
        uic.loadUi('main_window.ui', self)
        width, height = 2800, 1100
        self.setGeometry(50, 50, width, height)

        background_color = COLORS['white']
        self.line_color = COLORS['black']
        self.canvas = Canvas(self.canvas_lbl, background_color)
        self.change_line_color(self.line_color)

        self.color_btns_clicked()
        self.param_spectr_circle_gp.buttonClicked.connect(self.change_param_spectr_circle)
        self.set_center_btn.clicked.connect(self.set_center)
        self.draw_circle_btn.clicked.connect(self.draw_circle)
        self.draw_spec_circle_btn.clicked.connect(self.draw_spec_circle)
        self.draw_ellipse_btn.clicked.connect(self.draw_ellipse)
        self.draw_spec_ellipse_btn.clicked.connect(self.draw_spec_ellipse)

        self.cmp_time_circle_btn.clicked.connect(self.cmp_time_circle)
        self.cmp_time_ellipse_btn.clicked.connect(self.cmp_time_ellipse)
        self.clear_canvas_btn.clicked.connect(self.clear_canvas)

        # меню
        self.info_widget = InfoWidget()
        self.info_qm.aboutToShow.connect(self.show_info)
        self.exit_pbtn.aboutToShow.connect(self.exit)
        ##
        self.update()

    def update(self) -> None:
        print('update main_window')
        self.canvas.update()
        pmp = QPixmap.fromImage(self.canvas.img)
        self.canvas_lbl.setPixmap(pmp)

    def draw_circle(self):
        r = self.r_circle_dsp.value()
        cx = self.center_x_sp.value()
        cy = self.center_y_sp.value()
        center = Point(cx, cy)
        algos = self.choose_algos()
        print(f'draw_circle: ')

        fig = FigureCircle(algos, self.line_color, center, r)
        self.canvas.add_figure(fig)
        self.update()

    def draw_spec_circle(self):
        cx = self.center_x_sp.value()
        cy = self.center_y_sp.value()
        center = Point(cx, cy)
        algos = self.choose_algos()
        begr = self.beg_r_circle_dsp.value()
        endr = self.end_r_circle_dsp.value()
        step = self.step_circle_dsp.value()
        count = self.count_circle_dsp.value()
        if self.beg_r_circle_rb.isChecked():
            begr = 0
        elif self.end_r_circle_rb.isChecked():
            endr = 0
        elif self.step_circle_rb.isChecked():
            step = 0
        else:
            count = 0
        print(f'draw_spec_circle:')

        fig = FigureCircleSpec(algos, self.line_color, center, begr, endr, step, count)
        if fig.err != 0:
            err = Errors_my(ERRS_FIGURE[fig.err])
            err.show()
            return
        self.canvas.add_figure(fig)
        self.update()

    def draw_ellipse(self):
        rx = self.rx_ellipse_dsp.value()
        ry = self.ry_ellipse_dsp.value()
        cx = self.center_x_sp.value()
        cy = self.center_y_sp.value()
        center = Point(cx, cy)
        algos = self.choose_algos()
        print(f'draw_ellipse: ')

        fig = FigureEllipse(algos, self.line_color, center, rx, ry)
        self.canvas.add_figure(fig)
        self.update()

    def draw_spec_ellipse(self):
        cx = self.center_x_sp.value()
        cy = self.center_y_sp.value()
        center = Point(cx, cy)
        algos = self.choose_algos()
        beg_rx = self.beg_rx_ellipse_dsp.value()
        beg_ry = self.beg_ry_ellipse_dsp.value()
        step_rx = self.step_rx_ellipse_dsp.value()
        step_ry = self.step_ry_ellipse_dsp.value()
        count = self.count_ellipse_sp.value()
        print(f'draw_spec_ellipse: ')

        fig = FigureEllipseSpec(algos, self.line_color, center, beg_rx, beg_ry, step_rx, step_ry, count)
        self.canvas.add_figure(fig)
        self.update()

    def set_center(self):
        self.canvas.update()
        cx = self.canvas_lbl.size().width() // 2
        cy = self.canvas_lbl.size().height() // 2
        self.center_x_sp.setValue(cx)
        self.center_y_sp.setValue(cy)

    def change_param_spectr_circle(self):
        print(f'change_param_spectr_circle: ')
        for dsp in [self.beg_r_circle_dsp, self.end_r_circle_dsp, self.step_circle_dsp, self.count_circle_dsp]:
            dsp.setReadOnly(False)
            dsp.setStyleSheet('')

        if self.beg_r_circle_rb.isChecked():
            dsp = self.beg_r_circle_dsp
            print('beg_r_circle_dsp')
        elif self.end_r_circle_rb.isChecked():
            dsp = self.end_r_circle_dsp
            print('end_r_circle_dsp')
        elif self.step_circle_rb.isChecked():
            dsp = self.step_circle_dsp
            print('step_circle_dsp')
        else:
            dsp = self.count_circle_dsp
            print('count_circle_dsp')
        dsp.setReadOnly(True)
        dsp.setStyleSheet("background-color: rgb(191, 191, 191);\n")


    def choose_algos(self):
        if self.canon_eq_rb.isChecked():
            print('canon_eq_rb')
            algos = canonic_eq
        elif self.param_eq_rb.isChecked():
            print('param_eq_rb')
            algos = param_eq
        elif self.brez_rb.isChecked():
            print('brez_rb')
            algos = breakpoint
        elif self.mid_point_rb.isChecked():
            print('mid_point_rb')
            algos = alg_midpoint
        else:
            print('lib_rb')
            algos = lib

        return algos

    def color_btns_clicked(self):
        self.black_bg_btn.clicked.connect(self.change_background_color_to_black)
        self.white_bg_btn.clicked.connect(self.change_background_color_to_white)
        self.red_bg_btn.clicked.connect(self.change_background_color_to_red)
        self.blue_bg_btn.clicked.connect(self.change_background_color_to_blue)
        self.green_bg_btn.clicked.connect(self.change_background_color_to_green)

        self.black_line_btn.clicked.connect(self.change_line_color_to_black)
        self.white_line_btn.clicked.connect(self.change_line_color_to_white)
        self.red_line_btn.clicked.connect(self.change_line_color_to_red)
        self.blue_line_btn.clicked.connect(self.change_line_color_to_blue)
        self.green_line_btn.clicked.connect(self.change_line_color_to_green)

    def change_background_color(self, color):
        self.canvas.set_background_color(color)
        # self.background_color = color
        self.update()

    def change_line_color(self, color):
        print(f'change_line_color to {color.getRgb()}')
        self.color_line_show.setStyleSheet(f"background-color: {color.name()}")
        self.line_color = color
        self.update()

    def change_background_color_to_black(self):
        self.change_background_color(COLORS['black'])

    def change_background_color_to_white(self):
        self.change_background_color(COLORS['white'])

    def change_background_color_to_red(self):
        self.change_background_color(COLORS['red'])

    def change_background_color_to_blue(self):
        self.change_background_color(COLORS['blue'])

    def change_background_color_to_green(self):
        self.change_background_color(COLORS['green'])

    def change_line_color_to_black(self):
        self.change_line_color(COLORS['black'])

    def change_line_color_to_white(self):
        self.change_line_color(COLORS['white'])

    def change_line_color_to_red(self):
        self.change_line_color(COLORS['red'])

    def change_line_color_to_blue(self):
        self.change_line_color(COLORS['blue'])

    def change_line_color_to_green(self):
        self.change_line_color(COLORS['green'])

    def cmp_time_circle(self):
        print('cmp_time_circle')
        # self.time_graph = TimeGraphWidget(self.canvas_lbl)
        # self.time_graph.show()

    def cmp_time_ellipse(self):
        print('cmp_time_ellipse')

    def clear_canvas(self):
        print('clear_canvas')
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
