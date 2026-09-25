from mind.demo import run
from tests.helpers import TempDirCase


class DemoTests(TempDirCase):
    def test_demo_end_to_end_all_checks_pass(self):
        checks = run(self.tmp / "demo", quiet=True)
        failed = [k for k, v in checks.items() if not v]
        self.assertEqual(failed, [])
        self.assertGreaterEqual(len(checks), 30)
