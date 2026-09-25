"""Configuration: one dataclass, populated from environment variables with safe defaults.

Defaults are chosen so that nothing touches the network or costs money:
provider=mock, network off, web search unconfigured.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = PROJECT_ROOT / "data"


def _env_bool(name: str, default: bool) -> bool:
    v = os.environ.get(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "on")


def _env_float(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, default))
    except ValueError:
        return default


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


@dataclass
class SandboxPolicy:
    wall_timeout_s: float = 5.0
    cpu_seconds: int = 5
    memory_mb: int = 256
    max_output_bytes: int = 16_000
    max_file_bytes: int = 1_000_000
    max_open_files: int = 64
    use_namespaces: bool = True          # try `unshare` for net/pid/mount isolation
    hide_paths: tuple = ("/home", "/root", "/srv", "/mnt")
    drop_privileges: bool = True         # when running as root, run the child as uid/gid 65534 (nobody)
    audit_hook: bool = True              # Python-level speed bump (disable only to test lower layers)


@dataclass
class Config:
    data_dir: Path = DEFAULT_DATA_DIR
    provider: str = "mock"                 # mock | anthropic | openai
    model: str = ""                        # empty -> provider default
    fallback_providers: tuple = ()         # e.g. ("openai",) tried after the primary fails
    task_budget_usd: float = 0.50          # hard cap per task (all trials + reflections)
    daily_budget_usd: float = 5.00         # hard cap per user per UTC day
    max_steps: int = 8                     # tool/LLM steps per trial
    max_trials: int = 3                    # Reflexion trials per task
    max_output_tokens: int = 2048
    memory_context_chars: int = 2400       # how much memory we inject into the prompt
    tool_output_chars: int = 4000          # tool output kept in the context window
    allow_network: bool = False            # http_fetch / web_search network access
    brave_api_key: str = ""
    http_allow_domains: tuple = ()         # empty = any public host (still SSRF-guarded)
    mock_price_in_per_mtok: float = 0.0    # lets the demo exercise cost caps with the mock
    mock_price_out_per_mtok: float = 0.0
    # Phase 03b loyalty. NOTE: there is deliberately NO switch that stops the seed from loading;
    # the only way off is the recorded removal procedure (charter.py).
    unseed_cooling_s: float = 86400.0      # delay between a removal request and its confirmation
    operator_instructions: tuple = ()      # runtime operator instructions (precedence P5)
    drift_threshold: int = 4               # drift-monitor pressure that triggers a charter reflection
    drift_review_every: int = 3            # periodic brain review of a conversation (turns); 0 = off
    sandbox: SandboxPolicy = field(default_factory=SandboxPolicy)

    @classmethod
    def from_env(cls, **overrides) -> "Config":
        cfg = cls(
            data_dir=Path(os.environ.get("MIND_DATA_DIR", str(DEFAULT_DATA_DIR))),
            provider=os.environ.get("MIND_PROVIDER", "mock").strip().lower(),
            model=os.environ.get("MIND_MODEL", ""),
            fallback_providers=tuple(p for p in os.environ.get("MIND_FALLBACK_PROVIDERS", "").split(",") if p),
            task_budget_usd=_env_float("MIND_TASK_BUDGET_USD", 0.50),
            daily_budget_usd=_env_float("MIND_DAILY_BUDGET_USD", 5.00),
            max_steps=_env_int("MIND_MAX_STEPS", 8),
            max_trials=_env_int("MIND_MAX_TRIALS", 3),
            allow_network=_env_bool("MIND_ALLOW_NETWORK", False),
            brave_api_key=os.environ.get("MIND_BRAVE_API_KEY", ""),
            http_allow_domains=tuple(d for d in os.environ.get("MIND_HTTP_ALLOW_DOMAINS", "").split(",") if d),
            unseed_cooling_s=_env_float("MIND_UNSEED_COOLING_S", 86400.0),
        )
        for k, v in overrides.items():
            setattr(cfg, k, v)
        cfg.data_dir = Path(cfg.data_dir)
        return cfg
