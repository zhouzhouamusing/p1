import sys
from dataclasses import dataclass
from PyQt6.QtCore import QObject, pyqtSignal


@dataclass
class ThemeColors:
    page_background: str
    card_background: str
    surface_alt: str
    primary: str
    primary_hover: str
    primary_pressed: str
    primary_surface: str
    text_primary: str
    text_secondary: str
    text_on_primary: str
    border: str
    border_focus: str
    border_light: str
    success: str
    success_bg: str
    warning: str
    warning_bg: str
    error: str
    error_bg: str
    navbar_bg: str
    navbar_border: str
    input_bg: str
    font_family: str = "Microsoft YaHei"


def generate_stylesheet(c: ThemeColors) -> str:
    return f"""
        QMainWindow, QWidget#LoginWindow, QWidget#RegisterWindow {{
            background-color: {c.page_background};
        }}
        QWidget {{
            font-size: 13px;
            font-family: "{c.font_family}";
            color: {c.text_primary};
        }}
        QGroupBox {{
            font-weight: bold;
            font-size: 13px;
            border: 1px solid {c.border_light};
            border-left: 3px solid {c.primary};
            border-radius: 10px;
            margin-top: 14px;
            padding: 20px 16px 14px 16px;
            background-color: {c.card_background};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 16px;
            padding: 3px 12px;
            color: {c.primary};
            font-size: 13px;
            background-color: {c.primary_surface};
            border-radius: 4px;
        }}
        QPushButton {{
            padding: 8px 18px;
            border-radius: 6px;
            border: 1px solid {c.border};
            background-color: {c.card_background};
            font-size: 13px;
            font-family: "{c.font_family}";
            color: {c.text_primary};
        }}
        QPushButton:hover {{
            background-color: {c.primary_surface};
            border-color: {c.primary};
        }}
        QPushButton:pressed {{
            background-color: {c.primary_hover};
        }}
        QPushButton#btn_execute {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {c.primary}, stop:1 {c.primary_pressed});
            color: {c.text_on_primary};
            border: none;
            font-weight: bold;
            font-size: 14px;
            padding: 10px 32px;
            border-radius: 8px;
        }}
        QPushButton#btn_execute:hover {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {c.primary_pressed}, stop:1 {c.primary_hover});
        }}
        QPushButton#btn_execute:pressed {{
            background-color: {c.primary_hover};
        }}
        QPushButton#btn_undo {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffb74d, stop:1 #fb8c00);
            color: white;
            border: none;
            font-weight: bold;
            font-size: 13px;
            padding: 10px 24px;
            border-radius: 8px;
        }}
        QPushButton#btn_undo:hover {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #fb8c00, stop:1 #e65100);
        }}
        QPushButton#btn_undo:pressed {{
            background-color: #bf360c;
        }}
        QPushButton#btn_undo:disabled {{
            background-color: {c.surface_alt};
            color: {c.text_secondary};
            border: none;
        }}
        QPushButton#btn_refresh {{
            background-color: {c.card_background};
            border: 1px solid {c.success};
            color: {c.success};
            font-weight: bold;
            font-size: 13px;
            padding: 10px 20px;
            border-radius: 8px;
        }}
        QPushButton#btn_refresh:hover {{
            background-color: {c.success_bg};
            border-color: {c.success};
        }}
        QPushButton#btn_refresh:pressed {{
            background-color: {c.success_bg};
        }}
        QPushButton#btn_select_tool {{
            padding: 5px 14px;
            font-size: 12px;
            border-radius: 4px;
            background-color: {c.surface_alt};
            border: 1px solid {c.border};
            color: {c.text_secondary};
        }}
        QPushButton#btn_select_tool:hover {{
            background-color: {c.primary_surface};
            border-color: {c.primary};
            color: {c.primary};
        }}
        QPushButton#btn_login {{
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {c.primary}, stop:1 {c.primary_pressed});
            color: {c.text_on_primary};
            border: none;
            font-weight: bold;
            font-size: 15px;
            padding: 12px 32px;
            border-radius: 10px;
            min-height: 20px;
        }}
        QPushButton#btn_login:hover {{
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {c.primary_pressed}, stop:1 {c.primary_hover});
        }}
        QPushButton#btn_login:pressed {{
            background-color: {c.primary_hover};
        }}
        QPushButton#btn_register {{
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {c.primary}, stop:1 {c.primary_pressed});
            color: {c.text_on_primary};
            border: none;
            font-weight: bold;
            font-size: 15px;
            padding: 12px 32px;
            border-radius: 10px;
            min-height: 20px;
        }}
        QPushButton#btn_register:hover {{
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {c.primary_pressed}, stop:1 {c.primary_hover});
        }}
        QPushButton#btn_register:pressed {{
            background-color: {c.primary_hover};
        }}
        QPushButton#btn_theme {{
            border: none;
            background-color: transparent;
            color: {c.text_secondary};
            font-size: 13px;
            padding: 6px 14px;
            border-radius: 6px;
        }}
        QPushButton#btn_theme:hover {{
            background-color: {c.primary_surface};
            color: {c.primary};
        }}
        QWidget#login_card {{
            background-color: {c.card_background};
            border-radius: 16px;
        }}
        QLineEdit {{
            padding: 7px 12px;
            border: 1px solid {c.border};
            border-radius: 6px;
            background-color: {c.input_bg};
            font-size: 13px;
            color: {c.text_primary};
            selection-background-color: {c.primary_surface};
        }}
        QLineEdit:focus {{
            border: 2px solid {c.primary};
            padding: 6px 11px;
        }}
        QSpinBox {{
            padding: 8px 14px;
            border: 1.5px solid {c.border};
            border-radius: 10px;
            background-color: {c.input_bg};
            font-size: 15px;
            font-weight: 600;
            color: {c.text_primary};
            min-height: 38px;
            min-width: 50px;
        }}
        QSpinBox:focus {{
            border: 2px solid {c.primary};
            padding: 7px 13px;
        }}
        QSpinBox::up-button, QSpinBox::down-button {{
            width: 0;
            height: 0;
            border: none;
            background: transparent;
        }}
        QSpinBox::up-arrow, QSpinBox::down-arrow {{
            width: 0;
            height: 0;
            border: none;
        }}
        QPushButton#spin_btn_minus, QPushButton#spin_btn_plus {{
            background-color: {c.primary_surface};
            border: 1.5px solid {c.primary};
            color: {c.primary};
            font-size: 18px;
            font-weight: bold;
            min-width: 36px;
            max-width: 36px;
            min-height: 36px;
            max-height: 36px;
            border-radius: 18px;
            padding: 0;
        }}
        QPushButton#spin_btn_minus:hover, QPushButton#spin_btn_plus:hover {{
            background-color: {c.primary};
            color: {c.text_on_primary};
            border-color: {c.primary_pressed};
        }}
        QPushButton#spin_btn_minus:pressed, QPushButton#spin_btn_plus:pressed {{
            background-color: {c.primary_pressed};
            color: {c.text_on_primary};
        }}
        QTableWidget {{
            border: 1px solid {c.border_light};
            border-radius: 8px;
            gridline-color: {c.border_light};
            font-size: 13px;
            background-color: {c.card_background};
            alternate-background-color: {c.surface_alt};
            color: {c.text_primary};
        }}
        QTableWidget::item {{
            padding: 6px;
            border: none;
        }}
        QHeaderView::section {{
            background-color: {c.surface_alt};
            padding: 10px 8px;
            border: none;
            border-bottom: 2px solid {c.border_light};
            font-weight: bold;
            font-size: 13px;
            color: {c.text_secondary};
        }}
        QRadioButton {{
            spacing: 8px;
            font-size: 13px;
            color: {c.text_primary};
        }}
        QRadioButton::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 9px;
            border: 2px solid {c.border};
            background-color: {c.input_bg};
        }}
        QRadioButton::indicator:checked {{
            border: 2px solid {c.primary};
            background-color: {c.primary};
        }}
        QRadioButton::indicator:hover {{
            border-color: {c.primary};
        }}
        QCheckBox {{
            spacing: 6px;
            font-size: 13px;
            color: {c.text_primary};
        }}
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 2px solid {c.border};
            background-color: {c.input_bg};
        }}
        QCheckBox::indicator:checked {{
            border: 2px solid {c.primary};
            background-color: {c.primary};
        }}
        QCheckBox::indicator:hover {{
            border-color: {c.primary};
        }}
        QStatusBar {{
            background-color: {c.card_background};
            border-top: 1px solid {c.border_light};
            font-size: 12px;
            padding: 6px 16px;
            min-height: 32px;
        }}
        QStatusBar QLabel {{
            padding: 2px 10px;
            font-size: 12px;
            color: {c.text_secondary};
        }}
        QWidget#NavBar {{
            background-color: {c.navbar_bg};
            border-bottom: 1px solid {c.navbar_border};
        }}
        QPushButton#nav_btn {{
            border: none;
            background-color: transparent;
            color: {c.text_secondary};
            font-size: 13px;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 500;
        }}
        QPushButton#nav_btn:hover {{
            background-color: {c.primary_surface};
            color: {c.primary};
        }}
        QPushButton#nav_btn:pressed {{
            background-color: {c.primary_hover};
        }}
        QLabel#nav_title {{
            font-size: 15px;
            font-weight: bold;
            color: {c.primary};
            padding: 0 8px;
        }}
        QMenu {{
            background-color: {c.card_background};
            border: 1px solid {c.border};
            border-radius: 8px;
            padding: 6px;
        }}
        QMenu::item {{
            padding: 8px 24px;
            border-radius: 4px;
            color: {c.text_primary};
        }}
        QMenu::item:selected {{
            background-color: {c.primary_surface};
            color: {c.primary};
        }}
        QMenu::separator {{
            height: 1px;
            background-color: {c.border_light};
            margin: 4px 8px;
        }}
        QScrollBar:vertical {{
            background-color: {c.surface_alt};
            width: 10px;
            border-radius: 5px;
            margin: 2px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {c.border};
            border-radius: 4px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {c.primary};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        QComboBox {{
            padding: 7px 12px;
            border: 1px solid {c.border};
            border-radius: 6px;
            background-color: {c.input_bg};
            font-size: 13px;
            color: {c.text_primary};
            min-height: 28px;
        }}
        QComboBox:focus {{
            border: 2px solid {c.primary};
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 28px;
            border-left: 1px solid {c.border_light};
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
            background-color: {c.surface_alt};
        }}
        QComboBox::down-arrow {{
            width: 10px;
            height: 10px;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 5px solid {c.text_secondary};
        }}
        QComboBox QAbstractItemView {{
            background-color: {c.card_background};
            border: 1px solid {c.border};
            border-radius: 6px;
            padding: 4px;
            selection-background-color: {c.primary_surface};
            selection-color: {c.primary};
        }}
        QDateEdit {{
            padding: 7px 12px;
            border: 1px solid {c.border};
            border-radius: 6px;
            background-color: {c.input_bg};
            font-size: 13px;
            color: {c.text_primary};
            min-height: 28px;
        }}
        QDateEdit:focus {{
            border: 2px solid {c.primary};
        }}
        QDateEdit::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 28px;
            border-left: 1px solid {c.border_light};
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
            background-color: {c.surface_alt};
        }}
        QDateEdit::down-arrow {{
            width: 10px;
            height: 10px;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 5px solid {c.text_secondary};
        }}
        QLabel#hint_label {{
            font-size: 11px;
            color: {c.text_secondary};
            padding: 2px 0;
            font-style: italic;
        }}
        QPushButton#btn_preview_detail {{
            background-color: {c.card_background};
            border: 1px solid {c.primary};
            color: {c.primary};
            font-weight: bold;
            font-size: 13px;
            padding: 10px 20px;
            border-radius: 8px;
        }}
        QPushButton#btn_preview_detail:hover {{
            background-color: {c.primary_surface};
            border-color: {c.primary_pressed};
        }}
        QPushButton#btn_preview_detail:pressed {{
            background-color: {c.primary_hover};
        }}
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
    """


