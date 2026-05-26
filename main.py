import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from themes.theme_manager import ThemeManager
from utils.i18n import I18n
from ui.login_window import LoginWindow, RegisterWindow
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
    register_window = RegisterWindow()
    main_window = BatchRenamerWindow()

    def on_login_success():
        login_window.close()
        main_window.show()

    def on_show_register():
        login_window.close()
        register_window._clear_fields()
        register_window.show()

    def on_show_login():
        register_window.close()
        login_window.show()

    def on_register_success(msg: str):
        register_window.close()
        login_window.username_edit.clear()
        login_window.password_edit.clear()
        login_window.show_success_message(msg)
        login_window.show()

    login_window.login_success.connect(on_login_success)
    login_window.show_register.connect(on_show_register)
    register_window.show_login.connect(on_show_login)
    register_window.register_success.connect(on_register_success)

    login_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
