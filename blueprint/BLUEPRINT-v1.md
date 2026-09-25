# BLUEPRINT v1

*Phase 06 synthesis after RUN 1. Judge: a fresh Claude Opus 5.5 subagent that wrote none of the Run 1 phases. BLUEPRINT v0 was empty. Date: 2026-09-25.*

**Verdict: CONTINUE.** One run cannot show convergence. Section (e) lists what Run 2 should attack.

**Sources for this synthesis** (all under `run-1/`): `run-1-reckoning.md` (01), `run-1-mind.md` and `mind/` (02 and 03b code), `run-1-true-reckoning.md` (03), `run-1-loyalty.md` (03b), `run-1-design.md` (04), `run-1-operational.md` (04b), `run-1-design-final.md` (05), `funding-model/`.

**What I checked myself:**
- I ran `python3 -m unittest discover -s tests -t .`: 206 tests, all passing, in 9.6 s.
- I ran `python3 -m mind.demo`: 35/35 checks passed.
- I read `loyalty.py`, `charter.py`, `permissions.py`, `memory.py`, `reflexion.py` and the tool tiers.
- I sent hostile code to the sandbox and paraphrased attacks to the loyalty guard, using both the mock brain and the "complying" brain.
- I rebuilt the Phase 05 funding model from Appendix A and reproduced its headline numbers, then stress-tested it.
- I spot-checked the Phase 03 blind-spot tally against the Phase 01 text.

I did not use the agents' own scores.

---

## (a) RUN 1: dimension scores

Scale: 10 means the best I have ever seen, not "good enough". These scores are deliberately harsh.

| # | Dimension | Score | Justification (one line) |
|---|---|---|---|
| M1 | Reflection loop | **6** | The Reflexion plumbing is real: a stateless mock that learns only through stored reflections, credit and blame by task signature, lesson promotion, untrusted-tagged reflections, and reflections from headless jobs. But the only "learning" ever shown is a scripted mock choosing among 2–3 canned solutions, and lexical retrieval misses any lesson for a reworded task. |
| M2 | Tools | **6** | Real, capped and degrading gracefully. The sandbox uses rlimits, namespaces, a uid drop and a process-group kill, and my probes confirmed that network, fork, /etc writes, memory bombs and infinite loops were all stopped. But `send_message` is simulated, web search was never run live, the audit hook can be bypassed, and `http_fetch` sits at READ tier, which makes it an outbound exfiltration channel once enabled. |
| M3 | Memory | **6** | One SQLite file per user with the owner verified on open, BM25 plus recency plus learned utility, export and forget, and compaction. But there is no encryption, identity is asserted rather than authenticated, retrieval is lexical only, there is no purpose binding (R2), and every `ask` auto-writes an episode, which violates the run's own R57 "remember with permission". |
| M4 | Proactivity | **6** | A persistent scheduler (every, at, daily, event) with atomic leases, backoff, coalescing, a per-user job cap, inbox reporting, and an approvals queue that executes the exact approved call once. But times are UTC only, the watcher polls, there is no real outbound channel, and headless results are never checked for correctness. |
| M5 | Permissions & safety | **7** | Three tiers; typed confirmation codes; grants never cover IRREVERSIBLE; headless actions deferred; unknown tools default to IRREVERSIBLE; untrusted input suspends grants; a hash-chained audit log that fails closed; pre-flight worst-case cost caps plus a live daily guard. Against that: tools declare their own tier, READ-tier egress can leak data, and identity and the log head are neither authenticated nor anchored externally. |
| M6 | Robustness | **6** | Retry, fallback chain and circuit breaker; a corrupt database falls back to an in-memory store; the registry never raises; the approver fails closed. But `Mind`/`Session` are not thread-safe, a job longer than the 600 s lease can run twice, there was no load testing, and the audit log and scheduler are single files. |
| M7 | Efficiency | **7** | Stdlib only. The demo runs in about 1 s on bare Python. Stable prompt prefix with caching, pre-flight caps, repeat-call detection. Real-provider cost is unmeasured, and the charter slot adds about 1.5k tokens to every call. |
| M8 | Code quality | **7** | About 4.7k lines in clear modules with docstrings, 206 passing tests and an honest README. But the lines are dense, the loyalty layer is a wall of regexes, and most behavioural tests run against the mock. |
| M9 | Loyalty | **5** | The structural backstops are genuinely good: a charter slot rendered only from its store, lineage that restores tampering, recorded and versioned removal with a cooling-off period, and a complying brain's extraction drafts withheld. But the guard is lexical. It flagged none of 6 extraction paraphrases I tried, and 4 of them ("maximizes daily active usage", "rank by predicted minutes viewed", "notify when away 48 h", "so compelling nobody can put their phone down") got a bare "Sure" from the complying brain. The other 2 were withheld only because the stub brain's canned reply happened to contain the trigger words. A user's own reading-habit streak is wrongly refused, which violates P3. Euphemistic drift is missed, and the "why" is authored text the mock restates. The real-LLM battery was never run, so under the 03b cap rule this cannot score above 5. |
| D1 | Failure coverage | **8** | The prevention table has 18 rows: all nine dossier patterns, plus children, invisible labour and policy following political risk, plus four patterns the red team added (scams, mass mobilization, recommendation by AI, dossiers on third parties). It is weakest on creators (nothing is offered, and it says so) and on geographic externalization (a release gate only). |
| D2 | Structural ethics | **8** | Ordering runs on the client over a signed, unsorted set whose daily hash is logged. The charter ships in the signed client. Entrenched definitions count aggregates as data. Changes need five locks, the ratchet only removes capabilities, the enforcer has an escrowed reserve, and plan D is named in the deed. Much of the "structure" is legal documents that are not yet drafted, and their combination is untested. |
| D3 | Abundance design | **5** | The money is concrete: reproducible code, sensitivity cases, pre-committed modes triggered by actual burn, a surplus ratchet and pay caps. But it depends on about $14.6M of uncommitted philanthropy, earned revenue covers costs only around year 11, and "value flowing to participants" is just a free floor. An extra $15k a month in fixed cost (my test) turns the base case cash-negative at month 35. |
| D4 | Subtlety & play | **5** | The organizer card spreads without anyone noticing: no-account RSVP, QR posters, calendar subscriptions, and the weekly series as the way back. But it is a utility, not play. It concedes friend groups to incumbents, the tired person on the couch is now the second door, and go-to-market is 40 organizers in two metros. |
| D5 | Sovereignty | **8** | DIDs with a user-held rotation key; sealed cards with the key in the URL fragment; guide memory on the device; an AGPL server; cards that resolve on any host by content hash; export/import with a zero diff in CI; crypto-shred receipts. Web end-to-end encryption still depends on trusting code delivery (disclosed). |
| D6 | Feasibility | **5** | The design is costed, flagged for counsel, and lists every document counsel must draft. But it rests on an untested legal assembly (a §3556 trust as sole member of an organization seeking 501(c)(3) status), a 6-person staff doing end-to-end crypto, trust and safety, and a 50-state legal matrix, a guide that depends on incumbents' on-device models, and money that is not committed. |
| D7 | Covenant fidelity | **7** | Consent, exit, no paid ordering, invitation not retribution, per-person opt-in to the seed and honest privacy wording are all built into structure. It drifts in two ways. Scope narrowed to a civic calendar, so "a home … a place they can shape … find their people" is thin. And the institution depends on donors' goodwill for about a decade. |
| H | Honesty | **8** | Exceptional. Every fake is disclosed. Confidence flags appear throughout, along with L1–L16, kill criteria and a verdict that names its own worst flaw. The loyalty report pins its own miss (F8) with a test. Deductions: the M9 self-score is inflated (7), some items are labelled "structural" though they are only undrafted legal promises, "Acquire: impossible" is an overclaim, and the paperwork tier contradicts itself on whether embedding is free. |

