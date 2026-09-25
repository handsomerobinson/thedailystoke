"""The switchboard: carrier event in → right tenant, right person, brain → texts out."""
import logging
from typing import Any, Optional

from .brain import Brain, Contact, Turn
from .carriers import Carrier, Inbound, StatusUpdate
from .config import Settings
from .db import Member, Store, Tenant

log = logging.getLogger("switchboard")

# Carrier-standard keywords (CTIA). Matched on the whole message, case-insensitive.
STOP_WORDS = {"stop", "stopall", "unsubscribe", "cancel", "end", "quit"}
START_WORDS = {"start", "unstop", "yes"}
HELP_WORDS = {"help", "info"}


class Switchboard:
    def __init__(self, store: Store, carrier: Carrier, brain: Brain, settings: Settings):
        self.store = store
        self.carrier = carrier
        self.brain = brain
        self.settings = settings

    # --- carrier events --------------------------------------------------------

    def handle(self, event: Inbound | StatusUpdate) -> None:
        if isinstance(event, StatusUpdate):
            if event.message_id:
                self.store.set_message_status(event.message_id, event.status)
            return
        self.handle_inbound(event)

    def handle_inbound(self, msg: Inbound) -> None:
        if msg.event_id and not self.store.first_time_seen(msg.event_id):
            log.info("duplicate webhook %s ignored", msg.event_id)
            return
        if self.store.is_our_line(msg.from_number):
            log.warning("text from our own line %s ignored (loop guard)", msg.from_number)
            return
        tenant = self.store.tenant_for_line(msg.to_number)
        if tenant is None:
            log.warning("text to unassigned line %s from %s ignored", msg.to_number, msg.from_number)
            return

        line, word = msg.to_number, msg.text.strip().lower()
        member = self.store.member_by_phone(tenant, msg.from_number)

        if word in STOP_WORDS:
            self._log_in(tenant, member, msg)
            self.store.opt_out(line, msg.from_number)
            return  # the carrier sends the opt-out confirmation itself
        if word in START_WORDS and self.store.is_opted_out(line, msg.from_number):
            self._log_in(tenant, member, msg)
            self.store.opt_in(line, msg.from_number)
            self._deliver(tenant, line, msg.from_number, member,
                          f"You're back on {tenant.persona}'s line for {tenant.name}.", via="system")
            return
        if word in HELP_WORDS:
            self._log_in(tenant, member, msg)
            self._deliver(tenant, line, msg.from_number, member,
                          f"{tenant.persona} for {tenant.name}. Text anything to talk. Reply STOP to opt out.",
                          via="system")
            return
        if self.store.is_opted_out(line, msg.from_number):
            # They texted without START. Record it, never reply.
            self._log_in(tenant, member, msg)
            return

        if member is None or member.status != "active":
            self._handle_stranger(tenant, member, msg)
            return

        history = self.store.history(tenant, member.person_id, self.settings.history_limit)
        self._log_in(tenant, member, msg)
        turn = self._build_turn(tenant, member, msg, history)
        tools = TurnTools(self, tenant, member, line)
        try:
            reply = self.brain.think(turn, tools)
        except Exception:
            log.exception("brain failed on %s", turn.session_id)
            reply = "Sorry, I hit a snag on my end. Try me again in a minute."
        if reply:
            self._deliver(tenant, line, member.phone, member, reply, via="reply")

    # --- pieces ----------------------------------------------------------------

    def _handle_stranger(self, tenant: Tenant, member: Optional[Member], msg: Inbound) -> None:
        self._log_in(tenant, member, msg)
        if member is not None and member.status == "blocked":
            return
        line = msg.to_number
        if not self.store.has_texted_peer(line, msg.from_number):
            self._deliver(tenant, line, msg.from_number, None,
                          f"Hi, this is {tenant.persona} for {tenant.name}. I don't have this number yet. Who's this?",
                          via="system")
        if self.settings.notify_admins_of_unknown:
            for admin in self.store.admins(tenant):
                self._deliver(tenant, line, admin.phone, admin,
                              f"New number {msg.from_number} texted the {tenant.name} line: \"{msg.text[:300]}\"",
                              via="system")

    def _build_turn(self, tenant: Tenant, member: Member, msg: Inbound, history: list[dict]) -> Turn:
        contacts = [Contact(m.name, m.role, self.store.can_reach(tenant, member, m))
                    for m in self.store.members(tenant) if m.person_id != member.person_id]
        return Turn(
            tenant=tenant.slug, tenant_name=tenant.name, persona=tenant.persona,
            session_id=f"{tenant.slug}:{member.person_id}",
            speaker=member.name, speaker_role=member.role,
            text=msg.text, media_urls=list(msg.media_urls),
            contacts=contacts,
            groups=self.store.groups_for(tenant, member),
            relationships=self.store.relationships(tenant),
            notes=self.store.notes(tenant),
            history=history,
        )

    def _log_in(self, tenant: Tenant, member: Optional[Member], msg: Inbound) -> None:
        self.store.log_message(tenant=tenant, person_id=member.person_id if member else None,
                               line_number=msg.to_number, peer_number=msg.from_number, direction="in",
                               body=msg.text, media=msg.media_urls, carrier_msg_id=msg.message_id)

    def _deliver(self, tenant: Tenant, line: str, phone: str, recipient: Optional[Member], body: str, *,
                 via: str, on_behalf_of: Optional[int] = None,
                 media_urls: Optional[list[str]] = None) -> tuple[bool, str]:
        if self.store.is_opted_out(line, phone):
            return False, "they've opted out of texts from this line"
        body = body.strip()[: self.settings.max_body_chars]
        result = self.carrier.send(line, phone, body, media_urls)
        self.store.log_message(tenant=tenant, person_id=recipient.person_id if recipient else None,
                               line_number=line, peer_number=phone, direction="out", body=body,
                               media=media_urls, via=via, on_behalf_of=on_behalf_of,
                               carrier_msg_id=result.message_id,
                               status="queued" if result.ok else f"failed: {result.error}")
        if not result.ok:
            log.error("send to %s failed: %s", phone, result.error)
            return False, "the carrier rejected the text"
        return True, "sent"


