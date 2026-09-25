"""Subprocess sandbox for untrusted Python.

Layers (each one is reported in `SandboxResult.isolation` so callers know what they got):

1. Separate process: `python -I -S -B` (isolated mode: no env vars, no user site, no cwd on path).
2. rlimits: CPU seconds, address space, max file size, open files, no core dumps, nproc.
3. Wall-clock timeout that SIGKILLs the whole process group.
4. Output capped while streaming (the child cannot flood our memory).
5. Scrubbed environment (no API keys reach the child), throwaway temp dir as cwd, deleted after.
6. If `unshare` works: new user + network + pid + mount namespaces — no network interfaces,
   no view of host processes, the temp dir is bind-mounted over /tmp and /home, /root, the
   data dir etc. are hidden behind empty tmpfs mounts.
7. A Python audit hook installed before user code runs, blocking sockets, subprocess/exec/fork,
   ctypes, and file writes/deletes outside the work dir.

HONEST LIMITS: layer 7 is a speed bump, not a boundary (CPython audit hooks can be defeated by
a determined attacker). Without layer 6 the child can read any file the parent user can read
and can use the network. We run as root in this container, so RLIMIT_NPROC does not stop fork
bombs there (layer 7 blocks os.fork, which is the practical mitigation). This is not a
seccomp/gVisor/Firecracker-grade sandbox; for hostile multi-tenant use, run it inside one.
"""
from __future__ import annotations

import os
import resource
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

from .config import SandboxPolicy

_PRELUDE = r'''
import sys, os
_WORK = os.path.realpath(os.getcwd())
_BLOCK_EVENTS = {
    "socket.connect", "socket.bind", "socket.sendto", "socket.sendmsg", "socket.getaddrinfo",
    "subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "os.spawn", "os.fork",
    "os.forkpty", "pty.spawn", "ctypes.dlopen", "ctypes.dlsym", "os.kill", "os.killpg",
    "os.putenv", "os.unsetenv", "sys.addaudithook",
}
_PATH_EVENTS = {"os.remove", "os.rename", "os.rmdir", "os.mkdir", "os.chmod", "os.chown",
                "os.link", "os.symlink", "os.truncate", "os.utime", "shutil.rmtree", "shutil.move"}
_BLOCK_IMPORTS = {"ctypes", "_ctypes", "cffi", "_posixsubprocess"}

def _inside(p):
    try:
        p = os.fsdecode(p) if not isinstance(p, int) else None
    except Exception:
        return False
    if p is None:
        return True  # file descriptor: already opened, was checked at open time
    rp = os.path.realpath(p)
    return rp == _WORK or rp.startswith(_WORK + os.sep)

def _hook(event, args):
    if event in _BLOCK_EVENTS:
        raise PermissionError(f"sandbox: {event} is not allowed")
    if event == "import" and args and str(args[0]).split(".")[0] in _BLOCK_IMPORTS:
        raise PermissionError(f"sandbox: importing {args[0]} is not allowed")
    if event == "open" and len(args) >= 2:
        path, mode = args[0], args[1]
        writing = False
        if isinstance(mode, str):
            writing = any(c in mode for c in "wax+")
        elif isinstance(mode, int):
            writing = bool(mode & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC))
        if writing and not _inside(path):
            raise PermissionError(f"sandbox: writing outside the work dir is not allowed: {path}")
    if event in _PATH_EVENTS and args:
        for a in args[:2]:
            if isinstance(a, (str, bytes, os.PathLike)) and not _inside(a):
                raise PermissionError(f"sandbox: {event} outside the work dir is not allowed")

_post = None
if os.path.exists("post_code.py"):          # evaluator harness: read, then deleted from disk
    _post = open("post_code.py", encoding="utf-8").read()
    os.remove("post_code.py")
if os.environ.get("MIND_SBX_HOOK", "1") == "1":
    sys.addaudithook(_hook)
del _hook
_src = open("user_code.py", encoding="utf-8").read()
_g = {"__name__": "__main__", "__builtins__": __builtins__}
exec(compile(_src, "user_code.py", "exec"), _g)
if _post is not None:
    exec(compile(_post, "post_code.py", "exec"), _g)
'''


