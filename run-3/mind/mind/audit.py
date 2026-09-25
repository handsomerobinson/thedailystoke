"""Append-only, hash-chained audit log (JSON Lines).

Every entry carries the SHA-256 of the previous entry, so any edit, deletion
or reordering of past lines is detected by verify().  This is *tamper
evidence*, not tamper *proofing*: someone with write access can rewrite the
whole chain.  Anchor the latest hash elsewhere if that matters to you.

Appends take an exclusive flock so the daemon and the CLI can share a log.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import threading
import time
from pathlib import Path
from typing import Any

GENESIS = "0" * 64


class AuditError(Exception):
    pass


def _digest(prev: str, body: dict[str, Any]) -> str:
    canon = json.dumps(body, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256((prev + canon).encode()).hexdigest()


class AuditLog:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _last_hash(self, fh) -> str:
        """Hash of the last entry, reading only the file tail (O(1) per append)."""
        fh.seek(0, 2)
        size = fh.tell()
        if size == 0:
            return GENESIS
        chunk = 4096
        data = b""
        pos = size
        raw = fh
        while pos > 0:
            step = min(chunk, pos)
            pos -= step
            raw.seek(pos)
            data = raw.read(step) + data
            lines = [ln for ln in data.split(b"\n") if ln.strip()]
            if len(lines) >= 2 or pos == 0:
                break
        lines = [ln for ln in data.split(b"\n") if ln.strip()]
        if not lines:
            return GENESIS
        try:
            return json.loads(lines[-1].decode("utf-8"))["hash"]
        except (ValueError, KeyError, UnicodeDecodeError):
            raise AuditError("audit log tail is corrupt; refusing to append (run `audit verify`)")

    def record(self, event: str, **fields: Any) -> dict[str, Any]:
        """Append an entry. Raises AuditError if it cannot be written.

        Callers that are about to change state must treat AuditError as a
        reason NOT to act (fail closed).
        """
        body = {"ts": round(time.time(), 3), "event": event, **fields}
        try:
            with self._lock, open(self.path, "a+b") as fh:
                fcntl.flock(fh, fcntl.LOCK_EX)
                try:
                    prev = self._last_hash(fh)
                    entry = {**body, "prev": prev, "hash": _digest(prev, body)}
                    fh.seek(0, 2)
                    fh.write((json.dumps(entry, sort_keys=True, default=str) + "\n").encode("utf-8"))
                    fh.flush()
                finally:
                    fcntl.flock(fh, fcntl.LOCK_UN)
        except OSError as exc:
            raise AuditError(f"cannot write audit log: {exc}") from exc
        return entry

    def entries(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        out = []
        with open(self.path, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    try:
                        out.append(json.loads(line))
                    except ValueError:
                        out.append({"event": "<corrupt line>", "raw": line.strip()[:200]})
        return out

    def verify(self) -> tuple[bool, str]:
        prev = GENESIS
        for i, entry in enumerate(self.entries()):
            if "hash" not in entry:
                return False, f"line {i + 1}: unparseable"
            body = {k: v for k, v in entry.items() if k not in ("prev", "hash")}
            if entry.get("prev") != prev:
                return False, f"line {i + 1}: chain broken (prev mismatch)"
            if _digest(prev, body) != entry["hash"]:
                return False, f"line {i + 1}: content altered (hash mismatch)"
            prev = entry["hash"]
        return True, f"ok ({len(self.entries())} entries, head {prev[:12]})"

    def tail(self, n: int = 20, user: str | None = None) -> list[dict[str, Any]]:
        items = self.entries()
        if user:
            items = [e for e in items if e.get("user") == user]
        return items[-n:]