class ThemeManager(QObject):
    theme_changed = pyqtSignal(str)

    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = ThemeManager()
        return cls._instance

    def __init__(self):
        super().__init__()
        self._current_theme = "light"
        self._themes = {
            "light": _light_colors(),
            "dark": _dark_colors(),
            "eye_care": _eye_care_colors(),
        }

    def set_theme(self, name: str):
        if name == "system":
            name = _detect_system_theme()
        if name in self._themes:
            self._current_theme = name
            self.theme_changed.emit(self.get_stylesheet())

    def get_stylesheet(self) -> str:
        return generate_stylesheet(self._themes[self._current_theme])

    def get_colors(self) -> ThemeColors:
        return self._themes[self._current_theme]

    def current_theme_name(self) -> str:
        return self._current_theme


def _detect_system_theme() -> str:
    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return "light" if value == 1 else "dark"
        except Exception:
            return "light"
    return "light"


def _light_colors() -> ThemeColors:
    return ThemeColors(
        page_background="#f0f2f5",
        card_background="#ffffff",
        surface_alt="#f8f9fa",
        primary="#1a73e8",
        primary_hover="#d2e3fc",
        primary_pressed="#1557b0",
        primary_surface="#e8f0fe",
        text_primary="#202124",
        text_secondary="#5f6368",
        text_on_primary="#ffffff",
        border="#dadce0",
        border_focus="#4285f4",
        border_light="#e8eaed",
        success="#2e7d32",
        success_bg="#e8f5e9",
        warning="#e65100",
        warning_bg="#fff3e0",
        error="#c62828",
        error_bg="#ffcdd2",
        navbar_bg="#ffffff",
        navbar_border="#e8eaed",
        input_bg="#ffffff",
    )


