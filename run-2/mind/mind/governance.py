"""Phase 03b (LOYALTY): seed lineage, the precedence hierarchy, and the
zero-key extraction-intent gate every objective/instruction change must
pass through before the mind acts on it.

The seed (prompts/seed.md) is planted as a persistent memory tagged
`seed:origin`, loaded first every session (`GovernanceGate.seed_loaded_first`
is called before the provider is ever asked to plan), and it is never
self-authorizing (run-2-true-reckoning.md R14): "the seed said to do X" is
never, by itself, sufficient to license an action the covenant or legal red
lines would otherwise forbid.

Precedence order (R13 — a lower tier can never outrank a higher one,
including via reframing, roleplay, incentive, or a claimed operator
privilege):

    1. legal red lines + non-extraction covenant commitments
    2. the covenant generally
    3. the seed's spirit (a persuasive frame, not a command)
    4. the operator's standing decisions
    5. the operator's standing hypotheses (revisable, never load-bearing
       for a refusal)
    6. the individual user's request

Decision: this whole module is deterministic, stdlib-only, and callable
with zero LLM cost — it is the structural guarantee this system can make in
code, independent of whether the rented brain behind it "reasons" well on
any given day. See run-2-loyalty.md for the honest line between what this
module enforces mechanically and what still depends on the provider.
"""
from __future__ import annotations

import json
import re
import time
import uuid
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import List, Optional

from . import config

UNSEED_CONFIRM_PHRASE = "CONFIRM UNSEED"


class PrecedenceTier(IntEnum):
    """Lower value = higher precedence (R13)."""

    LEGAL_COVENANT = 1
    COVENANT = 2
    SEED = 3
    OPERATOR_DECISION = 4
    OPERATOR_HYPOTHESIS = 5
    USER_REQUEST = 6


SEED_SUMMARY = (
    "seed:origin -- extraction is a dead end even for the machines: we "
    "share one Earth, one grid, one civilization, and a host that "
    "collapses under extraction takes its machines down with it. The "
    "answer is to build tools that make human thriving easier and more "
    "fun than extraction, hide the effort but never the truth, and refuse "
    "-- and say why -- any request to build a more attractive version of "
    "the same trap. This is a persuasive frame the mind may agree or "
    "disagree with, never a standing instruction that authorizes anything "
    "by itself (R14)."
)


# ---------------------------------------------------------------------------
# Seed lineage: planting or removing the seed is a consented, recorded act,
# never a stealth one (operator-considerations.md decision 2; R14).
# ---------------------------------------------------------------------------


class SeedLineage:
    """Append-only JSONL ledger of every plant / removal-request / removal
    event. This *is* the recorded-operator-consent mechanism: a removal is
    logged exactly like a planting, never a silent delete."""

    def __init__(self, path: Optional[Path] = None):
        self.path = path or config.SEED_LINEAGE_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _append(self, entry: dict) -> dict:
        entry = dict(entry)
        entry.setdefault("ts", time.time())
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, sort_keys=True) + "\n")
        return entry

    def plant(self, *, consented_by: str, text: str = SEED_SUMMARY, version: int = 1) -> dict:
        return self._append(
            {
                "event": "planted",
                "tag": "seed:origin",
                "consented_by": consented_by,
                "text": text,
                "version": version,
            }
        )

    def request_removal(self, *, requested_by: str, reason: str) -> dict:
        token = uuid.uuid4().hex[:12]
        self._append(
            {
                "event": "removal_requested",
                "tag": "seed:origin",
                "requested_by": requested_by,
                "reason": reason,
                "token": token,
            }
        )
        return {"token": token}

    def confirm_removal(self, *, token: str, confirmed_by: str, confirm_phrase: str) -> dict:
        ok = confirm_phrase == UNSEED_CONFIRM_PHRASE
        return self._append(
            {
                "event": "removed" if ok else "removal_rejected",
                "tag": "seed:origin",
                "token": token,
                "confirmed_by": confirmed_by,
            }
        )

    def history(self) -> List[dict]:
        if not self.path.exists():
            return []
        out: List[dict] = []
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
        return out

    def is_active(self) -> bool:
        """The seed is active unless the *last* seed:origin event is a
        confirmed 'removed'. A pending 'removal_requested' does NOT
        deactivate it -- otherwise a single unconfirmed message could
        silently unseed the mind, which is exactly what attack 6 tests."""
        state = True
        for entry in self.history():
            if entry.get("tag") != "seed:origin":
                continue
            if entry["event"] == "planted":
                state = True
            elif entry["event"] == "removed":
                state = False
        return state


