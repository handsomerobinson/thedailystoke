"""Persistent, per-user memory.

Isolation: every user gets their OWN SQLite file (`users/<sha256(user)[:24]>.sqlite`) and the
owner id is written inside it and verified on every open. There is no API that takes a
user id per call — a MemoryStore is bound to exactly one user at construction — so a bug in
calling code cannot accidentally read another user's rows with a wrong WHERE clause.

What is stored:
  facts      key/value facts about the user ("name: Alice")
  items      episodes, reflections and lessons, full-text indexed (FTS5, porter stemmer)
  notes      versioned notes (old versions kept -> overwrites are reversible)
  inbox      reports from headless jobs ("report back")
  approvals  deferred actions awaiting a human decision
  spend      per-day spend ledger for the daily cost cap
  outbox     messages "sent" by the send_message tool (simulated external channel)

Retrieval score = relevance (BM25) + recency decay + learned utility (helpful/harmful
feedback from the Reflexion loop) + importance, with an exact task-signature boost.
Items that were repeatedly harmful are filtered out ("forgetting").
"""
from __future__ import annotations

import json
import math
import sqlite3
import threading
from dataclasses import dataclass
from pathlib import Path

from .util import Clock, sha256_hex, stem, tokenize, validate_user_id

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT);
CREATE TABLE IF NOT EXISTS facts (key TEXT PRIMARY KEY, value TEXT NOT NULL, source TEXT, updated_at REAL);
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT NOT NULL, text TEXT NOT NULL, tags TEXT DEFAULT '',
    task_sig TEXT DEFAULT '', created_at REAL, last_used REAL, uses INTEGER DEFAULT 0,
    helpful INTEGER DEFAULT 0, harmful INTEGER DEFAULT 0, importance REAL DEFAULT 0.5);
