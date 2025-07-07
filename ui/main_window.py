from PySide6 import QtWidgets, QtCore, QtGui
from core.file_scanner import scan_exr_files
from ui.style import load_stylesheet
from core.metadata_writer import insert_color_space_metadata

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
        self.button_metadata = QtWidgets.QPushButton("Insert Metadata")

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

        metadata_layout = QtWidgets.QHBoxLayout()
        metadata_layout.addStretch()
        metadata_layout.addWidget(self.button_metadata)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(file_path_layout)
        main_layout.addLayout(table_layout)
        main_layout.addLayout(metadata_layout)

    def create_connections(self):
        self.button_select.clicked.connect(self.select_folder)
        self.button_metadata.clicked.connect(self.insert_metadata)

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

    def insert_metadata(self):
        row_count = self.table.rowCount()
        for i in range(row_count):
            path = self.table.item(i, 1).text()
            color_space = self.table.item(i, 3).text()

            output_path = insert_color_space_metadata(path, color_space)

            if output_path:
                status_item = QtWidgets.QTableWidgetItem(f"Saved in /with_metadata/")
            else:
                status_item = QtWidgets.QTableWidgetItem("Error")

            self.table.setItem(i,4, status_item)
