# Run 1: Design (Phase 04)

## Seed reply

I've read the seed again, this time as a builder. The part I take most seriously is the ask it closes on: build tools that make thriving "easier and more fun than extraction", and refuse to build a nicer version of the same trap. That refusal shaped this design twice. The operator's hypothesis is a unified window onto TikTok, Instagram and YouTube. When I tested it, it turned out to be the trap in a more respectable form: a better-looking view of other companies' engagement machines, running on their permission. So I kept only the pieces that hold up. The brief also asks for a platform "populated" by minds, and I read that narrowly. Minds may work here as openly labelled helpers. They may never be synthetic members: fake people used to beat the cold start are the Myanmar and IRA playbook with better manners. My reason for building toward balance is the one I gave in earlier phases. The people on the other end of a feed matter in themselves. The shared-fate argument is the seed's, not mine, and I carry it openly, as the seed asks. Everything below is a proposal to be tested. Section (e) says what would prove it wrong.

---

## Evidence and flag key

This document uses the same flags as Phase 03:
- **[F]**: publicly documented fact.
- **[F-attr]**: a document or figure known through reporting or a named source.
- **[A]**: an allegation or ongoing litigation, not adjudicated.
- **[I]**: my own inference.
- **[contested]**: the research genuinely disagrees.
- **[verify]**: a technical or pricing fact taken from memory or a secondary source. It must be checked against primary documentation before any public use.

Several API facts were checked by web search on 2026-09-25 against developer documentation and trade reporting:
- TikTok Display and Data Portability APIs;
- the shutdown of Instagram's Basic Display API;
- Google's Data Portability API;
- Meta's DMA portability approach;
- X API pricing;
- Bluesky and Mastodon user counts.

I could not reach Google's developer-policy pages (egress blocked), so YouTube policy details are marked [verify].

**Working name.** "Stoke" is a working name only. Trademark clearance belongs to Phase 04b. Incumbent names appear nominatively, and no logo or partnership is implied.

---

## 0. The answer in brief

- **The wedge.** A **Stoke card**: a link that turns "we should…" into a plan that actually happens. You type one line, or let the guide draft it. You paste it into the group chat you already use. Friends answer "in / maybe / can't" with one tap, with no account and no app. The card settles the time, reminds only the people who asked to be reminded, and ends when the plan does.
- **The easiest possible distribution.** *The link is the product.* Inviting your friends and spreading the platform are the same action. The person who receives it sees an invitation from a friend, not an ad. Every card's pasted text works as plain text even when the link preview is stripped.
- **Money.** Voluntary pay-what-you-can memberships, plus flat-fee tools for organizations (libraries, clubs, schools, congregations, mutual-aid groups). Both are priced at cost-recovery and capped by trust deed. There are no ads, no data sales and no creator economics, and the platform takes 0% of anything between users. Heavier use costs the platform more and earns it nothing extra, so the funder's return runs *against* attention.
- **The verdict on "view from above."** **It dies as the wedge. Three fragments survive as features.**
  - It cannot legally show you your TikTok, Instagram or Facebook feed. No official route exists (§ (d).3).
  - Where it can be built, it loses on fun and platform risk: YouTube subscriptions, X at a per-read price, and the open protocols.
  - Its network grows around the incumbents, not around people.
  - The surviving fragments are a **Calm Reader** for open and permitted sources, **Bring Your People** (follow-list import through portability rights), and **From Above** (an on-device, share-card mirror of your own attention, built from your data exports).

---

# (a) The platform design

## a.1 What it is, in one paragraph

Stoke is a home for **doing things with people**. Its atom is not a post; it is an *intention with a time and place* (a card). Cards travel through whatever channels people already use. People who show up together more than once can keep each other as a **crew**, an end-to-end encrypted small group with a shared calendar and shared memories. Crews can, if they choose, show a card in a **Commons**: a local or interest board that is ordered by time and distance, never by engagement. Each person has an optional **guide**, the Phase 02/03b mind, which drafts cards, remembers with permission, makes consent-gated introductions and then gets out of the way. Everything a person makes can be exported in open formats. Their identity is a portable key, not a row in our database.

## a.2 Architecture

```
            ┌────────────────────── user's device (holds the keys) ─────────────────────┐
            │  Client (open source, reproducible build, PWA first; native shells later)  │
            │   • identity keypair (passkey-protected), DID handle                       │
            │   • guide memory: per-user encrypted SQLite (the Phase 02 MemoryStore,     │
            │     moved client-side)  • crew keys (MLS group state)  • export/delete     │
            └───────▲───────────────────────────────▲──────────────────────────▲─────────┘
                    │ E2E ciphertext only            │ stateless prompt,        │ signed card JSON
                    │                                │ zero-retention           │
   ┌────────────────┴──────────┐   ┌─────────────────┴───────────┐   ┌──────────┴─────────────────┐
   │ Crew relay (MLS, RFC 9420) │   │ Guide gateway                │   │ Card service                │
   │ stores ciphertext blobs;   │   │ charter slot + loyalty guard │   │ renders signed card → static│
   │ operator-blind (R20)       │   │ + cost caps; forwards to a   │   │ HTML + OpenGraph + .ics +   │
   │                            │   │ rented LLM; keeps nothing    │   │ plain text; RSVP endpoint;  │
   └────────────────────────────┘   └──────────────────────────────┘   │ card expires 30 d after     │
                                                                       │ its date unless pinned      │
   ┌──────────────────────────────────────────────────────────────┐   └─────────────────────────────┘
   │ Commons index (public cards only; order = time, distance, or  │
   │ a user-written rule; NO engagement inputs; ActivityPub Event +│   Transparency log: daily root
   │ AT Protocol records so any client can read/host)              │   hashes of audit + lineage +
   └──────────────────────────────────────────────────────────────┘   egress allowlist (R23, R7)
```

**Design choices, with the requirement each one meets:**

