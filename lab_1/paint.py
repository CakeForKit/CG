from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import Qt, QPoint
from geometry import if_90_grad, find_triangle, center_of_rect, point_intersection_bisectrix


DEBUG = True


class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        # uic.loadUi('canvas.ui', self)

        self.frame_size = 50
        self.k = 1 # коэфицент масштабирования
        self.real_x = self.width()
        self.real_y = self.height()
        self.max_x = self.max_y = self.min_x = self.min_y = self.maxlen_x = self.maxlen_y = self.using_points_arr = None
        self.center = [0, 0]
        self.frame_size = 50
        self.text_height = 25
        self.text_width = 200
        self.triangle_paint = False
        self.points = self.point_bis = self.center_rect = None
        self.c_points = self.c_point_bis = self.c_center_rect = None
        self.angle = None

        self.rectp = dict()
        self.arrp = list()
        self.canvas_rect = dict()
        self.canvas_arr = list()

    def update_sup_data(self):
        self.real_x = self.width()
        self.real_y = self.height()
        if self.triangle_paint:
            self.using_points_arr = self.points
            if DEBUG:
                print(f'{self.update_sup_data.__name__}:\t self.using_points_arr: triangle_points {self.points}')
        else:
            self.using_points_arr = self.arrp
            if DEBUG:
                print(f'{self.update_sup_data.__name__}:\t self.using_points_arr: self.arrp')

        self.max_x = max([i[0] for i in self.rectp.values()] + [i[0] for i in self.using_points_arr])
        self.min_x = min([i[0] for i in self.rectp.values()] + [i[0] for i in self.using_points_arr])
        self.max_y = max([i[1] for i in self.rectp.values()] + [i[1] for i in self.using_points_arr])
        self.min_y = min([i[1] for i in self.rectp.values()] + [i[1] for i in self.using_points_arr])
        self.maxlen_x = self.max_x - self.min_x
        self.maxlen_y = self.max_y - self.min_y
        if self.maxlen_x == 0: self.maxlen_x = 1
        if self.maxlen_y == 0: self.maxlen_y = 1

    # высчитывает коэффицент масштабирования
    def update_koef(self):
        self.update_sup_data()
        self.k = min((self.real_x - self.frame_size * 2) / self.maxlen_x, (self.real_y - self.frame_size * 2) / self.maxlen_y)

        if DEBUG:
            print(f'{self.update_koef.__name__}:\t self.k: {self.k}, self.frame_size: {self.frame_size}\n'
                  f'(real_x, real_y): {(self.real_x, self.real_y)}\n'
                  f'(maxlen_x, maxlen_y): {(self.maxlen_x, self.maxlen_y)}')

    def point_on_positiv_fucus(self, x, y):
        plusx = plusy = 0
        if self.min_x < 0:
            plusx = -self.min_x
        elif self.min_x > 0:
            plusx -= self.min_x
        if self.min_y < 0:
            plusy -= self.min_y
        elif self.min_y > 0:
            plusy -= self.min_y
        x += plusx
        y += plusy

        return x, y

    def point_scaling(self, x, y):
        x = int(x * self.k)
        y = int(y * self.k)

        return x, y

    def point_reverse_y(self, y):
        roof = self.real_y # - self.frame_size
        y = roof - y
        return y

    def point_add_frame(self, x, y):
        x += self.frame_size
        y -= self.frame_size

        return x, y

    def point_convert_on_screen_coord_sys(self, x, y):
        if DEBUG:
            print(f'{(x, y)}:\t', end='')

        x, y = self.point_on_positiv_fucus(x, y)
        if DEBUG:
            print(f' -> pos_ficus{(x, y)}', end='')

        # x, y = self.point_to_positiv_coords(x, y)
        # if DEBUG:
        #     print(f' -> pos_coord{(x, y)}', end='')
        #
        # x, y = self.point_on_focus(x, y)
        # if DEBUG:
        #     print(f' -> on_focus{(x, y)}', end='')

        x, y = self.point_scaling(x, y)
        if DEBUG:
            print(f' -> scal{(x, y)}', end='')

        y = self.point_reverse_y(y)
        if DEBUG:
            print(f' -> reverse{(x, y)}', end='')

        x, y = self.point_add_frame(x, y)
        if DEBUG:
            print(f' -> add_frame{(x, y)}')
        # print()
        return x, y

    # преобразовывает точки прямоугольника и множества и цент в экранную систему координат
    # результат в self.canvas_rect, self.canvas_arr, self.center
    def convert_main_data(self):
        self.canvas_rect = dict()
        for k in self.rectp.keys():
            self.canvas_rect[k] = list(self.rectp[k])
        self.canvas_arr = list()
        for i in range(len(self.arrp)):
            self.canvas_arr.append(list(self.arrp[i]))

        if DEBUG:
            print(f'START {self.convert_main_data.__name__}:\n'
                  f'self.canvas_rect: {self.canvas_rect}\n'
                  f'self.canvas_arr: {self.canvas_arr}')

        self.update_koef()

        for k in self.canvas_rect.keys():
            self.canvas_rect[k] = tuple(self.point_convert_on_screen_coord_sys(*self.canvas_rect[k]))
        for i in range(len(self.canvas_arr)):
            self.canvas_arr[i] = tuple(self.point_convert_on_screen_coord_sys(*self.canvas_arr[i]))
        self.center = self.point_convert_on_screen_coord_sys(0, 0)

        if DEBUG:
            print(f'END {self.convert_main_data.__name__}:\t self.center: {self.center}\n'
                  f'self.canvas_rect: {self.canvas_rect}\n'
                  f'self.canvas_arr: {self.canvas_arr}\n' + '-' * 100)

    # определяет переменную self.triangle_paint
    # И если она True, высчитывает координаты треугольника
    def find_triangle_to_draw(self):
        if len(self.rectp) < 4 or len(self.arrp) < 3:
            self.triangle_paint = False
            return

        self.points, self.point_bis, self.center_rect, self.angle = find_triangle(list(self.rectp.values()), list(set(self.arrp)), debug_hear=True)
        if len(self.points) != 0:
            self.triangle_paint = True

            if DEBUG:
                print(f'{self.find_triangle_to_draw.__name__}:\t self.points: {self.points}')
        else:
            self.triangle_paint = False

    def find_canvas_triangle(self):
        if self.triangle_paint:
            tr_points_ind = [-1, -1, -1]
            for i in range(len(self.arrp)):
                for j in range(3):
                    if self.arrp[i] == self.points[j]:
                        tr_points_ind[j] = i
            if any(map(lambda x: x == -1, tr_points_ind)):
                raise Exception('ERR функция поиска треугольника вернула неверные точки!!!!!')

            self.c_points = tuple(self.canvas_arr[tr_points_ind[i]] for i in range(3))

            self.c_center_rect = self.point_convert_on_screen_coord_sys(*self.center_rect)
            self.c_point_bis = self.point_convert_on_screen_coord_sys(*self.point_bis)

            # self.c_center_rect = center_of_rect(list(self.canvas_rect.values()))
            # self.c_point_bis = point_intersection_bisectrix(*self.c_points, debug_hear=True)
            # self.c_center_rect = list(map(round, self.c_center_rect))
            # self.c_point_bis = list(map(round, self.c_point_bis))

            if DEBUG:
                print(f'{self.find_canvas_triangle.__name__}:\n'
                      f'tr_points_ind: {tr_points_ind}\n'
                      f'self.c_points: {self.c_points}\n'
                      f'self.c_center_rect: {self.c_center_rect}, self.c_point_bis: {self.c_point_bis}')

    # обновляет данные и рисует, возвращает текстовый ответ
    def set_data_and_update(self, rect, arr):
        if len(rect) + len(arr) == 0:
            return
        self.rectp = rect
        self.arrp = arr

        self.find_triangle_to_draw()
        self.convert_main_data()
        self.find_canvas_triangle()

        self.update()

        if self.triangle_paint:
            return f'Координаты треугольника: {list(self.points)}\n Искомый угол (в градусах): {self.angle:.2f}'
        else
            return 'Недостаточно данных для ответа'

    # оси координат
    def paint_axis(self, qp):
        pen = QPen()
        pen.setWidth(1)
        pen.setColor(Qt.black)
        qp.setPen(pen)

        x, y = self.center
        qp.drawLine(x, 0, x, self.height())
        qp.drawLine(0, y, self.width(), y)

    def paint_rect(self, qp):
        pen = QPen()
        pen.setWidth(5)
        pen.setColor(Qt.red)
        qp.setPen(pen)
        if len(self.rectp) == 1:
            qp.drawPoint(*list(self.canvas_rect.values())[0])
        elif len(self.rectp) == 2:
            p1, p2 = list(self.canvas_rect.values())
            qp.drawLine(*p1, *p2)
        elif len(self.rectp) == 3:
            p1, p2, p3 = list(self.rectp.values())
            c1, c2, c3 = list(self.canvas_rect.values())
            if if_90_grad(p1, p2, p3):
                qp.drawLine(*c1, *c2)
                qp.drawLine(*c3, *c2)
            elif if_90_grad(p1, p3, p2):
                qp.drawLine(*c1, *c3)
                qp.drawLine(*c3, *c2)
            elif if_90_grad(p2, p1, p3):
                qp.drawLine(*c1, *c3)
                qp.drawLine(*c1, *c2)
        elif len(self.rectp) == 4:
            p1, p2, p3, p4 = list(self.rectp.values())
            c1, c2, c3, c4 = list(self.canvas_rect.values())

            polygon_points = []
            if if_90_grad(p1, p2, p3):
                polygon_points = [c1, c2, c3, c4]
                # qp.drawPolygon(*map(lambda x: QPoint(*x), [c1, c2, c3, c4]))
            elif if_90_grad(p1, p3, p2):
                polygon_points = [c1, c3, c2, c4]
                # qp.drawPolygon(*map(lambda x: QPoint(*x), [c1, c3, c2, c4]))
            elif if_90_grad(p2, p1, p3):
                polygon_points = [c1, c3, c2, c4]
                # qp.drawPolygon(*map(lambda x: QPoint(*x), [c2, c1, c3, c4]))

            if len(polygon_points) != 0:
                for i in range(len(polygon_points) - 1):
                    qp.drawLine(*polygon_points[i], *polygon_points[i + 1])
                qp.drawLine(*polygon_points[0], *polygon_points[-1])

    def paint_points(self, qp):
        pen = QPen()
        pen.setWidth(10)
        pen.setColor(Qt.blue)
        qp.setPen(pen)

        for i in range(len(self.canvas_arr)):
            qp.drawPoint(*self.canvas_arr[i])

    def paint_text(self, qp):
        pen = QPen()
        pen.setWidth(1)
        pen.setColor(Qt.black)
        qp.setPen(pen)

        font = QFont()
        font.setPixelSize(self.text_height)
        qp.setFont(font)
        for k in self.rectp.keys():
            text = f'{k}{self.rectp[k]}'
            x, y = self.canvas_rect[k]
            qp.drawText(x + 5, y - 5, text)
            # qp.drawText(x + 5, y - self.text_height - 5, self.text_width, self.text_height, Qt.TextWordWrap, text)
        set_canvas_arr = set(self.arrp) - set(self.rectp.values())
        for i in range(len(self.arrp)):
            if self.arrp[i] in set_canvas_arr:
                set_canvas_arr -= {self.arrp[i]}
                text = f'{self.arrp[i]}'
                x, y = self.canvas_arr[i]
                qp.drawText(x + 5, y - 5, text)

        if self.triangle_paint:
            x, y = self.point_bis
            cx, cy = self.c_point_bis
            text = f'({x:.2f}, {y:.2f})'
            qp.drawText(cx + 5, cy - 5, text)

            x, y = self.center_rect
            cx, cy = self.c_center_rect
            text = f'({x:.2f}, {y:.2f})'
            qp.drawText(cx + 5, cy - 5, text)

    def paint_triangle(self, qp):
        if not self.triangle_paint:
            return
        if not self.c_points is None and not self.c_point_bis is None and not self.c_center_rect is None:
            if DEBUG:
                print(f'paint_triangle: c_points: {self.c_points}, c_point_bis: {self.c_point_bis}, c_center_rect: {self.c_center_rect}')
                print(f'paint_triangle: points: {self.points}')

            pen = QPen()
            pen.setWidth(5)
            pen.setColor(Qt.blue)
            qp.setPen(pen)
            for i in range(len(self.c_points) - 1):
                qp.drawLine(*self.c_points[i], *self.c_points[i + 1])
            qp.drawLine(*self.c_points[0], *self.c_points[-1])
            # qp.drawPolygon(*map(lambda x: QPoint(*x), self.c_points), fillRule=Qt.WindingFill)

            pen = QPen()
            pen.setWidth(3)
            pen.setColor(Qt.green)
            qp.setPen(pen)
            qp.drawLine(*self.c_point_bis, *self.c_center_rect)

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.begin(self)

        # делаем белый фон
        qp.setBrush(Qt.white)
        qp.drawRect(self.rect())
        #

        # оси координат
        self.paint_axis(qp)
        # прямоугольник
        self.paint_rect(qp)
        # точки
        self.paint_points(qp)
        # текст
        self.paint_text(qp)

        self.paint_triangle(qp)
        # qp.setPen(Qt.red)
        # print('height: ', self.height())
        # qp.drawLine(0, self.height() - 1, self.width(), self.height() - 1) # абсцисса
        # qp.drawLine(0, self.height() - 1, 0, 0) # орбината

        qp.end()











