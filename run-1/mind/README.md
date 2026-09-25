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
python3 -m mind.demo                                # end-to-end demo, 31 self-checks, ~1 s
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
```

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
