from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QSpinBox, QVBoxLayout, QFormLayout, QCheckBox, QGroupBox, QPushButton
import pymysql
import json
import random as rd
import functions

class RequestsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('TIISUD | Генерация тестовых запросов')

        layout = QVBoxLayout()

        method_label = QLabel('Метод генерации:')
        self.method_combobox = QComboBox()
        self.method_combobox.addItem('Автоматический')
        self.method_combobox.addItem('Ручной')

        self.method_combobox.currentIndexChanged.connect(self.update_method)

        num_queries_label = QLabel('Количество запросов:')
        self.num_queries_spinbox = QSpinBox()
        self.num_queries_spinbox.setRange(1, 1000)

        self.query_types_groupbox = QGroupBox('Типы запросов:')
        query_types_layout = QVBoxLayout()

        self.select_checkbox = QCheckBox('SELECT')
        self.insert_checkbox = QCheckBox('INSERT')
        self.update_checkbox = QCheckBox('UPDATE')
        self.delete_checkbox = QCheckBox('DELETE')

        query_types_layout.addWidget(self.select_checkbox)
        query_types_layout.addWidget(self.insert_checkbox)
        query_types_layout.addWidget(self.update_checkbox)
        query_types_layout.addWidget(self.delete_checkbox)

        self.query_types_groupbox.setLayout(query_types_layout)

        self.manual_query_input = QTextEdit()
        self.manual_query_input.setPlaceholderText("Введите ваш запрос здесь...")
        self.manual_query_input.hide()
        self.manual_query_input.setFixedHeight(200)

        generate_button = QPushButton('Сгенерировать запросы')
        generate_button.clicked.connect(self.generate_queries)

        form_layout = QFormLayout()
        form_layout.addRow(method_label, method_combobox)
        form_layout.addRow(num_queries_label, self.num_queries_spinbox)

        layout.addLayout(form_layout)
        layout.addWidget(query_types_groupbox)
        layout.addWidget(generate_button)

        self.setLayout(layout)

    def generate_queries(self):
        try:
            with open('settings_glob.json') as f:
                settings = json.load(f)

            connection = pymysql.connect(
                host=settings["host"],
                port=int(settings["port"]),
                user=settings["user"],
                password=settings["password"],
                database=settings["database"]
            )

            num_queries = self.num_queries_spinbox.value()

            try:
                with connection.cursor() as cursor:
                    try:
                        if self.select_checkbox.isChecked():
                            pass
                        if self.insert_checkbox.isChecked():
                            cursor.execute("SHOW TABLES")
                            tables = cursor.fetchall()

                            for table in tables:
                                cursor.execute(f"SHOW COLUMNS FROM {table[0]}")
                                columns = cursor.fetchall()

                                non_autoincrement_columns = [column for column in columns if column[5] != 'auto_increment']
                                column_names = ', '.join([column[0] for column in non_autoincrement_columns])

                                for _ in range(num_queries):
                                    values = []

                                    for column in non_autoincrement_columns:
                                        if column[1].lower().startswith('int'):
                                            values.append(str(rd.randint(0, 1000000)))
                                        elif column[1].lower().startswith('text'):
                                            values.append(f"'{functions.generate_string()}'")

                                    values_str = ', '.join(values)
                                    insert_query = f"INSERT INTO {table[0]} ({column_names}) VALUES ({values_str})"
                                    cursor.execute(insert_query)
                                    connection.commit()

                        if self.update_checkbox.isChecked():
                            pass
                        if self.delete_checkbox.isChecked():
                            pass
                    except Exception as e:
                        print("Ошибка при выполнении запроса:", e)
            finally:
                connection.close()
        except Exception as ex:
            print(ex)