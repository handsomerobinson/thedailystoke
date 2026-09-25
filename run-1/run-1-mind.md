# Run 1 — Build the Mind

(DRAFT — plan written before any code; later sections are filled in after build/attack/rebuild.)

## (a) Plan

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
