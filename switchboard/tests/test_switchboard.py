import base64
import json
import time
from pathlib import Path
from types import SimpleNamespace

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from fastapi.testclient import TestClient

from scout_switchboard import config
from scout_switchboard.app import create_app
from scout_switchboard.brain import DevBrain
from scout_switchboard.carriers import FakeCarrier, Inbound, SignatureError, TelnyxCarrier
from scout_switchboard.db import Store
from scout_switchboard.router import Switchboard
from scout_switchboard.scout_brain import ScoutBrain
from scout_switchboard.seed import load_seed

SEED = Path(__file__).resolve().parent.parent / "seeds" / "chester.example.json"
CHESTER, CHRISTY, ADAM, RYAN = "+15551234567", "+15557654321", "+15557650000", "+15559876543"
CHESTER_LINE, TENFOUR_LINE = "+15550000001", "+15550000002"
STRANGER = "+15550009999"


@pytest.fixture
def settings(tmp_path):
    return config.Settings(db_path=str(tmp_path / "t.db"), carrier="fake", telnyx_api_key="",
                           telnyx_messaging_profile_id="", telnyx_public_key="",
                           brain="scout_switchboard.brain:DevBrain", admin_token="secret",
                           notify_admins_of_unknown=True)


@pytest.fixture
def store(settings):
    s = Store(settings.db_path)
    load_seed(s, SEED)
    return s


@pytest.fixture
def board(store, settings):
    return Switchboard(store, FakeCarrier(echo=False), DevBrain(), settings)


_n = iter(range(10_000))


def text(board, frm, to, body, event_id=None):
    eid = event_id or f"evt-{next(_n)}"
    board.handle_inbound(Inbound(event_id=eid, message_id=f"m-{eid}", from_number=frm, to_number=to, text=body))


def sent_to(board, number):
    return [s["text"] for s in board.carrier.sent if s["to"] == number]


def test_known_sender_gets_reply_from_the_line_they_texted(board):
    text(board, CHESTER, CHESTER_LINE, "hello")
    (reply,) = board.carrier.sent
    assert reply["to"] == CHESTER and reply["from"] == CHESTER_LINE
    assert "Hi Chester (owner)" in reply["text"]
    assert "Christy" in reply["text"]


def test_tell_christy_reaches_christy_and_confirms_to_chester(board):
    text(board, CHESTER, CHESTER_LINE, "tell Christy we're on at 3")
    assert sent_to(board, CHRISTY) == ["Chester says: we're on at 3"]
    assert sent_to(board, CHESTER) == ["Sent to Christy."]


def test_permission_denied_without_reach_edge(board, store):
    tenant = store.tenant_by_slug("chester")
    adam = store.find_member(tenant, "Adam")[0]
    store._x("DELETE FROM reach WHERE from_person = ?", (adam.person_id,))
    text(board, ADAM, CHESTER_LINE, "tell Chester hi")
    assert sent_to(board, CHESTER) == []
    assert "isn't set up to reach Chester" in sent_to(board, ADAM)[0]


def test_admin_reaches_anyone(board):
    text(board, RYAN, CHESTER_LINE, "tell Adam the deck is ready")
    assert sent_to(board, ADAM) == ["Ryan says: the deck is ready"]


def test_tenants_are_isolated(board):
    # Ryan is on both lines. On the TENFOUR line, Chester's people don't exist.
    text(board, RYAN, TENFOUR_LINE, "tell Christy hi")
    assert sent_to(board, CHRISTY) == []
    assert "No one named Christy" in sent_to(board, RYAN)[0]
    # And Chester texting the TENFOUR line is a stranger there.
    text(board, CHESTER, TENFOUR_LINE, "hey")
    assert "Who's this?" in sent_to(board, CHESTER)[0]


def test_group_fan_out(board):
    text(board, CHESTER, CHESTER_LINE, "text the team: dinner at 7")
    assert sent_to(board, CHRISTY) == ["Chester: dinner at 7"]
    assert sent_to(board, ADAM) == ["Chester: dinner at 7"]
    assert sent_to(board, RYAN) == ["Chester: dinner at 7"]


def test_duplicate_webhook_processed_once(board):
    text(board, CHESTER, CHESTER_LINE, "hello", event_id="same")
    text(board, CHESTER, CHESTER_LINE, "hello", event_id="same")
    assert len(board.carrier.sent) == 1


def test_unknown_number_asked_once_and_admin_told(board, store):
    text(board, STRANGER, CHESTER_LINE, "hi is this Chester's assistant?")
    text(board, STRANGER, CHESTER_LINE, "it's Dana from the conference")
    assert sent_to(board, STRANGER) == ["Hi, this is Scout for Chester Elton. I don't have this number yet. Who's this?"]
    admin_notes = sent_to(board, RYAN)
    assert len(admin_notes) == 2 and STRANGER in admin_notes[0]
    assert len(store.unknown_inbound(CHESTER_LINE)) == 2


def test_stop_silences_line_until_start(board):
    text(board, CHRISTY, CHESTER_LINE, "STOP")
    assert board.carrier.sent == []
    text(board, CHESTER, CHESTER_LINE, "tell Christy hi")
    assert sent_to(board, CHRISTY) == []
    assert "opted out" in sent_to(board, CHESTER)[0]
    text(board, CHRISTY, CHESTER_LINE, "hello?")
    assert sent_to(board, CHRISTY) == []
    text(board, CHRISTY, CHESTER_LINE, "START")
    assert "back on" in sent_to(board, CHRISTY)[0]


