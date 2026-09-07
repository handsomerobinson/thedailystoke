# Client playbook

## Before you sell anyone anything

Run your own vault for **two weeks**. Put your real photo library in it. Do a
phone pull. Pass a restore test. You will discover your actual hours, your
actual upload speed, and two or three surprises that are much cheaper to find
on your own box than on a paying client's.

Then quote.

---

## What you are actually selling

> "Your phone stops being where your life is stored, and nothing is ever only
> on it again. Your photos, files, notes and messages live on a machine you
> own, encrypted, backed up somewhere that cannot read them, reachable from
> anywhere only by you."

That is true and deliverable. Things that are **not**, and must not be promised
— a self-emptying phone, a flip phone that reaches the vault, a full iCloud
replacement. See [WHAT-IS-POSSIBLE.md](WHAT-IS-POSSIBLE.md).

---

## Pricing

**Setup: $1,500–2,500** depending on library size, hardware included at cost.
$2,000 is a fair first-client number. Covers hardware, install, the iCloud
migration, the first phone pull, a verified restore test, and a walkthrough.

Expect **15–25 hours** on the first one. Most of it is waiting on the migration.
By the third it is under 8.

**Monthly: $20–40.** This is not optional. It covers:

- Backblaze (their bucket, roughly $6/TB — pass it through at cost)
- Monthly restore test — *this is the actual product*
- Security patches, disk monitoring, version upgrades
- Support when something breaks

> A one-time fee with nothing after it means you have signed up for unpaid
> support forever, and you are personally carrying their Backblaze bill.
> The recurring fee is what makes this a business instead of a favour.

---

## The model to start with

**Client-owned.** Their hardware, their Backblaze account, their passphrase.
You install and maintain.

- They pay Backblaze directly. You never front their storage bill.
- You never hold their key. You *cannot* read their data — say so plainly, it
  is a selling point and it is true.
- If they leave, they keep a working vault. Nothing is hostage.
- If you lose interest, nobody's photos are at risk.

Only move to hosting once you have several client-owned installs behind you.

---

## Onboarding checklist

**Before**
- [ ] Their iPhone's used storage, so you can size disks (`Settings > General > iPhone Storage`)
- [ ] Their home upload speed
- [ ] Hardware ordered — see [HARDWARE.md](HARDWARE.md)
- [ ] They created their own Backblaze account and bucket
- [ ] They created their own Tailscale account

**Install**
- [ ] `01-provision.sh`, `tailscale up`, `vault.env`, `02-deploy.sh`
- [ ] **Passphrase written on paper, in their hand, before the first backup**
- [ ] `03-verify.sh` passes clean
- [ ] Immich admin account created, their user added
- [ ] Immich + Nextcloud apps installed on their phone and logged in

**Migration** — [MIGRATION.md](MIGRATION.md)
- [ ] iCloud library exported and imported
- [ ] Photo count in Immich reconciled against the phone
- [ ] First `04-iphone-pull.sh` completed

**Proof — do this in front of them**
- [ ] `backup.sh` completed
- [ ] `restore-test.sh` **passes**
- [ ] Show them a photo restored out of Backblaze on your screen
- [ ] Only now: clear photos from their phone

**Handover**
- [ ] Both URLs written down
- [ ] The monthly ritual demonstrated, by them, not you
- [ ] The passphrase warning said out loud, again
- [ ] Date of the passed restore test recorded

---

## What you are taking on

Be clear-eyed. Once someone clears their phone, **you are part of the chain
that keeps their children's photos existing.** That is a real obligation.

It is manageable, and the design already does most of the work:

- The monthly restore test is what turns hope into evidence. Never skip it.
- Never let anyone delete anything before a restore test has passed.
- The client holds their own passphrase. If you hold it, you are the single
  point of failure for their entire life's record. Do not.
- Say plainly, in writing, that you are not liable for data loss and that the
  vault is one copy among several — not a replacement for them keeping their
  own. Get it in an email before you take money.

Anyone who tells you a backup is safe without having restored from it is
guessing. Do not be that person, and do not sell that.

---

## Where this goes

**Phase 1 — client-owned boxes.** You and Dan. Prove it, learn the hours,
build the repeatable install. You are here.

**Phase 2 — the cocoon.** Search across everything, not just photos. This is
the actual product; storage is table stakes. See [COCOON.md](COCOON.md).

**Phase 3 — hosted.** Your hardware, many tenants. Real margins, but you
become a data custodian: uptime obligations, liability, and you can no longer
say "I never have your key." Do not skip to this. The bandwidth math in
[HARDWARE.md](HARDWARE.md) is the part people get wrong.
