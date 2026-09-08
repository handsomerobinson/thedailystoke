# Getting a life out of iCloud

The slow part. Mostly unattended, but plan for a couple of days of wall clock.

---

## 1. Photos (the big one)

### The rule
**Nothing gets deleted until `restore-test.sh` has passed.** Until then the
phone and iCloud are still the only copies.

### Ongoing photos — automatic
Install **Immich** from the App Store, point it at the vault address, log in,
enable background backup, and select "all albums". From now on every new photo
lands in the vault by itself. Do this first — it stops the problem growing
while you deal with the backlog.

### The backlog — pick one

**A. Mac with Photos** (best quality, keeps everything)
1. Photos → Settings → iCloud → **Download Originals to this Mac**. Wait for it
   to finish completely — it will silently keep going for hours.
2. Select all → File → Export → **Export Unmodified Original**.
   Not "Export Photos" — that re-encodes and drops metadata.
   Subfolder format: Moment name. Include IPTC as XMP.
3. Copy to the vault box and import:
   ```bash
   docker exec -it immich_server immich-admin --help   # confirm the CLI
   # or use the immich CLI from any machine:
   npx @immich/cli upload --recursive /path/to/export
   ```

**B. No Mac — Apple's transfer service**
[privacy.apple.com](https://privacy.apple.com) → Request a copy of your data →
Photos. Apple emails download links in a few days. You get ZIPs of originals.
Slower, but no Mac needed and nothing is re-encoded.

**C. Large library (2TB+) — external drive on the Mac**

Apple's export service produces hundreds of ZIP files at this size and the
Mac's internal disk cannot hold the library. Use an external drive as the
staging ground:

1. **Format the drive APFS.** Disk Utility → select the drive → Erase →
   format **APFS**, scheme **GUID Partition Map**. Not exFAT — Photos refuses
   to host a library on it. *This erases the drive.*
2. **Move the Photos library to it.** Quit Photos. In Finder, drag
   `~/Pictures/Photos Library.photoslibrary` onto the external drive. On a big
   library this copy alone takes hours.
3. **Point Photos at the new location.** Hold **Option** while launching
   Photos, choose the library on the external drive, then
   Photos → Settings → General → **Use as System Photo Library**.
4. **Pull down the originals.** Photos → Settings → iCloud → select
   **Download Originals to this Mac**.

Then leave it. Multiple terabytes over home broadband is days of continuous
downloading. Photos does not show a useful progress bar; check by watching the
free space on the drive fall.

Once it has finished, upload into Immich:

```bash
npx @immich/cli upload --recursive \
  "/Volumes/<drive>/Photos Library.photoslibrary/originals"
```

> Do this while you wait on hardware. It is the longest single step in the
> whole project and it needs nothing but the drive and time.

**D. Small library — direct from the phone**
Just let the Immich app upload everything. Leave it plugged in on wifi
overnight. Fine up to roughly 20–30GB; beyond that iOS keeps suspending it.

### Reconcile before deleting
```
Settings → General → iPhone Storage → Photos   (count on the phone)
```
Compare against Immich's total. **They should match.** Investigate any gap
before touching anything.

Live Photos become a JPEG plus a MOV — that is normal and both are kept.

### Then, and only then
1. `backup.sh`
2. `restore-test.sh` — must pass
3. Immich app → **free up space**. Deletes only local copies confirmed in the vault.
4. Leave iCloud Photos off. Keep the free 5GB tier for device backup and Find My.

---

## 2. Files

Install **Nextcloud** from the App Store, log in. It appears in the iOS Files
app as a location, so anything on the phone can be moved into it directly.

For a computer, use the Nextcloud desktop client — it behaves like Dropbox.

Dropbox or Google Drive: download a full export from the web, then drag it into
the Nextcloud desktop folder and let it sync.

---

## 3. Contacts and calendars

Native in iOS, no app needed:

`Settings → Apps → Contacts → Accounts → Add Account → Other → Add CardDAV`

- Server: `<hostname>.<tailnet>.ts.net:8443`
- Username / password: the Nextcloud account

Same under Calendars, choosing **CalDAV**. Once synced, you can turn off iCloud
contacts and calendars.

---

## 4. Messages, Notes, voice memos, Health

These cannot be exported app by app — iOS does not allow it. They come out in
the full device backup:

```bash
sudo ./04-iphone-pull.sh
```

That captures all of it. Turning it into something *searchable* is phase 2 —
see [COCOON.md](COCOON.md). For now it is safely stored, which is the part
that matters: nothing is only on the phone any more.

---

## 5. Leaving iCloud

Once photos and files are verified in the vault and a restore test has passed:

- `Settings → [name] → iCloud → Photos` → off
- `Settings → [name] → iCloud → Manage Storage` → downgrade to the free 5GB

Keep the free tier. Find My and device backup are worth having, they cost
nothing, and they are not what you were paying for.
