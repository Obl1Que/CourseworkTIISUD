import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QStackedWidget
from settings import SettingsWindow
from list_view import LogWindow
from requests import RequestsWindow
from documents import DocumentsWindow
from analyse import AnalyseWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TIISUD')

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.settings_window = SettingsWindow()
        self.central_widget.addWidget(self.settings_window)

        self.log_window = LogWindow()
        self.central_widget.addWidget(self.log_window)

        self.requests_window = RequestsWindow()
        self.central_widget.addWidget(self.requests_window)

        self.documents_window = DocumentsWindow()
        self.central_widget.addWidget(self.documents_window)

        self.analyse_window = AnalyseWindow()
        self.central_widget.addWidget(self.analyse_window)

        self.init_ui()

    def init_ui(self):
        settings_action = QAction('Настройки', self)
        settings_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.settings_window))

        log_action = QAction('Журнал', self)
        log_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.log_window))

        requests_action = QAction('Запросы', self)
        requests_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.requests_window))

        documents_action = QAction('Документация', self)
        documents_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.documents_window))

        analysis_action = QAction('Анализ', self)
        analysis_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.analyse_window))

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        settings_menu = menu_bar.addMenu('Настройки')
        settings_menu.addAction(settings_action)

        log_menu = menu_bar.addMenu('Журнал')
        log_menu.addAction(log_action)

        requests_menu = menu_bar.addMenu('Запросы')
        requests_menu.addAction(requests_action)

        documents_menu = menu_bar.addMenu('Документация')
        documents_menu.addAction(documents_action)

        analysis_menu = menu_bar.addMenu('Анализ')
        analysis_menu.addAction(analysis_action)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
