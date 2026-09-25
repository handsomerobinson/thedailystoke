import shutil
import tempfile
import unittest
from pathlib import Path

from mind.config import Config
from mind.util import FakeClock


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="mind-test-"))
        self.clock = FakeClock()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def config(self, **kw):
        return Config(data_dir=self.tmp, **kw)
