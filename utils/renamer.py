import os
import re


class Renamer:
    MODE_PREFIX_SUFFIX = 0
    MODE_SEQUENTIAL = 1
    MODE_REPLACE = 2
    MODE_DIRECT_INPUT = 3

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

        return original