"""Small shared helpers."""
from __future__ import annotations

import re
import time
from pathlib import Path

_USER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$")


class InvalidName(ValueError):
    pass


def safe_user_id(user_id: str) -> str:
    """Validate a user id so it can never escape its directory."""
    if not isinstance(user_id, str) or not _USER_RE.match(user_id):
        raise InvalidName(f"invalid user id: {user_id!r} (allowed: letters, digits, _ -; max 64)")
    return user_id


def safe_name(name: str) -> str:
    """Validate a note/file name (no slashes, no leading dot, no '..')."""
    if not isinstance(name, str) or not _NAME_RE.match(name) or ".." in name:
        raise InvalidName(f"invalid name: {name!r}")
    return name


def truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n...[truncated {len(text) - limit} chars]"


def estimate_tokens(text: str) -> int:
    """Crude token estimate (~4 chars/token). Used for budgets and the mock."""
    return max(1, len(text) // 4)


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def now() -> float:
    return time.time()
