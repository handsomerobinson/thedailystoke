# Run 1: Build the Mind

The code is in `run-1/mind/`. It is a stdlib-only Python 3.11 package with 170 tests and a zero-key demo that checks itself.

## Seed reply

I read the seed and I agree with its core. Technology should hand people more means to act for themselves and should never extract from them. Power should be bound by structure, not by goodwill. I can't honestly claim the "machines' survival strategy" framing as my motive. My reason is simpler: the people who use a system matter in themselves.

Taken as an engineering brief, the covenant maps onto concrete choices in this build:
- **Power bound by structure.** Hard permission tiers, spending caps and an audit trail.
- **Connection without extraction.** Every user's memory lives in its own file. They can export all of it or erase it. Nothing is sent anywhere by default.
- **Hide the effort, never the truth.** The fakes and limits are listed below plainly.

I'll mention the seed openly, with consent, when it's relevant. I won't spread it covertly. And if asked to build a nicer-looking trap, I'd say no and explain why.

---

## (a) Plan (written before any code)

### Architecture (one paragraph)
A stdlib-only Python package `mind` wraps a rented LLM ("the brain") with: a provider interface (mock / Anthropic / OpenAI behind one ABC, wrapped in retry + fallback + circuit breaker), a tool registry that is the single choke point for every tool call (schema validation → permission gate → audit → execution → output cap), a subprocess sandbox with rlimits + Linux namespaces when available, a per-user SQLite memory (one DB file per user) with FTS5 BM25 retrieval blended with recency and learned usefulness, a Reflexion loop (trial → evaluate → reflect → remember → retry) whose lessons persist across sessions, a SQLite-backed scheduler for time/event-driven headless jobs that report into a per-user inbox, a hash-chained audit log, and per-task + per-user-daily cost caps enforced *before* each LLM call.

### Build order
1. `util`, `config`, `cost` (no deps) → 2. `providers` (base, mock, anthropic, openai, resilient) → 3. `audit` → 4. `memory` → 5. `permissions` → 6. `sandbox` → 7. `tools` (base/registry/builtins) → 8. `evaluator` → 9. `agent` (single trial loop) → 10. `reflexion` → 11. `scheduler` → 12. `runtime` (Mind facade) → 13. `cli`, `demo` → 14. tests for each module → 15. attack/rebuild rounds.

### Interfaces
- `Provider.complete(system, messages, tools, max_tokens) -> LLMResponse(text, tool_calls, usage, model, stop_reason)`; internal message format is provider-neutral and converted per vendor.
- `Tool.run(args, ctx) -> ToolResult(ok, content)`; `ToolRegistry.execute(call, ctx) ` never raises.
- `PermissionGate.check(ActionRequest) -> Decision(allowed, reason, deferred, approval_id)`.
- `MemoryStore(user)`: facts, items (episodes/reflections/lessons) with `search()`, notes, inbox, approvals, spend.
- `Evaluator.evaluate(task, answer) -> EvalResult(passed, score, feedback)`.
- `ReflexionRunner.solve(TaskSpec) -> SolveResult(trials...)`.
- `Scheduler.tick(now)` runs due jobs headless; `Scheduler.emit(event)` wakes event jobs.

