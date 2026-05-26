from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QLabel, QPushButton, QCheckBox, QGraphicsDropShadowEffect, QMenu
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QFont, QColor, QAction
from utils.i18n import I18n
from utils.user_manager import UserManager
from themes.theme_manager import ThemeManager


def _create_card():
    card = QWidget()
    card.setObjectName("login_card")
    card.setFixedWidth(400)
    return card


def _apply_card_shadow(card):
    shadow = QGraphicsDropShadowEffect(card)
    shadow.setBlurRadius(40)
    shadow.setColor(QColor(0, 0, 0, 30))
    shadow.setOffset(0, 8)
    card.setGraphicsEffect(shadow)


def _create_icon_label(text: str):
    icon_label = QLabel(text)
    icon_label.setFixedSize(72, 72)
    icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return icon_label


def _create_theme_button():
    i18n = I18n.instance()
    btn = QPushButton(i18n.tr("nav_skin"))
    btn.setObjectName("btn_theme")
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setFixedHeight(32)
    return btn


def _show_theme_menu(btn):
    i18n = I18n.instance()
    menu = QMenu(btn)
    theme_mgr = ThemeManager.instance()

    themes = [
        ("light", i18n.tr("skin_light")),
        ("dark", i18n.tr("skin_dark")),
        ("system", i18n.tr("skin_system")),
        ("eye_care", i18n.tr("skin_eye_care")),
    ]

    for theme_key, theme_label in themes:
        action = QAction(theme_label, menu)
        action.setCheckable(True)
        action.setChecked(theme_mgr.current_theme_name() == theme_key)
        action.triggered.connect(lambda checked, k=theme_key: theme_mgr.set_theme(k))
        menu.addAction(action)

    pos = btn.mapToGlobal(btn.rect().bottomRight())
    pos.setX(pos.x() - menu.sizeHint().width())
    menu.exec(pos)


