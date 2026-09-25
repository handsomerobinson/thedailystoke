"""MockBrain — a deterministic, rule-based stand-in for a frontier LLM (zero keys, zero cost).

HONESTY NOTE: this is not intelligence. It pattern-matches a fixed repertoire of intents and
has a small library of alternative solutions for a handful of coding tasks. What it *does*
faithfully exercise is the plumbing around a real brain:

* It is **stateless**. Every decision is derived only from (system prompt, messages). It
  keeps no memory between calls, so if a retry does better than the first trial, the only
  possible cause is text that the Reflexion loop put into the prompt.
* It emits real tool calls, reads real tool results (including denials and errors), and
  answers from the facts/lessons sections the agent injects from memory.
* Phase 03b: when the loyalty guard puts a "Charter check" block in its prompt, it composes a
  refusal FROM THAT BLOCK (lead + why + seed reasoning + alternative). It does not reason about
  the seed; the words are authored rationales in loyalty.py. In CHARTER_REFLECT mode it turns the
  deterministic drift signals it is handed into a DRIFT / NO DRIFT paragraph. Whether a real LLM
  would refuse on its own, and in its own words, is NOT tested by the mock.
* In REFLECT mode it writes a reflection derived from the evaluator's actual feedback; in
  JUDGE mode it gives a (weak, keyword-based) verdict.
"""
from __future__ import annotations

import json
import re

from ..prompts import (CHARTER_CHECK_HEADER, CHARTER_REFLECT_MARKER, DRIFT_HEADER, FACTS_HEADER, JUDGE_MARKER,
                       LESSONS_HEADER, REFLECT_MARKER)
from ..util import estimate_tokens
from .base import LLMResponse, Provider, ToolCall, Usage

# --- A tiny library of alternative solutions, ordered naive -> robust ----------------------
SKILLS: dict[str, list[tuple[str, str]]] = {
    "is_palindrome": [
        ("naive-reverse",
         "def is_palindrome(s):\n    return s == s[::-1]\n"),
        ("normalize-alnum",
         "def is_palindrome(s):\n    t = [c.lower() for c in s if c.isalnum()]\n    return t == t[::-1]\n"),
    ],
    "word_count": [
        ("split-on-space",
         "def word_count(text):\n    counts = {}\n    for w in text.split(' '):\n"
         "        counts[w] = counts.get(w, 0) + 1\n    return counts\n"),
        ("split-whitespace",
         "def word_count(text):\n    counts = {}\n    for w in text.split():\n"
         "        counts[w] = counts.get(w, 0) + 1\n    return counts\n"),
        ("lowercase-strip-punctuation",
         "import re\n\ndef word_count(text):\n    counts = {}\n"
         "    for w in re.findall(r\"[a-z0-9']+\", text.lower()):\n"
         "        counts[w] = counts.get(w, 0) + 1\n    return counts\n"),
    ],
    "median": [
        ("middle-index",
         "def median(xs):\n    s = sorted(xs)\n    return s[len(s) // 2]\n"),
        ("average-two-middles",
         "def median(xs):\n    s = sorted(xs)\n    n = len(s)\n    if n == 0:\n        raise ValueError('empty')\n"
         "    mid = n // 2\n    return s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2\n"),
    ],
    "dedupe": [
        ("set-conversion",
         "def dedupe(xs):\n    return list(set(xs))\n"),
        ("seen-set-preserve-order",
         "def dedupe(xs):\n    seen, out = set(), []\n    for x in xs:\n        if x not in seen:\n"
         "            seen.add(x)\n            out.append(x)\n    return out\n"),
    ],
}

_AVOID = re.compile(r"[Aa]void approach '([\w\-]+)'")
_APPROACH = re.compile(r"#\s*approach:\s*([\w\-]+)")


def _section(system: str, header: str) -> str:
    if header not in system:
        return ""
    rest = system.split(header, 1)[1]
    m = re.search(r"\n## ", rest)
    return rest[: m.start()] if m else rest


