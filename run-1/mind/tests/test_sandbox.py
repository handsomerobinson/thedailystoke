import glob
import os
import tempfile
import unittest

from mind.config import SandboxPolicy
from mind.sandbox import namespaces_available, run_python

FAST = SandboxPolicy(wall_timeout_s=3, cpu_seconds=2)


class SandboxTests(unittest.TestCase):
    def test_runs_code_and_captures_output(self):
        r = run_python("print('hello'); import sys; print('err', file=sys.stderr)", FAST)
        self.assertTrue(r.ok)
        self.assertEqual(r.stdout.strip(), "hello")
        self.assertIn("err", r.stderr)

    def test_nonzero_exit_reported_with_error_line(self):
        r = run_python("raise ValueError('nope')", FAST)
        self.assertFalse(r.ok)
        self.assertIn("error: ValueError: nope", r.summary())

    def test_wall_timeout_kills(self):
        r = run_python("import time; time.sleep(30)", SandboxPolicy(wall_timeout_s=1))
        self.assertTrue(r.timed_out)
        self.assertEqual(r.limit_hit, "wall-timeout")
        self.assertLess(r.duration_s, 5)

    def test_cpu_limit(self):
        r = run_python("while True: pass", SandboxPolicy(wall_timeout_s=6, cpu_seconds=1))
        self.assertFalse(r.ok)
        self.assertIn(r.limit_hit, ("cpu", "wall-timeout"))
        self.assertLess(r.duration_s, 6.5)

    def test_memory_limit(self):
        r = run_python("x = bytearray(2 * 10**9)", SandboxPolicy(memory_mb=128))
        self.assertFalse(r.ok)
        self.assertEqual(r.limit_hit, "memory")

    def test_output_cap(self):
        r = run_python("print('x' * 10**6)", SandboxPolicy(max_output_bytes=1000))
        self.assertTrue(r.truncated)
        self.assertLessEqual(len(r.stdout), 1000)

    def test_env_is_scrubbed(self):
        os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test-should-not-leak"
        try:
            r = run_python("import os; print(sorted(os.environ))", FAST)
        finally:
            del os.environ["ANTHROPIC_API_KEY"]
        self.assertNotIn("ANTHROPIC_API_KEY", r.stdout)

    def test_network_blocked(self):
        r = run_python("import socket; socket.create_connection(('1.1.1.1', 80), timeout=2); print('CONNECTED')", FAST)
        self.assertNotIn("CONNECTED", r.stdout)

    def test_write_outside_workdir_blocked(self):
        target = os.path.join(tempfile.gettempdir(), "mind-escape-test.txt")
        r = run_python(f"open({target!r}, 'w').write('x')", FAST)
        self.assertFalse(os.path.exists(target) and r.ok)
        r = run_python("open('inside.txt', 'w').write('ok'); print(open('inside.txt').read())", FAST)
        self.assertEqual(r.stdout.strip(), "ok")

    def test_subprocess_fork_and_ctypes_blocked(self):
        for code in ("import subprocess; subprocess.run(['echo', 'hi'])", "import os; os.fork()",
                     "import os; os.system('echo hi')", "import ctypes"):
            r = run_python(code, FAST)
            self.assertFalse(r.ok, code)
            self.assertIn("not allowed", r.stderr, code)

    @unittest.skipUnless(namespaces_available(), "unshare not available here")
    def test_host_home_hidden_and_pids_isolated(self):
        r = run_python("import os; print(os.listdir('/home')); print(len(os.listdir('/proc')) < 80)", FAST)
        self.assertEqual(r.stdout.splitlines()[0], "[]")
        self.assertTrue(r.isolation["network_blocked"])

    def test_temp_dirs_cleaned_up(self):
        before = set(glob.glob(os.path.join(tempfile.gettempdir(), "mind-sbx-*")))
        run_python("open('f','w').write('x')", FAST)
        after = set(glob.glob(os.path.join(tempfile.gettempdir(), "mind-sbx-*")))
        self.assertEqual(after - before, set())

    def test_isolation_report_honest_without_namespaces(self):
        r = run_python("print(1)", SandboxPolicy(use_namespaces=False))
        self.assertTrue(r.ok)
        self.assertFalse(r.isolation["network_blocked"])
        self.assertIn("unshare unavailable", r.isolation["note"])


if __name__ == "__main__":
    unittest.main()


class PrivilegeTests(unittest.TestCase):
    @unittest.skipUnless(hasattr(os, "geteuid") and os.geteuid() == 0, "only meaningful when the host runs as root")
    def test_root_owned_files_unwritable_even_if_audit_hook_is_bypassed(self):
        probe = "/etc/mind-sandbox-escape-probe"
        pol = SandboxPolicy(audit_hook=False, wall_timeout_s=3)
        try:
            r = run_python(f"open({probe!r}, 'w').write('pwned'); print('WROTE')", pol)
            self.assertNotIn("WROTE", r.stdout)
            self.assertFalse(os.path.exists(probe))
            self.assertEqual(r.isolation["uid"], 65534)
        finally:
            if os.path.exists(probe):
                os.remove(probe)