class LoginWindow(QWidget):
    login_success = pyqtSignal()
    show_register = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("LoginWindow")
        self.setWindowTitle(I18n.instance().tr("login_title"))
        self.setFixedSize(480, 600)
        self._init_ui()
        self._apply_theme()
        I18n.instance().language_changed.connect(self._retranslate)
        ThemeManager.instance().theme_changed.connect(self._apply_theme)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 12, 16, 0)
        top_bar.addStretch()
        self.theme_btn = _create_theme_button()
        self.theme_btn.clicked.connect(lambda: _show_theme_menu(self.theme_btn))
        top_bar.addWidget(self.theme_btn)
        layout.addLayout(top_bar)

        layout.addStretch(1)

        card = _create_card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(44, 36, 44, 36)
        card_layout.setSpacing(0)

        self.icon_label = _create_icon_label("R")
        icon_row = QHBoxLayout()
        icon_row.addStretch()
        icon_row.addWidget(self.icon_label)
        icon_row.addStretch()
        card_layout.addLayout(icon_row)

        card_layout.addSpacing(18)

        self.title_label = QLabel(I18n.instance().tr("app_title"))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Microsoft YaHei", 20)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        card_layout.addWidget(self.title_label)

        card_layout.addSpacing(6)

        self.subtitle_label = QLabel(I18n.instance().tr("login_subtitle"))
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.subtitle_label)

        card_layout.addSpacing(28)

        self.username_label = QLabel(I18n.instance().tr("username"))
        card_layout.addWidget(self.username_label)
        card_layout.addSpacing(4)

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText(I18n.instance().tr("username_placeholder"))
        self.username_edit.setMinimumHeight(44)
        card_layout.addWidget(self.username_edit)

        card_layout.addSpacing(16)

        self.password_label = QLabel(I18n.instance().tr("password"))
        card_layout.addWidget(self.password_label)
        card_layout.addSpacing(4)

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText(I18n.instance().tr("password_placeholder"))
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setMinimumHeight(44)
        card_layout.addWidget(self.password_edit)

        card_layout.addSpacing(14)

        options_row = QHBoxLayout()
        self.remember_check = QCheckBox(I18n.instance().tr("remember_password"))
        options_row.addWidget(self.remember_check)
        options_row.addStretch()

        self.forgot_btn = QPushButton(I18n.instance().tr("forgot_password"))
        self.forgot_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.forgot_btn.setObjectName("btn_forgot")
        options_row.addWidget(self.forgot_btn)
        card_layout.addLayout(options_row)

        card_layout.addSpacing(24)

        self.login_btn = QPushButton(I18n.instance().tr("login"))
        self.login_btn.setObjectName("btn_login")
        self.login_btn.setMinimumHeight(48)
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        card_layout.addWidget(self.login_btn)

        card_layout.addSpacing(12)

        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setVisible(False)
        card_layout.addWidget(self.error_label)

        self.success_label = QLabel("")
        self.success_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.success_label.setVisible(False)
        card_layout.addWidget(self.success_label)

        card_layout.addSpacing(16)

        footer_row = QHBoxLayout()
        footer_row.addStretch()
        self.no_account_label = QLabel(I18n.instance().tr("no_account"))
        footer_row.addWidget(self.no_account_label)
        self.register_btn = QPushButton(I18n.instance().tr("register"))
        self.register_btn.setObjectName("btn_link")
        self.register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        footer_row.addWidget(self.register_btn)
        footer_row.addStretch()
        card_layout.addLayout(footer_row)

        card_row = QHBoxLayout()
        card_row.addStretch()
        card_row.addWidget(card)
        card_row.addStretch()
        layout.addLayout(card_row)

        layout.addStretch(1)

        self.login_btn.clicked.connect(self._on_login)
        self.password_edit.returnPressed.connect(self._on_login)
        self.username_edit.returnPressed.connect(lambda: self.password_edit.setFocus())
        self.register_btn.clicked.connect(self.show_register.emit)

        self._card = card

    def _apply_theme(self, _stylesheet=None):
        c = ThemeManager.instance().get_colors()

        _apply_card_shadow(self._card)

        self.icon_label.setStyleSheet(f"""
            QLabel {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {c.primary}, stop:1 {c.primary_pressed});
                color: {c.text_on_primary};
                border-radius: 36px;
                font-size: 32px;
                font-weight: bold;
            }}
        """)

        self.title_label.setStyleSheet(f"color: {c.text_primary};")
        self.subtitle_label.setStyleSheet(f"color: {c.text_secondary}; font-size: 13px;")
        self.username_label.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {c.text_secondary};")
        self.password_label.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {c.text_secondary};")

        self.remember_check.setStyleSheet(f"font-size: 12px; color: {c.text_secondary};")
        self.forgot_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background: transparent;
                color: {c.primary};
                font-size: 12px;
                padding: 0;
            }}
            QPushButton:hover {{
                color: {c.primary_pressed};
                text-decoration: underline;
            }}
        """)

        self.error_label.setStyleSheet(f"""
            QLabel {{
                color: {c.error};
                font-size: 12px;
                background-color: {c.error_bg};
                border-radius: 6px;
                padding: 8px;
            }}
        """)
        self.success_label.setStyleSheet(f"""
            QLabel {{
                color: {c.success};
                font-size: 12px;
                background-color: {c.success_bg};
                border-radius: 6px;
                padding: 8px;
            }}
        """)

        self.no_account_label.setStyleSheet(f"color: {c.text_secondary}; font-size: 12px;")
        self.register_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background: transparent;
                color: {c.primary};
                font-size: 12px;
                font-weight: bold;
                padding: 0;
            }}
            QPushButton:hover {{
                color: {c.primary_pressed};
            }}
        """)

    def show_success_message(self, msg: str):
        self.error_label.setVisible(False)
        self.success_label.setText(msg)
        self.success_label.setVisible(True)

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(50, self._animate_entrance)

    def _animate_entrance(self):
        card = self._card
        end_pos = card.pos()
        start_pos = QPoint(end_pos.x(), end_pos.y() + 40)

        _apply_card_shadow(card)

        pos_anim = QPropertyAnimation(card, b"pos")
        pos_anim.setDuration(600)
        pos_anim.setStartValue(start_pos)
        pos_anim.setEndValue(end_pos)
        pos_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        pos_anim.start()
        self._pos_anim = pos_anim

        QTimer.singleShot(800, self._start_icon_float)

    def _start_icon_float(self):
        from utils.animations import float_animation
        float_animation(self.icon_label, amplitude=4, duration=2500)

    def _on_login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()

        self.success_label.setVisible(False)

        i18n = I18n.instance()
        if not username:
            self._show_error(i18n.tr("err_empty_username"))
            self.username_edit.setFocus()
            return
        if not password:
            self._show_error(i18n.tr("err_empty_password"))
            self.password_edit.setFocus()
            return

        if self._authenticate(username, password):
            self.login_success.emit()
        else:
            self._show_error(i18n.tr("err_auth_failed"))

    def _authenticate(self, username: str, password: str) -> bool:
        return UserManager.instance().authenticate(username, password)

    def _show_error(self, msg: str):
        self.success_label.setVisible(False)
        self.error_label.setText(msg)
        self.error_label.setVisible(True)

        anim = QPropertyAnimation(self.error_label, b"pos")
        anim.setDuration(300)
        pos = self.error_label.pos()
        anim.setKeyValueAt(0, pos)
        anim.setKeyValueAt(0.25, QPoint(pos.x() - 5, pos.y()))
        anim.setKeyValueAt(0.5, QPoint(pos.x() + 5, pos.y()))
        anim.setKeyValueAt(0.75, QPoint(pos.x() - 3, pos.y()))
        anim.setKeyValueAt(1, pos)
        anim.start()
        self._shake_anim = anim

    def _retranslate(self):
        i18n = I18n.instance()
        self.setWindowTitle(i18n.tr("login_title"))
        self.title_label.setText(i18n.tr("app_title"))
        self.subtitle_label.setText(i18n.tr("login_subtitle"))
        self.username_label.setText(i18n.tr("username"))
        self.password_label.setText(i18n.tr("password"))
        self.username_edit.setPlaceholderText(i18n.tr("username_placeholder"))
        self.password_edit.setPlaceholderText(i18n.tr("password_placeholder"))
        self.remember_check.setText(i18n.tr("remember_password"))
        self.forgot_btn.setText(i18n.tr("forgot_password"))
        self.login_btn.setText(i18n.tr("login"))
        self.no_account_label.setText(i18n.tr("no_account"))
        self.register_btn.setText(i18n.tr("register"))
        self.theme_btn.setText(i18n.tr("nav_skin"))


