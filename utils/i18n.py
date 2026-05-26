from PyQt6.QtCore import QObject, pyqtSignal


_ZH_CN = {
    "app_title": "文件批量重命名工具",
    "login_title": "登录 - 文件批量重命名工具",
    "login_subtitle": "请登录以继续使用",
    "username": "用户名",
    "password": "密码",
    "username_placeholder": "请输入用户名",
    "password_placeholder": "请输入密码",
    "remember_password": "记住密码",
    "forgot_password": "忘记密码?",
    "login": "登  录",
    "no_account": "没有账号？",
    "register": "注册",
    "err_empty_username": "请输入用户名",
    "err_empty_password": "请输入密码",
    "err_auth_failed": "用户名或密码错误",

    "nav_task": "任务",
    "nav_skin": "皮肤",
    "nav_language": "语言",
    "nav_help": "帮助",

    "task_new": "新建",
    "task_save_config": "保存当前配置",
    "task_export_list": "导出列表",

    "skin_light": "浅色主题",
    "skin_dark": "深色主题",
    "skin_system": "系统默认",
    "skin_eye_care": "护眼模式",

    "lang_zh_cn": "简体中文",
    "lang_zh_tw": "繁體中文",
    "lang_en": "English",

    "help_guide": "操作指南",
    "help_faq": "常见问题",

    "folder_select": "文件夹选择",
    "path_label": "路径:",
    "browse": "浏览...",
    "folder_placeholder": "请选择文件夹...",

    "rename_rules": "重命名规则",
    "mode_prefix_suffix": "添加前缀/后缀",
    "mode_sequential": "数字序号命名",
    "mode_replace": "查找替换",
    "mode_direct_input": "直接输入文件名",
    "prefix": "前缀:",
    "suffix": "后缀:",
    "prefix_placeholder": "输入前缀",
    "suffix_placeholder": "输入后缀（不含扩展名）",
    "start_num": "起始序号:",
    "digits": "位数:",
    "seq_prefix": "序号前缀:",
    "seq_prefix_placeholder": "序号前缀（可选）",
    "find": "查找:",
    "replace": "替换:",
    "find_placeholder": "查找内容",
    "replace_placeholder": "替换为",
    "case_sensitive": "区分大小写",
    "new_filename": "新文件名:",
    "direct_name_placeholder": "输入新文件名（不含扩展名）",

    "output_location": "输出位置",
    "output_original_dir": "原目录",
    "output_custom_dir": "自定义文件夹",
    "output_custom_placeholder": "选择输出文件夹...",

    "preview": "预览",
    "select_all": "全选",
    "deselect_all": "取消全选",
    "col_select": "选择",
    "col_original": "原文件名",
    "col_new": "新文件名",
    "col_status": "状态",
    "status_ready": "就绪",
    "status_conflict": "冲突",
    "status_no_change": "无变化",
    "status_skip": "跳过",

    "btn_refresh": "刷新列表",
    "btn_undo": "撤销重命名",
    "btn_execute": "执行重命名",

    "status_ready_msg": "就绪",
    "file_count": "文件数: {total} (已选: {selected})",
    "file_count_zero": "文件数: 0",
    "loaded_files": "已加载 {count} 个文件",

    "tip": "提示",
    "confirm": "确认",
    "cancel": "取消",
    "ok": "确定",
    "no_selected_files": "没有选中需要重命名的文件",
    "no_rename_needed": "没有需要重命名的文件。",
    "conflict_skip": "有 {count} 个文件因名称冲突被跳过。",
    "confirm_rename": "即将重命名 {count} 个文件。",
    "conflict_note": "（{count} 个冲突文件将被跳过）",
    "no_change_note": "（{count} 个无变化文件将被跳过）",
    "confirm_execute": "确认执行？",
    "confirm_rename_title": "确认重命名",
    "done": "完成",
    "done_msg": "成功重命名 {count} 个文件！\n可点击「撤销重命名」恢复。",
    "partial_done": "部分完成",
    "success_count": "成功: {success}, 失败: {errors}",
    "status_done": "完成: {success} 成功, {errors} 失败, {conflicts} 冲突跳过",

    "no_undo_history": "没有可撤销的操作",
    "confirm_undo": "将撤销上一次重命名操作（{count} 个文件）\n确认？",
    "confirm_undo_title": "确认撤销",
    "undo_done": "撤销完成",
    "undo_done_msg": "已恢复 {count} 个文件的原名称",
    "undo_partial": "部分撤销",
    "undo_status": "撤销完成: {success} 恢复, {errors} 失败",

    "permission_error": "权限错误",
    "permission_error_msg": "无法访问该文件夹",

    "new_task_done": "已重置工作区",
    "config_saved": "配置已保存",
    "config_saved_msg": "配置已保存到：\n{path}",
    "export_done": "导出完成",
    "export_done_msg": "对照表已导出到：\n{path}",
    "export_no_data": "没有可导出的数据，请先选择文件夹并设置重命名规则",

    "guide_title": "操作指南",
    "guide_content": (
        "1. 点击「浏览」选择包含目标文件的文件夹\n"
        "2. 选择重命名模式并配置参数\n"
        "3. 在预览表中查看效果，勾选需要重命名的文件\n"
        "4. 选择输出位置（原目录或自定义文件夹）\n"
        "5. 点击「执行重命名」完成操作\n"
        "6. 如需恢复，点击「撤销重命名」"
    ),
    "faq_title": "常见问题",
    "faq_content": (
        "Q: 重命名后可以撤销吗？\n"
        "A: 可以，点击「撤销重命名」即可恢复上一次操作。\n\n"
        "Q: 出现文件名冲突怎么办？\n"
        "A: 冲突文件会自动标记为红色并跳过，不会覆盖已有文件。\n\n"
        "Q: 如何批量添加序号？\n"
        "A: 选择「数字序号命名」模式，设置起始序号和位数即可。\n\n"
        "Q: 支持哪些文件类型？\n"
        "A: 支持所有文件类型，工具只修改文件名不修改文件内容。"
    ),
}