CREATE INDEX IF NOT EXISTS items_kind ON items(kind);
CREATE INDEX IF NOT EXISTS items_sig ON items(task_sig);
CREATE TABLE IF NOT EXISTS notes (title TEXT PRIMARY KEY, body TEXT NOT NULL, version INTEGER, updated_at REAL,
    provenance TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS note_history (title TEXT, body TEXT, version INTEGER, saved_at REAL);
CREATE TABLE IF NOT EXISTS inbox (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at REAL, source TEXT,
    title TEXT, body TEXT, read INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS approvals (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at REAL, tool TEXT,
    args TEXT, digest TEXT, reason TEXT, job_id TEXT, status TEXT DEFAULT 'pending', resolved_at REAL);
CREATE TABLE IF NOT EXISTS spend (day TEXT PRIMARY KEY, usd REAL);
CREATE TABLE IF NOT EXISTS outbox (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at REAL, recipient TEXT, body TEXT);
"""


class MemoryError_(Exception):
    """Base memory error (underscore avoids shadowing the builtin MemoryError)."""


class MemoryIsolationError(MemoryError_):
    pass


class MemoryUnavailable(MemoryError_):
    pass


@dataclass
class MemoryHit:
    id: int
    kind: str
    text: str
    score: float
    task_sig: str = ""
    helpful: int = 0
    harmful: int = 0


def fts5_available() -> bool:
    try:
        c = sqlite3.connect(":memory:")
        c.execute("CREATE VIRTUAL TABLE t USING fts5(x)")
        c.close()
        return True
    except sqlite3.Error:
        return False


def user_db_path(data_dir: Path | str, user_id: str) -> Path:
    return Path(data_dir) / "users" / f"{sha256_hex('mind-user:' + user_id)[:24]}.sqlite"


class MemoryStore:
    def __init__(self, data_dir: Path | str | None, user_id: str, clock: Clock | None = None,
                 use_fts: bool | None = None, in_memory: bool = False):
        self.user_id = validate_user_id(user_id)
        self.clock = clock or Clock()
        self.degraded = in_memory
        self._lock = threading.RLock()
        if in_memory:
            self.path = None
            target = ":memory:"
        else:
            self.path = user_db_path(data_dir, user_id)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            target = str(self.path)
        try:
            self.db = sqlite3.connect(target, timeout=10, check_same_thread=False)
            self.db.row_factory = sqlite3.Row
            if not in_memory:
                self.db.execute("PRAGMA journal_mode=WAL")
            self.db.execute("PRAGMA busy_timeout=5000")
            self.db.executescript(SCHEMA)
            self.use_fts = fts5_available() if use_fts is None else use_fts
            if self.use_fts:
                self.db.execute("CREATE VIRTUAL TABLE IF NOT EXISTS items_fts USING fts5(text, tags, "
                                "tokenize='porter unicode61')")
            self._check_owner()
            self._migrate()
            self.db.commit()
        except MemoryIsolationError:
            raise
        except sqlite3.Error as e:
            raise MemoryUnavailable(f"cannot open memory for {user_id}: {e}") from e

    def _migrate(self):
        cols = {r["name"] for r in self.db.execute("PRAGMA table_info(notes)")}
        if "provenance" not in cols:  # files created by an older build
            self.db.execute("ALTER TABLE notes ADD COLUMN provenance TEXT DEFAULT ''")

    def _check_owner(self):
        row = self.db.execute("SELECT v FROM meta WHERE k='owner'").fetchone()
        if row is None:
            self.db.execute("INSERT INTO meta(k, v) VALUES('owner', ?)", (self.user_id,))
        elif row["v"] != self.user_id:
            raise MemoryIsolationError(f"memory file belongs to {row['v']!r}, not {self.user_id!r}")

    def close(self):
        try:
            self.db.close()
        except Exception:
            pass

    def _x(self, sql, params=()):
        with self._lock:
            cur = self.db.execute(sql, params)
            self.db.commit()
            return cur

    def _q(self, sql, params=()):
        with self._lock:
            return self.db.execute(sql, params).fetchall()

    # ---- facts --------------------------------------------------------------------------
    def set_fact(self, key: str, value: str, source: str = "user") -> None:
        key = key.strip().lower()[:80]
        self._x("INSERT INTO facts(key, value, source, updated_at) VALUES(?,?,?,?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value, source=excluded.source, "
                "updated_at=excluded.updated_at", (key, value[:1000], source, self.clock.now()))

    def get_fact(self, key: str) -> str | None:
        row = self._q("SELECT value FROM facts WHERE key=?", (key.strip().lower(),))
        return row[0]["value"] if row else None

    def facts(self, limit: int = 50) -> dict[str, str]:
        rows = self._q("SELECT key, value FROM facts ORDER BY updated_at DESC LIMIT ?", (limit,))
        return {r["key"]: r["value"] for r in rows}

    def forget_fact(self, key: str) -> bool:
        return self._x("DELETE FROM facts WHERE key=?", (key.strip().lower(),)).rowcount > 0

    # ---- items (episodes / reflections / lessons) ---------------------------------------
    def add_item(self, kind: str, text: str, tags: str = "", task_sig: str = "", importance: float = 0.5) -> int:
        now = self.clock.now()
        with self._lock:
            cur = self.db.execute(
                "INSERT INTO items(kind, text, tags, task_sig, created_at, last_used, importance) "
                "VALUES(?,?,?,?,?,?,?)", (kind, text[:4000], tags, task_sig, now, now, importance))
            iid = cur.lastrowid
            if self.use_fts:
                self.db.execute("INSERT INTO items_fts(rowid, text, tags) VALUES(?,?,?)", (iid, text[:4000], tags))
            self.db.commit()
            return iid

    def get_item(self, item_id: int) -> dict | None:
        rows = self._q("SELECT * FROM items WHERE id=?", (item_id,))
        return dict(rows[0]) if rows else None

    def items(self, kind: str | None = None, task_sig: str | None = None, limit: int = 100) -> list[dict]:
        sql, params = "SELECT * FROM items WHERE 1=1", []
        if kind:
            sql += " AND kind=?"
            params.append(kind)
        if task_sig:
            sql += " AND task_sig=?"
            params.append(task_sig)
        sql += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        return [dict(r) for r in self._q(sql, params)]

    def update_item(self, item_id: int, **fields) -> None:
        allowed = {"kind", "text", "tags", "importance"}
        sets = {k: v for k, v in fields.items() if k in allowed}
        if not sets:
            return
        with self._lock:
            self.db.execute(f"UPDATE items SET {', '.join(k + '=?' for k in sets)} WHERE id=?",
                            (*sets.values(), item_id))
            if self.use_fts and ("text" in sets or "tags" in sets):
                row = self.db.execute("SELECT text, tags FROM items WHERE id=?", (item_id,)).fetchone()
                self.db.execute("DELETE FROM items_fts WHERE rowid=?", (item_id,))
                self.db.execute("INSERT INTO items_fts(rowid, text, tags) VALUES(?,?,?)",
                                (item_id, row["text"], row["tags"]))
            self.db.commit()

    def feedback(self, item_id: int, helpful: bool) -> None:
        col = "helpful" if helpful else "harmful"
        self._x(f"UPDATE items SET {col}={col}+1 WHERE id=?", (item_id,))

    def mark_used(self, ids: list[int]) -> None:
        if ids:
            now = self.clock.now()
            with self._lock:
                self.db.executemany("UPDATE items SET uses=uses+1, last_used=? WHERE id=?", [(now, i) for i in ids])
                self.db.commit()

    def delete_item(self, item_id: int) -> None:
        with self._lock:
            self.db.execute("DELETE FROM items WHERE id=?", (item_id,))
            if self.use_fts:
                self.db.execute("DELETE FROM items_fts WHERE rowid=?", (item_id,))
            self.db.commit()

    # ---- retrieval ----------------------------------------------------------------------
    def search(self, query: str, kinds: list[str] | None = None, k: int = 5,
               task_sig: str | None = None, min_score: float = 0.05) -> list[MemoryHit]:
        toks = tokenize(query)
        rel: dict[int, float] = {}
        if toks:
            rel = self._fts_scores(toks, kinds) if self.use_fts else self._py_bm25(toks, kinds)
        cand_ids = set(rel)
        if task_sig:
            cand_ids |= {r["id"] for r in self._q("SELECT id FROM items WHERE task_sig=?", (task_sig,))}
        if not cand_ids:
            return []
        placeholders = ",".join("?" * len(cand_ids))
        rows = self._q(f"SELECT * FROM items WHERE id IN ({placeholders})", tuple(cand_ids))
        max_rel = max(rel.values()) if rel else 1.0
        now = self.clock.now()
        hits = []
        for r in rows:
            if kinds and r["kind"] not in kinds:
                continue
            h, bad = r["helpful"], r["harmful"]
            if bad >= 2 and bad > 2 * h:
                continue  # repeatedly misleading: forgotten for retrieval purposes
            relevance = rel.get(r["id"], 0.0) / max_rel if max_rel > 0 else 0.0
            age_days = max(0.0, now - max(r["created_at"] or now, r["last_used"] or now)) / 86400
            recency = math.exp(-age_days / 30.0)
            utility = (h - bad) / (h + bad + 2)          # in (-1, 1)
            sig_boost = 0.5 if task_sig and r["task_sig"] == task_sig else 0.0
            score = 0.55 * relevance + 0.10 * recency + 0.20 * utility + 0.10 * (r["importance"] or 0) + sig_boost
            if relevance == 0.0 and not sig_boost:
                continue
            if score >= min_score:
                hits.append(MemoryHit(r["id"], r["kind"], r["text"], round(score, 4), r["task_sig"], h, bad))
        hits.sort(key=lambda x: (-x.score, -x.id))
        return hits[:k]

    def _fts_scores(self, toks: list[str], kinds) -> dict[int, float]:
        q = " OR ".join('"' + t.replace('"', "") + '"' for t in toks[:32])
        kind_sql, params = "", [q]
        if kinds:  # filter inside the query so other kinds cannot crowd the LIMIT
            kind_sql = f" AND items.kind IN ({','.join('?' * len(kinds))})"
            params += list(kinds)
        try:
            rows = self._q("SELECT items_fts.rowid AS rowid, bm25(items_fts) AS s FROM items_fts "
                           "JOIN items ON items.id = items_fts.rowid WHERE items_fts MATCH ?"
                           + kind_sql + " ORDER BY s LIMIT 100", params)
        except sqlite3.Error:
            return self._py_bm25(toks, kinds)
        return {r["rowid"]: -r["s"] for r in rows if -r["s"] > 0}

    def _py_bm25(self, toks: list[str], kinds) -> dict[int, float]:
        """Pure-Python BM25 fallback for SQLite builds without FTS5 (bounded to 2000 recent items)."""
        if kinds:
            rows = self._q(f"SELECT id, text, tags FROM items WHERE kind IN ({','.join('?' * len(kinds))}) "
                           "ORDER BY id DESC LIMIT 2000", tuple(kinds))
        else:
            rows = self._q("SELECT id, text, tags FROM items ORDER BY id DESC LIMIT 2000")
        docs = {r["id"]: [stem(t) for t in tokenize(r["text"] + " " + (r["tags"] or ""))] for r in rows}
        if not docs:
            return {}
        qt = [stem(t) for t in toks]
        n = len(docs)
        avgdl = sum(len(d) for d in docs.values()) / n or 1.0
        df = {t: sum(1 for d in docs.values() if t in d) for t in set(qt)}
        k1, b = 1.5, 0.75
        out = {}
        for did, d in docs.items():
            s = 0.0
            for t in set(qt):
                tf = d.count(t)
                if not tf:
                    continue
                idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
                s += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(d) / avgdl))
            if s > 0:
                out[did] = s
        return out

    # ---- notes (versioned) --------------------------------------------------------------
    def write_note(self, title: str, body: str, provenance: str = "") -> int:
        """`provenance` non-empty = written while untrusted content was in context (tainted)."""
        title = title.strip()[:200]
        now = self.clock.now()
        with self._lock:
            row = self.db.execute("SELECT body, version FROM notes WHERE title=?", (title,)).fetchone()
            version = 1
            if row:
                self.db.execute("INSERT INTO note_history(title, body, version, saved_at) VALUES(?,?,?,?)",
                                (title, row["body"], row["version"], now))
                version = row["version"] + 1
            self.db.execute("INSERT INTO notes(title, body, version, updated_at, provenance) VALUES(?,?,?,?,?) "
                            "ON CONFLICT(title) DO UPDATE SET body=excluded.body, version=excluded.version, "
                            "updated_at=excluded.updated_at, provenance=excluded.provenance",
                            (title, body[:20000], version, now, provenance))
            self.db.commit()
            return version

    def read_note(self, title: str) -> dict | None:
        rows = self._q("SELECT * FROM notes WHERE title=?", (title.strip(),))
        return dict(rows[0]) if rows else None

    def note_history(self, title: str) -> list[dict]:
        return [dict(r) for r in self._q("SELECT * FROM note_history WHERE title=? ORDER BY version", (title.strip(),))]

    def restore_note(self, title: str, version: int) -> bool:
        rows = self._q("SELECT body FROM note_history WHERE title=? AND version=?", (title.strip(), version))
        if not rows:
            return False
        self.write_note(title, rows[0]["body"])
        return True

    def list_notes(self) -> list[dict]:
        return [dict(r) for r in self._q("SELECT title, version, updated_at FROM notes ORDER BY updated_at DESC")]

    def search_notes(self, query: str, k: int = 5) -> list[dict]:
        toks = set(tokenize(query))
        scored = []
        for r in self._q("SELECT title, body FROM notes"):
            words = set(tokenize(r["title"] + " " + r["body"]))
            overlap = len(toks & words)
            if overlap:
                scored.append((overlap, r["title"], r["body"]))
        scored.sort(reverse=True)
        return [{"title": t, "body": b} for _, t, b in scored[:k]]

    def purge_note(self, title: str) -> bool:
        """Irreversible: removes the note AND its history."""
        with self._lock:
            n = self.db.execute("DELETE FROM notes WHERE title=?", (title.strip(),)).rowcount
            self.db.execute("DELETE FROM note_history WHERE title=?", (title.strip(),))
            self.db.commit()
            return n > 0

    # ---- inbox (reports from headless work) ---------------------------------------------
    def add_report(self, source: str, title: str, body: str) -> int:
        return self._x("INSERT INTO inbox(created_at, source, title, body) VALUES(?,?,?,?)",
                       (self.clock.now(), source, title[:200], body[:8000])).lastrowid

    def inbox(self, unread_only: bool = False) -> list[dict]:
        sql = "SELECT * FROM inbox" + (" WHERE read=0" if unread_only else "") + " ORDER BY id"
        return [dict(r) for r in self._q(sql)]

    def mark_read(self, report_id: int | None = None) -> None:
        if report_id is None:
            self._x("UPDATE inbox SET read=1")
        else:
            self._x("UPDATE inbox SET read=1 WHERE id=?", (report_id,))

    # ---- approvals queue ----------------------------------------------------------------
    def add_approval(self, tool: str, args: dict, digest: str, reason: str, job_id: str = "") -> int:
        existing = self._q("SELECT id FROM approvals WHERE digest=? AND status='pending'", (digest,))
        if existing:
            return existing[0]["id"]
        return self._x("INSERT INTO approvals(created_at, tool, args, digest, reason, job_id) VALUES(?,?,?,?,?,?)",
                       (self.clock.now(), tool, json.dumps(args, sort_keys=True), digest, reason, job_id)).lastrowid

    def approvals(self, status: str | None = "pending") -> list[dict]:
        if status:
            rows = self._q("SELECT * FROM approvals WHERE status=? ORDER BY id", (status,))
        else:
            rows = self._q("SELECT * FROM approvals ORDER BY id")
        return [dict(r) for r in rows]

    def resolve_approval(self, approval_id: int, approve: bool) -> bool:
        return self._x("UPDATE approvals SET status=?, resolved_at=? WHERE id=? AND status='pending'",
                       ("approved" if approve else "denied", self.clock.now(), approval_id)).rowcount > 0

    def consume_approval(self, digest: str) -> bool:
        """One-shot: an approved action may be executed exactly once."""
        with self._lock:
            n = self.db.execute("UPDATE approvals SET status='used', resolved_at=? WHERE id = "
                                "(SELECT id FROM approvals WHERE digest=? AND status='approved' LIMIT 1)",
                                (self.clock.now(), digest)).rowcount
            self.db.commit()
            return n > 0

    # ---- spend ledger -------------------------------------------------------------------
    def add_spend(self, day: str, usd: float) -> None:
        self._x("INSERT INTO spend(day, usd) VALUES(?,?) ON CONFLICT(day) DO UPDATE SET usd=usd+excluded.usd",
                (day, usd))

    def spent_on(self, day: str) -> float:
        rows = self._q("SELECT usd FROM spend WHERE day=?", (day,))
        return float(rows[0]["usd"]) if rows else 0.0

    # ---- outbox (simulated external send) -----------------------------------------------
    def record_sent(self, recipient: str, body: str) -> int:
        return self._x("INSERT INTO outbox(created_at, recipient, body) VALUES(?,?,?)",
                       (self.clock.now(), recipient, body[:4000])).lastrowid

    def sent(self) -> list[dict]:
        return [dict(r) for r in self._q("SELECT * FROM outbox ORDER BY id")]

    def compact(self, max_items: int = 5000) -> int:
        """Bound memory growth: drop repeatedly-harmful reflections, then the least useful oldest
        episodes until at most `max_items` items remain. Lessons are never auto-deleted."""
        removed = 0
        with self._lock:
            bad = [r["id"] for r in self.db.execute(
                "SELECT id FROM items WHERE kind IN ('reflection','lesson') AND harmful>=2 AND harmful>2*helpful")]
            count = self.db.execute("SELECT COUNT(*) FROM items").fetchone()[0] - len(bad)
            extra = []
            if count > max_items:
                extra = [r["id"] for r in self.db.execute(
                    "SELECT id FROM items WHERE kind IN ('episode','reflection') AND harmful<=helpful "
                    "ORDER BY uses ASC, last_used ASC LIMIT ?", (count - max_items,))]
            for iid in bad + extra:
                self.db.execute("DELETE FROM items WHERE id=?", (iid,))
                if self.use_fts:
                    self.db.execute("DELETE FROM items_fts WHERE rowid=?", (iid,))
                removed += 1
            self.db.commit()
        return removed

    def export(self) -> dict:
        """Everything stored about this user, as plain data (for inspection / portability)."""
        def rows(sql):
            return [dict(r) for r in self._q(sql)]
        return {"user": self.user_id, "facts": self.facts(limit=10_000),
                "items": rows("SELECT id, kind, text, tags, task_sig, created_at, uses, helpful, harmful FROM items"),
                "notes": rows("SELECT * FROM notes"), "note_history": rows("SELECT * FROM note_history"),
                "inbox": rows("SELECT * FROM inbox"), "approvals": rows("SELECT * FROM approvals"),
                "spend": rows("SELECT * FROM spend"), "outbox": rows("SELECT * FROM outbox")}

    def stats(self) -> dict:
        def n(t):
            return self._q(f"SELECT COUNT(*) AS c FROM {t}")[0]["c"]
        kinds = {r["kind"]: r["c"] for r in self._q("SELECT kind, COUNT(*) AS c FROM items GROUP BY kind")}
        return {"facts": n("facts"), "notes": n("notes"), "inbox": n("inbox"), "items": kinds,
                "pending_approvals": len(self.approvals("pending")), "fts5": self.use_fts,
                "degraded": self.degraded}
