import os
import re
from datetime import datetime


class Renamer:
    MODE_PREFIX_SUFFIX = 0
    MODE_SEQUENTIAL = 1
    MODE_REPLACE = 2
    MODE_DIRECT_INPUT = 3
    MODE_REGEX = 4
    MODE_DATETIME = 5
    MODE_ATTRIBUTES = 6
    MODE_SEQ_ENHANCED = 7

    def __init__(self):
        self.mode = self.MODE_PREFIX_SUFFIX
        self.prefix = ""
        self.suffix = ""
        self.start_num = 1
        self.digits = 3
        self.seq_prefix = ""
        self.find_text = ""
        self.replace_text = ""
        self.case_sensitive = True
        self.direct_name = ""
        self.regex_pattern = ""
        self.regex_replace = ""
        self.datetime_format = "IMG_{Y}{M}{D}_{h}{m}{s}"
        self.datetime_source = "modified"
        self.attr_template = "{name}_{size}"
        self.seq_enh_prefix = ""
        self.seq_enh_suffix = ""
        self.seq_enh_start = 1
        self.seq_enh_step = 1
        self.seq_enh_digits = 3
        self.seq_enh_format = "decimal"

        self._folder_path = ""
        self._warnings = []

    def set_folder_path(self, path: str):
        self._folder_path = path

    def get_warnings(self) -> list:
        return self._warnings

    def clear_warnings(self):
        self._warnings = []

    def generate_new_name(self, original: str, index: int) -> str:
        name, ext = os.path.splitext(original)

        if self.mode == self.MODE_PREFIX_SUFFIX:
            return f"{self.prefix}{name}{self.suffix}{ext}"

        elif self.mode == self.MODE_SEQUENTIAL:
            num_str = str(self.start_num + index).zfill(self.digits)
            return f"{self.seq_prefix}{num_str}{ext}"

        elif self.mode == self.MODE_REPLACE:
            if not self.find_text:
                return original
            if self.case_sensitive:
                new_name = name.replace(self.find_text, self.replace_text)
            else:
                new_name = re.sub(re.escape(self.find_text), self.replace_text, name, flags=re.IGNORECASE)
            return f"{new_name}{ext}"

        elif self.mode == self.MODE_DIRECT_INPUT:
            if not self.direct_name:
                return original
            return f"{self.direct_name}{ext}"

        elif self.mode == self.MODE_REGEX:
            return self._generate_regex(name, ext, original)

        elif self.mode == self.MODE_DATETIME:
            return self._generate_datetime(original, name, ext)

        elif self.mode == self.MODE_ATTRIBUTES:
            return self._generate_attributes(original, name, ext)

        elif self.mode == self.MODE_SEQ_ENHANCED:
            return self._generate_seq_enhanced(name, ext, index)

        return original

    def _generate_regex(self, name: str, ext: str, original: str) -> str:
        if not self.regex_pattern:
            return f"{name}{ext}"
        try:
            pattern = re.compile(self.regex_pattern)
            new_name = pattern.sub(self.regex_replace, name)
            return f"{new_name}{ext}"
        except re.error as e:
            self._warnings.append(f"[{original}] regex error: {e}")
            return f"{name}{ext}"

    def _generate_datetime(self, original: str, name: str, ext: str) -> str:
        file_path = os.path.join(self._folder_path, original) if self._folder_path else original
        fallback = False
        try:
            if self.datetime_source == "created":
                timestamp = os.path.getctime(file_path)
            else:
                timestamp = os.path.getmtime(file_path)
            dt = datetime.fromtimestamp(timestamp)
        except (OSError, ValueError):
            dt = datetime.now()
            fallback = True
            self._warnings.append(f"[{original}] time_fallback")

        fmt = self.datetime_format
        result = fmt.replace("{Y}", str(dt.year).zfill(4))
        result = result.replace("{M}", str(dt.month).zfill(2))
        result = result.replace("{D}", str(dt.day).zfill(2))
        result = result.replace("{h}", str(dt.hour).zfill(2))
        result = result.replace("{m}", str(dt.minute).zfill(2))
        result = result.replace("{s}", str(dt.second).zfill(2))
        result = result.replace("{name}", name)
        if fallback:
            result = result + "~"
        return f"{result}{ext}"

    def _generate_attributes(self, original: str, name: str, ext: str) -> str:
        file_path = os.path.join(self._folder_path, original) if self._folder_path else original
        fallback = False
        try:
            size_bytes = os.path.getsize(file_path)
        except OSError:
            size_bytes = 0
            fallback = True
            self._warnings.append(f"[{original}] size_fallback")

        size_str = self._format_size(size_bytes)
        ext_type = ext[1:] if ext else "unknown"

        result = self.attr_template
        result = result.replace("{name}", name)
        result = result.replace("{size}", size_str)
        result = result.replace("{type}", ext_type)
        result = result.replace("{ext}", ext_type)
        if fallback:
            result = result + "~"
        return f"{result}{ext}"

    def _generate_seq_enhanced(self, name: str, ext: str, index: int) -> str:
        num = self.seq_enh_start + index * self.seq_enh_step
        num_str = self._format_number(num, self.seq_enh_format, self.seq_enh_digits)
        return f"{self.seq_enh_prefix}{num_str}{self.seq_enh_suffix}{ext}"

    def _format_number(self, num: int, fmt: str, digits: int) -> str:
        if fmt == "roman":
            return self._to_roman(num)
        elif fmt == "alpha_upper":
            return self._to_alpha(num).upper()
        elif fmt == "alpha_lower":
            return self._to_alpha(num).lower()
        elif fmt == "hex":
            return hex(num)[2:].upper().zfill(digits)
        else:
            return str(num).zfill(digits)

    @staticmethod
    def _to_roman(num: int) -> str:
        if num <= 0 or num > 3999:
            return str(num)
        val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        syms = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
        result = ''
        for i in range(len(val)):
            while num >= val[i]:
                result += syms[i]
                num -= val[i]
        return result

    @staticmethod
    def _to_alpha(num: int) -> str:
        if num <= 0:
            return str(num)
        result = ''
        while num > 0:
            num -= 1
            result = chr(65 + num % 26) + result
            num //= 26
        return result

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        if size_bytes < 1024:
            return f"{size_bytes}B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes // 1024}KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{round(size_bytes / (1024 * 1024), 1)}MB"
        else:
            return f"{round(size_bytes / (1024 * 1024 * 1024), 1)}GB"
