# Proving it

Four stages. Each one proves a specific thing and is worth doing in order,
because each is useless if the one before it failed. You can reach stage 3 —
the one that actually matters — **without buying anything.**

---

## Stage 1 — the core loop  ·  1 hour  ·  $0

**Proves:** photos leave my phone by themselves and land somewhere I own.

On any computer you already have with Docker installed:

```bash
./00-START-HERE/proof.sh
```

Point the Immich app on your phone at the address it prints, on the same wifi.
Enable background backup. Leave the phone on the charger and go do something else.

Come back and search your own library for something you never tagged — "beach",
"snow", "whiteboard". That search ran on your machine, against your photos, and
touched nobody else's computer.

**If this feels good, the concept is real.** If it doesn't, you have learned
that for the cost of an afternoon instead of $425.

---

## Stage 2 — from anywhere  ·  30 min  ·  $0

**Proves:** I don't need to be home, and nothing is exposed to the internet.

Install Tailscale on the computer and on the phone, same account. Turn the
phone's wifi off. Open Immich over cellular. It works, and there is still no
open port anywhere.

This is the moment it stops being a science project.

---

## Stage 3 — it survives the house burning down  ·  1 hour  ·  $0

**Proves:** the thing I would actually be selling.

You do **not** need to back up your whole library to prove backup works.
Backblaze's first 10GB are free, so a few hundred photos proves the entire
chain for nothing:

```bash
restic init                    # against a b2: repo, or any external drive
restic backup ./proof-vault/library
restic restore latest --target /tmp/restore-test
```

Open a restored photo. Look at it.

**That is the demo.** A photo pulled back out of encrypted storage that cannot
read it. Everything else in this project is a nice interface on top of that
one fact — and it is the only part that justifies anyone trusting you with
their life's record.

If you only ever prove one thing, prove this one.

---

## Stage 4 — make it permanent  ·  a weekend  ·  ~$425

Now buy the hardware, because now you know it works and roughly what it costs
you in hours.

`00-START-HERE/README.md`, scripts in order. Everything from stage 1–3 gets
thrown away; nothing is wasted, because what you were buying was confidence.

---

## What proof gets you

**For yourself:** you know it works, you know your real hours, and you know
which parts fought back. You cannot quote anyone honestly before that.

**For Dan:** you sit down, open your own vault on your own phone, search it,
and then restore a photo out of encrypted off-site storage in front of him.
No slides. No promises about the future. A working thing you built and use.

That conversation goes differently than any pitch, and it is worth waiting the
extra week to be able to have it.

---

## An honest thing to say before it exists

> "I'm building a vault. All your stuff goes in it — photos, files, notes,
> messages. I can't promise you anything yet except that I'm going to try
> really hard, and that I need it for myself either way. Most of the tools
> already exist; what's missing is the front end, and I'm building that.
> If it works for me, I'll show you, and then you can decide."

Everything in that survives contact with reality, including the parts that
might not work. Which means you can say it today, before a single thing is
built, and still be able to look him in the eye in six weeks either way.
