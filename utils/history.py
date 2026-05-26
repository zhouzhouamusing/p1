import os
from typing import List, Tuple


class RenameHistory:
    def __init__(self):
        self.history: List[List[Tuple[str, str]]] = []

    def add_batch(self, batch: List[Tuple[str, str]]) -> None:
        if batch:
            self.history.append(batch)

    def get_last_batch(self) -> List[Tuple[str, str]]:
        if self.history:
            return self.history[-1]
        return []

    def undo_last(self) -> bool:
        if self.history:
            self.history.pop()
            return True
        return False

    def has_history(self) -> bool:
        return len(self.history) > 0

    def clear(self) -> None:
        self.history.clear()

    def undo_batch(self, folder_path: str, batch: List[Tuple[str, str]]) -> Tuple[int, int]:
        success = 0
        errors = 0
        for old_name, new_name in batch:
            new_path = os.path.join(folder_path, new_name)
            old_path = os.path.join(folder_path, old_name)
            try:
                os.rename(new_path, old_path)
                success += 1
            except OSError:
                errors += 1
        return success, errors

    def execute_batch(self, folder_path: str, batch: List[Tuple[str, str]]) -> Tuple[int, int]:
        success = 0
        errors = 0
        for old_name, new_name in batch:
            old_path = os.path.join(folder_path, old_name)
            new_path = os.path.join(folder_path, new_name)
            try:
                os.rename(old_path, new_path)
                success += 1
            except OSError:
                errors += 1
        return success, errors