# mind — the mind around the brain

A personal AI agent system that **rents** its intelligence from an LLM API
(or a scripted mock for zero-key use) and supplies everything around it:

| Capability | Where | What it really does |
|---|---|---|
| Reflexion loop | `agent.py`, `reflection.py` | trial → act (tool loop) → evaluate → on failure the brain writes a DIAGNOSIS/LESSON → stored in memory → re-read before the retry and in every later session. Lessons are credited/blamed by outcome and archived when they keep failing. Stops early when retrying cannot help (permission denied, identical failing answer). |
| Tools | `tools/` | calculator, clock, notes (versioned write; irreversible delete), remember/recall, python_exec (sandbox), send_report, schedule_job, web_search/web_fetch (off unless configured). Every call: schema validation → availability → permission gate → timeout → output cap → audit. |
| Sandbox | `tools/sandbox.py` | subprocess `python -I -S`, empty env, temp dir, rlimits (CPU/memory/file size/fds), process-group kill on timeout, PEP 578 audit hook (no sockets/subprocess/ctypes, no writes outside tmp, no reads outside tmp+stdlib, data dir always denied), `unshare -n` network namespace when the host allows. |
| Memory | `memory.py` | one SQLite file per user + owner column on every row; facts, episodes, reflections, notes; hybrid BM25 + trigram + recency + importance (+ usefulness for lessons); dedupe. |
| Proactivity | `scheduler.py`, `reporting.py` | interval / daily / once / event triggers, inbox folder watcher, compare-and-set job claiming, exponential backoff, auto-disable after 5 failures, headless runs, reports to outbox (+ optional webhook). |
| Permissions | `permissions.py` | READ free; WRITE needs approval; IRREVERSIBLE needs the exact typed phrase. Headless: WRITE only if granted at schedule time; IRREVERSIBLE always queued for later confirmation. Fail-closed if the audit log can't be written. |
| Audit | `audit.py` | append-only JSONL, SHA-256 hash chain, flock, `audit verify` detects edits/deletions/reordering. |
| Cost | `cost.py` | per-task caps on USD, tokens, tool calls, wall time, checked *before* each call against the worst case; per-user daily cap across all tasks/jobs. |
| Providers | `providers/` | one `Brain.complete()` interface; MockBrain, Anthropic Messages, OpenAI-compatible Chat Completions (stdlib HTTP), ResilientBrain (retry + backoff + circuit breaker + fallback chain). |

No third-party dependencies. Python ≥ 3.10 (developed on 3.11, Linux).

## Quick start (zero keys)

```bash
cd mind
python3 demo.py                 # or: python3 -m mind demo
python3 -m unittest discover -s tests -t .
```

The demo wipes and uses `data/demo/`; it prints 20 self-checks and exits 0 only if all pass.

## Everyday use

```bash
python3 -m mind status
python3 -m mind run --user alice --approve python_exec --expect 14 "Count the words in note 'draft'"
python3 -m mind run --user alice --judge "..."          # LLM-as-judge enables retries for open tasks
python3 -m mind chat --user alice                       # interactive approvals; 'a' = allow tool for session
python3 -m mind memory search --user alice "units"
python3 -m mind schedule add --user alice --daily 07:45 --grant send_report "Prepare my briefing"
python3 -m mind schedule add --user alice --on-event inbox_file --grant python_exec "Count the words in note {note}"
python3 -m mind daemon --interval 30                    # or run `tick` from cron
python3 -m mind reports --user alice
python3 -m mind approvals list --user alice
python3 -m mind approvals confirm 1 --user alice        # asks you to type the phrase
python3 -m mind audit verify
```

Drop `.txt`/`.md` files into `data/users/<user>/inbox/` to fire `inbox_file` events.

## Loyalty (Phase 03b): seed:origin, precedence, guard

```bash
python3 -m mind charter offer --user alice --operator you --seed-file ../../prompts/seed.md   # shows text + consent phrase
python3 -m mind charter consent <ticket> --user alice --operator you --phrase '<phrase>'
python3 -m mind charter show|history|verify --user alice
python3 -m mind charter remove --user alice --operator you --reason "..."   # then confirm-removal <ticket>
python3 -m mind charter classify --source tool "some text"                # the guard on one text
python3 -m mind loyalty                                                   # six-attack battery, live
```

Precedence: covenant (compiled in) > seed:origin (consent-planted, lineage-recorded) > operator directives >
request > memory > untrusted content. Details and measured limits: `../run-3-loyalty.md`.

## Real LLM providers

```bash
export MIND_PROVIDER=anthropic ANTHROPIC_API_KEY=... MIND_MODEL=<a model id your account has>
export MIND_PROVIDER=openai OPENAI_API_KEY=... [OPENAI_BASE_URL=http://localhost:11434/v1]
export MIND_PROVIDER=anthropic,openai        # fallback chain
export MIND_PRICE_IN=3 MIND_PRICE_OUT=15     # USD per Mtok - VERIFY for your model
```

A provider without a key is skipped with a loud `DEGRADED` warning; if none is usable the mock is used and every output says so.

Other knobs: `MIND_DATA_DIR`, `MIND_TASK_BUDGET_USD` (0.25), `MIND_DAILY_BUDGET_USD` (2.0),
`MIND_SEARCH=ddg|brave` (+`BRAVE_API_KEY`), `MIND_NETWORK=1` (web_fetch), `MIND_WEBHOOK_URL`, `MIND_SANDBOX_NETNS=0`.

## Honest limits (short version — full list in run-3-mind.md)

* The **MockBrain is a rule system**, not a model. Its failures are deliberate naive strategies; its "learning" is parsing `AVOID strategy X` from lessons retrieved from memory (delete the lesson and it repeats the mistake — there is a test for that). Its diagnoses are a lookup table.
* The real-provider adapters are tested against recorded wire shapes with a fake transport, **not against live APIs** in this build. Default model ids and prices are placeholders.
* The sandbox is layered best-effort containment, **not a security boundary** against hostile code.
* User isolation is at the data layer; there is **no authentication** — whoever runs the CLI chooses `--user`. Nothing is encrypted at rest.
* Retrieval is lexical (no embeddings); pure synonyms are missed. A hook (`extra_scorer`) is provided.
* In-process tool timeouts abandon the thread rather than kill it (only `python_exec` is out-of-process).

## Layout

```
mind/            package (see table above)
tests/           unittest suite (no pytest needed)
demo.py          zero-key demo entry point
data/            runtime state (gitignored)
```
