import os
import json
import hashlib
import re
import sys


class UserManager:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = UserManager()
        return cls._instance

    def __init__(self):
        self._data_file = self._get_data_path()
        self._users = self._load_users()

    def _get_data_path(self) -> str:
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, "users.json")

    def _load_users(self) -> dict:
        if not os.path.exists(self._data_file):
            return {}
        try:
            with open(self._data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_users(self):
        with open(self._data_file, "w", encoding="utf-8") as f:
            json.dump(self._users, f, ensure_ascii=False, indent=2)

    def _hash_password(self, password: str) -> str:
        salt = "batch_renamer_salt_2024"
        return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()

    def validate_username(self, username: str) -> str | None:
        if len(username) < 3:
            return "username_too_short"
        if len(username) > 20:
            return "username_too_long"
        if not re.match(r'^[a-zA-Z0-9_一-鿿]+$', username):
            return "username_invalid_chars"
        return None

    def validate_password(self, password: str) -> str | None:
        if len(password) < 6:
            return "password_too_short"
        if len(password) > 32:
            return "password_too_long"
        return None

    def user_exists(self, username: str) -> bool:
        return username in self._users

    def register(self, username: str, password: str) -> tuple[bool, str]:
        username_err = self.validate_username(username)
        if username_err:
            return False, username_err

        password_err = self.validate_password(password)
        if password_err:
            return False, password_err

        if self.user_exists(username):
            return False, "username_exists"

        self._users[username] = {
            "password_hash": self._hash_password(password)
        }
        self._save_users()
        return True, "register_success"

    def authenticate(self, username: str, password: str) -> bool:
        if not username or not password:
            return False
        if username not in self._users:
            return False
        stored_hash = self._users[username]["password_hash"]
        return stored_hash == self._hash_password(password)
