import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from themes.theme_manager import ThemeManager
from utils.i18n import I18n
from ui.login_window import LoginWindow
from ui.main_window import BatchRenamerWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)

    I18n.instance()

    theme_mgr = ThemeManager.instance()
    app.setStyleSheet(theme_mgr.get_stylesheet())
    theme_mgr.theme_changed.connect(app.setStyleSheet)

    login_window = LoginWindow()
    main_window = BatchRenamerWindow()

    def on_login_success():
        login_window.close()
        main_window.show()

    login_window.login_success.connect(on_login_success)
    login_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
