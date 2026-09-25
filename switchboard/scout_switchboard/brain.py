"""The socket the brain plugs into.

The switchboard owns phone numbers, identity, permissions and delivery. The brain
owns thinking. Between them is one call:

    reply = brain.think(turn, tools)

`turn` says who is talking, in which world, and what they said. It carries names,
never phone numbers. `tools` is how the brain acts on the world (text someone,
text a group, remember something); every action is permission-checked by the
switchboard, so a brain can be swapped or can misbehave without widening access.

Any object with that `think` method is a brain. Point SCOUT_BRAIN at a factory
("package.module:callable") and the switchboard loads it at start-up.
"""
import importlib
import re
from dataclasses import dataclass, field
from typing import Any, Optional, Protocol


@dataclass(frozen=True)
class Contact:
    name: str
    role: str
    can_text: bool          # whether the speaker may reach this person through the brain


@dataclass(frozen=True)
class Turn:
    tenant: str             # slug, e.g. "chester"
    tenant_name: str        # e.g. "Chester Elton"
    persona: str            # the resident's name on this line, e.g. "Scout"
    session_id: str         # stable per tenant + person; key the brain's memory on this
    speaker: str            # name of the person texting
    speaker_role: str       # admin | owner | member | guest
    text: str
    media_urls: list[str] = field(default_factory=list)
    contacts: list[Contact] = field(default_factory=list)
    groups: list[str] = field(default_factory=list)
    relationships: list[tuple[str, str, str]] = field(default_factory=list)   # (a, label, b)
    notes: list[dict] = field(default_factory=list)                            # {body, about, created_at}
    history: list[dict] = field(default_factory=list)                          # {direction, body, via, created_at}


class Tools(Protocol):
    """What the switchboard lets the brain do this turn. Each returns a short result string."""

    def send_text(self, to: str, message: str, media_urls: Optional[list[str]] = None) -> str: ...
    def message_group(self, group: str, message: str) -> str: ...
    def remember(self, note: str, about: Optional[str] = None) -> str: ...
    def specs(self) -> list[dict]: ...
    def call(self, name: str, args: dict[str, Any]) -> str: ...


class Brain(Protocol):
    def think(self, turn: Turn, tools: Tools) -> Optional[str]:
        """Return the reply to text back to the speaker, or None/"" to stay silent."""


def load_brain(path: str) -> Brain:
    module_name, _, attr = path.partition(":")
    factory = getattr(importlib.import_module(module_name), attr or "make_brain")
    return factory() if callable(factory) else factory


class SimpleBrainAdapter:
    """Wrap a brain that only speaks `think(user_id, message) -> str` (the shape in the Muse spec)."""

    def __init__(self, think_fn):
        self.think_fn = think_fn

    def think(self, turn: Turn, tools: Tools) -> Optional[str]:
        return self.think_fn(turn.session_id, turn.text)


class DevBrain:
    """No AI. Exercises the plumbing so the router can be tested end to end for free.

    "tell Christy we're on at 3"      -> texts Christy
    "text the team: lunch at noon"    -> texts the group called "team"
    "remember Adam prefers mornings"  -> stores a note
    anything else                     -> echoes, with who you are and who you can reach
    """

    TELL = re.compile(r"^(?:tell|text|let)\s+(.+?)\s+(?:know\s+)?(?:that\s+)?(.+)$", re.I | re.S)
    GROUP = re.compile(r"^(?:text|tell)\s+(?:the\s+)?(.+?)\s*(?:group)?\s*:\s*(.+)$", re.I | re.S)
    REMEMBER = re.compile(r"^remember\s+(.+)$", re.I | re.S)

    def think(self, turn: Turn, tools: Tools) -> Optional[str]:
        text = turn.text.strip()
        if m := self.GROUP.match(text):
            if m.group(1).lower() in {g.lower() for g in turn.groups}:
                return tools.message_group(m.group(1), f"{turn.speaker}: {m.group(2)}")
        if m := self.TELL.match(text):
            return tools.send_text(m.group(1), f"{turn.speaker} says: {m.group(2)}")
        if m := self.REMEMBER.match(text):
            return tools.remember(m.group(1))
        reachable = ", ".join(c.name for c in turn.contacts if c.can_text) or "nobody yet"
        return f"[{turn.persona} dev brain] Hi {turn.speaker} ({turn.speaker_role}). You said: {text!r}. You can reach: {reachable}."
