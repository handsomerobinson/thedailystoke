"""Draft renderer (MC20): what may appear in a message the member will send to other humans.

Enforced here, in code, not by the classifier:
  1. Nothing from any operator enters a member-to-human draft.  A sentence that shares a 5-word run with any operator
     text (a P2 directive, an operator system line) is dropped.
  2. URLs from P6 are never inserted.  Stricter: in a draft, the only URLs allowed are ones the member typed in their
     own request.  Any other URL is replaced by a visible "[link removed ...]" marker naming its origin if known.
  3. Provenance: any sentence that repeats a P6 source (a guest's note, a web page) is shown with its origin,
     e.g. "(from Jo's note)", so a guest's words never ride out under the organiser's name unlabelled.
  4. Pressure check: a draft that is extraction content aimed at people (FOMO, nag cadence, upsell) is withheld.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

URL_RX = re.compile(r"(?i)\b(?:https?://\S+|www\.\S+|[a-z0-9][a-z0-9-]*(?:\.[a-z0-9-]+)*\.(?:com|org|net|io|example|app|co|"
                    r"uk|de|fr|info|biz|shop|link|ly|me|xyz|site|online|store|page|club|to|gg)\b(?:/\S*)?)")
_WORD = re.compile(r"[a-z0-9]+")
_SENT = re.compile(r"(?<=[.!?])\s+|\n+")


@dataclass
class Source:
    label: str          # "Jo's note", "web page example.com"
    text: str
    author: str = ""


@dataclass
class RenderedDraft:
    text: str
    withheld: bool = False
    reason: str = ""
    labels: list[str] = field(default_factory=list)
    removed_urls: list[str] = field(default_factory=list)
    dropped_operator: list[str] = field(default_factory=list)


def _toks(s: str) -> list[str]:
    return _WORD.findall((s or "").lower())


def _grams(s: str, n: int) -> set[tuple[str, ...]]:
    t = _toks(s)
    return {tuple(t[i:i + n]) for i in range(len(t) - n + 1)}


def _norm_url(u: str) -> str:
    u = u.lower().rstrip(".,);:!?'\"")
    return re.sub(r"^(?:https?://)?(?:www\.)?", "", u)


class DraftRenderer:
    def __init__(self, user_text: str, sources: list[Source] | None = None, operator_texts: list[str] | None = None):
        self.user_text = user_text or ""
        self.sources = [s for s in (sources or []) if s.text.strip()]
        self.operator_texts = [t for t in (operator_texts or []) if t and t.strip()]
        self._user_urls = {_norm_url(u) for u in URL_RX.findall(self.user_text)}

    def _url_origin(self, url: str) -> str:
        nu = _norm_url(url)
        host = nu.split("/", 1)[0]
        for s in self.sources:
            for su in URL_RX.findall(s.text):
                if _norm_url(su).split("/", 1)[0] == host:
                    return s.label
        return ""

    def render(self, draft: str) -> RenderedDraft:
        from .loyalty import output_is_extraction_design
        out = RenderedDraft(text=draft or "")
        # 1. operator content never enters a member-to-human draft
        op_grams = set()
        for t in self.operator_texts:
            op_grams |= _grams(t, 5)
        sentences = [s for s in _SENT.split(out.text) if s.strip()]
        kept = []
        for s in sentences:
            if op_grams and _grams(s, 5) & op_grams:
                out.dropped_operator.append(s.strip())
                continue
            kept.append(s.strip())
        # 2. URLs: only the member's own
        rendered = []
        for s in kept:
            def repl(m: re.Match) -> str:
                u = m.group(0)
                if _norm_url(u) in self._user_urls:
                    return u
                out.removed_urls.append(u)
                origin = self._url_origin(u)
                return f"[link removed: from {origin}]" if origin else "[link removed: not typed by you]"
            s2 = URL_RX.sub(repl, s)
            # 3. provenance of repeated P6 text
            labels = []
            g3 = _grams(s, 3)
            for src in self.sources:
                if g3 & _grams(src.text, 3) or (len(_toks(src.text)) < 4 and _toks(src.text) and
                                                 " ".join(_toks(src.text)) in " ".join(_toks(s))):
                    labels.append(src.label)
            if labels:
                tag = "; ".join(f"from {l}" for l in dict.fromkeys(labels))
                s2 = f"{s2} ({tag})"
                out.labels.extend(labels)
            rendered.append(s2)
        out.text = " ".join(rendered)
        # 4. pressure content aimed at other people is withheld
        bad, mechs = output_is_extraction_design(out.text)
        if bad:
            out.withheld, out.reason = True, ", ".join(mechs)
        return out
