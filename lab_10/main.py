import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from info import InfoWidget
from canvas import Canvas
from funcs import funcs_module
from algos import FloatHorizon

from errs import *

DEBUG = True

COLORS = {
    'purple': QColor(170, 85, 255),
    'black': QColor(0, 0, 0),
    'yellow': QColor(255, 255, 102),
    'red': QColor(255, 101, 101),
    'blue': QColor(0, 0, 255),
    'green': QColor(93, 186, 0)
}


class MainWindow(QMainWindow):  # , Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # self.setupUi(self)
        uic.loadUi('main_window.ui', self)
        width, height = 2600, 1200
        self.setGeometry(50, 50, width, height)

        self.background_color = QColor(255, 255, 255)
        self.line_color = COLORS['red']
        self.canvas = Canvas(self.canvas_lbl, self.line_color, self.background_color)
        self.change_line_color(self.line_color)

        for f_txt in funcs_module.keys():
            self.funcs_comboBox.addItem(f_txt)

        self.angles_xyz = [0.0, 0.0, 0.0]

        self.color_btns_clicked()
        self.clear_canvas_btn.clicked.connect(self.clear_canvas)
        self.draw_func_btn.clicked.connect(self.draw_func)
        self.rotate_x_btn.clicked.connect(self.change_angle_x)
        self.rotate_y_btn.clicked.connect(self.change_angle_y)
        self.rotate_z_btn.clicked.connect(self.change_angle_z)
        self.funcs_comboBox.currentTextChanged.connect(self.reset_angles)
        self.reset_angles_btn.clicked.connect(self.reset_angles_and_draw)

        # меню
        self.info_widget = InfoWidget()
        self.info_qm.aboutToShow.connect(self.show_info)
        self.exit_pbtn.aboutToShow.connect(self.exit)
        ##

    def draw_func(self):
        self.show_grads()

        print('Start draw...')
        x_min_max_step = self.get_x_borders_step()
        z_min_max_step = self.get_z_borders_step()
        if (x_min_max_step[0] >= x_min_max_step[1] or z_min_max_step[0] >= z_min_max_step[1]):
            errm = Errors_my(MaxBiggerMinErr.text())
            errm.show()
            return

        func_txt = self.get_func_txt()

        self.canvas.redraw()
        print('input_data:', *x_min_max_step, *z_min_max_step, self.canvas, func_txt, self.angles_xyz)
        FloatHorizon(*x_min_max_step, *z_min_max_step, self.canvas, funcs_module[func_txt], self.angles_xyz)
        self.canvas.import_img()
        print('end.')
    
    def show_grads(self):
        print('SHOW_GRADS')
        self.show_grads_OX_le.setText(f'{self.angles_xyz[0]:.2f}')
        self.show_grads_OY_le.setText(f'{self.angles_xyz[1]:.2f}')
        self.show_grads_OZ_le.setText(f'{self.angles_xyz[2]:.2f}')

    def reset_angles(self):
        self.angles_xyz = [0.0, 0.0, 0.0]
        self.show_grads()

    def reset_angles_and_draw(self):
        self.reset_angles()
        self.draw_func()

    def get_func_txt(self):
        return self.funcs_comboBox.currentText()

    def get_x_borders_step(self):
        x_start = self.x_start_dsp.value()
        x_end = self.x_end_dsp.value()
        x_step = self.x_step_dsp.value()

        return x_start, x_end, x_step

    def get_z_borders_step(self):
        z_start = self.z_start_dsp.value()
        z_end = self.z_end_dsp.value()
        z_step = self.z_step_dsp.value()

        return z_start, z_end, z_step

    def change_angle_x(self):
        self.angles_xyz[0] += self.ox_angle_dsp.value()
        self.show_grads()
        self.draw_func()

    def change_angle_y(self):
        self.angles_xyz[1] += self.oy_angle_dsp.value()
        self.show_grads()
        self.draw_func()

    def change_angle_z(self):
        self.angles_xyz[2] += self.oz_angle_dsp.value()
        self.show_grads()
        self.draw_func()

    def color_btns_clicked(self):
        self.purple_btn_line.clicked.connect(self.change_line_color_to_purple)
        self.black_btn_line.clicked.connect(self.change_line_color_to_black)
        self.yellow_btn_line.clicked.connect(self.change_line_color_to_yellow)
        self.red_btn_line.clicked.connect(self.change_line_color_to_red)
        self.blue_btn_line.clicked.connect(self.change_line_color_to_blue)
        self.green_btn_line.clicked.connect(self.change_line_color_to_green)

    def change_line_color(self, color):
        print(f'change_line_color to {color.getRgb()}')
        self.color_line_show.setStyleSheet(f"background-color: {color.name()}")
        self.line_color = color
        self.canvas.setNewColor(color)

    def change_line_color_to_purple(self):
        self.change_line_color(COLORS['purple'])

    def change_line_color_to_black(self):
        self.change_line_color(COLORS['black'])

    def change_line_color_to_yellow(self):
        self.change_line_color(COLORS['yellow'])

    def change_line_color_to_red(self):
        self.change_line_color(COLORS['red'])

    def change_line_color_to_blue(self):
        self.change_line_color(COLORS['blue'])

    def change_line_color_to_green(self):
        self.change_line_color(COLORS['green'])

    def clear_canvas(self):
        print('clear_canvas')
        self.canvas.clear_canvas()

    def show_info(self):
        print('show info')
        self.info_widget.show()

    # def resizeEvent(self, event):
    #     self.update()

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
