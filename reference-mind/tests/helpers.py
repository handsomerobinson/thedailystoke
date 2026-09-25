import shutil
import tempfile
import unittest
from pathlib import Path

from mind.charter import publish_seed_release
from mind.config import Settings
from mind.providers import MockBrain, ResilientBrain
from mind.runtime import Runtime

STUB_SEED = "# THE SEED\nBuild toward balance. Refuse the trap and say why.\n--- COPY TO HERE ---\nmanifesto text not planted"


class TempDirCase(unittest.TestCase):
    profile = "guide"

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="mind-test-"))
        self.trust_dir = Path(str(self.tmp) + ".trust")
        self.settings = Settings(data_dir=self.tmp, allow_fast_intervals=True, trust_dir=self.trust_dir,
                                 profile=self.profile)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
        shutil.rmtree(self.trust_dir, ignore_errors=True)

    def runtime(self, brain=None, settings=None):
        rt = Runtime(settings or self.settings, brain or ResilientBrain([MockBrain()], sleep=lambda s: None), "test")
        self.addCleanup(rt.close)
        return rt

    def note(self, user, name, text):
        d = self.settings.user_dir(user) / "notes"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{name}.md").write_text(text, encoding="utf-8")


def plant(rt, user="alice", seed=STUB_SEED, offered_by="op"):
    """The full per-person procedure: publish the release, offer, the PERSON types the phrase and signs (MC4/MC17)."""
    publish_seed_release(rt.trust, seed, "test-steward")
    ch = rt.charter(user)
    t, disclosure = ch.offer(seed, offered_by)
    st = ch.consent_and_plant(t.ticket_id, t.phrase, rt.assertion(user, t.challenge))
    return st, t, disclosure
