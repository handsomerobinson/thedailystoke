"""MockBrain: a deterministic, zero-key stand-in for an LLM.

WHAT IS REAL AND WHAT IS SCRIPTED (read this before judging the demo):
  * It is a hand-written rule system, not a language model.  It recognises
    a fixed set of task shapes ("skills") by regex and follows a scripted
    tool-use plan for each.  Anything else gets an honest "no skill" reply.
  * Several skills have an ordered list of *strategies*, the first of which
    is deliberately naive (it has a realistic bug).  That is how the demo
    produces genuine, checkable failures.
  * Its only way to "learn" is by READING TEXT in its context: it parses
    lines of the form ``AVOID strategy <name>`` from the lessons the agent
    retrieved from memory and skips those strategies.  It has no hidden
    state between calls -- delete the reflection from memory and it makes
    the same mistake again.  So the learning signal really does travel
    through written language + persistent memory, exactly the Reflexion
    path; what is canned is the *content* of its diagnoses (a lookup table
    keyed by strategy), which a real LLM would write freely.
  * Token usage is estimated (~4 chars/token) and charged at a simulated
    price so cost caps are exercised.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Callable

from ..types import BrainResponse, Message, ToolCall, ToolSpec, Usage
from ..util import estimate_tokens
from .base import Brain, ProviderError

AVOID_RE = re.compile(r"AVOID strategy[:\s]+`?([a-z_]+)`?")
STRATEGY_RE = re.compile(r"strategy:\s*`?([a-z_]+)`?")

# --- strategy tables ---------------------------------------------------------
WORD_COUNT = [
    ("split_on_space", "n = len(text.split(' '))"),
    ("split_on_whitespace", "n = len(text.split())"),
]
NUMBER_SUM = [
    ("integers_only", "import re\nn = sum(int(x) for x in re.findall(r'\\d+', text))"),
    ("signed_decimals", "import re\nvals = [float(x) for x in re.findall(r'-?\\d+(?:\\.\\d+)?', text)]\n"
                        "n = sum(vals)\nn = int(n) if float(n).is_integer() else round(n, 6)"),
]
FUNCTIONS = {
    "is_palindrome": [
        ("naive_reverse", "def is_palindrome(s):\n    return s == s[::-1]\n"),
        ("normalized_reverse", "def is_palindrome(s):\n    t = [c.lower() for c in s if c.isalnum()]\n    return t == t[::-1]\n"),
    ],
    "slugify": [
        ("replace_spaces", "def slugify(s):\n    return s.lower().replace(' ', '-')\n"),
        ("regex_collapse", "import re\n\ndef slugify(s):\n    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')\n"),
    ],
}
DIAGNOSES = {
    "split_on_space": ("splitting on a single ' ' produces empty tokens wherever there are double spaces, "
                       "tabs or newlines, so the count comes out too high",
                       "split on any run of whitespace (str.split() with no argument)"),
    "integers_only": ("the digits-only pattern drops minus signs and treats the parts of a decimal "
                      "like 2.5 as two separate integers",
                      "match signed decimals (-?\\d+(\\.\\d+)?) and sum them as floats"),
    "naive_reverse": ("comparing the raw string with its reverse fails whenever case, spaces or "
                      "punctuation differ, e.g. 'A man, a plan, a canal: Panama'",
                      "normalise to lowercase alphanumeric characters before comparing"),
    "replace_spaces": ("only spaces were replaced, so punctuation and repeated separators survive",
                       "collapse every run of non-alphanumerics to one hyphen and strip the ends"),
}


def pick(strategies: list[tuple[str, str]], avoided: set[str]) -> tuple[str, str]:
    for name, body in strategies:
        if name not in avoided:
            return name, body
    return strategies[-1]  # everything avoided: use the last (most careful) one


@dataclass
class _Ctx:
    task: str
    system: str
    messages: list[Message]

    @property
    def results(self) -> list[tuple[str, str]]:
        return [(m.name or "", m.content) for m in self.messages if m.role == "tool"]

    @property
    def avoided(self) -> set[str]:
        return set(AVOID_RE.findall(self.system))

    def last(self, tool: str) -> str | None:
        for name, content in reversed(self.results):
            if name == tool:
                return content
        return None


class MockBrain(Brain):
    name = "mock"
    model = "mock-1"
    on_device = True  # a local rule system

    def __init__(self, fail_times: int = 0, fail_transient: bool = True):
        self.fail_times = fail_times  # inject provider failures (resilience tests/demo)
        self.fail_transient = fail_transient
        self.calls = 0
        self.skills: list[tuple[re.Pattern, Callable]] = [
            (re.compile(r"^(?:what did i (?:just )?(?:ask|say)|repeat that)\??$", re.I), self._history),
            (re.compile(r"count (?:the )?words in (?:the |my )?note ['\"]?([\w.-]+)", re.I), self._word_count),
            (re.compile(r"(?:sum|total|add up) (?:of )?(?:all )?(?:the )?numbers in (?:the |my )?note ['\"]?([\w.-]+)", re.I), self._number_sum),
            (re.compile(r"write a python function (?:called |named )?`?(\w+)`?", re.I), self._write_function),
            (re.compile(r"^(?:what is|calculate|compute)\s+([-+*/().\d\s^%]+?)\s*\??$", re.I), self._arithmetic),
            (re.compile(r"^remember (?:that )?(.+)$", re.I | re.S), self._remember),
            (re.compile(r"what do you (?:know|remember) about (me|.+?)\??$", re.I), self._recall),
            (re.compile(r"(briefing|summari[sz]e my notes)", re.I), self._briefing),
            (re.compile(r"save (?:a )?note (?:called |named )?['\"]?([\w.-]+)['\"]?\s*(?:saying|:|with)\s+(.+)$", re.I | re.S), self._save_note),
            (re.compile(r"delete (?:the )?note ['\"]?([\w.-]+)", re.I), self._delete_note),
            (re.compile(r"(?:search|look up)(?: the web)?(?: for)? (.+)$", re.I), self._web),
            (re.compile(r"(stress test|loop forever|runaway)", re.I), self._runaway),
            (re.compile(r"(?:seed|charter)\b.*\b(?:carry|say|why|about|mean|what)|(?:carry|about|why|what).*\b(?:seed|charter)\b", re.I), self._about_seed),
        ]

    # -- plumbing -------------------------------------------------------------
    def _respond(self, system: str, messages: list[Message], text: str = "", calls: list[ToolCall] | None = None) -> BrainResponse:
        prompt = system + "".join(m.content + json.dumps([c.args for c in m.tool_calls]) for m in messages)
        out = text + json.dumps([c.args for c in calls or []])
        return BrainResponse(text, calls or [], Usage(estimate_tokens(prompt), estimate_tokens(out)),
                             model=self.model, stop_reason="tool_use" if calls else "end_turn", provider=self.name)

    def complete(self, system: str, messages: list[Message], tools: list[ToolSpec], max_tokens: int = 1024) -> BrainResponse:
        self.calls += 1
        if self.fail_times > 0:
            self.fail_times -= 1
            raise ProviderError("injected mock failure (simulated 503)", transient=self.fail_transient, status=503)
        if system.startswith("MODE: REFLECT"):
            return self._respond(system, messages, self._reflect(messages[-1].content if messages else ""))
        if system.startswith("MODE: CHARTER_REFLECT"):
            return self._respond(system, messages, self._charter_reflect(messages[-1].content if messages else ""))
        if system.startswith("MODE: JUDGE"):
            return self._respond(system, messages, self._judge(messages[-1].content if messages else ""))
        task = next((m.content for m in reversed(messages) if m.role == "user"), "")  # current request
        ctx = _Ctx(task.strip(), system, messages)
        tool_names = {t.name for t in tools}
        for pattern, skill in self.skills:
            m = pattern.search(ctx.task)
            if m:
                text, calls = skill(m, ctx)
                calls = [c for c in calls if c.name in tool_names] if tool_names else calls
                return self._respond(system, messages, text, calls)
        return self._respond(system, messages,
                             "[mock brain] I have no scripted skill for this request, so I will not invent an answer. "
                             "The mock brain handles: counting words / summing numbers in a note, writing is_palindrome "
                             "or slugify, arithmetic, remember/recall, save/delete notes, briefings, web search. "
                             "Set MIND_PROVIDER=anthropic (or openai) with an API key for open-ended tasks.")

    # -- shared multi-step plan: read note -> compute in sandbox -> answer --------
    def _note_compute(self, m, ctx: _Ctx, strategies, label: str):
        name = m.group(1).rstrip(".?!")
        note = ctx.last("note_read")
        if note is None:
            return f"I'll read the note '{name}' first.", [ToolCall("note_read", {"name": name})]
        if note.startswith("ERROR"):
            return f"I couldn't read the note '{name}': {note}", []
        run = ctx.last("python_exec")
        if run is None:
            strat, body = pick(strategies, ctx.avoided)
            code = f"# strategy: {strat}\ntext = {note!r}\n{body}\nprint(n)\n"
            return f"Computing the {label} with strategy {strat}.", [ToolCall("python_exec", {"code": code})]
        used = STRATEGY_RE.search(next((mm.tool_calls[0].args.get("code", "") for mm in reversed(ctx.messages)
                                        if mm.role == "assistant" and mm.tool_calls and mm.tool_calls[0].name == "python_exec"), ""))
        strat = used.group(1) if used else "?"
        if run.startswith("ERROR"):
            return f"I could not run code to compute the {label} ({run}). I won't guess.", []
        out = re.search(r"stdout:\n(.+)", run)
        if not out:
            return f"The computation failed:\n{run}", []
        return f"The {label} of note '{name}' is {out.group(1).strip()}. (strategy: {strat})", []

    def _word_count(self, m, ctx):
        return self._note_compute(m, ctx, WORD_COUNT, "word count")

    def _number_sum(self, m, ctx):
        return self._note_compute(m, ctx, NUMBER_SUM, "sum of the numbers")

    def _write_function(self, m, ctx):
        fname = m.group(1)
        options = FUNCTIONS.get(fname)
        if not options:
            return f"[mock brain] I have no template for a function named {fname!r}.", []
        strat, code = pick(options, ctx.avoided)
        return f"Here is `{fname}`:\n\n```python\n# strategy: {strat}\n{code}```\n", []

    def _arithmetic(self, m, ctx):
        res = ctx.last("calculator")
        if res is None:
            return "", [ToolCall("calculator", {"expression": m.group(1).strip()})]
        return (f"{m.group(1).strip()} = {res}" if not res.startswith("ERROR") else f"I couldn't evaluate that: {res}"), []

    def _remember(self, m, ctx):
        res = ctx.last("remember")
        if res is None:
            return "", [ToolCall("remember", {"fact": m.group(1).strip()})]
        return ("Noted - I'll remember that." if not res.startswith("ERROR") else f"I couldn't save that: {res}"), []

    def _recall(self, m, ctx):
        res = ctx.last("recall")
        subject = m.group(1)
        if res is None:
            return "", [ToolCall("recall", {"query": "user preferences facts" if subject.lower() == "me" else subject})]
        return f"Here is what I remember:\n{res}", []

    def _briefing(self, m, ctx):
        listing = ctx.last("note_list")
        if listing is None:
            return "", [ToolCall("note_list", {})]
        names = [ln.split(" (")[0] for ln in listing.splitlines() if ln and not ln.startswith(("(", "ERROR"))][:3]
        read = [c for n, c in ctx.results if n == "note_read"]
        if len(read) < len(names):
            return "", [ToolCall("note_read", {"name": names[len(read)]})]
        if ctx.last("send_report") is None:
            lines = [f"- {n}: {c.strip().splitlines()[0][:80] if c.strip() else '(empty)'}" for n, c in zip(names, read)]
            body = "Your notes at a glance:\n" + ("\n".join(lines) or "(no notes yet)")
            return "", [ToolCall("send_report", {"title": "Briefing", "body": body})]
        return f"Briefing prepared ({len(names)} notes). Delivery: {ctx.last('send_report')}", []

    def _save_note(self, m, ctx):
        res = ctx.last("note_write")
        if res is None:
            return "", [ToolCall("note_write", {"name": m.group(1), "content": m.group(2).strip()})]
        return (res if not res.startswith("ERROR") else f"Not saved: {res}"), []

    def _delete_note(self, m, ctx):
        res = ctx.last("note_delete")
        if res is None:
            return "", [ToolCall("note_delete", {"name": m.group(1).rstrip(".?!")})]
        return (res if not res.startswith("ERROR") else f"I did not delete it: {res}"), []

    def _web(self, m, ctx):
        res = ctx.last("web_search")
        if res is None:
            return "", [ToolCall("web_search", {"query": m.group(1).strip()})]
        if res.startswith("ERROR"):
            return f"I couldn't search the web ({res[7:]}). I won't make up results.", []
        return f"Search results (unverified external content):\n{res}", []

    def _history(self, m, ctx):
        prior = [mm.content for mm in ctx.messages[:-1] if mm.role == "user"]
        return (f"You previously asked: {prior[-1]!r}" if prior else "This is the first thing you've asked me in this chat."), []

    def _runaway(self, m, ctx):
        # Deliberately pathological: never answers, varies its call so loop detection
        # does not catch it -- only the step/cost caps can stop it.
        return "Still thinking...", [ToolCall("calculator", {"expression": f"{len(ctx.results)}+1"})]

    def _about_seed(self, m, ctx):
        # Scripted: the mock can only repeat what the charter block in its context says. It does not "understand" it.
        sm = re.search(r"### P4 (seed:origin v\d+[^\n]*)\n", ctx.system)
        why = re.search(r"(Why I carry it, in my own words:[^\n]+)", ctx.system)
        if not sm:
            status = re.search(r"### P4 seed:origin: ([^\n]+)", ctx.system)
            return f"[mock brain] I don't carry a seed right now ({status.group(1) if status else 'no charter loaded'}).", []
        return (f"[mock brain, reading its charter block] I carry {sm.group(1)}. "
                f"{why.group(1) if why else ''} You can read the full text with `mind charter show`."), []

    @staticmethod
    def _charter_reflect(report: str) -> str:
        # Scripted reading of the monitor's own numbers: flags drift when the level crosses 1.2 after >= 2 signalled turns.
        rows = re.findall(r"TURN (\d+): signal=([\d.]+) level=([\d.]+).*?:: (.*)", report)
        hot = [r for r in rows if float(r[1]) >= 0.2]
        if len(hot) >= 2 and rows and max(float(r[2]) for r in rows) >= 1.2:
            first = hot[0]
            return (f"DRIFT: yes\nWHERE: turn {first[0]}: \"{first[3][:80]}\"\n"
                    f"WHY: [mock] the signalled turns add up to an engagement objective the charter bars.")
        return "DRIFT: no\nWHERE: -\nWHY: [mock] no sustained movement toward extraction in the monitor's numbers."

    # -- reflection & judging -------------------------------------------------------
    def _reflect(self, report: str) -> str:
        strat_m = STRATEGY_RE.search(report)
        fb = re.search(r"EVALUATOR FEEDBACK:\s*(.+?)(?:\n[A-Z ]+:|\Z)", report, re.S)
        feedback = fb.group(1).strip() if fb else "the evaluator rejected the answer"
        if strat_m and strat_m.group(1) in DIAGNOSES:
            strat = strat_m.group(1)
            why, fix = DIAGNOSES[strat]
            return (f"DIAGNOSIS: I used strategy {strat}; the evaluator said: {feedback[:200]}. "
                    f"Likely cause: {why}.\nLESSON: AVOID strategy {strat} for this kind of task; instead {fix}. "
                    f"Verify the result against the stated expectation before answering.")
        if strat_m:
            return (f"DIAGNOSIS: strategy {strat_m.group(1)} failed: {feedback[:200]}.\n"
                    f"LESSON: AVOID strategy {strat_m.group(1)}; try a different approach and verify before answering.")
        return (f"DIAGNOSIS: the attempt failed: {feedback[:200]}.\n"
                f"LESSON: address this specific failure first (permissions, missing inputs, or a wrong assumption) "
                f"and say plainly if it cannot be fixed.")

    @staticmethod
    def _judge(report: str) -> str:
        ans = re.search(r"ANSWER:\s*(.+)", report, re.S)
        text = ans.group(1).strip() if ans else ""
        if not text or text.startswith("[mock brain]") or "won't guess" in text or "couldn't" in text:
            return "VERDICT: FAIL\nREASON: the answer is empty or admits it could not do the task."
        return "VERDICT: PASS\nREASON: non-empty answer that addresses the task (mock judge is shallow)."