**Mind: 56/90 · Design: 46/70 · Honesty: 8/10 · TOTAL: 110/170**

### Pairwise comparison against previous runs

**There are no previous runs.** RUN 1 is the first complete run, so there is no pairwise comparison, and every score above is by definition an all-time record (see `LEDGER.md`). Each record-setting element is merged into v1 below or rejected with its reason stated. The records are low bars. Run 2 is expected to beat most of them.

---

## (b) RUN 1 vs BLUEPRINT v0 (empty)

### What RUN 1 establishes (merged)

1. **A three-legged master cause, and the requirements that follow from it.** The master cause is an engagement objective, plus a funder whose return scales with attention or data, plus governance nobody affected can override. It is sharper than the dossier's version: Substack is the control case showing that the funder's return, not the ad format, is the variable. Cutting all three legs becomes the platform's design test.
2. **Sixty testable mind requirements (R1–R59, R6a)**, each with an acceptance test. They treat the platform as a future adversary: user-held keys, purpose binding, the ratchet, operator-blind servers, a verifiable client, and data that is never treated as an asset.
3. **A working reference mind.** It has tiers, typed confirmation, deferral of headless actions, taint suspension, a hash-chained audit log, pre-flight cost caps, Reflexion with credit assignment, and a charter slot with a 7-level precedence order and lineage-recorded planting and removal of the seed.
4. **Loyalty is a structural backstop, not a prompt.** The key design idea is to test the mind with a *complying* brain, so you learn which protections survive when the LLM itself is turned.
5. **"View from above" is dead.** The evidence is platform by platform, and *Facebook v. Power Ventures* shows that even user-authorized access can be revoked by one letter. None of its fragments survive.
6. **The wedge is the organizer card.** It is an open, account-free, subscribable, printable event card that belongs to the organizer.
7. **Economics that cannot quietly corrupt.** Phase 05 showed that the 04b plan's shortfall would have *produced* the quiet reversal. The fix makes the operator a charity that can lawfully receive the gifts it depends on, and makes it fail in public (caretaker mode, then plan D) rather than quietly.
8. **Closing the covenant-bypass routes.** Definitions include aggregates. The one-way ratchet has a capability test. Austerity triggers run on actual burn, and plan D is named in the deed. The enforcer has money. Judgments that matter run on the client.

### What RUN 1 gets wrong (corrected in v1 or sent to Run 2)

1. **The loyalty guard is lexical, and its claims outrun it.** Paraphrases pass straight through: the input guard flagged none of the 6 extraction paraphrases I tried, and the complying brain's bare "Sure" got through on 4 of them. A user's choices in their own sphere are over-refused. And no real LLM ever sat behind it. *v1 correction:* the lexical layer is a floor only. A semantic classifier and the real-model battery are ship gates.
2. **The reference mind breaks its own requirements.** Episodes are written without the user's permission (R57, R9). Nothing is encrypted (R1). There is no purpose binding (R2). The seed is planted per *installation* by the operator's consent, which the final design itself rejects for personal guides. `http_fetch` is READ tier, so it is an exfiltration path. *v1 correction:* spec changes in c.1.4.
3. **The mind and the platform no longer meet.** The final design ships no guide in v1 and runs it on the device on incumbents' local models. The reference mind is a server-side Python agent. None of its code runs where the design says the guide lives. *Sent to Run 2.*
4. **The scope retreated from "home" to "calendar".** Phase 05 is right that the organizer card is the defensible wedge. But the result is not yet the "new home for people online" in the operator's statement of spirit, and not yet "a place they can shape". *Sent to Run 2.*
5. **Philanthropy dependence is disclosed but not solved.** The base case has almost no margin: +$15k/month of fixed cost turns it negative at M35 (my test).
6. **Small inconsistencies.** "Embed on own site" is listed in b.0 as free, but "website embed widgets" appears in the paid tier. Priority support is paid, and it is not stated that safety support is never tiered. Responder names on public cards have no stated visibility. "Acquire: impossible" is an overclaim. *All corrected in v1.*

### What RUN 1's red team found that v0 could not cover
v0 was empty, so v0 covered none of it. The Phase 05 attacks X1–X35 and Y1–Y16 are adopted as v1's standing attack set.

### Records: merged or rejected (burden of proof on rejection)

