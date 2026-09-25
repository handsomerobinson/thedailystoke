"""Append-only, hash-chained JSONL audit log.

Every record carries `prev` (hash of the previous record) and `hash` (sha256 over the
canonical JSON of the record without `hash`). `verify()` recomputes the chain and reports
the first broken line. Secrets are redacted and large fields truncated before writing.

Limit (stated plainly): a hash chain is tamper-EVIDENT, not tamper-proof. Someone with write
access can rewrite the entire file and recompute every hash. `head()` returns the latest
hash so it can be anchored somewhere the attacker cannot write (printed in reports).
"""
from __future__ import annotations

import fcntl
import json
import os
import threading
from pathlib import Path

from .util import Clock, canonical_json, redact_obj, sha256_hex, truncate

GENESIS = "0" * 64


class AuditError(Exception):
    pass


class AuditLog:
    def __init__(self, path: Path | str, clock: Clock | None = None, field_limit: int = 2000):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.clock = clock or Clock()
        self.field_limit = field_limit
        self._lock = threading.Lock()

    def _tail(self) -> tuple[int, str]:
        """Return (last seq, last hash) by reading the final line of the file."""
        if not self.path.exists() or self.path.stat().st_size == 0:
            return 0, GENESIS
        with open(self.path, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            back = min(size, 65536)
            f.seek(size - back)
            lines = f.read().splitlines()
        for raw in reversed(lines):
            if raw.strip():
                try:
                    rec = json.loads(raw)
                    return int(rec["seq"]), rec["hash"]
                except Exception as e:
                    raise AuditError(f"audit log tail is corrupt: {e}") from e
        return 0, GENESIS

    def _clip(self, obj):
        if isinstance(obj, str):
            return truncate(obj, self.field_limit)
        if isinstance(obj, dict):
            return {k: self._clip(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._clip(v) for v in obj[:50]]
        return obj

    def write(self, event: str, **fields) -> dict:
        """Append one record. Raises AuditError on failure (callers decide fail-open/closed)."""
        with self._lock:
            try:
                with open(self.path, "a+", encoding="utf-8") as f:
                    fcntl.flock(f, fcntl.LOCK_EX)  # serialise writers across processes
                    try:
                        seq, prev = self._tail()
                        body = {k: v for k, v in self._clip(redact_obj(fields)).items()
                                if k not in ("seq", "ts", "event", "prev", "hash")}
                        rec = {"seq": seq + 1, "ts": round(self.clock.now(), 3), "event": event,
                               **body, "prev": prev}
                        rec["hash"] = sha256_hex(canonical_json(rec))
                        f.write(canonical_json(rec) + "\n")
                        f.flush()
                        os.fsync(f.fileno())
                    finally:
                        fcntl.flock(f, fcntl.LOCK_UN)
                return rec
            except AuditError:
                raise
            except Exception as e:
                raise AuditError(f"cannot write audit log: {e}") from e

    def records(self, user: str | None = None) -> list[dict]:
        if not self.path.exists():
            return []
        out = []
        with open(self.path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if user is None or rec.get("user") == user:
                        out.append(rec)
        return out

    def verify(self) -> tuple[bool, str]:
        if not self.path.exists():
            return True, "empty log"
        prev = GENESIS
        n = 0
        with open(self.path, encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    return False, f"line {lineno}: not valid JSON"
                h = rec.pop("hash", None)
                if rec.get("prev") != prev:
                    return False, f"line {lineno}: chain broken (prev mismatch)"
                if sha256_hex(canonical_json(rec)) != h:
                    return False, f"line {lineno}: record hash mismatch (edited)"
                prev = h
                n += 1
        return True, f"{n} records verified, head={prev[:16]}"

    def head(self) -> str:
        return self._tail()[1]
