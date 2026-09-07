# Immich first-run setup

The choices to make in the onboarding wizard, and why. Same answers for your
vault and for a client's.

---

## Storage template — **enable it**

This is the most important switch in the whole product, and it is off by default.

**Off:** photos are stored as random UUIDs in a hashed directory tree.
Machine-readable, human-meaningless. If Immich ever breaks, or you decide to
leave it, you are holding a folder of files named `a3f9c2e1-...jpg` with no
order to them.

**On:** files are written as real folders with real names:

```
2024/2024-03-15/IMG_4821.jpg
```

Browsable in Finder. Restorable by hand. Portable to anything.

That is the difference between a vault and an app that holds your photos
hostage. The entire pitch is *you own this* — the storage template is what
makes that literally true rather than a slogan.

**Template:**

```
{{y}}/{{y}}-{{MM}}-{{dd}}/{{filename}}
```

Year folder, date folder, original filename. Sorts correctly, survives
timezones, and needs no explanation to anyone who opens it.

> Enable it **before** importing a library. Immich can reorganise afterwards,
> but on a large library that means moving every file, which takes hours and
> is a bad first experience.

---

## The rest of the wizard

**Admin account** — this is the account that owns the server, not your day-to-day
login. Use a real password and store it in your password manager.

**Separate user for yourself** — after onboarding, create a normal user account
and use that for your phone. Keeping admin separate means a mistake in the app
cannot reconfigure the server, and it is how you will add other people later
(Immich is multi-user; each account has a completely separate library).

**Machine learning** — leave it on. This is what powers "red bike at the beach"
search and face grouping. It is the whole reason Immich beats a folder of files.
It runs entirely on your machine; nothing is sent anywhere.

---

## Worth changing afterwards

Settings → Administration → Settings:

| Setting | Set it to | Why |
|---|---|---|
| **Storage template** | as above | see above |
| **Machine learning → Smart search** | on | semantic search |
| **Machine learning → Facial recognition** | on | people grouping |
| **Trash → days** | 30 | a real undo window for accidental deletes |
| **Backup (database dumps)** | off | `backup.sh` makes its own, correctly |
| **Video transcoding** | leave default | only tune if playback stutters |

---

## On the phone

Once the server is set up, in the Immich app: log in as your **user** account
(not admin), then Backup → select **all albums** → enable **background backup**
and **foreground backup**.

Then leave the phone on a charger on wifi and let it work through the backlog.

---

## Do not delete anything yet

Uploaded is not the same as safe. Nothing comes off the phone until
`restore-test.sh` has passed against a real off-site copy. See
[PROOF.md](PROOF.md).
