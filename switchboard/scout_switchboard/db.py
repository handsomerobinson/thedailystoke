"""SQLite store: tenants, lines, people, how they connect, and every message.

The phone number is the identity key. A person exists once globally (one row in
`people`) and joins any number of tenants through `memberships`. Everything the
brain can see or touch is filtered through a single tenant, so Chester's world
and TENFOUR's world never leak into each other even when one person is in both.
"""
import json
import sqlite3
import threading
from dataclasses import dataclass
from typing import Iterable, Optional

SCHEMA = """
CREATE TABLE IF NOT EXISTS tenants (
    id         INTEGER PRIMARY KEY,
    slug       TEXT NOT NULL UNIQUE,
    name       TEXT NOT NULL,
    persona    TEXT NOT NULL DEFAULT 'Scout',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
-- Each phone number we own belongs to exactly one tenant. The inbound `to`
-- number is how the switchboard knows which world a text belongs to.
CREATE TABLE IF NOT EXISTS lines (
    number    TEXT PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id),
    channel   TEXT NOT NULL DEFAULT 'sms',
    label     TEXT
);
CREATE TABLE IF NOT EXISTS people (
    id         INTEGER PRIMARY KEY,
    phone      TEXT NOT NULL UNIQUE,
    name       TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS memberships (
    tenant_id INTEGER NOT NULL REFERENCES tenants(id),
    person_id INTEGER NOT NULL REFERENCES people(id),
    role      TEXT NOT NULL CHECK (role IN ('admin', 'owner', 'member', 'guest')),
    status    TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'pending', 'blocked')),
    alias     TEXT,
    PRIMARY KEY (tenant_id, person_id)
);
-- Who may text whom through the brain. Admins may reach anyone in their tenant
-- without an edge; everyone else needs one.
CREATE TABLE IF NOT EXISTS reach (
    tenant_id   INTEGER NOT NULL,
    from_person INTEGER NOT NULL,
    to_person   INTEGER NOT NULL,
    PRIMARY KEY (tenant_id, from_person, to_person)
);
-- How people are connected, in words the brain can read ("assistant to").
CREATE TABLE IF NOT EXISTS relationships (
    tenant_id INTEGER NOT NULL,
    person_a  INTEGER NOT NULL,
    person_b  INTEGER NOT NULL,
    label     TEXT NOT NULL,
    PRIMARY KEY (tenant_id, person_a, person_b, label)
);
CREATE TABLE IF NOT EXISTS groups (
    id        INTEGER PRIMARY KEY,
    tenant_id INTEGER NOT NULL,
    name      TEXT NOT NULL,
    UNIQUE (tenant_id, name)
);
CREATE TABLE IF NOT EXISTS group_members (
    group_id  INTEGER NOT NULL REFERENCES groups(id),
    person_id INTEGER NOT NULL REFERENCES people(id),
    PRIMARY KEY (group_id, person_id)
);
-- Every text in and out: conversation history for the brain and the action
-- record for humans. `via` says why an outbound text was sent.
CREATE TABLE IF NOT EXISTS messages (
    id             INTEGER PRIMARY KEY,
    tenant_id      INTEGER,
    person_id      INTEGER,
    line_number    TEXT NOT NULL,
    peer_number    TEXT NOT NULL,
    direction      TEXT NOT NULL CHECK (direction IN ('in', 'out')),
    body           TEXT NOT NULL,
    media          TEXT NOT NULL DEFAULT '[]',
    via            TEXT,
    on_behalf_of   INTEGER,
    carrier_msg_id TEXT,
    status         TEXT,
    created_at     TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS messages_by_person ON messages (tenant_id, person_id, id);
CREATE INDEX IF NOT EXISTS messages_by_peer ON messages (line_number, peer_number, id);
-- Carrier webhooks are retried; an event id is processed once.
CREATE TABLE IF NOT EXISTS events_seen (
    event_id TEXT PRIMARY KEY,
    seen_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
-- Durable things the brain chose to remember, scoped to a tenant and
-- optionally to one person in it.
CREATE TABLE IF NOT EXISTS notes (
    id         INTEGER PRIMARY KEY,
    tenant_id  INTEGER NOT NULL,
    person_id  INTEGER,
    author_id  INTEGER,
    body       TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
-- STOP is per sending number, as carriers enforce it.
CREATE TABLE IF NOT EXISTS opt_outs (
    line_number TEXT NOT NULL,
    phone       TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (line_number, phone)
);
"""