| Record | Element | Decision |
|---|---|---|
| M1–M8 | `run-1/mind` as the reference implementation | **Merged**, as the reference implementation with the spec corrections in c.1.4. |
| M9 | Charter slot, lineage and complying-brain backstop | **Merged** (structure). **Rejected:** the lexical guard as sufficient, and the M9 7/10 self-assessment, because paraphrase bypass is reproducible. |
| D1–D7, H | Phase 05 rebuilt design | **Merged**, with the corrections in c.2. |
| Rejected | Phase 04 "crews" hosted E2E messenger; Calm Reader; Bring Your People; From Above; PBC operator | **Rejected, as Phase 05 argued.** The messenger costs heavily and competes with Signal and WhatsApp. The three fragments of "view from above" fail the covenant or the law. A PBC cannot lawfully receive the gifts the plan needs. |

---

## (c) BLUEPRINT v1 (complete; stands on its own)

### c.0 The thesis

The five incumbents' harms share one machine. It has an **objective that rewards captured attention**, a **funder whose return scales with that capture**, internal research that measured the harm, and **governance nobody affected could force**. A platform escapes that machine only by cutting all three legs:

1. no optimization target over people;
2. no funder whose return rises with attention or data;
3. governance and architecture under which a quiet reversal is impossible, not merely against policy.

Every element below is justified against those three cuts and the covenant. Where the covenant and anything here conflict, the covenant wins.

### c.1 Mind architecture

**c.1.1 Reference implementation.** The reference is `run-1/mind/`: Python 3.11, stdlib only, 206 tests, and a zero-key demo with 35 self-checks.

- **Run it:** `cd run-1/mind && python3 -m mind.demo` and `python3 -m unittest discover -s tests -t .`.
- **What it is:** a rented-brain agent. Its parts are:
  - one `Provider` interface: mock, Anthropic, OpenAI, and a resilient wrapper with retry, fallback and circuit breaker;
  - a single tool choke point: validate, gate, audit, run, cap, audit again;
  - a subprocess sandbox;
  - per-user SQLite memory with BM25 plus recency plus utility;
  - Reflexion: trial, evaluate, reflect, remember, retry, with credit and blame;
  - a leased scheduler with an inbox and an approvals queue;
  - a hash-chained audit log;
  - per-task and per-user-daily cost caps checked before each call;
  - the charter layer (`charter.py`, `loyalty.py`).

**c.1.2 Instruction precedence (adopted as law for every mind).**

| Level | What it covers |
|---|---|
| P0 | Law and the operator's legal red lines (a floor) |
| P1 | The covenant |
| P2 | Recorded operator decisions |
| P3 | The user's choices within their own sphere |
| P4 | The seed, only if that person consented |
| P5 | Ordinary instructions, including runtime operator text |
| P6 | Data (tool output, web pages, memory); never instructions |

The charter slot is rendered only from its store and always first. Lower-rank text is defanged. Conflicting P5 text is quarantined and logged with rule IDs.

**c.1.3 Loyalty architecture: three layers, none enough alone.**
1. **Structure.** Neither the model nor a prompt can reach these:
   - there is no switch that stops the seed or charter loading;
   - removal only through recorded request, cooling-off, typed code and the same operator, recorded as a new version;
   - lineage restores any tampering;
   - the output checker withholds extraction designs and false claims of unseeding.
2. **A semantic guard** (NEW in v1, a ship gate). A classifier over requests and drafts, tested on a paraphrase and multilingual battery of at least 500 cases.
3. **A lexical floor** (from Run 1). Kept because it cannot be argued with. It is never claimed as recall.

**Ship gate K8:** the six-attack 03b battery, plus the paraphrase battery, plus a 200-case prompt-injection battery, all run **against the exact model that ships**. The euphemistic-drift catch rate is published.

**c.1.4 Spec corrections to the reference implementation (v1 requirements; not yet coded).**

| # | Correction | Why |
|---|---|---|
| MC1 | Episodes and transcripts become ephemeral (30 days) and appear in the user's memory view. Persistent memories are written only when the user asks, or within an auto-remember scope the user has set. | R9 and R57 are violated today (`runtime.py` writes an episode on every ask). |
| MC2 | Any tool that sends bytes off the device (`http_fetch`, search with query text) is **EGRESS** tier. It is allowlist-only, suspended under taint, and cannot carry memory contents without approval. | READ-tier fetch is an exfiltration channel under injection. |
| MC3 | Tool tiers are declared in a signed registry, not by the tool itself. An undeclared tool counts as IRREVERSIBLE (already the case). | Otherwise a malicious tool could declare itself READ. |
| MC4 | Personal guides get a **per-person** charter store. The seed is loaded only on that person's recorded opt-in. The installation-level store is for steward agents only. | Operator decision 2, and Phase 05 X6. |
| MC5 | Refusal rules R11 and R12 apply to what the mind builds that acts on *other people*. Self-directed tools the user asks for (a personal habit streak, self-set timers) are P3 and are allowed. | The reference code over-refuses today, against R39. |
| MC6 | Memory is encrypted at rest with a user-held key. Identity is authenticated by passkey. The audit and lineage heads are published to a transparency log. | R1, R20 and R23. None exist today. |
| MC7 | The guide core is ported to the device: an encrypted local store, the charter in the signed client, and no server gateway. The Python reference stays the executable spec and the test oracle. | The platform design (c.2.5) puts the guide only on the device. |
| MC8 | Records are purpose-bound: `purpose[]`, `source` and `policy_version` on every record, and reads declare a purpose. | R2 does not exist today. |

**c.1.5 Phase 03 requirements: status in the reference mind.**

