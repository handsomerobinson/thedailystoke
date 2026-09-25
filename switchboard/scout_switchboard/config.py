"""Settings, read once from the environment."""
import os
from dataclasses import dataclass


def _bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    db_path: str
    carrier: str
    telnyx_api_key: str
    telnyx_messaging_profile_id: str
    telnyx_public_key: str
    brain: str
    admin_token: str
    notify_admins_of_unknown: bool
    # Loop guard: most texts the brain may send to other people in one turn.
    max_sends_per_turn: int = 5
    # Hard cap on any outbound body; carriers split long texts into segments and bill each one.
    max_body_chars: int = 1600
    # How many past messages from this person the brain sees each turn.
    history_limit: int = 20


def load() -> Settings:
    return Settings(
        db_path=os.environ.get("SWITCHBOARD_DB", "switchboard.db"),
        carrier=os.environ.get("SWITCHBOARD_CARRIER", "telnyx"),
        telnyx_api_key=os.environ.get("TELNYX_API_KEY", ""),
        telnyx_messaging_profile_id=os.environ.get("TELNYX_MESSAGING_PROFILE_ID", ""),
        telnyx_public_key=os.environ.get("TELNYX_PUBLIC_KEY", ""),
        brain=os.environ.get("SCOUT_BRAIN", "scout_switchboard.brain:DevBrain"),
        admin_token=os.environ.get("SWITCHBOARD_ADMIN_TOKEN", ""),
        notify_admins_of_unknown=_bool("NOTIFY_ADMINS_OF_UNKNOWN", True),
    )