@dataclass(frozen=True)
class Tenant:
    id: int
    slug: str
    name: str
    persona: str


@dataclass(frozen=True)
class Member:
    """A person as seen from inside one tenant."""
    person_id: int
    tenant_id: int
    phone: str
    name: str
    role: str
    status: str

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"


class Store:
    def __init__(self, path: str):
        self._conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.execute("PRAGMA journal_mode = WAL")
        self._lock = threading.RLock()
        with self._lock:
            self._conn.executescript(SCHEMA)

    def _q(self, sql: str, args: Iterable = ()) -> list[sqlite3.Row]:
        with self._lock:
            return self._conn.execute(sql, tuple(args)).fetchall()

    def _x(self, sql: str, args: Iterable = ()) -> int:
        with self._lock:
            return self._conn.execute(sql, tuple(args)).lastrowid

    # --- setup ---------------------------------------------------------------

    def upsert_tenant(self, slug: str, name: str, persona: str = "Scout") -> Tenant:
        self._x(
            "INSERT INTO tenants (slug, name, persona) VALUES (?, ?, ?) "
            "ON CONFLICT(slug) DO UPDATE SET name = excluded.name, persona = excluded.persona",
            (slug, name, persona),
        )
        return self.tenant_by_slug(slug)

    def add_line(self, number: str, tenant: Tenant, channel: str = "sms", label: str = "") -> None:
        self._x(
            "INSERT INTO lines (number, tenant_id, channel, label) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(number) DO UPDATE SET tenant_id = excluded.tenant_id, "
            "channel = excluded.channel, label = excluded.label",
            (number, tenant.id, channel, label),
        )

    def upsert_person(self, phone: str, name: str) -> int:
        self._x(
            "INSERT INTO people (phone, name) VALUES (?, ?) "
            "ON CONFLICT(phone) DO UPDATE SET name = excluded.name",
            (phone, name),
        )
        return self._q("SELECT id FROM people WHERE phone = ?", (phone,))[0]["id"]

    def add_member(self, tenant: Tenant, person_id: int, role: str,
                   status: str = "active", alias: Optional[str] = None) -> None:
        self._x(
            "INSERT INTO memberships (tenant_id, person_id, role, status, alias) VALUES (?, ?, ?, ?, ?) "
            "ON CONFLICT(tenant_id, person_id) DO UPDATE SET role = excluded.role, "
            "status = excluded.status, alias = COALESCE(excluded.alias, memberships.alias)",
            (tenant.id, person_id, role, status, alias),
        )

    def allow(self, tenant: Tenant, from_person: int, to_person: int, both_ways: bool = True) -> None:
        pairs = [(from_person, to_person)] + ([(to_person, from_person)] if both_ways else [])
        for a, b in pairs:
            self._x("INSERT OR IGNORE INTO reach VALUES (?, ?, ?)", (tenant.id, a, b))

    def relate(self, tenant: Tenant, person_a: int, person_b: int, label: str) -> None:
        self._x("INSERT OR IGNORE INTO relationships VALUES (?, ?, ?, ?)",
                (tenant.id, person_a, person_b, label))

    def add_group(self, tenant: Tenant, name: str, person_ids: Iterable[int]) -> int:
        self._x("INSERT OR IGNORE INTO groups (tenant_id, name) VALUES (?, ?)", (tenant.id, name))
        gid = self._q("SELECT id FROM groups WHERE tenant_id = ? AND name = ?", (tenant.id, name))[0]["id"]
        for pid in person_ids:
            self._x("INSERT OR IGNORE INTO group_members VALUES (?, ?)", (gid, pid))
        return gid

    # --- lookups -------------------------------------------------------------

    def tenant_by_slug(self, slug: str) -> Optional[Tenant]:
        rows = self._q("SELECT id, slug, name, persona FROM tenants WHERE slug = ?", (slug,))
        return Tenant(**dict(rows[0])) if rows else None

    def tenant_for_line(self, number: str) -> Optional[Tenant]:
        rows = self._q(
            "SELECT t.id, t.slug, t.name, t.persona FROM lines l JOIN tenants t ON t.id = l.tenant_id "
            "WHERE l.number = ?", (number,))
        return Tenant(**dict(rows[0])) if rows else None

    def line_for_tenant(self, tenant: Tenant) -> Optional[str]:
        rows = self._q("SELECT number FROM lines WHERE tenant_id = ? ORDER BY rowid LIMIT 1", (tenant.id,))
        return rows[0]["number"] if rows else None

    def is_our_line(self, number: str) -> bool:
        return bool(self._q("SELECT 1 FROM lines WHERE number = ?", (number,)))

    _MEMBER_SQL = (
        "SELECT p.id AS person_id, m.tenant_id, p.phone, COALESCE(m.alias, p.name) AS name, m.role, m.status "
        "FROM memberships m JOIN people p ON p.id = m.person_id WHERE m.tenant_id = ?"
    )

    def member_by_phone(self, tenant: Tenant, phone: str) -> Optional[Member]:
        rows = self._q(self._MEMBER_SQL + " AND p.phone = ?", (tenant.id, phone))
        return Member(**dict(rows[0])) if rows else None

    def member_by_id(self, tenant: Tenant, person_id: int) -> Optional[Member]:
        rows = self._q(self._MEMBER_SQL + " AND p.id = ?", (tenant.id, person_id))
        return Member(**dict(rows[0])) if rows else None

    def members(self, tenant: Tenant, status: str = "active") -> list[Member]:
        rows = self._q(self._MEMBER_SQL + " AND m.status = ? ORDER BY name", (tenant.id, status))
        return [Member(**dict(r)) for r in rows]

    def find_member(self, tenant: Tenant, name: str) -> list[Member]:
        """Resolve a name the brain used. Exact full name wins; else unique first-name match."""
        wanted = name.strip().lower()
        everyone = self.members(tenant)
        exact = [m for m in everyone if m.name.lower() == wanted]
        if exact:
            return exact
        return [m for m in everyone if m.name.lower().split()[0] == wanted.split()[0]] if wanted else []

    def can_reach(self, tenant: Tenant, sender: Member, recipient: Member) -> bool:
        if sender.status != "active" or recipient.status != "active":
            return False
        if sender.is_admin:
            return True
        return bool(self._q("SELECT 1 FROM reach WHERE tenant_id = ? AND from_person = ? AND to_person = ?",
                            (tenant.id, sender.person_id, recipient.person_id)))

    def reachable(self, tenant: Tenant, sender: Member) -> list[Member]:
        return [m for m in self.members(tenant)
                if m.person_id != sender.person_id and self.can_reach(tenant, sender, m)]

    def relationships(self, tenant: Tenant) -> list[tuple[str, str, str]]:
        rows = self._q(
            "SELECT COALESCE(ma.alias, pa.name) AS a, r.label, COALESCE(mb.alias, pb.name) AS b "
            "FROM relationships r "
            "JOIN people pa ON pa.id = r.person_a JOIN people pb ON pb.id = r.person_b "
            "JOIN memberships ma ON ma.person_id = r.person_a AND ma.tenant_id = r.tenant_id "
            "JOIN memberships mb ON mb.person_id = r.person_b AND mb.tenant_id = r.tenant_id "
            "WHERE r.tenant_id = ?", (tenant.id,))
        return [(r["a"], r["label"], r["b"]) for r in rows]

    def groups_for(self, tenant: Tenant, member: Member) -> list[str]:
        if member.is_admin:
            rows = self._q("SELECT name FROM groups WHERE tenant_id = ? ORDER BY name", (tenant.id,))
        else:
            rows = self._q(
                "SELECT g.name FROM groups g JOIN group_members gm ON gm.group_id = g.id "
                "WHERE g.tenant_id = ? AND gm.person_id = ? ORDER BY g.name", (tenant.id, member.person_id))
        return [r["name"] for r in rows]

    def group_members(self, tenant: Tenant, group: str) -> list[Member]:
        rows = self._q(
            "SELECT gm.person_id FROM groups g JOIN group_members gm ON gm.group_id = g.id "
            "WHERE g.tenant_id = ? AND lower(g.name) = lower(?)", (tenant.id, group))
        found = (self.member_by_id(tenant, r["person_id"]) for r in rows)
        return [m for m in found if m and m.status == "active"]

    def admins(self, tenant: Tenant) -> list[Member]:
        return [m for m in self.members(tenant) if m.is_admin]

    # --- messages ------------------------------------------------------------

    def log_message(self, *, tenant: Optional[Tenant], person_id: Optional[int], line_number: str,
                    peer_number: str, direction: str, body: str, media: list[str] | None = None,
                    via: Optional[str] = None, on_behalf_of: Optional[int] = None,
                    carrier_msg_id: Optional[str] = None, status: Optional[str] = None) -> int:
        return self._x(
            "INSERT INTO messages (tenant_id, person_id, line_number, peer_number, direction, body, media, "
            "via, on_behalf_of, carrier_msg_id, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (tenant.id if tenant else None, person_id, line_number, peer_number, direction, body,
             json.dumps(media or []), via, on_behalf_of, carrier_msg_id, status),
        )

    def set_message_status(self, carrier_msg_id: str, status: str) -> None:
        self._x("UPDATE messages SET status = ? WHERE carrier_msg_id = ?", (status, carrier_msg_id))

    def history(self, tenant: Tenant, person_id: int, limit: int) -> list[dict]:
        rows = self._q(
            "SELECT direction, body, media, via, created_at FROM messages "
            "WHERE tenant_id = ? AND person_id = ? ORDER BY id DESC LIMIT ?", (tenant.id, person_id, limit))
        return [dict(r) | {"media": json.loads(r["media"])} for r in reversed(rows)]

    def has_texted_peer(self, line_number: str, peer_number: str) -> bool:
        return bool(self._q("SELECT 1 FROM messages WHERE line_number = ? AND peer_number = ? AND direction = 'out'",
                            (line_number, peer_number)))

    def messages(self, tenant: Tenant, limit: int = 100) -> list[dict]:
        rows = self._q("SELECT * FROM messages WHERE tenant_id = ? ORDER BY id DESC LIMIT ?", (tenant.id, limit))
        return [dict(r) for r in rows]

    def unknown_inbound(self, line_number: str) -> list[dict]:
        rows = self._q("SELECT peer_number, body, created_at FROM messages WHERE line_number = ? "
                       "AND person_id IS NULL AND direction = 'in' ORDER BY id DESC", (line_number,))
        return [dict(r) for r in rows]

    # --- notes -------------------------------------------------------------

    def add_note(self, tenant: Tenant, body: str, person_id: Optional[int], author_id: Optional[int]) -> None:
        self._x("INSERT INTO notes (tenant_id, person_id, author_id, body) VALUES (?, ?, ?, ?)",
                (tenant.id, person_id, author_id, body))

    def notes(self, tenant: Tenant, limit: int = 50) -> list[dict]:
        rows = self._q(
            "SELECT n.body, n.created_at, COALESCE(m.alias, p.name) AS about FROM notes n "
            "LEFT JOIN people p ON p.id = n.person_id "
            "LEFT JOIN memberships m ON m.person_id = n.person_id AND m.tenant_id = n.tenant_id "
            "WHERE n.tenant_id = ? ORDER BY n.id DESC LIMIT ?", (tenant.id, limit))
        return [dict(r) for r in reversed(rows)]

    # --- delivery hygiene ----------------------------------------------------

    def first_time_seen(self, event_id: str) -> bool:
        with self._lock:
            cur = self._conn.execute("INSERT OR IGNORE INTO events_seen (event_id) VALUES (?)", (event_id,))
            return cur.rowcount == 1

    def opt_out(self, line_number: str, phone: str) -> None:
        self._x("INSERT OR IGNORE INTO opt_outs (line_number, phone) VALUES (?, ?)", (line_number, phone))

    def opt_in(self, line_number: str, phone: str) -> None:
        self._x("DELETE FROM opt_outs WHERE line_number = ? AND phone = ?", (line_number, phone))

    def is_opted_out(self, line_number: str, phone: str) -> bool:
        return bool(self._q("SELECT 1 FROM opt_outs WHERE line_number = ? AND phone = ?", (line_number, phone)))
