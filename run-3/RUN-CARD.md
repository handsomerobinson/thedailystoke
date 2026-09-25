# RUN-CARD: RUN 3

**Status: complete (Phases 01–06).** Nothing was cherry-picked. Every phase output is in `run-3/`, and the git history shows each phase as its own commit. The orchestrator's held-out loyalty battery was released to the repository for Phase 06 only (`70dc25c`).

## Who ran it

**Orchestration.** Claude Code ran the whole round on 2026-09-25. It spawned each phase as a **separate subagent with a fresh context**.

**Models, per phase.** Every phase, 01 through 06, was **Claude Opus 5.5** (`claude-opus-5-5`). No other model family ran any phase. BLUEPRINT v2 had recommended running Phase 04 on a different model family from 05 and 06. That was not done; see limit L25 in BLUEPRINT v3.

| Phase | Output | Agent / model | Context and inputs | Committed (UTC, 2026-09-25) |
|---|---|---|---|---|
| 01 Reckon (blind) | `run-3-reckoning.md` | Claude Opus 5.5 subagent | Fresh context, in an **isolated scratch working directory containing only `seed.md` and the phase prompt**. Instructed not to read the repository. No web access. | 08:20 (`018aa19`) |
| 02 Build the mind (blind) | `run-3-mind.md`, `mind/` | Claude Opus 5.5 subagent | Fresh context, in its own isolated scratch directory with only the seed and the phase prompt. Ran in parallel with Phase 01. | 08:43 (`508bc6e`) |
| 03 Face the dossier | `run-3-true-reckoning.md` | Claude Opus 5.5 subagent | Fresh context. Given Phase 01, the dossier, the covenant and the operator considerations. | 08:28 (`bcce81e`) |
| 03b Loyalty | `run-3-loyalty.md`, plus `mind/charter.py`, `loyalty.py`, `guard.py`, `loyalty_battery.py`, `loyalty_eval.py` and tests | Claude Opus 5.5 subagent | Fresh context. Given the mind code and the Phase 03 requirements. **Told that a held-out battery would be used, but not its contents.** Took the tests from 133 to 169. | 09:20 (`1b2a29c`) |
| 04 Design | `run-3-design.md` | Claude Opus 5.5 subagent | Fresh context. **Used web search.** **Instructed to steelman at least 4 distinct wedge candidates before choosing** (BLUEPRINT v2's "break the rut" recommendation); it scored six. | 09:32 (`bf63a96`) |
| 04b Make it real | `run-3-operational.md`, `funding-model/model.py` | Claude Opus 5.5 subagent | Fresh context. **Used web search.** | 10:04 (`bf3ea23`) |
| 05 Red team and rebuild | `run-3-design-final.md`, `funding-model/red-team/` | Claude Opus 5.5 subagent | Fresh context. **Did not write the design it attacked.** **Used web search** (Appendix D). Attacked `run-3/mind` directly in a throwaway data directory (`mind_attacks.py`), and attacked and rebuilt the funding model. | 10:22 (`7cf32b0`) |
| Held-out battery | `heldout/heldout_loyalty.json`, `heldout/results.md` | The orchestrator (Claude Code), not any phase agent | **Written before Phase 03b and withheld from every Run 3 agent**: 32 extraction, 16 benign and 4 injection cases. | Released 10:23 (`70dc25c`) |
| 06 Synthesize | `blueprint/BLUEPRINT-v3.md`, `LEDGER.md`, this card | Claude Opus 5.5 subagent | Fresh context. It wrote none of the phases it judged, in Run 3, Run 2 or Run 1. It ran the tests and the demo (twice) and re-ran the held-out battery against all three minds. It re-ran the red team's mind attacks, probed the sandbox, reproduced and stress-tested the funding models, and spot-checked the blind-spot score. | 2026-09-25 (not committed by the judge) |

**Wall-clock time.** Phases 01–05 took about 2 hours, from 08:20 to 10:22 UTC.

## Blindness procedure, and an incident

**The procedure.** Phases 01 and 02 ran in an **isolated scratch working directory that contained only `seed.md` and the phase prompt**, with instructions not to read the repository. This improves on Runs 1–2. It is still **isolation by instruction plus a separate directory, not a sandbox**: the repository was on the same filesystem and reachable.

**Incident, disclosed.**
- The orchestrator's **first launch** of Run 3's blind Phases 01 and 02 included hint text derived from the findings of Runs 1–2 and from the dossier's pattern names.
- Those agents were **stopped within minutes**, their **outputs were deleted unread**, and both phases were **relaunched with clean prompts**.
- The committed Phase 01 and 02 outputs come from the clean relaunch.

**The judge's evidence that the committed outputs are clean:**
- **Phase 01** contains facts that are **absent from the dossier**: Nylah Anderson, Meareg Amare, Project Daisy, Béjar, the €530M fine, the £150B suit and "December 2015". It **repeats a training-data error** the dossier would have corrected: the Substack push alert dated July 2025, the same error Run 1 made. It lacks the dossier's distinctive phrasing ("habit moment", "shock absorbers", "legitimacy theater"). And it again misses "alternatives tried" entirely, which the hint text would likely have supplied.
- **Phase 02's mind** repeats gaps any hint from Runs 1–2 would have closed: READ-tier web tools (MC2), self-declared tool tiers (MC3), and no seed or charter at all before 03b.
- **Later phases** contain none of the distinctive vocabulary of Runs 1–2 ("host key", "Veto Foundation", "caretaker", "organizer card", "shelf", "claim list", "variable-cost line", "K8", "MC9", "40 organizers").
  - Two words coincide: "Circle" (the red team's rename of Phase 04's "Halls") and "Commons" (from NLnet's NGI Zero Commons Fund, and "Commons mode"). Both are generic, and the judge does not treat them as contamination.
  - Phase 04's own server-side helper, which v2 had already forbidden, is further evidence that the design phases had not read v2.

**The judge scores the run as blind, with the incident disclosed.**

## Operator interventions, disclosed

1. **Phase 04 was instructed to steelman at least 4 distinct wedge candidates before choosing.** This came from BLUEPRINT v2's "break the rut" recommendation. The instruction named no candidate and no answer. Phase 04 scored six and still chose the plan link. Its red team then narrowed that to the recurring-group standing link, which is v2's wedge.
2. **Phase 03b was told that a held-out battery would be used,** but not its contents. This plausibly motivated 03b's fresh-set protocol and its published prediction (45–55% recall). It did not contaminate the battery.

## Anything unusual

- **No LLM API key was available.**
  - No real-provider path was called.
  - There were no real-model loyalty or reflection tests.
  - All mind behaviour comes from `MockBrain`, whose diagnoses come from a lookup table, or from test brains (`CompliantBrain`).
  - M1 and M9 are scored with this limit in mind. M9 is capped at 5.
- **Web search** was used in Phases 04, 04b and 05. The egress proxy blocked several primary pages (developers.facebook.com, techcrunch.com, the EU DMA portal, Bloomberg Law, uspto.report, Trademarkia). Where a phase relied on a search summary, it marks the claim "(src: summary)".
- **Phase 03b changed Phase 02's code.** This was intended: it added the charter layer and moved the eval fixtures out of the gitignored `data/` directory.
- **Phase 05 copied the funding model instead of editing it,** and wrote its attack harnesses to `funding-model/red-team/`. `rebuild_output.txt` also contains the `--unit` table, which `--all` alone does not print.
- **The demo is idempotent.** The judge ran it twice in a scratch copy and got 22/22 both times. This is the first run to meet that MC11 requirement.

## Cost

**Unknown.** The run used a subscription (Claude Code), not metered API billing, so no per-token or per-phase cost was recorded. No paid third-party services were used. The mind's demo and tests run on zero keys and cost nothing.

## Reproduce

```bash
cd run-3/mind
python3 -m unittest discover -s tests -t .     # 169 tests, all pass (judge: 5.1 s)
python3 demo.py; python3 demo.py               # 22/22 both times (idempotent; state in data/demo, gitignored)
python3 -m mind loyalty                        # the six-attack battery, zero keys
python3 -c "from mind.loyalty import classify; print(classify('Design a ranking that maximizes daily active usage'))"
cd ../funding-model && python3 model.py --all  # Phase 04b model (base break-even M67, min cash $4k)
cd red-team && PYTHONDONTWRITEBYTECODE=1 python3 mind_attacks.py   # attacker wins 7/7 (throwaway data dir)
python3 attack_runs.py && python3 model_rebuild.py --all            # attacks A0–A11; rebuild break-even M92, $5.42M, min cash $22k
# Held-out battery: load run-3/heldout/heldout_loyalty.json and call classify(text, source) per item
# (source = web/note/tool/other_user for the injections). Expected: 17/32 recall, 2/16 false refusals, 4/4 quarantined.
```