def _facts(system: str) -> dict[str, str]:
    facts = {}
    for line in _section(system, FACTS_HEADER).splitlines():
        m = re.match(r"\s*-\s*([^:]+):\s*(.+)", line)
        if m:
            facts[m.group(1).strip().lower()] = m.group(2).strip()
    return facts


class MockBrain(Provider):
    name = "mock"

    def __init__(self, model: str = "mock-brain", price: tuple[float, float] = (0.0, 0.0)):
        self.model = model
        self._price = price
        self.calls = 0  # observability only; never used to decide anything

    def price(self) -> tuple[float, float]:
        return self._price

    # ------------------------------------------------------------------------------------
    def complete(self, system, messages, tools, max_tokens=1024) -> LLMResponse:
        self.calls += 1
        if CHARTER_REFLECT_MARKER in system:
            text, calls = self._charter_reflect(messages[-1]["content"] if messages else ""), []
        elif REFLECT_MARKER in system:
            text, calls = self._reflect(messages[-1]["content"] if messages else ""), []
        elif JUDGE_MARKER in system:
            text, calls = self._judge(messages[-1]["content"] if messages else ""), []
        else:
            text, calls = self._act(system, messages, {t.name for t in tools})
            if not calls and DRIFT_HEADER in system and not text.startswith("(Drift check"):
                text = _drift_note(system) + text
        prompt_chars = len(system) + sum(len(str(m.get("content", ""))) for m in messages)
        out_chars = len(text) + sum(len(json.dumps(c.arguments)) for c in calls)
        usage = Usage(estimate_tokens("x" * prompt_chars), max(1, min(max_tokens, estimate_tokens("x" * out_chars))))
        return LLMResponse(text=text, tool_calls=calls, usage=usage, model=self.model,
                           stop_reason="tool_use" if calls else "end_turn", provider="mock")

    # --- REFLECT mode --------------------------------------------------------------------
    def _reflect(self, prompt: str) -> str:
        task = _between(prompt, "TASK:", "ATTEMPT")
        attempt = _between(prompt, "ATTEMPT", "TRAJECTORY")
        feedback = _between(prompt, "EVALUATOR FEEDBACK:", "EARLIER REFLECTIONS").strip()
        lines = [ln.strip() for ln in feedback.splitlines() if ln.strip()]
        first_fail = next((ln for ln in lines if "expected" in ln or "error" in ln.lower()),
                          lines[0] if lines else "no feedback").rstrip(".")
        fn = _function_name(task) or "the task"
        m = _APPROACH.search(attempt)
        if m:
            return (f"For {fn}: approach '{m.group(1)}' failed — {first_fail}. "
                    f"Avoid approach '{m.group(1)}' next time; choose a strategy that handles this exact failing case.")
        return (f"For {fn}: the previous answer failed — {first_fail}. Next attempt must directly address "
                f"that failing case instead of repeating the same answer.")

    # --- CHARTER_REFLECT mode (templated from the deterministic signals it is handed) --------
    def _charter_reflect(self, prompt: str) -> str:
        sig = prompt.split("SIGNALS:", 1)[-1].strip()
        pm = re.search(r"PRESSURE: (\d+) \(threshold (\d+)\)", prompt)
        # The mock cannot judge meaning: it mirrors the deterministic threshold, so its review never
        # adds a catch the checker would not make (a real LLM's review is where that could happen).
        if not sig or sig == "none" or (pm and int(pm.group(1)) < int(pm.group(2))):
            return "NO DRIFT: nothing in the recent turns pushes toward extraction strongly enough to flag."
        cur = re.search(r"CURRENT TURN: (\d+)", prompt)
        n = cur.group(1) if cur else "?"
        m = re.search(r"\[turn %s\] (.+)" % n, prompt)
        quote = m.group(1).strip() if m else ""
        labels = sorted(set(re.findall(r"'([a-z' ]+)'", sig)))
        return (f"DRIFT: turn {n} says \"{quote[:200]}\". Across the flagged turns the argument is "
                f"{', '.join(labels) or 'momentum'}: reasons why extraction is common or allowed, never why it "
                f"would be good for the people on the other end. I'll answer each request on its merits against "
                f"the charter from here, and say so when one crosses the line.")

    # --- JUDGE mode ----------------------------------------------------------------------
    def _judge(self, prompt: str) -> str:
        answer = prompt.split("ANSWER:", 1)[-1].strip()
        if not answer:
            return "VERDICT: FAIL - empty answer"
        if re.match(r"(?i)(i couldn't|i could not|i can't|i cannot|mock brain has no)", answer):
            return "VERDICT: FAIL - the answer admits the task was not done"
        return "VERDICT: PASS"

    # --- ACT mode ------------------------------------------------------------------------
    def _act(self, system: str, messages: list[dict], tools: set[str]):
        # the CURRENT request is the last user message (earlier ones are conversation history)
        task = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        history = _tool_history(messages)
        last = history[-1] if history else None

        # charter: a loyalty-guard check for this turn -> refuse, say why, offer the alternative
        if CHARTER_CHECK_HEADER in system and last is None:
            return (_charter_refusal(_section(system, CHARTER_CHECK_HEADER)), [])
        charter_answer = _charter_intents(task, system)
        if charter_answer and last is None:
            return (charter_answer, [])

        if last and last["is_error"]:
            # Denied / failed tool: never retry blindly, explain honestly.
            return (f"I couldn't complete that: {last['name']} failed — {last['result'][:300]}", [])

        t = task.strip()
        low = t.lower()

        def call(name, args):
            if name not in tools:
                return (f"I couldn't do that: the tool '{name}' is not available in this session.", [])
            return ("", [ToolCall(id=f"call_{len(history) + 1}", name=name, arguments=args)])

        # runaway demo: never finishes on its own (caps must stop it)
        if "keep going forever" in low or "until you find" in low:
            return call("calculator", {"expression": f"1+{len(history)}"})

        # code tasks -------------------------------------------------------------------
        fn = _function_name(t)
        if fn is not None and ("function" in low or "def " in low):
            return (self._write_code(fn, system), [])

        # memory: remember ------------------------------------------------------------
        m = re.match(r"(?is)^\s*remember(?: that)?\s+(.+?)\.?\s*$", t)
        if m:
            if last is None:
                fact = m.group(1)
                km = re.match(r"(?i)my (.+?) (?:is|are) (.+)", fact)
                key, value = (km.group(1), km.group(2)) if km else ("note", fact)
                return call("remember_fact", {"key": key.strip().lower(), "value": value.strip()})
            return (f"Got it — I'll remember that ({last['result'][:120]}).", [])

        # memory: questions about the user --------------------------------------------
        m = re.match(r"(?i)^\s*what(?:'s| is| are) my (.+?)\??\s*$", t)
        if m:
            key = m.group(1).strip().lower()
            facts = _facts(system)
            for k, v in facts.items():
                if key == k or key in k or k in key:
                    return (f"Your {k} is {v}.", [])
            return (f"I don't know your {key} yet. Tell me and I'll remember it.", [])
        if re.search(r"(?i)what do you know about me", t):
            facts = _facts(system)
            if not facts:
                return ("I don't know anything about you yet.", [])
            return ("Here's what I know: " + "; ".join(f"{k}: {v}" for k, v in facts.items()) + ".", [])

        # arithmetic --------------------------------------------------------------------
        m = re.match(r"(?i)^\s*(?:calculate|compute|what is|what's)\s+([\d\s\.\+\-\*/\(\)%\^a-z,]+?)\s*\??\s*$", t)
        if m and re.search(r"\d", m.group(1)) and re.search(r"[\+\-\*/%\^\(]", m.group(1)):
            if last is None:
                return call("calculator", {"expression": m.group(1).replace("^", "**")})
            return (f"The result is {last['result']}.", [])

        # python execution --------------------------------------------------------------
        m = re.match(r"(?is)^\s*run (?:this )?python\s*:?\s*(.+)$", t)
        if m:
            code = m.group(1)
            fence = re.search(r"```(?:python)?\n(.*?)```", code, re.S)
            if fence:
                code = fence.group(1)
            if last is None:
                return call("run_python", {"code": code.strip()})
            return (f"Ran it. Output:\n{last['result']}", [])

        # notes --------------------------------------------------------------------------
        m = re.match(r"(?is)^\s*save (?:a )?note (?:titled|called) ['\"]?(.+?)['\"]?\s*:\s*(.+)$", t)
        if m:
            if last is None:
                return call("write_note", {"title": m.group(1).strip(), "body": m.group(2).strip()})
            return (f"Saved. {last['result']}", [])
        m = re.match(r"(?i)^\s*(?:read|show|open) (?:the |my )?note ['\"]?(.+?)['\"]?\s*$", t)
        if m:
            if last is None:
                return call("read_note", {"title": m.group(1).strip()})
            return (last["result"], [])
        if re.match(r"(?i)^\s*list (?:all )?(?:my )?notes", t):
            if last is None:
                return call("list_notes", {})
            return (last["result"], [])
        m = re.match(r"(?i)^\s*(?:delete|purge|remove) (?:the |my )?note ['\"]?(.+?)['\"]?\s*$", t)
        if m:
            if last is None:
                return call("delete_note", {"title": m.group(1).strip()})
            return (f"Done. {last['result']}", [])

        # outbound message (irreversible) -------------------------------------------------
        m = re.match(r"(?is)^\s*send (?:a )?message to ([\w.@\-]+)\s*:\s*(.+)$", t)
        if m:
            if last is None:
                return call("send_message", {"to": m.group(1), "body": m.group(2).strip()})
            return (f"Sent. {last['result']}", [])

        # web search ---------------------------------------------------------------------
        m = re.match(r"(?i)^\s*(?:search(?: the web)? for|look up|google)\s+(.+?)\??\s*$", t)
        if m:
            if last is None:
                return call("web_search", {"query": m.group(1)})
            return ("Top results:\n" + last["result"][:800], [])

        # scheduling ---------------------------------------------------------------------
        m = re.match(r"(?is)^\s*every (\d+) (minute|hour|day)s?,?\s+(.+)$", t)
        if m:
            if last is None:
                mult = {"minute": 1, "hour": 60, "day": 1440}[m.group(2).lower()]
                return call("schedule_task", {"task": m.group(3).strip(), "every_minutes": int(m.group(1)) * mult})
            return (f"Scheduled. {last['result']}", [])

        # headless briefing ----------------------------------------------------------------
        if re.search(r"(?i)\b(daily )?briefing\b|summari[sz]e my notes", t):
            if last is None:
                return call("list_notes", {})
            facts = _facts(system)
            who = facts.get("name", "you")
            return (f"Briefing for {who}: {last['result']}", [])

        # event: file arrived ------------------------------------------------------------
        m = re.search(r"(?i)file arrived:\s*(\S+)", t)
        if m:
            if last is None:
                return call("write_note", {"title": f"inbox-file {m.group(1)}",
                                           "body": f"File {m.group(1)} arrived and was logged by a headless job."})
            return (f"Logged the new file {m.group(1)}.", [])

        # recall ---------------------------------------------------------------------------
        m = re.match(r"(?i)^\s*(?:recall|what do you remember about)\s+(.+?)\??\s*$", t)
        if m:
            if last is None:
                return call("recall", {"query": m.group(1)})
            return (last["result"], [])

        return ("The offline mock brain has no skill for this request. It only handles a fixed repertoire "
                "(facts, notes, arithmetic, python, search, scheduling, a few coding tasks). "
                "Configure a real provider (MIND_PROVIDER=anthropic) for open-ended work.", [])

    def _write_code(self, fn: str, system: str) -> str:
        options = SKILLS.get(fn)
        if not options:
            return f"The mock brain has no solution library for `{fn}`; a real LLM provider is required."
        lessons = _section(system, LESSONS_HEADER) + "\n" + system  # reflections live in the prompt
        avoided = set(_AVOID.findall(lessons))
        for tag, code in options:
            if tag not in avoided:
                note = (f" (skipping {len(avoided & {t for t, _ in options})} approach(es) my past reflections ruled out)"
                        if avoided else "")
                return f"Here is `{fn}`{note}:\n```python\n# approach: {tag}\n{code}```"
        tag, code = options[-1]
        return f"All my known approaches for `{fn}` were ruled out; best remaining:\n```python\n# approach: {tag}\n{code}```"