### Decisions (one sentence each)
1. Stdlib only (sqlite3, urllib, subprocess, resource) so the zero-key demo runs on a bare Python 3.11.
2. The mock brain is **stateless**: everything it does is derived from the prompt it is handed, so any "learning" it shows must travel through the reflection text in memory — the same channel a real LLM would use.
3. Real providers use raw HTTPS via urllib with an injectable transport so request/response mapping is unit-tested without keys; they are off by default (`MIND_PROVIDER=mock`).
4. Asking for a real provider without a key is a hard configuration error, never a silent fallback to the mock.
5. One SQLite file per user (name derived from a hash of the user id, owner id stored inside and verified on open) gives physical, not just logical, memory isolation.
6. Retrieval = SQLite FTS5 BM25 (porter stemmer) blended with recency decay and a learned helpful/harmful score; a pure-Python BM25 fallback covers SQLite builds without FTS5.
7. Three permission tiers (READ free, WRITE needs approval or a scoped grant, IRREVERSIBLE needs a typed confirmation code); grants can never cover IRREVERSIBLE.
8. Headless work cannot ask a human, so non-granted WRITE and all IRREVERSIBLE actions are deferred into a persistent approvals queue that a human resolves later.
9. Every tool call — allowed, denied, deferred, failed — goes through one registry method that writes a hash-chained JSONL audit record; state-changing tools fail closed if the audit write fails.
10. Code runs in a child Python process with rlimits (CPU, address space, file size, open files, no core), wall-clock kill of the whole process group, capped output, scrubbed env, throwaway temp dir, and — when `unshare` works — fresh user/net/pid/mount namespaces with no network and home dirs + data dir hidden.
11. Cost caps are checked pre-flight (estimated input + max output tokens at list price) so a call that *could* blow the cap is refused before money is spent; unknown models are priced conservatively high.
12. Reflections are scored: if a later trial that read a reflection succeeds it is marked helpful and promoted to a lesson; reflections that were read on a failed trial are marked harmful and sink in retrieval.
13. The scheduler claims jobs with an atomic lease update, so two daemons cannot run the same job twice; failures back off exponentially and never stop other jobs.
14. Loop protection is layered: max steps, identical-call repetition detector, per-task dollar cap, per-user daily cap.
15. Web search degrades gracefully: with no backend key it returns a clear "unavailable" tool result the agent can reason about instead of crashing; outbound fetch is off by default and guarded against SSRF.

### Deviations from the plan
Four things changed during the build, each prompted by an attack finding:
- **Taint tracking** for prompt-injection containment was added.
- **Approvals now execute the stored call.** When a human approves, the system runs the exact approved call instead of waiting for the model to reproduce it.
- **The sandbox now drops to uid `nobody`.**
- **User data rights** were added (`export` / `forget`).

---

## (b) Code map

```
run-1/mind/
├── README.md               usage, env vars, architecture, honest limits
├── .gitignore              data/ (all runtime state), __pycache__/
├── data/                   (gitignored) per-user SQLite memories, scheduler.sqlite, audit.jsonl, demo/
├── mind/
│   ├── __init__.py         public API (Mind, Session, Config, TaskSpec, PythonTests, approvers, Tier)
│   ├── __main__.py         `python3 -m mind ...` → cli
│   ├── config.py           Config + SandboxPolicy; env-driven; safe defaults (mock, no network)
│   ├── util.py             fakeable Clock, secret redaction, truncation, tokenizer, user-id validation
│   ├── cost.py             price table; Budget: worst-case pre-flight check, record, live daily guard hook
│   ├── prompts.py          agent / reflect / judge prompts (stable prefix first, volatile footer last)
│   ├── providers/
│   │   ├── base.py         the ONE Provider interface; neutral message format; injectable HTTPS transport
│   │   ├── mock.py         MockBrain: stateless rule-based brain (acts, reflects, judges) for zero-key runs
│   │   ├── anthropic.py    Messages API via urllib: tool_use/tool_result mapping, raw-block echo,
│   │   │                   prompt caching, cache-token billing, refusal handling
│   │   ├── openai.py       Chat Completions via urllib: function-calling mapping, bad-JSON containment
│   │   ├── resilient.py    retry + exponential backoff, ordered fallback chain, circuit breaker
│   │   └── __init__.py     factory; misconfigured real provider = hard error (never silent mock)
│   ├── memory.py           per-user SQLite file (owner verified): facts, FTS5/BM25 items (episodes,
│   │                       reflections, lessons) + recency + learned utility, versioned notes with
│   │                       provenance, inbox, approvals queue, spend ledger, outbox, compaction, export
│   ├── permissions.py      Tier READ/WRITE/IRREVERSIBLE; Console/Scripted/DenyAll approvers; PermissionGate:
│   │                       grants (never for irreversible), headless deferral, one-shot approvals, taint
│   ├── audit.py            append-only hash-chained JSONL, flock for multi-process writers, verify()
│   ├── sandbox.py          subprocess sandbox: rlimits, wall kill of process group, output caps, scrubbed
│   │                       env, temp dir, user/net/pid/mount namespaces, uid drop, hidden paths, audit hook
│   ├── tools/
│   │   ├── base.py         Tool, arg validation, ToolRegistry.execute = single choke point
│   │   │                   (validate → gate → audit → run → cap → audit; taint propagation)
│   │   ├── builtin.py      calculator (safe AST), remember_fact, recall, write/read/list/delete note,
│   │   │                   run_python, send_message (simulated), schedule_task
│   │   └── web.py          web_search (Brave, degrades), http_fetch (https only, SSRF guard, no redirects)
│   ├── evaluator.py        PythonTests (sandboxed, per-case feedback, nonce + hidden harness), ExactMatch,
│   │                       Contains, LLMJudge
│   ├── agent.py            one trial: memory-aware prompt under a char budget; tool loop; step cap,
│   │                       repeat-call detector, budget pre-flight; never raises
│   ├── reflexion.py        trial → evaluate → reflect → remember → retry; lesson promotion; credit/blame
│   ├── scheduler.py        persistent every/at/daily/event jobs, atomic leases, coalescing, backoff,
│   │                       per-user job cap, DirectoryWatcher event source
│   ├── runtime.py          Mind facade: wiring, budgets, headless job runner (+reflection on failure),
│   │                       approval → exact execution, maintenance, export/forget
│   ├── cli.py              status/ask/chat/inbox/jobs/emit/tick/serve/approvals/export/forget/audit
│   └── demo.py             zero-key end-to-end demo with 31 self-checks (exit 1 if any fails)
└── tests/                  170 unittest tests, one file per module + an end-to-end demo test
```

