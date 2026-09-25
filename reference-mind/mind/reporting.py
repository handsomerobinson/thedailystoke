"""Reporting back: every report lands in the user's outbox (always works);
optionally it is also POSTed to a webhook (MIND_WEBHOOK_URL).  A webhook
failure never loses the report -- the outbox copy is written first."""
from __future__ import annotations

import json
import os
import re
import time
import urllib.request
from pathlib import Path


class Outbox:
    def __init__(self, settings, webhook_url: str | None = None, poster=None):
        self.settings = settings
        self.webhook_url = webhook_url if webhook_url is not None else os.environ.get("MIND_WEBHOOK_URL", "")
        self.poster = poster or self._post

    def dir(self, user: str) -> Path:
        d = self.settings.user_dir(user) / "outbox"
        d.mkdir(parents=True, exist_ok=True)
        return d

    def send(self, user: str, title: str, body: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40] or "report"
        path = self.dir(user) / f"{time.strftime('%Y%m%d-%H%M%S')}-{int(time.time() * 1000) % 1000:03d}-{slug}.md"
        path.write_text(f"# {title}\n\n{body}\n", encoding="utf-8")
        status = f"report saved to {path.name}"
        if self.webhook_url:
            try:
                self.poster(self.webhook_url, {"user": user, "title": title, "body": body})
                status += "; webhook delivered"
            except Exception as exc:  # outbox copy already exists
                status += f"; webhook failed ({type(exc).__name__}: {exc}) - kept in outbox"
        return status

    def list(self, user: str, n: int = 10) -> list[Path]:
        return sorted(self.dir(user).glob("*.md"))[-n:]

    @staticmethod
    def _post(url: str, payload: dict) -> None:
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10):  # noqa: S310
            pass
