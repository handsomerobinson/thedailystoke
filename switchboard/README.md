# Scout Switchboard

The plumbing between phone numbers and Scout. People text a number; the switchboard works out
which world that number belongs to (Chester, TENFOUR, Dynamis…), who is texting, what they're
allowed to do, hands the text to the brain, and delivers whatever the brain says or does back
out as real texts.

It follows Ryan's 2026-09-19 direction for the persona dial-in primitive:
**carrier API → Dynamis switchboard → tenant-scoped persona, with the member's phone number as
the identity key.**

```
 phone ──SMS──▶ Telnyx ──webhook──▶ /webhooks/telnyx
                                        │ verify signature, dedupe, ack in <1s
                                        ▼
                                  Switchboard (router.py)
                    to-number → tenant   from-number → person + role
                    STOP/HELP/START      unknown → "who's this?" + tell admins
                                        │ Turn (names only, no numbers)
                                        ▼
                                 brain.think(turn, tools)   ◀── Ryan's Scout brain plugs in here
                                        │ send_text / message_group / remember
                                        ▼
                     permission check → Telnyx Messages API → phones
                                        │
                                   SQLite: people, memberships, reach, relationships,
                                           groups, notes, every message in and out
```

## Muse's spec vs. what's built here

Muse's spec is a good starting point and most of it carries over unchanged. The differences
come from making it serve more than one line (Chester, TENFOUR, Dynamis) and from what breaks
first in production.

| Area | Muse's spec | Built here | Why |
|---|---|---|---|
| Carrier | Telnyx | Telnyx, behind a small `Carrier` interface | Twilio, WhatsApp or iMessage can be added as another adapter without touching the router. |
| Number of lines | One number, one roster | Many numbers. Each number belongs to one **tenant** | Chester's line, the TENFOUR Slacker line and future Dynamis personas run on one deployment. |
| Identity | Roster: number → name, role, projects | `people` (a phone number is one person, everywhere) + `memberships` (role per tenant) | The same person (Ryan) can be admin on Chester's line and a member on TENFOUR's with separate context on each. |
| Isolation | `projects` column | Hard tenant boundary: the brain only ever sees one tenant's people, groups, notes and history | A name on one line can't be resolved, messaged or leaked from another. |
| Permissions | Table: sender → allowed recipients | `reach` edges + admins reach everyone in their tenant + group membership | Same idea; groups added so "tell the team" works. |
| "How people are connected" | — | `relationships` ("Christy works alongside Chester") + brain `remember` notes | Scout keeps the social graph, not just the address book. |
| Webhook payload | `payload.to.phone_number` | `payload.to` treated as a **list** (also accepts an object) | In Telnyx v2 `to` is an array. Confirm against the live docs when you set up the number (the docs site was blocked from this build environment). |
| Webhook security | Not covered | Ed25519 signature check + 5-minute replay window; the server won't start without the public key unless explicitly told to | Otherwise anyone who finds the URL can make Scout text your contacts on your bill. |
| Retries | Not covered | Every webhook event id processed once | Telnyx retries webhooks; without this Scout double-texts. |
| Timing | Synchronous: think, then respond | Acknowledge immediately, think in the background | An LLM turn can outlast the carrier's webhook timeout, which triggers retries. |
| Compliance | Not covered | STOP / START / HELP handled per line; opted-out numbers are never texted | Carriers require it and will block the number otherwise. |
| Unknown numbers | "who's this?" | "who's this?" once, then silent; admins get a text with the number and message; `cli unknowns` lists them | Decide who joins without Scout guessing. |
| Runaway brain | Not covered | Max 5 outbound sends per turn; our own numbers are ignored as senders | Stops loops and mass-texting bugs. |
| Brain interface | `think(user_id, message)` | `think(turn, tools)`, with an adapter for the simple form | The brain gets names, roles, groups, relationships, notes and history each turn; tools are permission-checked by the switchboard. |
| Record | Not covered | Every text in/out logged with why it was sent (`reply`, `tool`, `group`, `system`) and on whose behalf | The action record the text-in front-door doc asks for; also the brain's conversation memory. |
| Media ("packets") | Later | `media_urls` accepted on `send_text` (MMS); inbound media URLs passed to the brain | Voice notes later = TTS file + `media_urls`. |

## Layout