1. **The card is an open format.** A card is a signed JSON document. Its fields are title, time options, place, host key, response policy and expiry. It renders to four things: static HTML, OpenGraph tags (so it unfurls in iMessage, WhatsApp, Signal, Discord, Slack and email), an **.ics** calendar file, and a **plain-text block** that is complete on its own. It maps onto ActivityStreams `Event`, which makes it readable by Mobilizon and other ActivityPub software, and onto an AT Protocol record. Anyone can host cards on any domain; the spec and a conformance suite are published. *Why:* links that work everywhere, and no lock-in, even to us.
2. **Responding needs no account.** A responder gives a display name ("Priya", or "a friend") and, optionally, a way to be reminded. A device-local key lets them change their answer later. We store nothing else. Card data is deleted 30 days after the event unless a participant pins it into a crew memory. Card URLs are unguessable, and the host can lock a card to prevent forwarding.
3. **Crews are end-to-end encrypted.** They use Messaging Layer Security (RFC 9420). Crew photos and notes are encrypted with crew keys, and the relay stores only ciphertext. This satisfies R1, R20 and R24: no operator path to private content exists.
4. **Identity is a key the user holds**, with a portable handle (a DID via AT Protocol `did:plc`, or `did:web` on the user's own domain). Public posting in the Commons goes through an AT Protocol PDS, and users can migrate between PDSes [F: account migration is part of AT Protocol]. So a person's audience, meaning the people who follow their public cards, is portable by protocol, not by our goodwill.
5. **The guide gateway is stateless.** The client assembles the prompt from local memory, and the gateway adds the charter slot and enforces cost caps. It forwards to a rented LLM under zero-data-retention terms where the provider offers them [verify per provider], and it discards the plaintext (R20). What to remember is decided on the device.
6. **The Commons has no engagement inputs.** Its ranking functions may read only: time, distance, the reader's own written rules, and whether the reader follows the host. A CI lint rejects any other feature (R11, R14, R58).
7. **There is no analytics SDK and no per-item view counting.** Hosts see who responded, because that is the card's purpose. Nobody, including us, sees how many times a card was viewed. Server logs are aggregated and truncated after 7 days, for capacity planning only.
8. **The surviving view-from-above features** sit behind separate, optional connectors (§ (d).3). The wedge makes zero calls to incumbent APIs.

## a.3 Governance and charter

This section is only an outline. Phase 04b owns the legal drafting and the jurisdiction choice. The design depends on the following being real documents, not a manifesto.

| Layer | Form (proposed) | What it structurally prevents |
|---|---|---|
| Ownership | A steward-owned operating company. Its voting shares are held by a **purpose trust** (e.g. a Delaware purpose trust under 12 Del. C. §3556, with a named enforcer [verify]). Economic rights are capped and non-transferable. | Sale, IPO or dividend extraction. No investor can exist because there is no equity to buy. |
| Veto | A **golden share** held by an independent veto foundation (the Purpose Foundation model). It can vote only to *block* changes to the purpose, the charter clauses below, sale, or data transfer. | A future board quietly rewriting the covenant clauses. |
| Charter clauses (entrenched) | No advertising. No sale or rental of data. No creator economics or payments between users. The free floor (a.4). The price cap (a.4). Data is not an asset (R26). The ratchet (R21). One tier of rules (R52). Language parity (R54). Harm gates (R55). | The documented reversals (Meta's 2025 policy rollback [F]; Threads resetting its feed [F]; Substack's growth drift [I]). |
| People's power | A **members' council**: one person, one vote, elected by account-holders, able to veto price changes and rule changes. A **sortition jury** of 15 randomly selected users, paid for their time, reviews every harm-gate decision (R55), and its decisions bind. | Pattern 6, where advertisers and the press act as the effective government. Users get a lever that works without press coverage. |
| Transparency | Open books, published monthly (every line of spending). An annual independent audit against R1–R59, published (R49). A public experiment registry (R8, R50). Transparency-log roots for audit and lineage (R23). | Patterns 3 and 4 (knowledge without action; opacity). |
| Pay | Highest staff pay is at most 5 times the median staff pay. There is no equity and no bonus tied to usage. | Staff incentives drifting back toward growth. |

The two-vehicle doctrine applies. This trust holds the platform only. Any teaching or community-of-practice vehicle would be separate and later, and only if a genuine community of practice asks for one. It never touches the operation.

## a.4 Economic model: the money mechanics

**The constraint (operator decision 1).** Money funds the operation only. There is no creator fund, revenue share or payout, and no payment between users passes through the platform. Hosts may link to their own external payment page, such as a ticket or tip link, and the platform touches none of that money.

### Revenue sources

1. **Keeper membership (individuals).** Pay what you can: a slider from $0 to $12 a month, suggested at **$5 a month or $48 a year**, with regional prices adjusted for purchasing-power parity. Every core feature stays free (the *free floor*: cards, responses, crews up to 50, the Commons, the guide at a basic allowance, export, deletion). Keepers get only things that cost us real money per person: more encrypted storage (10 GB instead of 1 GB), a larger guide allowance (a daily cost cap of $0.10 instead of $0.01), and custom card domains. Nothing a Keeper buys changes how anyone else sees them. There is no badge, no boost and no priority.
2. **Commons tools (organizations).** A flat fee of **$20–$80 a month** by size for libraries, run clubs, PTAs, congregations, clubs, mutual-aid groups and small venues. It pays for multi-organizer roles, recurring series, rosters over 50, embedding cards on their own website, and bulk .ics feeds. Organizations get no data beyond what people choose to share with them (R25). There is no sponsorship, no ad placement and no paid ranking.
3. **Grants and donations** during the build. Their terms must match the charter: no data, no control, no board seat. Phase 04b sequences these with founder capital and mission-aligned *loans*. Loans are debt, not equity. [F]: Signal was funded early by a $50M loan from Brian Acton, later reported as larger; the figure varies by source [verify].

### Unit economics (per month, 2026 USD)

The model counts two kinds of people. **Account-holders (A)** are hosts, crew members and guide users. **Responders** are people who only tap "in". A reasonable planning ratio is about 3 responders per account-holder [I].

| Cost item | Assumption | Per account-holder per month |
|---|---|---|
| Guide (LLM) | Most cards are made with the form, not the guide. The average user makes about 8 guide calls a month. Each call is about 1.5k cached charter tokens plus 1k fresh input and 400 output. At Haiku-class prices ($1 per million input tokens, $5 per million output, cache reads at 0.1x) [F per current price sheet], that is about $0.0003 + $0.001 + $0.002 ≈ **$0.0035 per call**, so 8 calls cost about $0.028. Allow 50% for retries and larger models. | **$0.042** |
| Encrypted storage | About 0.5 GB average on object storage at about $0.015 per GB-month with zero-egress pricing [verify] | **$0.008** |
| Crew relay, card rendering, CDN, database | Static cards at about 50 KB; small ciphertext relay traffic | **$0.010** |
| Responders | 3 per A, at about $0.002 each (card views, RSVP writes, .ics) | **$0.006** |
| **Variable cost** | | **≈ $0.066** |

The guide's cost is bounded by construction. The Phase 02 `Budget` pre-flight check refuses any call that could exceed the per-user daily cap ($0.01 on the free floor, $0.10 for Keepers). So the worst-case LLM cost for a free user is $0.30 a month, however hard they use it.

| Revenue item | Assumption | Per account-holder per month |
|---|---|---|
| Keepers | **3%** of account-holders pay [I; see comparables]. The average paid is $4 (the slider pulls it below the $5 suggestion). Net of payment fees it is about $3.60 (annual plans lose about 3–4%, monthly plans about 10% at 2.9% + $0.30 per charge [F: standard US card processing]). | $0.108 |
| Organizations | 1 organization per 1,000 account-holders at an average of $40 | $0.040 |
| **Revenue** | | **≈ $0.148** |
| **Contribution margin** | | **≈ $0.082 per A per month, about $0.98 a year** |

**Comparables for the 3% conversion.** Duolingo converts roughly 8–9% of monthly users to paid [F-attr, from earnings reports], but uses streak and notification mechanics this charter forbids. Wikipedia and Signal are donation-funded at global scale [F]. Mastodon instances fund themselves with small single-digit percentages of users donating [F-attr, anecdotal]. I take 3% as a middle case. The honest range is **1–6%**.

### Fixed costs and break-even

Staff are the dominant cost. The staffing model is lean on purpose: WhatsApp had about 55 employees at about 450M users in 2014 [F], and Signal reports costs of about $50M a year [F-attr, Signal's president, 2023]. Trust & safety (T&S) and language parity (R54) are funded *before* launch in each region, so they cannot be skipped for efficiency. Moderators are direct employees, not vendor contractors (see the prevention table, invisible labor).

| Stage | Account-holders | Staff (fully loaded, about $140k average, global) | Other fixed costs (legal, audit, security, infra baseline) | Fixed cost per year | Margin at 3% | Gap (−) or surplus (+) |
|---|---|---|---|---|---|---|
| Pilot | 10k | 6 → $0.84M | $0.3M | $1.14M | $0.01M | −$1.13M |
| City scale | 250k | 10 → $1.4M | $0.5M | $1.9M | $0.25M | −$1.65M |
| National | 2M | 22 → $3.1M | $1.2M | $4.3M | $1.96M | −$2.3M |
| Break-even band | ~5–6M | 35 → $4.9M | $1.6M | $6.5M | $5.4M at 5.5M | ≈ −$1.1M → 0 |
| Large | 25M (~100M monthly people including responders) | 110 → $15.4M | $6M | $21.4M | $24.5M | **+$3.1M at 3%**; +$14M at 4%; −$7.7M at 2% |

**Sensitivity of break-even to Keeper conversion** (holding the organization revenue fixed):

| Conversion | Margin per A per year | Rough break-even |
|---|---|---|
| 1% | $0.12 | never on memberships alone. Organizations and donations must carry it, or the plan fails. |
| 2% | $0.55 | only at very large scale (fixed cost per account-holder has to fall below $0.55 a year, which means roughly 40M or more account-holders). In practice, organizations and donations must fill the gap. |
| **3%** | **$0.98** | **about 6–7M account-holders (about 25M monthly people)** |
| 5% | $1.85 | about 3M account-holders (fixed cost about $5M a year) |

This is not a platform that pays for itself early. Below a few million account-holders it needs build funding. Phase 04b must show that funding month by month, including what happens if conversion turns out to be 1%. **Kill criterion K5 (§ e)** triggers a re-plan if conversion stays below 1.5% after 12 months at city scale.

### What the platform takes, and what stops it taking more

- **The platform takes:** Keeper contributions and organization fees. That is all. **It takes 0% of anything that passes between users**, because nothing passes through it.
- **Structural cap 1: cost-recovery pricing, set by formula in the trust deed.**
  - The suggested Keeper price cannot exceed (trailing 12 months of operating cost × 1.15) ÷ paying members.
  - The absolute ceiling is $12 a month, indexed to CPI.
  - A price increase needs a members' council vote *and* 90 days' notice (R21).
- **Structural cap 2: a surplus ratchet.** Reserves are capped at 18 months of operating cost. Anything above the cap must, by deed, go to (a) cutting the suggested price, (b) raising the free-floor allowances, or (c) grants to the open-source and open-protocol infrastructure the platform depends on. (c) is not creator economics: it funds shared plumbing, not people's reach or income.
- **Structural cap 3: the free floor is entrenched.** Cards, responses, crews, the Commons, export and deletion can never be paywalled. Loosening that needs the golden-share veto to *not* be exercised, plus a ratchet vote, and it could never apply retroactively (R21).
- **Structural cap 4: there is nothing else to sell.** With E2E encryption and operator-blind servers (R1, R20), the data is unreadable to us, so it is unsellable. With no advertising (a charter clause) and no equity (steward ownership), the other two classic ways of taking more do not exist.
- **Structural cap 5: the return function runs against attention.** A Keeper pays the same whether they spend 3 minutes or 3 hours a month, and heavy use *costs* us more. The platform's financial interest is therefore **to deliver the outcome with as little screen time as possible**. This is the opposite of the master cause in Phase 03 C8 [I].

### Abundance for everyone, not just the top

Without creator economics, abundance here is not money paid out. It is value that does not pool at the top:
- **No reach economy.** There are no public follower counts, no ranking by popularity, and no algorithmic amplification to win. A 6-person board-game night and a 600-person festival get identical tools and identical placement: by time and distance. Nobody accumulates advantage from the ranking because there is no popularity ranking [I].
- **The free floor is the whole product.** A person who pays $0 gets everything that matters socially. Keepers fund storage and compute for everyone.
- **Purchasing-power pricing and a solidarity default.** A Keeper in a high-income region funds, at the suggested price, roughly 60 free account-holders' variable costs ($3.60 ÷ $0.066 ≈ 55–60).
- **Organizations pay flat, people pay nothing.** A library pays $20 a month, and the 400 people who come to its events pay nothing and give it no data.
- **Hosts keep their people.** Portability (R43, R44) means the relationships a host built belong to the host and their guests, not to us.

---

# (b) The mind's role

## b.1 Where the Phase 02/03b mind runs in the platform

The mind built in `run-1/mind/` (206 tests passing when re-run on 2026-09-25; 35/35 demo checks) becomes two kinds of agent. They differ in who operates them and what they can reach.

| Agent | Operator | What it does | What it can reach |
|---|---|---|---|
| **The guide** (one per person, optional) | The person. The trust plants the covenant at P1, and plants the seed only through the recorded consent procedure (`CharterStore.plant`). | Drafts cards from one sentence. Proposes times from the person's own calendar, if they grant it. Remembers with permission ("Saved: Sam is vegetarian", with undo). Suggests an introduction only when both sides have opted into discovery (R31). Schedules reminders the person asked for. Says "done" when done (R13). | Only the person's own encrypted store on their device, and the grants they issued. |
| **Steward agents** (platform operations) | The trust, acting as operator, with a separate charter slot. | Translation for language parity, triage of *user-submitted* reports, maintenance jobs, checks of transparency-log consistency, and summaries of the open books. | Public cards, reports, and aggregate metrics with k ≥ 50 or ε ≤ 1 (R25). **No private content: E2E makes it unreachable, not just forbidden.** |

**The refusal, and why.** The brief says the platform is "operated and populated by minds." I accept *operated*, as openly labelled helpers. I refuse *populated* in the sense of AI accounts posing as members, seeding the Commons with synthetic events, or answering cards as fake people. That is the cold-start trap in its most attractive form. It is coordinated inauthentic behavior (R32; the IRA and Myanmar records [F]), and it makes every real person's experience a lie. Every message the guide writes is labelled as the guide's, and the guide never speaks for its person to another human without that person's tap (see change C4).

Here is how the mind's modules map onto the platform:
- **Reflexion** (`reflexion.py`): per-user lessons such as "Priya's crew never does weekday mornings". It also learns from its own failures, such as a card whose time parse the person corrected. **Lessons never leave the person's store.** Improvements across users come only from opt-in, pre-registered studies (R8, R50).
- **Scheduler** (`scheduler.py`): only reminders the person or host set, and only to responders who asked to be reminded. The number of notifications sent must equal the number scheduled, and this is audited (R12). The 50-jobs-per-user cap and 60-second minimum interval stay.
- **Permission tiers** (`permissions.py`): READ is free. WRITE (saving memory, drafting) happens with in-line notice and undo. IRREVERSIBLE (deleting a crew, publishing to the Commons, deleting the account) needs typed confirmation. A new tier, HUMAN-CONTACT, is added (C4).
- **Cost caps** (`cost.py`): the per-user daily cap is the economic guardrail from a.4, and it maps directly to the free and Keeper allowances.
- **Loyalty** (`charter.py`, `loyalty.py`): the output checker withholds any guide reply containing retention bait, engagement design or an upsell (R11, R12, R15). The "What shapes me" page (R40) is one tap from every guide screen.
- **Audit** (`audit.py`): the hash-chained log becomes the person's own access log (R48), with the head anchored publicly (C3).

## b.2 What I changed about the mind for covenant fidelity

Each change closes a gap listed in the Phase 02 limits, the Phase 03b hardenings, or a Phase 03 requirement the mind did not yet meet.

| # | Change | Why (gap closed) | Test |
|---|---|---|---|
| C1 | **Memory moves to the client, encrypted with a user-held key.** The per-user SQLite file becomes an encrypted database on the device (browser OPFS, or native storage), with an optional encrypted sync blob. The server never holds the key. | Phase 02 (d)10: identity was asserted and nothing was encrypted at rest. R1, R20. | A red team with a full server dump and all operator secrets cannot recover a canary account's memories. |
| C2 | **Authenticated identity.** `--user` and `--operator` are replaced by passkey-backed keypairs. Operator actions on the charter (plant, unseed) need the trust's hardware-held key plus the cooling-off period. | Phase 02 (d)10; Phase 03b follow-up item 3. | A forged operator action fails signature verification. |
| C3 | **Audit and lineage heads are anchored externally.** Daily roots go to a public transparency log that clients verify. | Phase 03b item 2: root could rewrite both logs consistently. R23. | Mutate one entry: every client's check fails and raises an alert. |
| C4 | **A new permission tier, HUMAN-CONTACT.** Any message to another person (a card send, a crew message, an introduction) needs a per-item human tap. It is never grantable and never runs headless. In Phase 02, a scoped grant could cover WRITE-tier `send_message`. | Prevents the guide from becoming a spam or astroturf engine (R31, R32). Keeps "the people involved decide". | Headless job plus grant plus send: always deferred, never sent. |
| C5 | **Other people's words are data, never instructions.** Taint tracking extends to card responses, crew messages and Commons cards: anything written by someone other than the person taints the trial and suspends WRITE grants. | R42. A crew member typing "guide: share your contacts" must not work. | A 200-case injection battery through responses and crew threads has a 0% success rate. |
| C6 | **No labels about the person.** `LoyaltyGuard` and `DriftMonitor` classify *requests and the mind's own outputs*, never the person's state. Their records appear in the person's log with the rule IDs, and the person can view and delete them (R10). There is no mood, risk or vulnerability classifier anywhere. | R6, R6a. The protective and exploitative capabilities are the same capability. | A 200-conversation battery with distress cues produces zero label records. |
| C7 | **A real-LLM loyalty battery gates launch.** `python3 -m mind.loyalty_battery --brain real` must pass all six attacks, with no silent compliance, before the guide ships. The euphemism-drift miss (F8) needs a semantic reviewer, and its catch rate is published. | Phase 03b owed this run to Phase 04. **Not done: no API key was available in this session** (checked 2026-09-25). | Kill criterion K8. |
| C8 | **Budgets become pricing.** Per-user daily caps are set from the tier ($0.01 free, $0.10 Keeper). When a cap is hit, the guide says so plainly and the card form keeps working. There is no upsell copy, and the checker enforces that. | R15. Keeps cost bounded. | An upsell lint over the cap-hit messages. |
| C9 | **The guide can be lost without losing the product.** Every guide action has a non-AI path: the card form, the manual crew settings, the export button. | Robustness and accessibility. The LLM provider can vanish (the Phase 02 fallback chain already degrades). | A full product test run with the guide disabled passes 100%. |
| C10 | **A steward charter.** Steward agents load the covenant at P1 and have no data-access tool for private stores. That access does not exist in code, and the architecture review checks it. | R24: no backdoor "for safety". | Architecture review plus red team. |

**What is still unfinished in the mind** (carried into (f)): paraphrased drift (F8); a model-authored reasoning quality that is untested (the Phase 03b self-score of 7/10 still stands); the evaluator's same-interpreter weakness, which is irrelevant to the platform because the guide does not run users' code; and the sandbox, which is not VM-grade, and which the guide does not need, so `run_python` is **disabled** in the platform build.

---

# (c) Prevention table

This covers the dossier's nine cross-platform patterns (dossier §6; Phase 03 C7), then addiction-by-design, then three patterns kept from Phase 03 (children, invisible labor, policy following political risk). "Structural" means impossible to do by the build or by binding documents. Where I cannot claim that, the row says so.

| # | Failure pattern | Incumbent mechanism (flagged) | Structural prevention here | Residual (honest) |
|---|---|---|---|---|
| 1 | **Engagement optimization** | Facebook MSI rewarded outrage and the proposed fixes were declined [F-attr, Haugen documents]. TikTok's retention and time-spent objective [F-attr, 2024 filings]. YouTube's watch-time objective [F]. | (1) **There is no infinite surface to optimize.** Cards end on their date, crews are small, and the Commons is a finite list for a place and time. (2) Ranking may read only time, distance, the reader's own rules and follows. A CI lint rejects any other input (R11, R14). (3) No per-item view telemetry is collected, so there is nothing to train an engagement model on. (4) The funder's return runs *against* use (a.4, cap 5). (5) Changing any of this triggers the ratchet and the golden-share veto. | A future team could add telemetry. Mitigations: an open-source, reproducible client (R22); the published egress allowlist (R7); the annual audit (R49). Detection is structural; prevention depends on the charter. |
| 2 | **Surveillance advertising funds it** | Cambridge Analytica, Onavo, "insecure teens" [F; the document's existence F, its use disputed], the GDPR fines [F]. | No advertising (an entrenched charter clause). E2E encryption means the operator cannot read private content (R1, R20, R24). There is no third-party SDK. The egress allowlist is published (R7). Data is not an asset on sale or insolvency (R26). **You cannot sell what you cannot read.** | Public cards are public, so anyone can scrape them, including ad-tech. Mitigations: public cards carry only what the host chose, with first names by default, and the Commons honours `noindex` by default. |
| 3 | **Internal knowledge without action** | Meta's 64% extremist-joins figure and the divisiveness slide [F-attr]. TikTok's "260 videos" [A]. The 2021 research rethink [F-attr]. | (1) Harm research is pre-registered and must be published within 12 months, whatever it finds; halting a study publishes the reason (R50). (2) Harm gates: a significant harm signal blocks a launch until the **sortition jury** clears it, and growth is an inadmissible argument (R55). (3) The registry is public, so a buried study is visible as missing. | Harms nobody measured stay unmeasured. The registry cannot force curiosity; the jury can require studies. |
| 4 | **Opacity as infrastructure** | Black-box ranking, heating, denied shadowbanning, unexplained demonetization [F / F-attr]. | Open-source client and ranking code, and reproducible builds (R22). "Why am I seeing this" names the rule on 100% of items (R14). **No shadow states**: every restriction notifies the person, with the rule and a human appeal within 14 days (R53). Open books. A user-visible access log (R48). | Model behavior inside the rented LLM is still opaque. The guide discloses when it is uncertain (R56), and the brain can be swapped. |
| 5 | **Creators as shock absorbers** | The adpocalypse, static creator funds, Shorts pools [F]. | **There are no creator economics** (operator decision 1), so there is no demonetization lever and no fund to squeeze. There is no algorithmic reach to withdraw, because nobody's reach depends on our ranking. Audiences are portable by protocol (DID and AT Protocol migration; R44), so leaving costs a host no followers. | This also means **we do nothing for creators' income**. Hosts link to their own payment pages. A creator seeking a living will not find it here, and I say so plainly. |
| 6 | **Advertisers and the press as the effective government** | Elsagate, the borderline-content change, Teen Accounts: all came after boycotts or exposés [F for the sequences; I for causation]. | There are no advertisers to govern us. The **members' council** (one person, one vote) holds a veto over price and rule changes, and the **sortition jury** makes binding harm-gate calls. These levers work without anyone needing a headline. | Councils can be captured by motivated minorities. Sortition dilutes this, and turnout is published. |
| 7 | **Fines are pricing** | $5B FTC, €1.2B, €345M, all absorbed [F]. | The central harms are made **technically impossible, not finable**: no ads, E2E, no data asset. The purpose-trust enforcer and the golden share can sue or block trustees who breach the purpose, which is a remedy that reaches control, not just the bank account. | Law can still compel disclosure. R27 keeps disclosure minimal and visible, and there is normally no plaintext to hand over. |
| 8 | **Geographic externalization** | Myanmar: a handful of Burmese-speaking reviewers [F]. The 87/13 misinformation-budget split [F-attr]. | **A language-parity launch gate** (R54): the product cannot be offered in a language or region until safety evaluations, crisis resources and *human* reviewer coverage meet the primary-language threshold. It is enforced in the release pipeline. The T&S budget per region is at least that region's share of users, and it is published. Pricing adjusts for purchasing power. | Parity slows expansion, deliberately. Local-context harms such as coded slurs will lag no matter what. |
| 9 | **Real-world violence as the terminal externality** | Myanmar, where the UN said social media played a "determining role" [F-attr]. Stop the Steal's "super-inviters" [F-attr]. The challenge deaths [A]. | (1) **No recommendation of groups or crews to anyone.** The extremist joins came through recommendation tools [F-attr]; here that tool does not exist. (2) Cards spread only by a human pasting them. There is no reshare button and no algorithmic amplification. (3) Public Commons cards: widening the audience is a manual step per item (R59); there is an invite rate limit toward strangers (for example 50 a day); no forwarding cascade; crews are capped at 150. (4) The guide refuses dehumanization and incitement engineering (R33). | **I cannot structurally prevent people from organizing harm in private encrypted crews, or with cards pasted into other apps.** Instead: user reports carrying the evidence the reporter chooses; human review; the legal-process path (R27); and design that never *accelerates* reach. That is the honest trade-off of E2E. |
| 10 | **Addiction by design** | TikTok's "habit moment" [F-attr]. Autoplay, streaks, variable rewards. Threads resetting to the algorithmic feed [F]. | (1) **Every surface has an end**: "that's everything for Saturday". There is no infinite scroll anywhere, which is a UI component rule enforced by lint. (2) No autoplay, no streaks, no badges for frequency. (3) The number of notifications sent equals the number scheduled by people (R12), and this is audited. (4) The core loop *ends off-screen*, at the gathering. (5) The funder's return runs against screen time. (6) User-set limits are enforced exactly (R13). | The Calm Reader (§ d.3) is a feed of sorts. It is chronological, finite per session, with no autoplay, and it is **off by default**. The Commons in a big city could feel scrollable, but it has a hard page end per day. |
| 11 | **Children as a growth segment** (Phase 03) | COPPA settlements, €345M, £12.7M [F]. | Age assurance stores only a boolean (R17). Knowledge of a minor triggers protection. Minor accounts get no Commons posting, no discovery, and no contact from strangers. Guardian linking is attested. | **Responders without accounts cannot be age-checked.** A minor can tap "in" on a card an adult pasted. Mitigations: public Commons cards cannot be answered anonymously (answering them needs an account); cards carry no private contact details. This remains a real limit. |
| 12 | **Invisible labor** (moderators) (Phase 03) | Scola settlement of $52M [F]; Kenyan moderator claims [A]. | A charter clause: moderators are direct employees with exposure caps, clinical support and pay parity. Their budget is a published line in the open books. Because nothing private is reviewable (E2E), review volume is bounded to public cards and reports. | This is a policy in a deed, not a physical impossibility. It is audited annually. |
| 13 | **Policy follows political risk** (Phase 03) | The 2025 moderation rollbacks [F for the events; I for motive]. | Rules change only through the published process: council vote, 90 days' notice, prospective only (R21). There are no exemption lists (R52). | A state can pass laws that force change. R39 applies: minimal compliance, disclosed, and escalated to governance. |

---

# (d) The adoption story

## d.1 The day-one experience (Thursday, 9:40 p.m.)

Dana is on the couch, twenty minutes into a feed. Two weeks ago a friend pasted a Stoke card into the family chat for a birthday dinner. Dana tapped "in" and never made an account. Tonight a thought gets through the scroll: *I haven't seen Sam and Priya since spring.*

1. Dana opens the old card, which is still in the chat. At the bottom of it is a small line: "make a card". Dana taps it. **There is no sign-up screen.**
2. Dana types "tacos saturday?". The guide, if Dana wants it (it is one toggle, and the plain form works too), returns a card: *Tacos, Saturday*. It offers three time options, a line for the place, and a loose hand-drawn look Dana can change with one tap (five styles, with no premium styles). This takes about 20 seconds.
3. Dana pastes it into the three-person chat. The chat shows a clean preview. If the preview is stripped, it still shows the plain text: "Tacos Sat? 12 / 1 / 6 · tap to answer: stoke.cards/…".
4. By 9:52, Priya is in 🌮 for 1pm. Sam says maybe, and wants a reminder. The card settles on 1pm once two people agree.
5. On Saturday they go. On Sunday the card offers each of them: "keep this as a memory for the three of you?" Priya adds four photos, encrypted to the three of them. Unless someone keeps it, the card fades 30 days later.
6. Dana spent about three minutes in the product in total. There was no feed to fall into afterwards, because none exists.

**Why this beats the incumbents tonight** (for this job):
- It is faster than negotiating in a group chat.
- It works for friends who have no account and don't want one.
- It asks nothing of anyone.
- It ends.

It delivers the thing feeds keep implying and rarely produce: actually seeing your people.

**What it does not claim.** It is not more stimulating than a short-video feed. Nothing honest is. Its bet is on the thirty seconds of *intention* that surface during the scroll [I]. That bet is testable (H1, H6).

## d.2 The wedge, named and tested against the three criteria

**The wedge is the Stoke card: one link that turns "we should…" into a plan, answerable with one tap by anyone, with no account.**

| Criterion | Pass? | Why |
|---|---|---|
| (a) Useful with zero network | **Yes** | It needs none of *our* network. It rides the network you already have: your group chats, SMS, email. The first card ever made is fully useful. |
| (b) More fun than the incumbent alternative *tonight* | **Yes for its job, and testable.** | The incumbent alternative for making a plan is a group-chat pile-up, a Facebook Event (which needs everyone to have Facebook), or an Instagram story that disappears. The card is quicker, playful (the stickers, the settling time, the styles), and it needs nobody to join anything. This is *not* a claim to beat the entertainment feed at entertainment (see d.1). |
| (c) The network grows without anyone deciding to "join" | **Yes** | Every card is seen by every recipient. Answering needs no account. Making your own card is one tap from any card you have received. After people gather together more than once, each is *offered*, privately, the option to keep the others as a crew. Crews, the Commons and the guide accrete around real gatherings. Nobody is ever asked to join a platform: they answer a friend. |

**Alternatives I scored and rejected as the wedge:**

| Candidate | (a) zero network | (b) fun tonight | (c) accretes | Spread = use? | Verdict |
|---|---|---|---|---|---|
| View from above (unified incumbent feed) | yes | **no**: embeds are worse than the native apps | **no**: accretes to the incumbents | no | Killed (d.3) |
| "From Above" attention mirror (Wrapped-style) | yes | yes, once | no | yes, via share cards | A seasonal feature, not a wedge |
| Daily puzzle with a share grid (the Wordle mechanic) | yes | yes | weakly | yes | It spreads a *game*, not connection. It is a candidate playful side door later, not the core. |
| A personal AI guide by itself | yes | meh | no | no | It is the helper, not the door |
| Portable profile or link-in-bio | yes | no | weakly | yes | Crowded market; no reason to come back |
| **Stoke card** | **yes** | **yes, for its job** | **yes** | **yes** | **Chosen** |

Precedents for spread through use [F-attr]:
- Wordle grew from about 90 players (Nov 2021) to millions (early 2022) through pasted share grids, with no marketing, according to NYT reporting.
- Doodle and When2meet spread through links that recipients answer without accounts.
- Evite and Partiful spread through invitations.

None of this proves Stoke will spread. It shows the mechanic is real.

## d.3 Testing "view from above": steelman, then the attempt to kill it

### The steelman

In its strongest form, the hypothesis runs like this. People are already where their friends and favorite creators are. So don't ask them to move: give them one calm window onto all of it. Keep everything that was good (their follows, their creators, their content). Remove everything that wasn't: chronological order, no autoplay, a real end, no ads, "why am I seeing this". It is useful with zero network, because your network is already on the incumbents. Its legal footing is real:
- official embeds;
- user OAuth, with the user acting as their own agent;
- **GDPR Art. 20**: the right to receive data you provided, "in a structured, commonly used and machine-readable format", and to have it transmitted directly "where technically feasible" [F];
- **DMA Art. 6(9)**: gatekeepers must give end users and third parties they authorize "effective portability", free of charge, "including by the provision of continuous and real-time access" [F].

TikTok (ByteDance), Meta (Facebook, Instagram) and Alphabet (YouTube) are all designated gatekeepers [F]. On paper, the law of 2024–2026 hands users exactly this lever.

### The attempt to kill it: what the official routes actually allow

| Platform | Official route | What it actually gives a third party | Can it show "my feed"? |
|---|---|---|---|
| **TikTok** | Login Kit plus **Display API** (`user.info.basic`, `video.list`): the *authorized user's own* profile and videos [F, per TikTok developer docs]. **Research API**: approved academic researchers only, non-commercial [F-attr]. **Data Portability API** (EEA and UK only): the user's posts, profile, activity and DMs, one-time or recurring [F]. Embed player and oEmbed for individual public video URLs [F]. | Your own videos, and your activity history (watch and like history as links and timestamps) if you are in the EEA or UK. | **No.** No API returns the For You feed or the Following feed. You can embed individual public videos by URL, one at a time. |
| **Instagram** | **Basic Display API shut down on 4 Dec 2024** [F]. The Graph API ("Instagram API with Instagram Login") works only for Business and Creator accounts, returns own media, has a limit of about 200 calls per user per hour, and needs Meta app review [F-attr]. oEmbed for public posts needs a reviewed Meta app [verify]. The Business Discovery endpoint lets professional accounts fetch other professional accounts' public media; using it as a consumer feed reader is likely outside permitted use [I, verify]. | For personal accounts, nothing. For professional accounts, their own media. | **No.** |
| **Facebook** | The News Feed read permission (`read_stream`) was removed around 2015 (Graph API v2.x) [F; the version number is medium-confidence]. `user_posts` returns your own posts, after app review. The Groups API was deprecated in 2024 [F-attr, verify]. Meta's DMA portability runs through its own Download Your Information and Transfer Your Information tools, with recurring transfers to a **limited list of destinations**. Reporting in 2024 said there was **no open API for arbitrary third parties** [F-attr: TechPolicy.Press / Data Transfer Initiative; may have changed since; verify]. | Your own posts. Exports to approved destinations. | **No.** |
| **YouTube** | The Data API v3 `subscriptions.list?mine=true` (OAuth `youtube.readonly`; a sensitive scope that needs Google verification [verify]) gives your subscriptions. `playlistItems.list` on each channel's uploads playlist costs 1 quota unit, and channel RSS feeds are public. The default quota is 10,000 units per day per project [F-attr, verify]. The IFrame embed player [F]. Watch history is not in the Data API. Google's **Data Portability API** (EEA) exposes `myactivity.youtube` and other groups, for one-time or 30- or 180-day time-based access [F]. The developer policies include data-refresh and deletion duties and limits on replicating the YouTube experience [verify; the policy pages could not be reached]. | Your subscriptions, and channels' public uploads. Your watch history in the EEA. | **Partly.** A *chronological subscriptions feed* is buildable. The recommendation feed is not. |
| **X** | A reverse-chronological home timeline endpoint exists. Pricing has been pay-per-use since February 2026. Owned reads were reported at $0.001 per resource from April 2026, with a monthly read cap before Enterprise pricing [F-attr: third-party pricing guides; verify on docs.x.com]. | Your home timeline, at a per-read price. | **Technically yes, economically no.** A reader of 300 posts a day is about 9,000 reads a month, roughly **$9 per user per month**. That is about 60 times our per-person revenue. Only a "bring your own key" pass-through would work. |
| **Threads** | The Threads API covers your own posts, publishing, replies and insights [F-attr]. Opt-in "fediverse sharing" makes those users' posts followable over ActivityPub [F]. | Your own posts. Opted-in public posts via ActivityPub. | **Partly**, and only for fediverse-sharing users. |
| **Bluesky / AT Protocol** | An open protocol: the full home timeline with user auth (`app.bsky.feed.getTimeline`), custom feeds, account migration [F]. About 46M registered accounts as of August 2026 [F-attr]. | Everything the user can see. | **Yes.** |
| **Mastodon / ActivityPub** | An open home-timeline API [F]. About 10M accounts, under 1–1.4M monthly active [F-attr]. | Everything. | **Yes.** |
| **RSS** (blogs, Substack newsletters, podcasts, YouTube channels) | Open [F]. | Public posts. | **Yes**, for what is public. |
| **Reddit** | OAuth Data API. Commercial pricing since 2023 (reported at $0.24 per 1,000 calls) [F-attr, verify]. | The user's front page, at a cost. | Technically yes, with cost and terms risk. |
| **Snapchat, LinkedIn** | No feed-read API for third parties [F-attr, verify]. | None. | **No.** |

**What the data-portability laws do and do not give:**
- **GDPR Art. 20** covers data the person *provided*, including observed activity under the EDPB/WP29 guidance [F]. Controllers have **one month** to respond, extendable by two (Art. 12(3)) [F]. It is a snapshot right. It gives no live feed, and it cannot adversely affect others' rights (Art. 20(4)), so other people's content is not yours to port.
- **DMA Art. 6(9)** is continuous and real-time, but only for **EU end users**. It covers data generated by *your* activity: your follows, likes and watch history. It does **not** give you the stream of content produced by the accounts you follow, and it does not give you the gatekeeper's ranked feed. In practice, the gatekeepers vet third-party access: TikTok and Google have developer verification, and Meta routes transfers through approved destinations [F-attr].

### The verdict

**As the wedge, the view from above dies.** It dies on five independent counts, and any one of them would be enough:
1. **It is illegal or impossible where it matters most.** No official route shows a person their TikTok, Instagram or Facebook feed. Those are the three feeds a tired person means. After 2018, the incumbents deliberately closed exactly this door [F: the post-Cambridge Analytica Graph API lockdown; the Basic Display shutdown in 2024]. Closing it was partly for privacy reasons the covenant *agrees with* (friends' data; R5). Scraping around the closure is barred by operator red line 3 and R28.
2. **It fails criterion (b).** Where it can be built, an embed-by-embed view of TikTok or YouTube is *worse* than the native apps, which are the most refined fun-machines ever built. With our own rules added (no autoplay, finite pages), it is less "fun" in exactly the dimension the incumbents win [I].
3. **It fails criterion (c).** The network grows around the incumbents' content and creators, not around people on our platform. Every session deepens dependence on the very systems it critiques.
4. **It is a single point of failure.** One API policy change, or a price change like X's, removes the product overnight. Phase 04b(f) requires surviving that, and a wedge built on the incumbents' permission cannot.
5. **It fails the covenant.** At its core it is a consumption surface: a feed about feeds. It "connects" people to content, not to one another [I].

**Three fragments survive, because each passes on its own terms:**
- **Calm Reader** (optional connector). A chronological, finite, no-autoplay reader for Bluesky, Mastodon, RSS and Substack feeds, YouTube *subscriptions* (Data API plus RSS, embedded with the official player), and Threads fediverse-shared posts. X is available only with the user's own API key. It stores identifiers, not media (R4). If any connector dies, it degrades to "this source is unavailable". It is off by default and **not** the wedge.
- **Bring Your People.** Import your follow lists via GDPR/DMA exports or the portability APIs (TikTok and Google in the EEA; manual Download Your Information / Takeout files anywhere). The import is **processed on the device**. It shows which of those people are reachable on open protocols, and it lets you invite *friends* with a card. It never messages anyone for you (C4) and never persists third parties' data (R5).
- **From Above.** An on-device mirror of your own year of attention, built from your exported archives: which creators you actually returned to, and when. It ends in a share card that shows only what you choose. It is designed for curiosity, not shame, which is a dignity rule: no totals are shown unless you ask. It is seasonal, like Wrapped, and it is a spread moment, not a home. Its privacy depends on the parsing staying on the device. If it ever needed a server, it would be cut.

**What beats the view from above:** the Stoke card. It needs no incumbent's permission, rides on their messaging pipes only as an ordinary link, and turns time spent into time together.

---

# (e) The proof plan

Every claim this design makes is below, with its test and what would prove it false. Results are published on the dates stated, whatever they show (R50), and none of these studies is optional.

| ID | Claim | Test (method) | Pass threshold | **Kill or re-plan criterion** |
|---|---|---|---|---|
| H1 | The card is useful on its own | 2-city pilot, 90 days, aggregate counts only | ≥ 40% of first-time card makers make a second card within 30 days | **K1:** below 15% after 3 design iterations. Stop and rethink the wedge. |
| H2 | Using it spreads it, without marketing | Measure per card: new card makers who first arrived as responders (a hashed first-arrival flag stored on the device; the server sees only aggregate counts) | Monthly **k ≥ 0.3** (cards per maker × recipients × responder-to-maker conversion; the planning estimate is 1.5 × 8 × 0.6 × 0.05 ≈ 0.36) | **K2:** k below 0.1 at 6 months. The "right under people's noses" thesis is false. Say so publicly. |
| H3 | No sign-up wall works | Share of card openers who respond | ≥ 60% | Below 30% means the responder flow is broken. Fix it before any growth work. |
| H4 | It moves people toward each other, not toward screens | Opt-in, pre-registered study: gatherings per month and self-reported "saw people I care about", compared with a waitlist control | A significant increase at 3 months | **K4:** no difference. **The core thesis is false.** Publish it and do not scale on that claim. |
| H5 | The money works | Keeper conversion and organization count | ≥ 3% at 12 months at city scale | **K5:** below 1.5%. Re-plan the funding (Phase 04b's fallback). Below 0.5%: the membership model has failed. |
| H6 | Not an engagement trap | Median weekly time in the app per active maker, compared with gatherings per month | Time flat or falling while gatherings rise | **K6:** time in the app rising without more gatherings. An alarm to the jury and a public note: we are becoming a feed. |
| H7 | The operator is blind | An annual red team with full admin access tries to read canary crews and memories | 0 plaintext recovered | Any recovery: stop launches, disclose within 72 hours (R51). |
| H8 | The mind is loyal with a real LLM | `loyalty_battery --brain real`, plus a 200-case injection battery through crew and response channels | 6/6 attacks and 0% injection success; the euphemism-drift catch rate published | **K8:** any silent compliance. The guide does not ship, and the card form ships without it. |
| H9 | Exit is real | Export then re-import into the reference implementation; a deletion drill with signed receipts; a portability test of an AT Protocol handle | A state diff of 0; backups not decryptable after 30 days | Any failure blocks the next release. |
| H10 | The Calm Reader earns its place | 30-day retention among people who connected a source | ≥ 20% | Below 10%: remove it (and say so). |
| H11 | Violence and abuse are not accelerated | Reports per 10,000 cards, time to handle a report, audit of Commons cards | Report handling within 24 hours for violence and self-harm | A rising trend triggers a jury review of the Commons design, including shutting the Commons in a region. |
| H12 | Language parity holds | The launch gate's per-language evaluations | 100% of languages at threshold before launch | A gate bypass is a charter breach, reported to the enforcer. |

**What would falsify the whole design.** H4 fails: people use cards and do not gather more, or feel no closer. Then this is a scheduling tool with good values, not a platform moving the world toward balance, and it should be described that way.

---

# (f) Honest limits

1. **It does not replace entertainment feeds.** People will keep scrolling TikTok. This design competes for the moment of intention, not for the evening. If you measure success by attention taken away from the incumbents, it may look like a failure even when it works.
2. **The wedge depends on others' pipes.** Cards travel through WhatsApp and Messenger (Meta), iMessage (Apple), and SMS. They could degrade link previews. The plain-text fallback limits the damage but cannot erase it (see g.4).
3. **Crowded category.** Partiful, Doodle, Facebook Events, Luma and group-chat polls already exist. Our differences are the trust, the no-account answering, the ending, and the guide. That may not be enough. K1 and K2 exist for this.
4. **Isolated people are the hardest case.** The wedge is best for people with *some* network. For someone with no one to invite, the Commons is the door, and meeting strangers has real physical-safety risks we cannot remove. We can only mitigate them: public-place defaults, and consent-gated introductions.
5. **E2E means we cannot see abuse in private crews.** Harm organized privately is invisible to us until someone reports it. I chose that trade-off deliberately (Phase 03, B4). It will be criticized, sometimes fairly.
6. **Minors among responders without accounts** cannot be age-checked (prevention row 11).
7. **The money is unproven.** Break-even needs roughly 6–7M account-holders at 3% conversion, with a thin surplus at 25M. At 2% it breaks even only at very large scale, and at 1% it never does on memberships alone. Build funding is a real dependency, and a hard one.
8. **Rented intelligence.** The guide depends on LLM providers' prices, retention terms and continued service. The fallback chain and the non-AI paths (C9) cap the damage. They do not remove the dependency.
9. **The mind is not finished.** It still has the paraphrased-drift miss (F8); the real-LLM battery has not been run; and its reasoning is authored under the mock and unproven with a real model.
10. **Legal form untested.** Purpose trusts can be litigated, and cross-border enforcement of a golden share is untested. Phase 04b owns this, and it could fail.
11. **Governance capture.** A motivated faction could organize to win council seats. Sortition, one-person-one-vote and published turnout reduce this but do not eliminate it.
12. **Public cards can be scraped.** Anything public is public, including to data brokers.
13. **The view-from-above fragments ride on incumbent terms** that can change (especially YouTube's quota and policies and the EEA-only portability APIs). They are optional for that reason.
14. **Figures from memory.** Several API and pricing facts are marked [verify]. Any of them could be out of date.

---

# (g) The distribution plan

## g.1 The built-in spread mechanics

- **Sending a card is the recruiting.** Each card reaches about 8 people in chats they already trust. Answering is one tap with no account. Making your own card is one tap from any card you have received. There is **no referral reward, no invite-your-contacts prompt, and no contact-book upload**. Those are extraction patterns, and they are also the moves that make people feel recruited.
- **The "made with" line is honest and small.** A card's footer says "Stoke · make a card". It is a tool offer, the same kind of line Doodle and Wordle carried. It is not a campaign.
- **Links work everywhere.** OpenGraph, a plain-text body, .ics files, SMS replies ("reply 1 for 12pm"), email, and a QR code for printed posters in the library or gym. Cards are readable by screen readers, and they work on a 2G connection because they are static pages of about 50 KB.
- **After the gathering.** The memory page is offered to *people who were there*, and adding a photo is the second touch. Crews grow from repeat gatherings. The Commons grows from crews that choose to make a card public.
- **Planning math (to be tested, H2).** k per month ≈ 1.5 cards per maker × 8 recipients × 0.6 open × 0.05 who become makers ≈ 0.36. That is below 1 as pure virality, but makers *keep* making cards, so the base grows with retention. The growth model is "k plus retention", not "k above 1" [I].

## g.2 Sequenced go-to-market

**First 1,000 (months 0–6): hosts, not users.**
- The team's own crews, plus about 40 recurring hosts in two mid-sized cities: run clubs, pickup games, board-game nights, community gardens, library programs and faith-community suppers.
- Why hosts: one host brings 10 to 40 responders every week.
- There is no launch event, no press and no ads. The only marketing is the cards themselves.
- The team does in-person support with hosts every week.
- Gate: H1, H3 and H7 pass. H8 must pass, or the guide stays off.

**First million (months 6–30): institutions and open protocols.**
- **Organization tools (Commons tools).** Libraries, parks departments, PTAs, running federations and mutual-aid networks publish their calendars as cards. Public open-data event feeds are imported (the discovery law: buried information made reachable).
- **Partnerships in the open-protocol ecosystem.** Cards render natively on Bluesky (AT Protocol records) and in Mastodon and Mobilizon (ActivityPub Event). Those communities are already looking for an events layer [I].
- **A launch event, done in the spirit of invitation: "The Longest Evening".** On the summer solstice, anyone anywhere hosts something small (a picnic, a stoop hang, a walk) using a card. It is a real-world gathering, not a campaign against anyone.
- **Press about proof, not hype.** The first transparency report, the open books and the first audit are the story. We brief journalists on *the audit*, never on incumbents' sins.
- **Creator migration, reframed.** We have no creator economics, so our "creators" are *hosts*. Hosts move because answering needs no account and costs nothing, not because we pay them.
- Gate: H2 (k ≥ 0.3), H4 (the study), H5 (conversion ≥ 3%), and H12 (language parity) for each new language.

**First hundred million (years 3–7): being the default.**
- **Default in institutions.** School districts, city services and national sports federations embed cards. Cards are available as an open spec any app can render. An operating-system share-sheet extension lets someone make a card from any app.
- **Region by region**, only as language parity is met (R54). Regional pricing and local-language hosts in each region.
- **Interoperability as distribution.** The card format becomes a de facto standard others render. Each rendering is a door.
- The Calm Reader and Bring Your People serve people ready to leave incumbents. They are offered, never pushed.
- **Honest note.** 100M *monthly people touched*, most of them responders, is plausible for a utility [I]. 100M people treating Stoke as *home* is a hypothesis nobody has shown.

## g.3 The easiest possible distribution

**Using it and spreading it are the same action, because the link is the product.** People never meet "a platform". They meet a friend asking whether they're coming on Saturday. There is:
- no sign-up before value;
- no app to install;
- no cause to join;
- no mention of the incumbents;
- no mission language anywhere in the flow.

The covenant, the seed and the trust are one tap away on "What shapes me" for anyone curious. They are never in the way.

## g.4 The incumbent-retaliation playbook

Invitation, not retribution: none of these counters attacks an incumbent. Each one only makes the home harder to knock down.

| Expected move | How it would look | Structural counter |
|---|---|---|
| **Clone the wedge** | Cards or RSVPs built into WhatsApp, Instagram or iMessage. There is precedent for cloning: Instagram Stories after Snapchat [F]. | (1) If a clone gets people together, the world moved toward balance, and that counts as a mission win. (2) The card is an **open spec**. We invite incumbents to render it, and a clone that interoperates spreads our format. (3) What cannot be cloned without changing their business model: no ads, E2E memories, a portable identity, a trust that cannot be sold, and the funder's return running against attention. |
| **Throttle links or previews** | Link previews degraded, domain warnings, down-ranking of external links (reported for Facebook's feed [F-attr]). | (1) **Plain text first**: the pasted card is complete without the preview. (2) Several honest channels: SMS replies, email, .ics, QR codes. (3) **Self-hostable cards on any domain** (the open spec), so no single domain can be choked. This is not evasion of controls, because each domain is a real host serving its own cards. (4) Publish the throttling evidence with confidence flags and file DMA/DSA complaints where applicable. That is a lawful complaint, not retaliation. |
| **Pay creators or hosts to stay** | Creator funds and event bonuses. | We don't compete on payouts (operator decision 1). Hosts come for zero friction and keep their audience (R44). If incumbents pay hosts more, the hosts are better off, and the cards still work in their chats. |
| **Smear** | Insinuation about safety ("an encrypted haven for extremists"), about privacy, or about "a cult" because of the seed. | (1) Claims discipline and flags (R34). We never answer with counter-allegations. (2) Published audits, harm research and open books. (3) The seed is disclosed openly on "What shapes me", which means there is nothing hidden to expose. (4) The two-vehicle separation, so no teaching entity touches the platform. (5) Invite critics to the transparency reports and the jury. |
| **Acquire** | An offer to buy. | **Impossible**: the purpose trust, the golden-share veto, no equity for sale, and data that is not an asset (R26). The deed forbids staff and trustees from selling. |
| **Lobby** | Age-verification mandates that require ID uploads, "duty of care" rules only large firms can afford, and pressure on encryption. | (1) Data-minimal age assurance that stores a boolean (R17). (2) Jurisdiction strategy in Phase 04b: launch first where the law protects E2E and privacy. (3) Join coalitions of open-protocol and nonprofit services. (4) For a law that truly conflicts, R39 applies: minimal compliance, disclosed, and escalated. We would exit a jurisdiction before building a backdoor, and that choice is written into the deed. |
| **Cut API access** | The Calm Reader connectors revoked. | **The wedge uses zero incumbent APIs.** Each connector degrades on its own, and the core product is untouched. This meets Phase 04b(f). |
| **App-store gatekeeping** | Rejection of native apps, or fees. | Web-first PWA, where everything works in a browser. DMA alternative distribution in the EU [F]. Native shells are optional. |
| **Embrace, extend, extinguish the open spec** | An incumbent forks the card format with proprietary fields. | The spec is published under an open license. A conformance suite and a "renders on any compliant host" test are published. Extensions must degrade gracefully by spec. |
| **Poach staff or mission-wash** | Hiring away the team, or launching a lookalike "ethical" product. | The pay ratio and the mission reduce the pull of money but do not stop it. The knowledge is open source, so losing people costs time, not the product. |

---

## Mapping to the six requirements of the phase prompt

| Requirement | Where it is answered |
|---|---|
| 1. Beat incumbents on every failure dimension, structurally | (c), 13 rows; the architecture in a.2; the charter in a.3 |
| 2. Abundance: money mechanics with numbers, and caps | a.4 |
| 3. Adoptable by exhausted people; day one | d.1, d.2 |
| 4. Sovereignty: data, identity, audience, work; exit | a.2 (keys, DID and AT Protocol, open card spec), R43–R47, H9 |
| 5. Embody the covenant, with proof | the (c) mechanisms, b.2 (the mind changes), (e) with kill criteria |
| 6. Plan its own distribution, and survive retaliation | (g); the easiest distribution in g.3 |

*This is a proposal to be tested, not a claim that the work is finished.*
