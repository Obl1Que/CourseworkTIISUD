from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QSpinBox, QVBoxLayout, QFormLayout, QCheckBox, QGroupBox, QPushButton, QTextEdit
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

        reset_id_button = QPushButton('Обнулить id')
        reset_id_button.clicked.connect(self.reset_id)

        form_layout = QFormLayout()
        form_layout.addRow(method_label, self.method_combobox)
        form_layout.addRow(num_queries_label, self.num_queries_spinbox)

        layout.addLayout(form_layout)
        layout.addWidget(self.query_types_groupbox)
        layout.addWidget(self.manual_query_input)
        layout.addWidget(generate_button)
        layout.addWidget(reset_id_button)

        self.setLayout(layout)
        self.log = functions.logger()

    def update_method(self, index):
        if index == 1:
            self.manual_query_input.show()
            self.query_types_groupbox.hide()
        else:
            self.manual_query_input.hide()
            self.query_types_groupbox.show()
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
            manual_query = self.manual_query_input.toPlainText()

            try:
                with connection.cursor() as cursor:
                    if self.method_combobox.currentIndex() == 1:
                        try:
                            cursor.execute(manual_query)
                            connection.commit()
                        except Exception as e:
                            print("Ошибка при выполнении запроса:", e)

                    else:
                        try:
                            if self.select_checkbox.isChecked():
                                cursor.execute("SHOW TABLES")
                                tables = cursor.fetchall()

                                for _ in range(num_queries):
                                    table = rd.choice(tables)[0]

                                    cursor.execute(f"SHOW COLUMNS FROM {table}")
                                    columns = cursor.fetchall()

                                    num_columns = rd.randint(1, len(columns))

                                    selected_columns = rd.sample(columns, num_columns)
                                    column_names = ', '.join([column[0] for column in selected_columns])

                                    select_query = f"SELECT {column_names} FROM {table}"
                                    self.log.add(f"SELECT {column_names} FROM {table}")
                                    cursor.execute(select_query)
                                    result = cursor.fetchall()
                                    self.log.add(result, _type = "r")
                                    self.log.save("requests.log")

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
                                cursor.execute("SHOW TABLES")
                                tables = cursor.fetchall()

                                for _ in range(num_queries):
                                    table = rd.choice(tables)[0]

                                    cursor.execute(f"SHOW COLUMNS FROM {table}")
                                    columns = cursor.fetchall()

                                    num_columns = rd.randint(1, len(columns))

                                    selected_columns = rd.sample(columns, num_columns)

                                    update_parts = []
                                    for column in selected_columns:
                                        if not column[0].lower().startswith('id'):
                                            if column[1].lower().startswith('int'):
                                                new_value = str(rd.randint(0, 1000000))
                                            elif column[1].lower().startswith('text'):
                                                new_value = f"'test-{functions.generate_string()}'"
                                            update_parts.append(f"{column[0]} = {new_value}")

                                    if len(update_parts) > 0:
                                        update_str = ', '.join(update_parts)
                                        cursor.execute(f"SELECT id FROM {table}")
                                        rows = cursor.fetchall()
                                        if len(rows) > 0:
                                            id_value = rd.choice(rows)[0]
                                            print(f"UPDATE {table} SET {update_str} WHERE id = {id_value}")
                                            update_query = f"UPDATE {table} SET {update_str} WHERE id = {id_value}"
                                            cursor.execute(update_query)
                                            connection.commit()

                            if self.delete_checkbox.isChecked():
                                cursor.execute("SHOW TABLES")
                                tables = cursor.fetchall()

                                for _ in range(num_queries):
                                    table = rd.choice(tables)[0]

                                    cursor.execute(f"SHOW COLUMNS FROM {table}")
                                    columns = cursor.fetchall()

                                    delete_query = f"DELETE FROM {table}"
                                    where_conditions = []

                                    cursor.execute(f"SELECT id FROM {table}")
                                    rows = cursor.fetchall()
                                    id_value = rd.choice(rows)[0]

                                    for column in columns:
                                        if column[0].lower().startswith('id'):
                                            where_conditions.append( f"{column[0]} = {id_value}")

                                    if len(where_conditions) > 0:
                                        where_str = ' AND '.join(where_conditions)
                                        delete_query += f" WHERE {where_str}"
                                    print(delete_query)
                                    cursor.execute(delete_query)
                                    connection.commit()

                        except Exception as e:
                            print("Ошибка при выполнении запроса:", e)
            finally:
                connection.close()
        except Exception as ex:
            print(ex)

    def reset_id(self):
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

            try:
                with connection.cursor() as cursor:
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()

                    for table in tables:
                        cursor.execute(f"ALTER TABLE {table[0]} AUTO_INCREMENT = 1")
                        connection.commit()

            except Exception as e:
                print("Ошибка при выполнении запроса:", e)
            finally:
                connection.close()
        except Exception as ex:
            print(ex)