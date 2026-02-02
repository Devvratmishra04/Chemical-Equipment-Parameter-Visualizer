import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QMessageBox, QListWidget
from desktop.ui.upload_widget import UploadWidget
from desktop.ui.dashboard_widget import DashboardWidget
from desktop.utils.api_client import APIClient

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 1000, 800)
        
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Upload Tab
        self.upload_tab = UploadWidget()
        self.upload_tab.upload_success.connect(self.on_data_received)
        self.tabs.addTab(self.upload_tab, "Upload")

        # Dashboard Tab
        self.dashboard_tab = DashboardWidget()
        self.tabs.addTab(self.dashboard_tab, "Dashboard")

        # History Tab
        self.history_tab = QWidget()
        self.history_layout = QVBoxLayout()
        self.history_tab.setLayout(self.history_layout)
        
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.load_history_item)
        self.history_layout.addWidget(self.history_list)
        
        self.refresh_history_btn = QListWidget() # Mistake in variable name but concept clear, fix below
        # actually separate button
        from PyQt5.QtWidgets import QPushButton
        self.btn_refresh = QPushButton("Refresh History")
        self.btn_refresh.clicked.connect(self.load_history)
        self.history_layout.addWidget(self.btn_refresh)
        
        self.tabs.addTab(self.history_tab, "History")
        
        # Initial load
        self.load_history()

    def on_data_received(self, data):
        self.dashboard_tab.display_data(data)
        self.tabs.setCurrentIndex(1) # Switch to dashboard
        self.load_history() # Refresh history

    def load_history(self):
        self.history_list.clear() # Fix: Use history_list not btn
        history_data = APIClient.get_history()
        
        if isinstance(history_data, list):
            self.history_data_cache = history_data # Cache to retrieve summary later
            for item in history_data:
                label = f"ID: {item.get('id')} - {item.get('uploaded_at')}"
                self.history_list.addItem(label)
        else:
             self.history_list.addItem("Failed to load history")

    def load_history_item(self, item):
        index = self.history_list.row(item)
        if hasattr(self, 'history_data_cache') and index < len(self.history_data_cache):
            data = self.history_data_cache[index]
            if 'summary' in data:
                self.dashboard_tab.display_data(data['summary'])
                self.tabs.setCurrentIndex(1)

def main():
    app = QApplication(sys.argv)
    
    # Set dark theme or similar if desired, but sticking to default for now
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
