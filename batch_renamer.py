import sys
import os
import json
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QGroupBox, QPushButton, QLineEdit, QLabel,
    QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView,
    QSpinBox, QRadioButton, QButtonGroup, QMessageBox, QStatusBar,
    QComboBox, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QIcon


class BatchRenamer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_list = []
        self.rename_history = []
        self.current_folder = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("文件批量重命名工具")
        self.setMinimumSize(960, 700)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(10, 10, 10, 10)

        self.setup_folder_section(main_layout)
        self.setup_mode_section(main_layout)
        self.setup_preview_table(main_layout)
        self.setup_action_buttons(main_layout)
        self.setup_statusbar()
        self.apply_styles()

    def setup_folder_section(self, layout):
        group = QGroupBox("📁 文件夹选择")
        h = QHBoxLayout(group)
        self.folder_path_edit = QLineEdit()
        self.folder_path_edit.setReadOnly(True)
        self.folder_path_edit.setPlaceholderText("请选择文件夹...")
        btn = QPushButton("浏览...")
        btn.setFixedWidth(80)
        btn.clicked.connect(self.select_folder)
        h.addWidget(QLabel("路径:"))
        h.addWidget(self.folder_path_edit)
        h.addWidget(btn)
        layout.addWidget(group)

    def setup_mode_section(self, layout):
        group = QGroupBox("⚙️ 重命名规则")
        grid = QGridLayout(group)
        grid.setSpacing(8)

        self.mode_group = QButtonGroup(self)
        self.radio_prefix_suffix = QRadioButton("添加前缀/后缀")
        self.radio_sequential = QRadioButton("数字序号命名")
        self.radio_replace = QRadioButton("查找替换")
        self.radio_prefix_suffix.setChecked(True)

        self.mode_group.addButton(self.radio_prefix_suffix, 0)
        self.mode_group.addButton(self.radio_sequential, 1)
        self.mode_group.addButton(self.radio_replace, 2)

        grid.addWidget(self.radio_prefix_suffix, 0, 0)
        grid.addWidget(self.radio_sequential, 0, 1)
        grid.addWidget(self.radio_replace, 0, 2)

        # 前缀/后缀
        self.prefix_edit = QLineEdit()
        self.prefix_edit.setPlaceholderText("输入前缀")
        self.suffix_edit = QLineEdit()
        self.suffix_edit.setPlaceholderText("输入后缀（不含扩展名）")
        grid.addWidget(QLabel("前缀:"), 1, 0)
        grid.addWidget(self.prefix_edit, 1, 1, 1, 2)
        grid.addWidget(QLabel("后缀:"), 2, 0)
        grid.addWidget(self.suffix_edit, 2, 1, 1, 2)

        # 数字序号
        grid.addWidget(QLabel("起始序号:"), 3, 0)
        self.start_num_spin = QSpinBox()
        self.start_num_spin.setMinimum(0)
        self.start_num_spin.setMaximum(99999)
        self.start_num_spin.setValue(1)
        grid.addWidget(self.start_num_spin, 3, 1)

        self.digits_spin = QSpinBox()
        self.digits_spin.setMinimum(1)
        self.digits_spin.setMaximum(10)
        self.digits_spin.setValue(3)
        digits_layout = QHBoxLayout()
        digits_layout.addWidget(QLabel("位数:"))
        digits_layout.addWidget(self.digits_spin)
        digits_widget = QWidget()
        digits_widget.setLayout(digits_layout)
        grid.addWidget(digits_widget, 3, 2)

        self.seq_prefix_edit = QLineEdit()
        self.seq_prefix_edit.setPlaceholderText("序号前缀（可选）")
        grid.addWidget(QLabel("序号前缀:"), 4, 0)
        grid.addWidget(self.seq_prefix_edit, 4, 1, 1, 2)

        # 查找替换
        self.find_edit = QLineEdit()
        self.find_edit.setPlaceholderText("查找内容")
        self.replace_edit = QLineEdit()
        self.replace_edit.setPlaceholderText("替换为")
        grid.addWidget(QLabel("查找:"), 5, 0)
        grid.addWidget(self.find_edit, 5, 1, 1, 2)
        grid.addWidget(QLabel("替换:"), 6, 0)
        grid.addWidget(self.replace_edit, 6, 1, 1, 2)

        self.case_sensitive_check = QCheckBox("区分大小写")
        self.case_sensitive_check.setChecked(True)
        grid.addWidget(self.case_sensitive_check, 7, 1)

        # 信号连接 - 实时预览
        self.mode_group.buttonClicked.connect(self.update_preview)
        self.prefix_edit.textChanged.connect(self.update_preview)
        self.suffix_edit.textChanged.connect(self.update_preview)
        self.start_num_spin.valueChanged.connect(self.update_preview)
        self.digits_spin.valueChanged.connect(self.update_preview)
        self.seq_prefix_edit.textChanged.connect(self.update_preview)
        self.find_edit.textChanged.connect(self.update_preview)
        self.replace_edit.textChanged.connect(self.update_preview)
        self.case_sensitive_check.stateChanged.connect(self.update_preview)

        layout.addWidget(group)

    def setup_preview_table(self, layout):
        group = QGroupBox("👁️ 预览（实时）")
        v = QVBoxLayout(group)

        self.table = QTableWidget()
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

        v.addWidget(self.table)
        layout.addWidget(group)

    def setup_action_buttons(self, layout):
        h = QHBoxLayout()
        h.setSpacing(12)

        self.btn_refresh = QPushButton("🔄 刷新列表")
        self.btn_refresh.clicked.connect(self.load_files)

        self.btn_execute = QPushButton("✅ 执行重命名")
        self.btn_execute.setFixedHeight(36)
        self.btn_execute.clicked.connect(self.execute_rename)

        self.btn_undo = QPushButton("↩️ 撤销重命名")
        self.btn_undo.clicked.connect(self.undo_rename)
        self.btn_undo.setEnabled(False)

        h.addWidget(self.btn_refresh)
        h.addStretch()
        h.addWidget(self.btn_undo)
        h.addWidget(self.btn_execute)

        layout.addLayout(h)

    def setup_statusbar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.status_label = QLabel("就绪")
        self.file_count_label = QLabel("文件数: 0")
        self.statusbar.addWidget(self.status_label)
        self.statusbar.addPermanentWidget(self.file_count_label)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 1px solid #ccc;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
            }
            QPushButton {
                padding: 6px 14px;
                border-radius: 4px;
                border: 1px solid #bbb;
                background-color: #fff;
            }
            QPushButton:hover {
                background-color: #e8f0fe;
                border-color: #4285f4;
            }
            QPushButton:pressed {
                background-color: #d2e3fc;
            }
            QPushButton#btn_execute {
                background-color: #1a73e8;
                color: white;
                border: none;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton#btn_execute:hover {
                background-color: #1557b0;
            }
            QPushButton#btn_undo {
                background-color: #f9ab00;
                color: white;
                border: none;
                font-weight: bold;
            }
            QPushButton#btn_undo:hover {
                background-color: #e69500;
            }
            QPushButton#btn_undo:disabled {
                background-color: #ddd;
                color: #999;
            }
            QLineEdit {
                padding: 5px 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border-color: #4285f4;
            }
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                gridline-color: #eee;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QHeaderView::section {
                background-color: #e8eaed;
                padding: 6px;
                border: none;
                border-bottom: 1px solid #ccc;
                font-weight: bold;
            }
            QRadioButton {
                spacing: 6px;
                font-size: 12px;
            }
            QStatusBar {
                background-color: #e8eaed;
            }
        """)
        self.btn_execute.setObjectName("btn_execute")
        self.btn_undo.setObjectName("btn_undo")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            self.current_folder = folder
            self.folder_path_edit.setText(folder)
            self.load_files()

    def load_files(self):
        if not self.current_folder:
            return
        self.file_list = []
        try:
            for entry in sorted(os.listdir(self.current_folder)):
                full_path = os.path.join(self.current_folder, entry)
                if os.path.isfile(full_path):
                    self.file_list.append(entry)
        except PermissionError:
            QMessageBox.warning(self, "权限错误", "无法访问该文件夹")
            return

        self.file_count_label.setText(f"文件数: {len(self.file_list)}")
        self.status_label.setText(f"已加载 {len(self.file_list)} 个文件")
        self.update_preview()

    def generate_new_name(self, original, index):
        name, ext = os.path.splitext(original)
        mode = self.mode_group.checkedId()

        if mode == 0:  # 前缀/后缀
            prefix = self.prefix_edit.text()
            suffix = self.suffix_edit.text()
            return f"{prefix}{name}{suffix}{ext}"

        elif mode == 1:  # 数字序号
            start = self.start_num_spin.value()
            digits = self.digits_spin.value()
            seq_prefix = self.seq_prefix_edit.text()
            num_str = str(start + index).zfill(digits)
            return f"{seq_prefix}{num_str}{ext}"

        elif mode == 2:  # 查找替换
            find_text = self.find_edit.text()
            replace_text = self.replace_edit.text()
            if not find_text:
                return original
            if self.case_sensitive_check.isChecked():
                new_name = name.replace(find_text, replace_text)
            else:
                import re
                new_name = re.sub(re.escape(find_text), replace_text, name, flags=re.IGNORECASE)
            return f"{new_name}{ext}"

        return original

    def update_preview(self):
        self.table.setRowCount(len(self.file_list))
        seen_names = {}

        for i, filename in enumerate(self.file_list):
            new_name = self.generate_new_name(filename, i)

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

    def execute_rename(self):
        if not self.file_list:
            QMessageBox.information(self, "提示", "没有可重命名的文件")
            return

        rename_map = []
        seen_names = set()
        conflicts = 0
        skipped = 0

        for i, filename in enumerate(self.file_list):
            new_name = self.generate_new_name(filename, i)
            if new_name == filename:
                skipped += 1
                continue
            if new_name in seen_names or os.path.exists(os.path.join(self.current_folder, new_name)):
                conflicts += 1
                continue
            seen_names.add(new_name)
            rename_map.append((filename, new_name))

        if not rename_map:
            msg = "没有需要重命名的文件。"
            if conflicts > 0:
                msg += f"\n有 {conflicts} 个文件因名称冲突被跳过。"
            QMessageBox.information(self, "提示", msg)
            return

        confirm_msg = f"即将重命名 {len(rename_map)} 个文件。"
        if conflicts > 0:
            confirm_msg += f"\n（{conflicts} 个冲突文件将被跳过）"
        if skipped > 0:
            confirm_msg += f"\n（{skipped} 个无变化文件将被跳过）"
        confirm_msg += "\n\n确认执行？"

        reply = QMessageBox.question(self, "确认重命名", confirm_msg,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return

        success = 0
        errors = 0
        history_entry = []

        for old_name, new_name in rename_map:
            old_path = os.path.join(self.current_folder, old_name)
            new_path = os.path.join(self.current_folder, new_name)
            try:
                os.rename(old_path, new_path)
                history_entry.append((old_name, new_name))
                success += 1
            except OSError as e:
                errors += 1

        if history_entry:
            self.rename_history.append(history_entry)
            self.btn_undo.setEnabled(True)

        self.status_label.setText(f"完成: {success} 成功, {errors} 失败, {conflicts} 冲突跳过")
        self.load_files()

        if errors == 0:
            QMessageBox.information(self, "完成",
                                    f"成功重命名 {success} 个文件！\n可点击「撤销重命名」恢复。")
        else:
            QMessageBox.warning(self, "部分完成",
                                f"成功: {success}, 失败: {errors}")

    def undo_rename(self):
        if not self.rename_history:
            QMessageBox.information(self, "提示", "没有可撤销的操作")
            return

        last_batch = self.rename_history[-1]
        reply = QMessageBox.question(self, "确认撤销",
                                     f"将撤销上一次重命名操作（{len(last_batch)} 个文件）\n确认？",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return

        success = 0
        errors = 0
        for old_name, new_name in last_batch:
            new_path = os.path.join(self.current_folder, new_name)
            old_path = os.path.join(self.current_folder, old_name)
            try:
                os.rename(new_path, old_path)
                success += 1
            except OSError:
                errors += 1

        self.rename_history.pop()
        if not self.rename_history:
            self.btn_undo.setEnabled(False)

        self.status_label.setText(f"撤销完成: {success} 恢复, {errors} 失败")
        self.load_files()

        if errors == 0:
            QMessageBox.information(self, "撤销完成", f"已恢复 {success} 个文件的原名称")
        else:
            QMessageBox.warning(self, "部分撤销", f"恢复: {success}, 失败: {errors}")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)
    window = BatchRenamer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
