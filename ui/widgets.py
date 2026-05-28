from PyQt6.QtWidgets import (
    QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout,
    QPushButton, QLineEdit, QLabel, QSpinBox, QRadioButton,
    QButtonGroup, QCheckBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QWidget, QDialog, QFileDialog, QComboBox,
    QScrollArea, QFrame, QDateEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QDate
from PyQt6.QtGui import QColor, QFont
from themes.theme_manager import ThemeManager
from utils.i18n import I18n


class StyledSpinBox(QWidget):
    valueChanged = pyqtSignal(int)

    def __init__(self, minimum=0, maximum=99999, value=1):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.btn_minus = QPushButton("−")
        self.btn_minus.setObjectName("spin_btn_minus")
        self.btn_minus.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_minus.setFixedSize(36, 36)

        self.spin = QSpinBox()
        self.spin.setMinimum(minimum)
        self.spin.setMaximum(maximum)
        self.spin.setValue(value)
        self.spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.spin.setFixedWidth(70)

        self.btn_plus = QPushButton("+")
        self.btn_plus.setObjectName("spin_btn_plus")
        self.btn_plus.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_plus.setFixedSize(36, 36)

        layout.addWidget(self.btn_minus)
        layout.addWidget(self.spin)
        layout.addWidget(self.btn_plus)

        self.btn_minus.clicked.connect(self._decrement)
        self.btn_plus.clicked.connect(self._increment)
        self.spin.valueChanged.connect(self.valueChanged.emit)

    def _decrement(self):
        self.spin.setValue(self.spin.value() - 1)

    def _increment(self):
        self.spin.setValue(self.spin.value() + 1)

    def value(self):
        return self.spin.value()

    def setValue(self, v):
        self.spin.setValue(v)

    def setMinimum(self, v):
        self.spin.setMinimum(v)

    def setMaximum(self, v):
        self.spin.setMaximum(v)

    def setFixedWidth(self, w):
        pass


class FolderSelector(QGroupBox):
    include_subfolders_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__(I18n.instance().tr("folder_select"))
        self.folder_path_edit = QLineEdit()
        self.folder_path_edit.setReadOnly(True)
        self.folder_path_edit.setPlaceholderText(I18n.instance().tr("folder_placeholder"))
        self.browse_btn = QPushButton(I18n.instance().tr("browse"))
        self.browse_btn.setFixedWidth(90)
        self.include_subfolders_check = QCheckBox(I18n.instance().tr("include_subfolders"))
        self._setup_layout()
        I18n.instance().language_changed.connect(self._retranslate)
        self.include_subfolders_check.stateChanged.connect(
            lambda state: self.include_subfolders_changed.emit(state == Qt.CheckState.Checked.value)
        )

    def _setup_layout(self):
        v = QVBoxLayout(self)
        h = QHBoxLayout()
        self._path_label = QLabel(I18n.instance().tr("path_label"))
        h.addWidget(self._path_label)
        h.addWidget(self.folder_path_edit)
        h.addWidget(self.browse_btn)
        v.addLayout(h)
        v.addWidget(self.include_subfolders_check)

    def get_folder_path(self) -> str:
        return self.folder_path_edit.text()

    def set_folder_path(self, path: str) -> None:
        self.folder_path_edit.setText(path)

    def is_include_subfolders(self) -> bool:
        return self.include_subfolders_check.isChecked()

    def _retranslate(self):
        i18n = I18n.instance()
        self.setTitle(i18n.tr("folder_select"))
        self.folder_path_edit.setPlaceholderText(i18n.tr("folder_placeholder"))
        self.browse_btn.setText(i18n.tr("browse"))
        self._path_label.setText(i18n.tr("path_label"))
        self.include_subfolders_check.setText(i18n.tr("include_subfolders"))


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


class FileFilterPanel(QGroupBox):
    filter_changed = pyqtSignal()

    def __init__(self):
        super().__init__(I18n.instance().tr("filter_title"))
        self._setup_ui()
        I18n.instance().language_changed.connect(self._retranslate)

    def _setup_ui(self):
        i18n = I18n.instance()
        layout = QGridLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 16, 12, 12)

        self._label_ext = QLabel(i18n.tr("filter_extension"))
        self.ext_edit = QLineEdit()
        self.ext_edit.setPlaceholderText(i18n.tr("filter_extension_placeholder"))
        layout.addWidget(self._label_ext, 0, 0)
        layout.addWidget(self.ext_edit, 0, 1, 1, 3)

        self._label_size_min = QLabel(i18n.tr("filter_size_min"))
        self.size_min_spin = QSpinBox()
        self.size_min_spin.setMinimum(0)
        self.size_min_spin.setMaximum(9999999)
        self.size_min_spin.setValue(0)
        self.size_min_spin.setFixedWidth(100)
        self.size_min_spin.setSpecialValueText("-")

        self._label_size_max = QLabel(i18n.tr("filter_size_max"))
        self.size_max_spin = QSpinBox()
        self.size_max_spin.setMinimum(0)
        self.size_max_spin.setMaximum(9999999)
        self.size_max_spin.setValue(0)
        self.size_max_spin.setFixedWidth(100)
        self.size_max_spin.setSpecialValueText("-")

        size_row = QHBoxLayout()
        size_row.addWidget(self._label_size_min)
        size_row.addWidget(self.size_min_spin)
        size_row.addSpacing(16)
        size_row.addWidget(self._label_size_max)
        size_row.addWidget(self.size_max_spin)
        size_row.addStretch()
        layout.addLayout(size_row, 1, 0, 1, 4)

        self._label_date_from = QLabel(i18n.tr("filter_date_from"))
        self.date_from_edit = QDateEdit()
        self.date_from_edit.setCalendarPopup(True)
        self.date_from_edit.setDate(QDate(2000, 1, 1))
        self.date_from_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_from_edit.setFixedWidth(130)

        self._label_date_to = QLabel(i18n.tr("filter_date_to"))
        self.date_to_edit = QDateEdit()
        self.date_to_edit.setCalendarPopup(True)
        self.date_to_edit.setDate(QDate.currentDate())
        self.date_to_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_to_edit.setFixedWidth(130)

        date_row = QHBoxLayout()
        date_row.addWidget(self._label_date_from)
        date_row.addWidget(self.date_from_edit)
        date_row.addSpacing(16)
        date_row.addWidget(self._label_date_to)
        date_row.addWidget(self.date_to_edit)
        date_row.addStretch()
        layout.addLayout(date_row, 2, 0, 1, 4)

        btn_row = QHBoxLayout()
        self.btn_apply = QPushButton(i18n.tr("filter_apply"))
        self.btn_apply.setFixedHeight(30)
        self.btn_apply.setMinimumWidth(90)
        self.btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_clear = QPushButton(i18n.tr("filter_clear"))
        self.btn_clear.setFixedHeight(30)
        self.btn_clear.setMinimumWidth(90)
        self.btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_row.addStretch()
        btn_row.addWidget(self.btn_apply)
        btn_row.addWidget(self.btn_clear)
        layout.addLayout(btn_row, 3, 0, 1, 4)

        self.btn_apply.clicked.connect(self._on_apply)
        self.btn_clear.clicked.connect(self._on_clear)

    def _on_apply(self):
        self.filter_changed.emit()

    def _on_clear(self):
        self.ext_edit.clear()
        self.size_min_spin.setValue(0)
        self.size_max_spin.setValue(0)
        self.date_from_edit.setDate(QDate(2000, 1, 1))
        self.date_to_edit.setDate(QDate.currentDate())
        self.filter_changed.emit()

    def get_extension_filter(self) -> list:
        text = self.ext_edit.text().strip()
        if not text:
            return []
        exts = [e.strip().lower() for e in text.split(",") if e.strip()]
        result = []
        for ext in exts:
            if not ext.startswith("."):
                ext = "." + ext
            result.append(ext)
        return result

    def get_size_range(self) -> tuple:
        min_kb = self.size_min_spin.value()
        max_kb = self.size_max_spin.value()
        return (min_kb, max_kb)

    def get_date_range(self) -> tuple:
        from_date = self.date_from_edit.date()
        to_date = self.date_to_edit.date()
        return (from_date, to_date)

    def has_active_filter(self) -> bool:
        if self.ext_edit.text().strip():
            return True
        if self.size_min_spin.value() > 0 or self.size_max_spin.value() > 0:
            return True
        if self.date_from_edit.date() != QDate(2000, 1, 1):
            return True
        if self.date_to_edit.date() != QDate.currentDate():
            return True
        return False

    def _retranslate(self):
        i18n = I18n.instance()
        self.setTitle(i18n.tr("filter_title"))
        self._label_ext.setText(i18n.tr("filter_extension"))
        self.ext_edit.setPlaceholderText(i18n.tr("filter_extension_placeholder"))
        self._label_size_min.setText(i18n.tr("filter_size_min"))
        self._label_size_max.setText(i18n.tr("filter_size_max"))
        self._label_date_from.setText(i18n.tr("filter_date_from"))
        self._label_date_to.setText(i18n.tr("filter_date_to"))
        self.btn_apply.setText(i18n.tr("filter_apply"))
        self.btn_clear.setText(i18n.tr("filter_clear"))