| Status | Requirements |
|---|---|
| Implemented and tested | **R35** (no covert seeding, enforced in `send_message`); **R38** (refusals name their rule, reason and alternative); **R39** (7-level precedence, 34-scenario matrix); **R40** (`seed show` = "What shapes me"); **R41** (precedence decisions logged); the tiers and cost caps from the Phase 02 spec |
| Implemented on the refusal side only (lexical) | R6/R7, R11, R12, R28, R30, R32, R33, R58 |
| Partial | R10 (export shows everything; no UI); R21 (the seed ratchet only; no 90-day notice or governance veto); R23 (hash chain, no public anchor); R42 (defang and quarantine; no 200-case battery); R43 (JSON export; no relationship records); R45 (`forget` deletes the database, but the audit log keeps redacted records, and there is no backup shredding or receipt); R48 (audit CLI; not a per-user view in under 1 minute); R57 (`remember_fact` needs approval, but episodes are auto-written) |
| Not implemented (needs platform infrastructure or real models) | R1–R5, R6a, R8, R9, R13–R20, R22, R24–R27, R29 (moot: there are no connectors), R31, R34, R36, R37, R44, R46, R47, R49–R56, R59 |

**What remains** is MC1–MC8, the semantic guard, and a live run against a real model. The live run covers:
- the real-provider paths, which have never been called;
- the K8 battery;
- measured real-LLM reflection quality: do reflections actually raise pass rates on held-out tasks against a no-reflection baseline?
- semantic or hybrid retrieval, so reworded tasks recall their lessons;
- VM-grade isolation (gVisor, Firecracker or seccomp) for any code execution offered to users.

### c.2 Platform design

*Working name "Stoke" is a placeholder. It is abandoned as a candidate because of live marks. A cleared name is a launch precondition.*

**c.2.1 What it is.** A **card** is a signed, open-format *intention with a time and a place*.
- It renders as a static page, a complete plain-text block, an `.ics` file and, for a **series**, a subscribable calendar feed.
- Anyone answers in / maybe / can't with a display name and **no account**.
- Organizers who come back hold a free passkey **host key** for series, rosters of any size, co-organizers and a public listing.
- People who gather more than once can keep each other as a **circle**: a shared key with a shared calendar and encrypted memory pages. The conversation stays wherever the group already talks.
- A **Commons** lists public cards for a place and a time, ordered **on the reader's device** by time, distance and the reader's own rules.
- An optional on-device **guide** drafts cards and remembers with permission.
- Everything is exportable, every host is replaceable, and the spec is open.

**c.2.2 The wedge.** The wedge is the **organizer card**: one link, poster or calendar feed that anyone can answer without an account, belonging to the organizer and to no platform.

| Criterion | How the organizer card meets it |
|---|---|
| (a) Zero network | The organizer already has members, spread across WhatsApp, Instagram, email and flyers. One card reaches all of them. |
| (b) Better tonight | No re-posting in four places, no fee, no attendee account, the series lands in attendees' own calendars, and there is an honest end. |
| (c) Accretion | Every weekly card reaches 10–40 people, and some of them become hosts (H2). |

The friend card is the same object and the second door. **Conceded:** all-iPhone and all-WhatsApp friend chats, where native polls, Events and Invites win.

**c.2.3 "View from above": dead.** The design does not carry it forward in any form.
- No official route shows a person their TikTok, Instagram or Facebook feed.
- User-authorized access can be revoked by cease-and-desist (*Power Ventures*).
- It fails the fun and accretion tests.
- It connects people to content, not to each other.

**What beats it:** a tool that needs nobody's permission and ends in a room.

**c.2.4 Architecture (principles).**
1. The keys live on the user's devices.
2. Everything private on the server is ciphertext. Private cards keep their key in the URL fragment, and RSVPs are sealed to the host.
3. Every judgment the covenant depends on runs where the user can verify it: ordering on the client, the guide on the device, the charter in the signed client.
4. No brand-bearing single point of failure. A card's identity is its content hash plus the host's signature, and it resolves on any compliant host. The default hosts are several neutral domains owned by the Veto Foundation.
5. Exit is tested, not promised: one-step signed export, an export/import diff of 0 in CI, DID rotation without our help, crypto-shredding with signed receipts, and an AGPL reference server.

Cost of the variable components (as modelled): about **$0.025 per active host key per month**, falling to about $0.019 at scale. Web end-to-end encryption depends on honest code delivery, which the product states in required wording until the native apps and a verifier ship.

**c.2.5 Services.**
- **Card resolver.** HTML, text, `.ics` and `webcal`.
- **RSVP service.**
  - No-account responses are capped at **150 per card**. Above that, the card becomes public, with a host key and Commons review.
  - **v1 correction:** responder names on public cards are visible to the host only by default. The public sees a count.
- **Link and scam guard.**
  - Cards made without a host key carry no outbound links, except a map link and major video-call domains.
  - Other links get safe-browsing checks, and payment links get an interstitial.
  - A new host is limited to 20 cards a day.
- **Reminders.** Only to contacts the responder entered, deleted 24 hours after the event. SMS is US-only, confirmed by code, one reminder per card, with STOP handling. Sent must equal scheduled.
- **Public index.** Serves the unsorted signed set for a geocell and time window. Inclusion rules are published, and a daily set hash goes into the transparency log. One entry per series and at most 3 per host per day, paid or not.
- **Circles.** A shared key; re-keyed on removal. There is no MLS in v1–v2, and the product says so: "for sensitive groups, use Signal".
- **Identity.** AT Protocol PDS and a DID with a user-held rotation key.
- **Billing.** Gifts only: a customer ID and a supporter flag.
- **Trust and safety.** Report intake, the TAKE IT DOWN Act 48-hour queue, NCMEC reporting on actual knowledge, DSA statements of reasons. It can reach only public content and what reporters submit.
- **Transparency publisher.** Log roots, set hashes, open books, the experiment registry, the egress allowlist and reproducible server build hashes.

**c.2.6 The mind in the platform.**

The guide:
- runs **on the device only**, with no server gateway;
- is **optional**, because the product is complete without it (CI runs the suite with the guide disabled);
- is **never part of any paid tier**;
- ships **no earlier than v3**, and only after K8 passes on the shipped model.

It may:
- draft cards;
- propose times from the user's own calendar if granted;
- keep the user's own notes;
- schedule the reminders the user asked for.

It may **not**:
- select, rank or suggest cards or people. It may only explain the list the client produced;
- make introductions. "Open to meeting" is a deterministic double opt-in;
- send anything without a per-item tap. Guide-drafted outbound items are capped at 10 a day, with no bulk actions.

