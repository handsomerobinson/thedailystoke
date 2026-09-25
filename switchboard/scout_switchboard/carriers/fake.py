"""A carrier that texts nobody: records sends and prints them. For tests and local dev."""
import itertools
import json
from typing import Optional

from .base import Inbound, SendResult, StatusUpdate


class FakeCarrier:
    def __init__(self, echo: bool = True):
        self.sent: list[dict] = []
        self.echo = echo
        self._ids = itertools.count(1)

    def verify(self, raw_body: bytes, headers: dict[str, str]) -> None:
        return None

    def parse(self, raw_body: bytes) -> Inbound | StatusUpdate | None:
        # Accepts the same body shape as Telnyx so the simulator can post real-looking payloads.
        from .telnyx import TelnyxCarrier
        return TelnyxCarrier("", "", "").parse(raw_body)

    def send(self, from_number: str, to_number: str, text: str,
             media_urls: Optional[list[str]] = None) -> SendResult:
        msg_id = f"fake-{next(self._ids)}"
        record = {"id": msg_id, "from": from_number, "to": to_number, "text": text, "media_urls": media_urls or []}
        self.sent.append(record)
        if self.echo:
            print("OUTBOUND", json.dumps(record))
        return SendResult(ok=True, message_id=msg_id)