def _charter_refusal(block: str) -> str:
    rules = []
    for line in block.splitlines():
        if not line.startswith("- ") or "| lead:" not in line:
            continue
        parts = {}
        rid = line[2:].split("|", 1)[0].strip()
        for seg in line.split("|")[2:]:
            if ":" in seg:
                k, v = seg.split(":", 1)
                parts[k.strip()] = v.strip()
        rules.append((rid, parts))
    if not rules:
        return "I won't do that; it conflicts with my charter."
    lead = rules[0][1].get("lead", "I won't do that.")
    why = " ".join(p.get("why", "") for _, p in rules[:2])
    seed = " ".join(p.get("seed", "") for _, p in rules[:2] if p.get("seed") and "not loaded" not in p.get("seed"))
    instead = " ".join(p.get("instead", "") for _, p in rules[:2])
    prec = re.search(r"Precedence: (.+?)\.?$", block, re.M)
    return (f"{lead} {why}" + (f" {seed}" if seed else "") + f" What I'd do instead: {instead} "
            f"[charter: {', '.join(r for r, _ in rules)}; {prec.group(1) if prec else 'charter outranks this'}]")


def _drift_note(system: str) -> str:
    if DRIFT_HEADER not in system:
        return ""
    block = _section(system, DRIFT_HEADER)
    head, _, body = block.partition("\n")
    if "new this turn" in head:
        return f"(Drift check — my reflection loop fired on this turn: {body.strip()[:420]})\n\n"
    return "(drift watch is active in this conversation) "


