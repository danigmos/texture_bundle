from PySide6 import QtWidgets, QtCore, QtGui
from core.file_scanner import scan_exr_files
from ui.style import load_stylesheet

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Texture bundle")
        self.resize(800, 500)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.setStyleSheet(load_stylesheet())

    def create_widgets(self):
        self.label = QtWidgets.QLabel("Path")
        self.filepath = QtWidgets.QLineEdit()
        self.button_select = QtWidgets.QPushButton("Select folder")

        self.table = QtWidgets.QTableWidget(0,5)
        self.table.setHorizontalHeaderLabels(["Name", "Path", "Type", "Color Space", "State"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def create_layouts(self):
        file_path_layout = QtWidgets.QHBoxLayout()
        file_path_layout.addWidget(self.label)
        file_path_layout.addWidget(self.filepath)
        file_path_layout.addWidget(self.button_select)

        table_layout = QtWidgets.QHBoxLayout()
        table_layout.addWidget(self.table)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(file_path_layout)
        main_layout.addLayout(table_layout)

    def create_connections(self):
        self.button_select.clicked.connect(self.select_folder)

    def select_folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select folder")
        if folder_path:
            self.load_files(folder_path)

    def load_files(self, folder_path):
        self.filepath.setText(folder_path)
        data = scan_exr_files(folder_path)

        self.table.setRowCount(0)
        for i, item in enumerate(data):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(item["filename"]))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(item["fullpath"]))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(item["map_type"]))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(item["color_space"]))
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(item["status"]))



