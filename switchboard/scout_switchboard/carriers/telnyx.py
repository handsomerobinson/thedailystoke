"""Telnyx Messaging API v2.

Inbound: Telnyx POSTs {"data": {"event_type": "message.received", "id": ..., "payload": {...}}}.
In the payload, `from` is an object and `to` is a LIST of objects (a group MMS has
several), so `payload.to.phone_number` from the original spec does not exist; we
take the entry that is one of our lines. Both shapes are accepted in case Telnyx
changes it.

Signing: headers `telnyx-signature-ed25519` (base64) and `telnyx-timestamp`; the
signed bytes are b"{timestamp}|{raw body}", verified with the account public key
from Portal → Keys & Credentials → Public Key.
"""
import base64
import json
import time
from typing import Callable, Optional

import httpx
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .base import Inbound, SendResult, SignatureError, StatusUpdate

API = "https://api.telnyx.com/v2/messages"
# Reject webhooks older than this, so a captured request cannot be replayed later.
MAX_SKEW_SECONDS = 300


class TelnyxCarrier:
    def __init__(self, api_key: str, messaging_profile_id: str, public_key_b64: str,
                 is_our_line: Callable[[str], bool] = lambda n: True,
                 client: Optional[httpx.Client] = None):
        self.api_key = api_key
        self.messaging_profile_id = messaging_profile_id
        self.public_key = (Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key_b64))
                           if public_key_b64 else None)
        self.is_our_line = is_our_line
        self.client = client or httpx.Client(timeout=15)

    def verify(self, raw_body: bytes, headers: dict[str, str]) -> None:
        if self.public_key is None:
            # Allowed only so local curl tests work; app.py refuses this in production mode.
            return
        h = {k.lower(): v for k, v in headers.items()}
        signature, timestamp = h.get("telnyx-signature-ed25519"), h.get("telnyx-timestamp")
        if not signature or not timestamp:
            raise SignatureError("missing Telnyx signature headers")
        try:
            if abs(time.time() - int(timestamp)) > MAX_SKEW_SECONDS:
                raise SignatureError("stale Telnyx timestamp")
            self.public_key.verify(base64.b64decode(signature), timestamp.encode() + b"|" + raw_body)
        except (InvalidSignature, ValueError) as exc:
            raise SignatureError("bad Telnyx signature") from exc

    def parse(self, raw_body: bytes) -> Inbound | StatusUpdate | None:
        data = json.loads(raw_body).get("data") or {}
        event_type = data.get("event_type", "")
        payload = data.get("payload") or {}
        event_id = data.get("id") or payload.get("id") or ""

        if event_type == "message.received":
            to_entries = payload.get("to") or []
            if isinstance(to_entries, dict):
                to_entries = [to_entries]
            to_numbers = [t.get("phone_number", "") for t in to_entries]
            to_number = next((n for n in to_numbers if self.is_our_line(n)), to_numbers[0] if to_numbers else "")
            return Inbound(
                event_id=event_id,
                message_id=payload.get("id", ""),
                from_number=(payload.get("from") or {}).get("phone_number", ""),
                to_number=to_number,
                text=(payload.get("text") or "").strip(),
                media_urls=[m["url"] for m in payload.get("media") or [] if m.get("url")],
            )
        if event_type in ("message.sent", "message.finalized"):
            to_entries = payload.get("to") or [{}]
            if isinstance(to_entries, dict):
                to_entries = [to_entries]
            return StatusUpdate(event_id=event_id, message_id=payload.get("id", ""),
                                status=to_entries[0].get("status", event_type))
        return None

    def send(self, from_number: str, to_number: str, text: str,
             media_urls: Optional[list[str]] = None) -> SendResult:
        body = {"from": from_number, "to": to_number, "text": text}
        if self.messaging_profile_id:
            body["messaging_profile_id"] = self.messaging_profile_id
        if media_urls:
            body["media_urls"] = media_urls  # turns the text into an MMS
        try:
            resp = self.client.post(API, json=body, headers={"Authorization": f"Bearer {self.api_key}"})
        except httpx.HTTPError as exc:
            return SendResult(ok=False, error=f"network: {exc}")
        if resp.status_code >= 300:
            return SendResult(ok=False, error=f"telnyx {resp.status_code}: {resp.text[:300]}")
        return SendResult(ok=True, message_id=(resp.json().get("data") or {}).get("id"))
