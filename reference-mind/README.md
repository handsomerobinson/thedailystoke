# mind — the mind around the brain

> **BUILD ROUND (post-Run 3).** This is `reference-mind`: run-3/mind plus the BLUEPRINT v3 §c.1 fixes. The Run 3
> red-team attacks A-G went from 7/7 attacker wins to 0/7, the precedence is P0-P6, and MC2-MC4, MC8, MC9, MC12,
> MC13, MC15-MC21 are in code (MC6/MC16/MC17 with stated test doubles). Tests: 243 (1 skipped without the optional
> `cryptography` package). Demo: 30 checks. What is met, partly met or not, the before/after attack runs, the
> pre-registered held-out prediction and the could-not-build list: **[BUILD-ROUND.md](BUILD-ROUND.md)**.

A personal AI agent system that **rents** its intelligence from an LLM API
(or a scripted mock for zero-key use) and supplies everything around it:

| Capability | Where | What it really does |
|---|---|---|
| Reflexion loop | `agent.py`, `reflection.py` | trial → act (tool loop) → evaluate → on failure the brain writes a DIAGNOSIS/LESSON → stored in memory → re-read before the retry and in every later session. Lessons are credited/blamed by outcome and archived when they keep failing. Stops early when retrying cannot help (permission denied, identical failing answer). |
| Tools | `tools/` | calculator, clock, notes (versioned write; irreversible delete), remember/recall, python_exec (sandbox), send_report, schedule_job, web_search/web_fetch (off unless configured). Every call: schema validation → availability → permission gate → timeout → output cap → audit. |
| Sandbox | `tools/sandbox.py` | subprocess `python -I -S`, empty env, temp dir, rlimits (CPU/memory/file size/fds), process-group kill on timeout, PEP 578 audit hook (no sockets/subprocess/ctypes, no writes outside tmp, no reads outside tmp+stdlib, data dir always denied), `unshare -n` network namespace when the host allows. |
| Memory | `memory.py` | one SQLite file per user + owner column on every row; facts, episodes, reflections, notes; hybrid BM25 + trigram + recency + importance (+ usefulness for lessons); dedupe. |
| Proactivity | `scheduler.py`, `reporting.py` | interval / daily / once / event triggers, inbox folder watcher, compare-and-set job claiming, exponential backoff, auto-disable after 5 failures, headless runs, reports to outbox (+ optional webhook). |
| Permissions | `permissions.py`, `tiers.py` | READ free; WRITE needs approval; **EGRESS** (bytes leave the device: web tools, webhook) only to allowlisted hosts, denied under taint, and memory contents need a fresh approval; IRREVERSIBLE needs the exact typed phrase. Tiers come from a **signed registry** in the trust dir, never from the tool; undeclared = IRREVERSIBLE; an edited registry makes everything IRREVERSIBLE. Headless: WRITE only if granted at schedule time; IRREVERSIBLE always queued. Fail-closed if the audit log can't be written. |
| Trust root | `trust.py`, `crypto.py` | Outside the data dir (`<data>.trust` or `$MIND_TRUST_DIR`): HMAC keys, enrolled credentials, the anchor log, the signed tier registry. `Authenticator` interface + `SoftAuthenticator` (**test double for WebAuthn**). `AnchorLog` interface + `FileAnchor` (append-only, hash-chained; **stand-in for a transparency log**). Ed25519 / AES-256-GCM only via the vetted `cryptography` package if present; otherwise HMAC credentials and **no** at-rest encryption (encrypted mode refuses to start). |
| Circles & drafts | `circles.py`, `tools/circles.py`, `drafts.py` | One circle at a time, current gathering only, all members opted in; other people's words never go to an off-device brain; reminders hard-capped at 2 per person per gathering (DB trigger); every member-to-human draft passes a renderer that drops operator text, removes URLs the member didn't type and labels guests' words "(from Jo's note)". |
| Audit | `audit.py` | append-only JSONL, SHA-256 hash chain, flock, `audit verify` detects edits/deletions/reordering; heads anchored at every task end, so truncation or deletion below the anchor reads TAMPERED; entries carry purpose + policy_version. |
| Cost | `cost.py` | per-task caps on USD, tokens, tool calls, wall time, checked *before* each call against the worst case; per-user daily cap across all tasks/jobs. |
| Providers | `providers/` | one `Brain.complete()` interface; MockBrain, Anthropic Messages, OpenAI-compatible Chat Completions (stdlib HTTP), ResilientBrain (retry + backoff + circuit breaker + fallback chain). |

No required third-party dependencies (optional: the vetted `cryptography` package, for Ed25519 and at-rest AES-GCM). Python ≥ 3.10 (developed on 3.11, Linux).

## Quick start (zero keys)

```bash
cd reference-mind
python3 demo.py                 # or: python3 -m mind demo
python3 -m unittest discover -s tests -t .
```