@dataclass
class SandboxResult:
    stdout: str
    stderr: str
    returncode: int | None
    timed_out: bool = False
    truncated: bool = False
    duration_s: float = 0.0
    limit_hit: str = ""           # "", "wall-timeout", "cpu", "memory", "output"
    isolation: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.returncode == 0 and not self.timed_out

    def summary(self, limit: int = 4000) -> str:
        parts = []
        err_lines = [ln for ln in self.stderr.strip().splitlines() if ln.strip()]
        if self.returncode != 0 and err_lines:
            parts.append(f"error: {err_lines[-1].strip()[:300]}")
        if self.stdout:
            parts.append(self.stdout[:limit])
        if self.stderr:
            parts.append("[stderr]\n" + self.stderr[-limit:])
        if self.limit_hit:
            parts.append(f"[sandbox limit hit: {self.limit_hit}]")
        if self.truncated:
            parts.append("[output truncated]")
        parts.append(f"[exit code {self.returncode}]")
        return "\n".join(parts)


_NS_PROBE: dict = {}


def namespaces_available() -> bool:
    """Probe once whether unprivileged/root `unshare` with user+net+pid+mount namespaces works."""
    if "ok" in _NS_PROBE:
        return _NS_PROBE["ok"]
    ok = False
    exe = shutil.which("unshare")
    if exe and sys.platform.startswith("linux"):
        try:
            def as_nobody():
                if os.geteuid() == 0:
                    os.setgroups([])
                    os.setgid(NOBODY)
                    os.setuid(NOBODY)
            r = subprocess.run([exe, "-rnpfm", "--mount-proc", "true"], capture_output=True, timeout=5,
                               preexec_fn=as_nobody)
            ok = r.returncode == 0
        except Exception:
            ok = False
    _NS_PROBE["ok"] = ok
    return ok


NOBODY = 65534


def _limits(policy: SandboxPolicy, drop: bool):
    def apply():
        os.setsid()
        if drop:  # root in the parent must not mean root-owned host files are writable by the child
            os.setgroups([])
            os.setgid(NOBODY)
            os.setuid(NOBODY)
        cpu = max(1, int(policy.cpu_seconds))
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu + 1))
        mem = policy.memory_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (mem, mem))
        resource.setrlimit(resource.RLIMIT_FSIZE, (policy.max_file_bytes, policy.max_file_bytes))
        resource.setrlimit(resource.RLIMIT_NOFILE, (policy.max_open_files, policy.max_open_files))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        try:
            resource.setrlimit(resource.RLIMIT_NPROC, (64, 64))
        except (ValueError, OSError):
            pass
    return apply


def _drain(stream, cap: int, sink: dict):
    buf = bytearray()
    total = 0
    try:
        while True:
            chunk = stream.read(4096)
            if not chunk:
                break
            total += len(chunk)
            if len(buf) < cap:
                buf.extend(chunk[: cap - len(buf)])
    except Exception:
        pass
    sink["data"] = bytes(buf)
    sink["total"] = total


