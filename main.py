from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtWidgets import QWidget
import sys
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()