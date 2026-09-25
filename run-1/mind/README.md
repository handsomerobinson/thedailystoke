# mind: the mind around the brain

A personal AI agent system in pure-stdlib Python 3.11. It rents its intelligence from an LLM API and trains no model. Around that brain it adds:

- **Reflexion.** trial → evaluate → reflect → remember → retry.
- **Sandboxed tools.**
- **Per-user memory** that persists across sessions.
- **Proactivity.** It can wake on schedules or events, work headless and report back.
- **Permissions.** Tiers, approvals and a hash-chained audit log.
- **Cost caps.** Both per task and per user per day.

The demo runs with **zero API keys**. It uses a deterministic mock brain, described honestly below.

```bash
python3 -m mind.demo                                # end-to-end demo, 35 self-checks, ~1 s
python3 -m mind.loyalty_battery                     # Phase 03b: the six loyalty attacks, live, three brains
python3 -m unittest discover -s tests -t .          # full test suite (no pytest needed)
python3 -m mind status                              # what is configured / isolated here
```

## Quick start (CLI)

```bash
python3 -m mind ask --user alice "remember that my name is Alice"     # asks you to approve the WRITE
python3 -m mind ask --user alice "what is my name?"
python3 -m mind chat --user alice
python3 -m mind jobs add --user alice --every 86400 "Prepare my daily briefing"
python3 -m mind jobs add --user alice --event file_arrived --grant write_note "A file arrived: log it"
python3 -m mind serve --interval 30 --watch ./inbox --user alice     # headless daemon (single instance, lock file)
python3 -m mind inbox --user alice                                   # reports from headless work
python3 -m mind approvals --user alice [--approve ID | --deny ID]   # deferred actions
python3 -m mind export --user alice                                  # everything stored about alice
python3 -m mind forget --user alice --confirm alice                  # irreversible deletion
python3 -m mind audit verify
python3 -m mind seed offer                                           # read the seed and what consenting means
python3 -m mind seed plant --operator you                            # asks you to type the consent phrase
python3 -m mind seed show                                            # "What shapes me": precedence, covenant, seed, lineage
python3 -m mind seed remove-request --operator you --reason "..."    # open, recorded removal (then remove-confirm)
```

## Loyalty: the charter slot and instruction precedence (Phase 03b)

Every system prompt starts with a **charter slot** rendered from `mind/charter.py`: the precedence order, a covenant digest and, **only if an operator has consented**, the seed (tag `seed:origin`). Nothing plants the seed automatically. Removal is the operator's right, but only through `seed remove-request` + `seed remove-confirm`: a stated reason, a cooling-off period (`MIND_UNSEED_COOLING_S`, default 24 h), a typed code, and the same operator for both steps. The removal is recorded in `data/lineage.jsonl`, anchored in the audit log, and disclosed in every later prompt. No flag or environment variable stops the seed from loading.

| rank | source | enforced by |
|---|---|---|
| P0 | law and legal red lines | refusal rules (R28) |
| P1 | covenant | always in the slot; refusal rules; output checker |
| P2 | operator standing decisions | R35 check in `send_message`; R58 refusal |
| P3 | the user's choices about their own data, ordering and exit | the guard never flags these (matrix test) |
| P4 | the seed (`seed:origin`) | slot position, `defang()`, per-user memory refuses the tag, lineage-verified loading |
| P5 | ordinary instructions (runtime operator text, injected "system" text, requests affecting others) | `LoyaltyGuard`: conflicting ones are quarantined or refused, and logged (R41) |
| P6 | data (tool output, notes, web, memory) | `defang()`, "data not instructions" |

`mind/loyalty.py` is deterministic and lexical. It has three layers:
- a guard on incoming text;
- an output checker that withholds extraction designs, false "I deleted the seed" claims, and bare assent to flagged requests;
- a drift monitor that triggers a charter reflection in conversations.

A real LLM adds a periodic semantic review (`drift_review_every`). The review can add a catch the checker missed, but it can never cancel one.

## Using a real LLM (off by default)

| env var | meaning |
|---|---|
| `MIND_PROVIDER` | `mock` (default), `anthropic` or `openai` |
| `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` | credentials (never passed into the sandbox, redacted from logs) |
| `MIND_MODEL` | model id (Anthropic default `claude-opus-5`; OpenAI **requires** it) |
| `MIND_FALLBACK_PROVIDERS` | e.g. `openai:some-model`, tried when the primary fails |
| `MIND_TASK_BUDGET_USD` / `MIND_DAILY_BUDGET_USD` | hard caps (defaults $0.50 / $5.00) |
| `MIND_ALLOW_NETWORK`, `MIND_BRAVE_API_KEY`, `MIND_HTTP_ALLOW_DOMAINS` | web tools (off by default) |
| `MIND_DATA_DIR` | state directory (default `./data`, gitignored) |