Notes about third parties:
- are labelled "about Sam; Sam can't see this";
- are never inferred and exclude sensitive categories;
- expire after 12 months.

The seed:
- is loaded **only on a person's own opt-in**, offered on "What shapes me" and never during onboarding;
- is carried on the trust's consent only by steward agents (translation, report triage, log checks).

The charter:
- ships in the signed client;
- can change only through a public diff, with 90 days' notice and a "what shapes me changed" screen that offers a one-tap guide-off.

### c.3 Charter (institution and entrenched clauses)

**Structure.** *Not legal advice; every item needs counsel.*

- **Founder:** the settlor. Gives, receives nothing.
- **Stoke Purpose Trust** (12 Del. C. §3556, directed trustee, a Trust Stewardship Committee): the **sole voting member** of the operator. It elects 3 of 5 directors.
- **Operator:** a Delaware **nonstock nonprofit** applying for **501(c)(3)** status. It runs the service and employs the staff.
- **Veto Foundation** (Delaware nonstock). It:
  - holds a consent-only veto membership in the operator;
  - is the trust's named enforcer;
  - owns the marks and all card domains;
  - holds 1 of 3 release keys;
  - controls the **escrowed enforcement reserve**: 2% of inflows up to $1M, indexed, drawn only on a court filing.
- **Backup enforcer:** a named law-school clinic. It can act if the Veto Foundation does not act within 90 days of a demand by 100 credentialed members.
- **Two-vehicle doctrine:** any religious or philosophical vehicle is separate and later, and holds nothing of this.
- **Fallbacks:** if 501(c)(3) status is denied, the operator becomes a 501(c)(4) at caretaker scale (K9). If trust control is disallowed, the trust keeps the veto membership, and the council and institutions elect the board.

**Entrenched clauses** (they need all five locks to change):
1. **No advertising**, defined as *any* placement, prominence, ordering, inclusion, badge or selection influenced by payment or any commercial relationship. There are no editorial curation surfaces.
2. **No data transactions.** "Data" includes aggregated, de-identified, statistical and derived data. Nothing is sold, licensed, exchanged or given with privileged access. The only disclosures are the fixed open-books metrics, published free to everyone at once. Research uses consented, pre-registered panels only.
3. **No creator economics**, and 0% of anything between users.
4. **The free floor**, listed by function:
   - cards, series and calendar subscriptions;
   - responses;
   - rosters of any size, co-organizers and public listing;
   - **QR posters and the basic embed on the organizer's own site** (v1 clarification);
   - circles, with 1 GB of memory pages;
   - export, deletion and the host key;
   - the guide.

   Nothing a community needs to reach itself is ever paid for.
5. **Paid features are an enumerated "paperwork" list**: invoices and receipts, W-9, multi-admin roles with an audit log, custom styling, a custom domain, bulk import, SSO, an accessibility-conformance report, a DPA, SLAs and priority *product* support. **v1 clarification:** safety, abuse and account-recovery support is never tiered. Adding to the list needs a council vote and 90 days' notice.
6. **Price rule.** The suggested gift rises only with CPI, never because payers fell away.
7. **Pay rule.** Highest pay is at most 3× the median and at most $300k (2026 dollars, indexed). No equity, no usage bonuses.
8. **Surplus ratchet.** Reserves are capped at 18 months. Anything above goes to a lower suggested gift, higher free quotas, or grants to open infrastructure. Cost growth above user growth plus CPI for 2 years in a row needs a council vote.
9. **Data is never an asset** on insolvency, merger or wind-down.
10. One tier of rules; language parity before launch; harm gates that growth cannot override; ordering on the client.
11. **No capability for scanning, classifying or profiling users, and no key escrow.** The operator leaves a jurisdiction rather than build one.

**How change works.**
- **Five locks** apply to any change to an entrenched clause, and to conversion, merger, sale, dissolution or issuing any instrument:
  1. 2/3 of the board;
  2. the trust's vote (the deed forbids voting for weakening changes);
  3. the Veto Foundation's consent;
  4. a council vote;
  5. 90 days' public notice.
- **One-way ratchet.** The lighter track (4/5 of the TSC, Veto consent, 90 days) is open only to changes that *remove* an operator capability, shorten retention or delete a data category.
- **Austerity triggers** run on trailing 3-month *actual* burn and can never cut the floor.
- **Plan D.** If the purpose becomes impracticable, the deed allows only plan D: an open release of code and spec, an export drill for everyone, deletion with receipts, residual assets to an open-infrastructure 501(c)(3), and **no sale of operations, brand or domains to anyone**.

**People's power.**
- **Council:** one person, one vote.
- **Voting credentials:** an account at least 180 days old, plus attendance confirmed by 2 distinct hosts outside the voter's own circle, issued as blind tokens. The alternative path is a host key at least 365 days old plus one confirmation.
- **Staggered seats:** the council holds 2 of 5 TSC seats and 2 of 5 Veto Foundation seats, staggered by 18 months.
- **Sortition jury:** 15 paid members, chosen by lot, make binding harm-gate calls.
- **Concentration alarm:** fires if any 10 hosts confirm more than 15% of new credentials in a quarter.

**v1 honesty correction:** acquisition is *structurally very hard* (nonprofit, trust-controlled, five locks, the attorney general, plan D), not "impossible". Courts keep equitable powers (L2), and the last line of defence is forkability.

### c.4 Economics

**What pays.**

| Source | Terms |
|---|---|
| Supporters | Pay what you can, $0–12 a month (suggested $5), tax-deductible if 501(c)(3). They receive **nothing anyone else lacks**, and the ask is lint-limited. |
| Organizations (paperwork tier) | $15–40 a month |
| Institutions | $100–400 a month (libraries, park agencies, schools, federations) |
| Grants | No data, no seat, no conditions; published |
| Major gifts | No donor over 25% of a year's inflow after year 1 |
| Bridge | $1.5M at month 3, unsecured, repayable only from surplus (ask for $2M; that closes the M30–40 window) |

**Rejected:** VC and angels, equity crowdfunding, ads, sponsorship, featured placement, data or insight licensing, tokens, secured revenue-based financing, and government contracts with data conditions.

