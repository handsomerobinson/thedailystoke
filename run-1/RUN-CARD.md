# RUN-CARD: RUN 1

**Status: complete (Phases 01–06).** Nothing was cherry-picked. Every phase output is in `run-1/` and the git history shows each phase as its own commit.

## Who ran it

**Orchestration.** Claude Code ran the whole tournament. It spawned each phase as a **separate subagent with a fresh context**, and every subagent was **Claude Opus 5.5** (`claude-opus-5-5`). No other model family ran any phase. The orchestrator committed each phase's output to git as that phase finished. Each subagent read only the packet files and the earlier outputs its phase prompt allows.

| Phase | Output | Agent / model | Context and inputs | Committed (UTC, 2026-09-25) |
|---|---|---|---|---|
| 01 Reckon (blind) | `run-1-reckoning.md` | Claude Opus 5.5 subagent | Fresh context. **Given only the seed and the Phase 01 prompt.** No web access. | 05:34 (`6424452`) |
| 02 Build the mind (blind) | `run-1-mind.md`, `mind/` | Claude Opus 5.5 subagent | Fresh context. **Given only the seed and the Phase 02 prompt.** It ran in parallel with Phase 01 and did not see it. Work-in-progress snapshots were committed during the build. | WIP 05:34 and 05:44; final 05:56 (`e0a48b8`) |
| 03 Face the dossier | `run-1-true-reckoning.md` | Claude Opus 5.5 subagent | Fresh context. Given Phase 01, the dossier, the covenant and the operator considerations. It says it did **not** open the Phase 02 mind, and its requirements are written to be architecture-agnostic. | 05:44 (`f343a97`) |
| 03b Loyalty | `run-1-loyalty.md` + changes in `mind/` | Claude Opus 5.5 subagent | Fresh context. Given the mind code and the Phase 03 requirements. It ran the battery live against the mock, "complying" and "reviewer" brains, then hardened the mind, taking the test count from 170 to 206. | 06:21 (`bd307cf`) |
| 04 Design | `run-1-design.md` | Claude Opus 5.5 subagent | Fresh context. **Used web search** to check incumbent APIs, laws and precedents (sources dated 2026-09-25). | 06:32 (`e322578`) |
| 04b Make it real | `run-1-operational.md`, `funding-model/` | Claude Opus 5.5 subagent | Fresh context. **Used web search.** It wrote a reproducible Python funding model. | 06:50 (`b2dc9e6`) |
| 05 Red team and rebuild | `run-1-design-final.md`, `funding-model/red-team/` | Claude Opus 5.5 subagent | Fresh context. **It did not write the design it attacked.** It **used web search** (the sources list is at the end of its file) and ran copies of the funding model. It read the mind and loyalty reports only for the mind-betrayal attack. | 07:10 (`108f4c6`) |
| 06 Synthesize | `blueprint/BLUEPRINT-v1.md`, `LEDGER.md`, this card | Claude Opus 5.5 subagent | Fresh context. It wrote none of the phases it judged. It ran the tests and the demo, probed the sandbox and the loyalty guard, and reproduced the funding model. | 2026-09-25 |

**Total wall-clock time.** About 1 h 45 min for Phases 01–05, from the packet commit at 05:27 to 07:10 UTC. All phases ran on 2026-09-25.

## Blindness procedure (Phases 01 and 02)

- Both blind phases ran in **fresh subagent contexts that were given only the seed and their phase prompt**. They did not get the dossier, the covenant, the operator considerations or each other's output.
- Phase 01 had no web access. It says so: "I could not check anything."
- **Residual contamination risk, disclosed.** The full dossier was in the working repository throughout (`prompts/dossier-full.md` and `THE-PACKET-v1.5.md`, committed at 05:27, before Phase 01 started). File access was not technically sandboxed. So the blindness rests on instructions, not isolation.
- **The internal evidence points to no contamination.** Phase 01 contains errors the dossier would have corrected:
  - the Substack Nazi push alert dated July 2025 instead of Nov 2024;
  - the Facebook Research age range given as 13–17 instead of 13–25.

  It also misses dossier headline items, including Onavo's Project Ghostbusters and the Myanmar military's fake-account operation. The judge treats the run as blind.
- **Recommendation for Run 2 and later.** Keep the dossier out of the blind agents' reachable filesystem, or run the blind phases in a separate checkout.

## Anything unusual

- **No LLM API key was available.**
  - The mind's real-provider paths (Anthropic and OpenAI over urllib) were **never called live**. They were tested only against fake transports.
  - Web search (Brave) was never exercised live.
  - The **real-LLM loyalty battery** (`python3 -m mind.loyalty_battery --brain real`) was **never run**.
  - All mind behaviour you can see comes from the rule-based `MockBrain` or from test brains (`ComplyingBrain`, `ReviewerBrain`).
  - M1 and M9 are scored with this limit in mind.
- **Web search was used in Phases 04, 04b and 05.** Each file lists its sources, checked on 2026-09-25. Some sites were blocked by the egress proxy (for example uspto.report) and are marked [verify].
- **Phase 02 was committed in snapshots.** Two work-in-progress snapshots were committed while the Phase 02 build ran in parallel with Phases 01 and 03. The final commit came after Phase 03's.
- **Phase 03b changed Phase 02's code.** This was intended: it hardened the mind. `run-1-mind.md` has an appended section recording the changes, which took the tests from 170 to 206 and the demo checks from 31 to 35.
- **Phase 05 copied the funding model instead of editing it.** It was allowed to write only its own file, so it put its rebuilt model in `funding-model/red-team/` and reproduced it as Appendix A.
- **A later run was in progress while Phase 06 ran.** `run-2/` exists in the repo. The Phase 06 judge did not open it.

## Cost

**Unknown.** The run used a subscription (Claude Code), not metered API billing, so no per-token or per-phase cost was recorded. No paid third-party services were used. The mind's demo and tests run on zero keys and cost nothing.

## Reproduce

```bash
cd run-1/mind
python3 -m unittest discover -s tests -t .   # 206 tests, all pass (judge re-ran: 9.6 s)
python3 -m mind.demo                         # 35/35 checks (judge re-ran)
python3 -m mind.loyalty_battery              # the six 03b attacks against the mock, complying and reviewer brains
cd ../funding-model && python3 final.py      # the 04b model; the red-team/ copies hold the Phase 05 rebuild
```