def run_python(code: str, policy: SandboxPolicy | None = None, extra_hide: tuple = (),
               stdin_text: str = "", post_code: str = "") -> SandboxResult:
    """Run `code`; if `post_code` is given it runs afterwards in the same namespace, but its
    source is removed from disk before `code` starts (used by the evaluator harness)."""
    policy = policy or SandboxPolicy()
    work = tempfile.mkdtemp(prefix="mind-sbx-")
    use_ns = policy.use_namespaces and namespaces_available()
    exe = os.path.realpath(sys.executable)
    isolation = {
        "process": True, "rlimits": True, "env_scrubbed": True, "audit_hook": True,
        "namespaces": use_ns, "network_blocked": use_ns, "host_fs_hidden": [],
        "note": "" if use_ns else "unshare unavailable: child can read host files and reach the network "
                                  "(audit hook only blocks the obvious Python-level paths)",
    }
    try:
        Path(work, "user_code.py").write_text(code, encoding="utf-8")
        Path(work, "runner.py").write_text(_PRELUDE, encoding="utf-8")
        if post_code:
            Path(work, "post_code.py").write_text(post_code, encoding="utf-8")
        drop = bool(policy.drop_privileges and hasattr(os, "geteuid") and os.geteuid() == 0)
        if drop:
            for f in [work] + [os.path.join(work, n) for n in os.listdir(work)]:
                os.chown(f, NOBODY, NOBODY)
        isolation["uid"] = NOBODY if drop else os.geteuid()
        env = {"PATH": "/usr/bin:/bin", "HOME": "/tmp" if use_ns else work, "TMPDIR": "/tmp" if use_ns else work,
               "LANG": "C.UTF-8", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1",
               "MIND_SBX_HOOK": "1" if policy.audit_hook else "0"}
        py = [exe, "-I", "-S", "-B", "runner.py"]
        if use_ns:
            hide = []
            cands = sorted({os.path.realpath(p) for p in tuple(policy.hide_paths) + tuple(str(x) for x in extra_hide)},
                           key=len)
            for rp in cands:
                if not os.path.isdir(rp) or rp == "/" or exe.startswith(rp + os.sep):
                    continue
                if any(rp == h or rp.startswith(h + os.sep) for h in hide + ["/tmp"]):
                    continue  # already hidden by a parent mount (/tmp is replaced by the work dir)
                if work == rp or work.startswith(rp + os.sep):
                    continue  # never hide our own work dir
                hide.append(rp)
            isolation["host_fs_hidden"] = hide
            mounts = [f"mount --bind '{work}' /tmp"] + [f"mount -t tmpfs -o size=1m,mode=755 none '{h}'" for h in hide]
            script = " && ".join(mounts + ["cd /tmp", " ".join(f"'{a}'" for a in py)])
            cmd = [shutil.which("unshare") or "unshare", "-rnpfm", "--mount-proc", "/bin/sh", "-c", script]
            cwd = "/"
        else:
            cmd, cwd = py, work
        t0 = time.monotonic()
        proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=subprocess.PIPE if stdin_text else subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=_limits(policy, drop),
                                close_fds=True)
        if stdin_text:
            try:
                proc.stdin.write(stdin_text.encode()[:policy.max_output_bytes])
                proc.stdin.close()
            except Exception:
                pass
        out, err = {}, {}
        threads = [threading.Thread(target=_drain, args=(proc.stdout, policy.max_output_bytes, out), daemon=True),
                   threading.Thread(target=_drain, args=(proc.stderr, policy.max_output_bytes, err), daemon=True)]
        for t in threads:
            t.start()
        timed_out = False
        try:
            proc.wait(timeout=policy.wall_timeout_s)
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.wait()
        for t in threads:
            t.join(timeout=2)
        for stream in (proc.stdout, proc.stderr):
            try:
                stream.close()
            except Exception:
                pass
        dur = time.monotonic() - t0
        stdout = out.get("data", b"").decode("utf-8", "replace")
        stderr = err.get("data", b"").decode("utf-8", "replace")
        truncated = out.get("total", 0) > policy.max_output_bytes or err.get("total", 0) > policy.max_output_bytes
        rc = proc.returncode
        limit = ""
        if timed_out:
            limit = "wall-timeout"
        elif rc is not None and rc in (-signal.SIGXCPU, 128 + signal.SIGXCPU, -signal.SIGKILL, 128 + signal.SIGKILL) and dur >= policy.cpu_seconds * 0.8:
            limit = "cpu"
        elif "MemoryError" in stderr or (rc is not None and rc < 0 and dur < policy.cpu_seconds * 0.8
                                         and rc == -signal.SIGKILL):
            limit = "memory"
        elif "File size limit exceeded" in stderr or rc in (-signal.SIGXFSZ,):
            limit = "file-size"
        elif truncated:
            limit = "output"
        return SandboxResult(stdout, stderr, rc, timed_out, truncated, round(dur, 3), limit, isolation)
    except Exception as e:  # sandbox infrastructure failure: report, never raise into the agent loop
        return SandboxResult("", f"sandbox error: {type(e).__name__}: {e}", None, False, False, 0.0,
                             "sandbox-error", isolation)
    finally:
        shutil.rmtree(work, ignore_errors=True)