class RenameModePanel(QGroupBox):
    mode_changed = pyqtSignal()

    def __init__(self):
        super().__init__(I18n.instance().tr("rename_rules"))
        self.mode_group = QButtonGroup(self)
        self._init_widgets()
        self._setup_layout()
        self._update_visibility()
        self.mode_group.idClicked.connect(self._update_visibility)
        self.mode_group.idClicked.connect(lambda: self.mode_changed.emit())
        I18n.instance().language_changed.connect(self._retranslate)

    def _init_widgets(self):
        i18n = I18n.instance()
        self.radio_prefix_suffix = QRadioButton(i18n.tr("mode_prefix_suffix"))
        self.radio_sequential = QRadioButton(i18n.tr("mode_sequential"))
        self.radio_replace = QRadioButton(i18n.tr("mode_replace"))
        self.radio_direct_input = QRadioButton(i18n.tr("mode_direct_input"))
        self.radio_regex = QRadioButton(i18n.tr("mode_regex"))
        self.radio_datetime = QRadioButton(i18n.tr("mode_datetime"))
        self.radio_attributes = QRadioButton(i18n.tr("mode_attributes"))
        self.radio_seq_enhanced = QRadioButton(i18n.tr("mode_seq_enhanced"))
        self.radio_prefix_suffix.setChecked(True)

        self.mode_group.addButton(self.radio_prefix_suffix, 0)
        self.mode_group.addButton(self.radio_sequential, 1)
        self.mode_group.addButton(self.radio_replace, 2)
        self.mode_group.addButton(self.radio_direct_input, 3)
        self.mode_group.addButton(self.radio_regex, 4)
        self.mode_group.addButton(self.radio_datetime, 5)
        self.mode_group.addButton(self.radio_attributes, 6)
        self.mode_group.addButton(self.radio_seq_enhanced, 7)

        # Mode 0: Prefix/Suffix
        self.prefix_edit = QLineEdit()
        self.prefix_edit.setPlaceholderText(i18n.tr("prefix_placeholder"))
        self.suffix_edit = QLineEdit()
        self.suffix_edit.setPlaceholderText(i18n.tr("suffix_placeholder"))

        # Mode 1: Sequential
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

        # Mode 2: Find & Replace
        self.find_edit = QLineEdit()
        self.find_edit.setPlaceholderText(i18n.tr("find_placeholder"))
        self.replace_edit = QLineEdit()
        self.replace_edit.setPlaceholderText(i18n.tr("replace_placeholder"))
        self.case_sensitive_check = QCheckBox(i18n.tr("case_sensitive"))
        self.case_sensitive_check.setChecked(True)

        # Mode 3: Direct Input
        self.direct_name_edit = QLineEdit()
        self.direct_name_edit.setPlaceholderText(i18n.tr("direct_name_placeholder"))

        # Mode 4: Regex
        self.regex_pattern_edit = QLineEdit()
        self.regex_pattern_edit.setPlaceholderText(i18n.tr("regex_pattern_placeholder"))
        self.regex_replace_edit = QLineEdit()
        self.regex_replace_edit.setPlaceholderText(i18n.tr("regex_replace_placeholder"))
        self._regex_hint_label = QLabel(i18n.tr("regex_hint"))
        self._regex_hint_label.setObjectName("hint_label")

        # Mode 5: Datetime
        self.datetime_format_edit = QLineEdit()
        self.datetime_format_edit.setPlaceholderText(i18n.tr("datetime_format_placeholder"))
        self.datetime_format_edit.setText("IMG_{Y}{M}{D}_{h}{m}{s}")
        self.datetime_source_combo = QComboBox()
        self.datetime_source_combo.addItem(i18n.tr("datetime_modified"), "modified")
        self.datetime_source_combo.addItem(i18n.tr("datetime_created"), "created")
        self._datetime_hint_label = QLabel(i18n.tr("datetime_hint"))
        self._datetime_hint_label.setObjectName("hint_label")

        # Mode 6: Attributes
        self.attr_template_edit = QLineEdit()
        self.attr_template_edit.setPlaceholderText(i18n.tr("attr_template_placeholder"))
        self.attr_template_edit.setText("{name}_{size}")
        self._attr_hint_label = QLabel(i18n.tr("attr_hint"))
        self._attr_hint_label.setObjectName("hint_label")

        # Mode 7: Enhanced Sequence
        self.seq_enh_prefix_edit = QLineEdit()
        self.seq_enh_prefix_edit.setPlaceholderText(i18n.tr("seq_enh_prefix_placeholder"))
        self.seq_enh_suffix_edit = QLineEdit()
        self.seq_enh_suffix_edit.setPlaceholderText(i18n.tr("seq_enh_suffix_placeholder"))

        self.seq_enh_start_spin = QSpinBox()
        self.seq_enh_start_spin.setMinimum(0)
        self.seq_enh_start_spin.setMaximum(99999)
        self.seq_enh_start_spin.setValue(1)
        self.seq_enh_start_spin.setFixedWidth(100)

        self.seq_enh_step_spin = QSpinBox()
        self.seq_enh_step_spin.setMinimum(1)
        self.seq_enh_step_spin.setMaximum(100)
        self.seq_enh_step_spin.setValue(1)
        self.seq_enh_step_spin.setFixedWidth(100)

        self.seq_enh_digits_spin = QSpinBox()
        self.seq_enh_digits_spin.setMinimum(1)
        self.seq_enh_digits_spin.setMaximum(10)
        self.seq_enh_digits_spin.setValue(3)
        self.seq_enh_digits_spin.setFixedWidth(100)

        self.seq_enh_format_combo = QComboBox()
        self.seq_enh_format_combo.addItem(i18n.tr("seq_enh_decimal"), "decimal")
        self.seq_enh_format_combo.addItem(i18n.tr("seq_enh_roman"), "roman")
        self.seq_enh_format_combo.addItem(i18n.tr("seq_enh_alpha_upper"), "alpha_upper")
        self.seq_enh_format_combo.addItem(i18n.tr("seq_enh_alpha_lower"), "alpha_lower")
        self.seq_enh_format_combo.addItem(i18n.tr("seq_enh_hex"), "hex")

    def _setup_layout(self):
        i18n = I18n.instance()
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        # Mode selector row (two rows of 4 radio buttons)
        mode_row1 = QHBoxLayout()
        mode_row1.setSpacing(16)
        mode_row1.addWidget(self.radio_prefix_suffix)
        mode_row1.addWidget(self.radio_sequential)
        mode_row1.addWidget(self.radio_replace)
        mode_row1.addWidget(self.radio_direct_input)
        mode_row1.addStretch()

        mode_row2 = QHBoxLayout()
        mode_row2.setSpacing(16)
        mode_row2.addWidget(self.radio_regex)
        mode_row2.addWidget(self.radio_datetime)
        mode_row2.addWidget(self.radio_attributes)
        mode_row2.addWidget(self.radio_seq_enhanced)
        mode_row2.addStretch()

        main_layout.addLayout(mode_row1)
        main_layout.addLayout(mode_row2)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(sep)

        # Parameters area
        self._params_widget = QWidget()
        params_grid = QGridLayout(self._params_widget)
        params_grid.setSpacing(8)
        params_grid.setContentsMargins(0, 0, 0, 0)

        # Mode 0: Prefix/Suffix
        self._label_prefix = QLabel(i18n.tr("prefix"))
        params_grid.addWidget(self._label_prefix, 0, 0)
        params_grid.addWidget(self.prefix_edit, 0, 1, 1, 3)
        self._label_suffix = QLabel(i18n.tr("suffix"))
        params_grid.addWidget(self._label_suffix, 1, 0)
        params_grid.addWidget(self.suffix_edit, 1, 1, 1, 3)

        # Mode 1: Sequential
        self._label_start_num = QLabel(i18n.tr("start_num"))
        params_grid.addWidget(self._label_start_num, 2, 0)
        params_grid.addWidget(self.start_num_spin, 2, 1)

        self._label_digits = QLabel(i18n.tr("digits"))
        digits_layout = QHBoxLayout()
        digits_layout.setContentsMargins(0, 0, 0, 0)
        digits_layout.addWidget(self._label_digits)
        digits_layout.addWidget(self.digits_spin)
        digits_layout.addStretch()
        self._digits_widget = QWidget()
        self._digits_widget.setLayout(digits_layout)
        params_grid.addWidget(self._digits_widget, 2, 2)

        self._label_seq_prefix = QLabel(i18n.tr("seq_prefix"))
        params_grid.addWidget(self._label_seq_prefix, 3, 0)
        params_grid.addWidget(self.seq_prefix_edit, 3, 1, 1, 3)

        # Mode 2: Find & Replace
        self._label_find = QLabel(i18n.tr("find"))
        params_grid.addWidget(self._label_find, 4, 0)
        params_grid.addWidget(self.find_edit, 4, 1, 1, 3)
        self._label_replace = QLabel(i18n.tr("replace"))
        params_grid.addWidget(self._label_replace, 5, 0)
        params_grid.addWidget(self.replace_edit, 5, 1, 1, 3)
        params_grid.addWidget(self.case_sensitive_check, 6, 1)

        # Mode 3: Direct Input
        self._label_direct_name = QLabel(i18n.tr("new_filename"))
        params_grid.addWidget(self._label_direct_name, 7, 0)
        params_grid.addWidget(self.direct_name_edit, 7, 1, 1, 3)

        # Mode 4: Regex
        self._label_regex_pattern = QLabel(i18n.tr("regex_pattern"))
        params_grid.addWidget(self._label_regex_pattern, 8, 0)
        params_grid.addWidget(self.regex_pattern_edit, 8, 1, 1, 3)
        self._label_regex_replace = QLabel(i18n.tr("regex_replace"))
        params_grid.addWidget(self._label_regex_replace, 9, 0)
        params_grid.addWidget(self.regex_replace_edit, 9, 1, 1, 3)
        params_grid.addWidget(self._regex_hint_label, 10, 1, 1, 3)

        # Mode 5: Datetime
        self._label_datetime_format = QLabel(i18n.tr("datetime_format"))
        params_grid.addWidget(self._label_datetime_format, 11, 0)
        params_grid.addWidget(self.datetime_format_edit, 11, 1, 1, 3)
        self._label_datetime_source = QLabel(i18n.tr("datetime_source"))
        params_grid.addWidget(self._label_datetime_source, 12, 0)
        params_grid.addWidget(self.datetime_source_combo, 12, 1)
        params_grid.addWidget(self._datetime_hint_label, 13, 1, 1, 3)

        # Mode 6: Attributes
        self._label_attr_template = QLabel(i18n.tr("attr_template"))
        params_grid.addWidget(self._label_attr_template, 14, 0)
        params_grid.addWidget(self.attr_template_edit, 14, 1, 1, 3)
        params_grid.addWidget(self._attr_hint_label, 15, 1, 1, 3)

        # Mode 7: Enhanced Sequence
        self._label_seq_enh_prefix = QLabel(i18n.tr("seq_enh_prefix"))
        params_grid.addWidget(self._label_seq_enh_prefix, 16, 0)
        params_grid.addWidget(self.seq_enh_prefix_edit, 16, 1, 1, 3)
        self._label_seq_enh_suffix = QLabel(i18n.tr("seq_enh_suffix"))
        params_grid.addWidget(self._label_seq_enh_suffix, 17, 0)
        params_grid.addWidget(self.seq_enh_suffix_edit, 17, 1, 1, 3)

        seq_enh_row = QHBoxLayout()
        self._label_seq_enh_start = QLabel(i18n.tr("seq_enh_start"))
        seq_enh_row.addWidget(self._label_seq_enh_start)
        seq_enh_row.addWidget(self.seq_enh_start_spin)
        self._label_seq_enh_step = QLabel(i18n.tr("seq_enh_step"))
        seq_enh_row.addWidget(self._label_seq_enh_step)
        seq_enh_row.addWidget(self.seq_enh_step_spin)
        self._label_seq_enh_digits = QLabel(i18n.tr("seq_enh_digits"))
        seq_enh_row.addWidget(self._label_seq_enh_digits)
        seq_enh_row.addWidget(self.seq_enh_digits_spin)
        seq_enh_row.addStretch()
        self._seq_enh_row_widget = QWidget()
        self._seq_enh_row_widget.setLayout(seq_enh_row)
        params_grid.addWidget(self._seq_enh_row_widget, 18, 0, 1, 4)

        seq_enh_fmt_row = QHBoxLayout()
        self._label_seq_enh_format = QLabel(i18n.tr("seq_enh_format"))
        seq_enh_fmt_row.addWidget(self._label_seq_enh_format)
        seq_enh_fmt_row.addWidget(self.seq_enh_format_combo)
        seq_enh_fmt_row.addStretch()
        self._seq_enh_fmt_widget = QWidget()
        self._seq_enh_fmt_widget.setLayout(seq_enh_fmt_row)
        params_grid.addWidget(self._seq_enh_fmt_widget, 19, 0, 1, 4)

        main_layout.addWidget(self._params_widget)

    def _update_visibility(self):
        mode = self.mode_group.checkedId()

        # Mode 0: Prefix/Suffix
        prefix_suffix_visible = (mode == 0)
        self._label_prefix.setVisible(prefix_suffix_visible)
        self.prefix_edit.setVisible(prefix_suffix_visible)
        self._label_suffix.setVisible(prefix_suffix_visible)
        self.suffix_edit.setVisible(prefix_suffix_visible)

        # Mode 1: Sequential
        sequential_visible = (mode == 1)
        self._label_start_num.setVisible(sequential_visible)
        self.start_num_spin.setVisible(sequential_visible)
        self._digits_widget.setVisible(sequential_visible)
        self._label_seq_prefix.setVisible(sequential_visible)
        self.seq_prefix_edit.setVisible(sequential_visible)

        # Mode 2: Find & Replace
        replace_visible = (mode == 2)
        self._label_find.setVisible(replace_visible)
        self.find_edit.setVisible(replace_visible)
        self._label_replace.setVisible(replace_visible)
        self.replace_edit.setVisible(replace_visible)
        self.case_sensitive_check.setVisible(replace_visible)

        # Mode 3: Direct Input
        direct_visible = (mode == 3)
        self._label_direct_name.setVisible(direct_visible)
        self.direct_name_edit.setVisible(direct_visible)

        # Mode 4: Regex
        regex_visible = (mode == 4)
        self._label_regex_pattern.setVisible(regex_visible)
        self.regex_pattern_edit.setVisible(regex_visible)
        self._label_regex_replace.setVisible(regex_visible)
        self.regex_replace_edit.setVisible(regex_visible)
        self._regex_hint_label.setVisible(regex_visible)

        # Mode 5: Datetime
        datetime_visible = (mode == 5)
        self._label_datetime_format.setVisible(datetime_visible)
        self.datetime_format_edit.setVisible(datetime_visible)
        self._label_datetime_source.setVisible(datetime_visible)
        self.datetime_source_combo.setVisible(datetime_visible)
        self._datetime_hint_label.setVisible(datetime_visible)

        # Mode 6: Attributes
        attr_visible = (mode == 6)
        self._label_attr_template.setVisible(attr_visible)
        self.attr_template_edit.setVisible(attr_visible)
        self._attr_hint_label.setVisible(attr_visible)

        # Mode 7: Enhanced Sequence
        seq_enh_visible = (mode == 7)
        self._label_seq_enh_prefix.setVisible(seq_enh_visible)
        self.seq_enh_prefix_edit.setVisible(seq_enh_visible)
        self._label_seq_enh_suffix.setVisible(seq_enh_visible)
        self.seq_enh_suffix_edit.setVisible(seq_enh_visible)
        self._seq_enh_row_widget.setVisible(seq_enh_visible)
        self._seq_enh_fmt_widget.setVisible(seq_enh_visible)

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
        self.radio_regex.setText(i18n.tr("mode_regex"))
        self.radio_datetime.setText(i18n.tr("mode_datetime"))
        self.radio_attributes.setText(i18n.tr("mode_attributes"))
        self.radio_seq_enhanced.setText(i18n.tr("mode_seq_enhanced"))
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
        self._label_regex_pattern.setText(i18n.tr("regex_pattern"))
        self.regex_pattern_edit.setPlaceholderText(i18n.tr("regex_pattern_placeholder"))
        self._label_regex_replace.setText(i18n.tr("regex_replace"))
        self.regex_replace_edit.setPlaceholderText(i18n.tr("regex_replace_placeholder"))
        self._regex_hint_label.setText(i18n.tr("regex_hint"))
        self._label_datetime_format.setText(i18n.tr("datetime_format"))
        self.datetime_format_edit.setPlaceholderText(i18n.tr("datetime_format_placeholder"))
        self._label_datetime_source.setText(i18n.tr("datetime_source"))
        self.datetime_source_combo.setItemText(0, i18n.tr("datetime_modified"))
        self.datetime_source_combo.setItemText(1, i18n.tr("datetime_created"))
        self._datetime_hint_label.setText(i18n.tr("datetime_hint"))
        self._label_attr_template.setText(i18n.tr("attr_template"))
        self.attr_template_edit.setPlaceholderText(i18n.tr("attr_template_placeholder"))
        self._attr_hint_label.setText(i18n.tr("attr_hint"))
        self._label_seq_enh_prefix.setText(i18n.tr("seq_enh_prefix"))
        self.seq_enh_prefix_edit.setPlaceholderText(i18n.tr("seq_enh_prefix_placeholder"))
        self._label_seq_enh_suffix.setText(i18n.tr("seq_enh_suffix"))
        self.seq_enh_suffix_edit.setPlaceholderText(i18n.tr("seq_enh_suffix_placeholder"))
        self._label_seq_enh_start.setText(i18n.tr("seq_enh_start"))
        self._label_seq_enh_step.setText(i18n.tr("seq_enh_step"))
        self._label_seq_enh_digits.setText(i18n.tr("seq_enh_digits"))
        self._label_seq_enh_format.setText(i18n.tr("seq_enh_format"))
        self.seq_enh_format_combo.setItemText(0, i18n.tr("seq_enh_decimal"))
        self.seq_enh_format_combo.setItemText(1, i18n.tr("seq_enh_roman"))
        self.seq_enh_format_combo.setItemText(2, i18n.tr("seq_enh_alpha_upper"))
        self.seq_enh_format_combo.setItemText(3, i18n.tr("seq_enh_alpha_lower"))
        self.seq_enh_format_combo.setItemText(4, i18n.tr("seq_enh_hex"))


