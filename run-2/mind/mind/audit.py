"""Append-only, per-user audit log for every tool call and permission
decision.

Decision: JSON Lines on disk (one dict per line) — trivial to append
atomically, trivial to grep/replay, no DB dependency.
"""
from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from typing import Any, Dict, Iterator, Optional

from . import config


class AuditLog:
    def __init__(self, path: Optional[Path] = None):
        self.path = path or config.AUDIT_LOG_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def record(
        self,
        *,
        user_id: str,
        actor: str,
        action: str,
        tier: str,
        granted: bool,
        detail: Optional[Dict[str, Any]] = None,
        cost_usd: float = 0.0,
    ) -> Dict[str, Any]:
        entry = {
            "ts": time.time(),
            "user_id": user_id,
            "actor": actor,
            "action": action,
            "tier": tier,
            "granted": granted,
            "cost_usd": cost_usd,
            "detail": detail or {},
        }
        line = json.dumps(entry, sort_keys=True)
        with self._lock:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        return entry

    def read_all(self) -> Iterator[Dict[str, Any]]:
        if not self.path.exists():
            return
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield json.loads(line)

    def for_user(self, user_id: str):
        return [e for e in self.read_all() if e["user_id"] == user_id]