class RegisterWindow(QWidget):
    register_success = pyqtSignal(str)
    show_login = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("RegisterWindow")
        self.setWindowTitle(I18n.instance().tr("register_title"))
        self.setFixedSize(480, 680)
        self._init_ui()
        self._apply_theme()
        I18n.instance().language_changed.connect(self._retranslate)
        ThemeManager.instance().theme_changed.connect(self._apply_theme)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 12, 16, 0)
        top_bar.addStretch()
        self.theme_btn = _create_theme_button()
        self.theme_btn.clicked.connect(lambda: _show_theme_menu(self.theme_btn))
        top_bar.addWidget(self.theme_btn)
        layout.addLayout(top_bar)

        layout.addStretch(1)

        card = _create_card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(44, 36, 44, 36)
        card_layout.setSpacing(0)

        self.icon_label = _create_icon_label("+")
        icon_row = QHBoxLayout()
        icon_row.addStretch()
        icon_row.addWidget(self.icon_label)
        icon_row.addStretch()
        card_layout.addLayout(icon_row)

        card_layout.addSpacing(18)

        self.title_label = QLabel(I18n.instance().tr("register"))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Microsoft YaHei", 20)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        card_layout.addWidget(self.title_label)

        card_layout.addSpacing(6)

        self.subtitle_label = QLabel(I18n.instance().tr("register_subtitle"))
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.subtitle_label)

        card_layout.addSpacing(28)

        self.username_label = QLabel(I18n.instance().tr("username"))
        card_layout.addWidget(self.username_label)
        card_layout.addSpacing(4)

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText(I18n.instance().tr("username_placeholder"))
        self.username_edit.setMinimumHeight(44)
        self.username_edit.setMaxLength(20)
        card_layout.addWidget(self.username_edit)

        card_layout.addSpacing(16)

        self.password_label = QLabel(I18n.instance().tr("password"))
        card_layout.addWidget(self.password_label)
        card_layout.addSpacing(4)

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText(I18n.instance().tr("password_placeholder"))
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setMinimumHeight(44)
        self.password_edit.setMaxLength(32)
        card_layout.addWidget(self.password_edit)

        card_layout.addSpacing(16)

        self.confirm_password_label = QLabel(I18n.instance().tr("confirm_password"))
        card_layout.addWidget(self.confirm_password_label)
        card_layout.addSpacing(4)

        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setPlaceholderText(I18n.instance().tr("confirm_password_placeholder"))
        self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_edit.setMinimumHeight(44)
        self.confirm_password_edit.setMaxLength(32)
        card_layout.addWidget(self.confirm_password_edit)

        card_layout.addSpacing(24)

        self.register_btn = QPushButton(I18n.instance().tr("register_btn"))
        self.register_btn.setObjectName("btn_register")
        self.register_btn.setMinimumHeight(48)
        self.register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        card_layout.addWidget(self.register_btn)

        card_layout.addSpacing(12)

        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setVisible(False)
        self.error_label.setWordWrap(True)
        card_layout.addWidget(self.error_label)

        card_layout.addSpacing(16)

        footer_row = QHBoxLayout()
        footer_row.addStretch()
        self.have_account_label = QLabel(I18n.instance().tr("have_account"))
        footer_row.addWidget(self.have_account_label)
        self.back_login_btn = QPushButton(I18n.instance().tr("back_to_login"))
        self.back_login_btn.setObjectName("btn_link")
        self.back_login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        footer_row.addWidget(self.back_login_btn)
        footer_row.addStretch()
        card_layout.addLayout(footer_row)

        card_row = QHBoxLayout()
        card_row.addStretch()
        card_row.addWidget(card)
        card_row.addStretch()
        layout.addLayout(card_row)

        layout.addStretch(1)

        self.register_btn.clicked.connect(self._on_register)
        self.confirm_password_edit.returnPressed.connect(self._on_register)
        self.username_edit.returnPressed.connect(lambda: self.password_edit.setFocus())
        self.password_edit.returnPressed.connect(lambda: self.confirm_password_edit.setFocus())
        self.back_login_btn.clicked.connect(self.show_login.emit)

        self._card = card

    def _apply_theme(self, _stylesheet=None):
        c = ThemeManager.instance().get_colors()

        _apply_card_shadow(self._card)

        self.icon_label.setStyleSheet(f"""
            QLabel {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {c.primary}, stop:1 {c.primary_pressed});
                color: {c.text_on_primary};
                border-radius: 36px;
                font-size: 32px;
                font-weight: bold;
            }}
        """)

        self.title_label.setStyleSheet(f"color: {c.text_primary};")
        self.subtitle_label.setStyleSheet(f"color: {c.text_secondary}; font-size: 13px;")
        self.username_label.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {c.text_secondary};")
        self.password_label.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {c.text_secondary};")
        self.confirm_password_label.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {c.text_secondary};")

        self.error_label.setStyleSheet(f"""
            QLabel {{
                color: {c.error};
                font-size: 12px;
                background-color: {c.error_bg};
                border-radius: 6px;
                padding: 8px;
            }}
        """)

        self.have_account_label.setStyleSheet(f"color: {c.text_secondary}; font-size: 12px;")
        self.back_login_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background: transparent;
                color: {c.primary};
                font-size: 12px;
                font-weight: bold;
                padding: 0;
            }}
            QPushButton:hover {{
                color: {c.primary_pressed};
            }}
        """)

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(50, self._animate_entrance)

    def _animate_entrance(self):
        card = self._card
        end_pos = card.pos()
        start_pos = QPoint(end_pos.x(), end_pos.y() + 40)

        _apply_card_shadow(card)

        pos_anim = QPropertyAnimation(card, b"pos")
        pos_anim.setDuration(600)
        pos_anim.setStartValue(start_pos)
        pos_anim.setEndValue(end_pos)
        pos_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        pos_anim.start()
        self._pos_anim = pos_anim

        QTimer.singleShot(800, self._start_icon_float)

    def _start_icon_float(self):
        from utils.animations import float_animation
        float_animation(self.icon_label, amplitude=4, duration=2500)

    def _on_register(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()

        i18n = I18n.instance()

        if not username:
            self._show_error(i18n.tr("err_empty_username"))
            self.username_edit.setFocus()
            return
        if not password:
            self._show_error(i18n.tr("err_empty_password"))
            self.password_edit.setFocus()
            return
        if not confirm_password:
            self._show_error(i18n.tr("err_confirm_password_empty"))
            self.confirm_password_edit.setFocus()
            return
        if password != confirm_password:
            self._show_error(i18n.tr("err_password_mismatch"))
            self.confirm_password_edit.setFocus()
            return

        success, msg_key = UserManager.instance().register(username, password)
        if success:
            self.register_success.emit(i18n.tr(msg_key))
        else:
            self._show_error(i18n.tr(msg_key))

    def _show_error(self, msg: str):
        self.error_label.setText(msg)
        self.error_label.setVisible(True)

        anim = QPropertyAnimation(self.error_label, b"pos")
        anim.setDuration(300)
        pos = self.error_label.pos()
        anim.setKeyValueAt(0, pos)
        anim.setKeyValueAt(0.25, QPoint(pos.x() - 5, pos.y()))
        anim.setKeyValueAt(0.5, QPoint(pos.x() + 5, pos.y()))
        anim.setKeyValueAt(0.75, QPoint(pos.x() - 3, pos.y()))
        anim.setKeyValueAt(1, pos)
        anim.start()
        self._shake_anim = anim

    def _clear_fields(self):
        self.username_edit.clear()
        self.password_edit.clear()
        self.confirm_password_edit.clear()
        self.error_label.setVisible(False)

    def _retranslate(self):
        i18n = I18n.instance()
        self.setWindowTitle(i18n.tr("register_title"))
        self.title_label.setText(i18n.tr("register"))
        self.subtitle_label.setText(i18n.tr("register_subtitle"))
        self.username_label.setText(i18n.tr("username"))
        self.password_label.setText(i18n.tr("password"))
        self.confirm_password_label.setText(i18n.tr("confirm_password"))
        self.username_edit.setPlaceholderText(i18n.tr("username_placeholder"))
        self.password_edit.setPlaceholderText(i18n.tr("password_placeholder"))
        self.confirm_password_edit.setPlaceholderText(i18n.tr("confirm_password_placeholder"))
        self.register_btn.setText(i18n.tr("register_btn"))
        self.have_account_label.setText(i18n.tr("have_account"))
        self.back_login_btn.setText(i18n.tr("back_to_login"))
        self.theme_btn.setText(i18n.tr("nav_skin"))
