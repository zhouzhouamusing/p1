from PyQt6.QtWidgets import (
    QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout,
    QPushButton, QLineEdit, QLabel, QSpinBox, QRadioButton,
    QButtonGroup, QCheckBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class FolderSelector(QGroupBox):
    def __init__(self):
        super().__init__("📁 文件夹选择")
        self.folder_path_edit = QLineEdit()
        self.folder_path_edit.setReadOnly(True)
        self.folder_path_edit.setPlaceholderText("请选择文件夹...")
        self.browse_btn = QPushButton("浏览...")
        self.browse_btn.setFixedWidth(80)
        self._setup_layout()

    def _setup_layout(self):
        h = QHBoxLayout(self)
        h.addWidget(QLabel("路径:"))
        h.addWidget(self.folder_path_edit)
        h.addWidget(self.browse_btn)

    def get_folder_path(self) -> str:
        return self.folder_path_edit.text()

    def set_folder_path(self, path: str) -> None:
        self.folder_path_edit.setText(path)


class RenameModePanel(QGroupBox):
    def __init__(self):
        super().__init__("⚙️ 重命名规则")
        self.mode_group = QButtonGroup(self)
        self._init_widgets()
        self._setup_layout()

    def _init_widgets(self):
        self.radio_prefix_suffix = QRadioButton("添加前缀/后缀")
        self.radio_sequential = QRadioButton("数字序号命名")
        self.radio_replace = QRadioButton("查找替换")
        self.radio_prefix_suffix.setChecked(True)

        self.mode_group.addButton(self.radio_prefix_suffix, 0)
        self.mode_group.addButton(self.radio_sequential, 1)
        self.mode_group.addButton(self.radio_replace, 2)

        self.prefix_edit = QLineEdit()
        self.prefix_edit.setPlaceholderText("输入前缀")
        self.suffix_edit = QLineEdit()
        self.suffix_edit.setPlaceholderText("输入后缀（不含扩展名）")

        self.start_num_spin = QSpinBox()
        self.start_num_spin.setMinimum(0)
        self.start_num_spin.setMaximum(99999)
        self.start_num_spin.setValue(1)

        self.digits_spin = QSpinBox()
        self.digits_spin.setMinimum(1)
        self.digits_spin.setMaximum(10)
        self.digits_spin.setValue(3)

        self.seq_prefix_edit = QLineEdit()
        self.seq_prefix_edit.setPlaceholderText("序号前缀（可选）")

        self.find_edit = QLineEdit()
        self.find_edit.setPlaceholderText("查找内容")
        self.replace_edit = QLineEdit()
        self.replace_edit.setPlaceholderText("替换为")

        self.case_sensitive_check = QCheckBox("区分大小写")
        self.case_sensitive_check.setChecked(True)

    def _setup_layout(self):
        grid = QGridLayout(self)
        grid.setSpacing(8)

        grid.addWidget(self.radio_prefix_suffix, 0, 0)
        grid.addWidget(self.radio_sequential, 0, 1)
        grid.addWidget(self.radio_replace, 0, 2)

        grid.addWidget(QLabel("前缀:"), 1, 0)
        grid.addWidget(self.prefix_edit, 1, 1, 1, 2)
        grid.addWidget(QLabel("后缀:"), 2, 0)
        grid.addWidget(self.suffix_edit, 2, 1, 1, 2)

        grid.addWidget(QLabel("起始序号:"), 3, 0)
        grid.addWidget(self.start_num_spin, 3, 1)

        digits_layout = QHBoxLayout()
        digits_layout.addWidget(QLabel("位数:"))
        digits_layout.addWidget(self.digits_spin)
        digits_widget = QWidget()
        digits_widget.setLayout(digits_layout)
        grid.addWidget(digits_widget, 3, 2)

        grid.addWidget(QLabel("序号前缀:"), 4, 0)
        grid.addWidget(self.seq_prefix_edit, 4, 1, 1, 2)

        grid.addWidget(QLabel("查找:"), 5, 0)
        grid.addWidget(self.find_edit, 5, 1, 1, 2)
        grid.addWidget(QLabel("替换:"), 6, 0)
        grid.addWidget(self.replace_edit, 6, 1, 1, 2)

        grid.addWidget(self.case_sensitive_check, 7, 1)


class PreviewTable(QGroupBox):
    def __init__(self):
        super().__init__("👁️ 预览（实时）")
        self.table = QTableWidget()
        self._setup_table()
        self._setup_layout()

    def _setup_table(self):
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["原文件名", "新文件名", "状态"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(2, 80)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

    def _setup_layout(self):
        v = QVBoxLayout(self)
        v.addWidget(self.table)

    def update_preview(self, file_list: list, generate_new_name_func):
        self.table.setRowCount(len(file_list))
        seen_names = {}

        for i, filename in enumerate(file_list):
            new_name = generate_new_name_func(filename, i)

            item_old = QTableWidgetItem(filename)
            item_new = QTableWidgetItem(new_name)

            if new_name in seen_names:
                status = "⚠️ 冲突"
                color = QColor("#ffcdd2")
                item_status = QTableWidgetItem(status)
                item_status.setForeground(QColor("#c62828"))
            elif new_name == filename:
                status = "— 无变化"
                color = QColor("#fff9c4")
                item_status = QTableWidgetItem(status)
                item_status.setForeground(QColor("#f57f17"))
            else:
                status = "✓ 就绪"
                color = QColor("#c8e6c9")
                item_status = QTableWidgetItem(status)
                item_status.setForeground(QColor("#2e7d32"))

            seen_names[new_name] = seen_names.get(new_name, 0) + 1

            item_old.setBackground(QColor("#ffffff"))
            item_new.setBackground(color)
            item_status.setBackground(color)
            item_status.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(i, 0, item_old)
            self.table.setItem(i, 1, item_new)
            self.table.setItem(i, 2, item_status)


class ActionButtons(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(12)
        self._init_widgets()

    def _init_widgets(self):
        self.btn_refresh = QPushButton("🔄 刷新列表")
        self.btn_execute = QPushButton("✅ 执行重命名")
        self.btn_execute.setFixedHeight(36)
        self.btn_execute.setObjectName("btn_execute")

        self.btn_undo = QPushButton("↩️ 撤销重命名")
        self.btn_undo.setObjectName("btn_undo")
        self.btn_undo.setEnabled(False)

        self.addWidget(self.btn_refresh)
        self.addStretch()
        self.addWidget(self.btn_undo)
        self.addWidget(self.btn_execute)