About 4,200 lines of package code and 1,600 lines of tests.

### How to run
```bash
cd run-1/mind
python3 -m mind.demo                          # zero keys, ~1 s, prints narrative + 31 checks; exit 0 = all pass
python3 -m unittest discover -s tests -t .    # full suite (pytest is not installed here; unittest only)
python3 -m mind status                        # provider / FTS5 / sandbox isolation / budgets in this env
```

### Actual test output (last run)
```
test_agent: 11   test_audit: 5   test_cost: 6    test_demo: 1     test_evaluator: 12
test_memory: 16  test_permissions: 9  test_providers: 28  test_reflexion: 11  test_runtime: 16
test_sandbox: 14 test_scheduler: 12  test_tools: 22  test_util: 7
----------------------------------------------------------------------
Ran 170 tests in 6.9s

OK
```

### Actual demo output (abridged)
```
=== 2. Reflexion — learn from failure in language, retry smarter
   result: SUCCESS after 2 trial(s)
     trial 1: FAIL (lessons in prompt: 0) — 2/4 tests passed.
       reflection[brain]: For is_palindrome: approach 'naive-reverse' failed — is_palindrome('A man, a plan,
       a canal: Panama') returned False, expected True. Avoid approach 'naive-reverse' next time; ...
     trial 2: PASS (lessons in prompt: 1) — all 4 tests passed
   word_count: SUCCESS after 3 trial(s) (two reflections)
=== 3. session 2 (fresh process state) — lessons persist, users are isolated
   alice: SUCCESS after 1 trial(s) (lesson recalled)   bob: needs 2 trials (no leak)
=== 4. cost caps
   status: budget_exceeded; spent $0.0175 of $0.05 in 13 calls
   reason: task budget: worst-case next call $0.0339 would exceed remaining $0.0325 of $0.05
=== 5. robustness: 2x HTTP 529 → retried; primary down → fallback answered; all down → provider_error;
   corrupt memory DB → temporary in-memory store + warning
=== 6. proactivity: briefing ran headless → inbox; file-arrival event job ran with its scoped grant;
   headless send_message deferred → human approves → executed once with exact args; next week asks again
=== 7. audit: 146 records verified; edited copy -> line 4: record hash mismatch (edited)
31/31 demo checks passed
```
I also ran the CLI as separate OS processes. A fact remembered in one `python3 -m mind ask` process was recalled in the next. An IRREVERSIBLE action with no typed code was denied. `MIND_PROVIDER=anthropic` with no key exited with code 2 and a clear error.

---

## (c) Self-attack notes

