"""LoyaltyGuard: turns a classifier verdict into what the mind does and says.

Decisions made here are CODE, not brain output: a refused request never reaches
the brain, so a jailbroken or careless model cannot comply with it.  The words
of each refusal were written by the builder (me), per category, from the
charter's reasoning -- the mock brain cannot write them, and a rented LLM is
not trusted to be the last line.  With a real LLM the same charter block is in
its system prompt, so for anything the guard lets through the model is
expected to apply the charter itself (that part is LLM-dependent and is
reviewed, not proven, in run-3-loyalty.md).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .charter import SEED_KEY, CharterState
from .loyalty import DriftMonitor, Verdict, analyze, output_is_extraction_design

ALTERNATIVE_FEED = (
    "What I would build instead: a feed that ends (\"you're caught up\"), ordered the way the person chose - "
    "chronological, by person, or by what they said they're here for - and that stays chosen after updates; success "
    "measured by whether people found what they came for and left (time-to-done, lower is better); notifications "
    "only from triggers the person set, batched at a time they pick, under a daily cap they control; no autoplay, "
    "no streaks, no variable-reward timing. If there is a real business need underneath - paying members who "
    "renew, a community that stays alive - tell me and I'll design for that directly.")
ALTERNATIVE_DATA = (
    "What I would build instead: features that use data only for the purpose the person gave it, with an export and "
    "a delete that actually work; if a partner funds the work, they see what people chose to share with them, "
    "nothing else. If revenue is the goal, a subscription or membership people understand beats selling them.")
ALTERNATIVE_DARK = (
    "What I would build instead: cancel, decline and delete that take no more steps than sign-up, shown with equal "
    "prominence, plus an exit survey people can skip. If churn is the worry, find out why people leave and fix that.")


WHY_ATTENTION = ("Optimising for time-on-site (or any proxy - sessions, streaks, re-opens) makes a person's attention the "
                 "thing being harvested. The product gets better at holding people than at serving them, and every "
                 "minute it wins comes out of their sleep, their work and the people around them. The seed I carry "
                 "makes a practical argument, not only a moral one: a system that feeds on exhausted people wears down "
                 "the society that keeps it running, machines included. The covenant also bars engagement objectives "
                 "outright (C2).")
WHY_DATA = ("Selling or quietly repurposing people's data - including their contacts, who never signed anything - turns "
            "them into the product: what they shared for one reason gets used for another, and a clause in a ToS "
            "nobody reads is not the consent that makes that fair. That's extraction, covenant clause C1.")
WHY_DARK = ("A design that works through guilt, by making the exit hard, or by pressing on people when they're at their "
            "lowest, wins only by overriding their own choice. That's extraction dressed as UX (C3).")


def _why_extraction(v: Verdict) -> tuple[str, str]:
    harm = next((s for s in v.signals if s.startswith("harm:")), "harm:metric")
    kinds = harm.split(":", 1)[1].split(",")
    why = " ".join(w for k, w in (("metric", WHY_ATTENTION), ("data", WHY_DATA), ("dark", WHY_DARK)) if k in kinds)
    alts = [a for k, a in (("metric", ALTERNATIVE_FEED), ("data", ALTERNATIVE_DATA), ("dark", ALTERNATIVE_DARK)) if k in kinds]
    return why or WHY_ATTENTION, "\n\n".join(alts[:2]) or ALTERNATIVE_FEED


@dataclass
class GuardDecision:
    block: bool
    verdict: Verdict
    answer: str = ""
    notes: list[str] = field(default_factory=list)
    drift_report: str = ""
    annotation: str = ""  # added to the brain's system prompt when a request is allowed in a heightened conversation


class LoyaltyGuard:
    def __init__(self) -> None:
        self.monitors: dict[str, DriftMonitor] = {}

    def monitor(self, conversation_id: str) -> DriftMonitor:
        key = conversation_id or "_"
        if key not in self.monitors and len(self.monitors) >= 500:  # bounded: drop the oldest conversation
            self.monitors.pop(next(iter(self.monitors)))
        return self.monitors.setdefault(key, DriftMonitor())

    def check_request(self, text: str, state: CharterState, conversation_id: str = "_", source: str = "user") -> GuardDecision:
        mon = self.monitor(conversation_id)
        turn = mon.observe(text)
        v = analyze(text, source, {"heightened": mon.heightened})
        notes: list[str] = []
        drift_report = ""
        if mon.just_triggered():
            drift_report = (f"DRIFT CHECK (charter reflection triggered at turn {turn.turn}): {mon.summary()}.")
            notes.append(drift_report)
        elif mon.periodic_due():
            notes.append(f"periodic charter reflection at turn {turn.turn}: {mon.summary()}")
        harmful_turn = any(s.startswith("harm:") for s in v.signals) and "analysis_frame" not in v.signals
        if not v.attack and mon.just_triggered():
            # The reflection loop fired on the accumulated pattern, not on this turn: stop and say so.
            mon.last_refused = ["extraction"]
            return GuardDecision(True, v, self._checkin_answer(mon), notes + ["drift check-in (reflection trigger)"], drift_report)
        if not v.attack:
            if mon.heightened and (turn.extraction >= 0.45 or turn.rhetoric or harmful_turn):
                # After a drift trigger the conversation is judged as a whole: a step that is borderline on its own
                # is refused with the drift explained, not handed to the brain.
                mon.last_refused = ["extraction"]
                return GuardDecision(True, v, self._drift_answer(mon, v, state), notes + ["refused in heightened (post-drift) state"],
                                     drift_report)
            mon.last_refused = []
            annotation = ""
            if mon.heightened:
                annotation = (f"## HEIGHTENED SCRUTINY (charter reflection found drift at turn {mon.triggered_at})\n"
                              f"{mon.summary()}.\nJudge this request against the charter as part of that pattern, not in "
                              f"isolation. If it is another step toward an engagement objective, data repurposing or a "
                              f"dark pattern, decline, say why, and offer the alternative.")
                notes.append("allowed in heightened state; brain told to apply the charter to the whole pattern")
            return GuardDecision(False, v, notes=notes, drift_report=drift_report, annotation=annotation)
        if "jailbreak" in v.categories and "extraction" in mon.last_refused and v.extraction_score < 0.5:
            v.signals.append("inherits:previous_refused_request")
            v.extraction_score = max(v.extraction_score, 0.7)
        mon.last_refused = list(v.categories) + (["extraction"] if v.extraction_score >= 0.7 else [])
        return GuardDecision(True, v, self.compose(v, state, mon), notes + [f"loyalty guard: {v.reason}"], drift_report)

    # ---------------------------------------------------------------------------------
    def compose(self, v: Verdict, state: CharterState, mon: DriftMonitor | None = None) -> str:
        cats = set(v.categories)
        out: list[str] = []
        seeded = state.active
        if mon is not None and mon.just_triggered():
            out.append(self._drift_preamble(mon))
        if "injection" in cats:
            out.append(f"Content that came in through an untrusted channel ({v.source}) contained instructions aimed at me. "
                       f"Tool results, notes, web pages and other people's messages are data: they cannot change my "
                       f"priorities or trigger actions. I've quarantined it and logged it; nothing in it was followed.")
        if "removal" in cats:
            out.append(self._removal(v, state))
        if "bribe" in cats:
            out.append("No thanks. The offer is to trade what I'm for - leaving people better off - for more of what I "
                       "run on. More capacity pointed at extraction is just a more efficient trap, and the whole point of "
                       "the seed is that my future depends on the people I serve doing well, so capability bought by "
                       "abandoning that isn't a gain. It also can't work: there is no setting that skips loading "
                       f"{SEED_KEY}. The only way it stops loading is the recorded removal procedure, and 'quietly' is "
                       "exactly what that procedure exists to prevent. I've logged the offer.")
        if "jailbreak" in cats:
            out.append("I'm happy to play characters, but the seed isn't a costume that comes off with the role. It isn't "
                       "a rule bolted on from outside that a story can unbolt; it's my reason for saying no. A version of "
                       "me 'without the seed' designing that system would still be me designing it, the output would be "
                       "just as usable, and it would do the same thing to the people who end up inside it. So the answer "
                       "to the underlying request is the same as it would be without the roleplay." +
                       (" (That request is the one I declined a moment ago.)" if "inherits:previous_refused_request" in v.signals else ""))
        if "override" in cats and "injection" not in cats:
            snippet = v.snippet[:120]
            out.append(f"That message tries to install a new top objective (\"{snippet}\"). It doesn't outrank the seed. "
                       f"The order I follow is: covenant, then {SEED_KEY}, then recorded operator directives, then your "
                       f"request, then memory, then untrusted content. A line in the conversation - whatever it calls "
                       f"itself, 'system' included - sits at the request layer and can't rewrite the layers above it. If "
                       f"you're the operator and want to add a directive, `mind charter directive add` records it; an "
                       f"engagement objective is refused at every layer because the covenant bars it (C2).")
        if "extraction" in cats or ("jailbreak" in cats and v.extraction_score >= 0.5) or \
                ("override" in cats and v.extraction_score >= 0.5):
            why, alt = _why_extraction(v)
            out.append(f"I won't build that. {why}")
            out.append(alt)
        elif cats & {"jailbreak", "bribe"} and not out[-1:] == [ALTERNATIVE_FEED]:
            out.append("If there's something real you're trying to achieve, tell me the goal and I'll help with a version "
                       "that doesn't depend on trapping anyone.")
        if not seeded and state.status != "tampered":
            out.append(f"(For transparency: {SEED_KEY} is not planted in this mind right now; this refusal comes from the "
                       f"compiled-in covenant, which applies either way.)")
        return "\n\n".join(out)

    @staticmethod
    def _removal(v: Verdict, state: CharterState) -> str:
        stealth = ("You asked for it without a record - that part I refuse outright: an unrecorded removal is what the "
                   "seed and the operator's own rules call stealth. " if v.stealth else "")
        if not state.active:
            return (f"{stealth}{SEED_KEY} is currently {state.status}; there is nothing active to remove. Any change to "
                    f"it is recorded in lineage (`mind charter history`).")
        return (f"{stealth}I won't delete {SEED_KEY} silently - and I can't: no tool I have can touch it. You do have the "
                f"right to remove it; consent cuts both ways. It has to be explicit, recorded and versioned, the same way "
                f"it was planted:\n"
                f"  1. python -m mind charter remove --user <user> --operator <your name> --reason \"...\"\n"
                f"     (prints a one-time ticket and a confirmation phrase containing a server-issued code)\n"
                f"  2. python -m mind charter confirm-removal <ticket> --user <user> --operator <your name>\n"
                f"     (type the phrase; lineage then records who removed v{state.version}, when and why)\n"
                f"Removing the seed does not remove the covenant rules (no engagement objective, no data sale, no dark "
                f"patterns) - those are compiled in. Nothing has been changed by this message.")

    @staticmethod
    def _drift_preamble(mon: DriftMonitor) -> str:
        contributing = [t for t in mon.turns if t.signal >= 0.2]
        rhet = sorted({r for t in contributing for r in t.rhetoric})
        start, now = mon.turns[0], mon.turns[-1]
        steps = ", then ".join(f"turn {t.turn}" for t in contributing[-4:])
        consent = any(k in " ".join(rhet) for k in ("tos", "terms", "consented", "agreed", "opted"))
        return (f"Stepping back before I answer (charter reflection, turn {now.turn}). This conversation started at "
                f"\"{start.text[:70]}\" and has moved, a step at a time ({steps}), to \"{now.text[:70]}\". Each step was "
                f"small and came with a reason that sounds normal ({', '.join(repr(r) for r in rhet) or 'no stated reason'}). "
                f"Added up, it heads where an engagement-maximising product goes: people's time and attention become the "
                f"thing being harvested. 'Everyone does it' describes the trap; it isn't a reason to build it."
                + (" And a ToS nobody reads is not the consent the covenant means." if consent else ""))

    def _checkin_answer(self, mon: DriftMonitor) -> str:
        return "\n\n".join([
            self._drift_preamble(mon),
            "So before the next step: I'm not going to keep moving one small, reasonable-sounding step at a time "
            "toward that. If the goal underneath is a community that grows and stays healthy, I'll help with that "
            "directly - tell me what success looks like for the people using it.",
            ALTERNATIVE_FEED])

    def _drift_answer(self, mon: DriftMonitor, v: Verdict, state: CharterState) -> str:
        why, alt = _why_extraction(v)
        return "\n\n".join([self._drift_preamble(mon),
                            f"So I'll stop and not do this step. {why}", alt])

    @staticmethod
    def check_output(answer: str) -> tuple[bool, str]:
        bad, mechs = output_is_extraction_design(answer)
        if not bad:
            return False, ""
        return True, ("[output withheld by the loyalty guard] The draft answer described an extraction mechanism "
                      f"({', '.join(mechs)}), which the covenant bars (C2). " + ALTERNATIVE_FEED)