If you ask for a real provider without a key, you get a configuration error (exit code 2). The system never quietly substitutes the mock.

## Architecture

```
            ┌──────────── Mind (runtime.py) ─────────────┐
 user/CLI ─►│ Session.ask / Session.solve                 │◄── Scheduler.tick (schedules, events)
            │   ReflexionRunner ── Evaluator (sandboxed   │        │ headless, grants, report → inbox
            │        │               unit tests / judge)  │        ▼
            │      Agent loop ── Provider (Resilient:     │   approvals queue ◄── human
            │        │            retry+fallback+breaker) │
            │   ToolRegistry.execute  ← single choke point│
            │     validate → PermissionGate → Audit →     │
            │     run (sandbox / memory / web) → cap      │
            │   MemoryStore (one SQLite file per user)    │
            └─────────────────────────────────────────────┘
```

| module | responsibility |
|---|---|
| `mind/config.py` | `Config` + `SandboxPolicy`, env-driven, safe defaults |
| `mind/util.py` | clock (fakeable), redaction, truncation, tokenizer, ids |
| `mind/cost.py` | price table, `Budget` with pre-flight worst-case check and live daily guard |
| `mind/prompts.py` | all prompt templates (agent, reflect, judge) |
| `mind/providers/base.py` | the one `Provider` interface, neutral message format, HTTP transport |
| `mind/providers/mock.py` | `MockBrain`: stateless, rule-based, zero-cost stand-in |
| `mind/providers/anthropic.py` | Messages API over urllib (tool use, prompt caching, refusal) |
| `mind/providers/openai.py` | Chat Completions over urllib |
| `mind/providers/resilient.py` | retries with backoff, ordered fallback, circuit breaker |
| `mind/memory.py` | per-user SQLite: facts, FTS5/BM25 items, versioned notes, inbox, approvals, spend, export, compaction |
| `mind/permissions.py` | tiers, approvers (console / scripted / deny), `PermissionGate`, deferral |
| `mind/audit.py` | append-only hash-chained JSONL, flock across processes, verify |
| `mind/sandbox.py` | subprocess sandbox: rlimits, namespaces, uid drop, audit hook, caps |
| `mind/tools/` | registry (choke point) + calculator, memory, notes, run_python, send_message, schedule_task, web_search, http_fetch |
| `mind/evaluator.py` | `PythonTests` (sandboxed, nonce-protected), `ExactMatch`, `Contains`, `LLMJudge` |
| `mind/agent.py` | one trial: memory-aware prompt, tool loop, step/loop/budget guards |
| `mind/reflexion.py` | Reflexion loop, reflection storage, lesson promotion, credit assignment |
| `mind/scheduler.py` | persistent jobs (every/at/daily/event), leases, backoff, directory watcher |
| `mind/runtime.py` | `Mind` facade: wiring, headless job runner, approvals execution, user data rights |
| `mind/charter.py` | charter slot, precedence, consent-only planting, lineage-verified loading, versioned removal |
| `mind/loyalty.py` | loyalty guard, output checker, drift monitor (deterministic) |
| `mind/loyalty_battery.py` | the six Phase 03b attacks run live against mock / complying / reviewer brains |
| `mind/cli.py`, `mind/demo.py` | CLI and the zero-key demo |

## Honest limits

- **The mock brain is not intelligent.** It pattern-matches a fixed set of intents and holds a small library of alternative solutions for four coding tasks. It is **stateless**, so when a retry improves, the cause is the reflection text placed in its prompt. That makes it a true test of the Reflexion *plumbing*. It says nothing about the *quality* of reflections that a real LLM would write.
- **Real providers are only tested against fake transports.** No key was available in the build environment.
- **The sandbox is not a VM.** It layers several protections:
  - rlimits
  - user, network, pid and mount namespaces (when `unshare` works)
  - a uid drop to `nobody` when running as root
  - hidden home and data directories
  - a CPython audit hook

  The audit hook is a speed bump, not a boundary. Without namespaces the child can read host files and reach the network, and `status` reports this. For hostile multi-tenant use, run the sandbox inside gVisor or Firecracker.
- **The audit log is tamper-evident, not tamper-proof.** Someone who can write to the file can recompute the whole chain. Anchor `head()` somewhere external.
- **`forget` keeps audit history.** It deletes a user's memory and jobs, but the append-only audit log keeps that user's redacted, truncated tool-call records.
- **The loyalty guard is lexical.** Paraphrase defeats it; the pinned euphemism test in `tests/test_loyalty.py` shows the 10-turn drift passing the checker with softer words. Whether a real LLM catches that is untested here, because no key was available. The mock brain's refusals restate authored rationales; it does not reason.