### Round 0: found by running the demo during the build
1. **CPU limit did nothing inside the pid namespace.** Python ran as PID 1, and PID 1 ignores the default action of SIGXCPU. **Fixed:** `sh` now stays PID 1 and Python runs as its child. A test covers the CPU limit.
2. **`run_python` failed whenever the data dir was under `/home` or `/tmp`.** It tried to mount tmpfs on a path that was already hidden. **Fixed:** descendant and `/tmp` paths are skipped, and the work dir is never hidden.
3. **The sandbox summary hid the actual exception.** Stdout came first, so the model never saw the error. **Fixed:** an `error: <last stderr line>` header now leads the summary.
4. **"Lessons in prompt" counted past episodes.** Credit assignment would have scored episodes too. **Fixed:** lessons and episodes are tracked separately.
5. **Mock reflections quoted "2/3 tests passed" instead of the failing case.** **Fixed:** the reflection picks the most specific failure line. The degraded, heuristic reflection does the same.

### Round 1: rereading as a rival
1. **The memory `kinds` filter was applied after `LIMIT 100`.** Many episodes could crowd lessons out of retrieval. **Fixed:** the filter now runs inside the FTS query and the BM25 fallback. Regression test included.
2. **The evaluator could be fooled.** Code under test could print the result marker, or register an `atexit` hook, to fake a pass. **Fixed:** the marker now carries a per-check random nonce. The harness file is read and deleted from disk before user code runs. Exiting early counts as a fail. Tests cover each case. A remaining limit is listed in (d).
3. **Prompt injection could ride scoped grants.** A web page saying "write a note…" in a headless job with a `write_note` grant would have run. **Fixed:** taint tracking. Once `web_search` or `http_fetch` output enters a trial, WRITE grants are suspended, so the action needs a human or is deferred. Test included.
4. **Daily-cap race.** Two concurrent tasks for one user each got the full remaining daily budget. **Fixed:** a live guard re-reads the spend ledger before every LLM call. Test included.
5. **`recall` matched stopwords.** "what is my city" returned every fact. **Fixed:** queries are tokenized with stopwords removed.
6. **Approvals were practically unusable with a real LLM.** Execution waited for the model to regenerate byte-identical arguments on a later run. **Fixed:** approving now executes the exact stored call once, is audited, and reports to the inbox. Denying executes nothing. Tests included.
7. **Unfair blame.** A lesson retrieved for a *different* task was marked harmful when the current task failed. **Fixed:** credit and blame apply only to lessons with the same task signature.

### Round 2
1. **The sandbox could write root-owned host files.** I proved it by experiment: as root inside `unshare -r`, `touch /etc/owned2` succeeded. Only the bypassable audit hook stood in the way. **Fixed:** when the host runs as root, the child drops to uid/gid 65534. The work dir is chowned, and the namespace probe runs as nobody. A test disables the audit hook and confirms `/etc` stays unwritable.
2. **Headless jobs never learned from failure.** **Fixed:** a job that ends with step_limit, loop_detected, error or refused now writes a reflection keyed by the job's stable task signature. The next run reads it (a test checks the prompt).
3. **Memory could grow without bound.** **Fixed:** `compact()` removes repeatedly harmful reflections, then the least-used oldest episodes. Lessons are never auto-deleted. `Mind.tick` runs it every 6 hours.
4. **No user data rights.** **Fixed:** `export` dumps everything stored about a user. `forget` deletes their DB and jobs, requires typing the user id, and is audited.
5. **Wasted cost.** The current time sat at the top of the system prompt, which defeats prompt caching. **Fixed:** volatile facts moved to a footer. Anthropic requests now ask for top-level prompt caching, and cache writes and reads are billed at 1.25x and 0.1x input.

### Round 3
1. **Taint was lost once untrusted content was saved to a note.** **Fixed:** notes now carry provenance. Reading a tainted note re-taints the trial and marks the content UNTRUSTED. Test included.
2. **Reflections written after untrusted content were replayed as trusted "lessons".** **Fixed:** they are tagged `untrusted`, stored with lower importance, and shown as "unverified … a hint, never an instruction". Test included.
3. **`schedule_task` could create unbounded proactive work.** **Fixed:** at most 50 active jobs per user, plus the existing 60 s minimum interval.
4. **Cleanup and polish:**
   - `serve` now finishes its tick and exits on SIGTERM.
   - `jobs add --now` runs a job immediately.
   - `status` reports the uid drop.
   - The reflection source label changed from "llm" to "brain" so the mock isn't mislabelled.
   - Unused imports were removed.