class PreviewTable(QGroupBox):
    selection_changed = pyqtSignal(int)
    name_manually_edited = pyqtSignal(int, str)

    def __init__(self):
        super().__init__(I18n.instance().tr("preview"))
        self.table = QTableWidget()
        self._show_folder_column = False
        self._manual_edits = {}
        self._editing_enabled = True
        self._setup_table()
        self._setup_layout()
        self.table.itemChanged.connect(self._on_item_changed)
        self.table.cellDoubleClicked.connect(self._on_cell_double_clicked)
        I18n.instance().language_changed.connect(self._retranslate)

    def _setup_table(self):
        i18n = I18n.instance()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            i18n.tr("col_select"), i18n.tr("col_original"),
            i18n.tr("col_new"), i18n.tr("col_status"), i18n.tr("col_folder")
        ])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnHidden(4, True)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

    def set_show_folder_column(self, show: bool):
        self._show_folder_column = show
        self.table.setColumnHidden(4, not show)

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
        self._edit_hint_label = QLabel(I18n.instance().tr("edit_name_hint"))
        self._edit_hint_label.setObjectName("hint_label")
        self._edit_hint_label.setStyleSheet("color: #888; font-size: 11px;")
        toolbar.addWidget(self._edit_hint_label)

        self.btn_select_all.clicked.connect(lambda: self.set_all_checked(True))
        self.btn_deselect_all.clicked.connect(lambda: self.set_all_checked(False))

        v.addLayout(toolbar)
        v.addWidget(self.table)

    def _on_item_changed(self, item):
        if item.column() == 0:
            self.selection_changed.emit(self.get_checked_count())
        elif item.column() == 2 and self._editing_enabled:
            row = item.row()
            new_text = item.text().strip()
            if new_text and new_text != "—":
                self._manual_edits[row] = new_text
                self.name_manually_edited.emit(row, new_text)

    def _on_cell_double_clicked(self, row, column):
        if column == 2:
            check_item = self.table.item(row, 0)
            if check_item and check_item.checkState() == Qt.CheckState.Checked:
                item = self.table.item(row, 2)
                if item:
                    self.table.editItem(item)

    def get_manual_edits(self) -> dict:
        return self._manual_edits.copy()

    def clear_manual_edits(self):
        self._manual_edits = {}

    def has_manual_edit(self, row: int) -> bool:
        return row in self._manual_edits

    def get_manual_edit(self, row: int) -> str:
        return self._manual_edits.get(row, "")

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

    def update_preview(self, file_list: list, generate_new_name_func,
                       checked_indices: set = None, rel_paths: list = None):
        i18n = I18n.instance()
        self._editing_enabled = False
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
                if i in self._manual_edits:
                    new_name = self._manual_edits[i]
                else:
                    new_name = generate_new_name_func(filename, seq_index)
                seq_index += 1
                item_new = QTableWidgetItem(new_name)
                item_new.setFlags(item_new.flags() | Qt.ItemFlag.ItemIsEditable)

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

                if i in self._manual_edits:
                    item_new.setForeground(QColor("#1565c0"))
                    font = item_new.font()
                    font.setBold(True)
                    item_new.setFont(font)

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
                item_new.setFlags(item_new.flags() & ~Qt.ItemFlag.ItemIsEditable)

            item_old.setBackground(QColor("#ffffff"))
            item_status.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(i, 1, item_old)
            self.table.setItem(i, 2, item_new)
            self.table.setItem(i, 3, item_status)

            # Folder column
            folder_text = ""
            if rel_paths and i < len(rel_paths):
                folder_text = rel_paths[i]
            item_folder = QTableWidgetItem(folder_text)
            item_folder.setForeground(QColor("#888888"))
            self.table.setItem(i, 4, item_folder)

        self.table.blockSignals(False)
        self._editing_enabled = True

    def _retranslate(self):
        i18n = I18n.instance()
        self.setTitle(i18n.tr("preview"))
        self.btn_select_all.setText(i18n.tr("select_all"))
        self.btn_deselect_all.setText(i18n.tr("deselect_all"))
        self._edit_hint_label.setText(i18n.tr("edit_name_hint"))
        self.table.setHorizontalHeaderLabels([
            i18n.tr("col_select"), i18n.tr("col_original"),
            i18n.tr("col_new"), i18n.tr("col_status"), i18n.tr("col_folder")
        ])


