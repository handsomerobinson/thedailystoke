import shutil
import tempfile
import unittest
from pathlib import Path

from mind.config import Settings
from mind.providers import MockBrain, ResilientBrain
from mind.runtime import Runtime


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="mind-test-"))
        self.settings = Settings(data_dir=self.tmp, allow_fast_intervals=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def runtime(self, brain=None):
        rt = Runtime(self.settings, brain or ResilientBrain([MockBrain()], sleep=lambda s: None), "test")
        self.addCleanup(rt.close)
        return rt

    def note(self, user, name, text):
        d = self.settings.user_dir(user) / "notes"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{name}.md").write_text(text, encoding="utf-8")
