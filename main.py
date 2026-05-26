import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from ui.main_window import BatchRenamerWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)
    window = BatchRenamerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()