def test_loop_guard_ignores_our_own_numbers(board):
    text(board, TENFOUR_LINE, CHESTER_LINE, "hello")
    assert board.carrier.sent == []


def test_brain_crash_gets_a_polite_reply(store, settings):
    class Boom:
        def think(self, turn, tools):
            raise RuntimeError("x")
    board = Switchboard(store, FakeCarrier(echo=False), Boom(), settings)
    text(board, CHESTER, CHESTER_LINE, "hi")
    assert "snag" in sent_to(board, CHESTER)[0]


def test_turn_never_contains_phone_numbers(board):
    seen = {}

    class Spy:
        def think(self, turn, tools):
            seen["turn"] = turn
            return None
    board.brain = Spy()
    text(board, CHESTER, CHESTER_LINE, "hi")
    dumped = repr(seen["turn"])
    for number in (CHESTER, CHRISTY, ADAM, RYAN, CHESTER_LINE):
        assert number not in dumped
    assert seen["turn"].session_id.startswith("chester:")


def test_send_budget_per_turn(board, settings):
    class Spammer:
        def think(self, turn, tools):
            return " | ".join(tools.send_text("Christy", "hi") for _ in range(8))
    board.brain = Spammer()
    text(board, CHESTER, CHESTER_LINE, "go")
    assert len(sent_to(board, CHRISTY)) == settings.max_sends_per_turn


# --- Telnyx parsing and signatures ------------------------------------------------

def telnyx_body(frm, to, body, event_id="e1", to_as_list=True):
    to_field = [{"phone_number": to, "status": "webhook_delivered"}] if to_as_list else {"phone_number": to}
    return json.dumps({"data": {"event_type": "message.received", "id": event_id, "payload": {
        "id": "msg1", "from": {"phone_number": frm}, "to": to_field, "text": body,
        "media": [{"url": "https://example.com/a.jpg", "content_type": "image/jpeg"}]}}}).encode()


@pytest.mark.parametrize("to_as_list", [True, False])
def test_telnyx_parse_inbound(to_as_list):
    event = TelnyxCarrier("", "", "").parse(telnyx_body(CHESTER, CHESTER_LINE, " hi ", to_as_list=to_as_list))
    assert event.from_number == CHESTER and event.to_number == CHESTER_LINE and event.text == "hi"
    assert event.media_urls == ["https://example.com/a.jpg"]


def test_telnyx_signature():
    key = Ed25519PrivateKey.generate()
    pub = base64.b64encode(key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)).decode()
    carrier = TelnyxCarrier("", "", pub)
    body, ts = b'{"data":{}}', str(int(time.time()))
    good = base64.b64encode(key.sign(ts.encode() + b"|" + body)).decode()
    carrier.verify(body, {"Telnyx-Signature-Ed25519": good, "Telnyx-Timestamp": ts})
    with pytest.raises(SignatureError):
        carrier.verify(body + b" ", {"Telnyx-Signature-Ed25519": good, "Telnyx-Timestamp": ts})
    with pytest.raises(SignatureError):
        carrier.verify(body, {})
    old = str(int(time.time()) - 3600)
    stale = base64.b64encode(key.sign(old.encode() + b"|" + body)).decode()
    with pytest.raises(SignatureError):
        carrier.verify(body, {"telnyx-signature-ed25519": stale, "telnyx-timestamp": old})


def test_webhook_endpoint_end_to_end(store, settings):
    carrier = FakeCarrier(echo=False)
    client = TestClient(create_app(settings, store=store, carrier=carrier, brain=DevBrain()))
    r = client.post("/webhooks/telnyx", content=telnyx_body(CHESTER, CHESTER_LINE, "tell Christy we're on at 3"))
    assert r.status_code == 200
    assert sent_to(SimpleNamespace(carrier=carrier), CHRISTY) == ["Chester says: we're on at 3"]
    assert client.get("/admin/chester/messages").status_code == 401
    log = client.get("/admin/chester/messages", headers={"Authorization": "Bearer secret"}).json()
    assert {m["via"] for m in log} >= {"tool", "reply"}


# --- starter Scout brain, with a fake Claude client ------------------------------

class FakeClaude:
    """Replays scripted responses: first a send_text tool call, then a final text."""

    def __init__(self):
        self.calls = []
        tool_use = SimpleNamespace(type="tool_use", id="tu1", name="send_text",
                                   input={"to": "Christy", "message": "Chester asked me to tell you: on at 3."})
        self.script = [
            SimpleNamespace(stop_reason="tool_use", content=[tool_use]),
            SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text="Done. Told Christy.")]),
        ]
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        return self.script[len(self.calls) - 1]


def test_scout_brain_tool_loop(store, settings):
    fake = FakeClaude()
    board = Switchboard(store, FakeCarrier(echo=False), ScoutBrain(client=fake), settings)
    text(board, CHESTER, CHESTER_LINE, "tell Christy we're on at 3")
    assert sent_to(board, CHRISTY) == ["Chester asked me to tell you: on at 3."]
    assert sent_to(board, CHESTER) == ["Done. Told Christy."]
    first = fake.calls[0]
    assert first["model"] == "claude-opus-5" and first["fallbacks"] == "default"
    assert "Chester Elton's line" in first["system"][1]["text"]      # brief loaded
    assert CHRISTY not in json.dumps(first["system"])                   # names only
    second = fake.calls[1]["messages"][-1]["content"][0]
    assert second["type"] == "tool_result" and second["content"] == "Sent to Christy."
