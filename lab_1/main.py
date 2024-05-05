import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTableWidgetItem)
from geometry import if_90_grad, find_x4_y4_in_rect
from paint import CanvasWidget


DEBUG = True

# ERRORS
ERR = 'ERROR: '
ERR_NOT_RECT = ERR + 'Данная точка вместе с уже введенными не может образовать прямоугольник'
ERR_RECT_EXIST_POINT = ERR + 'Данная точка уже определена, если хотите ее изменить, то выберете функцию редактирования '
ERR_EDIT_RECT_POINT = ERR + 'Редактировать точку можно только, когда их введено 1, 2 или 3 шт'
ERR_NO_DATA = ERR + 'Не введена еще ни одна точка'
##


class InfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('info.ui', self)
        self.setGeometry(1000, 500, 1000, 800)

        self.ok_pbtn.clicked.connect(self.close_window)

    def close_window(self):
        self.hide()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.setGeometry(500, 100, 2000, 1500)

        # холст
        self.canvas = CanvasWidget()
        self.stackedWidget.addWidget(self.canvas)
        self.stackedWidget.setCurrentWidget(self.canvas)
        ##

        # словарь и масссив точек
        self.rect = dict() # {a: (x, y), b: (x, y), c: (x, y)}
        self.arrp = list()
        ##

        # кнопки
        self.add_pa_pbtn.clicked.connect(self.add_pa)
        self.add_pb_pbtn.clicked.connect(self.add_pb)
        self.add_pc_pbtn.clicked.connect(self.add_pc)
        self.add_pd_pbtn.clicked.connect(self.add_pd)
        self.del_all_points_rect_pbtn.clicked.connect(self.del_all_points_rect)
        self.del_point_rect_pbtn.clicked.connect(self.del_point_rect)
        self.edit_point_rect_pbtn.clicked.connect(self.edit_point_rect)

        self.add_point_arr_pbtn.clicked.connect(self.add_point_arr)
        self.del_all_points_arr_pbtn.clicked.connect(self.del_all_points_arr)
        self.edit_point_arr_pbtn.clicked.connect(self.edit_point_arr)
        self.del_point_arr_pbtn.clicked.connect(self.del_point_arr)

        self.spinBox_x.valueChanged.connect(self.clean_status_bar)
        self.spinBox_y.valueChanged.connect(self.clean_status_bar)
        self.edit_point_rect_cb.currentIndexChanged.connect(self.clean_status_bar)

        self.paint_res_pbtn.clicked.connect(self.paint_res)
        ##

        # таблицы
        self.table_rect.setColumnCount(3)
        self.table_rect.setHorizontalHeaderLabels(['id', 'X', 'Y'])
        ##

        # меню
        self.info_widget = InfoWidget()
        self.info_qm.aboutToShow.connect(self.show_info)
        self.exit_pbtn.aboutToShow.connect(self.exit)
        ##

    def add_point_rect_to_data(self, id, x, y):
        self.rect[id] = (x, y)
        self.del_point_rect_cb.addItem(id)
        self.edit_point_rect_cb.addItem(id)

        numrow = self.table_rect.rowCount()
        self.table_rect.setRowCount(numrow + 1)

        for i, data in enumerate([id, x, y]):
            self.table_rect.setItem(numrow, i, QTableWidgetItem(str(data)))

    def check_and_add_point_rect(self, id):
        self.clean_status_bar()
        x = self.spinBox_x.value()
        y = self.spinBox_y.value()

        if (x, y) not in self.rect.values() and id not in self.rect.keys():
            if len(self.rect) == 0:
                self.add_point_rect_to_data(id, x, y)
            elif len(self.rect) == 1:
                if list(self.rect.values())[0] == (x, y):
                    self.statusbar.showMessage(ERR_NOT_RECT)
                else:
                    self.add_point_rect_to_data(id, x, y)
            elif len(self.rect) == 3:
                p1, p2, p3 = self.rect.values()
                x4y4 = find_x4_y4_in_rect(p1, p2, p3)
                if x4y4 is None:
                    self.statusbar.showMessage(ERR_NOT_RECT)
                    return
                x4, y4 = x4y4
                if x == x4 and y == y4:
                    id4 = 'ABCD'
                    for i in self.rect.keys():
                        id4 = id4.replace(i, '')
                    self.add_point_rect_to_data(id4, x4, y4)
                else:
                    self.statusbar.showMessage(ERR_NOT_RECT)

            else:
                p1, p2 = self.rect.values()  # координаты двух имеющихся точек
                p3 = (x, y)

                if p1 == (x, y) or p2 == (x, y):
                    self.statusbar.showMessage(ERR_NOT_RECT)
                    return

                x4y4 = find_x4_y4_in_rect(p1, p2, p3)
                if x4y4 is None:
                    self.statusbar.showMessage(ERR_NOT_RECT)
                    return
                x4, y4 = x4y4

                self.add_point_rect_to_data(id, x, y)
                id4 = 'ABCD'
                for i in self.rect.keys():
                    id4 = id4.replace(i, '')
                self.add_point_rect_to_data(id4, x4, y4)
        else:
            self.statusbar.showMessage(ERR_RECT_EXIST_POINT)

        if DEBUG:
            print(f'{self.check_and_add_point_rect.__name__}:\t self.rect: {self.rect}')

    def add_pa(self):
        self.check_and_add_point_rect('A')

    def add_pb(self):
        self.check_and_add_point_rect('B')

    def add_pc(self):
        self.check_and_add_point_rect('C')

    def add_pd(self):
        self.check_and_add_point_rect('D')

    def del_all_points_rect(self):
        self.clean_status_bar()

        self.rect = dict()
        self.table_rect.setRowCount(0)
        self.edit_point_rect_cb.clear()
        self.del_point_rect_cb.clear()
        if DEBUG:
            print(f'{self.del_all_points_rect.__name__}:\t\t self.rect: {self.rect}')

    def del_point_rect(self):
        self.clean_status_bar()

        id = self.del_point_rect_cb.currentText()
        if id != '':
            # удаляем из таблицы
            for i in range(len(self.rect.keys())):
                if self.table_rect.item(i, 0).text() == id:
                    self.table_rect.removeRow(i)
                    break

            # удаляем из выпадающего списка
            for i in range(len(self.rect.keys())):
                if self.del_point_rect_cb.itemText(i) == id:
                    self.del_point_rect_cb.removeItem(i)
                    break
            for i in range(len(self.rect.keys())):
                if self.edit_point_rect_cb.itemText(i) == id:
                    self.edit_point_rect_cb.removeItem(i)
                    break

            # удаляем из словаря
            del self.rect[id]

            if DEBUG:
                print(f'{self.del_point_rect.__name__}:\t self.rect: {self.rect}')

    def edit_point_rect(self):
        self.clean_status_bar()

        if len(self.rect.keys()) == 0 or len(self.rect.keys()) == 4:
            self.statusbar.showMessage(ERR_EDIT_RECT_POINT)
        else:
            id = self.edit_point_rect_cb.currentText()
            x = self.spinBox_x.value()
            y = self.spinBox_y.value()

            # если редактировать 3ю точку то надо проверить что образуется прямой угол
            if len(self.rect) == 3:
                points = list()
                for k in self.rect.keys():
                    if k != id:
                        points.append(self.rect[k])
                points.append((x, y))
                if not if_90_grad(*points):
                    self.statusbar.showMessage(ERR_NOT_RECT)
                    return

            for i in self.rect.keys():
                if i != id and x == self.rect[i][0] and y == self.rect[i][1]:
                    self.statusbar.showMessage(ERR_NOT_RECT)
                    return

            # изменяем в таблице
            for i in range(len(self.rect.keys())):
                if self.table_rect.item(i, 0).text() == id:
                    self.table_rect.setItem(i, 1, QTableWidgetItem(str(x)))
                    self.table_rect.setItem(i, 2, QTableWidgetItem(str(y)))
            # изменяем в словаре
            self.rect[id] = (x, y)

        if DEBUG:
            print(f'{self.check_and_add_point_rect.__name__}:\t self.rect: {self.rect}')

    def add_point_arr(self):
        self.clean_status_bar()
        x = self.spinBox_x.value()
        y = self.spinBox_y.value()

        self.arrp.append((x, y))
        id = 'p' + str(len(self.arrp))
        self.del_point_arr_cb.addItem(id)
        self.edit_point_arr_cb.addItem(id)

        numrow = self.table_arr.rowCount()
        self.table_arr.setRowCount(numrow + 1)

        for i, data in enumerate([id, x, y]):
            self.table_arr.setItem(numrow, i, QTableWidgetItem(str(data)))

        if DEBUG:
            print(f'{self.add_point_arr.__name__}:\t\t self.arrp: {self.arrp}')

    def del_all_points_arr(self):
        self.clean_status_bar()
        self.arrp = list()
        self.table_arr.setRowCount(0)
        self.edit_point_arr_cb.clear()
        self.del_point_arr_cb.clear()

        if DEBUG:
            print(f'{self.del_all_points_arr.__name__}:\t self.arrp: {self.arrp}')

    def edit_point_arr(self):
        self.clean_status_bar()

        id = int(self.edit_point_arr_cb.currentText()[1:])
        x = self.spinBox_x.value()
        y = self.spinBox_y.value()
        self.arrp[id - 1] = (x, y)

        # изменяем в таблице
        for i in range(len(self.arrp)):
            if self.table_arr.item(i, 0).text() == f'p{id}':
                self.table_arr.setItem(i, 1, QTableWidgetItem(str(x)))
                self.table_arr.setItem(i, 2, QTableWidgetItem(str(y)))

        if DEBUG:
            print(f'{self.edit_point_arr.__name__}:\t\t self.arrp: {self.arrp}')

    def del_point_arr(self):
        self.clean_status_bar()

        id = self.del_point_arr_cb.currentText()
        if id != '':
            idi = int(id[1:]) - 1
            # удаляем из таблицы
            self.table_arr.removeRow(idi)
            for i in range(idi, len(self.arrp)):
                self.table_arr.setItem(i, 0, QTableWidgetItem('p' + str(i + 1)))

            # удаляем из выпадающего списка
            self.del_point_arr_cb.removeItem(idi)
            for i in range(idi, len(self.arrp)):
                self.del_point_arr_cb.setItemText(i, 'p' + str(i + 1))

            self.edit_point_arr_cb.removeItem(idi)
            for i in range(idi, len(self.arrp)):
                self.edit_point_arr_cb.setItemText(i, 'p' + str(i + 1))

            # удаляем из массива
            del self.arrp[idi]

            if DEBUG:
                print(f'{self.del_point_arr.__name__}:\t\t self.arrp: {self.arrp}')

    def clean_status_bar(self):
        self.statusbar.clearMessage()

    def paint_res(self):
        if len(self.rect) == 0 and len(self.arrp) == 0:
            self.canvas.set_data_and_update({}, [])
            self.statusbar.showMessage(ERR_NO_DATA)
        else:
            res_text = self.canvas.set_data_and_update(self.rect, self.arrp)
            self.res_te.setPlainText(res_text)
            # self.canvas.set_data(self.rect, self.arrp)

    def show_info(self):
        print('show')
        self.info_widget.show()

    def exit(self):
        sys.exit(0)


def exept_hooks(cls, exeption, trades):
    sys.__excepthook__(cls, exeption, trades)


if __name__ == '__main__':
    sys.excepthook = exept_hooks
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
