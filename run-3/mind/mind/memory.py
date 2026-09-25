"""Persistent, per-user isolated memory with hybrid lexical retrieval.

Isolation is structural and double-checked:
  * each user has their OWN SQLite file under data/users/<user_id>/memory.db
    (user ids are validated so they cannot traverse paths), and
  * every row also carries an ``owner`` column that every query filters on,
    so a mis-wired path still cannot leak another user's rows.

Kinds of memory:
  fact        things about the user ("prefers metric units")
  episode     one-line outcome of each past task
  reflection  verbal lessons written after failures (Reflexion)
  note        free-form saved snippets

Retrieval = BM25 over stemmed tokens + character-trigram similarity (catches
morphology/typos BM25 misses) + recency + importance, and for reflections a
Laplace-smoothed usefulness score learned from whether the lesson helped.
It is lexical: it will NOT match pure synonyms ("car" vs "automobile").
Plug an embedding model in via ``MemoryStore.search(extra_scorer=...)`` if you
need semantic recall; the zero-key build deliberately ships none.
"""
from __future__ import annotations

import json
import math
import re
import sqlite3
import threading
import time
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable

from .util import safe_user_id

KINDS = ("fact", "episode", "reflection", "note")

_STOP = set("""a an the and or but if then of to in on at for from by with about as is are was were be been being
it its this that these those i me my you your we our they them their he she his her do does did done have has had
what which who whom how why when where can could should would will shall may might must not no yes so than too very
just also into over under up down out please""".split())

_WORD = re.compile(r"[a-z0-9]+")


def stem(tok: str) -> str:
    """Tiny suffix stripper (not Porter): running->run, preferences->prefer."""
    for suf in ("ingly", "edly", "ences", "ence", "ing", "ed", "ies", "es", "s", "ly"):
        if len(tok) > len(suf) + 2 and tok.endswith(suf):
            base = tok[: -len(suf)] + ("y" if suf == "ies" else "")
            if suf in ("ing", "ed", "ingly", "edly") and len(base) > 2 and base[-1] == base[-2] and base[-1] not in "lsz":
                base = base[:-1]
            return base
    return tok


def tokenize(text: str) -> list[str]:
    return [stem(t) for t in _WORD.findall(text.lower()) if t not in _STOP]


def trigrams(text: str) -> set[str]:
    s = " " + " ".join(_WORD.findall(text.lower())) + " "
    return {s[i:i + 3] for i in range(len(s) - 2)}


def _normalize(text: str) -> str:
    return " ".join(_WORD.findall(text.lower()))


@dataclass
class MemoryItem:
    id: int
    kind: str
    text: str
    meta: dict[str, Any] = field(default_factory=dict)
    importance: float = 0.5
    created: float = 0.0
    helped: int = 0
    hurt: int = 0
    score: float = 0.0

    @property
    def utility(self) -> float:
        return (self.helped + 1) / (self.helped + self.hurt + 2)


