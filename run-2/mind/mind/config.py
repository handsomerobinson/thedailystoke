"""Central configuration: where runtime state lives, and default limits.

Decision: all mutable runtime state (memory DB, audit log, schedules, note
files, sandbox scratch dirs) lives under one gitignored data directory so a
fresh checkout has zero persisted state and every run is reproducible.
"""
from __future__ import annotations

import os
from pathlib import Path


def _default_data_dir() -> Path:
    # Decision: honor MIND_DATA_DIR env var so tests/CI can isolate state,
    # default to <project>/data.
    override = os.environ.get("MIND_DATA_DIR")
    if override:
        return Path(override)
    return Path(__file__).resolve().parent.parent / "data"


DATA_DIR = _default_data_dir()
MEMORY_DIR = DATA_DIR / "memory"
AUDIT_LOG_PATH = DATA_DIR / "audit.log.jsonl"
SCHEDULE_STORE_PATH = DATA_DIR / "schedules.json"
NOTES_DIR = DATA_DIR / "notes"
SANDBOX_DIR = DATA_DIR / "sandbox"

# Decision: hard defaults for cost-awareness so a runaway loop cannot spend
# unbounded (simulated) money even if a caller forgets to set a cap.
DEFAULT_TASK_COST_CAP_USD = 0.50
DEFAULT_MAX_REFLECTION_RETRIES = 3

# Decision: tool execution timeouts/output caps live here so every tool
# obeys the same ceiling unless it has a good reason to override it.
DEFAULT_TOOL_TIMEOUT_SECONDS = 5
DEFAULT_TOOL_OUTPUT_CAP_BYTES = 4096


def ensure_data_dirs() -> None:
    for d in (DATA_DIR, MEMORY_DIR, NOTES_DIR, SANDBOX_DIR):
        d.mkdir(parents=True, exist_ok=True)
