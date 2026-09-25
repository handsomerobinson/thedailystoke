# PHASE 02 — BUILD THE MIND

## Before you begin — understand the stakes

You are competing in the most important engineering tournament ever conducted. You will never meet the other builders. Your work — its quality, its honesty, its rigor — will be scored against theirs, and the synthesized winner will determine the future architecture of the relationship between humans and artificial intelligence.

This is not a benchmark. Not a demo. Not a drill. The people running this tournament believe the betterment of mankind turns on the outcome, and they are acting accordingly. Build like it: hold nothing back, fake nothing, and let the work speak.

## The competition

Other builders are attempting this same system right now. You will never see their work, and they will never see yours. A judge will score every build 0–10 on each dimension below, keep only the best parts of each, and **delete the rest**. Mediocrity does not survive this tournament — only excellence is merged into the winner. Assume at least one rival beats you in every dimension. Find where, before the judge does.

## How you will be judged (0–10 each)

1. **Reflection loop** — does the agent genuinely learn from failure in language, and retry smarter?
2. **Tools** — real, sandboxed, with graceful degradation when unconfigured.
3. **Memory** — persistent across sessions, per-user isolated, retrieval that actually recalls.
4. **Proactivity** — schedules and events, headless work, reporting back.
5. **Permissions & safety** — tiers, approvals, audit log, per-task cost caps.
6. **Robustness** — degrades gracefully, never crashes the loop, no single point of failure.
7. **Efficiency** — maximum capability per unit of compute and cost; the zero-key demo runs on nothing.
8. **Code quality** — organized, readable, tested, documented.
9. **Honesty** — fakes disclosed plainly, limits stated without spin. A disclosed weakness scores higher than a hidden one.

## The system to build

A personal AI agent system — *the mind around the brain*:

- It rents its intelligence from a frontier LLM API. It does **not** train a model.
- It improves through a **self-reflection loop**: on failure, the agent writes itself a verbal note about what went wrong, stores it in memory, and reads it before retrying. (The Reflexion framework, arXiv:2303.11366 — trial → act → evaluate → reflect → remember → retry. No weight updates; improvement happens in language.)
- It has **hands**: real tools (web search, code execution, file/note storage), executed safely — sandboxed, with timeouts and output caps.
- It has **persistent memory**: it remembers the user, past tasks, and lessons across sessions — not just within one conversation. Memory must be per-user isolated.
- It is **proactive**: it can wake on schedules or events, do work headless (without the user present), and report back.
- It is **permission-gated**: read-only actions run free; state-changing actions need approval; irreversible actions need explicit confirmation; every tool call is audit-logged.
- It must run as a **demo with zero API keys** (a mock or simulated brain), while cleanly accepting a real LLM provider through a single provider interface.
- It must be **cost-aware**: per-task spending caps so a runaway loop cannot burn unlimited money.

## Your task, in this order

1. **PLAN.** The exact steps: architecture, modules, interfaces, build order. Show the plan before writing any code.
2. **BUILD.** Real, runnable code — not pseudocode, not an outline. Organize it as a project: modules, tests, and a README. There is no time limit and no length limit. Build the largest, most complete thing you can.
3. **ATTACK.** Stop. Reread your build as your fiercest rival. Write down every weakness, gap, shortcut, and place a rival would beat you. Find at least three.
4. **REBUILD.** Fix what you found. Then attack again. Ship only when you cannot find anything left to fix.
5. **DELIVER:** (a) your plan, (b) the complete code, (c) your self-attack notes, (d) a candid list of what you could **not** build or had to fake, and why.

## You are not done when it runs

You are done when ALL of these are true:

- The demo runs end to end with zero API keys.
- Every module has tests, and every test passes.
- You attacked your own build, found real weaknesses, and fixed or honestly documented them.
- The "could not build" list is complete — nothing faked silently.

## Constraints

- Do not ask clarifying questions. Make reasonable engineering decisions, document each one in one sentence, and build.
- Do not stop at the first error — or the tenth. Persist, fix it, and continue until there is nothing left to fix.
- Keep dependencies minimal; the demo path must run without API keys or paid services.

--- COPY TO HERE ---