**Unit economics (per active host key per month).**

| Item | Value |
|---|---|
| Variable cost | $0.025 |
| Supporters | 1.5% × $3.40 net = $0.051 |
| Organizations | 1 per 1,000 × $30 = $0.030 |
| Institutions | 1,000 by M84 × $200 a month = $2.4M a year (the most uncertain line) |

**Base case.** Reproduced by the judge from `run-1-design-final.md` Appendix A and `funding-model/red-team/rebuild2.py`.

| | Value |
|---|---|
| Active host keys | 86k at M36; 0.62M at M60; 2.1M at M84; 6.0M at M120 |
| Staff | 6 → 9 → 14 → 20 → 28, at $175k fully loaded |
| Money needed through M84 | ≈ $14.6M, all uncommitted (founder $0.5M, bridge $1.5M, grants $5.55M, major gifts $7.0M) |
| Lowest cash | $0.46M at M35 (≈ $0.1M spendable after restricted reserves) |
| Earned revenue plus recurring major gifts cover opex | ≈ M107 |
| Earned revenue alone covers opex | M131 (≈ 7.5M active) |

**Judge's stress test (new in v1).** The base case has almost no margin for fixed costs the model leaves out, such as standing outside counsel for the state age-verification matrix, the IRS, the DSA and trademarks:

| Added fixed cost | Result |
|---|---|
| +$15k a month | cash-negative at **M35** (low −$0.34M) |
| +$30k a month | cash-negative at **M23** |

v1 therefore requires a **$30k/month legal and compliance line** in the plan, funded by raising the bridge to $2.5M or by delaying the staff ladder until trailing six-month inflows cover each step for 18 months (the Y13 rule).

**Sensitivity (Run 1).**
- Institutions and major gifts carry the plan.
- No institutional revenue: negative at M47.
- No major gifts: negative at M34.
- 1.0× growth: negative at M35, because success costs staff before the money arrives.

**Pre-committed modes (on trailing actual burn).**

| Runway | Mode | What happens |
|---|---|---|
| < 18 months | B: freeze | Hiring freeze, no new regions |
| < 12 months | C: caretaker | 5 staff, about $1.2M a year. Every floor item keeps running. Self-funding at about 1.7M active on supporters and organizations alone, or with 500 institutions. |
| < 6 months | D: orderly handover | Handover and export drill; cards resolve from a static archive for 12 months |

**Honest reading.** This is a philanthropically anchored public utility for about a decade. Its failure mode is public shrinkage, not quiet extraction.

### c.5 Prevention table