class MemoryStore:
    SCHEMA = """
    CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner TEXT NOT NULL,
        kind TEXT NOT NULL,
        text TEXT NOT NULL,
        norm TEXT NOT NULL,
        meta TEXT NOT NULL DEFAULT '{}',
        importance REAL NOT NULL DEFAULT 0.5,
        created REAL NOT NULL,
        updated REAL NOT NULL,
        hits INTEGER NOT NULL DEFAULT 1,
        helped INTEGER NOT NULL DEFAULT 0,
        hurt INTEGER NOT NULL DEFAULT 0,
        archived INTEGER NOT NULL DEFAULT 0,
        UNIQUE(owner, kind, norm)
    );
    CREATE INDEX IF NOT EXISTS idx_owner_kind ON memories(owner, kind, archived);
    """

    MAX_SCAN = 20000  # retrieval scans at most this many most-recent rows per query
    MAX_TEXT = 8000

    def __init__(self, data_dir: Path, user_id: str, clock: Callable[[], float] = time.time):
        self.user_id = safe_user_id(user_id)
        self.dir = Path(data_dir) / "users" / self.user_id
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / "memory.db"
        self.clock = clock
        self._lock = threading.RLock()
        self._db = sqlite3.connect(str(self.path), timeout=10, check_same_thread=False)
        self._db.row_factory = sqlite3.Row
        try:
            self._db.execute("PRAGMA journal_mode=WAL")
        except sqlite3.DatabaseError:
            pass
        self._db.executescript(self.SCHEMA)
        self._cache: dict[tuple[int, float], tuple[Counter, set[str], int]] = {}

    # -- writes ------------------------------------------------------------
    def add(self, kind: str, text: str, meta: dict | None = None, importance: float = 0.5) -> int:
        if kind not in KINDS:
            raise ValueError(f"unknown memory kind {kind!r}")
        text = (text or "").strip()[: self.MAX_TEXT]
        if not text:
            raise ValueError("empty memory")
        norm = _normalize(text) or text
        ts = self.clock()
        meta_json = json.dumps(meta or {}, default=str)
        with self._lock, self._db:
            row = self._db.execute(
                "SELECT id, hits FROM memories WHERE owner=? AND kind=? AND norm=?",
                (self.user_id, kind, norm)).fetchone()
            if row:  # dedupe: reinforce instead of duplicating
                self._db.execute(
                    "UPDATE memories SET hits=hits+1, updated=?, archived=0, importance=MAX(importance, ?) WHERE id=? AND owner=?",
                    (ts, importance, row["id"], self.user_id))
                return int(row["id"])
            cur = self._db.execute(
                "INSERT INTO memories(owner, kind, text, norm, meta, importance, created, updated) VALUES (?,?,?,?,?,?,?,?)",
                (self.user_id, kind, text, norm, meta_json, float(importance), ts, ts))
            return int(cur.lastrowid)

    def record_outcome(self, ids: Iterable[int], helped: bool) -> None:
        """Credit/blame reflections that were in context for a trial.

        A lesson that keeps failing to help (hurt >= 3, never helped) is
        archived so it stops crowding the context.
        """
        col = "helped" if helped else "hurt"
        with self._lock, self._db:
            for mid in ids:
                self._db.execute(f"UPDATE memories SET {col}={col}+1, updated=? WHERE id=? AND owner=?",
                                 (self.clock(), int(mid), self.user_id))
            self._db.execute(
                "UPDATE memories SET archived=1 WHERE owner=? AND kind='reflection' AND hurt>=3 AND helped=0",
                (self.user_id,))

    def delete(self, mid: int) -> bool:
        with self._lock, self._db:
            cur = self._db.execute("DELETE FROM memories WHERE id=? AND owner=?", (int(mid), self.user_id))
            return cur.rowcount > 0

    # -- reads -------------------------------------------------------------
    def _item(self, row: sqlite3.Row, score: float = 0.0) -> MemoryItem:
        try:
            meta = json.loads(row["meta"])
        except ValueError:
            meta = {}
        return MemoryItem(id=row["id"], kind=row["kind"], text=row["text"], meta=meta,
                          importance=row["importance"], created=row["created"],
                          helped=row["helped"], hurt=row["hurt"], score=score)

    def get(self, mid: int) -> MemoryItem | None:
        with self._lock:
            row = self._db.execute("SELECT * FROM memories WHERE id=? AND owner=?", (int(mid), self.user_id)).fetchone()
        return self._item(row) if row else None

    def recent(self, kind: str | None = None, n: int = 10) -> list[MemoryItem]:
        q = "SELECT * FROM memories WHERE owner=? AND archived=0"
        args: list[Any] = [self.user_id]
        if kind:
            q += " AND kind=?"
            args.append(kind)
        q += " ORDER BY updated DESC, id DESC LIMIT ?"
        args.append(int(n))
        with self._lock:
            rows = self._db.execute(q, args).fetchall()
        return [self._item(r) for r in rows]

    def count(self, kind: str | None = None) -> int:
        q, args = "SELECT COUNT(*) FROM memories WHERE owner=?", [self.user_id]
        if kind:
            q += " AND kind=?"
            args.append(kind)
        with self._lock:
            return int(self._db.execute(q, args).fetchone()[0])

    def _features(self, row: sqlite3.Row) -> tuple[Counter, set[str], int]:
        key = (row["id"], row["updated"])
        feat = self._cache.get(key)
        if feat is None:
            toks = tokenize(row["text"])
            feat = (Counter(toks), trigrams(row["text"]), len(toks))
            if len(self._cache) > 50000:
                self._cache.clear()
            self._cache[key] = feat
        return feat

    def search(self, query: str, k: int = 5, kinds: Iterable[str] | None = None,
               min_score: float = 0.12, meta_boost: dict[str, Any] | None = None,
               extra_scorer: Callable[[str, MemoryItem], float] | None = None) -> list[MemoryItem]:
        """Hybrid ranked retrieval. Returns at most k items above min_score.

        meta_boost: e.g. {"family": "word_count"} adds +0.3 to rows whose meta
        matches exactly (used to pull lessons from the same task family).
        """
        kinds = list(kinds) if kinds else list(KINDS)
        placeholders = ",".join("?" * len(kinds))
        with self._lock:
            rows = self._db.execute(
                f"SELECT * FROM memories WHERE owner=? AND archived=0 AND kind IN ({placeholders}) "
                f"ORDER BY updated DESC LIMIT ?", [self.user_id, *kinds, self.MAX_SCAN]).fetchall()
        if not rows:
            return []
        q_tokens = set(tokenize(query))
        q_tri = trigrams(query)
        feats = [self._features(r) for r in rows]
        n_docs = len(rows)
        avgdl = sum(f[2] for f in feats) / n_docs or 1.0
        df: Counter = Counter()
        for tf, _, _ in feats:
            for t in q_tokens:
                if t in tf:
                    df[t] += 1
        k1, b = 1.4, 0.75
        bm25s = []
        for tf, _, dl in feats:
            s = 0.0
            for t in q_tokens:
                f = tf.get(t, 0)
                if f:
                    idf = math.log(1 + (n_docs - df[t] + 0.5) / (df[t] + 0.5))
                    s += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * dl / avgdl))
            bm25s.append(s)
        # Absolute (not max-relative) scale: divide by the best score this query
        # could possibly get, so a weak match stays weak even if it is the best one.
        ceiling = sum(math.log(1 + (n_docs - df[t] + 0.5) / (df[t] + 0.5)) * (k1 + 1) for t in q_tokens) or 1.0
        now = self.clock()
        scored: list[MemoryItem] = []
        for row, (tf, tri, _), bm in zip(rows, feats, bm25s):
            lexical = min(1.0, bm / ceiling)
            coverage = (sum(1 for t in q_tokens if t in tf) / len(q_tokens)) if q_tokens else 0.0
            tri_sim = len(q_tri & tri) / math.sqrt((len(q_tri) or 1) * (len(tri) or 1))  # set cosine
            relevance = 0.4 * lexical + 0.35 * coverage + 0.25 * tri_sim
            item = self._item(row)
            if meta_boost and all(item.meta.get(key) == val for key, val in meta_boost.items()):
                relevance += 0.3
            if extra_scorer is not None:
                try:
                    relevance += float(extra_scorer(query, item))
                except Exception:  # a broken plug-in scorer must not break recall
                    pass
            if relevance < min_score:
                continue
            age_days = max(0.0, (now - row["updated"]) / 86400)
            recency = math.exp(-age_days / 30)
            score = relevance + 0.08 * recency + 0.07 * item.importance
            if item.kind == "reflection":
                score *= 0.5 + item.utility
            item.score = round(score, 4)
            scored.append(item)
        scored.sort(key=lambda it: it.score, reverse=True)
        return scored[:k]

    def close(self) -> None:
        with self._lock:
            self._db.close()
