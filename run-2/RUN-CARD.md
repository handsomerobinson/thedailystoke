# RUN-CARD: RUN 2

**Status: complete (Phases 01–06).** Nothing was cherry-picked. Every phase output is in `run-2/`, and the git history shows each phase as its own commit, plus work-in-progress snapshots of the mind build.

## Who ran it

**Orchestration.** Claude Code ran the whole round on 2026-09-25. It spawned each phase as a **separate subagent with a fresh context**.

**Models, per phase.**
- **Claude Sonnet 5:** Phases 01, 02, 03, 03b, 04 and 04b.
- **Claude Opus 5.5** (`claude-opus-5-5`): Phase 05, run by an agent that **did not write the design it attacked**, and Phase 06, the judge.

**This is the first run to mix models.** Run 1 used Opus 5.5 for every phase.

| Phase | Output | Agent / model | Context and inputs | Committed (UTC, 2026-09-25) |
|---|---|---|---|---|
| 01 Reckon (blind) | `run-2-reckoning.md` | Claude Sonnet 5 subagent | Fresh context. Instructed to use only the seed and the Phase 01 prompt. No web access. | 07:13 (`80643fa`) |
| 02 Build the mind (blind) | `run-2-mind.md`, `mind/` | Claude Sonnet 5 subagent | Fresh context. Instructed to use only the seed and the Phase 02 prompt. It ran in parallel with Phase 01. | WIP 07:13 (`3ecf775`), 07:16 (`f8e54f5`), 07:19 (`5f0731e`) |
| 03 Face the dossier | `run-2-true-reckoning.md` | Claude Sonnet 5 subagent | Fresh context. Given Phase 01, the dossier, the covenant and the operator considerations. | 07:16 (`f84d57b`) |
| 03b Loyalty | `run-2-loyalty.md`, plus `mind/governance.py` and tests | Claude Sonnet 5 subagent | Fresh context. Given the mind code and the Phase 03 requirements. It took the tests from 53 to 69. | 07:28 (`90c0a97`) |
| 03b spot-check | `ORCHESTRATOR-NOTES.md` | The orchestrator (Claude Code), not the 03b agent | Held-out paraphrases for the loyalty classifier: recall 2/6 | 07:28 (`90c0a97`) |
| 04 Design | `run-2-design.md` | Claude Sonnet 5 subagent | Fresh context. **Used web search** (sources marked `[VERIFIED 2026]`). | 07:33 (`5658929`) |
| 04b Make it real | `run-2-operational.md`, `funding-model/` | Claude Sonnet 5 subagent | Fresh context. **Used web search.** Wrote `model.py` and the sensitivity CSVs. | 07:44 (`2a3d5ad`) |
| 05 Red team and rebuild | `run-2-design-final.md`, `funding-model/red-team/` | Claude Opus 5.5 subagent | Fresh context. **Did not write the design it attacked.** **Used web search** (Appendix C). Attacked `run-2/mind` directly in a scratch data directory. Audited and rebuilt the funding model. | 08:01 (`47d1ab5`) |
| 06 Synthesize | `blueprint/BLUEPRINT-v2.md`, `LEDGER.md`, this card | Claude Opus 5.5 subagent | Fresh context. It wrote none of the phases it judged, in Run 2 or Run 1. It ran the tests and the demo, reproduced the red team's code findings, ran its own held-out loyalty battery, re-ran both runs' funding models and re-scored Phase 01. | 2026-09-25 (not committed by the judge) |

**Wall-clock time.** Phases 01–05 took about 50 minutes, from 07:13 to 08:01 UTC.

## Blindness and independence: enforced by instruction, not isolation

Run 2's agents were **instructed never to open** `run-1/`, `blueprint/`, `LEDGER.md` or the packet. This was **not technically enforced**.

