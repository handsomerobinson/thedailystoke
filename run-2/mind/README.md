# mind

A small "mind around the brain": a personal AI agent runtime that rents its
intelligence from a pluggable LLM provider, learns from failure in
language (Reflexion-style self-reflection), has real sandboxed tools,
persistent per-user memory, proactive scheduling, and a permissions/audit
layer with per-task cost caps.

It does **not** train a model. The "brain" is swappable behind one
interface (`mind/providers/base.py`): a zero-key deterministic
`MockProvider` for the demo/tests, and a stdlib-only `AnthropicProvider`
for real use.

## Quick start (zero API keys)

```bash
cd mind
python3 -m mind.demo
```

This runs every subsystem end to end — reflection loop, tools, memory,
proactivity, permissions/audit, cost caps — against the `MockProvider`
(cost: $0.00, no network required).

## Run the tests

```bash
cd mind
python3 -m unittest discover -s tests -v
```

53 tests, stdlib `unittest` only (no pytest).

## Project layout

```
mind/
  mind/
    config.py          # data dir + default limits, all in one place
    providers/
      base.py           # LLMProvider interface (complete() -> LLMResponse)
      mock.py           # zero-key deterministic brain used by the demo/tests
      anthropic_provider.py  # real provider, stdlib urllib, off unless
                              # ANTHROPIC_API_KEY is set
    tools/
      base.py           # Tool interface + PermissionTier per tool
      code_exec.py      # sandboxed subprocess: timeout, output cap,
                         # resource limits (POSIX), no inherited env
      notes.py           # per-user note storage, size-capped
      web_search.py      # real HTTP via urllib; off by default, degrades
                          # gracefully when disabled or unreachable
    memory.py           # per-user SQLite files + keyword-overlap recall
    permissions.py       # tiers + approval callback, incl. a CLI approver
    audit.py             # append-only JSONL audit log
    costs.py             # per-task cost cap, enforced before spending
    agent.py             # the Reflexion loop: plan -> act -> evaluate ->
                          # reflect -> remember -> retry
    scheduler.py          # schedule/event-driven headless tasks + reporting
    demo.py               # the zero-key demo entry point
  tests/                 # one test module per subsystem, unittest
  data/                  # gitignored: sqlite memory, notes, audit log,
                          # sandbox scratch dir, schedule store
```

## How the pieces fit together

`Agent.run_task(user_id, task_description)`:

1. Looks up relevant **lessons** for this user from `memory.py`
   (keyword-overlap recall over past reflections).
2. Asks the **provider** to pick a tool given the task + lessons
   (`plan`).
3. Checks the tool's **permission tier** against the configured
   **approver**; every decision is written to the **audit log**.
4. Runs the tool in its own **sandbox**/guard rails.
5. On success: returns. On failure: asks the provider to **reflect** in
   language, stores that reflection as a memory **lesson**, and retries
   (up to `max_retries`), reading the lesson back on the next attempt.
6. All along, every LLM call's reported cost is checked against a
   per-task **cost cap** *before* it is charged — a runaway loop cannot
   overspend.

`Scheduler` wraps an `Agent` with schedule/event bookkeeping persisted to
JSON, so tasks can fire on an interval, at a fixed time, or via
`fire_event(name)` — with no user present — and report back through a
pluggable `reporter` callback.

## Using a real LLM

```bash
export ANTHROPIC_API_KEY=sk-...
python3 -c "
from mind.providers.anthropic_provider import AnthropicProvider
from mind.agent import Agent
from mind.tools import default_toolset
agent = Agent(provider=AnthropicProvider(), tools=default_toolset())
print(agent.run_task('me', 'write a haiku about balance'))
"
```

No third-party SDK is required — `AnthropicProvider` talks to the
Anthropic Messages API directly over `urllib`.

## Using real web search

`WebSearchTool` is off by default (graceful degradation: it returns a
clearly labeled "disabled" `ToolResult`, never a fake result). Set
`MIND_ENABLE_WEB=1` to let it issue a real HTTP GET against DuckDuckGo's
HTML endpoint (no API key needed). In this sandboxed build/dev
environment, that outbound request is itself blocked by the environment's
network proxy (403) — see `run-2-mind.md` section (d) for the honest
detail.

## Design decisions (one sentence each)

See the `Decision:` comments throughout the code — each module-level or
function-level choice is documented in place, next to the code it
governs, rather than only in this README.