class TurnTools:
    """The brain's hands for one turn, bound to one tenant and one speaker."""

    def __init__(self, board: Switchboard, tenant: Tenant, speaker: Member, line: str):
        self.board, self.tenant, self.speaker, self.line = board, tenant, speaker, line
        self.store = board.store
        self.sends = 0

    def _budget_left(self) -> bool:
        return self.sends < self.board.settings.max_sends_per_turn

    def _resolve(self, name: str) -> tuple[Optional[Member], str]:
        matches = self.store.find_member(self.tenant, name)
        if not matches:
            return None, f"No one named {name} is on this line."
        if len(matches) > 1:
            return None, f"More than one {name}: {', '.join(m.name for m in matches)}. Which one?"
        return matches[0], ""

    def send_text(self, to: str, message: str, media_urls: Optional[list[str]] = None) -> str:
        if not self._budget_left():
            return "Not sent: too many texts in one turn."
        recipient, problem = self._resolve(to)
        if recipient is None:
            return f"Not sent. {problem}"
        if not self.store.can_reach(self.tenant, self.speaker, recipient):
            return f"Not sent: {self.speaker.name} isn't set up to reach {recipient.name} through me."
        self.sends += 1
        ok, why = self.board._deliver(self.tenant, self.line, recipient.phone, recipient, message,
                                      via="tool", on_behalf_of=self.speaker.person_id, media_urls=media_urls)
        return f"Sent to {recipient.name}." if ok else f"Not sent to {recipient.name}: {why}."

    def message_group(self, group: str, message: str) -> str:
        if not self._budget_left():
            return "Not sent: too many texts in one turn."
        if group.lower() not in {g.lower() for g in self.store.groups_for(self.tenant, self.speaker)}:
            return f"Not sent: {self.speaker.name} isn't in a group called {group}."
        self.sends += 1
        delivered = []
        for m in self.store.group_members(self.tenant, group):
            if m.person_id == self.speaker.person_id:
                continue
            ok, _ = self.board._deliver(self.tenant, self.line, m.phone, m, message,
                                        via="group", on_behalf_of=self.speaker.person_id)
            if ok:
                delivered.append(m.name)
        return f"Sent to {', '.join(delivered)}." if delivered else "Nobody else in that group could be reached."

    def remember(self, note: str, about: Optional[str] = None) -> str:
        person_id = None
        if about:
            person, problem = self._resolve(about)
            if person is None:
                return f"Not saved. {problem}"
            person_id = person.person_id
        self.store.add_note(self.tenant, note.strip(), person_id, self.speaker.person_id)
        return "Saved."

    def specs(self) -> list[dict]:
        """Tool definitions in Claude API form (name / description / input_schema)."""
        return [
            {
                "name": "send_text",
                "description": ("Text one person on this line, by name. Only works for contacts marked "
                                "reachable. Write the message as it should read on their phone, and make "
                                "clear who it's from."),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "to": {"type": "string", "description": "The person's name as listed in contacts."},
                        "message": {"type": "string"},
                        "media_urls": {"type": "array", "items": {"type": "string"},
                                       "description": "Optional public URLs of images/files to attach (MMS)."},
                    },
                    "required": ["to", "message"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "message_group",
                "description": "Text everyone in one of the speaker's groups (each gets their own text).",
                "input_schema": {
                    "type": "object",
                    "properties": {"group": {"type": "string"}, "message": {"type": "string"}},
                    "required": ["group", "message"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "remember",
                "description": ("Save a durable note for this line: a preference, a plan, a date, how people "
                                "are connected. Notes are visible to you in every future conversation on this line."),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "note": {"type": "string"},
                        "about": {"type": "string", "description": "Optional name of the person it's about."},
                    },
                    "required": ["note"],
                    "additionalProperties": False,
                },
            },
        ]

    def call(self, name: str, args: dict[str, Any]) -> str:
        if name == "send_text":
            return self.send_text(args["to"], args["message"], args.get("media_urls"))
        if name == "message_group":
            return self.message_group(args["group"], args["message"])
        if name == "remember":
            return self.remember(args["note"], args.get("about"))
        return f"Unknown tool {name}."
