import unittest

from mind.tools.sandbox import run_python


class SandboxTests(unittest.TestCase):
    def test_runs_code(self):
        r = run_python("print(sum(range(10)))")
        self.assertTrue(r.ok)
        self.assertEqual(r.stdout.strip(), "45")

    def test_timeout_kills(self):
        r = run_python("while True: pass", timeout=1)
        self.assertTrue(r.timed_out)
        self.assertFalse(r.ok)

    def test_blocks_network_subprocess_ctypes(self):
        for code in ("import socket", "import subprocess", "import ctypes",
                     "import os; os.system('echo hi')", "import os; os.fork()",
                     "__import__('_socket')", "import urllib.request"):
            r = run_python(code, timeout=5)
            self.assertFalse(r.ok, code)
            self.assertIn("sandbox", r.stderr, code)

    def test_filesystem_confinement(self):
        self.assertIn("blocked", run_python("open('/etc/passwd').read()").stderr)
        self.assertIn("blocked", run_python("open('/tmp/mind-escape.txt','w').write('x')").stderr)
        self.assertIn("blocked", run_python("import os; os.listdir('/')").stderr)
        self.assertIn("blocked", run_python("import os; os.remove('/tmp/whatever')").stderr)
        r = run_python("open('local.txt','w').write('ok'); print(open('local.txt').read())")
        self.assertEqual(r.stdout.strip(), "ok")

    def test_env_is_empty(self):
        r = run_python("import os; print(sorted(os.environ))")
        self.assertNotIn("KEY", r.stdout)
        self.assertNotIn("PATH'", r.stdout)

    def test_memory_limit(self):
        r = run_python("x = bytearray(2 * 1024 ** 3)", memory_mb=256)
        self.assertFalse(r.ok)
        self.assertIn("MemoryError", r.stderr)

    def test_output_capped(self):
        r = run_python("print('x' * 100000)", output_cap=1000)
        self.assertLessEqual(len(r.stdout), 1100)
        self.assertIn("truncated", r.stdout)

    def test_stdlib_still_works(self):
        r = run_python("import json, re, math, statistics, datetime, collections; print(statistics.mean([1,2,3]))")
        self.assertEqual(r.stdout.strip(), "2")


class DenyPathTests(unittest.TestCase):
    def test_deny_paths_override_allowed_roots(self):
        import sys
        target = sys.prefix  # normally readable (stdlib lives there)
        r = run_python(f"import os; print(os.listdir({target!r}))", deny_paths=[target])
        self.assertIn("off limits", r.stderr)
        self.assertTrue(run_python(f"import os; print(os.listdir({target!r}))").ok)
