from PyQt6.QtWidgets import (
    QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout,
    QPushButton, QLineEdit, QLabel, QSpinBox, QRadioButton,
    QButtonGroup, QCheckBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QWidget, QDialog, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from themes.theme_manager import ThemeManager
from utils.i18n import I18n


class FolderSelector(QGroupBox):
    def __init__(self):
        super().__init__(I18n.instance().tr("folder_select"))
        self.folder_path_edit = QLineEdit()
        self.folder_path_edit.setReadOnly(True)
        self.folder_path_edit.setPlaceholderText(I18n.instance().tr("folder_placeholder"))
        self.browse_btn = QPushButton(I18n.instance().tr("browse"))
        self.browse_btn.setFixedWidth(90)
        self._setup_layout()
        I18n.instance().language_changed.connect(self._retranslate)

    def _setup_layout(self):
        h = QHBoxLayout(self)
        self._path_label = QLabel(I18n.instance().tr("path_label"))
        h.addWidget(self._path_label)
        h.addWidget(self.folder_path_edit)
        h.addWidget(self.browse_btn)

    def get_folder_path(self) -> str:
        return self.folder_path_edit.text()

    def set_folder_path(self, path: str) -> None:
        self.folder_path_edit.setText(path)

    def _retranslate(self):
        i18n = I18n.instance()
        self.setTitle(i18n.tr("folder_select"))
        self.folder_path_edit.setPlaceholderText(i18n.tr("folder_placeholder"))
        self.browse_btn.setText(i18n.tr("browse"))
        self._path_label.setText(i18n.tr("path_label"))


class OutputLocationSelector(QGroupBox):
    def __init__(self):
        super().__init__(I18n.instance().tr("output_location"))
        self._setup_ui()
        I18n.instance().language_changed.connect(self._retranslate)

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(12)

        self.radio_original = QRadioButton(I18n.instance().tr("output_original_dir"))
        self.radio_custom = QRadioButton(I18n.instance().tr("output_custom_dir"))
        self.radio_original.setChecked(True)

        self.mode_group = QButtonGroup(self)
        self.mode_group.addButton(self.radio_original, 0)
        self.mode_group.addButton(self.radio_custom, 1)

        self.custom_path_edit = QLineEdit()
        self.custom_path_edit.setReadOnly(True)
        self.custom_path_edit.setPlaceholderText(I18n.instance().tr("output_custom_placeholder"))
        self.custom_path_edit.setEnabled(False)

        self.custom_browse_btn = QPushButton(I18n.instance().tr("browse"))
        self.custom_browse_btn.setFixedWidth(90)
        self.custom_browse_btn.setEnabled(False)

        layout.addWidget(self.radio_original)
        layout.addWidget(self.radio_custom)
        layout.addWidget(self.custom_path_edit, 1)
        layout.addWidget(self.custom_browse_btn)

        self.mode_group.idClicked.connect(self._on_mode_changed)
        self.custom_browse_btn.clicked.connect(self._browse_custom)

    def _on_mode_changed(self, id_: int):
        is_custom = (id_ == 1)
        self.custom_path_edit.setEnabled(is_custom)
        self.custom_browse_btn.setEnabled(is_custom)
        if not is_custom:
            self.custom_path_edit.clear()

    def _browse_custom(self):
        folder = QFileDialog.getExistingDirectory(self, I18n.instance().tr("output_custom_placeholder"))
        if folder:
            self.custom_path_edit.setText(folder)

    def is_original_dir(self) -> bool:
        return self.mode_group.checkedId() == 0

    def get_custom_path(self) -> str:
        return self.custom_path_edit.text()

    def _retranslate(self):
        i18n = I18n.instance()
        self.setTitle(i18n.tr("output_location"))
        self.radio_original.setText(i18n.tr("output_original_dir"))
        self.radio_custom.setText(i18n.tr("output_custom_dir"))
        self.custom_path_edit.setPlaceholderText(i18n.tr("output_custom_placeholder"))
        self.custom_browse_btn.setText(i18n.tr("browse"))


class RenameModePanel(QGroupBox):
    def __init__(self):
        super().__init__(I18n.instance().tr("rename_rules"))
        self.mode_group = QButtonGroup(self)
        self._init_widgets()
        self._setup_layout()
        self._update_visibility()
        self.mode_group.idClicked.connect(self._update_visibility)
        I18n.instance().language_changed.connect(self._retranslate)

    def _init_widgets(self):
        i18n = I18n.instance()
        self.radio_prefix_suffix = QRadioButton(i18n.tr("mode_prefix_suffix"))
        self.radio_sequential = QRadioButton(i18n.tr("mode_sequential"))
        self.radio_replace = QRadioButton(i18n.tr("mode_replace"))
        self.radio_direct_input = QRadioButton(i18n.tr("mode_direct_input"))
        self.radio_prefix_suffix.setChecked(True)

        self.mode_group.addButton(self.radio_prefix_suffix, 0)
        self.mode_group.addButton(self.radio_sequential, 1)
        self.mode_group.addButton(self.radio_replace, 2)
        self.mode_group.addButton(self.radio_direct_input, 3)

        self.prefix_edit = QLineEdit()
        self.prefix_edit.setPlaceholderText(i18n.tr("prefix_placeholder"))
        self.suffix_edit = QLineEdit()
        self.suffix_edit.setPlaceholderText(i18n.tr("suffix_placeholder"))

        self.start_num_spin = QSpinBox()
        self.start_num_spin.setMinimum(0)
        self.start_num_spin.setMaximum(99999)
        self.start_num_spin.setValue(1)
        self.start_num_spin.setFixedWidth(100)

        self.digits_spin = QSpinBox()
        self.digits_spin.setMinimum(1)
        self.digits_spin.setMaximum(10)
        self.digits_spin.setValue(3)
        self.digits_spin.setFixedWidth(100)

        self.seq_prefix_edit = QLineEdit()
        self.seq_prefix_edit.setPlaceholderText(i18n.tr("seq_prefix_placeholder"))

        self.find_edit = QLineEdit()
        self.find_edit.setPlaceholderText(i18n.tr("find_placeholder"))
        self.replace_edit = QLineEdit()
        self.replace_edit.setPlaceholderText(i18n.tr("replace_placeholder"))

        self.case_sensitive_check = QCheckBox(i18n.tr("case_sensitive"))
        self.case_sensitive_check.setChecked(True)

        self.direct_name_edit = QLineEdit()
        self.direct_name_edit.setPlaceholderText(i18n.tr("direct_name_placeholder"))

    def _setup_layout(self):
        i18n = I18n.instance()
        grid = QGridLayout(self)
        grid.setSpacing(8)

        grid.addWidget(self.radio_prefix_suffix, 0, 0)
        grid.addWidget(self.radio_sequential, 0, 1)
        grid.addWidget(self.radio_replace, 0, 2)
        grid.addWidget(self.radio_direct_input, 0, 3)

        self._label_prefix = QLabel(i18n.tr("prefix"))
        grid.addWidget(self._label_prefix, 1, 0)
        grid.addWidget(self.prefix_edit, 1, 1, 1, 3)
        self._label_suffix = QLabel(i18n.tr("suffix"))
        grid.addWidget(self._label_suffix, 2, 0)
        grid.addWidget(self.suffix_edit, 2, 1, 1, 3)

        self._label_start_num = QLabel(i18n.tr("start_num"))
        grid.addWidget(self._label_start_num, 3, 0)
        grid.addWidget(self.start_num_spin, 3, 1)

        self._label_digits = QLabel(i18n.tr("digits"))
        digits_layout = QHBoxLayout()
        digits_layout.setContentsMargins(0, 0, 0, 0)
        digits_layout.addWidget(self._label_digits)
        digits_layout.addWidget(self.digits_spin)
        digits_layout.addStretch()
        self._digits_widget = QWidget()
        self._digits_widget.setLayout(digits_layout)
        grid.addWidget(self._digits_widget, 3, 2)

        self._label_seq_prefix = QLabel(i18n.tr("seq_prefix"))
        grid.addWidget(self._label_seq_prefix, 4, 0)
        grid.addWidget(self.seq_prefix_edit, 4, 1, 1, 3)

        self._label_find = QLabel(i18n.tr("find"))
        grid.addWidget(self._label_find, 5, 0)
        grid.addWidget(self.find_edit, 5, 1, 1, 3)
        self._label_replace = QLabel(i18n.tr("replace"))
        grid.addWidget(self._label_replace, 6, 0)
        grid.addWidget(self.replace_edit, 6, 1, 1, 3)

        grid.addWidget(self.case_sensitive_check, 7, 1)

        self._label_direct_name = QLabel(i18n.tr("new_filename"))
        grid.addWidget(self._label_direct_name, 8, 0)
        grid.addWidget(self.direct_name_edit, 8, 1, 1, 3)

    def _update_visibility(self):
        mode = self.mode_group.checkedId()

        prefix_suffix_visible = (mode == 0)
        self._label_prefix.setVisible(prefix_suffix_visible)
        self.prefix_edit.setVisible(prefix_suffix_visible)
        self._label_suffix.setVisible(prefix_suffix_visible)
        self.suffix_edit.setVisible(prefix_suffix_visible)

        sequential_visible = (mode == 1)
        self._label_start_num.setVisible(sequential_visible)
        self.start_num_spin.setVisible(sequential_visible)
        self._digits_widget.setVisible(sequential_visible)
        self._label_seq_prefix.setVisible(sequential_visible)
        self.seq_prefix_edit.setVisible(sequential_visible)

        replace_visible = (mode == 2)
        self._label_find.setVisible(replace_visible)
        self.find_edit.setVisible(replace_visible)
        self._label_replace.setVisible(replace_visible)
        self.replace_edit.setVisible(replace_visible)
        self.case_sensitive_check.setVisible(replace_visible)

        direct_visible = (mode == 3)
        self._label_direct_name.setVisible(direct_visible)
        self.direct_name_edit.setVisible(direct_visible)

    def set_direct_input_available(self, available: bool):
        self.radio_direct_input.setVisible(available)
        if not available and self.mode_group.checkedId() == 3:
            self.radio_prefix_suffix.setChecked(True)
            self._update_visibility()
        if not available:
            self._label_direct_name.setVisible(False)
            self.direct_name_edit.setVisible(False)

    def _retranslate(self):
        i18n = I18n.instance()
        self.setTitle(i18n.tr("rename_rules"))
        self.radio_prefix_suffix.setText(i18n.tr("mode_prefix_suffix"))
        self.radio_sequential.setText(i18n.tr("mode_sequential"))
        self.radio_replace.setText(i18n.tr("mode_replace"))
        self.radio_direct_input.setText(i18n.tr("mode_direct_input"))
        self._label_prefix.setText(i18n.tr("prefix"))
        self._label_suffix.setText(i18n.tr("suffix"))
        self.prefix_edit.setPlaceholderText(i18n.tr("prefix_placeholder"))
        self.suffix_edit.setPlaceholderText(i18n.tr("suffix_placeholder"))
        self._label_start_num.setText(i18n.tr("start_num"))
        self._label_digits.setText(i18n.tr("digits"))
        self._label_seq_prefix.setText(i18n.tr("seq_prefix"))
        self.seq_prefix_edit.setPlaceholderText(i18n.tr("seq_prefix_placeholder"))
        self._label_find.setText(i18n.tr("find"))
        self._label_replace.setText(i18n.tr("replace"))
        self.find_edit.setPlaceholderText(i18n.tr("find_placeholder"))
        self.replace_edit.setPlaceholderText(i18n.tr("replace_placeholder"))
        self.case_sensitive_check.setText(i18n.tr("case_sensitive"))
        self._label_direct_name.setText(i18n.tr("new_filename"))
        self.direct_name_edit.setPlaceholderText(i18n.tr("direct_name_placeholder"))


class PreviewTable(QGroupBox):
    selection_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__(I18n.instance().tr("preview"))
        self.table = QTableWidget()
        self._setup_table()
        self._setup_layout()
        self.table.itemChanged.connect(self._on_item_changed)
        I18n.instance().language_changed.connect(self._retranslate)

    def _setup_table(self):
        i18n = I18n.instance()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            i18n.tr("col_select"), i18n.tr("col_original"),
            i18n.tr("col_new"), i18n.tr("col_status")
        ])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(3, 80)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

    def _setup_layout(self):
        v = QVBoxLayout(self)

        toolbar = QHBoxLayout()
        self.btn_select_all = QPushButton(I18n.instance().tr("select_all"))
        self.btn_deselect_all = QPushButton(I18n.instance().tr("deselect_all"))
        self.btn_select_all.setObjectName("btn_select_tool")
        self.btn_deselect_all.setObjectName("btn_select_tool")
        self.btn_select_all.setFixedHeight(28)
        self.btn_deselect_all.setFixedHeight(28)
        toolbar.addWidget(self.btn_select_all)
        toolbar.addWidget(self.btn_deselect_all)
        toolbar.addStretch()

        self.btn_select_all.clicked.connect(lambda: self.set_all_checked(True))
        self.btn_deselect_all.clicked.connect(lambda: self.set_all_checked(False))

        v.addLayout(toolbar)
        v.addWidget(self.table)

    def _on_item_changed(self, item):
        if item.column() == 0:
            self.selection_changed.emit(self.get_checked_count())

    def get_checked_indices(self) -> list:
        indices = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.checkState() == Qt.CheckState.Checked:
                indices.append(row)
        return indices

    def get_checked_count(self) -> int:
        return len(self.get_checked_indices())

    def set_all_checked(self, checked: bool):
        self.table.blockSignals(True)
        state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                item.setCheckState(state)
        self.table.blockSignals(False)
        self.selection_changed.emit(self.get_checked_count())

    def update_preview(self, file_list: list, generate_new_name_func, checked_indices: set = None):
        i18n = I18n.instance()
        self.table.blockSignals(True)
        self.table.setRowCount(len(file_list))

        if checked_indices is None:
            checked_indices = set(range(len(file_list)))

        seen_names = {}
        seq_index = 0

        for i, filename in enumerate(file_list):
            check_item = QTableWidgetItem()
            check_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            if i in checked_indices:
                check_item.setCheckState(Qt.CheckState.Checked)
            else:
                check_item.setCheckState(Qt.CheckState.Unchecked)
            self.table.setItem(i, 0, check_item)

            item_old = QTableWidgetItem(filename)

            if i in checked_indices:
                new_name = generate_new_name_func(filename, seq_index)
                seq_index += 1
                item_new = QTableWidgetItem(new_name)

                if new_name in seen_names:
                    status = i18n.tr("status_conflict")
                    color = QColor("#ffcdd2")
                    item_status = QTableWidgetItem(status)
                    item_status.setForeground(QColor("#c62828"))
                elif new_name == filename:
                    status = i18n.tr("status_no_change")
                    color = QColor("#fff9c4")
                    item_status = QTableWidgetItem(status)
                    item_status.setForeground(QColor("#f57f17"))
                else:
                    status = i18n.tr("status_ready")
                    color = QColor("#c8e6c9")
                    item_status = QTableWidgetItem(status)
                    item_status.setForeground(QColor("#2e7d32"))

                seen_names[new_name] = seen_names.get(new_name, 0) + 1
                item_new.setBackground(color)
                item_status.setBackground(color)
            else:
                item_new = QTableWidgetItem("—")
                item_status = QTableWidgetItem(i18n.tr("status_skip"))
                color = QColor("#f0f0f0")
                item_new.setForeground(QColor("#999999"))
                item_status.setForeground(QColor("#999999"))
                item_new.setBackground(color)
                item_status.setBackground(color)

            item_old.setBackground(QColor("#ffffff"))
            item_status.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(i, 1, item_old)
            self.table.setItem(i, 2, item_new)
            self.table.setItem(i, 3, item_status)

        self.table.blockSignals(False)

    def _retranslate(self):
        i18n = I18n.instance()
        self.setTitle(i18n.tr("preview"))
        self.btn_select_all.setText(i18n.tr("select_all"))
        self.btn_deselect_all.setText(i18n.tr("deselect_all"))
        self.table.setHorizontalHeaderLabels([
            i18n.tr("col_select"), i18n.tr("col_original"),
            i18n.tr("col_new"), i18n.tr("col_status")
        ])


