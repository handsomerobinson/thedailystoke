"""What the switchboard needs from any messaging carrier.

Telnyx is the first one. Twilio, WhatsApp Cloud API or an iMessage bridge plug
in by implementing the same three methods, and nothing above this layer changes.
"""
from dataclasses import dataclass, field
from typing import Optional, Protocol


@dataclass(frozen=True)
class Inbound:
    event_id: str          # carrier's webhook event id, used for de-duplication
    message_id: str
    from_number: str       # E.164, e.g. +15551234567
    to_number: str         # our line
    text: str
    media_urls: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class StatusUpdate:
    event_id: str
    message_id: str
    status: str            # e.g. queued, sent, delivered, delivery_failed


@dataclass(frozen=True)
class SendResult:
    ok: bool
    message_id: Optional[str] = None
    error: Optional[str] = None


class SignatureError(Exception):
    pass


class Carrier(Protocol):
    def verify(self, raw_body: bytes, headers: dict[str, str]) -> None:
        """Raise SignatureError unless the webhook really came from the carrier."""

    def parse(self, raw_body: bytes) -> Inbound | StatusUpdate | None:
        """Turn a webhook body into an event we care about, or None to ignore it."""

    def send(self, from_number: str, to_number: str, text: str,
             media_urls: Optional[list[str]] = None) -> SendResult:
        ...