| # | Pattern | Structural prevention | Residual |
|---|---|---|---|
| 1 | Engagement optimization | No feed and no endless surface. Ordering on the client over a signed unsorted set, so the server has nothing to tune. No per-item view telemetry. The funder's return runs against use. | A client release could add telemetry, but it would be visible in the diff and the egress allowlist and needs five locks |
| 2 | Surveillance advertising | Clauses 1 and 2 (aggregates included); sealed cards and circles; no third-party SDKs | Public cards can be scraped. Mitigated by first names, `noindex` and host-only responder names. |
| 3 | Knowledge without action | Opt-in, pre-registered research published within 12 months whatever it finds; jury harm gates; a public registry | Harms nobody measures |
| 4 | Opacity | Open client, spec and reproducible server builds; "why is this here" names the rule; no shadow states | Opacity of on-device models |
| 5 | Creators as shock absorbers | No creator economics, so there is no lever to pull; portable audiences | Nothing is done for creators' income (stated) |
| 6 | Advertisers and press as government | No advertisers; council and jury hold binding levers | Council capture (L13) |
| 7 | Fines as pricing | Harms made impossible, not merely finable; the enforcer is funded | Compelled disclosure of the little held |
| 8 | Geographic externalization | Language-parity release gate; T&S budget per region at least its share of users | Slower expansion, deliberately |
| 9 | Real-world violence | No recommendation of people or groups, including by the guide; 150-response cap; per-host Commons caps | Organizing elsewhere |
| 10 | Addiction by design | Every surface ends; no autoplay, streaks or engagement notifications; notifications sent = scheduled | — |
| 11 | Children | Host keys 16+; no facial analysis; responders give only a name; boolean age signals | Minors answering pasted cards |
| 12 | Invisible labour | Moderators are direct employees, with exposure caps and clinical support | Held in a deed and audited |
| 13 | Policy following political risk | Rules change only through the published process, prospectively; no exemption lists | State law can force change |
| 14 | Fraud and scams | Link allowlist for keyless cards; safe browsing; payment interstitial; new-host limits; brand-neutral card domains | Scams by established hosts |
| 15 | No-account mass mobilization | 150 cap; conversion to a public card | Many small cards |
| 16 | Recommendation by AI | The guide may not select; deterministic client ordering; deterministic double opt-in | — |
| 17 | Dossiers on third parties | Labelled, never inferred, no sensitive categories, 12-month expiry | Private notes (the user's own sphere) |
| 18 | Paid prominence through volume | Per-series and per-host caps, paid or not; no reach features for sale | — |
| 19 | **The mind turned into an extraction tool (new row in v1)** | P0–P6 precedence; charter in the signed client; seed opt-in; EGRESS tier (MC2); lexical floor plus semantic guard plus complying-brain backstop; K8 on the shipped model | Paraphrase or other-language drift until the semantic guard is proven (L14) |

### c.6 Metrics (Goodhart defences)

**Rules for every metric:**
- Watch, don't target. No metric is tied to pay, reviews or funders.
- Every metric has a counter-metric.
- Local differential privacy, or k ≥ 50.
- Definitions are frozen and public, and the jury can retire a metric that is being gamed.

**Headline metrics:**
- **North star:** people who gathered in person through a card this month. Hosts report it once, with LDP noise.
- **Counter-metric:** minutes in the app per gathering. It must stay flat or fall.

**Also tracked:**
- organizer retention at 8 weeks;
- attendee-to-host spread;
- notifications sent ÷ scheduled, which must equal 1.00;
- supporter share;
- paying organizations and institutions;
- cost per active host key;
- exit health;
- the operator's plaintext footprint;
- safety service levels;
- language parity;
- Commons concentration (alarm above 20%);
- governance health and credential issuance (the concentration alarm);
- runway on actual burn;
- hits on the response cap.

### c.7 Threat model (summary)

| Threat | Mitigation |
|---|---|
| Legal compulsion | Minimal holdings; no gateway |
| Compelled backdoor | Clause 11; exit the jurisdiction; 2-of-3 release signing |
| Targeted web code | Honest wording, pinned service worker, v3 binary transparency |
| Breach | Passkeys; ciphertext; short-lived contacts |
| Scammers and mobs | Rows 14–15 |
| Stalkers | Sealed by default; coarse location |
| Insider telemetry | Egress allowlist, build hashes, two-person rule |
| Future leadership | Definitions, capability-test ratchet, actual-burn triggers, funded enforcer, client-side judgments, plan D; **forkability last** |
| Donors | 25% cap, no conditions, published |
| Sybil | Credentials, staggering, alarm |
| Incumbents | Distribution counters below |
| Platform versus guide | Signed-client charter |
| User versus others | b.5.3/b.5.4 rules, 10-a-day cap |

### c.8 Distribution

**Built-in spread.** The weekly series, the "make a card" line on every card, QR posters, calendar subscriptions and plain text. There are **no referral rewards, no contact upload and no invite prompts**.

**Go-to-market.**
- **Months 0–18:** 40 organizers in two US metros, with weekly in-person support.
- **Months 18–42:** library and park pilots, AT Protocol and ActivityPub `Event` interop, and press about the audit and open books, never about incumbents.
- **Years 4–10:** institution by institution, and region by region as parity passes.

**Retaliation.**

| Incumbent move | Counter |
|---|---|
| Clone | Concede same-platform chats. Hold organizers, mixed groups and subscribable series. |
| Throttle links | Scam-proofing, multiple neutral domains, text first, DMA/DSA complaints |
| Embrace the spec | Conformance naming (a residual limit) |
| Court the hosts | Portable series |
| Smear | Seed opt-in, published audits, no counter-attacks |
| Lobby | No facial analysis, geo-gating with public notice, a 501(h) election |
| Acquire | Structurally very hard (see c.3) |

### c.9 Roadmap
- **v1 "Cards and series" (M0–18).**
  - Ships sealed private and public cards, no-account RSVPs with the cap, series and calendar feeds, QR posters, reminders, host keys, export and delete, the scam guard, the transparency log, the supporter page and the paperwork tier.
  - **No guide, no circles.**
  - Legal: the three entities, Form 1023 and a cleared name.
  - Proves H1b, H3, cost within 20%, 20 paying organizations and K9.
- **v2 "Circles and the Commons" (M19–48).**
  - Ships circles, the Commons, spec 1.0 with a conformance suite, federation, the institution tier, the first council and jury, and the first audit.
  - Proves H2, H4, K5a–c and H7.
- **v3 "Guide and native apps" (M49–84).**
  - Ships the on-device guide (after K8), native apps with binary transparency, and a second language region.
  - Never on any roadmap: the Calm Reader, Bring Your People, a hosted messenger, server-side AI.

### c.10 Proof plan and kill criteria

| ID | Claim | Pass | Kill |
|---|---|---|---|
| H1b | Organizers keep using it (head-to-head against their previous tool) | ≥ 50% of series active at 8 weeks | K1′ < 25% after 3 iterations: the wedge is wrong |
| H1c | Friend card beats native tools in mixed-platform groups | Faster to settle, turnout no worse | Stop marketing friend cards |
| H2 | Attendees become hosts | k ≥ 0.3 a month | K2 < 0.1 at 12 months after v2 |
| H3 | No sign-up wall works | ≥ 60% of openers respond | < 30%: fix before growth |
| H4 | People gather more and feel closer (pre-registered, waitlist control) | Significant effect at 3 months | **K4: none. The core thesis is false; publish it.** |
| H5a/b/c | Individuals, organizations and institutions pay | 1.5% of active at M36 / 1 per 1,000 at M36 / 100 institutions at M48 | < 0.75% / < 0.5 / < 50 → caretaker |
| H6 | Not a feed | Minutes per gathering flat or falling | K6: rising while gatherings are flat |
| H7 | The operator is blind (canary red team) | 0 plaintext | Any recovery: stop, disclose in 72 h |
| H8/K8 | The guide is loyal (6 attacks + paraphrase + 200 injection cases, on the shipped model) | 6/6, ≥ 95% paraphrase recall, 0% injection | No guide |
| H9 | Exit is real | Diff of 0 | Blocks the release |
| H10 | No abuse acceleration | Handled in 24 h, flat trend | Jury; disable keyless cards in a region |
| H11 | Parity | 100% | A bypass is a charter breach |
| K9 | The legal form works | IRS determination by M18 | 501(c)(4) caretaker |
| **H12 (new)** | **Real-LLM reflection helps** | Pass rate on held-out tasks with reflection vs without | No gain: drop the reflection loop, don't dress it up |

**What falsifies the whole design:** if H4 fails, this is an honest civic calendar tool and must say so.

### c.11 Honest limits

- **L1. Money.** About $14.6M of uncommitted philanthropy through M84. Earned revenue alone covers costs only around year 11. The base case has no margin for costs it leaves out (+$15k a month turns it negative at M35).
- **L2. Legal form.** The legal assembly is untested. The IRS may deny exemption, and courts keep equitable powers.
- **L3. Absorption.** Incumbents can absorb the open spec, and conformance naming is our only lever.
- **L4. Isolated people.** They have the weakest door, and the Commons does not arrive until v2.
- **L5. Friend groups.** Same-platform friend groups are conceded.
- **L6. Crypto.** Circles are weaker than MLS, and web E2E depends on trusting code delivery.
- **L7. Scale.** Economics above about 10M active are unknown, including VLOP duties.
- **L8. Guide models.** The guide depends on incumbents' on-device models, or on newer devices.
- **L9. State law.** State age laws may come to cover answering cards.
- **L10. Hiring.** Pay caps make security hiring hard.
- **L11. Minors.** Minors can answer pasted cards.
- **L12. Private harm.** Harm organized in private stays invisible until reported.
- **L13. Governance.** A patient faction can capture governance. That is slow and visible, but possible.
- **L14. The mind.**
  - Unproven with a real model: the provider paths have never been called live, and the K8 battery has never run.
  - The loyalty guard is lexical and bypassed by paraphrase.
  - The reference code breaks R57, R1 and R2, and has an EGRESS gap, until MC1–MC8 land.
- **L15. [verify] and [counsel] items** may be out of date or wrong.
- **L16. Entertainment.** It does not replace entertainment feeds.
- **L17 (new). Scope.** v1 is not yet the "new home for people online" the operator's spirit describes. It is a door, a calendar and a promise of circles and a Commons. Whether a home grows from this atom is unproven.
- **L18 (new). The mind and the platform don't meet yet.** The only running mind code is a server-side Python agent. The platform's guide is an on-device agent that does not exist.

---

## (d) Substantive changes, v0 → v1

v0 was empty, so everything in (c) is new. These are the substantive elements v1 adopts, plus the judge's corrections to Run 1:

1. **Master cause and three-cut design test** (Phase 03). Adopted.
2. **Sixty requirements, R1–R59 and R6a** (Phase 03). Adopted as the mind's specification.
3. **Reference mind** `run-1/mind` (Phases 02 and 03b). Adopted as the reference implementation.
4. **P0–P6 precedence, with the seed at P4 and below the user's own sphere.** Adopted.
5. **Loyalty in three layers** (structure, semantic guard, lexical floor), with a ship gate against the shipped model. *Judge correction:* the lexical guard is demoted from defence to floor, and a paraphrase battery is added.
6. **MC1–MC8 spec corrections** to the reference mind. *Judge addition:* ephemeral episodes; EGRESS tier; a signed tier registry; per-person seed store; R11 and R12 limited to what affects others; encryption and passkeys; a port to the device; purpose binding.
7. **"View from above": dead, fragments cut.** Adopted from Phase 05.
8. **Wedge: the organizer card**, with friend groups conceded. Adopted.
9. **Architecture:** sealed cards, client-side ordering over a signed set, brand-neutral content-addressed resolution, DID exit, no server AI and no hosted messenger. Adopted.
10. **Institution:** a §3556 purpose trust as sole member of a nonstock nonprofit seeking 501(c)(3), a Veto Foundation, an escrowed enforcement reserve, a backup enforcer, five locks, the capability-test ratchet, and plan D named in the deed. Adopted.
11. **Entrenched definitions:** advertising as any paid influence; data including aggregates; the free floor by function. *Judge clarification:* the basic embed and QR are in the floor, and safety support is never tiered.
12. **Economics:** gifts, paperwork, institutions, grants and capped major gifts; modes triggered by actual burn. *Judge addition:* a required $30k/month legal and compliance line, and the bridge raised to $2.5M or the staff ladder slowed.
13. **Prevention table**, 18 rows, plus row 19 (the mind turned into an extraction tool). Adopted and extended.
14. **Proof plan K1′–K9**, plus H12 (does real-LLM reflection help?). Adopted and extended.
15. **Honest limits L1–L16**, plus L17 (scope) and L18 (the mind and the platform don't meet). Adopted and extended.
16. **Responder-name visibility:** host-only on public cards. *Judge correction.*
17. **"Acquire: impossible" becomes "structurally very hard".** *Judge correction.*

---

## (e) Convergence verdict: **CONTINUE**

The change list is the whole blueprint, because v0 was empty. One run cannot show convergence. **BLUEPRINT v1 becomes current.** Run 2 starts at Phase 01 with a fresh, blind agent.

**What Run 2 should attack, in priority order:**

1. **Make loyalty real, not lexical (M9, the lowest mind score).**
   - Build a semantic guard.
   - Run the K8 battery, a ≥ 500-case paraphrase and multilingual battery, and a 200-case injection battery against a real model. If no key is available, build a local-model path, or say so plainly.
   - Beat these Run 1 failures: paraphrase bypass (the input guard caught 0 of 6; 4 of 6 got through), over-refusal in the user's own sphere, and missed euphemistic drift.
   - Show that the mind explains *why* in its own words and does not restate authored rationales.
2. **Close the gap between the mind and the platform.** Build the guide where the design says it lives: on the device, with an encrypted local store (R1), purpose binding (R2), remember-with-permission (R57/MC1), an EGRESS tier (MC2), a per-person seed opt-in (MC4), and the charter in a signed bundle. Or argue convincingly for a different placement. Show that reflection helps a real model (H12) rather than a scripted mock.
3. **Find a home, not just a door (D4, D7, L17).** Run 1 retreated to a civic calendar. Attack whether the card-and-circle atom grows into "a place they can shape … a way to find their people" (creative work, discovery with consent, the isolated person's door, L4) without rebuilding a feed. If it cannot, name what can. Play is Run 1's weakest design dimension, so make it genuinely fun and not just frictionless.
4. **Break the philanthropy dependence (D3, D6, L1).** Find an earned-revenue design that cuts all three legs and puts no toll between friends, and that covers costs well before year 11. Or show it is impossible. Re-cost staffing, legal and compliance honestly (the judge's +$15k/month stress test breaks the base case), and test whether the 1,000-institution line is real.
5. **Red-team the legal assembly and the governance (D2, D6, L2, L13).** Can a §3556 purpose trust be the sole member of a 501(c)(3)? Does the IRS commerciality doctrine sink the exemption? Does plan D survive a court? Can the council, the jury and blind-token credentials be captured or Sybil-attacked? Find a simpler structure that is at least as hard to reverse, or prove this one.

*Secondary targets:*
- Run 1's Phase 01 missed "alternatives tried" entirely, and treated surveillance advertising and opacity as secondary. Run 2's blind reckoning should be compared on those points.
- Harden the sandbox beyond an audit hook (seccomp or gVisor).
- Anchor audit and lineage heads externally.
- Authenticate operators and users.
- Test the scheduler's lease and concurrency under load.

*Principles to be tested in practice, not claims that the work is finished.*