_ZH_TW = {
    "app_title": "檔案批次重新命名工具",
    "login_title": "登入 - 檔案批次重新命名工具",
    "login_subtitle": "請登入以繼續使用",
    "username": "使用者名稱",
    "password": "密碼",
    "username_placeholder": "請輸入使用者名稱",
    "password_placeholder": "請輸入密碼",
    "remember_password": "記住密碼",
    "forgot_password": "忘記密碼?",
    "login": "登  入",
    "no_account": "沒有帳號？",
    "register": "註冊",
    "err_empty_username": "請輸入使用者名稱",
    "err_empty_password": "請輸入密碼",
    "err_auth_failed": "使用者名稱或密碼錯誤",

    "nav_task": "任務",
    "nav_skin": "皮膚",
    "nav_language": "語言",
    "nav_help": "說明",

    "task_new": "新建",
    "task_save_config": "儲存目前配置",
    "task_export_list": "匯出列表",

    "skin_light": "淺色主題",
    "skin_dark": "深色主題",
    "skin_system": "系統預設",
    "skin_eye_care": "護眼模式",

    "lang_zh_cn": "简体中文",
    "lang_zh_tw": "繁體中文",
    "lang_en": "English",

    "help_guide": "操作指南",
    "help_faq": "常見問題",

    "folder_select": "資料夾選擇",
    "path_label": "路徑:",
    "browse": "瀏覽...",
    "folder_placeholder": "請選擇資料夾...",

    "rename_rules": "重新命名規則",
    "mode_prefix_suffix": "新增前綴/後綴",
    "mode_sequential": "數字序號命名",
    "mode_replace": "尋找取代",
    "mode_direct_input": "直接輸入檔名",
    "prefix": "前綴:",
    "suffix": "後綴:",
    "prefix_placeholder": "輸入前綴",
    "suffix_placeholder": "輸入後綴（不含副檔名）",
    "start_num": "起始序號:",
    "digits": "位數:",
    "seq_prefix": "序號前綴:",
    "seq_prefix_placeholder": "序號前綴（選填）",
    "find": "尋找:",
    "replace": "取代:",
    "find_placeholder": "尋找內容",
    "replace_placeholder": "取代為",
    "case_sensitive": "區分大小寫",
    "new_filename": "新檔名:",
    "direct_name_placeholder": "輸入新檔名（不含副檔名）",

    "output_location": "輸出位置",
    "output_original_dir": "原目錄",
    "output_custom_dir": "自訂資料夾",
    "output_custom_placeholder": "選擇輸出資料夾...",

    "preview": "預覽",
    "select_all": "全選",
    "deselect_all": "取消全選",
    "col_select": "選擇",
    "col_original": "原檔名",
    "col_new": "新檔名",
    "col_status": "狀態",
    "status_ready": "就緒",
    "status_conflict": "衝突",
    "status_no_change": "無變化",
    "status_skip": "跳過",

    "btn_refresh": "重新整理",
    "btn_undo": "復原重新命名",
    "btn_execute": "執行重新命名",

    "status_ready_msg": "就緒",
    "file_count": "檔案數: {total} (已選: {selected})",
    "file_count_zero": "檔案數: 0",
    "loaded_files": "已載入 {count} 個檔案",

    "tip": "提示",
    "confirm": "確認",
    "cancel": "取消",
    "ok": "確定",
    "no_selected_files": "沒有選中需要重新命名的檔案",
    "no_rename_needed": "沒有需要重新命名的檔案。",
    "conflict_skip": "有 {count} 個檔案因名稱衝突被跳過。",
    "confirm_rename": "即將重新命名 {count} 個檔案。",
    "conflict_note": "（{count} 個衝突檔案將被跳過）",
    "no_change_note": "（{count} 個無變化檔案將被跳過）",
    "confirm_execute": "確認執行？",
    "confirm_rename_title": "確認重新命名",
    "done": "完成",
    "done_msg": "成功重新命名 {count} 個檔案！\n可點擊「復原重新命名」恢復。",
    "partial_done": "部分完成",
    "success_count": "成功: {success}, 失敗: {errors}",
    "status_done": "完成: {success} 成功, {errors} 失敗, {conflicts} 衝突跳過",

    "no_undo_history": "沒有可復原的操作",
    "confirm_undo": "將復原上一次重新命名操作（{count} 個檔案）\n確認？",
    "confirm_undo_title": "確認復原",
    "undo_done": "復原完成",
    "undo_done_msg": "已恢復 {count} 個檔案的原名稱",
    "undo_partial": "部分復原",
    "undo_status": "復原完成: {success} 恢復, {errors} 失敗",

    "permission_error": "權限錯誤",
    "permission_error_msg": "無法存取該資料夾",

    "new_task_done": "已重置工作區",
    "config_saved": "配置已儲存",
    "config_saved_msg": "配置已儲存到：\n{path}",
    "export_done": "匯出完成",
    "export_done_msg": "對照表已匯出到：\n{path}",
    "export_no_data": "沒有可匯出的資料，請先選擇資料夾並設定重新命名規則",

    "guide_title": "操作指南",
    "guide_content": (
        "1. 點擊「瀏覽」選擇包含目標檔案的資料夾\n"
        "2. 選擇重新命名模式並配置參數\n"
        "3. 在預覽表中查看效果，勾選需要重新命名的檔案\n"
        "4. 選擇輸出位置（原目錄或自訂資料夾）\n"
        "5. 點擊「執行重新命名」完成操作\n"
        "6. 如需恢復，點擊「復原重新命名」"
    ),
    "faq_title": "常見問題",
    "faq_content": (
        "Q: 重新命名後可以復原嗎？\n"
        "A: 可以，點擊「復原重新命名」即可恢復上一次操作。\n\n"
        "Q: 出現檔名衝突怎麼辦？\n"
        "A: 衝突檔案會自動標記為紅色並跳過，不會覆蓋已有檔案。\n\n"
        "Q: 如何批次新增序號？\n"
        "A: 選擇「數字序號命名」模式，設定起始序號和位數即可。\n\n"
        "Q: 支援哪些檔案類型？\n"
        "A: 支援所有檔案類型，工具只修改檔名不修改檔案內容。"
    ),
}