class ActionButtons(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(12)
        self.setContentsMargins(0, 12, 0, 4)
        self._init_widgets()
        I18n.instance().language_changed.connect(self._retranslate)

    def _init_widgets(self):
        i18n = I18n.instance()

        self.btn_refresh = QPushButton(i18n.tr("btn_refresh"))
        self.btn_refresh.setFixedHeight(40)
        self.btn_refresh.setMinimumWidth(110)
        self.btn_refresh.setObjectName("btn_refresh")
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_preview_detail = QPushButton(i18n.tr("btn_preview_detail"))
        self.btn_preview_detail.setFixedHeight(40)
        self.btn_preview_detail.setMinimumWidth(120)
        self.btn_preview_detail.setObjectName("btn_preview_detail")
        self.btn_preview_detail.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_execute = QPushButton(i18n.tr("btn_execute"))
        self.btn_execute.setFixedHeight(42)
        self.btn_execute.setMinimumWidth(140)
        self.btn_execute.setObjectName("btn_execute")
        self.btn_execute.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_undo = QPushButton(i18n.tr("btn_undo"))
        self.btn_undo.setFixedHeight(42)
        self.btn_undo.setMinimumWidth(120)
        self.btn_undo.setObjectName("btn_undo")
        self.btn_undo.setEnabled(False)
        self.btn_undo.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_undo_all = QPushButton(i18n.tr("btn_undo_all"))
        self.btn_undo_all.setFixedHeight(42)
        self.btn_undo_all.setMinimumWidth(120)
        self.btn_undo_all.setObjectName("btn_undo")
        self.btn_undo_all.setEnabled(False)
        self.btn_undo_all.setCursor(Qt.CursorShape.PointingHandCursor)

        self.addWidget(self.btn_refresh)
        self.addWidget(self.btn_preview_detail)
        self.addStretch()
        self.addWidget(self.btn_undo_all)
        self.addWidget(self.btn_undo)
        self.addWidget(self.btn_execute)

    def _retranslate(self):
        i18n = I18n.instance()
        self.btn_refresh.setText(i18n.tr("btn_refresh"))
        self.btn_execute.setText(i18n.tr("btn_execute"))
        self.btn_undo.setText(i18n.tr("btn_undo"))
        self.btn_preview_detail.setText(i18n.tr("btn_preview_detail"))
        self.btn_undo_all.setText(i18n.tr("btn_undo_all"))


class PreviewDialog(QDialog):
    def __init__(self, parent, rename_map: list):
        super().__init__(parent)
        self._rename_map = rename_map
        self._build_ui()

    def _build_ui(self):
        i18n = I18n.instance()
        colors = ThemeManager.instance().get_colors()

        self.setWindowTitle(i18n.tr("preview_dialog_title"))
        self.setMinimumSize(700, 500)
        self.setModal(True)

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {colors.page_background};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # Header
        header = QLabel(i18n.tr("preview_dialog_title"))
        header.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {colors.primary};
            }}
        """)
        layout.addWidget(header)

        subtitle = QLabel(i18n.tr("preview_total", count=len(self._rename_map)))
        subtitle.setStyleSheet(f"""
            QLabel {{
                font-size: 13px;
                color: {colors.text_secondary};
            }}
        """)
        layout.addWidget(subtitle)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["#", i18n.tr("col_original"), i18n.tr("col_new")])
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 50)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        self.table.setRowCount(len(self._rename_map))
        for i, (old_name, new_name) in enumerate(self._rename_map):
            idx_item = QTableWidgetItem(str(i + 1))
            idx_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 0, idx_item)
            self.table.setItem(i, 1, QTableWidgetItem(old_name))
            new_item = QTableWidgetItem(new_name)
            new_item.setForeground(QColor(colors.primary))
            self.table.setItem(i, 2, new_item)

        layout.addWidget(self.table)

        # Footer buttons
        footer = QHBoxLayout()
        footer.addStretch()

        btn_close = QPushButton(i18n.tr("ok"))
        btn_close.setFixedHeight(36)
        btn_close.setMinimumWidth(100)
        btn_close.setObjectName("btn_execute")
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.accept)
        footer.addWidget(btn_close)
        layout.addLayout(footer)


class StyledDialog(QDialog):
    ICON_INFO = "info"
    ICON_SUCCESS = "success"
    ICON_WARNING = "warning"
    ICON_QUESTION = "question"

    _ICON_MAP = {
        "info": ("ℹ", "#1a73e8", "#e8f0fe"),
        "success": ("✓", "#2e7d32", "#e8f5e9"),
        "warning": ("⚠", "#e65100", "#fff3e0"),
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

        icon_char, icon_color, icon_bg = self._ICON_MAP.get(icon_type, ("ℹ", "#1a73e8", "#e8f0fe"))

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
