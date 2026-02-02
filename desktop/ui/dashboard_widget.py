from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QScrollArea
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Scroll area for dashboards with many items
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        scroll.setWidget(self.content_widget)
        self.layout.addWidget(scroll)

        # Placeholder
        self.msg_label = QLabel("No data loaded. Please upload a file via the Upload tab.")
        self.msg_label.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(self.msg_label)
        
        self.stats_layout = QHBoxLayout()
        self.content_layout.addLayout(self.stats_layout)

        self.charts_layout = QVBoxLayout()
        self.content_layout.addLayout(self.charts_layout)

        self.table = QTableWidget()
        self.content_layout.addWidget(self.table)
        self.table.hide()

    def display_data(self, data):
        self.msg_label.hide()
        
        # Clear previous layouts
        self.clear_layout(self.stats_layout)
        self.clear_layout(self.charts_layout)
        
        stats = data.get('stats', {})
        type_dist = data.get('type_distribution', {})
        records = data.get('data', [])

        # Display Stats
        for key, value in stats.items():
            lbl = QLabel(f"{key.replace('_', ' ').title()}:\n{value}")
            lbl.setStyleSheet("border: 1px solid #ccc; padding: 10px; border-radius: 5px; background: #f0f0f0; font-size: 14px; font-weight: bold;")
            lbl.setAlignment(Qt.AlignCenter)
            self.stats_layout.addWidget(lbl)

        # Display Chart
        self.plot_distribution(type_dist)

        # Display Table
        self.populate_table(records)

    def plot_distribution(self, type_dist):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        types = list(type_dist.keys())
        counts = list(type_dist.values())
        
        ax.bar(types, counts, color='#38bdf8')
        ax.set_title('Equipment Type Distribution')
        ax.set_ylabel('Count')
        ax.set_xlabel('Type')
        
        canvas = FigureCanvas(fig)
        self.charts_layout.addWidget(canvas)

    def populate_table(self, records):
        if not records:
            return
        
        self.table.setRowCount(len(records))
        self.table.setColumnCount(len(records[0]))
        self.table.setHorizontalHeaderLabels(records[0].keys())
        
        for row_idx, row_data in enumerate(records):
            for col_idx, (key, value) in enumerate(row_data.items()):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        
        self.table.show()
        self.table.setMinimumHeight(300)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
