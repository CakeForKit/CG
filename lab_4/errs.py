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
