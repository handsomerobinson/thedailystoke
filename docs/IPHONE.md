# Your iPhone and the vault

Everything about living with this day to day: what to install, what flows by
itself, what does not, and how to know it is actually working.

---

## Install these three

All free, all App Store.

**1. Tailscale** — sign in to the same account as the vault box. This is the
private network everything else rides on. Leave it connected always; it uses
almost no battery.

**2. Immich** — server address `https://<hostname>.<tailnet>.ts.net`. Then:
- Log in, go to **Backup**
- Select **all albums** (including Recents)
- Turn on **background backup**
- Leave **foreground backup** on too

**3. Nextcloud** — server `https://<hostname>.<tailnet>.ts.net:8443`, log in
with the account from `vault.env`. It then appears inside the iOS **Files**
app as a location, which means every app on your phone can save into the vault
directly — share sheet, Save to Files, all of it.

## Then contacts and calendars — no app needed

`Settings → Apps → Contacts → Accounts → Add Account → Other → Add CardDAV`

- Server: `<hostname>.<tailnet>.ts.net:8443`
- Username / password: your Nextcloud login

Repeat under Calendar, choosing **CalDAV**. Both sync in both directions,
automatically, forever. Once they are syncing you can turn off iCloud contacts
and calendars.

---

## What flows by itself

| | |
|---|---|
| Photos and video you take | Immich, background upload |
| Anything saved into Files | Nextcloud |
| Contacts | CardDAV, two-way |
| Calendars | CalDAV, two-way |
| Anything from a share sheet → Save to Files | Nextcloud |

**Timing, honestly:** iOS throttles background work. New photos land within
hours on wifi, or immediately when you open the Immich app. Not seconds. On a
charger overnight on wifi it reliably catches up. If you want something in the
vault *right now*, open Immich for ten seconds.

---

## What does not flow by itself

**Apple Notes** and **Apple Voice Memos**. Apple gives no third-party app any
access to either — this is not an Immich or Nextcloud limitation, and no
product on the market does it. They are captured by the monthly cable pull
(`04-iphone-pull.sh`) but nothing syncs them live.

### Closing that gap properly

Change where you capture, and the gap disappears:

| Instead of | Use | Result |
|---|---|---|
| Apple Notes | **Nextcloud Notes** (App Store, free) | Notes sync continuously, readable on any device, and land in the vault as plain markdown |
| Apple Voice Memos | Any recorder that saves to Files → Nextcloud | Voice notes sync like any other file |
| Apple Notes, if you want more | **Obsidian** with its folder in Nextcloud | Full markdown vault, syncs everywhere |

This is the single highest-value change you can make. It converts your two
biggest blind spots into automatic ones, today, with no code — and it means
that when the cocoon's search arrives, your notes and voice memos are already
plain files sitting there indexed-ready rather than locked in Apple's format.

Your *existing* Apple Notes and voice memos still come out in the device pull.
Nothing is lost by switching; you just stop adding to the pile.

---

## The monthly ritual — about five minutes

1. **Plug the phone into the vault box** and run `sudo ./04-iphone-pull.sh`.
   Captures Messages, Notes, voice memos, Health, call history, app data.
   Leave it running; the first one takes hours, later ones are incremental.
2. **`sudo ./05-coverage.sh`** — tells you what is in the vault and how stale
   each source is.
3. **`sudo ./restore-test.sh`** — proves the off-site copy actually restores.
4. **Immich app → free up space.** Deletes local copies of photos it has
   confirmed are safely in the vault. This is what keeps the phone empty.

---

## Emptying the phone

**Never delete anything until `restore-test.sh` has passed at least once.**
Before that, the phone is still the only copy and clearing it destroys data.

Once it has passed:

- **Photos** — Immich app → free up space. It only removes what it has verified
  is in the vault. Your library stays fully browsable in the app; the files
  just live on your own hardware now instead of the phone.
- **Files** — move them into Nextcloud via the Files app, then delete the local copy.
- **iCloud** — `Settings → [name] → iCloud → Photos` off, then downgrade
  storage to the free 5GB tier.

Keep the free tier. Find My and iOS device backup are worth having, cost
nothing, and are not what you were paying for.

---

## What stays with Apple

Worth being clear-eyed about, since "completely off iCloud" is the goal:

- **iMessage** still routes through Apple. Its *history* is in your vault via
  the device pull, but the service is Apple's.
- **Find My** — keep it. It is free and useful.
- **iOS device backup** — the free 5GB tier covers settings and app layout.
  Your actual data is in the vault.

Photos, files, notes, contacts, calendars: fully yours. That is the ~95% that
matters, and it is the part you were paying for.

---

## Am I sure it is all in there?

Run `sudo ./05-coverage.sh`. It reports item counts, how recently each source
synced, and flags anything going stale.

Then reconcile the number that matters by hand, once, before you delete
anything: **Settings → General → iPhone Storage → Photos** on the phone,
against the total Immich reports. They should match. Investigate any gap
before clearing a single photo.
