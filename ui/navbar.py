from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QMenu
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction
from themes.theme_manager import ThemeManager
from utils.i18n import I18n


class NavBar(QWidget):
    action_new = pyqtSignal()
    action_save_config = pyqtSignal()
    action_export_list = pyqtSignal()
    action_theme_changed = pyqtSignal(str)
    action_language_changed = pyqtSignal(str)
    action_show_guide = pyqtSignal()
    action_show_faq = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("NavBar")
        self.setFixedHeight(52)
        self._setup_ui()
        self._connect_signals()
        I18n.instance().language_changed.connect(self._retranslate)

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(4)

        self.title_label = QLabel(I18n.instance().tr("app_title"))
        self.title_label.setObjectName("nav_title")

        self.btn_tasks = self._create_nav_btn(I18n.instance().tr("nav_task"))
        self.btn_skin = self._create_nav_btn(I18n.instance().tr("nav_skin"))
        self.btn_language = self._create_nav_btn(I18n.instance().tr("nav_language"))
        self.btn_help = self._create_nav_btn(I18n.instance().tr("nav_help"))

        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.btn_tasks)
        layout.addWidget(self.btn_skin)
        layout.addWidget(self.btn_language)
        layout.addWidget(self.btn_help)

    def _create_nav_btn(self, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setObjectName("nav_btn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn

    def _connect_signals(self):
        self.btn_tasks.clicked.connect(self._show_task_menu)
        self.btn_skin.clicked.connect(self._show_skin_menu)
        self.btn_language.clicked.connect(self._show_language_menu)
        self.btn_help.clicked.connect(self._show_help_menu)

    def _show_task_menu(self):
        i18n = I18n.instance()
        menu = QMenu(self)

        act_new = QAction(i18n.tr("task_new"), menu)
        act_new.triggered.connect(self.action_new.emit)
        menu.addAction(act_new)

        act_save = QAction(i18n.tr("task_save_config"), menu)
        act_save.triggered.connect(self.action_save_config.emit)
        menu.addAction(act_save)

        menu.addSeparator()

        act_export = QAction(i18n.tr("task_export_list"), menu)
        act_export.triggered.connect(self.action_export_list.emit)
        menu.addAction(act_export)

        pos = self.btn_tasks.mapToGlobal(self.btn_tasks.rect().bottomLeft())
        menu.exec(pos)

    def _show_skin_menu(self):
        i18n = I18n.instance()
        menu = QMenu(self)
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
            current = theme_mgr.current_theme_name()
            action.setChecked(current == theme_key)
            action.triggered.connect(lambda checked, k=theme_key: self._on_theme_selected(k))
            menu.addAction(action)

        pos = self.btn_skin.mapToGlobal(self.btn_skin.rect().bottomLeft())
        menu.exec(pos)

    def _on_theme_selected(self, theme_key: str):
        ThemeManager.instance().set_theme(theme_key)
        self.action_theme_changed.emit(theme_key)

    def _show_language_menu(self):
        i18n = I18n.instance()
        menu = QMenu(self)

        languages = [
            ("zh_CN", i18n.tr("lang_zh_cn")),
            ("zh_TW", i18n.tr("lang_zh_tw")),
            ("en_US", i18n.tr("lang_en")),
        ]

        for lang_key, lang_label in languages:
            action = QAction(lang_label, menu)
            action.setCheckable(True)
            action.setChecked(i18n.current_language() == lang_key)
            action.triggered.connect(lambda checked, k=lang_key: self._on_language_selected(k))
            menu.addAction(action)

        pos = self.btn_language.mapToGlobal(self.btn_language.rect().bottomLeft())
        menu.exec(pos)

    def _on_language_selected(self, lang_key: str):
        I18n.instance().set_language(lang_key)
        self.action_language_changed.emit(lang_key)

    def _show_help_menu(self):
        i18n = I18n.instance()
        menu = QMenu(self)

        act_guide = QAction(i18n.tr("help_guide"), menu)
        act_guide.triggered.connect(self.action_show_guide.emit)
        menu.addAction(act_guide)

        act_faq = QAction(i18n.tr("help_faq"), menu)
        act_faq.triggered.connect(self.action_show_faq.emit)
        menu.addAction(act_faq)

        pos = self.btn_help.mapToGlobal(self.btn_help.rect().bottomLeft())
        menu.exec(pos)

    def _retranslate(self):
        i18n = I18n.instance()
        self.title_label.setText(i18n.tr("app_title"))
        self.btn_tasks.setText(i18n.tr("nav_task"))
        self.btn_skin.setText(i18n.tr("nav_skin"))
        self.btn_language.setText(i18n.tr("nav_language"))
        self.btn_help.setText(i18n.tr("nav_help"))
