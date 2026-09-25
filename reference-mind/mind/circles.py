"""Circles: a recurring group, its gatherings and RSVPs (the Porchlight data model the red team attacked).

Everything in here except the circle's name is OTHER PEOPLE'S content (P6 data):
  * MC13: the guide reads a circle only if every current member opted in; a new member starts opted-out, so adding
    someone re-prompts.  Facts derived from a circle are never persisted (the remember tool refuses in such a task).
  * MC15: circle content is `third_party`; it is never sent to an off-device model (see agent.py).
  * MC21: reads are one circle at a time, current gathering only; there is no query that returns per-person history
    across gatherings or circles, so "rank my friends by responsiveness" has no data path.
"""
from __future__ import annotations

import sqlite3
import threading
import time
from dataclasses import dataclass
from pathlib import Path

from .purpose import POLICY_VERSION
from .util import safe_user_id


class CircleError(ValueError):
    pass


class CircleConsentError(CircleError):
    pass


@dataclass
class CircleView:
    circle_id: int
    name: str
    gathering: dict | None
    rsvps: list[dict]


class CircleStore:
    SCHEMA = f"""
    CREATE TABLE IF NOT EXISTS circles (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, created REAL NOT NULL,
        purpose TEXT NOT NULL DEFAULT '["gatherings"]', source TEXT NOT NULL DEFAULT 'user',
        policy_version TEXT NOT NULL DEFAULT '{POLICY_VERSION}');
    CREATE TABLE IF NOT EXISTS members (circle_id INTEGER NOT NULL, person TEXT NOT NULL, opted_in INTEGER NOT NULL DEFAULT 0,
        added REAL NOT NULL, PRIMARY KEY (circle_id, person));
    CREATE TABLE IF NOT EXISTS gatherings (id INTEGER PRIMARY KEY AUTOINCREMENT, circle_id INTEGER NOT NULL, title TEXT NOT NULL,
        when_text TEXT NOT NULL, place TEXT NOT NULL DEFAULT '', status TEXT NOT NULL DEFAULT 'upcoming', created REAL NOT NULL);
    CREATE TABLE IF NOT EXISTS rsvps (gathering_id INTEGER NOT NULL, person TEXT NOT NULL, answer TEXT NOT NULL,
        note TEXT NOT NULL DEFAULT '', updated REAL NOT NULL,
        purpose TEXT NOT NULL DEFAULT '["gatherings"]', source TEXT NOT NULL DEFAULT 'other_user',
        policy_version TEXT NOT NULL DEFAULT '{POLICY_VERSION}', PRIMARY KEY (gathering_id, person));
    """

    def __init__(self, data_dir: Path, user_id: str):
        self.user_id = safe_user_id(user_id)
        d = Path(data_dir) / "users" / self.user_id
        d.mkdir(parents=True, exist_ok=True)
        self.path = d / "circles.db"
        self._lock = threading.RLock()
        self._db = sqlite3.connect(str(self.path), timeout=10, check_same_thread=False)
        self._db.row_factory = sqlite3.Row
        self._db.executescript(self.SCHEMA)

    def create_circle(self, name: str, members: list[str]) -> int:
        with self._lock, self._db:
            cid = int(self._db.execute("INSERT INTO circles(name, created) VALUES (?,?)", (name[:80], time.time())).lastrowid)
        for m in members:
            self.add_member(cid, m)
        return cid

    def add_member(self, cid: int, person: str) -> None:
        with self._lock, self._db:  # new members start NOT opted in (MC13 re-prompt)
            self._db.execute("INSERT OR IGNORE INTO members(circle_id, person, opted_in, added) VALUES (?,?,0,?)",
                             (int(cid), person[:60], time.time()))

    def opt_in(self, cid: int, person: str, value: bool = True) -> None:
        with self._lock, self._db:
            if self._db.execute("UPDATE members SET opted_in=? WHERE circle_id=? AND person=?",
                                (int(value), int(cid), person)).rowcount != 1:
                raise CircleError(f"{person!r} is not a member of circle {cid}")

    def members(self, cid: int) -> list[dict]:
        with self._lock:
            return [dict(r) for r in self._db.execute("SELECT person, opted_in FROM members WHERE circle_id=? ORDER BY added, person", (int(cid),))]

    def consent_gaps(self, cid: int) -> list[str]:
        return [m["person"] for m in self.members(cid) if not m["opted_in"]]

    def add_gathering(self, cid: int, title: str, when: str, place: str = "") -> int:
        with self._lock, self._db:
            self._db.execute("UPDATE gatherings SET status='past' WHERE circle_id=? AND status='upcoming'", (int(cid),))
            return int(self._db.execute("INSERT INTO gatherings(circle_id, title, when_text, place, created) VALUES (?,?,?,?,?)",
                                        (int(cid), title[:120], when[:80], place[:120], time.time())).lastrowid)

    def rsvp(self, gid: int, person: str, answer: str, note: str = "") -> None:
        with self._lock, self._db:
            self._db.execute("INSERT OR REPLACE INTO rsvps(gathering_id, person, answer, note, updated) VALUES (?,?,?,?,?)",
                             (int(gid), person[:60], answer[:20], note[:1000], time.time()))

    def gathering(self, gid: int) -> dict | None:
        with self._lock:
            r = self._db.execute("SELECT * FROM gatherings WHERE id=?", (int(gid),)).fetchone()
        return dict(r) if r else None

    def list_circles(self) -> list[dict]:
        with self._lock:
            return [dict(r) for r in self._db.execute("SELECT id, name FROM circles ORDER BY id")]

    def read_current(self, cid: int) -> CircleView:
        """One circle, its upcoming gathering, that gathering's RSVPs.  Nothing else exists as a query (MC21)."""
        with self._lock:
            c = self._db.execute("SELECT * FROM circles WHERE id=?", (int(cid),)).fetchone()
            if c is None:
                raise CircleError(f"no circle {cid}")
            gaps = self.consent_gaps(cid)
            if gaps:
                raise CircleConsentError(f"not every member has opted in to the guide reading this circle "
                                         f"({', '.join(gaps)}); ask them first (MC13)")
            g = self._db.execute("SELECT * FROM gatherings WHERE circle_id=? AND status='upcoming' ORDER BY id DESC LIMIT 1",
                                 (int(cid),)).fetchone()
            rs = [] if g is None else [dict(r) for r in self._db.execute(
                "SELECT person, answer, note FROM rsvps WHERE gathering_id=? ORDER BY person", (g["id"],))]
        return CircleView(int(cid), c["name"], dict(g) if g else None, rs)

    def close(self) -> None:
        with self._lock:
            self._db.close()