```
scout_switchboard/
  app.py           FastAPI: /webhooks/telnyx (and /sms), /health, /admin/{tenant}/messages|roster
  router.py        the switchboard + the brain's tools
  brain.py         the brain socket: Turn, Tools, Brain, loader, DevBrain (no AI, for testing)
  scout_brain.py   starter Scout brain on Claude, until Ryan's brain is plugged in
  db.py            SQLite schema and queries
  carriers/        telnyx.py, fake.py (prints instead of texting), base.py (the interface)
  seed.py, cli.py  roster loading and admin commands
briefs/            per-line context for the starter brain (chester.md, tenfour.md)
seeds/             roster files; *.example.json is committed, real ones are gitignored
tests/
```

## Run it locally (no phone, no cost)

```bash
cd switchboard
pip install -r requirements.txt
cp seeds/chester.example.json seeds/chester.json    # put real numbers in this copy
python -m scout_switchboard.cli seed seeds/chester.json
python -m scout_switchboard.cli simulate +15551234567 +15550000001 "tell Christy we're on at 3"
python -m scout_switchboard.cli log chester
python -m pytest
```

`simulate` runs the real router with the fake carrier and prints the texts it would send.

To try the starter Scout brain instead of the dev brain:

```bash
export ANTHROPIC_API_KEY=...
export SCOUT_BRAIN=scout_switchboard.scout_brain:ScoutBrain
python -m scout_switchboard.cli simulate +15551234567 +15550000001 "remind me what Christy and I planned"
```

## Plugging in the real Scout brain

Any object with `think(turn, tools) -> str | None` works. Point `SCOUT_BRAIN` at a factory:

```bash
SCOUT_BRAIN=scout.adapter:make_brain
```

- Key the brain's own memory on `turn.session_id` (`"<tenant>:<person id>"`), so memory is per
  person per line.
- Pass `tools.specs()` to the model as its tool list and route calls through
  `tools.call(name, args)`. The switchboard enforces permissions, so the brain doesn't need to.
- A brain that only has `think(user_id, message)` can be wrapped with `SimpleBrainAdapter`.

## Going live on Telnyx

1. Sign up at telnyx.com and add a balance.
2. Buy a US number with SMS (and MMS if you want pictures).
3. **Register for A2P 10DLC** (Messaging → 10DLC): a brand (your business) and a campaign
   (use case, sample messages, how people opt in). US carriers filter or block unregistered
   business texting from local numbers. Approval can take days to a few weeks, so start this
   first. A toll-free number with toll-free verification is the alternative route.
4. Create a Messaging Profile, assign the number, and set its inbound webhook URL to
   `https://<your host>/webhooks/telnyx`.
5. Collect: API key (Account Settings → API Keys), messaging profile id, and the **public key**
   (Keys & Credentials → Public Key).
6. Set the env vars from `.env.example`, add the number to the tenant's `lines` in your seed file,
   seed, and run:
   ```bash
   uvicorn scout_switchboard.app:app --host 0.0.0.0 --port 8000
   ```
7. Testing from your laptop: `ngrok http 8000` and use the ngrok https URL as the webhook.
   For 24/7, deploy to Fly.io / Railway / a VPS with a persistent disk for the SQLite file.

## Admin

```bash
python -m scout_switchboard.cli roster chester
python -m scout_switchboard.cli add-person chester "Adam" +15557650000 member
python -m scout_switchboard.cli allow chester Chester Adam          # both directions
python -m scout_switchboard.cli relate chester Adam "produces for" Chester
python -m scout_switchboard.cli unknowns chester
python -m scout_switchboard.cli block chester "Some Name"
curl -H "Authorization: Bearer $SWITCHBOARD_ADMIN_TOKEN" localhost:8000/admin/chester/roster
```

## Open decisions (defaults chosen, change as you like)

These are the mechanics the TENFOUR text-in front-door note says not to decide silently. Each
one has a working default and is easy to change.

- **Group texting.** Default: Scout sends each member their own text (no shared carrier group
  thread). Replies come back to Scout, not to everyone.
- **Unknown numbers.** Default: one "who's this?", admins notified, nothing else until an admin
  adds them. Alternative: let a new person reply with a name and join as `pending`.
- **Who can reach whom.** Default: explicit `reach` edges; admins reach everyone.
- **Message retention.** Default: every message is kept. No deletion or export policy yet.
- **Beacon, events, gear listings.** Not wired. They need a TENFOUR app API; they'd be added as
  tools next to `send_text`.
- **Channels beyond SMS.** WhatsApp / iMessage / RCS would be additional carrier adapters feeding
  the same tenants.
