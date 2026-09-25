"""Small shared helpers: clock, ids, redaction, truncation, tokenising."""
from __future__ import annotations

import hashlib
import json
import re
import time
import uuid
from typing import Any, Iterable


class Clock:
    """Wall clock. Injected everywhere so tests and the scheduler can fake time."""

    def now(self) -> float:
        return time.time()

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)


class FakeClock(Clock):
    """Deterministic clock for tests: sleep() advances time instantly."""

    def __init__(self, start: float = 1_800_000_000.0):
        self.t = float(start)
        self.slept: list[float] = []

    def now(self) -> float:
        return self.t

    def sleep(self, seconds: float) -> None:
        self.slept.append(seconds)
        self.t += seconds

    def advance(self, seconds: float) -> None:
        self.t += seconds


def new_id(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:12]}"


def sha256_hex(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


_SECRET_PATTERNS = [
    re.compile(r"sk-ant-[A-Za-z0-9_\-]{8,}"),
    re.compile(r"sk-[A-Za-z0-9_\-]{16,}"),
    re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._\-]{12,}"),
    re.compile(r"(?i)((?:api[_-]?key|token|secret|password)\s*[=:]\s*)['\"]?[^\s'\"]{6,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]


def redact(text: str) -> str:
    """Mask things that look like credentials before they reach logs or memory."""
    if not isinstance(text, str):
        text = str(text)
    for pat in _SECRET_PATTERNS:
        if pat.groups:
            text = pat.sub(lambda m: m.group(1) + "[REDACTED]", text)
        else:
            text = pat.sub("[REDACTED]", text)
    return text


def redact_obj(obj: Any) -> Any:
    if isinstance(obj, str):
        return redact(obj)
    if isinstance(obj, dict):
        return {k: ("[REDACTED]" if re.search(r"(?i)key|token|secret|password", str(k)) else redact_obj(v))
                for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [redact_obj(v) for v in obj]
    return obj


def truncate(text: str, limit: int, marker: str = "…[truncated {n} chars]") -> str:
    if text is None:
        return ""
    if len(text) <= limit:
        return text
    cut = len(text) - limit
    return text[:limit] + marker.format(n=cut)


STOPWORDS = frozenset(
    """a an the and or but if then else of to in on at by for with from into over under is are was were be
    been being it its this that these those i me my you your we our they them their he she his her as do does
    did done can could should would will shall may might must not no yes so such than too very just also
    what which who whom whose when where why how all any each few more most other some own same only
    please write make function python return returns given""".split()
)

_WORD = re.compile(r"[A-Za-z0-9_]+")


def stem(word: str) -> str:
    """Tiny suffix stripper (fallback path only; FTS5 uses the porter stemmer)."""
    for suf in ("ingly", "edly", "ing", "ies", "ied", "ers", "es", "ed", "er", "ly", "s"):
        if len(word) > len(suf) + 2 and word.endswith(suf):
            return word[: -len(suf)] + ("y" if suf in ("ies", "ied") else "")
    return word


def tokenize(text: str, keep_stopwords: bool = False) -> list[str]:
    toks = []
    for w in _WORD.findall(text.lower()):
        # split snake_case identifiers too: is_palindrome -> is_palindrome, palindrome
        parts = [w] + ([p for p in w.split("_") if p] if "_" in w else [])
        for p in parts:
            if keep_stopwords or p not in STOPWORDS:
                toks.append(p)
    return toks


def uniq(seq: Iterable[Any]) -> list[Any]:
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def estimate_tokens(text: str) -> int:
    """Assumes ~3 chars/token (real English is ~4), i.e. deliberately over-estimates so the
    pre-flight cost check errs on the side of refusing. Not a real tokenizer."""
    if not text:
        return 0
    return len(text) // 3 + 1


VALID_USER = re.compile(r"^[A-Za-z0-9_.@\-]{1,64}$")


def validate_user_id(user_id: str) -> str:
    if not isinstance(user_id, str) or not VALID_USER.match(user_id):
        raise ValueError(f"invalid user id {user_id!r}: use 1-64 chars of [A-Za-z0-9_.@-]")
    return user_id
