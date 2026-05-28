import os
import json
import shutil
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFileDialog,
    QStatusBar, QLabel, QScrollArea
)
from PyQt6.QtCore import QTimer, Qt
from ui.widgets import (
    FolderSelector, RenameModePanel, PreviewTable,
    ActionButtons, StyledDialog, OutputLocationSelector,
    PreviewDialog
)
from ui.navbar import NavBar
from utils.renamer import Renamer
from utils.history import RenameHistory
from utils.i18n import I18n


class BatchRenamerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_list = []
        self.file_rel_paths = []
        self.current_folder = ""
        self.renamer = Renamer()
        self.history = RenameHistory()
        self.init_ui()
        I18n.instance().language_changed.connect(self._retranslate)

    def init_ui(self):
        i18n = I18n.instance()
        self.setWindowTitle(i18n.tr("app_title"))
        self.setMinimumSize(1060, 760)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.navbar = NavBar()
        main_layout.addWidget(self.navbar)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        scroll_content = QWidget()
        content_layout = QVBoxLayout(scroll_content)
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(20, 12, 20, 12)

        self._setup_widgets(content_layout)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

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
        self.undo_count_label = QLabel("")
        self.statusbar.addWidget(self.status_label)
        self.statusbar.addPermanentWidget(self.undo_count_label)
        self.statusbar.addPermanentWidget(self.file_count_label)

    def _connect_signals(self):
        self.folder_selector.browse_btn.clicked.connect(self.select_folder)
        self.folder_selector.include_subfolders_changed.connect(self._on_subfolders_changed)
        self.action_buttons.btn_refresh.clicked.connect(self.load_files)
        self.action_buttons.btn_execute.clicked.connect(self.execute_rename)
        self.action_buttons.btn_undo.clicked.connect(self.undo_rename)
        self.action_buttons.btn_undo_all.clicked.connect(self.undo_all)
        self.action_buttons.btn_preview_detail.clicked.connect(self._show_preview_dialog)

        self.preview_table.selection_changed.connect(self._on_selection_changed)

        self.mode_panel.mode_group.buttonClicked.connect(self._update_renamer_settings)
        self.mode_panel.mode_group.buttonClicked.connect(self.update_preview)

        # Mode 0: Prefix/Suffix
        self.mode_panel.prefix_edit.textChanged.connect(self._update_and_preview)
        self.mode_panel.suffix_edit.textChanged.connect(self._update_and_preview)

        # Mode 1: Sequential
        self.mode_panel.start_num_spin.valueChanged.connect(self._update_and_preview)
        self.mode_panel.digits_spin.valueChanged.connect(self._update_and_preview)
        self.mode_panel.seq_prefix_edit.textChanged.connect(self._update_and_preview)

        # Mode 2: Find & Replace
        self.mode_panel.find_edit.textChanged.connect(self._update_and_preview)
        self.mode_panel.replace_edit.textChanged.connect(self._update_and_preview)
        self.mode_panel.case_sensitive_check.stateChanged.connect(self._update_and_preview)

        # Mode 3: Direct Input
        self.mode_panel.direct_name_edit.textChanged.connect(self._update_and_preview)

        # Mode 4: Regex
        self.mode_panel.regex_pattern_edit.textChanged.connect(self._update_and_preview)
        self.mode_panel.regex_replace_edit.textChanged.connect(self._update_and_preview)

        # Mode 5: Datetime
        self.mode_panel.datetime_format_edit.textChanged.connect(self._update_and_preview)
        self.mode_panel.datetime_source_combo.currentIndexChanged.connect(self._update_and_preview)

        # Mode 6: Attributes
        self.mode_panel.attr_template_edit.textChanged.connect(self._update_and_preview)

        # Mode 7: Enhanced Sequence
        self.mode_panel.seq_enh_prefix_edit.textChanged.connect(self._update_and_preview)
        self.mode_panel.seq_enh_suffix_edit.textChanged.connect(self._update_and_preview)
        self.mode_panel.seq_enh_start_spin.valueChanged.connect(self._update_and_preview)
        self.mode_panel.seq_enh_step_spin.valueChanged.connect(self._update_and_preview)
        self.mode_panel.seq_enh_digits_spin.valueChanged.connect(self._update_and_preview)
        self.mode_panel.seq_enh_format_combo.currentIndexChanged.connect(self._update_and_preview)

        self.navbar.action_new.connect(self._new_task)
        self.navbar.action_save_config.connect(self._save_config)
        self.navbar.action_export_list.connect(self._export_list)
        self.navbar.action_show_guide.connect(self._show_guide)
        self.navbar.action_show_faq.connect(self._show_faq)

    def _update_and_preview(self):
        self._update_renamer_settings()
        self.update_preview()
        self._check_warnings()

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(50, self._animate_entrance)

    def _animate_entrance(self):
        from utils.animations import fade_in
        fade_in(self.centralWidget(), duration=400)

    def _check_warnings(self):
        i18n = I18n.instance()
        warnings = self.renamer.get_warnings()
        if not warnings:
            return
        has_time = any("time_fallback" in w for w in warnings)
        has_size = any("size_fallback" in w for w in warnings)
        msg = ""
        if has_time:
            msg += i18n.tr("datetime_fallback_warn")
        if has_size:
            if msg:
                msg += "\n"
            msg += i18n.tr("attr_fallback_warn")
        if msg:
            self.status_label.setText(msg)
        self.renamer.clear_warnings()

    def _on_subfolders_changed(self, include: bool):
        self.preview_table.set_show_folder_column(include)
        if self.current_folder:
            self.load_files()

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
        # Regex
        self.renamer.regex_pattern = self.mode_panel.regex_pattern_edit.text()
        self.renamer.regex_replace = self.mode_panel.regex_replace_edit.text()
        # Datetime
        self.renamer.datetime_format = self.mode_panel.datetime_format_edit.text()
        self.renamer.datetime_source = self.mode_panel.datetime_source_combo.currentData()
        # Attributes
        self.renamer.attr_template = self.mode_panel.attr_template_edit.text()
        # Enhanced Sequence
        self.renamer.seq_enh_prefix = self.mode_panel.seq_enh_prefix_edit.text()
        self.renamer.seq_enh_suffix = self.mode_panel.seq_enh_suffix_edit.text()
        self.renamer.seq_enh_start = self.mode_panel.seq_enh_start_spin.value()
        self.renamer.seq_enh_step = self.mode_panel.seq_enh_step_spin.value()
        self.renamer.seq_enh_digits = self.mode_panel.seq_enh_digits_spin.value()
        self.renamer.seq_enh_format = self.mode_panel.seq_enh_format_combo.currentData()
        # Folder path for datetime/attributes
        self.renamer.set_folder_path(self.current_folder)

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
        self.file_rel_paths = []
        include_sub = self.folder_selector.is_include_subfolders()

        try:
            if include_sub:
                for root, dirs, files in os.walk(self.current_folder):
                    rel_dir = os.path.relpath(root, self.current_folder)
                    if rel_dir == ".":
                        rel_dir = ""
                    for f in sorted(files):
                        self.file_list.append(f)
                        self.file_rel_paths.append(rel_dir)
            else:
                for entry in sorted(os.listdir(self.current_folder)):
                    full_path = os.path.join(self.current_folder, entry)
                    if os.path.isfile(full_path):
                        self.file_list.append(entry)
                        self.file_rel_paths.append("")
        except PermissionError:
            StyledDialog.show_warning(self, i18n.tr("permission_error"), i18n.tr("permission_error_msg"))
            return

        self.file_count_label.setText(
            i18n.tr("file_count", total=len(self.file_list), selected=len(self.file_list))
        )
        if include_sub:
            self.status_label.setText(i18n.tr("loaded_files_with_sub", count=len(self.file_list)))
        else:
            self.status_label.setText(i18n.tr("loaded_files", count=len(self.file_list)))
        self.mode_panel.set_direct_input_available(len(self.file_list) == 1)
        self.renamer.set_folder_path(self.current_folder)
        self.update_preview()

    def update_preview(self):
        self._update_renamer_settings()
        self.renamer.clear_warnings()
        checked_indices = set(self.preview_table.get_checked_indices())
        if not self.file_list:
            checked_indices = set()
        elif self.preview_table.table.rowCount() != len(self.file_list):
            checked_indices = set(range(len(self.file_list)))

        def generate_with_folder(filename, index):
            row_idx = None
            count = 0
            for i in range(len(self.file_list)):
                if i in checked_indices:
                    if count == index:
                        row_idx = i
                        break
                    count += 1
            if row_idx is not None and self.file_rel_paths[row_idx]:
                folder = os.path.join(self.current_folder, self.file_rel_paths[row_idx])
                self.renamer.set_folder_path(folder)
            else:
                self.renamer.set_folder_path(self.current_folder)
            return self.renamer.generate_new_name(filename, index)

        self.preview_table.update_preview(
            self.file_list, generate_with_folder, checked_indices,
            rel_paths=self.file_rel_paths
        )

    def _show_preview_dialog(self):
        i18n = I18n.instance()
        checked_indices = self.preview_table.get_checked_indices()
        if not checked_indices:
            StyledDialog.show_info(self, i18n.tr("tip"), i18n.tr("no_selected_files"))
            return

        self._update_renamer_settings()
        rename_map = []
        seq_index = 0
        for i in checked_indices:
            filename = self.file_list[i]
            if self.file_rel_paths[i]:
                folder = os.path.join(self.current_folder, self.file_rel_paths[i])
                self.renamer.set_folder_path(folder)
            else:
                self.renamer.set_folder_path(self.current_folder)
            new_name = self.renamer.generate_new_name(filename, seq_index)
            seq_index += 1
            if new_name != filename:
                display_old = filename
                display_new = new_name
                if self.file_rel_paths[i]:
                    display_old = os.path.join(self.file_rel_paths[i], filename)
                    display_new = os.path.join(self.file_rel_paths[i], new_name)
                rename_map.append((display_old, display_new))

        if not rename_map:
            StyledDialog.show_info(self, i18n.tr("tip"), i18n.tr("no_rename_needed"))
            return

        dlg = PreviewDialog(self, rename_map)
        dlg.exec()

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
        folder_map = []
        seen_names = set()
        conflicts = 0
        skipped = 0

        seq_index = 0
        for i in checked_indices:
            filename = self.file_list[i]
            rel_path = self.file_rel_paths[i] if self.file_rel_paths else ""
            file_folder = os.path.join(self.current_folder, rel_path) if rel_path else self.current_folder
            self.renamer.set_folder_path(file_folder)
            new_name = self.renamer.generate_new_name(filename, seq_index)
            seq_index += 1
            if new_name == filename and not use_custom_output:
                skipped += 1
                continue
            target_folder = custom_output_path if use_custom_output else file_folder
            full_key = os.path.join(rel_path, new_name) if rel_path else new_name
            if full_key in seen_names or os.path.exists(os.path.join(target_folder, new_name)):
                conflicts += 1
                continue
            seen_names.add(full_key)
            rename_map.append((filename, new_name))
            folder_map.append(file_folder)

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
            for idx, (old_name, new_name) in enumerate(rename_map):
                try:
                    src = os.path.join(folder_map[idx], old_name)
                    dst = os.path.join(custom_output_path, new_name)
                    shutil.copy2(src, dst)
                    success += 1
                except Exception:
                    errors += 1
        else:
            success = 0
            errors = 0
            executed_batch = []
            for idx, (old_name, new_name) in enumerate(rename_map):
                file_folder = folder_map[idx]
                old_path = os.path.join(file_folder, old_name)
                new_path = os.path.join(file_folder, new_name)
                try:
                    os.rename(old_path, new_path)
                    success += 1
                    executed_batch.append((old_name, new_name, file_folder))
                except OSError:
                    errors += 1

            if executed_batch:
                self.history.history.append(executed_batch)
                self._update_undo_buttons()

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
        self._update_undo_buttons()

        self.status_label.setText(i18n.tr("undo_status", success=success, errors=errors))
        self.load_files()

        if errors == 0:
            StyledDialog.show_success(self, i18n.tr("undo_done"),
                                      i18n.tr("undo_done_msg", count=success))
        else:
            StyledDialog.show_warning(self, i18n.tr("undo_partial"),
                                      i18n.tr("success_count", success=success, errors=errors))

    def undo_all(self):
        i18n = I18n.instance()
        if not self.history.has_history():
            StyledDialog.show_info(self, i18n.tr("tip"), i18n.tr("no_undo_history"))
            return

        count = self.history.history_count()
        if not StyledDialog.ask(self, i18n.tr("confirm_undo_all_title"),
                                i18n.tr("confirm_undo_all", count=count)):
            return

        success, errors = self.history.undo_all(self.current_folder)
        self._update_undo_buttons()

        self.status_label.setText(i18n.tr("undo_status", success=success, errors=errors))
        self.load_files()

        if errors == 0:
            StyledDialog.show_success(self, i18n.tr("undo_done"), i18n.tr("undo_all_done"))
        else:
            StyledDialog.show_warning(self, i18n.tr("undo_partial"),
                                      i18n.tr("success_count", success=success, errors=errors))

    def _update_undo_buttons(self):
        i18n = I18n.instance()
        has = self.history.has_history()
        self.action_buttons.btn_undo.setEnabled(has)
        self.action_buttons.btn_undo_all.setEnabled(has)
        if has:
            self.undo_count_label.setText(
                i18n.tr("undo_history_count", count=self.history.history_count())
            )
        else:
            self.undo_count_label.setText("")

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
            "regex_pattern": self.mode_panel.regex_pattern_edit.text(),
            "regex_replace": self.mode_panel.regex_replace_edit.text(),
            "datetime_format": self.mode_panel.datetime_format_edit.text(),
            "datetime_source": self.mode_panel.datetime_source_combo.currentData(),
            "attr_template": self.mode_panel.attr_template_edit.text(),
            "seq_enh_prefix": self.mode_panel.seq_enh_prefix_edit.text(),
            "seq_enh_suffix": self.mode_panel.seq_enh_suffix_edit.text(),
            "seq_enh_start": self.mode_panel.seq_enh_start_spin.value(),
            "seq_enh_step": self.mode_panel.seq_enh_step_spin.value(),
            "seq_enh_digits": self.mode_panel.seq_enh_digits_spin.value(),
            "seq_enh_format": self.mode_panel.seq_enh_format_combo.currentData(),
            "include_subfolders": self.folder_selector.is_include_subfolders(),
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
            rel_path = self.file_rel_paths[i] if self.file_rel_paths else ""
            if rel_path:
                folder = os.path.join(self.current_folder, rel_path)
                self.renamer.set_folder_path(folder)
            else:
                self.renamer.set_folder_path(self.current_folder)
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
                seq_index = 0
                for i in checked_indices:
                    filename = self.file_list[i]
                    rel_path = self.file_rel_paths[i] if self.file_rel_paths else ""
                    if rel_path:
                        folder = os.path.join(self.current_folder, rel_path)
                        self.renamer.set_folder_path(folder)
                    else:
                        self.renamer.set_folder_path(self.current_folder)
                    new_name = self.renamer.generate_new_name(filename, seq_index)
                    seq_index += 1
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
        self._update_undo_buttons()