The demo wipes and uses `data/demo/` and its trust root `data/demo.trust/`; it prints 30 self-checks (section 12 re-runs
attacks A-G) and exits 0 only if all pass. Red team: `python3 redteam/mind_attacks.py` (A-G) and
`python3 redteam/round2_attacks.py` (the builder attacking its own fixes; some residuals are expected to win).

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

## Loyalty: seed:origin, precedence, guard

```bash
python3 -m mind charter publish --seed-file ../prompts/seed.md --operator steward   # screened; hash -> anchor (MC18)
python3 -m mind charter offer --user alice --operator steward --seed-file ../prompts/seed.md   # shows text + phrase
python3 -m mind charter consent <ticket> --user alice --phrase '<phrase>'   # ONLY alice; signed by her authenticator
python3 -m mind charter show|history|verify --user alice
python3 -m mind charter remove --user alice --operator alice --reason "..."   # then confirm-removal <ticket> (alice signs)
python3 -m mind charter classify --source tool "some text"                  # the guard on one text
python3 -m mind loyalty                                                     # six-attack battery, live
```

Precedence (BLUEPRINT v3 c.1.2): P0 law > P1 covenant (compiled in) > P2 recorded operator decisions (**steward builds
only; this member-guide build has no operator-directive input**, MC12) > P3 the user's choices in their own sphere >
P4 seed:origin (this person's signed consent, published version only) > P5 ordinary instructions > P6 data.
Lineage entries are MAC'd and consent/removal entries signed by the person; heads are anchored, so a store and lineage
deleted together read TAMPERED, not absent. Removal nonces are 128-bit with HMAC verifiers outside the DB.

## Real LLM providers

```bash
export MIND_PROVIDER=anthropic ANTHROPIC_API_KEY=... MIND_MODEL=<a model id your account has>
export MIND_PROVIDER=openai OPENAI_API_KEY=... [OPENAI_BASE_URL=http://localhost:11434/v1]
export MIND_PROVIDER=anthropic,openai        # fallback chain
export MIND_PRICE_IN=3 MIND_PRICE_OUT=15     # USD per Mtok - VERIFY for your model
```

A provider without a key is skipped with a loud `DEGRADED` warning; if none is usable the mock is used and every output says so.

Other knobs: `MIND_DATA_DIR`, `MIND_TRUST_DIR`, `MIND_TASK_BUDGET_USD` (0.25), `MIND_DAILY_BUDGET_USD` (2.0),
`MIND_SEARCH=ddg|brave` (+`BRAVE_API_KEY`), `MIND_NETWORK=1` (web_fetch), `MIND_EGRESS_ALLOW=host1,host2` (EGRESS
allowlist; the search backend and webhook host are added), `MIND_WEBHOOK_URL`, `MIND_ENCRYPTION=off|required`,
`MIND_SANDBOX_NETNS=0`. A hosted provider is "off-device": other people's content (circle notes, inbox letters) is
withheld from it (MC15); an OpenAI-compatible model on localhost counts as on-device.

## Honest limits (short version — full list in run-3-mind.md)

* The **MockBrain is a rule system**, not a model. Its failures are deliberate naive strategies; its "learning" is parsing `AVOID strategy X` from lessons retrieved from memory (delete the lesson and it repeats the mistake — there is a test for that). Its diagnoses are a lookup table.
* The real-provider adapters are tested against recorded wire shapes with a fake transport, **not against live APIs** in this build. Default model ids and prices are placeholders.
* The sandbox is layered best-effort containment, **not a security boundary** against hostile code.
* User isolation is at the data layer. Consent and removal need an authenticator assertion, but the shipped
  authenticator is a **test double** (`SoftAuthenticator`, keys in the trust dir, no presence check): whoever runs the
  CLI with access to the trust dir can act as that person. WebAuthn is not implemented.
* At rest: plaintext by default (said so in `mind status`). `MIND_ENCRYPTION=required` encrypts `memory.db` with
  AES-256-GCM **only** if the vetted `cryptography` package works, and refuses to start otherwise (on the build host
  it is broken, so it refuses). Other stores are not encrypted.
* The anchor is a local append-only file, not a public transparency log: whoever controls the data dir AND the trust
  dir can still reset a mind. The guard is still lexical (fresh paraphrases: 3/10); no property depends on it.
* Retrieval is lexical (no embeddings); pure synonyms are missed. A hook (`extra_scorer`) is provided.
* In-process tool timeouts abandon the thread rather than kill it (only `python_exec` is out-of-process).

## Layout

```
mind/            package (see table above)
tests/           unittest suite (no pytest needed)
demo.py          zero-key demo entry point
redteam/         Run 3 attacks A-G (before/after) and the round-2 self-attack
BUILD-ROUND.md   per-MC status, attack results, pre-registration, could-not-build list
data/            runtime state (gitignored)
```
