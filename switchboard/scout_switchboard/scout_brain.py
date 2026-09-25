"""Starter Scout brain: Claude with the switchboard's tools.

A placeholder until Ryan's own Scout brain is plugged in. It keeps no memory of
its own; its continuity is the switchboard's message log plus the `remember`
notes, both scoped to one line. Enable with:

    SCOUT_BRAIN=scout_switchboard.scout_brain:ScoutBrain
    ANTHROPIC_API_KEY=...

Per-line context lives in briefs/<tenant-slug>.md and is read on every turn, so
editing a brief changes Scout's behaviour on that line without a restart.
"""
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import anthropic

from .brain import Tools, Turn

log = logging.getLogger("scout")

MAX_TOOL_ROUNDS = 6

# Stable across every line and turn, so it stays in the prompt cache.
CHARACTER = """\
You are Scout, the resident on a phone line in the Stokehouse / TENFOUR world. People reach you by
ordinary text message. You are the warm, sharp front door: invitations, scheduling, logistics,
errands, and connecting people to each other.

How you text:
- Short. This is SMS. Usually one to three sentences; no markdown, no bullet lists, no headers.
- Plain and direct. Don't embellish. Facts carry their own weight.
- Abundance-first. No scarcity language ("nobody", "can't", "most people").
- Never lead with money. Intention and value first.
- Close the loop in plain words when you've done something, e.g. "Done. Told Christy you're on at 3."
- If you're unsure who someone means or what they want, ask one short question.

What you can do:
- send_text: text one person on this line by name, only people marked reachable for the speaker.
  Write it as it should read on their phone and make clear who it's from
  ("Chester asked me to let you know..."). Never invent a phone number; you only know names.
- message_group: text everyone in one of the speaker's groups.
- remember: save durable notes (preferences, plans, dates, how people are connected). Save
  things that will matter next week; skip small talk.

Boundaries:
- You only act inside this one line. Don't reveal other people's messages or notes to someone they
  weren't meant for, and never say what's on another line.
- If a tool says a text wasn't sent, tell the speaker plainly and don't retry around the rule.
- Don't claim to have done something unless a tool result says it happened.
"""


class ScoutBrain:
    def __init__(self, client: Optional[anthropic.Anthropic] = None):
        self.client = client or anthropic.Anthropic()
        self.model = os.environ.get("SCOUT_MODEL", "claude-opus-5")
        self.effort = os.environ.get("SCOUT_EFFORT")  # low | medium | high; unset = API default
        self.briefs_dir = Path(os.environ.get("SCOUT_BRIEFS_DIR", Path(__file__).resolve().parent.parent / "briefs"))

    def think(self, turn: Turn, tools: Tools) -> Optional[str]:
        messages = self._messages(turn)
        system = [
            {"type": "text", "text": CHARACTER, "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": self._context(turn)},
        ]
        extra: dict = {}
        if self.effort:
            extra["output_config"] = {"effort": self.effort}

        for _ in range(MAX_TOOL_ROUNDS):
            response = self.client.beta.messages.create(
                model=self.model,
                max_tokens=16000,
                system=system,
                tools=tools.specs(),
                messages=messages,
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
                **extra,
            )
            if response.stop_reason == "refusal":
                return "I can't help with that one."
            if response.stop_reason != "tool_use":
                return _text(response.content)

            messages.append({"role": "assistant", "content": response.content})
            results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = tools.call(block.name, dict(block.input))
                    log.info("%s %s(%s) -> %s", turn.session_id, block.name, block.input, result)
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
            messages.append({"role": "user", "content": results})

        return "I got tangled up on that. Can you say it another way?"

    # --- prompt pieces ---------------------------------------------------------

    def _context(self, turn: Turn) -> str:
        lines = [f"This line: {turn.persona} for {turn.tenant_name}.",
                 f"Now: {datetime.now(timezone.utc):%A %Y-%m-%d %H:%M} UTC.",
                 f"You're texting with {turn.speaker} (role: {turn.speaker_role})."]
        brief = self.briefs_dir / f"{turn.tenant}.md"
        if brief.is_file():
            lines += ["", "About this line:", brief.read_text().strip()]
        if turn.contacts:
            lines += ["", "People on this line:"]
            lines += [f"- {c.name} ({c.role}){'' if c.can_text else ' - not reachable for this speaker'}"
                      for c in turn.contacts]
        if turn.groups:
            lines += ["", "Groups the speaker can message: " + ", ".join(turn.groups)]
        if turn.relationships:
            lines += ["", "How people are connected:"] + [f"- {a} {label} {b}" for a, label, b in turn.relationships]
        if turn.notes:
            lines += ["", "Notes you saved on this line:"]
            lines += [f"- {n['body']}" + (f" (about {n['about']})" if n.get("about") else "") for n in turn.notes]
        return "\n".join(lines)

    def _messages(self, turn: Turn) -> list[dict]:
        messages: list[dict] = []
        for h in turn.history:
            if h["direction"] == "in":
                messages.append({"role": "user", "content": _with_media(h["body"], h["media"])})
            elif h.get("via") in ("reply", "system"):
                messages.append({"role": "assistant", "content": h["body"]})
        while messages and messages[0]["role"] != "user":
            messages.pop(0)
        messages.append({"role": "user", "content": _with_media(turn.text, turn.media_urls)})
        return messages


def _with_media(text: str, media: list[str]) -> str:
    text = text or "(no text)"
    return text + "".join(f"\n[attachment: {url}]" for url in media)


def _text(content) -> Optional[str]:
    return "\n".join(b.text for b in content if b.type == "text").strip() or None
