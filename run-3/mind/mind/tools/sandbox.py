"""Out-of-process Python execution with layered, best-effort containment.

Layers (each one is independent; all that are available are used):
  1. separate process, `python -I -S -B` (isolated mode, no site, no env vars)
  2. throwaway temp working directory, deleted afterwards
  3. empty environment (no API keys leak into user code)
  4. rlimits: CPU seconds, address space, file size, open files, no core dumps
  5. wall-clock timeout; the whole process group is killed
  6. PEP 578 audit hook installed before user code runs: blocks sockets,
     subprocess/exec/fork/kill, ctypes, writes outside the temp dir, and reads
     outside the temp dir + the Python installation (so code cannot read
     other users' memory files)
  7. `unshare -n` (empty network namespace) when the host allows it
  8. stdout/stderr go to files capped by RLIMIT_FSIZE, then truncated

HONEST LIMIT: this is NOT a security boundary against a determined attacker
(CPython interpreter bugs, resource side channels, and whatever the host
allows).  For hostile code use a VM/container/gVisor/Firecracker.  It is a
strong guard against an LLM's accidental or casual misuse.
"""
from __future__ import annotations

import os
import resource
import shutil
import signal
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field

PRELUDE = r'''
import sys, os
_root = os.path.realpath(os.getcwd())
_deny = [os.path.realpath(p) for p in sys.argv[2:]]
_read_ok = [_root] + sorted({os.path.realpath(p) for p in (sys.prefix, sys.base_prefix, sys.exec_prefix) if p}) + \
    ["/usr/share/zoneinfo", "/etc/localtime", "/dev/null", "/dev/urandom"]
_BLOCK = {"socket.connect", "socket.bind", "socket.sendto", "socket.sendmsg", "socket.__new__",
          "subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "os.spawn", "os.fork",
          "os.forkpty", "os.kill", "os.killpg", "pty.spawn", "ctypes.dlopen", "ctypes.dlsym",
          "ctypes.cdata", "webbrowser.open", "os.startfile", "sys.setprofile"}
_BLOCK_MODS = {"ctypes", "_ctypes", "socket", "_socket", "subprocess", "multiprocessing",
               "_posixsubprocess", "pty", "urllib", "http", "ftplib", "smtplib", "ssl", "_ssl"}
_PATH_EVENTS = {"os.remove", "os.rename", "os.rmdir", "os.mkdir", "shutil.rmtree", "shutil.move",
                "os.chmod", "os.chown", "os.link", "os.symlink", "os.truncate", "os.utime", "shutil.copyfile"}
def _real(p):
    try:
        return os.path.realpath(os.fsdecode(p))
    except Exception:
        return None
def _under(rp, roots):
    return rp is not None and any(rp == r or rp.startswith(r.rstrip(os.sep) + os.sep) for r in roots)
def _hook(event, args):
    if event in ("open", "os.listdir", "os.scandir") and args and isinstance(args[0], (str, bytes, os.PathLike)):
        if _under(_real(args[0]), _deny):
            raise PermissionError("sandbox: that path is off limits")
    if event in _BLOCK:
        raise PermissionError("sandbox: '%s' is blocked" % event)
    if event == "import":
        if args[0] and args[0].split(".")[0] in _BLOCK_MODS:
            raise ImportError("sandbox: import of '%s' is blocked" % args[0])
    elif event == "open":
        path, mode, flags = (list(args) + [None, None, 0])[:3]
        if isinstance(path, int) or path is None:
            return
        rp = _real(path)
        writing = bool(mode and any(c in str(mode) for c in "wax+")) or bool((flags or 0) & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC))
        if writing and not _under(rp, [_root]):
            raise PermissionError("sandbox: writing outside the sandbox directory is blocked")
        if not writing and not _under(rp, _read_ok):
            raise PermissionError("sandbox: reading %s is blocked" % path)
    elif event in ("os.listdir", "os.scandir"):
        p = args[0] if args else "."
        if isinstance(p, int):
            return
        if not _under(_real(p if p is not None else "."), _read_ok):
            raise PermissionError("sandbox: listing that directory is blocked")
    elif event in _PATH_EVENTS:
        for a in args[:2]:
            if isinstance(a, (str, bytes, os.PathLike)) and not _under(_real(a), [_root]):
                raise PermissionError("sandbox: '%s' outside the sandbox directory is blocked" % event)
sys.addaudithook(_hook)
with open(sys.argv[1], encoding="utf-8") as _f:
    _src = _f.read()
_g = {"__name__": "__main__", "__builtins__": __builtins__}
exec(compile(_src, "<sandbox>", "exec"), _g)
'''

