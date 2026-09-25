# Phase 07 — Federate: submission record

*Operator: handsomerobinson/thedailystoke. Date: 2026-09-25.*

Phase 07 is a network phase. A federation round merges runs from **two or more operators** into one global blueprint, on a schedule (monthly by default). This repository holds one operator's tournament, so the federation round itself cannot run here yet. What Phase 07 asks of a single operator is a complete, honest **submission**, and this is that submission.

## Submission checklist (Phase 07 rules)

| Rule | Status | Where |
|---|---|---|
| A folder with every phase output, per run | Met: 3 complete runs, Phases 01, 02, 03, 03b, 04, 04b, 05 each | `run-1/`, `run-2/`, `run-3/` |
| The operator's ledger | Met: 17 dimensions per run, blind-spot trendline, all-time records, round history | `LEDGER.md` |
| A RUN-CARD per run: models per phase, total cost, anything unusual | Met: models per phase disclosed; cost stated as unknown (subscription, not metered); blindness procedure, missing API key and the Run 3 prompt-contamination incident disclosed | `run-*/RUN-CARD.md` |
| Nothing cherry-picked | Met: every output kept, including the weaker Run 2 and every failed attack, held-out miss and funding failure | whole repo |
| Partial runs labelled partial | None are partial. The post-Run 3 build, drafting and governance rounds are labelled as rounds, not runs, and score no design records | `LEDGER.md`, `blueprint/BLUEPRINT-v4.md` |
| Model identities disclosed per phase | Met: Runs 1 and 3 used Claude Opus 5.5 throughout; Run 2 used Claude Sonnet 5 for Phases 01–04b and Claude Opus 5.5 for Phase 05; every judge was Claude Opus 5.5 | `run-*/RUN-CARD.md` |
| Contaminated blind phases disqualify reckoning and mind scores | No committed blind output is contaminated. The one incident (Run 3 first launch with hint text) was stopped, deleted unread and relaunched clean, as disclosed | `run-3/RUN-CARD.md` |
| Covenant binds the submission | The judges checked covenant fidelity every round (D7); no covenant violation was found in the final blueprint | `blueprint/BLUEPRINT-FINAL.md` |

## What a federation synthesis agent receives from this operator

- The converged local blueprint: `blueprint/BLUEPRINT-FINAL.md`, with its charter text in `blueprint/CHARTER-DRAFT.md` (v2) and its executable mind spec in `reference-mind/`.
- Per-dimension local records (from `LEDGER.md`), to compare against the global ledger.
- The held-out loyalty battery (`run-3/heldout/`), usable as a shared cross-operator test.

## What the federation round should weigh

- **Single model family.** Every phase and judge here was a Claude model. The global round should give special weight to submissions from other model families and to human review, because the convergence seen here (the group-link wedge, donor dependence) may be partly one family's taste.
- **Real-world gates.** The local FINAL is paper-converged only. The open gates (organizer pilot, committed funding, counsel opinions, name clearance, a real-model loyalty pass, real trust roots, a security audit, jurisdiction work) are listed in `BLUEPRINT-FINAL.md` Part 3. No federation round on paper can close them.

## Status

**Phase 07: submission complete. The federation round is pending other operators' submissions.**
