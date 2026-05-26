import os
import json
import shutil
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFileDialog,
    QStatusBar, QLabel
)
from PyQt6.QtCore import QTimer
from ui.widgets import (
    FolderSelector, RenameModePanel, PreviewTable,
    ActionButtons, StyledDialog, OutputLocationSelector
)
from ui.navbar import NavBar
from utils.renamer import Renamer
from utils.history import RenameHistory
from utils.i18n import I18n


class BatchRenamerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_list = []
        self.current_folder = ""
        self.renamer = Renamer()
        self.history = RenameHistory()
        self.init_ui()
        I18n.instance().language_changed.connect(self._retranslate)

    def init_ui(self):
        i18n = I18n.instance()
        self.setWindowTitle(i18n.tr("app_title"))
        self.setMinimumSize(1000, 720)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.navbar = NavBar()
        main_layout.addWidget(self.navbar)

        content_layout = QVBoxLayout()
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(20, 12, 20, 12)
        main_layout.addLayout(content_layout)

        self._setup_widgets(content_layout)
        self._setup_statusbar()
        self._connect_signals()

    def _setup_widgets(self, layout):
        self.folder_selector = FolderSelector()
        self.mode_panel = RenameModePanel()
        self.output_location = OutputLocationSelector()
        self.preview_table = PreviewTable()
        self.action_buttons = ActionButtons()

        layout.addWidget(self.folder_selector)
        layout.addWidget(self.mode_panel)
        layout.addWidget(self.output_location)
        layout.addWidget(self.preview_table)
        layout.addLayout(self.action_buttons)

    def _setup_statusbar(self):
        i18n = I18n.instance()
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.status_label = QLabel(i18n.tr("status_ready_msg"))
        self.file_count_label = QLabel(i18n.tr("file_count_zero"))
        self.statusbar.addWidget(self.status_label)
        self.statusbar.addPermanentWidget(self.file_count_label)

    def _connect_signals(self):
        self.folder_selector.browse_btn.clicked.connect(self.select_folder)
        self.action_buttons.btn_refresh.clicked.connect(self.load_files)
        self.action_buttons.btn_execute.clicked.connect(self.execute_rename)
        self.action_buttons.btn_undo.clicked.connect(self.undo_rename)

        self.preview_table.selection_changed.connect(self._on_selection_changed)

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
        self.mode_panel.direct_name_edit.textChanged.connect(self._update_renamer_settings)
        self.mode_panel.direct_name_edit.textChanged.connect(self.update_preview)

        self.navbar.action_new.connect(self._new_task)
        self.navbar.action_save_config.connect(self._save_config)
        self.navbar.action_export_list.connect(self._export_list)
        self.navbar.action_show_guide.connect(self._show_guide)
        self.navbar.action_show_faq.connect(self._show_faq)

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(50, self._animate_entrance)

    def _animate_entrance(self):
        from utils.animations import fade_in
        fade_in(self.centralWidget(), duration=400)

    def _on_selection_changed(self, checked_count: int):
        i18n = I18n.instance()
        self.mode_panel.set_direct_input_available(checked_count == 1)
        self.file_count_label.setText(
            i18n.tr("file_count", total=len(self.file_list), selected=checked_count)
        )
        self.update_preview()

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
        self.renamer.direct_name = self.mode_panel.direct_name_edit.text()

    def select_folder(self):
        i18n = I18n.instance()
        folder = QFileDialog.getExistingDirectory(self, i18n.tr("folder_select"))
        if folder:
            self.current_folder = folder
            self.folder_selector.set_folder_path(folder)
            self.load_files()

    def load_files(self):
        if not self.current_folder:
            return
        i18n = I18n.instance()
        self.file_list = []
        try:
            for entry in sorted(os.listdir(self.current_folder)):
                full_path = os.path.join(self.current_folder, entry)
                if os.path.isfile(full_path):
                    self.file_list.append(entry)
        except PermissionError:
            StyledDialog.show_warning(self, i18n.tr("permission_error"), i18n.tr("permission_error_msg"))
            return

        self.file_count_label.setText(
            i18n.tr("file_count", total=len(self.file_list), selected=len(self.file_list))
        )
        self.status_label.setText(i18n.tr("loaded_files", count=len(self.file_list)))
        self.mode_panel.set_direct_input_available(len(self.file_list) == 1)
        self.update_preview()

    def update_preview(self):
        self._update_renamer_settings()
        checked_indices = set(self.preview_table.get_checked_indices())
        if not self.file_list:
            checked_indices = set()
        elif self.preview_table.table.rowCount() != len(self.file_list):
            checked_indices = set(range(len(self.file_list)))
        self.preview_table.update_preview(self.file_list, self.renamer.generate_new_name, checked_indices)

    def execute_rename(self):
        i18n = I18n.instance()
        checked_indices = self.preview_table.get_checked_indices()
        if not checked_indices:
            StyledDialog.show_info(self, i18n.tr("tip"), i18n.tr("no_selected_files"))
            return

        self._update_renamer_settings()

        use_custom_output = not self.output_location.is_original_dir()
        custom_output_path = self.output_location.get_custom_path() if use_custom_output else ""

        if use_custom_output and not custom_output_path:
            StyledDialog.show_warning(self, i18n.tr("tip"), i18n.tr("output_custom_placeholder"))
            return

        rename_map = []
        seen_names = set()
        conflicts = 0
        skipped = 0

        seq_index = 0
        for i in checked_indices:
            filename = self.file_list[i]
            new_name = self.renamer.generate_new_name(filename, seq_index)
            seq_index += 1
            if new_name == filename and not use_custom_output:
                skipped += 1
                continue
            target_folder = custom_output_path if use_custom_output else self.current_folder
            if new_name in seen_names or os.path.exists(os.path.join(target_folder, new_name)):
                conflicts += 1
                continue
            seen_names.add(new_name)
            rename_map.append((filename, new_name))

        if not rename_map:
            msg = i18n.tr("no_rename_needed")
            if conflicts > 0:
                msg += "\n" + i18n.tr("conflict_skip", count=conflicts)
            StyledDialog.show_info(self, i18n.tr("tip"), msg)
            return

        confirm_msg = i18n.tr("confirm_rename", count=len(rename_map))
        if conflicts > 0:
            confirm_msg += "\n" + i18n.tr("conflict_note", count=conflicts)
        if skipped > 0:
            confirm_msg += "\n" + i18n.tr("no_change_note", count=skipped)
        confirm_msg += "\n\n" + i18n.tr("confirm_execute")

        if not StyledDialog.ask(self, i18n.tr("confirm_rename_title"), confirm_msg):
            return

        if use_custom_output:
            os.makedirs(custom_output_path, exist_ok=True)
            success = 0
            errors = 0
            for old_name, new_name in rename_map:
                try:
                    src = os.path.join(self.current_folder, old_name)
                    dst = os.path.join(custom_output_path, new_name)
                    shutil.copy2(src, dst)
                    success += 1
                except Exception:
                    errors += 1
        else:
            success, errors = self.history.execute_batch(self.current_folder, rename_map)
            if rename_map:
                self.history.add_batch(rename_map)
                self.action_buttons.btn_undo.setEnabled(True)

        self.status_label.setText(
            i18n.tr("status_done", success=success, errors=errors, conflicts=conflicts)
        )
        self.load_files()

        if errors == 0:
            StyledDialog.show_success(self, i18n.tr("done"),
                                      i18n.tr("done_msg", count=success))
        else:
            StyledDialog.show_warning(self, i18n.tr("partial_done"),
                                      i18n.tr("success_count", success=success, errors=errors))

    def undo_rename(self):
        i18n = I18n.instance()
        if not self.history.has_history():
            StyledDialog.show_info(self, i18n.tr("tip"), i18n.tr("no_undo_history"))
            return

        last_batch = self.history.get_last_batch()
        if not StyledDialog.ask(self, i18n.tr("confirm_undo_title"),
                                i18n.tr("confirm_undo", count=len(last_batch))):
            return

        success, errors = self.history.undo_batch(self.current_folder, last_batch)
        self.history.undo_last()

        if not self.history.has_history():
            self.action_buttons.btn_undo.setEnabled(False)

        self.status_label.setText(i18n.tr("undo_status", success=success, errors=errors))
        self.load_files()

        if errors == 0:
            StyledDialog.show_success(self, i18n.tr("undo_done"),
                                      i18n.tr("undo_done_msg", count=success))
        else:
            StyledDialog.show_warning(self, i18n.tr("undo_partial"),
                                      i18n.tr("success_count", success=success, errors=errors))

    def _new_task(self):
        new_window = BatchRenamerWindow()
        new_window.show()
        self._child_windows = getattr(self, '_child_windows', [])
        self._child_windows.append(new_window)

    def _save_config(self):
        i18n = I18n.instance()
        config = {
            "mode": self.mode_panel.mode_group.checkedId(),
            "prefix": self.mode_panel.prefix_edit.text(),
            "suffix": self.mode_panel.suffix_edit.text(),
            "start_num": self.mode_panel.start_num_spin.value(),
            "digits": self.mode_panel.digits_spin.value(),
            "seq_prefix": self.mode_panel.seq_prefix_edit.text(),
            "find_text": self.mode_panel.find_edit.text(),
            "replace_text": self.mode_panel.replace_edit.text(),
            "case_sensitive": self.mode_panel.case_sensitive_check.isChecked(),
            "direct_name": self.mode_panel.direct_name_edit.text(),
        }
        path, _ = QFileDialog.getSaveFileName(
            self, i18n.tr("task_save_config"), "rename_config.json",
            "JSON (*.json)"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            StyledDialog.show_success(self, i18n.tr("config_saved"),
                                      i18n.tr("config_saved_msg", path=path))

    def _export_list(self):
        i18n = I18n.instance()
        if not self.file_list:
            StyledDialog.show_info(self, i18n.tr("tip"), i18n.tr("export_no_data"))
            return

        self._update_renamer_settings()
        checked_indices = self.preview_table.get_checked_indices()
        if not checked_indices:
            checked_indices = list(range(len(self.file_list)))

        lines = []
        seq_index = 0
        for i in checked_indices:
            filename = self.file_list[i]
            new_name = self.renamer.generate_new_name(filename, seq_index)
            seq_index += 1
            lines.append(f"{filename}\t{new_name}")

        path, _ = QFileDialog.getSaveFileName(
            self, i18n.tr("task_export_list"), "rename_list.txt",
            "Text (*.txt);;CSV (*.csv)"
        )
        if path:
            sep = "," if path.endswith(".csv") else "\t"
            header = f"{i18n.tr('col_original')}{sep}{i18n.tr('col_new')}\n"
            with open(path, "w", encoding="utf-8") as f:
                f.write(header)
                for i in checked_indices:
                    filename = self.file_list[i]
                    new_name = self.renamer.generate_new_name(filename, i)
                    f.write(f"{filename}{sep}{new_name}\n")
            StyledDialog.show_success(self, i18n.tr("export_done"),
                                      i18n.tr("export_done_msg", path=path))

    def _show_guide(self):
        i18n = I18n.instance()
        StyledDialog.show_info(self, i18n.tr("guide_title"), i18n.tr("guide_content"))

    def _show_faq(self):
        i18n = I18n.instance()
        StyledDialog.show_info(self, i18n.tr("faq_title"), i18n.tr("faq_content"))

    def _retranslate(self):
        i18n = I18n.instance()
        self.setWindowTitle(i18n.tr("app_title"))
        self.status_label.setText(i18n.tr("status_ready_msg"))
        self.file_count_label.setText(i18n.tr("file_count_zero"))
