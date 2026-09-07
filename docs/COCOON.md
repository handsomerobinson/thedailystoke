# The cocoon — phase 2

The vault is storage. The cocoon is what makes it *yours*: everything you have
ever written, said, photographed or been sent, in one place that can actually
be asked questions.

This is the product. Storage is table stakes — Dropbox has storage. Nobody has
a searchable index of their own life, because nobody has the raw material in
one place. **The vault is what makes the cocoon possible.** Build it first.

---

## What already works, day one

Not planned. Shipping, in the stack you just deployed:

- **Semantic photo search.** Immich runs CLIP locally. "Red bike at the beach",
  "that whiteboard with the diagram", "kitchen at night" — it finds them
  without a single tag or filename.
- **Faces.** Automatic clustering. Name someone once, get every photo of them.
- **Places and dates.** Map view, timeline, "this day in past years".

Go use it once your photos are in. That alone is more cocoon than most people
have ever had, and it costs no extra work.

---

## What phase 2 adds

The parts of a life that are not photographs.

### The raw material — you already have it

`04-iphone-pull.sh` pulls a full encrypted device backup: Messages and their
attachments, Notes, voice memos, call history, Safari history, Health, app data.
It is all sitting in `/srv/vault/iphone/<udid>/`.

**But it is in Apple's format**, which is the honest catch. A `Manifest.db`
SQLite index maps real filenames to thousands of hash-named files. Everything
is there and the format is well understood, but extracting it is real work —
a parser, not a flag.

### The pipeline

```
device backup ──► extract ──► transcribe ──► embed ──► ask
                (Manifest.db)  (Whisper)   (pgvector)  (local LLM)
```

1. **Extract** — parse `Manifest.db`, pull out the Notes store, the Messages
   database, voice memo audio, attachments. Land it as plain files and JSON.
2. **Transcribe** — Whisper, running locally on the same box, over every voice
   memo and video. This is where the scattered dreams actually become text.
3. **Embed** — chunk everything and store vectors. **You already have a vector
   database**: Immich's Postgres runs VectorChord for its own search. Reuse it.
4. **Ask** — a small web UI on the tailnet. "What did I say about the studio
   idea?", "everything from the week Dad was in hospital", "voice notes where
   I sounded excited".

### Why it is genuinely feasible

- The hardware is already there and already on.
- The vector database is already running.
- Whisper runs fine on CPU for a backlog you process once, overnight.
- A local LLM keeps it entirely on your own machine — which for this data is
  not a preference, it is the whole point.

Rough order: extraction is the hard part (a week or two of real work),
transcription is mostly waiting, search is a weekend once the data is clean.

---

## Sequencing

**Do not build this before the vault is solid.** An index over data you might
lose is worth nothing. Get to: photos flowing in automatically, a passed
restore test, one happy paying client. *Then* start extracting.

The good news is nothing is wasted. Every phone pull you take from today
onwards is cocoon training data, sitting there waiting, whether or not the
indexer exists yet.

---

## One thing to think hard about

An index of what someone wrote, said, and felt — searchable by mood, by
person, by the week their life went wrong — is the most sensitive data object
you could possibly build. For yourself, that is a gift.

For a client, it is a different conversation than "I back up your photos", and
it deserves one. Not a reason to avoid it. A reason to be deliberate about
consent, about it never leaving their own hardware, and about being honest
that this is a diary that answers questions, not a filing cabinet.
