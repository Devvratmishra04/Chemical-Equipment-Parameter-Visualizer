from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from ..utils.api_client import APIClient

class UploadWidget(QWidget):
    upload_success = pyqtSignal(dict) # Signal to emit analysis data on success

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel("Select a CSV file to upload")
        self.label.setStyleSheet("font-size: 16px; margin-bottom: 20px;")
        layout.addWidget(self.label)

        self.btn_select = QPushButton("Choose File")
        self.btn_select.setFixedSize(200, 50)
        self.btn_select.setStyleSheet("background-color: #38bdf8; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_select.clicked.connect(self.select_file)
        layout.addWidget(self.btn_select)

        self.file_path_label = QLabel("")
        layout.addWidget(self.file_path_label)

        self.btn_upload = QPushButton("Upload & Analyze")
        self.btn_upload.setFixedSize(200, 50)
        self.btn_upload.setStyleSheet("background-color: #22c55e; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_upload.clicked.connect(self.upload_file)
        self.btn_upload.setEnabled(False)
        layout.addWidget(self.btn_upload)

        self.setLayout(layout)
        self.selected_file = None

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            self.selected_file = file_path
            self.file_path_label.setText(f"Selected: {file_path}")
            self.btn_upload.setEnabled(True)

    def upload_file(self):
        if not self.selected_file:
            return
        
        self.label.setText("Uploading...")
        self.btn_upload.setEnabled(False)
        self.btn_select.setEnabled(False)

        # Call API (should ideally be in a thread to not freeze UI, but keeping simple for now)
        response = APIClient.upload_file(self.selected_file)

        if "error" in response:
             QMessageBox.critical(self, "Error", f"Upload failed: {response.get('error')}")
             self.label.setText("Upload Failed")
        else:
             self.upload_success.emit(response.get('analysis', {}))
             self.label.setText("Upload Successful!")
        
        self.btn_upload.setEnabled(True)
        self.btn_select.setEnabled(True)