_NETNS_PROBE: bool | None = None


def netns_available() -> bool:
    """Probe once whether `unshare -n` works here (needs root or user namespaces)."""
    global _NETNS_PROBE
    if os.environ.get("MIND_SANDBOX_NETNS", "1") == "0":
        return False
    if _NETNS_PROBE is None:
        exe = shutil.which("unshare")
        if not exe:
            _NETNS_PROBE = False
        else:
            try:
                _NETNS_PROBE = subprocess.run([exe, "-n", "true"], capture_output=True, timeout=5).returncode == 0
            except (OSError, subprocess.SubprocessError):
                _NETNS_PROBE = False
    return _NETNS_PROBE


@dataclass
class SandboxResult:
    exit_code: int | None
    stdout: str
    stderr: str
    timed_out: bool = False
    layers: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.timed_out

    def render(self, cap: int = 3000) -> str:
        parts = []
        if self.timed_out:
            parts.append("TIMED OUT (process killed)")
        parts.append(f"exit code: {self.exit_code}")
        if self.stdout:
            parts.append("stdout:\n" + self.stdout[:cap])
        if self.stderr:
            parts.append("stderr:\n" + self.stderr[-cap:])
        return "\n".join(parts)


def run_python(code: str, timeout: float = 10.0, memory_mb: int = 512, output_cap: int = 20000,
               stdin: str = "", deny_paths: list[str] | None = None) -> SandboxResult:
    """deny_paths: extra paths that stay unreadable even if under an allowed root
    (the agent passes its data dir, so code can never read any user's memory)."""
    workdir = tempfile.mkdtemp(prefix="mind-sbx-")
    layers = ["subprocess", "isolated-mode", "empty-env", "tempdir", "timeout", "audit-hook"]
    try:
        src = os.path.join(workdir, "main.py")
        with open(src, "w", encoding="utf-8") as fh:
            fh.write(code)
        out_path, err_path = os.path.join(workdir, ".stdout"), os.path.join(workdir, ".stderr")
        cpu = max(1, int(timeout) + 1)

        def limits() -> None:  # runs in the child between fork and exec
            os.setsid()
            for res, val in ((resource.RLIMIT_CPU, cpu),
                             (resource.RLIMIT_AS, memory_mb * 1024 * 1024),
                             (resource.RLIMIT_FSIZE, output_cap * 4 + 65536),
                             (resource.RLIMIT_NOFILE, 64),
                             (resource.RLIMIT_CORE, 0)):
                try:
                    resource.setrlimit(res, (val, val))
                except (ValueError, OSError):
                    pass

        layers.append("rlimits")
        cmd = [sys.executable, "-I", "-S", "-B", "-c", PRELUDE, src, *[str(p) for p in (deny_paths or [])]]
        if netns_available():
            cmd = [shutil.which("unshare") or "unshare", "-n", "--"] + cmd
            layers.append("no-network-namespace")
        with open(out_path, "wb") as out, open(err_path, "wb") as err:
            try:
                proc = subprocess.Popen(cmd, cwd=workdir, env={"PYTHONIOENCODING": "utf-8", "LANG": "C.UTF-8"},
                                        stdin=subprocess.PIPE, stdout=out, stderr=err, preexec_fn=limits)
            except OSError as exc:
                return SandboxResult(None, "", f"could not start sandbox: {exc}", layers=layers)
            timed_out = False
            try:
                proc.communicate(stdin.encode(), timeout=timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    proc.kill()
                proc.wait()
        def read(p: str) -> str:
            with open(p, "rb") as fh:
                data = fh.read(output_cap + 1)
            text = data[:output_cap].decode("utf-8", "replace")
            return text + ("\n...[output truncated]" if len(data) > output_cap else "")
        stderr = read(err_path)
        # Hide the prelude frame from tracebacks: it is noise for the brain.
        stderr = "\n".join(l for l in stderr.splitlines() if 'File "<string>"' not in l)
        return SandboxResult(proc.returncode, read(out_path), stderr, timed_out, layers)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
