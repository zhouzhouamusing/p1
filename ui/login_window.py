from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QLabel, QPushButton, QCheckBox, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QFont, QColor
from utils.i18n import I18n


class LoginWindow(QWidget):
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("LoginWindow")
        self.setWindowTitle(I18n.instance().tr("login_title"))
        self.setFixedSize(480, 600)
        self._init_ui()
        I18n.instance().language_changed.connect(self._retranslate)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addStretch(1)

        card = QWidget()
        card.setObjectName("login_card")
        card.setFixedWidth(400)
        card.setStyleSheet("""
            QWidget#login_card {
                background-color: rgba(255, 255, 255, 0.97);
                border-radius: 16px;
            }
        """)

        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 8)
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(44, 36, 44, 36)
        card_layout.setSpacing(0)

        self.icon_label = QLabel("R")
        self.icon_label.setFixedSize(72, 72)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("""
            QLabel {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border-radius: 36px;
                font-size: 32px;
                font-weight: bold;
            }
        """)
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
        self.title_label.setStyleSheet("color: #2d3748;")
        card_layout.addWidget(self.title_label)

        card_layout.addSpacing(6)

        self.subtitle_label = QLabel(I18n.instance().tr("login_subtitle"))
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setStyleSheet("color: #718096; font-size: 13px;")
        card_layout.addWidget(self.subtitle_label)

        card_layout.addSpacing(28)

        self.username_label = QLabel(I18n.instance().tr("username"))
        self.username_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #4a5568; margin-bottom: 4px;")
        card_layout.addWidget(self.username_label)
        card_layout.addSpacing(4)

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText(I18n.instance().tr("username_placeholder"))
        self.username_edit.setMinimumHeight(44)
        self.username_edit.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 10px 16px;
                border-radius: 10px;
                border: 1.5px solid #e2e8f0;
                background-color: #f7fafc;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: #ffffff;
                padding: 9px 15px;
            }
        """)
        card_layout.addWidget(self.username_edit)

        card_layout.addSpacing(16)

        self.password_label = QLabel(I18n.instance().tr("password"))
        self.password_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #4a5568; margin-bottom: 4px;")
        card_layout.addWidget(self.password_label)
        card_layout.addSpacing(4)

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText(I18n.instance().tr("password_placeholder"))
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setMinimumHeight(44)
        self.password_edit.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 10px 16px;
                border-radius: 10px;
                border: 1.5px solid #e2e8f0;
                background-color: #f7fafc;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: #ffffff;
                padding: 9px 15px;
            }
        """)
        card_layout.addWidget(self.password_edit)

        card_layout.addSpacing(14)

        options_row = QHBoxLayout()
        self.remember_check = QCheckBox(I18n.instance().tr("remember_password"))
        self.remember_check.setStyleSheet("font-size: 12px; color: #718096;")
        options_row.addWidget(self.remember_check)
        options_row.addStretch()

        self.forgot_btn = QPushButton(I18n.instance().tr("forgot_password"))
        self.forgot_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                color: #667eea;
                font-size: 12px;
                padding: 0;
            }
            QPushButton:hover {
                color: #5a67d8;
                text-decoration: underline;
            }
        """)
        self.forgot_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        options_row.addWidget(self.forgot_btn)
        card_layout.addLayout(options_row)

        card_layout.addSpacing(24)

        self.login_btn = QPushButton(I18n.instance().tr("login"))
        self.login_btn.setObjectName("btn_login")
        self.login_btn.setMinimumHeight(48)
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                font-weight: bold;
                font-size: 15px;
                padding: 12px 32px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a67d8, stop:1 #6b46a0);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4c51bf, stop:1 #553c9a);
            }
        """)
        card_layout.addWidget(self.login_btn)

        card_layout.addSpacing(12)

        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setStyleSheet("""
            QLabel {
                color: #e53e3e;
                font-size: 12px;
                background-color: #fed7d7;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        self.error_label.setVisible(False)
        card_layout.addWidget(self.error_label)

        card_layout.addSpacing(16)

        footer_row = QHBoxLayout()
        footer_row.addStretch()
        self.no_account_label = QLabel(I18n.instance().tr("no_account"))
        self.no_account_label.setStyleSheet("color: #a0aec0; font-size: 12px;")
        footer_row.addWidget(self.no_account_label)
        self.register_btn = QPushButton(I18n.instance().tr("register"))
        self.register_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                color: #667eea;
                font-size: 12px;
                font-weight: bold;
                padding: 0;
            }
            QPushButton:hover {
                color: #5a67d8;
            }
        """)
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

        self._card = card

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(50, self._animate_entrance)

    def _animate_entrance(self):
        card = self._card
        end_pos = card.pos()
        start_pos = QPoint(end_pos.x(), end_pos.y() + 40)

        from PyQt6.QtWidgets import QGraphicsOpacityEffect
        opacity_effect = QGraphicsOpacityEffect(card)
        card.setGraphicsEffect(None)
        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 8)
        card.setGraphicsEffect(shadow)

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
        return bool(username and password)

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
