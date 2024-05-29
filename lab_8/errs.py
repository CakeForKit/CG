from PyQt5.QtWidgets import QMessageBox


class Errors_my:
    def __init__(self, text):
        self.text = text
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setText("Ошибка")
        self.msg.setInformativeText(text)
        self.msg.setWindowTitle("Error")

    def show(self):
        self.msg.exec_()

    def __str__(self):
        return f'Error("{self.text}")'


class BaseErr(Exception):
    @staticmethod
    def text():
        return 'Ошибка\n'


class ConvexityErr(BaseErr):
    @staticmethod
    def text():
        return 'Отсекатель должен быть выпуклым многоугольником\n'


class PointCodeErr(BaseErr):
    @staticmethod
    def text():
        return 'PointCodeErr\n'


class AddPointToCloseFigureErr(BaseErr):
    @staticmethod
    def text():
        return 'Попытка добавить точку в замкнутый отсекатель\n'


class ErrPointExistInFigure(BaseErr):
    @staticmethod
    def text():
        return 'Точка с такими координатами уже есть в фигуре'


class ErrCanNotCloseFigure(BaseErr):
    @staticmethod
    def text():
        return 'В фигуре должно быть не менее 3х точек чтобы ее замкнуть'


class ErrNoSeedPoint(BaseErr):
    @staticmethod
    def text():
        return 'Затравочный пиксель не задан'
