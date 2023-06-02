import re
import pyqtgraph as pg
from pyqtgraph import BarGraphItem, TextItem
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from collections import Counter

class AnalyseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('TIISUD | Анализ')

        self.graph = pg.PlotWidget(self)
        self.graph.setLabel('left', 'Время выполнения (мс)')
        self.graph.setLabel('bottom', 'Номер запроса')
        self.graph.setBackground('w')
        self.graph.setFixedSize(400, 270)
        self.graph.move(20, 20)

        self.pie_chart = self.create_pie_chart()
        self.pie_chart.setFixedSize(360, 290)
        self.pie_chart.move(430, 10)

        self.histogram_widget = pg.PlotWidget(self)
        self.histogram_widget.setLabel('left', 'Среднее время выполнения (мс)')
        self.histogram_widget.setLabel('bottom', 'Типы запросов')
        self.histogram_widget.setBackground('w')
        self.histogram_widget.setFixedSize(340, 270)
        self.histogram_widget.move(440, 310)

        self.histogram_labels = []
        self.histogram = BarGraphItem(x=[0, 1, 2, 3], height=[0, 0, 0, 0], width=0.9)
        self.histogram_widget.addItem(self.histogram)
        
        self.update_btn = QPushButton('Обновить', self)
        self.update_btn.clicked.connect(self.update_grafs)
        self.update_btn.setFixedSize(self.width() - 40 - self.pie_chart.width(), 30)
        self.update_btn.move(20, self.height() - 20 - self.update_btn.height())

        self.all_queries = QLabel(self)
        self.load_stats()
        self.all_queries.setFixedSize(180, 200)
        self.all_queries.move(20, 310)

        self.parse_logs()

    def load_stats(self):
        requests = {
            "error": 0,
            "s-result": 0,
            "h-result": 0,
            "update": 0,
            "delete": 0,
            "insert": 0,
            "handler": 0,
            "select": 0
        }

        with open("requests.log") as file:
            pattern = r'\[\d+\]\[([\w-]+)\]'
            lines = file.readlines()
            for line in lines:
                match = re.search(pattern, line)
                if match:
                    query_type = match.group(1)
                    requests[query_type] += 1

        self.all_queries.setText(f"Общее количество запросов: {sum(requests.values())}\n\n"
                                  f"ERROR:   \t{requests['error']}\n"
                                  f"UPDATE:  \t{requests['update']}\n"
                                  f"DELETE:   \t{requests['delete']}\n"
                                  f"INSERT:   \t{requests['insert']}\n"
                                  f"SELECT:   \t{requests['select']}\n"
                                  f"HANDLER:\t{requests['handler']}\n"
                                  f"S-RESULT:\t{requests['s-result']}\n"
                                  f"H-RESULT:\t{requests['h-result']}\n")

    def parse_logs(self):
        query_numbers = []
        execution_times = []
        query_types = []

        with open('requests.log', 'r') as file:
            log_data = file.read()

            pattern = r'\[(\d+)\]\[(update|select|error|delete|h-result|s-result|handler|insert)\]\[(\d+) ms\] .+'

            for match in re.finditer(pattern, log_data):
                query_number = int(match.group(1))
                query_type = match.group(2)
                execution_time = int(match.group(3))

                query_numbers.append(query_number)
                execution_times.append(execution_time)
                query_types.append(query_type)

            pen = QPen(Qt.blue)
            pen.setWidthF(0.15)

            self.graph.plot(query_numbers, execution_times, pen=pen, symbol='o', symbolSize=5)

            if query_types and execution_times:
                self.update_histogram(query_types, execution_times)

            self.update_pie_chart(query_types)


    def create_pie_chart(self):
        chart = QChart()
        chart.setTitle("Типы ответов запросов")
        chart_view = QChartView(chart, self)
        chart_view.setFixedSize(300, 300)
        return chart_view

    def update_pie_chart(self, query_types):
        query_type_counts = Counter(query_types)

        pie_series = QPieSeries()
        for query_type, count in query_type_counts.items():
            if query_type == "h-result":
                pie_series.append(f"H-R", count)
            elif query_type == "s-result":
                pie_series.append(f"S-R", count)
            else:
                pie_series.append(f"{query_type.upper()[0]}", count)

        chart = self.pie_chart.chart()
        chart.removeAllSeries()
        chart.addSeries(pie_series)

    def update_histogram(self, query_types, execution_times):
        query_type_execution_times = {}
        query_type_counts = {}

        for query_type, execution_time in zip(query_types, execution_times):
            query_type_execution_times.setdefault(query_type, []).append(execution_time)
            query_type_counts[query_type] = query_type_counts.get(query_type, 0) + 1

        query_type_averages = {}
        for query_type, times in query_type_execution_times.items():
            query_type_averages[query_type] = sum(times) / query_type_counts[query_type]

        sorted_query_types = sorted(query_type_averages.keys())
        x = list(range(len(sorted_query_types)))
        heights = [query_type_averages[query_type] for query_type in sorted_query_types]

        self.histogram.setOpts(x=x, height=heights)
        self.add_histogram_labels(x, sorted_query_types, heights)

    def add_histogram_labels(self, x, labels, heights):
        for label in self.histogram_labels:
            self.histogram_widget.removeItem(label)

        self.histogram_labels.clear()

        for x_val, label in zip(x, labels):
            if label == "h-result":
                text_item = TextItem(text=f" H-R\n{round(heights[x_val], 2)}", color=(0, 0, 0), anchor=(0.5, 1.0))
            elif label == "s-result":
                text_item = TextItem(text=f" S-R\n{round(heights[x_val], 2)}", color=(0, 0, 0), anchor=(0.5, 1.0))
            else:
                text_item = TextItem(text=f"  {label.upper()[0]}\n{round(heights[x_val], 2)}", color=(0, 0, 0), anchor=(0.5, 1.0))
            self.histogram_widget.addItem(text_item)
            text_item.setPos(x_val, 0)
            self.histogram_labels.append(text_item)


    def update_grafs(self):
        self.load_stats()
        self.parse_logs()