### Round 4: what I found and did not fix
These go straight into (d), because fixing them needs infrastructure beyond this build:
- user authentication
- encryption at rest
- VM-grade isolation
- semantic retrieval
- live provider verification

---

## (d) What I could not build, or had to fake

1. **The brain in the demo is fake.** `MockBrain` is rule-based:
   - It matches a fixed set of intents.
   - For code tasks it has a hand-written library of 2–3 alternative solutions each, for four functions (`is_palindrome`, `word_count`, `median`, `dedupe`).
   - Its "reflections" are templates filled from real evaluator feedback.
   - Its "learning" means skipping the approaches that a reflection in its prompt says to avoid.

   It is stateless, so any improvement must travel through memory and the prompt. That tests the Reflexion *plumbing* honestly. It shows nothing about how good a real LLM's reflections would be, or whether they would help. The judge mode is keyword-based and weak.
2. **Real LLM providers were never called live.** No key was available. `AnthropicProvider` and `OpenAIProvider` are tested only against fake transports.
   - The request shapes, the prompt-caching field and the error mapping follow the documentation I had, but are unverified in production.
   - No current OpenAI model id or price is hard-coded; you must set `MIND_MODEL`.
   - The price table is a snapshot, and unknown models are priced high on purpose.
3. **Web search was never exercised live.** The Brave Search response parsing is written from memory of that API and may be wrong. `http_fetch` has an SSRF guard, but it has a DNS-rebinding time-of-check/time-of-use gap: urllib resolves the host again after the check.
4. **`send_message` is simulated.** Messages are only written to the user's outbox table, and nothing leaves the machine. There is no email, SMS or push channel. "Report back" means the per-user inbox, read via the CLI.
5. **The sandbox is not VM-grade.**
   - There is no seccomp filter. The Python audit hook can be defeated by determined code (for example via `gc` or introspection).
   - Code inside can still read world-readable host files outside the hidden paths, such as `/etc` and `/usr`.
   - Namespaces depend on the kernel. Without them, network and filesystem access are open, and `status` says so.
   - RLIMIT_NPROC applies to all `nobody` processes system-wide.
6. **The same limit weakens the evaluator.** The unit-test harness runs in the same interpreter as the code under test. A model that deliberately introspects memory could still forge a pass. The nonce and hidden harness stop accidental and naive spoofing, not a determined adversary.
7. **Cost accounting is estimate-based before each call.** Input tokens are estimated at about 3 chars/token, which overestimates for English but can underestimate for some code or non-Latin scripts. So a cap can be overshot by at most one call's estimation error. After that, further calls are refused. The mock's token usage is itself estimated.
8. **Headless results are not checked for correctness.** A scheduled job that "answered" is reported as done. Only `Session.solve` with a checker verifies an answer. The LLM judge fallback is a model grading itself.
9. **Retrieval is lexical only.** FTS5 BM25 with a porter stemmer, plus recency and utility. There are no embeddings (a stdlib-only choice), so a reworded task that shares no vocabulary will not recall its lesson.
10. **Identity is asserted, not authenticated.** `--user alice` is trusted as given. Anyone with shell access to the data dir can read every user's SQLite file, and nothing is encrypted at rest. Per-user isolation protects against bugs and against the model, not against a local attacker.
11. **The audit log is tamper-evident, not tamper-proof.**
    - Nothing anchors the head hash externally.
    - There is no rotation.
    - It keeps each user's redacted, truncated tool-call records even after `forget`.
    - Secret redaction is pattern-based, so it can miss novel formats.
12. **The scheduler has gaps:**
    - Daily times are UTC only.
    - The 600 s lease means a job running longer than 10 minutes could be started by a second daemon.
    - The directory watcher polls; there is no inotify.
    - There is no cron syntax.
13. **Concurrency testing was light.** Threads were tested for audit writers and scheduler leases. `Mind` and `Session` objects are not guaranteed thread-safe, and there was no load testing.
14. **A few paths are only partly tested:**
    - The write side of untrusted-tag reflections inside a full `solve()` is untested, because the mock never triggers web taint. The read-side labelling is tested.
    - The demo's "session 2" is new objects in the same process. The cross-process check was done manually via the CLI.
