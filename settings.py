import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.load_settings()

    def init_ui(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('TIISUD | Настройки')

        self.host_label = QLabel('Адрес:', self)
        self.host_label.move(250, 200)

        self.host_input = QLineEdit(self)
        self.host_input.setFixedWidth(200)
        self.host_input.move(350, 200)

        self.port_label = QLabel('Порт:', self)
        self.port_label.move(250, 230)

        self.port_input = QLineEdit(self)
        self.port_input.setFixedWidth(200)
        self.port_input.move(350, 230)

        self.user_label = QLabel('Имя пользователя:', self)
        self.user_label.move(250, 260)

        self.user_input = QLineEdit(self)
        self.user_input.setFixedWidth(200)
        self.user_input.move(350, 260)

        self.password_label = QLabel('Пароль:', self)
        self.password_label.move(250, 290)

        self.password_input = QLineEdit(self)
        self.password_input.setFixedWidth(200)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.move(350, 290)

        self.database_label = QLabel('База данных:', self)
        self.database_label.move(250, 320)

        self.database_input = QLineEdit(self)
        self.database_input.setFixedWidth(200)
        self.database_input.move(350, 320)

        save_btn = QPushButton('Сохранить', self)
        save_btn.setFixedSize(150, 25)
        save_btn.move(250, 350)

        clear_btn = QPushButton('Очистить', self)
        clear_btn.setFixedSize(150, 25)
        clear_btn.move(400, 350)

        save_btn.clicked.connect(self.save_settings)
        clear_btn.clicked.connect(self.clear_settings)

    def load_settings(self):
        try:
            with open('settings_glob.json') as f:
                settings = json.load(f)
        except FileNotFoundError:
            return
        self.host_input.setText(settings.get('host', ''))
        self.port_input.setText(settings.get('port', ''))
        self.user_input.setText(settings.get('user', ''))
        self.password_input.setText(settings.get('password', ''))
        self.database_input.setText(settings.get('database', ''))

    def save_settings(self):
        settings = {
            'host': self.host_input.text(),
            'port': self.port_input.text(),
            'user': self.user_input.text(),
            'password': self.password_input.text(),
            'database': self.database_input.text()
        }
        with open('settings_glob.json', 'w') as f:
            json.dump(settings, f, indent=4)

    def clear_settings(self):
        self.host_input.clear()
        self.port_input.clear()
        self.user_input.clear()
        self.password_input.clear()
        self.database_input.clear()

