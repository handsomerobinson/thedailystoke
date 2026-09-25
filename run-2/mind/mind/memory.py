"""Persistent, per-user-isolated memory: episodic task history + semantic
lesson store, with simple keyword retrieval that actually recalls.

Decision: one SQLite file per user (<data>/memory/<user_id>.db) — true
filesystem-level isolation between users (no shared table + WHERE clause
that a bug could leak across), zero external dependency (sqlite3 is
stdlib), and it survives process restarts for free.

Decision: retrieval is FTS-less keyword overlap scoring (stdlib only, no
embeddings) — good enough to "actually recall" relevant lessons/facts in a
demo/test scale corpus, and honestly documented as a limitation (see
README "could not build").
"""
from __future__ import annotations

import re
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from . import config

_WORD_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> List[str]:
    return _WORD_RE.findall(text.lower())


def _safe_user_id(user_id: str) -> str:
    # Decision: sanitize user_id before using it as a filename component —
    # a hostile or malformed user_id must never escape the memory dir.
    cleaned = re.sub(r"[^A-Za-z0-9_.-]", "_", user_id)
    if not cleaned:
        raise ValueError("user_id must contain at least one safe character")
    return cleaned


@dataclass
class MemoryItem:
    id: int
    kind: str  # "episode" | "lesson" | "fact"
    text: str
    ts: float
    task_id: Optional[str] = None
    score: float = 0.0


class UserMemory:
    """All memory for exactly one user. Never share an instance across
    users — that would defeat the point of the per-file isolation."""

    def __init__(self, user_id: str, base_dir: Optional[Path] = None):
        self.user_id = user_id
        safe = _safe_user_id(user_id)
        base = base_dir or config.MEMORY_DIR
        base.mkdir(parents=True, exist_ok=True)
        self.db_path = base / f"{safe}.db"
        self._conn = sqlite3.connect(self.db_path)
        self._conn.execute(
            """CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL,
                text TEXT NOT NULL,
                task_id TEXT,
                ts REAL NOT NULL
            )"""
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    # -- writes ---------------------------------------------------------
    def remember(self, kind: str, text: str, task_id: Optional[str] = None) -> int:
        cur = self._conn.execute(
            "INSERT INTO memory (kind, text, task_id, ts) VALUES (?, ?, ?, ?)",
            (kind, text, task_id, time.time()),
        )
        self._conn.commit()
        return cur.lastrowid

    def remember_episode(self, task_id: str, text: str) -> int:
        return self.remember("episode", text, task_id)

    def remember_lesson(self, task_id: str, text: str) -> int:
        return self.remember("lesson", text, task_id)

    # -- reads ------------------------------------------------------------
    def all(self, kind: Optional[str] = None) -> List[MemoryItem]:
        if kind:
            rows = self._conn.execute(
                "SELECT id, kind, text, task_id, ts FROM memory WHERE kind=? ORDER BY ts", (kind,)
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT id, kind, text, task_id, ts FROM memory ORDER BY ts"
            ).fetchall()
        return [MemoryItem(id=r[0], kind=r[1], text=r[2], task_id=r[3], ts=r[4]) for r in rows]

    def recall(self, query: str, kind: Optional[str] = None, limit: int = 5) -> List[MemoryItem]:
        """Keyword-overlap retrieval: score = |query tokens intersect item
        tokens| / |query tokens|, ties broken by recency. Actually returns
        the relevant items for the tokens present, unlike a stub that
        always returns the same thing."""
        q_tokens = set(_tokenize(query))
        if not q_tokens:
            return []
        items = self.all(kind=kind)
        scored: List[MemoryItem] = []
        for it in items:
            it_tokens = set(_tokenize(it.text))
            if not it_tokens:
                continue
            overlap = len(q_tokens & it_tokens)
            if overlap == 0:
                continue
            it.score = overlap / len(q_tokens)
            scored.append(it)
        scored.sort(key=lambda x: (x.score, x.ts), reverse=True)
        return scored[:limit]

    def lessons_for(self, query: str, limit: int = 3) -> List[MemoryItem]:
        return self.recall(query, kind="lesson", limit=limit)

    def wipe(self) -> None:
        """Irreversible: delete all memory for this user. Gated at the
        agent/permission layer, not here — this method just does it."""
        self._conn.execute("DELETE FROM memory")
        self._conn.commit()


class MemoryStore:
    """Factory/cache of UserMemory instances keyed by user_id — the thing
    the rest of the system actually holds a reference to."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or config.MEMORY_DIR
        self._cache: dict[str, UserMemory] = {}

    def for_user(self, user_id: str) -> UserMemory:
        if user_id not in self._cache:
            self._cache[user_id] = UserMemory(user_id, base_dir=self.base_dir)
        return self._cache[user_id]

    def close_all(self) -> None:
        for m in self._cache.values():
            m.close()
        self._cache.clear()
