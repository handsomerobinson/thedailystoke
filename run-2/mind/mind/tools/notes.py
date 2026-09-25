"""File/note storage tool: per-user notes under the gitignored data dir.

Decision: notes are plain .txt files named by a sanitized title, one dir
per user (mirrors memory's per-user isolation) — no DB needed for
something this simple, and it's trivially inspectable on disk.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from .. import config
from ..permissions import PermissionTier
from .base import Tool, ToolResult

_SAFE_RE = re.compile(r"[^A-Za-z0-9_.-]")


def _safe_name(name: str) -> str:
    cleaned = _SAFE_RE.sub("_", name).strip("._") or "note"
    return cleaned[:80]


class NotesTool(Tool):
    name = "notes"
    tier = PermissionTier.STATE_CHANGING  # writes/deletes are state changes
    description = "Read, write, list, or delete simple text notes for a user."

    def __init__(self, base_dir: Optional[Path] = None, max_bytes: int = config.DEFAULT_NOTE_MAX_BYTES):
        self.base_dir = base_dir or config.NOTES_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.max_bytes = max_bytes

    def _user_dir(self, user_id: str) -> Path:
        safe_user = _SAFE_RE.sub("_", user_id) or "anonymous"
        d = self.base_dir / safe_user
        d.mkdir(parents=True, exist_ok=True)
        return d

    def describe_call(self, **kwargs) -> str:
        return f"notes: {kwargs.get('action')} {kwargs.get('title', '')!r}"

    def run(
        self,
        action: str = "list",
        user_id: str = "anonymous",
        title: str = "",
        body: str = "",
        **kwargs,
    ) -> ToolResult:
        d = self._user_dir(user_id)

        if action == "write":
            if not title:
                return ToolResult(ok=False, output="", error="title required to write a note")
            body_bytes = body.encode("utf-8")
            if len(body_bytes) > self.max_bytes:
                return ToolResult(
                    ok=False,
                    output="",
                    error=f"note body exceeds {self.max_bytes} byte cap ({len(body_bytes)} bytes)",
                )
            path = d / f"{_safe_name(title)}.txt"
            path.write_text(body, encoding="utf-8")
            return ToolResult(ok=True, output=f"saved note {path.name}", meta={"path": str(path)})

        if action == "read":
            if not title:
                return ToolResult(ok=False, output="", error="title required to read a note")
            path = d / f"{_safe_name(title)}.txt"
            if not path.exists():
                return ToolResult(ok=False, output="", error=f"no such note: {title}")
            return ToolResult(ok=True, output=path.read_text(encoding="utf-8"))

        if action == "list":
            names = sorted(p.stem for p in d.glob("*.txt"))
            return ToolResult(ok=True, output="\n".join(names))

        if action == "delete":
            if not title:
                return ToolResult(ok=False, output="", error="title required to delete a note")
            path = d / f"{_safe_name(title)}.txt"
            if not path.exists():
                return ToolResult(ok=False, output="", error=f"no such note: {title}")
            path.unlink()
            return ToolResult(ok=True, output=f"deleted note {title}")

        return ToolResult(ok=False, output="", error=f"unknown action: {action}")
