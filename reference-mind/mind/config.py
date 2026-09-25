"""Settings, resolved from arguments and environment variables."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from .util import ensure_dir, safe_user_id

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILD_PROFILE = "guide"  # MC12: this build is the member guide.  A steward build changes this constant, not an env var.


@dataclass
class Settings:
    data_dir: Path = field(default_factory=lambda: Path(os.environ.get("MIND_DATA_DIR", PROJECT_ROOT / "data")))
    max_trials: int = 3
    max_steps: int = 8
    task_budget_usd: float = float(os.environ.get("MIND_TASK_BUDGET_USD", "0.25"))
    daily_budget_usd: float = float(os.environ.get("MIND_DAILY_BUDGET_USD", "2.0"))
    task_max_tokens: int = int(os.environ.get("MIND_TASK_MAX_TOKENS", "60000"))
    task_max_tool_calls: int = 30
    task_max_seconds: float = 300.0
    response_max_tokens: int = 1024
    tool_output_cap: int = 4000
    allow_fast_intervals: bool = False  # tests/demo only: permit intervals < 60s
    # Optional cooling-off between requesting and confirming seed removal (0 = none; set e.g. 86400 in production).
    charter_removal_cooldown_s: float = float(os.environ.get("MIND_CHARTER_REMOVAL_COOLDOWN_S", "0"))
    # BUILD ROUND
    # MC12: the build profile.  "guide" (the shipped member guide) has NO operator-directive input.  "steward" is for
    # steward/operator-side minds and test harnesses; it is chosen in code, never by an environment variable.
    profile: str = BUILD_PROFILE
    # Keys, credentials, anchors and the signed tier registry live OUTSIDE the data dir (MC6, MC16, MC17, MC3).
    trust_dir: Path | None = None
    # MC2: hosts EGRESS tools may reach (comma list).  The configured search backend and webhook are added.
    egress_allow: str = field(default_factory=lambda: os.environ.get("MIND_EGRESS_ALLOW", ""))
    # MC6: "off" (plaintext, disclosed) or "required" (AES-256-GCM via the vetted `cryptography` package, or refuse).
    encryption: str = field(default_factory=lambda: os.environ.get("MIND_ENCRYPTION", "off"))
    # MC1: episodes/transcripts are ephemeral
    episode_ttl_days: float = 30.0

    def __post_init__(self) -> None:
        self.data_dir = Path(self.data_dir)
        if self.trust_dir is None:
            from .trust import Trust
            self.trust_dir = Trust.default_dir(self.data_dir)
        self.trust_dir = Path(self.trust_dir)

    def egress_allowlist(self) -> frozenset:
        import urllib.parse
        hosts = {h.strip().lower() for h in (self.egress_allow or "").split(",") if h.strip()}
        backend = os.environ.get("MIND_SEARCH", "").lower()
        if backend:
            from .tools.web import SEARCH_HOSTS
            hosts.add(SEARCH_HOSTS.get(backend, backend))
        hook = urllib.parse.urlparse(os.environ.get("MIND_WEBHOOK_URL", "")).hostname
        if hook:
            hosts.add(hook.lower())
        return frozenset(hosts)

    def user_dir(self, user_id: str) -> Path:
        return ensure_dir(self.data_dir / "users" / safe_user_id(user_id))

    @property
    def audit_path(self) -> Path:
        return ensure_dir(self.data_dir) / "audit.jsonl"

    @property
    def scheduler_db(self) -> Path:
        return ensure_dir(self.data_dir) / "scheduler.db"

    @property
    def spend_db(self) -> Path:
        return ensure_dir(self.data_dir) / "spend.db"

    @property
    def approvals_db(self) -> Path:
        return ensure_dir(self.data_dir) / "approvals.db"
