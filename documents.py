from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton

class DocumentsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('TIISUD | Документация')

        self.about_text_b = QLabel(self)
        self.about_text_b.setText("\tДокументация")
        self.about_text_b.setStyleSheet('''
                    border-color: beige;
                    font: bold 16px;
                ''')
        self.about_text_b.setFixedSize(210, 100)
        self.about_text_b.move(self.width() // 2 - self.about_text_b.width() + 60, 80)

        self.about_text = QLabel(self)
        self.about_text.setText('''
        \t   Данная программа была реализована для выполнения курсовой работы.\n
        \tДисциплина: Технологии и инструменты систем управления данными
        \tТема курсовой работы: «Программа генерации тестовых запросов»
        \tСтудент группы: БСБО-09-20   Дёжин Александр Андреевич
        \tРуководитель курсовой работы: к.т.н., доц. Нурматова Елена Вячеславовна          
        ''')
        self.about_text.setStyleSheet('''
            border-color: beige;
            font: bold 14px;
        ''')
        self.about_text.move(30, 140)
        self.about_text.setFixedSize(self.width(), 200)