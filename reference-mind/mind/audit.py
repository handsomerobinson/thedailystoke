"""Append-only, hash-chained audit log (JSON Lines).

Every entry carries the SHA-256 of the previous entry, so any edit, deletion
or reordering of past lines is detected by verify().  This is *tamper
evidence*, not tamper *proofing*: someone with write access can rewrite the
whole chain.  BUILD ROUND (MC6/MC16): an optional MAC key (held outside the data dir) makes
every entry unforgeable without that key, and an optional external anchor records heads, so a log that
is shorter than, or diverges from, its last anchored head -- or is missing while an anchor exists --
fails verify() as TAMPERED instead of reading as fresh/absent.

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

from .purpose import POLICY_VERSION

GENESIS = "0" * 64


class AuditError(Exception):
    pass


def _digest(prev: str, body: dict[str, Any]) -> str:
    canon = json.dumps(body, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256((prev + canon).encode()).hexdigest()


class AuditLog:
    def __init__(self, path: Path, mac_key: bytes | None = None, anchor=None, stream: str | None = None,
                 anchor_every: bool = False, require_anchor: bool = False, purpose: str = "accountability"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self.mac_key = mac_key
        self.anchor = anchor
        self.stream = stream or f"log:{self.path.name}"
        self.anchor_every = anchor_every
        self.require_anchor = require_anchor
        self.purpose = purpose

    def _mac(self, body: dict[str, Any]) -> str:
        import hmac as _hmac
        canon = json.dumps(body, sort_keys=True, separators=(",", ":"), default=str).encode()
        return _hmac.new(self.mac_key, canon, hashlib.sha256).hexdigest()

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
        body = {"ts": round(time.time(), 3), "event": event, **fields,
                "purpose": self.purpose, "policy_version": POLICY_VERSION}  # MC8
        if self.mac_key is not None:
            body["mac"] = self._mac(body)
        count = 0
        try:
            with self._lock, open(self.path, "a+b") as fh:
                fcntl.flock(fh, fcntl.LOCK_EX)
                try:
                    prev = self._last_hash(fh)
                    entry = {**body, "prev": prev, "hash": _digest(prev, body)}
                    fh.seek(0, 2)
                    fh.write((json.dumps(entry, sort_keys=True, default=str) + "\n").encode("utf-8"))
                    fh.flush()
                    if self.anchor is not None and self.anchor_every:
                        fh.seek(0)
                        count = sum(1 for ln in fh.read().split(b"\n") if ln.strip())
                finally:
                    fcntl.flock(fh, fcntl.LOCK_UN)
        except OSError as exc:
            raise AuditError(f"cannot write audit log: {exc}") from exc
        if count:
            try:
                self.anchor.publish(self.stream, {"count": count, "head": entry["hash"]})
            except Exception as exc:  # noqa: BLE001 - an unanchored change must not pass as done
                raise AuditError(f"cannot anchor log head: {exc}") from exc
        return entry

    def anchor_head(self) -> dict[str, Any] | None:
        """Publish the current head to the external anchor (the audit log does this at every task end)."""
        if self.anchor is None:
            return None
        items = self.entries()
        if not items:
            return None
        last = self.anchor.latest(self.stream)
        if last and last.get("count") == len(items) and last.get("head") == items[-1].get("hash"):
            return last
        return self.anchor.publish(self.stream, {"count": len(items), "head": items[-1].get("hash")})

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
        items = self.entries()
        for i, entry in enumerate(items):
            if "hash" not in entry:
                return False, f"line {i + 1}: unparseable"
            body = {k: v for k, v in entry.items() if k not in ("prev", "hash")}
            if entry.get("prev") != prev:
                return False, f"line {i + 1}: chain broken (prev mismatch)"
            if _digest(prev, body) != entry["hash"]:
                return False, f"line {i + 1}: content altered (hash mismatch)"
            if self.mac_key is not None:
                unmac = {k: v for k, v in body.items() if k != "mac"}
                import hmac as _hmac
                if not _hmac.compare_digest(str(body.get("mac", "")), self._mac(unmac)):
                    return False, f"line {i + 1}: entry not signed with this mind's key (forged or foreign entry)"
            prev = entry["hash"]
        if self.anchor is not None:
            try:
                last = self.anchor.latest(self.stream)
            except Exception as exc:  # noqa: BLE001 - an unreadable anchor is not a pass
                return False, f"anchor unreadable: {exc}"
            if last:
                n = int(last.get("count", 0))
                if len(items) < n:
                    what = "missing" if not items else f"has {len(items)} entries"
                    return False, (f"anchor says this log had {n} entries (head {str(last.get('head'))[:12]}) but it is "
                                   f"{what}: deleted or truncated outside the procedure")
                if n and items[n - 1].get("hash") != last.get("head"):
                    return False, f"entry {n} differs from its anchored head: history rewritten"
            elif items and self.require_anchor:
                return False, "log has entries but no anchored head: minted outside the procedure"
        return True, f"ok ({len(items)} entries, head {prev[:12]})"

    def tail(self, n: int = 20, user: str | None = None) -> list[dict[str, Any]]:
        items = self.entries()
        if user:
            items = [e for e in items if e.get("user") == user]
        return items[-n:]
