import os
from typing import List, Tuple


class RenameHistory:
    def __init__(self):
        self.history: List[List[Tuple[str, str, str]]] = []

    def add_batch(self, batch: List[Tuple[str, str]], folder_path: str = "") -> None:
        if batch:
            tagged_batch = [(old, new, folder_path) for old, new in batch]
            self.history.append(tagged_batch)

    def get_last_batch(self) -> List[Tuple[str, str, str]]:
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

    def history_count(self) -> int:
        return len(self.history)

    def clear(self) -> None:
        self.history.clear()

    def undo_batch(self, folder_path: str, batch: List[Tuple[str, str, str]]) -> Tuple[int, int]:
        success = 0
        errors = 0
        for item in batch:
            if len(item) == 3:
                old_name, new_name, batch_folder = item
                target_folder = batch_folder if batch_folder else folder_path
            else:
                old_name, new_name = item[0], item[1]
                target_folder = folder_path
            new_path = os.path.join(target_folder, new_name)
            old_path = os.path.join(target_folder, old_name)
            try:
                os.rename(new_path, old_path)
                success += 1
            except OSError:
                errors += 1
        return success, errors

    def undo_all(self, folder_path: str) -> Tuple[int, int]:
        total_success = 0
        total_errors = 0
        while self.history:
            batch = self.history.pop()
            success, errors = self.undo_batch(folder_path, batch)
            total_success += success
            total_errors += errors
        return total_success, total_errors

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
