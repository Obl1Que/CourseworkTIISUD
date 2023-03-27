from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton

class LogWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('TIISUD | Журнал')