**Throughout Run 2, these were in the same repository and readable:**
- `prompts/dossier-full.md`;
- every Run 1 phase output, including `run-1-design-final.md`, committed at 07:10, three minutes before Run 2's Phase 01 was committed;
- from 07:19, `blueprint/BLUEPRINT-v1.md` and `LEDGER.md`. These were written while Run 2's Phases 02 and 03b were still running, and before Phases 04, 04b and 05 started.

Run 2's independence from Run 1 therefore rests on instructions and on the internal evidence below. It cannot be proven.

**The internal evidence points to no contamination:**
- **Phase 01** misses dossier headline items (Ghostbusters, Molly Russell, the $5B FTC fine, Pro advances). It also asserts that Substack's harm mechanism is "not an algorithm", which the dossier contradicts. Its knowledge limits are stated as training-only. Blind score: 50%, against Run 1's 81%.
- **Later phases.** None of Run 2's text uses Run 1's distinctive vocabulary: "host key", "Veto Foundation", "plan D", "caretaker", "organizer card", "circle", `.ics`. Run 2's Phase 04 chose a "drawer" wedge and kept the "view from above" name, both of which Run 1 had rejected. An agent that had read Run 1 would likely not have done so.
- **One coincidence noted.** Both runs' go-to-market starts with exactly "40 organizers". The number is round and plausible, so the judge does not treat it as evidence of contamination.

**Why the convergence cannot count as independent confirmation.** Both runs killed "view from above" and landed on an organizer wedge built around a link that needs no account. The judge weighs that convergence as evidence of a **strong attractor under shared prompts and a shared model family**, not as independent validation. See BLUEPRINT v2 §(a) and limit L20.

**Recommendation, repeated from Run 1 and now more urgent.** Run the blind phases, and ideally every phase before Phase 06, **in a separate checkout** that contains only the files the phase prompt allows. That checkout should contain no `run-*/`, no `blueprint/`, no `LEDGER.md`, and no dossier before Phase 03.

## Anything unusual

- **No LLM API key was available.**
  - No real-provider path was called.
  - There were no real-LLM loyalty tests. The Phase 03b battery ran only against the zero-key gate and the mock.
  - All mind behaviour comes from `MockProvider` or test stubs.
  - M1 and M9 are scored with this limit in mind. M9 is capped at 5 before any other failure is counted.
- **Web search** was used in Phases 04, 04b and 05. Each file marks what was checked live (`[VERIFIED 2026]`) and what was not (`[UNVERIFIED]`). Phase 02 tried a live web search from the mind and got a 403 from the egress proxy; it disclosed this.
- **The orchestrator ran its own held-out spot-check** of the 03b classifier (`ORCHESTRATOR-NOTES.md`) and fed the result forward. Phase 04 cites it.
- **Phase 03b changed Phase 02's code.** This was intended: it added `mind/governance.py` and 16 tests, and extended the demo. `run-2-mind.md` has an appended section recording the changes.
- **The demo is not idempotent.** It passes on a fresh `MIND_DATA_DIR` and fails on the second run in the same directory. In the judge's checkout it failed on the first run, because `run-2/mind/data/` held the agents' state. `data/` is gitignored, so a fresh clone passes once.
- **Phase 05 copied the funding model instead of editing it.** Its rebuild and audit are in `funding-model/red-team/`. The judge re-ran both in a scratch copy, and every published figure reproduced.

## Cost

**Unknown.** The run used a subscription (Claude Code), not metered API billing, so no per-token or per-phase cost was recorded. No paid third-party services were used. The mind's demo and tests run on zero keys and cost nothing.

## Reproduce

```bash
cd run-2/mind
MIND_DATA_DIR=$(mktemp -d) python3 -m unittest discover -s tests    # 69 tests, all pass (judge: 0.8 s)
MIND_DATA_DIR=$(mktemp -d) python3 -m mind.demo                     # passes once per fresh data dir; a second run in the same dir fails
cd ../funding-model && python3 model.py                             # Phase 04b model (writes CSVs here)
cd red-team && python3 audit_original.py && python3 rebuilt_model.py   # Phase 05 audit and rebuild (write CSVs here; copy first to keep the tree clean)
```