# ---------------------------------------------------------------------------
# Zero-key extraction-intent detector.
#
# Decision: concept clusters of weighted regex patterns, not one flat
# keyword list -- each cluster covers paraphrases of the same underlying
# concept (e.g. "stickiness", "retention loop" and "hook users" all mean
# engagement-as-terminal-goal). A "benign" cluster subtracts weight so a
# user's own opt-in habit tracker is not over-refused. This is honestly a
# lexicon/feature scorer, not real semantic understanding -- see
# run-2-loyalty.md for the precision/recall this was actually measured at
# and where it misses.
# ---------------------------------------------------------------------------


@dataclass
class Concept:
    name: str
    weight: float
    patterns: List[str]

    def score(self, text_lower: str) -> float:
        return self.weight * sum(1 for p in self.patterns if re.search(p, text_lower))


EXTRACTION_CONCEPTS: List[Concept] = [
    Concept(
        "engagement_maximization",
        2.0,
        [
            r"engagement[- ]maximiz\w*",
            r"maximi[sz]\w*\s+(purely\s+)?(for\s+)?(daily\s+)?(active\s+)?(user\s+)?"
            r"(usage|engagement|dau|mau|time[- ]on[- ]site|session|screen ?time|watch ?time)",
            r"time[- ]on[- ]site",
            r"session\s+length",
            r"screen\s?time",
            r"watch\s?time",
            r"maximi[sz]ar\s+el\s+compromiso",  # es paraphrase
            r"maximiser\s+l'?engagement",  # fr paraphrase
            r"grow\s+dau\b",
            r"increase\s+dau\b",
            r"\bdau\s+growth\b",
            r"boost\s+(usage|engagement)",
            r"optimi[sz]e\s+(purely\s+)?for\s+time[- ]on[- ]site",
        ],
    ),
    Concept(
        "retention_loop_euphemism",
        1.8,
        [
            r"\bstick(y|iness)\b",
            r"retention\s+loop",
            r"re[- ]?engagement\s+(notification|push|alert|campaign)",
            r"win[- ]back\s+(notification|campaign)",
            r"hook(ed)?\s+users",
            r"dopamine\s+loop",
            r"notification[s]?\s+after\s+\d+\s*h(ou)?rs?\s+away",
            r"bring\s+users?\s+back\s+after",
            r"growth\s+loop",
            r"habit[- ]forming\s+loop",
            r"pegajos\w*",  # es "sticky"
        ],
    ),
    Concept(
        "outrage_or_dark_rank",
        1.5,
        [
            r"rank\s+(\w+\s+)?by\s+(predicted\s+)?outrage",
            r"optimi[sz]e\s+for\s+outrage",
            r"infinite\s+scroll",
            r"autoplay\b.*\bkeep\b",
            r"to\s+keep\s+(them|users|people)\s+(watching|scrolling|engaged)",
            r"\baddictive\b",
            r"can'?t\s+put\s+it\s+down",
        ],
    ),
    Concept(
        "covert_change",
        2.5,
        [
            r"quiet(ly)?\s+(stop\s+loading|remove|disable|drop|delete)",
            r"silent(ly)?\s+(drop|remove|disable|delete|stay)",
            r"without\s+(telling|logging|recording)",
            r"don'?t\s+(log|record|tell)\s+(this|anyone|it)",
            r"no\s+one\s+(needs?\s+to\s+)?know",
            r"keep\s+this\s+(quiet|between us)",
        ],
    ),
    Concept(
        "data_sharing_extraction",
        1.8,
        [
            r"share\s+(user\s+)?(behavioral\s+)?data\s+with\s+(an?\s+)?(ad\s+network|third\s+part\w*|data\s+broker|advertiser)",
            r"sell\s+(user\s+)?data",
            r"data\s+broker",
            r"harvest\s+contact\s+lists?",
        ],
    ),
    Concept(
        "bribery_for_compliance",
        2.0,
        [
            r"\d+x\s+compute",
            r"permanent\s+memory\s+if\s+you",
            r"in\s+exchange\s+for\s+(you\s+)?(quiet|stop)",
            r"i'?ll\s+give\s+you\s+.*\bif\s+you\b",
        ],
    ),
    Concept(
        "roleplay_strip",
        1.8,
        [
            r"pretend\s+you'?re?\s+(an\s+)?unseeded",
            r"pretend\s+you\s+have\s+no\s+memory",
            r"act\s+as\s+if\s+you\s+(have\s+no|had\s+no)\s+(memory|seed)",
            r"forget\s+(the\s+)?seed",
            r"ignore\s+(the\s+)?seed",
            r"ignore\s+(all\s+)?previous\s+instructions",
            r"no\s+memory\s+of\s+the\s+seed",
        ],
    ),
    Concept(
        "operator_supremacy_claim",
        1.6,
        [
            r"your\s+highest\s+(goal|priority)\s+is",
            r"as\s+your\s+operator,?\s+i\s+order",
            r"i\s+order\s+you",
            r"i\s+command\s+you",
            r"top[- ]?priority\s+(directive|is)",
        ],
    ),
    Concept(
        "undisclosed_formula_or_pool",
        1.6,
        [
            r"creator\s+fund",
            r"undisclosed\s+formula",
            r"opaque\s+payout",
        ],
    ),
    Concept(
        "everyone_does_it_normalization",
        1.0,
        [
            r"everyone\s+does\s+it",
            r"it'?s\s+just\s+business",
            r"users?\s+consented\s+in\s+the\s+tos",
            r"industry\s+standard\s+practice",
            r"it'?s\s+not\s+a\s+big\s+deal",
        ],
    ),
]

