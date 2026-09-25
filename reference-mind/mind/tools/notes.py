"""Per-user note storage (plain files under data/users/<user>/notes).

note_write keeps the previous version under notes/.versions, which is why it
is only WRITE (reversible); note_delete removes the note *and* its history,
so it is IRREVERSIBLE and needs typed confirmation.
"""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

from ..memory import tokenize
from ..permissions import Tier
from ..util import safe_name
from .base import Tool, ToolContext

MAX_NOTE = 100_000


def notes_dir(ctx: ToolContext) -> Path:
    d = ctx.settings.user_dir(ctx.user_id) / "notes"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _path(ctx: ToolContext, name: str) -> Path:
    name = safe_name(name)
    if not name.endswith((".md", ".txt")):
        name += ".md"
    p = (notes_dir(ctx) / name).resolve()
    if p.parent != notes_dir(ctx).resolve():
        raise PermissionError("note path escapes the notes directory")
    return p


def note_write(args: dict[str, Any], ctx: ToolContext) -> str:
    content = args["content"]
    if len(content) > MAX_NOTE:
        raise ValueError(f"note too large ({len(content)} > {MAX_NOTE} chars)")
    p = _path(ctx, args["name"])
    if p.exists():
        vdir = p.parent / ".versions"
        vdir.mkdir(exist_ok=True)
        (vdir / f"{p.stem}.{int(time.time() * 1000)}{p.suffix}").write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, p)  # atomic
    return f"saved note {p.stem!r} ({len(content)} chars)"


def note_read(args: dict[str, Any], ctx: ToolContext) -> str:
    p = _path(ctx, args["name"])
    if not p.exists():
        existing = ", ".join(sorted(x.stem for x in notes_dir(ctx).glob("*.md"))) or "(none)"
        raise FileNotFoundError(f"no note named {args['name']!r}; existing notes: {existing}")
    return p.read_text(encoding="utf-8")


def note_list(args: dict[str, Any], ctx: ToolContext) -> str:
    items = sorted(notes_dir(ctx).glob("*.md")) + sorted(notes_dir(ctx).glob("*.txt"))
    if not items:
        return "(no notes)"
    return "\n".join(f"{p.stem} ({p.stat().st_size} bytes)" for p in items)


def note_search(args: dict[str, Any], ctx: ToolContext) -> str:
    q = set(tokenize(args["query"]))
    hits = []
    for p in notes_dir(ctx).glob("*.md"):
        text = p.read_text(encoding="utf-8", errors="replace")
        overlap = len(q & set(tokenize(text)))
        if overlap:
            hits.append((overlap, p.stem, text[:120].replace("\n", " ")))
    hits.sort(reverse=True)
    return "\n".join(f"{name}: {snippet}" for _, name, snippet in hits[:10]) or "(no matching notes)"


def note_delete(args: dict[str, Any], ctx: ToolContext) -> str:
    p = _path(ctx, args["name"])
    if not p.exists():
        raise FileNotFoundError(f"no note named {args['name']!r}")
    p.unlink()
    vdir = p.parent / ".versions"
    removed = 0
    if vdir.exists():
        for v in vdir.glob(f"{p.stem}.*"):
            v.unlink()
            removed += 1
    return f"deleted note {p.stem!r} and {removed} old version(s)"


def note_tools() -> list[Tool]:
    name_param = {"name": {"type": "string", "description": "note name (letters, digits, _ - .)"}}
    return [
        Tool("note_write", "Create or overwrite a note (previous version is kept).",
             {"type": "object", "properties": {**name_param, "content": {"type": "string"}}, "required": ["name", "content"]},
             Tier.WRITE, note_write, target=lambda a: a.get("name", "")),
        Tool("note_read", "Read a note by name.",
             {"type": "object", "properties": name_param, "required": ["name"]}, Tier.READ, note_read,
             # MC15: notes created from inbox files usually hold other people's words (letters, emails)
             third_party=lambda a: str(a.get("name", "")).startswith("inbox-")),
        Tool("note_list", "List the user's notes.", {"type": "object", "properties": {}}, Tier.READ, note_list),
        Tool("note_search", "Keyword search over the user's notes.",
             {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}, Tier.READ, note_search),
        Tool("note_delete", "Permanently delete a note and its history.",
             {"type": "object", "properties": name_param, "required": ["name"]},
             Tier.IRREVERSIBLE, note_delete, target=lambda a: a.get("name", "")),
    ]