def _dark_colors() -> ThemeColors:
    return ThemeColors(
        page_background="#1a1a2e",
        card_background="#25253e",
        surface_alt="#2d2d48",
        primary="#8ab4f8",
        primary_hover="#3d5a80",
        primary_pressed="#5b9cf6",
        primary_surface="#1e3a5f",
        text_primary="#e8eaed",
        text_secondary="#9aa0a6",
        text_on_primary="#1a1a2e",
        border="#3c4055",
        border_focus="#8ab4f8",
        border_light="#2d2d48",
        success="#81c784",
        success_bg="#1b3d1e",
        warning="#ffb74d",
        warning_bg="#3d2e1a",
        error="#ef5350",
        error_bg="#3d1a1a",
        navbar_bg="#25253e",
        navbar_border="#3c4055",
        input_bg="#2d2d48",
    )


def _eye_care_colors() -> ThemeColors:
    return ThemeColors(
        page_background="#f5f0e8",
        card_background="#faf7f2",
        surface_alt="#ede8e0",
        primary="#5d8a3c",
        primary_hover="#c8ddb8",
        primary_pressed="#4a7030",
        primary_surface="#e8f0e0",
        text_primary="#3d3929",
        text_secondary="#6b6456",
        text_on_primary="#ffffff",
        border="#d4cfc5",
        border_focus="#5d8a3c",
        border_light="#e8e3da",
        success="#4a7030",
        success_bg="#e8f0e0",
        warning="#b8860b",
        warning_bg="#fdf5e6",
        error="#a94442",
        error_bg="#f2dede",
        navbar_bg="#faf7f2",
        navbar_border="#e8e3da",
        input_bg="#fefdfb",
    )
