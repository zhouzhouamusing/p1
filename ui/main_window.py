import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFileDialog,
    QMessageBox, QStatusBar, QLabel
)
from ui.widgets import FolderSelector, RenameModePanel, PreviewTable, ActionButtons
from utils.renamer import Renamer
from utils.history import RenameHistory


class BatchRenamerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_list = []
        self.current_folder = ""
        self.renamer = Renamer()
        self.history = RenameHistory()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("文件批量重命名工具")
        self.setMinimumSize(960, 700)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(10, 10, 10, 10)

        self._setup_widgets(main_layout)
        self._setup_statusbar()
        self._connect_signals()
        self.apply_styles()

    def _setup_widgets(self, layout):
        self.folder_selector = FolderSelector()
        self.mode_panel = RenameModePanel()
        self.preview_table = PreviewTable()
        self.action_buttons = ActionButtons()

        layout.addWidget(self.folder_selector)
        layout.addWidget(self.mode_panel)
        layout.addWidget(self.preview_table)
        layout.addLayout(self.action_buttons)

    def _setup_statusbar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.status_label = QLabel("就绪")
        self.file_count_label = QLabel("文件数: 0")
        self.statusbar.addWidget(self.status_label)
        self.statusbar.addPermanentWidget(self.file_count_label)

    def _connect_signals(self):
        self.folder_selector.browse_btn.clicked.connect(self.select_folder)
        self.action_buttons.btn_refresh.clicked.connect(self.load_files)
        self.action_buttons.btn_execute.clicked.connect(self.execute_rename)
        self.action_buttons.btn_undo.clicked.connect(self.undo_rename)

        self.mode_panel.mode_group.buttonClicked.connect(self._update_renamer_settings)
        self.mode_panel.mode_group.buttonClicked.connect(self.update_preview)

        self.mode_panel.prefix_edit.textChanged.connect(self._update_renamer_settings)
        self.mode_panel.prefix_edit.textChanged.connect(self.update_preview)
        self.mode_panel.suffix_edit.textChanged.connect(self._update_renamer_settings)
        self.mode_panel.suffix_edit.textChanged.connect(self.update_preview)
        self.mode_panel.start_num_spin.valueChanged.connect(self._update_renamer_settings)
        self.mode_panel.start_num_spin.valueChanged.connect(self.update_preview)
        self.mode_panel.digits_spin.valueChanged.connect(self._update_renamer_settings)
        self.mode_panel.digits_spin.valueChanged.connect(self.update_preview)
        self.mode_panel.seq_prefix_edit.textChanged.connect(self._update_renamer_settings)
        self.mode_panel.seq_prefix_edit.textChanged.connect(self.update_preview)
        self.mode_panel.find_edit.textChanged.connect(self._update_renamer_settings)
        self.mode_panel.find_edit.textChanged.connect(self.update_preview)
        self.mode_panel.replace_edit.textChanged.connect(self._update_renamer_settings)
        self.mode_panel.replace_edit.textChanged.connect(self.update_preview)
        self.mode_panel.case_sensitive_check.stateChanged.connect(self._update_renamer_settings)
        self.mode_panel.case_sensitive_check.stateChanged.connect(self.update_preview)

    def _update_renamer_settings(self):
        self.renamer.mode = self.mode_panel.mode_group.checkedId()
        self.renamer.prefix = self.mode_panel.prefix_edit.text()
        self.renamer.suffix = self.mode_panel.suffix_edit.text()
        self.renamer.start_num = self.mode_panel.start_num_spin.value()
        self.renamer.digits = self.mode_panel.digits_spin.value()
        self.renamer.seq_prefix = self.mode_panel.seq_prefix_edit.text()
        self.renamer.find_text = self.mode_panel.find_edit.text()
        self.renamer.replace_text = self.mode_panel.replace_edit.text()
        self.renamer.case_sensitive = self.mode_panel.case_sensitive_check.isChecked()

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

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            self.current_folder = folder
            self.folder_selector.set_folder_path(folder)
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

    def update_preview(self):
        self._update_renamer_settings()
        self.preview_table.update_preview(self.file_list, self.renamer.generate_new_name)

    def execute_rename(self):
        if not self.file_list:
            QMessageBox.information(self, "提示", "没有可重命名的文件")
            return

        self._update_renamer_settings()
        rename_map = []
        seen_names = set()
        conflicts = 0
        skipped = 0

        for i, filename in enumerate(self.file_list):
            new_name = self.renamer.generate_new_name(filename, i)
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

        success, errors = self.history.execute_batch(self.current_folder, rename_map)

        if rename_map:
            self.history.add_batch(rename_map)
            self.action_buttons.btn_undo.setEnabled(True)

        self.status_label.setText(f"完成: {success} 成功, {errors} 失败, {conflicts} 冲突跳过")
        self.load_files()

        if errors == 0:
            QMessageBox.information(self, "完成",
                                    f"成功重命名 {success} 个文件！\n可点击「撤销重命名」恢复。")
        else:
            QMessageBox.warning(self, "部分完成",
                                f"成功: {success}, 失败: {errors}")

    def undo_rename(self):
        if not self.history.has_history():
            QMessageBox.information(self, "提示", "没有可撤销的操作")
            return

        last_batch = self.history.get_last_batch()
        reply = QMessageBox.question(self, "确认撤销",
                                     f"将撤销上一次重命名操作（{len(last_batch)} 个文件）\n确认？",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return

        success, errors = self.history.undo_batch(self.current_folder, last_batch)
        self.history.undo_last()

        if not self.history.has_history():
            self.action_buttons.btn_undo.setEnabled(False)

        self.status_label.setText(f"撤销完成: {success} 恢复, {errors} 失败")
        self.load_files()

        if errors == 0:
            QMessageBox.information(self, "撤销完成", f"已恢复 {success} 个文件的原名称")
        else:
            QMessageBox.warning(self, "部分撤销", f"恢复: {success}, 失败: {errors}")