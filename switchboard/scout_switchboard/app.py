"""HTTP front: carrier webhooks in, a health check, and a read-only admin view.

Run:  uvicorn scout_switchboard.app:app --port 8000
"""
import logging
import os
from typing import Optional

from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request

from . import config
from .brain import Brain, load_brain
from .carriers import Carrier, FakeCarrier, SignatureError, TelnyxCarrier
from .db import Store
from .router import Switchboard

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))


def build_carrier(settings: config.Settings, store: Store) -> Carrier:
    if settings.carrier == "fake":
        return FakeCarrier()
    if settings.carrier == "telnyx":
        if not settings.telnyx_public_key and os.environ.get("SWITCHBOARD_ALLOW_UNSIGNED") != "true":
            # Without the key anyone who finds the URL can make Scout text people on your bill.
            raise RuntimeError("TELNYX_PUBLIC_KEY is required (set SWITCHBOARD_ALLOW_UNSIGNED=true for local testing only)")
        return TelnyxCarrier(settings.telnyx_api_key, settings.telnyx_messaging_profile_id,
                             settings.telnyx_public_key, is_our_line=store.is_our_line)
    raise RuntimeError(f"unknown SWITCHBOARD_CARRIER {settings.carrier!r}")


def create_app(settings: Optional[config.Settings] = None, *, store: Optional[Store] = None,
               carrier: Optional[Carrier] = None, brain: Optional[Brain] = None) -> FastAPI:
    settings = settings or config.load()
    store = store or Store(settings.db_path)
    carrier = carrier or build_carrier(settings, store)
    brain = brain or load_brain(settings.brain)
    board = Switchboard(store, carrier, brain, settings)

    app = FastAPI(title="Scout Switchboard")
    app.state.board = board

    async def webhook(request: Request, background: BackgroundTasks):
        raw = await request.body()
        try:
            carrier.verify(raw, dict(request.headers))
        except SignatureError as exc:
            raise HTTPException(status_code=403, detail=str(exc))
        try:
            event = carrier.parse(raw)
        except ValueError:
            raise HTTPException(status_code=400, detail="unreadable webhook body")
        if event is not None:
            # Acknowledge now; the brain can take longer than the carrier waits for a response.
            background.add_task(board.handle, event)
        return {"ok": True}

    app.add_api_route("/webhooks/telnyx", webhook, methods=["POST"])
    app.add_api_route("/sms", webhook, methods=["POST"])  # the path the original spec used

    @app.get("/health")
    def health():
        return {"ok": True}

    def _admin(authorization: Optional[str]) -> None:
        if not settings.admin_token or authorization != f"Bearer {settings.admin_token}":
            raise HTTPException(status_code=401)

    @app.get("/admin/{slug}/messages")
    def admin_messages(slug: str, limit: int = 100, authorization: Optional[str] = Header(None)):
        _admin(authorization)
        tenant = store.tenant_by_slug(slug)
        if tenant is None:
            raise HTTPException(status_code=404)
        return store.messages(tenant, limit)

    @app.get("/admin/{slug}/roster")
    def admin_roster(slug: str, authorization: Optional[str] = Header(None)):
        _admin(authorization)
        tenant = store.tenant_by_slug(slug)
        if tenant is None:
            raise HTTPException(status_code=404)
        return {
            "members": [m.__dict__ for m in store.members(tenant)],
            "pending": [m.__dict__ for m in store.members(tenant, "pending")],
            "relationships": store.relationships(tenant),
            "notes": store.notes(tenant),
        }

    return app


def __getattr__(name: str):
    # `uvicorn scout_switchboard.app:app` builds the app lazily, so importing this module
    # (e.g. from tests) doesn't need credentials.
    if name == "app":
        return create_app()
    raise AttributeError(name)
