# Flip Phone Bridge — Plan

Talk to Claude Code, the vault, and iPhone functions from a dumb flip phone,
by text or voice, with the iPhone left at home.

## What it does

- Text or call one number from the flip phone. Same Claude Code session every time; context kept across days.
- Long-form voice: talk as long as you want, hear the reply spoken back, interrupt anytime.
- Vault: search, read, summarize, write notes, move and organize files. Writes and deletes wait for a "yes".
- iPhone functions via the Mac: send and read iMessages as you, Notes, Reminders, Calendar, Contacts, iCloud Photos and Files.
- Every voice conversation is transcribed and saved into the vault.
- Only your number gets through.
- Runs in the background and survives reboots.

## What it takes

- A Mac at base, always on, vault drives attached. Only hardware requirement.
- Claude Code installed, signed into the existing account.
- Twilio number pointed at a bridge script on the Mac, exposed via Tailscale Funnel or ngrok.
- One Apple MCP server for Messages, Notes, Reminders, Calendar.
- Speech-to-text and text-to-speech: Apple built-in (free) or Deepgram + ElevenLabs (better).
- The bridge script (to be written).

## Build order and time

1. SMS bridge working: half a day.
2. Voice calls: one more day.
3. iPhone functions and vault permissions tuned: half a day.

Total: two days, one focused weekend.

## Phone

- Nokia 2780 Flip, about $90. Verizon, AT&T, T-Mobile. Real buttons, basic browser fallback, hotspot.
- Sunbeam F1, about $200, if you want no browser at all.

## Running cost

| Item | Cost |
|---|---|
| Claude | existing plan |
| Twilio number | ~$1/month |
| Texts | under 1 cent each |
| Voice minutes | ~1.5 cents/minute |
| Premium STT/TTS (optional) | $10 to $20/month heavy use |
| Flip phone carrier plan | $15 to $30/month |
| Tailscale | free |

## Not covered

- Apps with no Mac counterpart (banking, Instagram).
- Two-factor codes that only land on the iPhone.
- Viewing images or video on the flip phone; they get described instead.