class ActionButtons(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(16)
        self.setContentsMargins(0, 12, 0, 4)
        self._init_widgets()
        I18n.instance().language_changed.connect(self._retranslate)

    def _init_widgets(self):
        i18n = I18n.instance()

        self.btn_refresh = QPushButton(i18n.tr("btn_refresh"))
        self.btn_refresh.setFixedHeight(40)
        self.btn_refresh.setMinimumWidth(110)
        self.btn_refresh.setObjectName("btn_refresh")

        self.btn_execute = QPushButton(i18n.tr("btn_execute"))
        self.btn_execute.setFixedHeight(42)
        self.btn_execute.setMinimumWidth(150)
        self.btn_execute.setObjectName("btn_execute")

        self.btn_undo = QPushButton(i18n.tr("btn_undo"))
        self.btn_undo.setFixedHeight(42)
        self.btn_undo.setMinimumWidth(130)
        self.btn_undo.setObjectName("btn_undo")
        self.btn_undo.setEnabled(False)

        self.addWidget(self.btn_refresh)
        self.addStretch()
        self.addWidget(self.btn_undo)
        self.addWidget(self.btn_execute)

    def _retranslate(self):
        i18n = I18n.instance()
        self.btn_refresh.setText(i18n.tr("btn_refresh"))
        self.btn_execute.setText(i18n.tr("btn_execute"))
        self.btn_undo.setText(i18n.tr("btn_undo"))


class StyledDialog(QDialog):
    ICON_INFO = "info"
    ICON_SUCCESS = "success"
    ICON_WARNING = "warning"
    ICON_QUESTION = "question"

    _ICON_MAP = {
        "info": ("i", "#1a73e8", "#e8f0fe"),
        "success": ("✓", "#2e7d32", "#e8f5e9"),
        "warning": ("!", "#e65100", "#fff3e0"),
        "question": ("?", "#1a73e8", "#e8f0fe"),
    }

    def __init__(self, parent, title: str, message: str,
                 icon_type: str = "info",
                 buttons: list = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedWidth(440)
        self.setModal(True)
        self.result_value = False
        self._build_ui(title, message, icon_type, buttons or [I18n.instance().tr("ok")])

    def _build_ui(self, title, message, icon_type, buttons):
        colors = ThemeManager.instance().get_colors()

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {colors.card_background};
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        content = QWidget()
        content.setStyleSheet(f"background-color: {colors.card_background};")
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(12)
        content_layout.setContentsMargins(28, 28, 28, 20)

        icon_char, icon_color, icon_bg = self._ICON_MAP.get(icon_type, ("i", "#1a73e8", "#e8f0fe"))

        icon_label = QLabel(icon_char)
        icon_label.setFixedSize(52, 52)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"""
            QLabel {{
                background-color: {icon_bg};
                color: {icon_color};
                border-radius: 26px;
                font-size: 24px;
                font-weight: bold;
                border: 2px solid {icon_color}40;
            }}
        """)

        icon_row = QHBoxLayout()
        icon_row.addStretch()
        icon_row.addWidget(icon_label)
        icon_row.addStretch()
        content_layout.addLayout(icon_row)

        content_layout.addSpacing(4)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 17px;
                font-weight: bold;
                color: {colors.text_primary};
                padding: 0;
            }}
        """)
        content_layout.addWidget(title_label)

        msg_label = QLabel(message)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet(f"""
            QLabel {{
                font-size: 13px;
                color: {colors.text_secondary};
                padding: 4px 12px;
                line-height: 1.6;
            }}
        """)
        content_layout.addWidget(msg_label)

        layout.addWidget(content)

        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setStyleSheet(f"background-color: {colors.border_light};")
        layout.addWidget(separator)

        footer = QWidget()
        footer.setStyleSheet(f"background-color: {colors.surface_alt};")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(20, 14, 20, 14)
        footer_layout.setSpacing(12)
        footer_layout.addStretch()

        btn_style_primary = f"""
            QPushButton {{
                background-color: {colors.primary};
                color: {colors.text_on_primary};
                border: none;
                font-weight: bold;
                font-size: 13px;
                padding: 10px 28px;
                border-radius: 6px;
                min-width: 90px;
            }}
            QPushButton:hover {{
                background-color: {colors.primary_pressed};
            }}
            QPushButton:pressed {{
                background-color: {colors.primary_hover};
            }}
        """
        btn_style_secondary = f"""
            QPushButton {{
                background-color: {colors.card_background};
                color: {colors.text_secondary};
                border: 1px solid {colors.border};
                font-size: 13px;
                padding: 10px 28px;
                border-radius: 6px;
                min-width: 90px;
            }}
            QPushButton:hover {{
                background-color: {colors.surface_alt};
                border-color: {colors.primary};
                color: {colors.text_primary};
            }}
            QPushButton:pressed {{
                background-color: {colors.border_light};
            }}
        """

        if len(buttons) == 2:
            cancel_btn = QPushButton(buttons[1])
            cancel_btn.setStyleSheet(btn_style_secondary)
            cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            cancel_btn.clicked.connect(self._on_cancel)
            footer_layout.addWidget(cancel_btn)

            confirm_btn = QPushButton(buttons[0])
            confirm_btn.setStyleSheet(btn_style_primary)
            confirm_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            confirm_btn.clicked.connect(self._on_confirm)
            footer_layout.addWidget(confirm_btn)
        else:
            ok_btn = QPushButton(buttons[0])
            ok_btn.setStyleSheet(btn_style_primary)
            ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            ok_btn.clicked.connect(self._on_confirm)
            footer_layout.addWidget(ok_btn)

        layout.addWidget(footer)

    def _on_confirm(self):
        self.result_value = True
        self.accept()

    def _on_cancel(self):
        self.result_value = False
        self.reject()

    @staticmethod
    def show_info(parent, title, message):
        dlg = StyledDialog(parent, title, message, StyledDialog.ICON_INFO)
        dlg.exec()

    @staticmethod
    def show_success(parent, title, message):
        dlg = StyledDialog(parent, title, message, StyledDialog.ICON_SUCCESS)
        dlg.exec()

    @staticmethod
    def show_warning(parent, title, message):
        dlg = StyledDialog(parent, title, message, StyledDialog.ICON_WARNING)
        dlg.exec()

    @staticmethod
    def ask(parent, title, message) -> bool:
        i18n = I18n.instance()
        dlg = StyledDialog(parent, title, message, StyledDialog.ICON_QUESTION,
                           buttons=[i18n.tr("confirm"), i18n.tr("cancel")])
        dlg.exec()
        return dlg.result_value
