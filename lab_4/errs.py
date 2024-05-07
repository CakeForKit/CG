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


class ErrParamCount(BaseErr):
    @staticmethod
    def text():
        return 'Неверное количество параметров класса\n'


class ErrParam(BaseErr):
    @staticmethod
    def text():
        return 'По заданным параметра нельзя построит спектр\n'


class ErrBegEndRadius(BaseErr):
    @staticmethod
    def text():
        return 'Начальный радиус не может быть больше конечного или равен ему\n'


class ErrStep(BaseErr):
    @staticmethod
    def text():
        return 'Слишком большой шаг изменения радиуса\n'