_EN_US = {
    "app_title": "Batch File Renamer",
    "login_title": "Login - Batch File Renamer",
    "login_subtitle": "Please login to continue",
    "username": "Username",
    "password": "Password",
    "username_placeholder": "Enter username",
    "password_placeholder": "Enter password",
    "remember_password": "Remember password",
    "forgot_password": "Forgot password?",
    "login": "Login",
    "no_account": "No account?",
    "register": "Sign up",
    "err_empty_username": "Please enter username",
    "err_empty_password": "Please enter password",
    "err_auth_failed": "Invalid username or password",

    "nav_task": "Task",
    "nav_skin": "Theme",
    "nav_language": "Language",
    "nav_help": "Help",

    "task_new": "New",
    "task_save_config": "Save Config",
    "task_export_list": "Export List",

    "skin_light": "Light Theme",
    "skin_dark": "Dark Theme",
    "skin_system": "System Default",
    "skin_eye_care": "Eye Care",

    "lang_zh_cn": "简体中文",
    "lang_zh_tw": "繁體中文",
    "lang_en": "English",

    "help_guide": "User Guide",
    "help_faq": "FAQ",

    "folder_select": "Folder Selection",
    "path_label": "Path:",
    "browse": "Browse...",
    "folder_placeholder": "Select a folder...",

    "rename_rules": "Rename Rules",
    "mode_prefix_suffix": "Add Prefix/Suffix",
    "mode_sequential": "Sequential Numbering",
    "mode_replace": "Find & Replace",
    "mode_direct_input": "Direct Input",
    "prefix": "Prefix:",
    "suffix": "Suffix:",
    "prefix_placeholder": "Enter prefix",
    "suffix_placeholder": "Enter suffix (without extension)",
    "start_num": "Start number:",
    "digits": "Digits:",
    "seq_prefix": "Number prefix:",
    "seq_prefix_placeholder": "Number prefix (optional)",
    "find": "Find:",
    "replace": "Replace:",
    "find_placeholder": "Text to find",
    "replace_placeholder": "Replace with",
    "case_sensitive": "Case sensitive",
    "new_filename": "New name:",
    "direct_name_placeholder": "Enter new filename (without extension)",

    "output_location": "Output Location",
    "output_original_dir": "Original Directory",
    "output_custom_dir": "Custom Folder",
    "output_custom_placeholder": "Select output folder...",

    "preview": "Preview",
    "select_all": "Select All",
    "deselect_all": "Deselect All",
    "col_select": "Select",
    "col_original": "Original Name",
    "col_new": "New Name",
    "col_status": "Status",
    "status_ready": "Ready",
    "status_conflict": "Conflict",
    "status_no_change": "No Change",
    "status_skip": "Skip",

    "btn_refresh": "Refresh",
    "btn_undo": "Undo Rename",
    "btn_execute": "Execute Rename",

    "status_ready_msg": "Ready",
    "file_count": "Files: {total} (Selected: {selected})",
    "file_count_zero": "Files: 0",
    "loaded_files": "Loaded {count} files",

    "tip": "Notice",
    "confirm": "Confirm",
    "cancel": "Cancel",
    "ok": "OK",
    "no_selected_files": "No files selected for renaming",
    "no_rename_needed": "No files need renaming.",
    "conflict_skip": "{count} files skipped due to name conflicts.",
    "confirm_rename": "About to rename {count} files.",
    "conflict_note": "({count} conflicting files will be skipped)",
    "no_change_note": "({count} unchanged files will be skipped)",
    "confirm_execute": "Proceed?",
    "confirm_rename_title": "Confirm Rename",
    "done": "Done",
    "done_msg": "Successfully renamed {count} files!\nClick 'Undo Rename' to revert.",
    "partial_done": "Partially Done",
    "success_count": "Success: {success}, Failed: {errors}",
    "status_done": "Done: {success} success, {errors} failed, {conflicts} conflicts skipped",

    "no_undo_history": "No operations to undo",
    "confirm_undo": "Undo the last rename operation ({count} files)?\nConfirm?",
    "confirm_undo_title": "Confirm Undo",
    "undo_done": "Undo Complete",
    "undo_done_msg": "Restored original names for {count} files",
    "undo_partial": "Partially Undone",
    "undo_status": "Undo complete: {success} restored, {errors} failed",

    "permission_error": "Permission Error",
    "permission_error_msg": "Cannot access this folder",

    "new_task_done": "Workspace reset",
    "config_saved": "Config Saved",
    "config_saved_msg": "Config saved to:\n{path}",
    "export_done": "Export Complete",
    "export_done_msg": "Mapping exported to:\n{path}",
    "export_no_data": "No data to export. Select a folder and configure rename rules first.",

    "guide_title": "User Guide",
    "guide_content": (
        "1. Click 'Browse' to select a folder with target files\n"
        "2. Choose a rename mode and configure parameters\n"
        "3. Preview the results in the table, check files to rename\n"
        "4. Choose output location (original dir or custom folder)\n"
        "5. Click 'Execute Rename' to apply\n"
        "6. Click 'Undo Rename' to revert if needed"
    ),
    "faq_title": "FAQ",
    "faq_content": (
        "Q: Can I undo a rename?\n"
        "A: Yes, click 'Undo Rename' to revert the last operation.\n\n"
        "Q: What if there are filename conflicts?\n"
        "A: Conflicting files are marked in red and skipped automatically.\n\n"
        "Q: How to add sequential numbers?\n"
        "A: Select 'Sequential Numbering' mode, set start number and digits.\n\n"
        "Q: Which file types are supported?\n"
        "A: All file types. The tool only modifies filenames, not file content."
    ),
}

_LANGUAGES = {
    "zh_CN": _ZH_CN,
    "zh_TW": _ZH_TW,
    "en_US": _EN_US,
}


class I18n(QObject):
    language_changed = pyqtSignal()

    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = I18n()
        return cls._instance

    def __init__(self):
        super().__init__()
        self._current_lang = "zh_CN"

    def set_language(self, lang_code: str):
        if lang_code in _LANGUAGES and lang_code != self._current_lang:
            self._current_lang = lang_code
            self.language_changed.emit()

    def current_language(self) -> str:
        return self._current_lang

    def tr(self, key: str, **kwargs) -> str:
        text = _LANGUAGES[self._current_lang].get(key, key)
        if kwargs:
            text = text.format(**kwargs)
        return text
