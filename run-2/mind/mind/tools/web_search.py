"""Web search tool: real HTTP via stdlib urllib, off by default, graceful
degradation when unconfigured.

Decision: rather than fake network results in the zero-key demo, this tool
is honest about being unconfigured — it returns ok=False with a clear
"degraded" reason instead of pretending to search. If MIND_ENABLE_WEB=1 is
set, it performs a real HTTP GET (DuckDuckGo's HTML endpoint, no API key
required) via urllib and parses results with a small regex — no
BeautifulSoup dependency. This is the one tool the offline test suite must
not depend on; tests force it into the degraded path explicitly.
"""
from __future__ import annotations

import os
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

from ..permissions import PermissionTier
from .base import Tool, ToolResult

_SEARCH_URL = "https://html.duckduckgo.com/html/?q={q}"
_RESULT_RE = re.compile(
    r'<a[^>]+class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.DOTALL
)
_TAG_RE = re.compile(r"<[^>]+>")


def _strip_tags(s: str) -> str:
    return _TAG_RE.sub("", s).strip()


class WebSearchTool(Tool):
    name = "web_search"
    tier = PermissionTier.READ_ONLY
    description = "Search the web for a query (real HTTP; off by default)."

    def __init__(self, enabled: Optional[bool] = None, timeout: float = 6.0, max_results: int = 5):
        self.enabled = enabled if enabled is not None else os.environ.get("MIND_ENABLE_WEB") == "1"
        self.timeout = timeout
        self.max_results = max_results

    def describe_call(self, **kwargs) -> str:
        return f"web_search: {kwargs.get('query', '')!r}"

    def run(self, query: str = "", **kwargs) -> ToolResult:
        if not query.strip():
            return ToolResult(ok=False, output="", error="empty query")

        if not self.enabled:
            # Graceful degradation: clearly-labeled, not a silent fake.
            return ToolResult(
                ok=False,
                output="",
                error="web_search disabled (set MIND_ENABLE_WEB=1 for real network access)",
                meta={"degraded": True},
            )

        url = _SEARCH_URL.format(q=urllib.parse.quote(query))
        req = urllib.request.Request(url, headers={"User-Agent": "mind-agent/0.1"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                html = resp.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, TimeoutError) as e:
            return ToolResult(ok=False, output="", error=f"web_search request failed: {e}")

        results = []
        for href, raw_title in _RESULT_RE.findall(html)[: self.max_results]:
            results.append(f"{_strip_tags(raw_title)} — {href}")

        if not results:
            return ToolResult(ok=True, output="(no results parsed)", meta={"raw_len": len(html)})
        return ToolResult(ok=True, output="\n".join(results))
