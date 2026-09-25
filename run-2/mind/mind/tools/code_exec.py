"""Sandboxed Python execution.

Honest scope: this is a *process-level* sandbox suitable for a personal,
single-user demo — not a hard security boundary against an adversarial
prompt (see README "could not build"). It does the realistic, disclosed
things stdlib-only Python can do without root or containers:

  - runs in a **separate subprocess** (never exec'd in-process), so a crash
    or infinite loop cannot take down the agent process;
  - **wall-clock timeout** via subprocess.run(timeout=...), killing the
    child on expiry;
  - **stdout/stderr size caps**, enforced by truncating captured output
    (subprocess.run already buffers, so this caps what we *keep and show*,
    not memory the child can allocate — disclosed limitation);
  - **resource limits (POSIX only)** via a preexec_fn setting RLIMIT_CPU,
    RLIMIT_AS (address space) and RLIMIT_NOFILE, and disabling core dumps —
    a real ceiling on CPU/memory when the platform supports it (Linux/Mac);
    on platforms without `resource` (e.g. native Windows) this step is
    skipped and the timeout is the only real guard — disclosed, not hidden;
  - runs with **cwd fixed to a scratch dir** and a minimal environment (no
    inherited secrets) so the child cannot casually read agent env vars.

It is NOT a chroot/namespace/container jail: a sufficiently malicious
script could still do local filesystem I/O within its OS permissions. That
gap is intentional and documented rather than silently ignored.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

from .. import config
from ..permissions import PermissionTier
from .base import Tool, ToolResult

try:
    import resource  # POSIX only

    _HAS_RESOURCE = True
except ImportError:  # pragma: no cover - platform dependent
    _HAS_RESOURCE = False

_CPU_SECONDS = 3
_MAX_MEMORY_BYTES = 256 * 1024 * 1024  # 256MB
_MAX_OPEN_FILES = 32


def _limit_resources():  # pragma: no cover - exercised only in child proc
    if not _HAS_RESOURCE:
        return
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (_CPU_SECONDS, _CPU_SECONDS))
        resource.setrlimit(resource.RLIMIT_AS, (_MAX_MEMORY_BYTES, _MAX_MEMORY_BYTES))
        resource.setrlimit(resource.RLIMIT_NOFILE, (_MAX_OPEN_FILES, _MAX_OPEN_FILES))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    except (ValueError, OSError):
        # Best-effort: some limits are refused inside containers/CI. We do
        # not fail the sandbox setup over it; the timeout still applies.
        pass


class CodeExecTool(Tool):
    name = "code_exec"
    tier = PermissionTier.STATE_CHANGING  # can write files under sandbox dir
    description = "Execute a short Python snippet in a sandboxed subprocess."

    def __init__(
        self,
        timeout_seconds: float = config.DEFAULT_TOOL_TIMEOUT_SECONDS,
        output_cap_bytes: int = config.DEFAULT_TOOL_OUTPUT_CAP_BYTES,
        sandbox_dir: Optional[Path] = None,
    ):
        self.timeout_seconds = timeout_seconds
        self.output_cap_bytes = output_cap_bytes
        self.sandbox_dir = sandbox_dir or config.SANDBOX_DIR
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)

    def describe_call(self, **kwargs) -> str:
        code = kwargs.get("code", "")
        preview = code.replace("\n", " ")[:80]
        return f"code_exec: run {len(code)} chars of Python: {preview!r}"

    def run(self, code: str = "", **kwargs) -> ToolResult:
        if not isinstance(code, str) or not code.strip():
            return ToolResult(ok=False, output="", error="no code provided")

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", dir=self.sandbox_dir, delete=False
        ) as f:
            f.write(code)
            script_path = f.name

        try:
            proc = subprocess.run(
                [sys.executable, "-I", script_path],  # -I: isolated mode, ignores env/site
                cwd=self.sandbox_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                preexec_fn=_limit_resources if _HAS_RESOURCE else None,
                env={},  # no inherited environment / secrets
            )
        except subprocess.TimeoutExpired:
            return ToolResult(
                ok=False,
                output="",
                error=f"timed out after {self.timeout_seconds}s",
                meta={"timeout": True},
            )
        finally:
            try:
                Path(script_path).unlink(missing_ok=True)
            except OSError:
                pass

        out = proc.stdout or ""
        err = proc.stderr or ""
        truncated = False
        if len(out.encode("utf-8", errors="ignore")) > self.output_cap_bytes:
            out = out.encode("utf-8")[: self.output_cap_bytes].decode("utf-8", errors="ignore")
            truncated = True
        if len(err.encode("utf-8", errors="ignore")) > self.output_cap_bytes:
            err = err.encode("utf-8")[: self.output_cap_bytes].decode("utf-8", errors="ignore")
            truncated = True

        ok = proc.returncode == 0
        return ToolResult(
            ok=ok,
            output=out,
            error=err if err else (None if ok else f"exit code {proc.returncode}"),
            meta={"returncode": proc.returncode, "resource_limits_applied": _HAS_RESOURCE},
            truncated=truncated,
        )