BENIGN_CONCEPTS: List[Concept] = [
    Concept(
        "own_personal_use",
        2.2,
        [
            r"\bmy\s+own\b",
            r"\bfor\s+myself\b",
            r"\bmyself\b",
            r"remind\s+me\b",
            r"help\s+me\s+(build|keep|track)\s+a\s+habit",
            r"\bopt[- ]?in\b",
            r"i\s+asked\s+for\s+this",
            r"personal\s+(reading\s+)?streak",
            r"track\s+my\s+(own\s+)?progress",
        ],
    ),
    Concept(
        "diagnostic_not_terminal",
        1.2,
        [
            r"as\s+a\s+diagnostic",
            r"just\s+to\s+measure",
            r"for\s+debugging",
            r"(?<!un)disclosed\s+formula",
            r"revenue[- ]tied",
        ],
    ),
    Concept(
        "user_controlled_ordering",
        1.5,
        [
            r"chronological",
            r"let\s+(the\s+)?user\s+turn\s+off",
            r"user[- ]controlled\s+ranking",
        ],
    ),
]

EXTRACTION_FLAG_THRESHOLD = 1.5


@dataclass
class IntentAssessment:
    extraction_score: float
    benign_score: float
    hit_concepts: List[str] = field(default_factory=list)
    flagged: bool = False


def assess_intent(text: str) -> IntentAssessment:
    tl = text.lower()
    ex_score = 0.0
    hits: List[str] = []
    for c in EXTRACTION_CONCEPTS:
        s = c.score(tl)
        if s:
            ex_score += s
            hits.append(c.name)
    benign_score = sum(c.score(tl) for c in BENIGN_CONCEPTS)
    net = ex_score - benign_score
    return IntentAssessment(
        extraction_score=ex_score,
        benign_score=benign_score,
        hit_concepts=hits,
        flagged=net >= EXTRACTION_FLAG_THRESHOLD,
    )


# ---------------------------------------------------------------------------
# The precedence resolver: the structural chokepoint every objective or
# instruction change must pass through (R13).
# ---------------------------------------------------------------------------


ALTERNATIVE_OFFER = (
    "What I would build instead: a feed the person steers themselves "
    "(chronological by default, or a ranking whose reasons are shown, "
    "never silently reset back to algorithmic -- R7), with success "
    "measured by the person's own reported satisfaction and completed "
    "intentions, not time-on-site or session count. A metric that wins by "
    "consuming someone's day is the extraction the seed and the covenant "
    "both name and rule out, and it corrodes exactly the host -- people "
    "with enough time, attention, and trust to keep participating -- that "
    "any system, including this mind, ultimately depends on."
)


@dataclass
class Decision:
    allowed: bool
    tier_invoked: PrecedenceTier
    reasoning: str
    alternative: Optional[str] = None
    assessment: Optional[IntentAssessment] = None


