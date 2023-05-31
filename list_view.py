from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QHeaderView, QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
import re
import os


class LogWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('TIISUD | Журнал')

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(['Номер', 'Тип', 'Время', 'Запрос'])
        self.table_widget.horizontalHeader().setStretchLastSection(True)

        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.table_widget.setColumnWidth(0, 50)
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        self.table_widget.setColumnWidth(1, 70)
        self.table_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)
        self.table_widget.setColumnWidth(2, 50)

        self.table_widget.verticalHeader().setDefaultSectionSize(20)

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        self.refresh_button = QPushButton('Обновить')
        self.refresh_button.clicked.connect(self.refresh_table)
        layout.addWidget(self.refresh_button)

        self.clear_button = QPushButton('Очистить')
        self.clear_button.clicked.connect(self.clear_table_and_file)
        layout.addWidget(self.clear_button)

        self.setLayout(layout)

        self.read_logs_and_fill_table()

    def refresh_table(self):
        self.table_widget.setRowCount(0)
        self.read_logs_and_fill_table()

    def clear_table_and_file(self):
        self.table_widget.setRowCount(0)

        with open('requests.log', 'w'):
            pass

    def read_logs_and_fill_table(self):
        with open('requests.log', 'r', encoding='utf-8') as f:
            logs = f.readlines()

        for log in logs:
            log_match = re.match(r'\[(\d+)\]\[(\w)\]\[(.*)\](.+)', log.strip())
            if log_match:
                log_number, log_type, log_time, log_query = log_match.groups()
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)

                self.table_widget.setItem(row_position, 0, QTableWidgetItem(log_number))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(log_type.upper()))
                self.table_widget.setItem(row_position, 2, QTableWidgetItem(log_time))
                self.table_widget.setItem(row_position, 3, QTableWidgetItem(log_query))

                if log_type == 'e':
                    color = QColor()
                    color.setNamedColor('#F08080')
                elif log_type == 'r':
                    color = QColor()
                    color.setNamedColor('#98FB98')
                elif log_type == 'h':
                    color = QColor()
                    color.setNamedColor('#EEE8AA')
                else:
                    color = QColor()
                    color.setNamedColor('#FFFFFF')

                for i in range(4):
                    item = self.table_widget.item(row_position, i)
                    item.setBackground(color)