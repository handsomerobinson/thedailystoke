# What is actually possible

Read this before promising anything to anybody. Everything here is either
"works today", "works with a ritual", or "does not work". Nothing is aspirational.

---

## Works today, automatically

| Thing | How |
|---|---|
| Photos and videos leave the phone continuously | Immich iOS app, background upload. Genuinely automatic. |
| Semantic photo search — "red bike at the beach" | Immich ships CLIP search. No extra build. |
| Face recognition and grouping by person | Immich, built in. |
| Files reachable from the iPhone Files app | Nextcloud iOS app registers as a Files provider. |
| Contacts and calendars sync | Nextcloud over CardDAV/CalDAV, native in iOS Settings. |
| Everything encrypted before it leaves the house | restic, then Backblaze stores ciphertext. |
| Nightly off-site backup | `ten4-backup.timer`. |

## Works, but needs a human for a couple of minutes

| Thing | The ritual |
|---|---|
| Emptying photos off the phone | Immich app → "free up space". Deletes only local copies it has confirmed are in the vault. Monthly, ~2 minutes. |
| Messages, Notes, voice memos, Health, app data | `04-iphone-pull.sh` with the phone on a USB cable. Monthly, or before any phone reset. |
| Proving the backup works | `restore-test.sh`. Monthly. |

## Does not work. Do not sell these.

**A phone that empties itself on a schedule.**
iOS sandboxes every app. There is no background daemon, and deleting from the
photo library requires a system confirmation dialog that a human physically
taps, every batch, every time. Apple has never exposed an API for this and
shows no sign of doing so. The closest real thing is the monthly ritual above.

**A flip phone that accesses the vault.**
Tailscale has no client for KaiOS or feature phones. Immich and Nextcloud need
a modern browser. A flip phone cannot reach a private tailnet, full stop.

> The honest version of this pitch: *carry a flip phone for calls, and reach
> your cocoon from any browser you sit down at.* If the phone itself must
> reach the vault, it stays a smartphone — just an empty one.

**Replacing iCloud completely.**
Photos and files, yes, entirely. But iMessage sync, Find My, and the encrypted
device backup stay with Apple unless you accept real friction. The recommended
end state is: move photos and files out, keep iCloud on the **free 5GB tier**
for Find My and device backup, stop paying Apple for storage. That is ~95% of
the benefit for ~20% of the pain.

**Automatic extraction of Notes and Messages into searchable text.**
The device backup contains all of it, but in Apple's own format — a `Manifest.db`
index over thousands of hashed SQLite files. Parsing it is real work, not a
flag on a command. That is phase 2. See [COCOON.md](COCOON.md).

---

## The rule that matters

**Nothing gets deleted from a phone until `restore-test.sh` has passed at
least once against that vault.**

Not "the backup ran". Not "the dashboard is green". A restore test that pulled
real files back out of Backblaze and verified them. Until then the phone is
still the only copy, and clearing it is destroying data.