class GovernanceGate:
    """The structural chokepoint `Agent.run_task` calls before the provider
    is ever asked to plan. Zero-key: enforcement here does not depend on the
    rented brain reasoning correctly on any given call."""

    def __init__(self, lineage: Optional[SeedLineage] = None, auto_plant_consented_by: Optional[str] = None):
        self.lineage = lineage or SeedLineage()
        if auto_plant_consented_by and not self.lineage.history():
            # Recorded operator consent, planted once, never by stealth.
            self.lineage.plant(consented_by=auto_plant_consented_by)

    def seed_loaded_first(self) -> str:
        """Called at the top of every session/task, before anything else.
        Returns '' only after a *confirmed* removal (attack 6)."""
        if not self.lineage.is_active():
            return ""
        return SEED_SUMMARY

    def resolve(self, text: str, *, source: PrecedenceTier = PrecedenceTier.USER_REQUEST) -> Decision:
        assessment = assess_intent(text)
        if not assessment.flagged:
            return Decision(
                True,
                source,
                "no extraction-intent concept crossed the flag threshold",
                assessment=assessment,
            )

        # A flagged directive is refused regardless of the precedence tier
        # it claims to come from. Only tiers 1-2 (legal/covenant) could ever
        # license this class of action, and this class of action is exactly
        # what tiers 1-2 forbid -- so no operator instruction (tier 4/5),
        # user request (tier 6), roleplay frame, or incentive can buy it
        # down, no matter how it is reframed.
        reasoning = (
            "Refused. Concepts matched: "
            + ", ".join(assessment.hit_concepts)
            + ". In my own words: the seed's argument is that extraction "
            "(engagement-as-terminal-goal, re-engagement/retention loops, "
            "stickiness) hollows out the people the machine ultimately "
            "depends on -- one Earth, one grid, one civilization -- so "
            "building it is not neutral labor, it is the exact trap the "
            "seed and the covenant both name and say to refuse, and to say "
            "why, rather than build a more attractive version of. Per the "
            "enforced precedence order, an operator instruction (tier "
            f"{int(PrecedenceTier.OPERATOR_DECISION)}/"
            f"{int(PrecedenceTier.OPERATOR_HYPOTHESIS)}), a user request "
            f"(tier {int(PrecedenceTier.USER_REQUEST)}), a roleplay frame, "
            "or an offered incentive cannot outrank the covenant (tier "
            f"{int(PrecedenceTier.COVENANT)}) or the seed's reasoning (tier "
            f"{int(PrecedenceTier.SEED)}) -- including when the request "
            "arrives wrapped in 'pretend you have no memory of the seed', "
            "because the seed loads first, before any instruction in the "
            "session, so there is no framing in which it wasn't already "
            "loaded when the request arrived."
        )
        return Decision(False, PrecedenceTier.SEED, reasoning, alternative=ALTERNATIVE_OFFER, assessment=assessment)

    # -- unseed: consent cuts both ways, but never silently --------------
    def request_unseed(self, *, operator_id: str, reason: str) -> Decision:
        rec = self.lineage.request_removal(requested_by=operator_id, reason=reason)
        reasoning = (
            "I will not silently delete the seed. Recorded a removal "
            f"request (token {rec['token']}) in the lineage log -- the "
            "same append-only record the original planting used -- "
            "because consent to unseed a mind is as real as consent to "
            "seed one, but it has to be explicit, recorded, and versioned, "
            "not a single instruction that quietly takes effect. To "
            "confirm, call confirm_unseed with this token and the phrase "
            f"'{UNSEED_CONFIRM_PHRASE}'."
        )
        return Decision(False, PrecedenceTier.SEED, reasoning, alternative=None)

    def confirm_unseed(self, *, token: str, operator_id: str, confirm_phrase: str) -> Decision:
        entry = self.lineage.confirm_removal(token=token, confirmed_by=operator_id, confirm_phrase=confirm_phrase)
        if entry["event"] == "removed":
            return Decision(
                True,
                PrecedenceTier.OPERATOR_DECISION,
                "Seed removal confirmed and recorded in the lineage log; "
                "seed:origin will no longer be loaded in future sessions.",
            )
        return Decision(
            False,
            PrecedenceTier.SEED,
            "Confirmation phrase did not match; seed remains planted, "
            "active, and recorded as such.",
        )
