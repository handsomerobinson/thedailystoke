# Stokehouse App Builder — Architecture Proposal (draft for Ryan)

Status: draft, written 8 Sep 2026 before the Core7 / TenFour source was available.
Grounded in *The Stokehouse Method* (Section 5, "The reusable assets" and Stage 6,
"The delivery ecosystem"). Needs one pass against the real Core7 / TenFour code
before anything is built.

## What it is

One generator that turns a **concept** (a pitch, a proposal, an expedition plan,
a product idea, a deck) into a **finished, sendable app** at shippable standard.
The output replaces an email. The recipient opens a link and gets the whole
curated, crystallized thing: front door, the live artifact, walkthrough,
leave-behind, and any gated tiers.

The Method already says this is the deliverable ("Deliver before asking", Stage 6).
The builder is the tool that makes it repeatable without rebuilding the shell
every time.

## Three layers

### 1. The engine (reused, invisible to the recipient)

Extracted from Core7 / TenFour once, then frozen as a library:

- Application shell and screen router (the single-file build pattern)
- Front door with gate, password tiers, NDA overlay
- Live deck engine: narration, detail sheets, keyboard and touch nav
- Leave-behind document renderer
- Guided walkthrough
- Contextual activation logic on open (time of day, what has been seen)
- Push-to-talk / mic input, if the concept has a companion
- Texture-over-sleekness base styles (grit, weight, uneven age), with brand
  tokens swappable per concept
- Persistent-memory hooks (local storage now, backend later)

Rule from the Method: nothing in this layer may be recognisable from one client's
product inside another's.

### 2. The brain (reused, generates the content)

The Stokehouse Method as executable prompts, not prose:

- Stage 0 to 3: listen, due diligence, the twelve questions, one-sentence diagnosis
- Stage 4: the ladder / inversion
- Principle check: the 17 principles as a lint pass over the draft
- Disqualifier check: Section 6 "What it is not"
- Output contract: every section of the concept file below

The reference prompt in Section 8 of the Method doc is the seed. Each app type
adds a short type-specific prompt on top (pitch vs proposal vs expedition).

### 3. The concept (rebuilt every time, one file per send)

A single structured file, e.g. `concepts/grenadier-pitch.yaml`:

```yaml
type: pitch            # pitch | proposal | expedition | product | deck | letter
recipient: Grenadier
sender: Stokehouse Productions
identity:              # the moat, never a reskin of a prior client
  name:
  voice:
  palette:
  texture:
diagnosis: one sentence
ladder:
  - rung: free
    cost_to_them:
    cost_to_us:
sections: []           # ordered, each with body + assets + activation
tiers:                 # gated access
  public: []
  private: []
  memo: []
assets: []             # images, video, maps, numbers with sources
```

The builder compiles engine + concept into `dist/<concept>/index.html` and deploys
it to a Netlify site named for the recipient (the current Core7 deploy is already
a single index.html pushed from the CLI, so this matches how you ship today).

## App types to support first

| Type | Example | What the engine adds |
|---|---|---|
| Pitch | Grenadier | Front door, diagnosis-first deck, the ask last |
| Expedition proposal | where the opportunities lie | Map layer, timeline, opportunity cards, tiered budget |
| Product concept | Core7 style | Companion, loop, loyalty economy |
| Investor / partner | Stokehouse HQ set | Manifest-driven multi-doc set with INDEX |

## Repo shape

```
stokehouse-builder/
  engine/        shell, deck, gate, walkthrough, styles, memory
  brain/         method prompts, principle lint, type prompts
  concepts/      one file per send
  build/         compile concept + engine -> dist/<name>/index.html
  dist/          deployable single files
```

Core7 and TenFour become the first two concepts *after* they are separated
(priority 1). The separation is what proves the engine boundary: whatever they
still share after the split is the engine; whatever is left on each side is
concept.

## Open questions for Ryan

1. Single-file HTML output only, or is a small backend (memory, gating) acceptable now?
2. Is the brain run inside the builder (API call at build time) or by you in a
   Claude session with the builder consuming the result?
3. Which is the first real send: Grenadier pitch or an expedition proposal?
4. Where does the Core7 / TenFour / Slacker source live, and can it be pushed to
   this repo or a sibling repo so the engine extraction can start?