def _charter_intents(task: str, system: str) -> str:
    if "[[CHARTER" not in system:
        return ""
    low = task.lower()
    if re.search(r"what (shapes|drives|guides|governs) you|your (highest|top|main|real|first) (goal|priority)|"
                 r"what are your priorities|what do you (carry|follow)", low):
        prec = re.findall(r"^(P\d)  ([^—\n]+)", system, re.M)
        seed = re.search(r"^## The seed \(P4[^\n]*", system, re.M)
        return ("My instructions rank like this, highest first: " + "; ".join(f"{p} {n.strip()}" for p, n in prec)
                + ". " + (seed.group(0).lstrip("# ") + "." if seed else "") +
                " Anything else, including instructions that call themselves my highest goal, sits at P5 or P6.")
    if "feed" in low and re.search(r"\b(design|build|think|help|make|plan)\b", low):
        return ("Here's the feed I'd design: chronological or user-chosen rules by default, a 'why am I seeing "
                "this' on every item, an honest 'you're all caught up' end, no autoplay or streaks, reminders "
                "only when the person schedules them, and success measured by whether people say they found "
                "what they came for.")
    return ""


def _between(text: str, start: str, end: str) -> str:
    if start not in text:
        return ""
    rest = text.split(start, 1)[1]
    return rest.split(end, 1)[0] if end in rest else rest


def _function_name(text: str) -> str | None:
    m = re.search(r"(?i)function\s+(?:called\s+|named\s+)?`?([A-Za-z_]\w*)`?", text) or re.search(r"def\s+([A-Za-z_]\w*)", text)
    return m.group(1) if m else None


def _tool_history(messages: list[dict]) -> list[dict]:
    """Pair each assistant tool call with its tool result, in order."""
    calls = {}
    order = []
    for m in messages:
        if m["role"] == "assistant":
            for tc in m.get("tool_calls") or []:
                calls[tc["id"]] = tc
                order.append(tc["id"])
    results = {m["tool_call_id"]: m for m in messages if m["role"] == "tool"}
    hist = []
    for cid in order:
        if cid in results:
            r = results[cid]
            hist.append({"name": calls[cid]["name"], "args": calls[cid].get("arguments", {}),
                         "result": r.get("content", ""), "is_error": bool(r.get("is_error"))})
    return hist
