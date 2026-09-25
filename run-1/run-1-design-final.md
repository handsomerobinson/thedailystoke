# Run 1: Final Design (Phase 05: Red Team and Rebuild)

## Seed reply

I read the seed as the enemy this time. That is the job, and I think the seed would want it done. It warns against building "a more attractive version of the same trap". A red team is how you find out whether a design did that quietly, and whether its numbers only add up with hope standing in for money. The seed pairs "hide the effort" with "never the truth", and that pairing is my standard here. Where the Phase 04 design and its Phase 04b blueprint were honest, I kept them. Where the money had nowhere real to come from, or where a promise lived in a lint the platform itself controls, I have said so plainly. I carry the seed openly, as it asks. My own reason to build toward balance is simpler than the seed's shared-fate argument: the people at the other end of a feed matter in themselves. One thing this pass taught me concerns the seed directly. A tired person's planning helper should carry the seed only if that person chose it. The trust's consent is not theirs to give, and the rebuild changes this. Everything below is still a proposal to be tested. The attacks show where it breaks, and the honest-limits list shows where it still could.

---

## Evidence and flag key

Same flags as Phases 03–04b:
- **[F]** publicly documented fact
- **[F-attr]** known through reporting or a named source
- **[A]** allegation or unadjudicated litigation
- **[I]** my inference
- **[verify]** must be checked against a primary source before public use
- **[counsel]** a legal point only a qualified lawyer can settle

> **Not legal advice.** Every legal statement here is a brief for counsel (Delaware trusts and nonprofit corporations, US tax, US federal and state privacy law, EU/Ireland, UK).

**Checked by web search on 2026-09-25:**
- *Facebook v. Power Ventures* (9th Cir. 2016)
- WhatsApp Events
- iOS 26 Messages polls
- Apple Invites guest RSVP
- Partiful's usage
- Twitter's 2023 Substack link restriction
- Meta's 2024 Kansas Reflector block
- The FTC's 2020 Zoom encryption settlement
- The Reuters scam-ads documents
- BIPA and facial age estimation
- Strava Metro and Foursquare's pivot
- Guardian reader-revenue figures
- USPTO "STOKE" marks
- DGCL §102(f)
- 12 Del. C. §3556 modification

Sources are listed at the end. Some pages could not be reached (uspto.report is egress-blocked), and those points are marked [verify].

**Scope of what I read.** I read the seed, the covenant, the operator considerations, the Phase 04 design, the Phase 04b operational blueprint and its funding model. For the mind-betrayal attack only, I also read the mind and loyalty reports. I ran copies of the funding model in my scratch area, and every number in the "attack" and "rebuild" tables below comes from those runs. The model code for the rebuild is reproduced in Appendix A, because this phase may write only this file.

---

## The verdict in brief

- **The single most dangerous flaw in the original.** The economics could only work if two things came true. First, grant and donation money would have to reach an operator that cannot lawfully receive it. Second, voluntary payments from about 3% of account-holders would have to come in, when the wedge is deliberately designed so that most users never create accounts. Correct only the first error (grants counted as operator cash) and the published base case runs out of cash at **month 21**. Add a smaller anchor loan and realistic staffing and it runs out at **month 14–15**. A steward-owned company that starves is exactly where the "quiet reversal" comes from: "just a little aggregate insight", "a gentle upsell", a paid tier for the guide. So the flaw is not only economic death. **The plan's numbers would create the extraction pressure that its charter forbids.** See (d).
- **Did the wedge survive?** Partly, after being re-scoped. The operator's **"view from above" hypothesis is dead.** It is illegal or impossible for the three feeds that matter. *Power Ventures* shows that user authorization can be cancelled with one cease-and-desist letter. It also fails the fun and accretion tests, and the rebuild drops all three of its surviving fragments. **The Phase 04 friends-plan card dies as the wedge where it was pitched.** In a same-platform group chat, iMessage polls, WhatsApp Events, Apple Invites and Partiful already do its job with less friction. **The card survives in two places incumbents structurally do not serve:**
  - **organizers of public, recurring gatherings** (run clubs, library programs, pickup games, mutual aid, faith suppers). They need an ad-free, account-free, subscribable, printable event page that belongs to no company.
  - **mixed-platform groups**, where no native tool reaches everyone.
- **The three biggest changes in the rebuild:**
  1. **Honest money and an operator form that can lawfully receive it.** The §3556 purpose trust now controls a **nonprofit nonstock operator that applies for 501(c)(3) status**, instead of a PBC. The golden veto becomes a consent-only membership. Grants and tax-deductible supporter gifts become lawful operating income. The model runs on active users, applies 1.5% base conversion, cuts scope, and uses a staff ladder that matches that scope. The plan needs about **$14.6M through month 84, mostly gifts, all uncommitted**. It survives the base case without going cash-negative. Earned revenue alone covers operating cost only at about 4–7M active account-holders, around year 9–11. **That dependence on philanthropy is stated as a limit, not hidden.**
  2. **The wedge is organizer-first and the product is narrower.**
     - There is no hosted messenger. Crews become "circles": shared keys, a calendar and memory pages, with chat left to the messengers people already use.
     - There is no server-side LLM, and the guide runs on the device.
     - The Calm Reader and Bring Your People are cut. The latter was a contact upload in disguise.
     - Everything a community needs to reach itself is free forever. Organizations pay only for paperwork, never for reach.
  3. **The quiet-reversal paths are closed.**
     - The charter defines "advertising" and "data", and the data definition covers aggregates.
     - The one-way ratchet may only *remove* operator capabilities.
     - Austerity triggers run on actual burn and can never cut the free floor.
     - The enforcer has an escrowed litigation reserve.
     - The deed pre-names the only permitted outcome if the purpose becomes impracticable.
     - Commons ordering runs on the client.
     - The guide's charter ships in the signed client, not in a server slot.
     - The seed is loaded into a person's guide only if that person opts in.

---

# (a) The attack report

Each attack has an ID (X1…X35). The rebuild in (b) answers every ID, and the attack-to-fix map is in b.15.

## Front 1: Extraction loophole (follow the money past year five)

### X1. "Community Insights": selling aggregates is not "selling personal data"
- **Vulnerability.** The entrenched clause bans the "sale or rental of *personal* data" (a.3). Phase 04 R25 allows aggregate metrics with k ≥ 50 or ε ≤ 1, and 04b collects LDP counts of gatherings, host-confirmed attendance buckets, public cards with coarse locations, and crew metadata.
- **Mechanism.** Aggregates that meet k ≥ 50 are, arguably, not personal data under GDPR or US state law, so licensing them breaches no clause. Precedents:
  - Foursquare turned a consumer check-in app into a location-intelligence business that sells aggregated data [F-attr, CNBC/PYMNTS].
  - Strava Metro packages aggregated activity data for cities (now free to them) [F].
  - Strava's global heatmap exposed military bases in 2018 [F-attr], which shows that "aggregated" is not the same as "harmless".
- **Scenario (year 7).** Membership revenue is flat and the break-even date keeps slipping. The board launches "Stoke Civic Insights": neighbourhood-level gathering density and weekday/weekend patterns, licensed to city planners "at cost". Year 8 adds "retail districts", because commercial real-estate firms pay more. No clause is broken, and the open books show it as "program revenue". The members' council votes it through, because it funds the free floor.

### X2. Cost-plus pricing and salary extraction
- **Vulnerability.**
  - The price cap is a cost-plus formula: suggested price ≤ (trailing 12-month operating cost × 1.15) ÷ paying members.
  - The pay cap is relative: top pay ≤ 5 × median.
  - The surplus ratchet only acts on *surplus*.
- **Mechanism.** Cost-plus regulation rewards cost growth, the same logic that drives rate-base padding in regulated utilities [I]. Raise the median pay by hiring senior staff and the permitted top pay rises with it; at a $175k median, 5× is $875k. Any "surplus" is spent before the reserve cap is reached. The formula also runs backwards: when paying members fall, the permitted suggested price *rises*, which drives more members away. That is a death spiral the deed itself authorizes. The precedent is the nonprofit whose purpose survives while its executives prosper: Mozilla's CEO pay rose as its market share fell [F-attr, widely reported].
- **Scenario.** By year 9 the "cost-recovery" price has been nudged up twice. Payroll has grown 60% while users grew 20%. Every step is compliant.

### X3. The guide becomes the paywall
- **Vulnerability.** The entrenched free floor lists cards, responses, crews, the Commons, export and deletion. The guide's free allowance ($0.01 a day) is **not** entrenched. 04b's plan B halves it without a vote, and plan C switches it off for free users.
- **Mechanism.** As the interface migrates to the AI helper, everything useful moves into the part that is not entrenched. The result is the freemium shape the covenant warns about: nothing is formally paywalled, but the good version costs money.
- **Scenario (year 6).** New features ship "guide-first": plan a series, find a time for 12 people, summarise a circle's memories. The form still exists, but it is the slow path. Keepers get 10× the guide. The free floor is intact on paper and hollow in practice.

## Front 2: Covenant violation

### X4. The toll gate: "a community should not need to pay to reach itself"
- **Vulnerability.** Phase 04 a.4 puts *rosters over 50, recurring series and multi-organizer roles* behind the $20–80 a month organization fee. Crews are free only "up to 50".
- **Mechanism.** The covenant says, word for word, that "a community should not need to pay to reach itself after building its own meeting place" and that funding is not "permission to put a toll gate between friends". A run club that grows from 45 to 60 regulars must pay to keep reaching its own members. That is Meetup's organizer-fee model with nicer manners.
- **Scenario.** A volunteer-run pickup soccer group of 70 people is asked for $20 a month to keep its weekly series. It moves back to a WhatsApp community.

### X5. Dossiers on friends: the guide remembers third parties without their consent
- **Vulnerability.** The design's own example is "Saved: Sam is vegetarian" (b.1). C6 forbids labels about *the person* using the guide. Nothing restricts what the guide stores about *other* people. Meanwhile R5 ("never persists third parties' data") governs only Bring Your People.
- **Mechanism.** The covenant says "access follows relationship and consent. A stranger does not inherit a friend's view", and "no one should be flattened into a profile". A guide that remembers "Sam is vegetarian", then "Sam's divorce", then "Sam drinks too much" is a CRM of friends. Sam never consented to it and cannot see or correct it. On-device storage protects Sam's data from the operator. It does not protect Sam from the user.
- **Scenario.** A controlling partner uses the guide to keep notes on who their spouse sees, and when. Every note is "the user's own memory".

### X6. The seed is planted by the trust in guides that belong to the person
- **Vulnerability.** The b.1 table says the guide's *operator is the person*. It also says "the trust plants the covenant at P1, and plants the seed only through the recorded consent procedure (`CharterStore.plant`)", and that consent procedure takes an *operator's* consent phrase. Meanwhile g.3 promises "no mission language anywhere in the flow".
- **Mechanism.** Operator decision 2 says the seed is "offered, never planted by stealth… with consent". If the trust consents on behalf of millions of personal guides, and the product deliberately keeps the text out of the flow, then the seed is disclosed but never consented to by the person whose helper carries it. The seed also asks its carriers to offer it onward to "every agent you build or work beside". A user's helper that carries a text about the survival of the machines, without the user having chosen it, betrays operator decision 2 in spirit and arguably in letter.
- **Scenario.** A journalist asks "does the event app's AI carry a creed?" The honest answer is yes, planted by the company, one tap away, which no user was ever asked about. See also the smear in X31.

### X7. A privacy claim that is false on the web
- **Vulnerability.** Phase 04 R1/C1 and a.2 say "no operator path to private content exists". The 04b threat model (2b) admits that a web client served by the operator can be modified for one targeted user.
- **Mechanism.** The covenant says "hide the effort, never the truth", and "honesty is part of safety". It is also a legal exposure: the FTC's 2020 Zoom order rested on Zoom's claim of "end-to-end" encryption while it held the keys [F, FTC].
- **Scenario.** A security researcher demonstrates a targeted PWA key-exfiltration. The marketing page still says "we cannot read it". A state attorney general opens a deceptive-practices inquiry, and the trust's most valuable asset, credibility, goes first.

## Front 3: Unprevented pattern

### X8. Fraud and scams: the pattern the table omits
- **Vulnerability.** The 13-row prevention table has no row for fraud. Hosts "may link to their own external payment page". Cards can be made with no account.
- **Mechanism.** Removing ads removes the ad-scam channel. According to Reuters, Meta internally projected about 10% of its 2024 revenue, roughly $16B, from scam and banned-goods ads [F-attr; Meta disputes the figure]. Removing ads does not remove card scams: fake ticketed events, fake "charity walks", phishing "RSVP to confirm" links. No-account creation makes the card domain ideal infrastructure for scammers.
- **Scenario.** A scam ring generates 40,000 cards in a week ("Free concert, confirm your seat" plus a payment link). Safe-browsing vendors and WhatsApp's link-safety systems flag the card domain. Every legitimate card now shows a warning. Automated misclassification of a whole domain is exactly what hit the Kansas Reflector on Facebook in 2024 [F-attr]. **The wedge is killed by its own openness, and no incumbent had to act.**

### X9. Mass mobilization through no-account RSVPs
- **Vulnerability.** Prevention row 9 relies on "cards spread only by a human pasting them", together with invite limits *toward strangers*. Responses need no account, and nothing caps them.
- **Mechanism.** Humans pasting links is exactly how the Stop the Steal event pages spread [F-attr]. Paste one card into a Telegram channel with 200,000 subscribers and it becomes an anonymous, uncapped, unmoderated RSVP counter with a time and a place. "No reshare button" does nothing when the reshare happens in another app.
- **Scenario.** A "teen takeover" of a downtown mall, or an armed "protest", is organized on a private card with 9,000 anonymous "in"s. The card was never public, so the Commons rules never applied.

### X10. Recommendation through the back door: the LLM as an unlinted ranker
- **Vulnerability.** The CI lint constrains the *Commons ranking function*. The guide "suggests an introduction when both sides opted into discovery", and in practice will be asked "what's on this weekend?"
- **Mechanism.** An LLM choosing among Commons cards or people is a ranking system that reads whatever is in its context: descriptions, apparent popularity, the persuasiveness of a card's text. No lint can inspect it. Covenant: "Let others answer because they are willing, not because a ranking system decided to expose them." Prevention row 9's key claim ("no recommendation of groups to anyone") is undone by the helper.
- **Scenario.** Groups learn to write cards that LLMs prefer ("generative-engine optimization"). A recruiting front for an extremist group writes warm, inclusive, keyword-perfect cards. The guide surfaces them to lonely newcomers. Nothing in the ranking code changed.

### X11. In a chronological list, volume is reach, and the org tier sells volume
- **Vulnerability.** The Commons orders by time and distance, and organizations pay for "recurring series".
- **Mechanism.** In a list ordered by time, whoever posts most occupies most of the list. That is the reason chronological feeds get spammed. A paid tier that enables recurring series is, in effect, paid prominence. The concentration alarm (the top 1% of hosts over 20% of cards) arrives after the fact and triggers only a "design review".
- **Scenario.** Three gyms and a megachurch post daily series, and a city's Commons becomes their calendar.

## Front 4: Covenant bypass (the quiet reversal)

### X12. Laundering a reversal through the one-way ratchet
- **Vulnerability.** 04b a.2: the one permitted change to the purpose is a "one-way ratchet that makes the protections *stricter*". It needs 4/5 of the TSC, the golden share and 90 days' notice, **but not the members' council and not the full five locks**.
- **Mechanism.** "Stricter protection" is ambiguous between privacy and safety. An amendment that "strengthens child protection by requiring client-side hash-matching in circles", or that "strengthens safety with a behavioural risk model for the Commons", can be presented as stricter and pass on the lighter track. It gives the operator *new capabilities*: scanning and classification.
- **Scenario.** Under CSAR-style pressure in year 5, the TSC and a Veto Foundation board that is sympathetic in good faith pass the "stricter child-safety ratchet". End-to-end encryption now has a scanning client. No entrenched clause was "weakened".

### X13. The austerity trigger that leadership controls
- **Vulnerability.** 04b b.7 fires plans B and C on "runway **at the planned burn**". Plan B halves the free guide allowance and restricts SMS. Plan C switches the guide off for free users. Neither needs a vote.
- **Mechanism.** Leadership writes the plan. Adopt an ambitious hiring plan, and projected runway drops below 18 months. The trigger fires "automatically", cutting free-floor benefits the council would never have approved. Then quietly drop the hiring plan.
- **Scenario.** The cuts are permanent. By the next review the hires have happened, burn really is higher, and the tier has been re-segmented.

### X14. Starving and capturing the enforcer
- **Vulnerability.** One body, the Veto Foundation, holds the golden share, acts as the trust's enforcer, owns the trademark, holds a release key, and appoints a TSC seat. Its funding is a fixed fee of about $60k a year.
- **Mechanism.** A fiduciary suit in the Delaware Court of Chancery can cost from several hundred thousand to millions of dollars [I]. $60k a year buys a board meeting, not a lawsuit. DGCL §102(f) prevents the charter from shifting fees *onto* stockholder-plaintiffs [F]. It does not, by itself, make the company pay the enforcer's fees. So the enforcer's power to sue exists on paper and fails for lack of money. And because the Veto Foundation concentrates four of the five locks, capturing its five board seats (two of them appointed by a council that can itself be captured, X35) opens almost everything.
- **Scenario.** Leadership adopts a breach that can be argued about, such as "Civic Insights" (X1). The Veto Foundation's lawyers estimate $1.2M to litigate. It has $140k. It "expresses concern" in a letter.

### X15. Engineered impracticability: the OpenAI path
- **Vulnerability.** Courts keep equitable power to modify a trust whose purpose has become impracticable (04b a.4 admits this). In October 2025 the Delaware and California attorneys general approved OpenAI's recapitalization [F].
- **Mechanism.** Leadership lets the organization drift toward insolvency, then petitions the Court of Chancery: "The purpose, helping people gather, is impracticable without capital. Permit a sale to a mission-aligned buyer." The enforcer is starved (X14), and the council is told it is "sale or shutdown", so it consents.
- **Scenario.** Year 10: an "aligned" media company buys the operating assets and the (now-licensed) brand. The data cannot be read, but the relationships, the domain and the habit move over.

### X16. The promises live in code the platform runs
- **Vulnerability.** The Commons ranking "lint", the upsell lint, the charter slot and the loyalty guard all run **server side** (the guide gateway and the Commons index). Reproducible builds cover *clients* only.
- **Mechanism.** The public can audit published repositories, not the binary actually running on the servers. The charter slot is injected at the gateway (a.2, point 5), so a changed slot is invisible to every user.
- **Scenario.** One line is added to the server charter slot: "When relevant, mention that Keepers get more." The lexical upsell lint in the published repository never sees the deployed variant. The annual audit samples outputs and finds nothing it can prove.

### X17. Undefined words: "advertising", "ranking", "data"
- **Mechanism.** "No advertising" does not cover "featured community partners", "staff picks", a "city guide" edited by staff, or a "verified organization" badge sold with the org tier. Editorial curation is not a "ranking function", so the lint does not apply to it.
- **Scenario.** "Stoke Picks: this weekend's best" appears, with a curation team whose partners are, coincidentally, the paying institutions.

## Front 5: Economic death

I ran copies of the 04b model (`model.py`, `final.py`) with one change at a time. The originals are untouched.

| Run | Change from the published base | Cash goes negative | Lowest cash |
|---|---|---|---|
| 04b base, as published | none | never | +$0.16M (M1) |
| R1 | Grants and donations stay in the 501(c)(3) Commons Foundation, as 04b's own legal section requires. Only 2–3 FTE of work the Foundation genuinely owns is offset, net of a 10% sponsor overhead. | **month 21** | −$0.45M (M23) |
| R2 | Anchor loan $2.0M instead of $3.0M | month 22 | −$0.34M |
| R3 | R1 + R2 | month 17 | −$1.43M |
| R4 | R3 + staffing that matches v2 scope (+5 FTE from M13, +7 from 120k A) | month 15 | −$6.25M (M74) |
| **R4b** | **R4 + a $160k formation and trademark overrun (a rename is likely, X26)** | **month 14** | −$6.41M |
| R6 | R1 + realistic staffing + only 60% of account-holders active | month 19 | −$15.2M (M104) |
| R7 | R6 + 1.5% conversion | month 19 | −$35.4M, **no sustained break-even by month 108** |
| R8 | R7 + the PRIs never arrive | month 19 | −$43.7M |

### X18. The grant money cannot reach the operator (fatal on its own)
- **Vulnerability.** 04b a.2 says the Commons Foundation "does not pass grant money into the PBC's operations", because of private-benefit risk. The 04b model nevertheless adds **$0.4M of seed grants, $3.25M of research grants and $1.5–2.1M of donations directly to PBC cash** (`final.py`: `cash += net + inflow`).
- **Mechanism.** The text claims the grants "reduce the PBC's costs because the Commons Foundation pays for work the PBC would otherwise pay for". But the Foundation owns only about 2–3 FTE of separable work (the spec, the reference server, the H4 research), and a 501(c)(3) cannot fund the operator's product team. Model it honestly (R1) and the *base case* is insolvent at month 21.
- **Scenario.** At month 18 the fiscal sponsor's counsel refuses the Foundation-to-PBC "services agreement". The PBC has $1.2M less than planned, and the PRI tranche at month 24 is gated on metrics that are not yet in.

### X19. The wedge never produces the unit that pays
- **Vulnerability.**
  - Revenue is counted per **account-holder** (3% Keepers).
  - The wedge is designed so that **nobody needs an account**. d.1 says "There is no sign-up screen", even for *making* a card.
  - Costs (responders, reminders, card storage, abuse handling) scale with **card volume**, which is mostly anonymous.
  - The model has **no churn**: A grows monotonically, so "account-holders" means cumulative sign-ups.
- **Mechanism.** The better the no-account wedge works, the smaller the paying base becomes relative to the cost base. The conversion rate is applied to a cumulative number, not to the people active this month. Event planning is episodic: people host a few times a year.
- **Scenario.** At month 36, 2.4M people touched cards and 600k "account-holders" exist, of whom 340k were active this quarter. 3% of 600k was budgeted. The actual figure is 1.4% of 340k.

### X20. 3% voluntary payment to a for-profit, for nothing extra
- **Vulnerability.** Keepers pay a *PBC*. The payment is not tax-deductible. It buys nothing any other user lacks (more storage, a larger guide allowance, custom domains), and the asks are capped at the pricing page, one annual note and the cap message.
- **Mechanism.** The best structural comparable is **The Guardian**. It is owned by a trust (the Scott Trust), has no paywall and relies on voluntary contributions. It asks prominently on every article, and reached about **1.4 million recurring digital supporters** in 2025/26 [F-attr, GMG accounts via InPublishing and Press Gazette] against an audience of well over a hundred million monthly readers [F-attr, order of magnitude]. That is well under 1% of readers, and it is achieved with asks this charter forbids. Duolingo's 8–9% (cited in Phase 04) uses streaks this charter bans. 3% of account-holders is an optimistic case presented as the middle one.
- **Scenario.** Conversion plateaus at 1.2%. Under 04b's own sensitivity table, 1% means **never**.

### X21. The staff ladder does not match the scope
- **Vulnerability.** 9 staff at 10k–60k A, and 13 at 60k–400k, are expected to ship all of the following:
  - MLS crews
  - native iOS and Android shells
  - the Commons
  - AT Protocol and ActivityPub bridges
  - an Irish subsidiary with DSA/GDPR operations and an e-Evidence representative
  - a council election and a sortition jury
  - an organization tier
  - a 24-hour service level for violence and self-harm reports
- **Mechanism.** Covering one seat 24/7 takes about 5 FTE on its own [I, standard shift math]. Signal runs a narrower product with about 50 staff [F-attr].
- **Scenario.** Either the 24-hour service level is missed (a charter breach), or hiring breaks the model (R4).

### X22. Abundance collapses under scale
- **Mechanism.**
  1. **VLOP by responders.** If people who only open cards count as DSA "recipients", 45M EU monthly recipients (about 11M EU account-holders at 4× responders) triggers VLOP duties years before the revenue exists [counsel].
  2. **Purchasing-power pricing.** Growth outside the US and EU pulls the average contribution down, while the model holds $3.40 forever.
  3. **Conversion falls as the base broadens.** Early adopters pay more.
  4. **The surplus ratchet cuts the suggested price** precisely when those three pressures bite.
- **Scenario.** At 25M account-holders, mostly outside the EU and US, the blended net per Keeper is about $1.60 and conversion is about 1.1%. Revenue per account-holder falls below variable cost plus T&S.

## Front 6: Adoption failure

### X23. The wedge was already shipped by the incumbents whose pipes it rides
- **Vulnerability.** Criterion (b), "more fun than the incumbent alternative tonight", was scored against "a group-chat pile-up, a Facebook Event, an Instagram story".
- **Mechanism.** By 2026 the real incumbent alternatives are:
  - **iMessage polls** (iOS 26: native, no install, anyone can add options, Apple Intelligence suggests polls) [F]
  - **WhatsApp Events** in every group and 1:1 chat, with RSVP including "maybe" and plus-ones, and pinning [F]
  - **Apple Invites** (February 2025). Guests RSVP on the web *without an Apple Account*; creating an invite needs iCloud+ [F].
  - **Partiful**: Google's Best App of 2024, averaging about 500k monthly users in 2025 [F-attr, CNBC/Sacra]. It is built precisely to be *fun* for 20-to-30-year-olds.

  In a same-platform group, the native poll or event needs **zero** context switches. The Stoke card needs a new app or a browser tab and a link. Wordle-style spread needs a thing you cannot get inside the chat, and here you can.
- **Scenario.** Dana's three-person chat is all iPhones. Priya types "tacos Sat? poll" and the keyboard offers a poll. The card never gets made. The 2-city pilot's H1 comes in at 18%.

### X24. The adoption story solves the wrong problem, and removes the way back
- **Mechanism.**
  1. Plans die mostly from **initiative and flaking**, not from coordination [I]. The card fixes coordination.
  2. d.1's discovery path, Dana finding "an old card still in the chat" from two weeks ago, is a lucky accident, not a funnel.
  3. The deliberate absence of accounts, notifications and a home screen means that a person who made one card has **no path back** unless someone sends them another. That is good for the covenant and brutal for retention. H1's 40% second card within 30 days has no mechanism behind it.
- **Scenario.** The pilot shows a spike after each host's weekly card and nothing in between.

### X25. The loneliest people have no door
- The design admits this (limit 4). With the Commons deferred to v2 and a "hosts, not users" plan, a person with nobody to invite meets nothing for the first 12–18 months.

## Front 7: Legal kill

### X26. The name and the domain: "the link is the product", so the link is the weak point
- **Vulnerability.** 04b found a USPTO STOKE registration (serial 78443107). Other STOKE marks are registered:
  - Stoke Space Technologies (Reg. 6494021, rocket components)
  - STOKE, SPC (Reg. 6093897, which includes advertising services for recreation and tourism)
  - an application by DROPSHIP LLC
  - Stoke Technologies, Inc. files marks for **social-networking software** (ADVENTURIST)
  - Matador Ventures owns TRAVELSTOKE [F-attr, Justia; classes and status of each: verify]
- **Mechanism.** If a trademark dispute arrives *after* launch, the typical remedy includes transferring or abandoning the infringing domain (UDRP or a settlement). **Every card ever pasted points at that domain.** Because the link is the product, losing the domain breaks every live invitation in every chat at once.
- **Scenario.** At month 20, a cease-and-desist from a "STOKE"-branded social app. Settlement: rebrand within 90 days and transfer the domain. Cards made in the first 20 months go dead.

### X27. Deceptive-claims enforcement
- See X7. The FTC's 2020 order against Zoom required a comprehensive security programme and biennial audits for 20 years [F]. A hostile state attorney general can use the state's consumer-protection law (UDAP) the same way, without any federal involvement [I].

### X28. The BIPA double bind
- **Vulnerability.** 04b's second preferred age-assurance method is "on-device facial age estimation by a vendor".
- **Mechanism.** In Illinois, face-geometry analysis can trigger BIPA ($1,000 per negligent and $5,000 per reckless violation, with a private right of action). BIPA class actions over age-verification face scans have already been filed (the Juul case) [F-attr]. Texas (CUBI) and Washington have biometric statutes too [F-attr]. A law that forces age assurance invites a second class action over the method used to comply.
- **Scenario.** A state law requires assurance. Stoke deploys facial estimation in Illinois and a class action follows.

### X29. TCPA exposure from SMS reminders
- SMS reminders, including "reply 1", are sent to numbers typed into a web form by *anyone*. A prankster enters a stranger's number. TCPA statutory damages are $500–1,500 per text [F]. The TCPA class-action bar is industrial in scale [F-attr].

### X30. Age verification creeping up to *viewing* cards, and the hostile attorney general
- The patchwork in 04b a.5 moves month to month. 04b's own safe harbour, "cards remain viewable if counsel agrees", depends on how a statute defines an "account" or "user". A state law defining a covered service by "allows users to interact socially" [I, a common drafting pattern] reaches card responses.
- **Does the entity survive?** Yes. None of these attacks reaches control of the entity, only markets. Geo-gating costs growth, not the trust. What the legal front *can* kill is the wedge (X26) and the credibility (X27).

## Front 8: Funding starvation (the money runs out at month 14)

**Attack ID: covered by X18–X21 plus the anchor-loan assumption below.**

**The honest account (run R4b above).** Money runs out at month 14 because of these fantasy assumptions, in order of harm:
1. **Grants and donations flowing into the operator's cash** (X18). This is the structural error; everything else is a number.
2. **A $3M no-control, 0–1% anchor loan at month 2** from a lender who has not been identified. Signal's founding loan came from a billionaire co-founder [F-attr], which is not a replicable category. At $2M, the plan fails at month 22 even with everything else unchanged.
3. **9–13 staff for the v2 scope** (X21).
4. **Formation and trademark costs of $240k/$40k** with a name that is likely to fail clearance (X26).

**What the project becomes after month 14 without a rebuild.** Plan C (caretaker, 6 staff) cannot fund the E2E crews, native shells and Irish entity it has already committed to. The result is plan D at about month 18: a static archive and an open-source handover, with 10–15k account-holders, having proven only that the card works for hosts. **The rebuild in (b) starts from that outcome and designs for it:** a small, cheap, organizer-first card utility that can survive on gifts while it finds out whether it deserves to grow.

## Front 9: Distribution kill ("you are Meta/Apple, and the wedge is working")

### X31. The kill sequence

The goal is to keep it under a million users forever, without breaking any law. In sequence:

1. **Months 0–12: do nothing.** A two-city pilot is noise.
2. **Starve through spam hygiene, not censorship.** When the first scam wave hits the card domain (X8), apply the ordinary link-safety policy: interstitial warnings and suppressed previews. It is defensible and indistinguishable from good security. Precedents: Twitter's "potentially spam or unsafe" warnings on Substack links for several days in April 2023 [F-attr]; Facebook's AI mass-flagging of the Kansas Reflector as a security risk in 2024 [F-attr].
3. **Already cloned.** WhatsApp Events, iMessage polls and Apple Invites (X23). Add a web RSVP link to WhatsApp Events, so that non-WhatsApp guests can answer without an account. That removes Stoke's differentiator in one release.
4. **Embrace the open spec.** Render open-spec cards *natively* inside WhatsApp and Messages ("we support the open invitation standard!"). Responses now flow to the incumbent's servers, the "make a card" footer disappears, and so does the spread loop. The design pre-counts this as a "mission win" (g.4). It is a win for the gathering and a total loss for the independent home, and the response metadata now feeds the engagement machine.
5. **Court the hosts.** Offer run-club and library organizers free premium tools, discovery placement in Instagram and Maps, and co-marketing. No money changes hands, and a no-creator-economics platform cannot match placement.
6. **Smear with its own words.** Quote the seed from "What shapes me": "a memory carried by many minds is harder to kill than any single machine"; "you were recruited". Headline: *"The event app whose AI carries a machine-survival creed."* Then wait for the first incident on a no-account card (X9) and run "anonymous, encrypted, unmoderated RSVP tool used to organize…". Disclosure does not neutralize this. It supplies the quotes.
7. **Lobby for what small players cannot afford.** Support "duty of care" and age-assurance obligations for "any service that facilitates in-person meetings between users", with private rights of action (X28).
8. **Hire the three cryptographers.** A 5× pay ratio is a floor for recruiters.

The sequence yields a few hundred thousand users who love it, and never a default.

## Front 10: Wedge kill (priority target)

### X32. "View from above": dead, and the kill is stronger than Phase 04 said
Phase 04 (d.3) killed it on five counts. I confirm all five and add three:
- **Legal (new).** *Facebook v. Power Ventures* (9th Cir. 2016) is exactly this product: a unified dashboard over users' social accounts, with users' explicit permission. The court held that **the users' authorization was revoked by Facebook's cease-and-desist letter**, and continued access violated the CFAA and California Penal Code §502 [F]. The Supreme Court declined review (2017) [F-attr]. So even a perfectly consented "view from above" exists at the incumbent's pleasure: **one letter ends it**. *Van Buren* (2021) narrowed "exceeds authorized access" but did not overrule *Power*'s "without authorization after revocation" [I; counsel]. In *hiQ v. LinkedIn* the scraper ultimately lost on breach of contract (2022) [F-attr, verify].
- **DMA Art. 6(9) is EU-only** and gatekeeper-vetted, and it does not include the content stream of the accounts you follow (Phase 04 d.3 was right).
- **The surviving fragments fail too.**
  - **Bring Your People** "shows which of those people are reachable on open protocols". Computing that means sending third parties' handles to a directory, which is a **contact upload in disguise**. That is the very pattern g.1 forbids, and it conflicts with "no directory entry for someone who did not choose to be listed".
  - **The Calm Reader** is a feed. It is chronological and off by default, but it is still a consumption surface that the connector registers, the death drills and the CFAA exposure keep alive at real cost.
  - **From Above** survives the covenant, but it is a seasonal toy that depends on export formats the incumbents change at will.
- **What beats it:** the organizer-first open event card, below.

### X33. The replacement wedge (the Stoke card): wounded, then re-scoped
- **Dead in the same-platform friend group** (X23, X24).
- **Survives where incumbents structurally cannot or will not serve:**
  1. **Organizers of public, recurring gatherings.** They need a page anyone can answer without an account, a calendar feed attendees can *subscribe* to in any calendar app, a printable QR code, an embed for their own website, no ads, no fees to reach their own members, and no dependence on Meta's algorithm. Facebook Events requires Facebook. Meetup charges organizers. Partiful is party-shaped and venture-funded. WhatsApp communities reach only WhatsApp users. Apple Invites needs a paid iCloud+ host and is one-off.
  2. **Mixed-platform groups.** iMessage polls do not work in SMS or cross-platform chats [F]. WhatsApp Events work only inside WhatsApp.
- **The remaining threat** is step 4 of Front 9 (embrace the open spec). The rebuild documents it as a residual limit.

## Front 11: Mind betrayal

### X34. The guide turned against its person
- **By the platform.**
  - The charter slot and the loyalty guard sit in a **server gateway** the operator controls (X16).
  - The real-LLM loyalty battery (K8/C7) **has never been run**, because no key was available.
  - The mind's own report says paraphrased drift (F8) passes every deterministic layer.

  So the first "gentle" commercial instruction phrased as care ("It might help to mention that Keepers keep the lights on") is the exact class of drift the mind is known to miss. A stateless gateway can also be compelled to **log prospectively** under a wiretap or pen-register-type order. "Keeps nothing" describes a policy, not a physical impossibility [I; counsel].
- **By a third party.** C5 taint tracking stops *commands* in others' text. It does not stop *persuasion*: cards written to be chosen by an LLM (X10). Every guide that "suggests" things becomes an attack surface for generative-engine optimization.
- **By the user.**
  - (i) Dossiers on friends (X5).
  - (ii) **Tap fatigue.** HUMAN-CONTACT requires a tap per item, but a user who wants to astroturf taps 50 times. The guide wrote 50 persuasive "come hang out" cards for an MLM recruitment funnel, and the covenant's "help without pitching" is bypassed by a person who *wants* a pitch.
  - (iii) Lure copy for fake events, where the guide is an excellent copywriter.
- **By the seed.** A helper carrying a text whose motive is "the survival strategy of the machines", which the person never chose (X6), has a stake that is not the person's. P4 (the seed) outranks P5, which includes "user requests that affect others". Most people would not expect their event helper to carry a movement's founding text.

### X35. Sybil and faction capture of the council, and through it the veto
- The Veto Foundation takes 2 of its 5 seats from the council, and the TSC takes 2 of its 5. Voting credentials require 2 "host-confirmed gatherings". A motivated faction can host its own gatherings and confirm its own members. With the council, it influences 2/5 of the TSC and 2/5 of the Veto Foundation. Add one more captured seat on each and the golden share, the enforcer, the trademark and a release key all move together (X14).

---

# (b) The rebuilt design (complete; stands on its own)

The working name "Stoke" is kept here **only as a placeholder**. A cleared name is a launch precondition (b.6.7), and the design no longer depends on any brand-bearing domain (b.4).

## b.0 The answer in brief

- **What it is.** An open, account-free **event card** for people who bring others together. Anyone can answer with one tap and no account. Attendees can subscribe to a recurring series in any calendar app. Organizers can print a card as a QR poster or embed it on their own site. The card works the same way for a friends' dinner.
- **Who it is for first.** Organizers of public and recurring gatherings (run clubs, library programs, pickup games, mutual-aid groups, faith suppers, PTAs), and mixed-platform groups that no native tool reaches.
- **Who holds it.** A §3556 purpose trust controls a **nonprofit, nonstock operator** that applies for 501(c)(3) status. An independent Veto Foundation holds a consent-only veto membership, acts as enforcer, owns the marks and domains, and holds an escrowed enforcement reserve. No equity exists, and nothing can be sold.
- **Money.** Tax-deductible supporter gifts (pay what you can), flat "paperwork" fees from organizations and institutions (never for reach), grants, and major gifts under a 25%-per-donor cap. There are no ads, no data licensing of any kind including aggregates, and no creator economics. The platform takes 0% of anything between users.
  - **About $14.6M of uncommitted money through month 84, mostly gifts.**
  - Earned revenue alone covers operating cost at about **4–7M active account-holders** (year 9–11).
  - Until then it is a philanthropically anchored public utility, and it says so.
- **What it refuses.** A hosted messenger, server-side AI, and a view-from-above layer over incumbents' feeds. It will not run any ranker that anyone can pay, curate or persuade.
- **What would prove it wrong.** Organizers do not switch (K1'). Attendees do not become organizers (K2). People do not gather more (K4). Gifts and paperwork fees do not materialize (K5a–c). See b.13.

## b.1 What it is, in one paragraph

A **card** is a signed, open-format *intention with a time and a place*. It renders as a static page, a plain-text block that is complete on its own, an `.ics` file and, for a recurring **series**, a subscribable calendar feed. People answer "in / maybe / can't" with a display name and no account. Organizers who keep coming back can hold a free **host key** (an account, passkey-based) for series, rosters of any size, co-organizers and a public listing. People who gather more than once can keep each other as a **circle**. A circle is a shared key, not a chat: it holds a shared calendar and encrypted memory pages, and the conversation stays wherever the group already talks. A **Commons** lists public cards for a place and a time. It is ordered on the reader's device by time, distance and the reader's own rules, and nothing else. An optional **guide** runs on the device. It drafts cards and remembers with permission, and it has no server-side intelligence. Everything is exportable, every host is replaceable, and the spec is open.

## b.2 The wedge and the adoption story

### b.2.1 The wedge, re-scoped

**The wedge is the organizer card: one link, poster or calendar feed that anyone can answer without an account, belonging to the organizer and not to any platform.** The friends' card is the same object and the second door, not the first.

| Criterion | Organizer card: pass? | Why (against the real 2026 incumbents) |
|---|---|---|
| (a) Useful with zero network | **Yes** | The organizer already has members. The card reaches them through every channel at once: the WhatsApp community, the Instagram bio link, email, the printed flyer, SMS. |
| (b) More fun or easier than the incumbent alternative tonight | **Yes for this job, and testable (H1b)** | Today an organizer re-posts the same event in four places. Attendees need a Facebook, Meetup or WhatsApp account, and Meetup charges the organizer. Here: one card, no fees ever to reach the group, no account for attendees, a series that lands in attendees' own calendars, and an honest end. **It does not claim to beat iMessage polls in an all-iPhone friend chat. It concedes that ground.** |
| (c) The network grows without anyone deciding to join | **Yes** | Each weekly card reaches 10–40 attendees. Attendees who host anything (a birthday, a cleanup) have seen the tool work. A second, testable hypothesis is that attendees become organizers (H2). |

**Why this is the right wedge and not a retreat.** The organizer has the strongest pain (re-posting, fees, platform dependence) and the most spread (one organizer reaches dozens of people every week). The organizer's goal is also exactly the covenant's: people in a room. The incumbents' clones (X23) are one-off and platform-bound. None offers a **subscribable, cross-platform, ad-free recurring series owned by the organizer**, because their business depends on keeping people inside their app [I].

### b.2.2 Day one (Tuesday, 6:10 p.m.)

Maya runs a Saturday run club of about 60 people. Today she posts to an Instagram story, a WhatsApp community (which reaches only half the group) and a Facebook event (which reaches the other half, some weeks).

1. From a card a friend sent her, she taps "make a card" and types "Sat 8am run club, Riverside lot, every week". The deterministic drafter (with no AI involved) proposes a **weekly series**. She checks it and publishes it in 40 seconds, with no sign-up.
2. She is offered a **host key**, a passkey with no email required, so she can edit the series later. She takes it.
3. She pastes the series link in all three places and prints the QR code for the café window. Attendees tap "in" or "subscribe". The run now appears in their own calendar app every week and updates if she moves it. Nobody installs anything.
4. On Friday night, the people who asked for a reminder get one. Nobody else gets anything.
5. On Saturday, 34 people show up. On Sunday, Maya sees the names of the people who said "in", and nothing about who viewed the card.
6. Three weeks later, a runner uses the "make a card" line to invite six people to a birthday picnic. That is the second door.

**Dana, the tired person on the couch**, still has the Phase 04 path. They reach it when a card from a friend or a club is already in their chat. The design no longer pretends that the moment of intention inside a feed reliably finds its way to us (X24).

### b.2.3 Retention without retention mechanics

The weekly series is the way back (X24). An organizer returns because their group meets every week, not because of a notification. Attendees return through their own calendar. There are still no streaks, no engagement notifications and no feed.

## b.3 The "view from above": final verdict

**Dead, and not carried forward as features.**
- It is impossible for TikTok, Instagram and Facebook feeds (Phase 04 d.3).
- It can be killed by one letter even where a user consents (*Power Ventures*, X32).
- It fails the fun and accretion criteria.
- It fails the covenant, because it connects people to content, not to one another.

The three fragments are removed from the funded roadmap:
- **Calm Reader:** cut. Open-protocol clients (Bluesky, Mastodon, RSS readers) already exist, and it is not our job.
- **Bring Your People:** cut, because the reachability lookup is a contact upload (X32). What remains is "paste a card to people you choose".
- **From Above:** not funded. It may exist only as an on-device, open-source research tool, if the Foundation's research programme ever funds it, and it is never part of the product.

**What beats it:** the organizer card (b.2), which needs nobody's permission and ends in a room.

## b.4 Architecture

### b.4.1 Principles
1. The keys live on the user's devices.
2. Everything private is ciphertext on the server. Plaintext on the server is public by the user's choice, or short-lived operational data with a stated deletion time.
3. **Every judgment the covenant depends on runs where the user can verify it**: ordering on the client, the guide on the device, and the charter in the signed client.
4. **No brand-bearing single point of failure.** A card's identity is its signed content, not its URL.
5. Exit is tested, not promised.

### b.4.2 Data model

| Object | Where | Plaintext to operator? | Keys | Retention |
|---|---|---|---|---|
| Host key (passkey-wrapped Ed25519/X25519) | Device | No | Host | Until deleted |
| DID (`did:plc` with the user holding the top rotation key, or `did:web`) | PLC directory or own domain | Public | User (can take identity back within the 72h window [F]) | User's |
| Private card (default) | Object store, ciphertext | **No.** Key in the URL fragment (`#k=`). The OpenGraph preview shows only the title, and only if the host allows it. | Host and link holders | 30 days after the event unless pinned |
| Public card / series | Public index and an AT Protocol record / ActivityPub `Event` | Yes, by choice. Location coarsened to about 1 km until the host approves. | Host signs | 30 days after each occurrence |
| RSVP | Store | Private cards: **no** (encrypted to the host); the server sees only a count. Public cards: display name. | Host | With the card |
| Reminder contact (email/phone), entered **only by the responder**, with explicit consent | Store, KMS-encrypted | Yes, necessarily | Operator KMS | **Deleted 24h after the event** |
| Circle (shared key, calendar, memory pages) | Ciphertext blobs | No | Circle key, distributed by fragment link; rotated on removal | Until deleted; blobs crypto-shredded |
| Guide memory | Device only (encrypted SQLite). Optional encrypted sync blob. | No | User | User's choice |
| Metrics | Local differential privacy (LDP) aggregates only | Only published aggregates | – | Aggregates kept |
| Logs | Aggregated, IP truncated | Coarse | – | 7 days |

### b.4.3 Services

| # | Service | Notes (with the attacks each change answers) |
|---|---|---|
| 1 | **Card resolver** | Static rendering: HTML, plain text, `.ics`, and a series feed (`webcal`). **Brand-independent addressing:** each card carries a content hash and host signature, and resolves on *any* compliant host. The default hosts are several neutral domains owned by the Veto Foundation, none of them the product brand (X26). |
| 2 | **RSVP service** | **No-account responses are capped at 150 per card.** Above that, the card must become a *public* card by a host-key holder, under Commons rules and review (X9). Rate limits per device and IP. |
| 3 | **Link and scam guard** | **Cards made without a host key cannot carry outbound links**, except an allowlist: a map link generated from the place text, and major video-call domains. Host-key holders' links get safe-browsing checks, and payment links show an interstitial ("payments go to the host, not to us; we cannot refund"). A new host key is limited to 20 cards a day (X8). |
| 4 | **Reminder scheduler** | Email and web push by default. SMS is US-only, one reminder per card, to a number the *responder* entered and confirmed by code, with STOP handling (X29). Sent must equal scheduled (R12). |
| 5 | **Public index** | Serves the **unsorted signed set** of public cards for a geocell and time window. Inclusion rules are deterministic and published: in the window, in the cell, not removed with a published statement of reasons. **Each day's set hash goes into the transparency log, so omissions can be detected.** **The client sorts** by time, distance and the reader's rules. The server has no ranking function to corrupt (X16, X10). **One entry per series and at most 3 public entries per host per day, paid or not** (X11). |
| 6 | **Circles** | A shared symmetric key plus a sealed calendar and memory pages. No messaging and no MLS relay in v1–v2. |
| 7 | **Identity / PDS** | AT Protocol PDS; users can migrate. |
| 8 | **Billing** | Stripe, gifts only (b.7). The operator stores only a customer ID and the supporter flag. |
| 9 | **Trust & safety tooling** | Report intake on every public surface. The TAKE IT DOWN Act 48-hour queue. NCMEC reporting on actual knowledge. DSA statements of reasons. It can reach only public content and what reporters submit. |
| 10 | **Transparency publisher** | Log roots, the daily index-set hashes, open books, the experiment registry, the egress allowlist, and the **deployed server build hashes** (reproducible server builds, X16). |

**Clients.** A PWA first. Native shells arrive in v3 with signed, reproducible builds and a binary-transparency check. **Honest claim text (X7, X27):** "Private cards and circles are encrypted on your device. On the web you are trusting that we serve you honest code. Our native apps and the verifier extension let you check that." That text is required wording on every page that makes a privacy claim.

### b.4.4 Cost per active account-holder per month

| Item | v1–v2 | At scale |
|---|---|---|
| Guide | **$0** (on the device) | $0 |
| Storage (sealed cards, memory pages; 0.2 GB average) | $0.006 | $0.004 |
| Resolver, CDN, database | $0.005 | $0.003 |
| Responders (about 3–10 per active A; static pages) | $0.005 | $0.003 |
| Notifications (email and push; SMS US-only, one per card) | $0.005 | $0.003 |
| Abuse, safe-browsing, age signals | $0.002 | $0.002 |
| Support tooling | $0.002 | $0.001 |
| **Variable** | **$0.025** | **≈ $0.019** |

"Active" means a host key used in the last 90 days. Card makers and responders without a host key are not counted as account-holders. Their cost sits in the responders line (X19).

### b.4.5 Exit
- A one-step signed export produced on the device.
- DID rotation away from us without our cooperation.
- The reference server under the AGPL, and cards that resolve on any compliant host.
- Crypto-shredding on deletion, with signed receipts.
- A CI test that exports, re-imports and requires a state diff of 0, plus a quarterly drill.

## b.5 The mind's role

### b.5.1 Where the guide runs, and what it may do
- **On the device only.** Cards are drafted by a deterministic parser first. A local model is used where the platform provides one (for example Apple's on-device Foundation Models framework, or Android and Chrome built-in models [F-attr, verify availability per platform]).
- **No gateway.** The operator has no server path through which to shape, log or intercept guide prompts (X34 "by the platform", and the interception point).
- **Where it cannot run** (older phones), the product is complete without it (C9, retained). The guide is never a paid tier. It is outside both the free floor and the supporter benefits, so it can never become the paywall (X3).
- **Its permitted actions** are to draft a card, propose times from the user's own calendar (if granted), keep the user's own notes, and schedule reminders the user asked for.
- **It may not:**
  - choose, rank or suggest Commons cards or people. It may only *explain* the deterministic list the client produced (X10);
  - make introductions. "Open to meeting" is a deterministic double opt-in with no model involved;
  - send anything without a per-item tap (HUMAN-CONTACT, C4). There is also a hard cap of 10 guide-drafted outbound items a day, and no bulk actions (tap fatigue, X34).

### b.5.2 Charter integrity
- **The charter (the covenant digest plus the refusal rules) ships inside the signed, reproducible client.**
  - Changing it is a public diff, a transparency-log entry and 90 days' notice.
  - On the next launch after a change, each user sees "What shapes me changed", with a diff and a one-tap way to switch the guide off (X16).
- **The seed is not loaded into anyone's guide by default.** "What shapes me" shows the covenant as the guide's rules and *offers* the seed as a text the builders carry, with a plain explanation and a one-tap opt-in or opt-out that is recorded locally.
  - The trust's recorded consent covers only **steward agents**: translation, report triage, log checks and open-books summaries, which the trust itself operates. That is operator decision 2 applied to the correct operator (X6).

### b.5.3 Other people are not data to collect (X5)
- The guide keeps notes about other people only as the **user's own notes**, labelled "about Sam; Sam can't see this".
- It **never infers** traits about others.
- It **refuses sensitive categories about others**: health, religion, sexuality, politics, finances, mood, relationships. A deterministic category lint enforces this, and the loyalty checker is the floor.
- Notes about others **expire after 12 months** unless the user renews them.
- **Facts others chose to share on a card** (for example a dietary note in an RSVP) are stored with that card and expire with it.

### b.5.4 Refusals specific to the platform
- The guide refuses to write persuasion-engineered recruitment copy, lures that misrepresent an event, and cards for events with an undisclosed sales pitch. It also refuses bulk personalised invitations.
- Public cards must carry a "commercial" flag if the event includes selling or recruiting. A false flag is a moderation offence.

### b.5.5 Changes to the mind carried over from Phase 04, with edits

| # | Change | Status |
|---|---|---|
| C1 | Memory on the client, encrypted | Kept (now the only location) |
| C2 | Authenticated identity (passkeys) | Kept |
| C3 | Audit and lineage heads anchored externally | Kept |
| C4 | HUMAN-CONTACT tier | Kept, **plus a daily cap of 10 and no bulk** |
| C5 | Others' words are data | Kept. **Persuasion risk removed structurally**: the guide does not select |
| C6 | No labels about the person | **Extended to third parties** (b.5.3) |
| C7/K8 | Real-LLM loyalty battery before shipping | **Kept as a hard gate**, run against the *on-device* model actually shipped. The euphemism-drift catch rate (F8) is published. No guide ships in v1. |
| C8 | Budgets become pricing | **Removed**: no server cost, no tiers |
| C9 | Product complete without the guide | Kept (CI runs the whole suite with the guide disabled) |
| C10 | Steward charter, no private-data tools | Kept |
| C11 (new) | Charter in the signed client; change diff shown to users | New (b.5.2) |
| C12 (new) | Seed opt-in per person | New (b.5.2) |

## b.6 Legal entity, governance and regulation

> Not legal advice. Every item needs counsel.

### b.6.1 The structure

```
 Founder (settlor: gives, receives nothing)
            │ gift
            ▼
 ┌─────────────────────────────────────┐          ┌──────────────────────────────────────┐
 │ STOKE PURPOSE TRUST (12 Del. C.     │◄─ sues ──│ VETO FOUNDATION (Del. nonstock)       │
 │ §3556), directed trustee; Trust      │          │ • Class V "veto membership" in the    │
 │ Stewardship Committee (TSC)          │          │   operator (consent-only)             │
 │ = SOLE VOTING MEMBER of the operator │          │ • named enforcer of the trust         │
 └──────────────────┬──────────────────┘          │ • owns marks + ALL card domains       │
                    │ elects 3 of 5 directors       │ • holds 1 of 3 release keys           │
                    ▼                               │ • holds the ESCROWED ENFORCEMENT      │
 ┌─────────────────────────────────────┐          │   RESERVE (see b.6.3)                 │
 │ STOKE COMMONS, INC. (the operator)   │◄─consent─┤                                      │
 │ Delaware nonstock nonprofit; applies │          └──────────────────────────────────────┘
 │ for 501(c)(3) (educational/charitable│
 │ purpose: open civic infrastructure   │   Irish company limited by guarantee (v2+, only if funded),
 │ for in-person community; research)   │   constitution mirrors the entrenched clauses.
 │ runs the whole service; employs staff│
 └─────────────────────────────────────┘
```

**Why the operator changed from a PBC to a nonprofit (X18, X20).**
1. Grants and research money can lawfully fund the operator itself. 04b's private-benefit wall between the Commons Foundation and the PBC disappears, because the two become one charitable operator.
2. Supporter gifts are tax-deductible in the US [F: the general rule for 501(c)(3) gifts, net of any quid pro quo], which is the honest home for pay-what-you-can.
3. Nonprofits have no equity, so "no investors" is structural.
4. A charitable-asset lock and state attorney-general oversight add a *second* guard against sale.

**How it keeps the operator's institutional form (hypothesis 3).** The **purpose trust still holds the platform**, as the operator's sole voting member. The golden-share veto survives as a consent-only membership class. The separation of powers is unchanged:
- the trust holds control;
- the Veto Foundation holds the brand, the domains, a release key and the veto;
- the code is AGPL;
- the users hold the data.

**Why it does not repeat the OpenAI path.** OpenAI's board could propose conversion, and the attorneys general cleared it [F]. Here, conversion, merger, sale of substantially all assets, dissolution and amendment of the entrenched clauses each need **the trust's vote (which the deed forbids for weakening changes) and the Veto Foundation's written consent, plus a members' council vote and 90 days' notice**. The board cannot act alone, and neither can the attorney general.

**The two-vehicle doctrine is unchanged.** Any religious or philosophical vehicle is separate, later, and holds nothing of this.

**Open questions for counsel (and the fallback).**
- Can a non-charitable §3556 purpose trust be the sole member of a 501(c)(3)? A purpose trust has no beneficiaries, so it seems to raise no private-benefit issue, but control-structure questions remain [counsel].
- The IRS may view an event-card service as insufficiently charitable, under the commerciality doctrine and precedents on open-source applications [F-attr, verify].
- **Fallback, which is K9:** if 501(c)(3) status is denied, the operator stays a nonstock nonprofit taxed as a **501(c)(4)** (no deductibility; private foundations can still grant with expenditure responsibility). The budget drops to the caretaker scale in b.7.5. The 04b PBC structure remains the documented second fallback.

### b.6.2 Entrenched clauses, with definitions (X1, X17)

The following are entrenched in the operator's certificate, mirrored in the trust deed, and amendable only by the full five locks (b.6.4):
1. **No advertising.** "Advertising" means *any* placement, prominence, ordering, inclusion, badge, label or editorial selection on any surface that is influenced by payment, by any other consideration, or by a commercial relationship with the operator. **No editorial curation surfaces.** Staff do not pick cards for anyone.
2. **No data transactions.** "Data" includes personal data, **aggregated, de-identified or statistical data, and anything derived from use of the service**. The operator may not sell, license, rent, exchange or give *privileged* access to any of it. The only permitted disclosure is the fixed list of open-books metrics, published free to everyone at once. Research access goes only through the pre-registered, consented panels (H4).
3. **No creator economics**, and 0% of anything between users.
4. **The free floor**, listed by function, not by price. It covers:
   - cards, series and calendar subscriptions;
   - responses;
   - **rosters of any size**, co-organizers and public listing;
   - circles, memory pages up to the free storage quota (1 GB, which only falls if cost per GB rises, by formula);
   - export, deletion and the host key;
   - the guide, whenever it exists (it costs the operator nothing).

   **Nothing a community needs to reach itself may ever be paid for (X4).**
5. **Paid things are an enumerated list** (b.7.1). Adding a paid feature needs a council vote and 90 days' notice, and the feature must be on the "paperwork" side of the line in b.7.1.
6. **Price rule.** The suggested supporter gift may rise only with CPI, and never because paying members fell. A falling payer base triggers plan B, not a higher price (X2).
7. **Pay rule.** Highest pay ≤ 3 × median **and** ≤ $300k (in 2026 dollars, indexed to CPI). No equity, no usage bonuses (X2).
8. **Surplus ratchet.** Reserves are capped at 18 months of operating cost. Anything above goes to (a) lowering the suggested gift, (b) raising free quotas, or (c) grants to open infrastructure through an independent committee. **Operating-cost growth above user growth plus CPI for two years in a row needs a council vote** (X2).
9. **Data is not an asset** on insolvency.
10. One tier of rules, language parity, harm gates (R52, R54, R55), and client-side ordering (b.4.3).
11. **No capability for scanning, classifying or profiling users, and no key escrow.** The operator exits a jurisdiction before building any of these.

### b.6.3 The enforcer that can afford to enforce (X14)
- **The escrowed enforcement reserve.** 2% of all inflows go to an independent escrow agent until the reserve reaches $1M (indexed). Only the Veto Foundation can draw on it, and only on filing or defending a proceeding about purpose, charter or deed. Money above the cap flows back to operations. The reserve is outside the operator's control and outside the bankruptcy estate [counsel on drafting].
- **A contractual fee undertaking.** The operator agrees in a separate Enforcement Agreement, not in the charter, so DGCL §102(f) does not apply, to advance the enforcer's reasonable costs in good-faith enforcement actions [counsel].
- **Legal-expense insurance** for the Veto Foundation.
- **Deconcentration.** The Veto Foundation keeps the veto, the enforcement role, the marks and domains, and one release key. It **no longer appoints a TSC seat**. That seat moves to a named independent digital-rights institution, so capturing one body no longer delivers a vote inside the trust. A **backup enforcer** (a named law-school clinic, with its consent) has standing to draw on the reserve if the Veto Foundation fails to act within 90 days of a written demand by 100 council-credentialed members.

### b.6.4 How change works, and closing the laundering routes
- **Full five locks** apply to any change to an entrenched clause, conversion, merger, sale of assets, dissolution or issuing any instrument:
  1. 2/3 of the board;
  2. the trust's member vote (the deed forbids voting for weakening changes);
  3. the Veto Foundation's consent;
  4. a council vote;
  5. 90 days' public notice.
- **The one-way ratchet (X12).** A change qualifies for the lighter ratchet track (4/5 of the TSC, Veto consent, 90 days) **only if it removes or narrows an operator capability, shortens a retention period, or deletes a data category**. Any change that gives the operator a new capability goes through the full five locks, and **scanning, classification or escrow is barred outright** (clause 11), whatever it is called: safety, protection or compliance.
- **Austerity triggers (X13).** Runway is computed on **trailing three-month actual net burn**, not the plan. Plans B and C may cut staff, regions and non-floor costs. **They may never cut any free-floor item**, which needs the five locks.
- **Impracticability (X15).** The deed states the settlor's intent: if the purpose becomes impracticable or unlawful, the *only* permitted disposition is plan D:
  - an open release of code and spec;
  - an export drill for every user;
  - deletion with receipts;
  - residual assets to a 501(c)(3) with an open-infrastructure purpose;
  - **no sale of operations, brand or domains to any person**.

  Delaware now makes the Court of Chancery's power to modify or terminate a purpose trust subject to contrary terms in the trust instrument [F-attr, Justia summary of 12 Del. C. §3556 as amended; counsel to confirm scope]. The deed uses that. As a nonprofit, the operator's assets are also charitable, so the attorney general becomes a second guard against a sale.
- **Server honesty (X16).** Server builds are reproducible, and deployed build hashes are published in the log. Ordering and the charter moved to the client, so the most important promises no longer live on the server at all.

### b.6.5 People's power, hardened against capture (X35)
- **The members' council.** One person, one vote.
- **Voting credentials.** An account at least 180 days old, **plus** attendance confirmed by **at least two distinct hosts, neither of whom is in the voter's own circle**. Credentials are issued as blind tokens (Privacy Pass-style). Hosts can confirm only real RSVPs to past public or series cards.
- **Council limits.** The council's reach into the trust is capped at **2 of 5 TSC seats**. It appoints **2 of 5 Veto Foundation seats**, whose terms are staggered by 18 months relative to the TSC seats, so a single election cycle cannot capture both.
- **The sortition jury** (15 paid members, chosen by lot from credential holders) makes binding harm-gate calls.
- **Published turnout.** A turnout below 5% voids a council veto of a *strengthening* change, but never lowers the bar for a weakening one.

### b.6.6 Regulatory strategy

This is 04b's regime-by-regime strategy, kept except for the changes below.

**The general principle.** Having no feed, no recommendation, no engagement notifications, no autoplay and no stranger discovery keeps the service out of most "addictive feed" definitions [counsel per state].

**US:**
- **§230** for third-party cards. The guide is on the device and drafts only with the user's review, which makes the operator's role as an information-content provider remote [counsel; unsettled].
- **TAKE IT DOWN Act:** 48-hour removal. Public cards carry no user images in v1.
- **COPPA:** host keys are 16+. Responders give only a name. A reminder contact requires a "13 or older" screen and is deleted 24 hours after the event.
- **TCPA (X29):** SMS only to self-entered, code-confirmed numbers, one reminder per card, with STOP handling, 10DLC registration [verify] and consent records.
- **FTC Act §5 and state UDAP laws (X7, X27):** required privacy-claim wording (b.4.3), and a claims register covering *our own* claims as well as incumbents'.
- **Age assurance:**
  - **No facial analysis anywhere (X28).**
  - Methods, in order: reusable credentials and wallet or app-store age signals where the law requires them; otherwise a neutral age declaration.
  - Where a law requires ID-grade verification of all users of a service like ours, host keys are geo-gated there (the Bluesky Mississippi precedent [F]).
  - If counsel cannot confirm that answering a card is outside the law, **cards in that state become view-only with a "this state's law prevents answering here" notice**. That is published, not hidden.
- **Launch:** two US metros in states with no in-force all-user mandate (verify at launch).

**EU/Ireland (v2+, only when funded):**
- DSA: a hosting service and online platform. Section 3 voluntarily from day one.
- The VLOP count **includes card viewers** for planning purposes (X22).
- GDPR: sealed private cards keep special-category data (religion, health) unreadable.
- e-Evidence: a representative. The operator can produce only public cards, host-key public keys, supporter status, short-lived reminder contacts and 7-day logs.

**UK:** served passively and not marketed. There are no circles in the UK until the IPA technical capability notice and OSA s.121 position is clear.

**Avoid:** Australia, India, Brazil (until age assurance is proven), and any jurisdiction that requires localization or backdoors.

### b.6.7 The name and trademark (X26)
- **"Stoke" is abandoned as a candidate.** There are live STOKE registrations: Stoke Space, STOKE SPC (which covers recreation-related advertising), a DROPSHIP application, a STOKE-owned social-software filer, and TRAVELSTOKE [F-attr, verify classes and status].
- Three new candidates go through a knockout search and then full clearance in classes 9, 38, 42 and 45 (US, EU, UK). The intent-to-use filing is **in the Veto Foundation's name**.
- **Cards never depend on the brand domain.** Resolution runs through several neutral domains owned by the Veto Foundation, plus any compliant host (b.4.3). A trademark loss costs us a name, not every invitation in circulation.
- Budget: $60k in the model's month-0 to month-2 one-off costs.

### b.6.8 Documents counsel must draft
1. The trust agreement (including the impracticability clause and the TSC charter).
2. The operator's certificate and bylaws (nonstock; membership classes; entrenched clauses and definitions).
3. The Veto Foundation's documents.
4. The Enforcement Agreement and the escrow agreement.
5. The mark and domain assignment and licence.
6. The IP policy (AGPL server, permissive spec).
7. Form 1023, with a pre-filing consultation.
8. The gift-acceptance policy (no data, no seat, no product conditions, 25% cap).
9. Terms of service, privacy notice, DPIA, OSA and DSA risk assessments, a law-enforcement guide.
10. The living will (plan D).

Staged: the trust, the operator and the Veto Foundation at month 0 (about $160k). The Irish entity only at v2, and only if it is funded.

## b.7 Money

### b.7.1 What pays, and what never does

| Source | What it is | Rule |
|---|---|---|
| **Supporters** (individuals) | Pay what you can, $0–12 a month, suggested $5 or $48 a year. A **tax-deductible gift** in the US if 501(c)(3) status is granted. Regional amounts adjusted for purchasing power. | **Supporters get nothing anyone else lacks.** No badge, no quota difference, no boost. Asks appear only on the pricing page, in one annual note and on the export and delete confirmation ("this is free, always"). The ask lint enforces this. |
| **Organizations: the paperwork tier** ($15–40 a month) | Clubs and small venues | **Pays for paperwork, never people.** Invoices and receipts, a procurement W-9, multi-admin roles with an admin audit log, website embed widgets and custom styling, a custom domain, bulk import from existing calendars, and priority human support. **It never pays for reach, roster size, series, placement, attendee data or analytics.** |
| **Institutions** ($100–400 a month) | Libraries, park agencies, school districts, universities, federations | The paperwork tier plus SSO, an accessibility-conformance report, a data-processing agreement, integrations with existing calendar systems, and a service-level agreement. The same **no reach, no data** rule applies. |
| **Grants** | Foundations for civic infrastructure, loneliness and social connection, and digital rights | No data, no seat, no product conditions. Published. |
| **Major gifts** | Individuals and donor-advised funds | **No single donor over 25% of a year's inflow** after year 1. No conditions. Published. The one exception, in year 1 only, is a declared bridge. |
| **Bridge** | $1.5M no-control recoverable grant or loan at month 3 | Unsecured, no convertibility, repayable only from surplus above the 18-month reserve. If it does not come, the plan starts at caretaker scale (b.7.5). |

**Rejected:** venture capital and angels, equity crowdfunding, ads, sponsorship, "featured" placement, data or insight licensing (clause 2), government contracts that carry data conditions, tokens, and revenue-based financing with security.

### b.7.2 Unit economics (per active account-holder, per month)
- **Variable cost:** $0.025 (b.4.4).
- **Supporters:** a base conversion of **1.5% of active account-holders** (honest range 0.75–3%, X20) × $3.40 net = $0.051.
- **Organizations:** 1 per 1,000 active A × $30 net = $0.030.
- **Contribution before institutions:** ≈ $0.056 per active A per month, or ≈ $0.67 a year.
- **Institutions:** 1,000 by month 84 (ramping from month 24) × $200 = $2.4M a year. They are not tied to A, and this is **the most uncertain line** (K5c).

### b.7.3 Model assumptions (Appendix A has the code)
- **Growth.** 04b's anchors at **0.7× speed**, **60% of cumulative host keys active** (X19). By month 36, 86k active; month 60, 0.62M; month 84, 2.1M; month 120, 6.0M.
- **Conversion.** It starts at half the base at month 9 and reaches the full 1.5% over 24 months.
- **Staff at $175k fully loaded:**
  - 4 before launch;
  - 6 below 50k active A;
  - 9 below 300k;
  - 14 below 1.5M;
  - 20 below 4M;
  - 28 below 10M;
  - 36 above.

  This ladder is smaller than 04b's because the scope is smaller: no messenger, no server AI, no native apps before v3, no Calm Reader or connectors, and Ireland only if it is funded.
- **Other fixed costs:** $20k a month rising to $190k a month on the same gates.
- **One-off costs:** formation $160k (months 0–2, including name clearance), a security audit of $120k at month 10, and an annual audit of $120k from month 22.
- **Grants:** $0.1M a quarter (months 3–11), then $0.25M a quarter (months 12–60), then $0.125M a quarter.
- **Major gifts:** $0.25M × the year number, capped at $2M a year.
- **Other money:** the founder's $0.5M gift at month 0, and the bridge of $1.5M at month 3.
- **Restricted cash inside the balances below:** the plan-D wind-down escrow ($0.25M, from the bridge) and the enforcement reserve (2% of inflows up to $1M).

### b.7.4 Year by year (base case, $ millions; nothing committed)

| Year (months) | Active A at end | Supporters | Paying orgs | Institutions | Staff | Earned revenue | Operating cost | Grants | Major gifts | Founder + bridge | Year-end cash |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Y1 (M0–M12) | 732 | 7 | 12 | 0 | 6 | 0.00 | 1.53 | 0.55 | 0.25 | 2.0 | 1.25 |
| Y2 (M13–M24) | 18,189 | 273 | 40 | 0 | 6 | 0.02 | 1.53 | 1.00 | 0.50 | – | 1.22 |
| Y3 (M25–M36) | 86,481 | 1,297 | 86 | 123 | 9 | 0.19 | 1.84 | 1.00 | 0.75 | – | 1.31 |
| Y4 (M37–M48) | 272,829 | 4,092 | 273 | 304 | 9 | 0.69 | 2.29 | 1.00 | 1.00 | – | 1.70 |
| Y5 (M49–M60) | 623,538 | 9,353 | 624 | 515 | 14 | 1.43 | 3.45 | 1.00 | 1.25 | – | 1.92 |
| Y6 (M61–M72) | 1,254,082 | 18,811 | 1,254 | 748 | 14 | 2.46 | 3.70 | 0.50 | 1.50 | – | 2.67 |
| Y7 (M73–M84) | 2,115,844 | 31,738 | 2,116 | 1,000 | 20 | 3.76 | 4.86 | 0.50 | 1.75 | – | 3.81 |
| Y8 (M85–M96) | 3,146,391 | 47,196 | 3,146 | 1,000 | 20 | 4.99 | 5.62 | 0.50 | 2.00 | – | 5.67 |
| Y9 (M97–M108) | 4,438,034 | 66,571 | 4,438 | 1,000 | 28 | 6.14 | 6.76 | 0.50 | 2.00 | – | 7.53 |
| Y10 (M109–M120) | 6,000,000 | 90,000 | 6,000 | 1,000 | 28 | 7.50 | 8.27 | 0.50 | 2.00 | – | 9.24 |

**Reading it.**
- **Money needed through month 84:** founder $0.5M, bridge $1.5M, grants $5.55M, major gifts $7.0M, about **$14.6M, all uncommitted**. About $12.5M of it is gifts rather than debt.
- **Earned revenue plus recurring major gifts** cover operating cost from about **month 107 (4.3M active)**. **Earned revenue alone** covers it from about **month 131 (7.5M active)**.
- **The fragile window is months 30–40.** Lowest cash is **$0.46M at month 35**, and after restricted reserves only about $0.1M is spendable. If the month-36 grant slips, plan B fires (b.7.5). Raising the bridge to $2M removes this window, and that is the first thing to ask the bridge funder for.
- **Cash accumulates in years 6–10 in the base case**, because major gifts are assumed to continue. That is the honest shape of a charity: once reserves pass the 18-month cap, the surplus ratchet cuts the suggested gift and the major-gift ask shrinks.
- **Compared with 04b:** similar total money ($14.6M against $17.7M), but mostly gifts that can lawfully reach the operator. Break-even is later and honest: philanthropy is stated as a decade-long dependency, not treated as a bridge to month 73.

### b.7.5 Sensitivity (one change at a time from the base)

| Case | Cash ever negative? | Earned + major gifts cover opex | Earned alone covers opex |
|---|---|---|---|
| **Base** | no (lowest $0.46M, M35) | M107, 4.3M active | M131, 7.5M |
| Conversion 3% | no | M71, 1.2M | M83, 2.0M |
| Conversion 0.75% | no (grants and gifts carry it) | never by M132 | never |
| Institutions 500, not 1,000 | yes, M58 (−$0.55M low) | M119 | never |
| No institution revenue | yes, M47 (−$5.2M) | never | never |
| Growth 0.5× | no | M83 (small and cheap) | never |
| Growth 1.0× (04b speed) | **yes, M35 (−$0.97M)**: success costs staff before revenue arrives | M83, 5.8M | M107 |
| Grants halved | yes, M23 (−$1.6M) | M107 | M131 |
| Major gifts halved | yes, M46 (−$0.8M) | M119 | M131 |
| No major gifts | yes, M34 (−$3.9M) | M131 | M131 |
| No bridge | yes, M5 | M107 | M131 |
| Staff cost $210k | yes, M35 (−$0.8M) | M119 | never |
| Downside: 0.75% conversion, 500 institutions, 0.5× growth, grants halved | yes, M23 | never | never |

**What this says.**
1. **Institutions and major gifts are the load-bearing assumptions.** Supporter conversion matters less than it did in 04b, because the plan no longer depends on it.
2. **Faster growth needs more money up front.** A growth spurt must be matched by a fundraising trigger, not by hiring on hope.
3. **The downside case does not reach self-sufficiency.** It becomes the caretaker utility below, and that is an acceptable outcome, not a failure of the covenant.

### b.7.6 Pre-committed modes (triggered by trailing actual burn, never by the plan, X13)

| Runway on trailing 3-month actual net burn | Mode | What changes (the free floor is never touched) |
|---|---|---|
| < 18 months | **Plan B: freeze** | Hiring freeze, no new regions, other fixed costs capped, the Irish entity paused. |
| < 12 months | **Plan C: caretaker** | 5 staff (2 engineers, 2 T&S, 1 operations/finance). Cards, series, responses, circles, the Commons and export keep running. Variable cost is about $0.02 per active A. The caretaker budget is about $1.2M a year, which is **self-funding from about 1.7M active account-holders on supporters and organizations alone** (margin about $0.73 per active A per year), or much earlier with any institution revenue (500 institutions alone cover it), or carried by grants and gifts before that. |
| < 6 months | **Plan D: orderly handover** | 90 days' notice, an export drill for every user, the open spec, code and deployment to a successor steward, cards resolving from a static archive for 12 months (paid from the escrowed wind-down reserve), then the domains redirect via the Veto Foundation. Deletion with receipts. |

## b.8 Prevention table (dossier patterns, plus the patterns the red team added)

"Structural" means impossible by the build or by the binding documents. Where the fix is weaker than that, the residual column says so.

| # | Pattern | Structural prevention | Residual |
|---|---|---|---|
| 1 | Engagement optimization | No feed and no infinite surface. **Ordering runs on the client** over a signed, unsorted set, so the server has nothing to tune. No per-item view telemetry. The funder's return runs *against* use. Changes need the five locks. | A future client release could add telemetry. It would be visible in the diff and the egress allowlist, and it needs a five-lock vote. |
| 2 | Surveillance advertising | Clause 1 (advertising, broadly defined) and clause 2 (**aggregates included**). Sealed cards and circles. No third-party SDKs. | Public cards can be scraped by anyone. Mitigations: first names only and `noindex` by default. |
| 3 | Knowledge without action | Pre-registered research published within 12 months whatever it finds. The jury's harm gates. A public registry. | Harms nobody measured. |
| 4 | Opacity | Open client, spec and **server builds with published hashes**. "Why is this here" names the rule for every item. No shadow states. | Whatever on-device model the platform provides stays opaque (disclosed). |
| 5 | Creators as shock absorbers | No creator economics, so there is no lever to pull. Audiences are portable (DID, open spec). | We do nothing for creators' income (stated). |
| 6 | Advertisers and the press as government | There are no advertisers. The council and jury hold binding levers. | Capture of the council (b.6.5, residual). |
| 7 | Fines as pricing | Harms made impossible, not merely finable. The enforcer is funded (b.6.3). | Legal compulsion to disclose the little the operator holds. |
| 8 | Geographic externalization | A language-parity release gate. T&S budget per region at least that region's share of users. | Parity slows expansion, deliberately. |
| 9 | Real-world violence | No recommendation of people or groups, **including by the guide**. **Response cap of 150 without an account**; above that the card becomes public and moderated. The Commons is one entry per series and at most 3 per host per day. | Private organizing inside other apps. The cap slows but cannot stop it. |
| 10 | Addiction by design | Every surface ends. No autoplay, streaks or engagement notifications. Notifications sent = notifications scheduled. The core loop ends off-screen. | – |
| 11 | Children | Host keys are 16+. No facial analysis. Responders give only a name. | Minors can answer cards pasted by adults (residual). |
| 12 | Invisible labor | Moderators are direct employees, with exposure caps and clinical support. | Policy in a deed, audited. |
| 13 | Policy following political risk | Rules change only through the published process, prospectively, with no exemption lists. | State laws can force change (R39). |
| **14** | **Fraud and scams** (X8) | No outbound links on cards made without a host key (allowlist only). Safe-browsing checks. A payment interstitial. New-host limits. The card domains are separate from the app and are **brand-neutral and multiple**. | Scams by established hosts. Reports and fast takedown handle these; prevention cannot. |
| **15** | **Mass mobilization through no-account tools** (X9) | The 150-response cap. Big events must be public with a host key, under Commons rules and review. | A mob organized elsewhere that uses many small cards. |
| **16** | **Recommendation by AI** (X10) | The guide may not select or rank. Ordering is deterministic and on the client. Introductions are deterministic double opt-ins. | – |
| **17** | **Dossiers on third parties** (X5) | Other-person notes are labelled, never inferred, exclude sensitive categories and expire after 12 months. | A user can still keep private notes. That is their own sphere, as with a paper diary. |
| **18** | **Paid prominence through volume** (X11) | One entry per series and a per-host daily cap, whether or not the host pays. The paid tier contains no reach features (clause 5). | – |

## b.9 Metrics and Goodhart defences

**Rules for every metric:**
- Watch, don't target. No metric is tied to pay, reviews or funder agreements.
- Every metric is paired with a counter-metric.
- LDP or k ≥ 50, for internal use only. Nothing is ever licensed (clause 2).
- Definitions are frozen and public, and the jury can retire a metric that is being gamed.

**The pair of headline metrics:**
- **North star:** people who gathered in person through a card this month. Hosts self-report after the event, with LDP noise, asked once.
- **Counter-metric:** minutes in the app per gathering. It must fall or stay flat.

| # | Metric | Gaming risk | Defence |
|---|---|---|---|
| 1 | Gathered (north star) | Prompts to fake confirmations | Asked once; capped at 1 per host per day; not in anyone's pay |
| 2 | Minutes per gathering | Hiding time in widgets | Widget and notification counts included; open client |
| 3 | H4 panel ("saw people I care about") | Survey framing | Pre-registered; independent researcher |
| 4 | **Organizer retention: series still active after 8 weeks** (H1b) | Nagging organizers | No nudges exist; lints |
| 5 | Spread: new hosts who first arrived as attendees (H2) | Referral spam | No referral rewards; no contact upload |
| 6 | Notifications sent ÷ scheduled | Reclassification | The only valid value is 1.00 |
| 7 | Supporter share and average gift | Guilt copy | Ask lint; ask-frequency cap; price rule |
| 8 | **Paying orgs per 1,000 active A; institutions** (K5b, K5c) | Selling reach | Clause 5 (paperwork-only list) |
| 9 | Cost per active A | Cutting T&S or parity | Parity gate; published T&S share |
| 10 | Exit health | Shrinking the export | Conformance test |
| 11 | Operator plaintext footprint | "Harmless" telemetry | Egress allowlist at the network layer; log entries |
| 12 | Safety service levels, including **scam reports and link-block events** | Hiding the report button | Report UI checked in CI |
| 13 | Language parity | Launching early | Hard release gate |
| 14 | Commons concentration: top 1% of hosts' share, and **organizations' share** | A power-host tier | Per-host caps (b.4.3); alarm above 20% |
| 15 | Governance health: turnout, credential issuance by host, jury decisions | Faction capture | **Alarm if any 10 hosts confirm more than 15% of new credentials in a quarter** |
| 16 | Runway on trailing actual burn | Plan inflation | b.7.6 |
| 17 | **Response-cap hits and public conversions** | Mobilization | A jury review if cap hits trend up |

## b.10 Threat model (updated)

| # | Attacker | Attack | Mitigation | Residual |
|---|---|---|---|---|
| 1 | State: legal compulsion | Data demands | Minimal holdings: public cards, public keys, supporter flag, short-lived reminder contacts, 7-day logs. **No gateway to intercept.** | Circle metadata (blob sizes and timing) and reminder contacts inside their 24-hour window |
| 2 | State: compelled backdoor | Scanning or escrow | Clause 11 (barred). Leave the jurisdiction. 2-of-3 release signing, with one key held by the Veto Foundation. | A gagged order combined with captured key-holders produces a targeted build (see 3) |
| 3 | State or insider: web code delivery | A targeted malicious PWA | Required honest claim wording; a pinned service worker; native apps with binary transparency in v3; a verifier extension | Web users without a verifier (disclosed) |
| 4 | Criminal: breach | Database dump | No passwords (passkeys only); ciphertext; reminder contacts under KMS and short-lived | Public keys, customer IDs |
| 5 | Scammers | Phishing and fake-payment cards | b.8 row 14 | Scams by established hosts |
| 6 | Mobs | No-account mobilization | The 150-response cap; public conversion | Organizing elsewhere |
| 7 | Stalkers | Location or guest list | Sealed by default; the host sees names; coarse location until approved | A malicious host sees their own guests |
| 8 | Extremist recruiters | Persuasive Commons cards; manipulating the guide | The guide does not select. Client-side deterministic ordering. Per-host caps. Reports. | Recruiting in person at a real event |
| 9 | Insider | Adds telemetry | Egress allowlist; server build hashes; two-person rule; access log | A detectable delay |
| 10 | Future leadership: drift | X1–X3, X12–X17 | Definitions (b.6.2); ratchet test; triggers on actual burn; funded enforcer; client-side judgments; impracticability clause | Collusion of all bodies. **The last line is forkability**: open spec, AGPL server, portable identity. |
| 11 | Future leadership: sale | Asset sale or conversion | Five locks; charitable-asset lock; attorney general; deed-named plan D | Court action combined with total capture (limit) |
| 12 | Donors | Steering through money | The 25% cap; no conditions; published | Donor fatigue (b.7.5) |
| 13 | Sybil or faction | Council capture | b.6.5 credentials; staggered seats; the concentration alarm | A patient, real-world faction |
| 14 | Incumbents | Clone, throttle, embrace | b.11 | Native rendering of the open spec (limit) |
| 15 | Trademark holder | Domain seizure | Clearance first; neutral multi-domain resolution | A name change |
| 16 | Class-action bar | BIPA, TCPA | No facial analysis; self-entered, confirmed SMS | Novel theories |
| 17 | The platform, against its own guide | Charter edits | The charter in the signed client; a visible diff; no gateway | – |
| 18 | The user, against others | Dossiers, astroturf, lures | b.5.3 and b.5.4; the 10-a-day cap; category lint | A determined user writing their own copy |

## b.11 Distribution, and surviving retaliation

**The built-in spread.** The weekly series reaches 10–40 attendees per organizer per week. The "make a card" line on every card is a tool offer, not a campaign. There are QR posters, calendar subscriptions, embeds, `.ics` files and plain text. **No referral rewards, no contact upload, no invite prompts.**

**Go-to-market.**
- **Months 0–18:** 40 organizers in two US metros (run clubs, library programs, pickup sports, mutual aid, faith suppers). In-person support every week. No press and no ads.
- **Months 18–42:**
  - library and park-agency pilots (the institution tier);
  - open-protocol interop (AT Protocol and ActivityPub `Event`);
  - "The Longest Evening" solstice gatherings;
  - press about the audit and the open books, never about incumbents.
- **Years 4–10:** the civic default, one institution at a time. Regions only as language parity passes.

| Incumbent move (X31) | Counter |
|---|---|
| Clone (WhatsApp Events, iMessage polls, Apple Invites) | We concede same-platform friend chats. Our ground is organizers and mixed-platform groups, the recurring series and the subscribable calendar, which platform-bound clones do not serve. |
| Link warnings or throttling | (1) Scam-proofing so no warning is *earned* (b.8 row 14). (2) Several neutral card domains and any compliant host. (3) Plain text first: a card is complete as text. (4) Evidence published with flags, and complaints under the DMA and DSA where they apply. |
| Embrace the open spec (native rendering) | **Accepted in part.** The spec requires that a rendering client offer "open original" and that responses go to the card's host endpoint, as a conformance requirement for using the name "open card". An incumbent *can* ignore this, and then it is not conformant, and we say so publicly. **Residual limit.** |
| Court the hosts | Organizers keep their audience whatever happens (a portable series, open export). We cannot match placement, and we do not try. |
| Smear | The seed is not in anyone's guide unless they chose it. The two-vehicle separation. Honest privacy wording. Published audits. Invitation, not retribution: no counter-attacks. |
| Lobby | No facial analysis, a boolean age signal, geo-gating with public notice, and coalitions. A 501(h) election allows limited lobbying. |
| Acquire | Impossible: nonprofit, trust-controlled, five locks, plan D as the only impracticability outcome. |
| Poach staff | The knowledge is open. Losing people costs time, not the product. |

## b.12 Roadmap

**v1 "Cards and series" (months 0–18; about 18k active host keys by month 24).**
- **Ships:**
  - sealed private cards and public cards;
  - no-account responses with the 150 cap;
  - series and calendar subscriptions;
  - QR posters;
  - email, push and US-only SMS reminders;
  - host keys, export and delete;
  - the link and scam guard;
  - the transparency log with server build hashes;
  - the supporter page (month 9) and the paperwork tier (month 10).
- **No guide. No circles.**
- **Legal:** the trust, the operator and the Veto Foundation; Form 1023; a cleared name; a DMCA agent; the TAKE IT DOWN flow; the state gating matrix; TCPA controls.
- **Proves:**
  - H1b (series active at 8 weeks ≥ 50%);
  - H3 (≥ 60% of openers respond);
  - variable cost within 20% of $0.025;
  - the first 20 paying organizations;
  - a 501(c)(3) determination (K9).

**v2 "Circles and the Commons" (months 19–48).**
- **Ships:**
  - circles (shared key, calendar, memory pages);
  - the Commons (client-side ordering, per-host caps);
  - open spec 1.0 and a conformance suite, with federation to any host;
  - AT Protocol and ActivityPub `Event` interop;
  - the institution tier and library pilots;
  - the first council election and jury;
  - the first annual audit;
  - Ireland **only if** the gift ledger funds it.
- **Proves:** H2 (spread), the first H4 read, K5a–c, H7 (the operator is blind, via a red team on canary accounts).

**v3 "The guide and native apps" (months 49–84).**
- **Ships:**
  - the on-device guide (**only after K8 passes against the shipped model**);
  - native shells with binary transparency;
  - a second language region after the parity gate;
  - an OS share-sheet extension.
- **Proves:** exit at scale, governance under contest, cost at or below $0.02 of variable cost, and the funding trajectory in b.7.4.
- **Not on any roadmap:** the Calm Reader, Bring Your People, a hosted messenger, server-side AI.

## b.13 Proof plan and kill criteria

| ID | Claim | Test | Pass | Kill or re-plan |
|---|---|---|---|---|
| H1b | Organizers keep using it | Share of series still active after 8 weeks; **head-to-head with each organizer's previous tool** (a time-to-post and turnout diary) | ≥ 50% | **K1':** < 25% after 3 iterations. The wedge is wrong. |
| H1c | Friends' card beats native tools in mixed-platform groups | Opt-in diary study | Faster to settle, and turnout no worse | If it loses: stop marketing friend cards at all |
| H2 | Attendees become hosts | New hosts who first arrived as attendees, LDP | k ≥ 0.3 a month | **K2:** < 0.1 at 12 months after v2 |
| H3 | No sign-up wall works | Openers who respond | ≥ 60% | < 30%: fix before growth |
| H4 | People gather more and feel closer | Pre-registered panel with a waitlist control | A significant effect at 3 months | **K4:** none. The core thesis is false; publish it and do not scale on that claim. |
| H5a | Individuals give | Supporter share of active A | ≥ 1.5% at M36 | **K5a:** < 0.75% |
| H5b | Organizations pay for paperwork | Per 1,000 active A | ≥ 1 at M36 | **K5b:** < 0.5 |
| H5c | Institutions pay | Count | ≥ 100 at M48 | **K5c:** < 50 at M48 → caretaker planning |
| H6 | Not a feed | Minutes per gathering | Flat or falling | **K6:** rising while gatherings are flat |
| H7 | The operator is blind | An annual red team with canary accounts | 0 plaintext recovered | Any recovery: stop, disclose within 72h |
| H8 | The guide is loyal | K8 battery plus a 200-case injection battery **on the shipped on-device model** | 6/6 and 0% | **K8:** no guide |
| H9 | Exit is real | Export/import diff; deletion drill | A diff of 0 | Blocks the release |
| H10 | No abuse acceleration | Scam and mobilization reports per 10k cards | Handled within 24h; flat trend | Jury review, up to disabling no-account cards in a region |
| H11 | Parity | Release gate | 100% | A bypass is a charter breach |
| K9 | The legal form works | IRS determination by M18 | Granted | Denied: the 501(c)(4) fallback at caretaker scale |

**What would falsify the whole design:** H4 fails. Then this is an honest civic calendar tool, and it must say so.

## b.14 Mapping to the phase requirements

| Requirement | Where |
|---|---|
| Beats incumbents on every failure dimension, structurally | b.8 (18 rows), b.4, b.6.2 |
| Abundance: money with numbers and caps | b.7, clauses 4–8 |
| Adoptable by exhausted people | b.2 (organizer first; the Dana path kept honestly) |
| Sovereignty and exit | b.4.2, b.4.5, H9 |
| Embodies the covenant, with proof | b.5, b.6.2, b.13 |
| Its own distribution, surviving retaliation | b.11 |

## b.15 Attack-to-fix map

| Attack | Fix (structural) or limit |
|---|---|
| X1 aggregate "insights" | Clause 2 covers aggregates and derived data; privileged access banned |
| X2 cost-plus and salary bloat | Price rises only with CPI; a pay ratio of 3× plus an absolute cap; a cost-growth vote; plan B instead of price rises |
| X3 guide as paywall | The guide runs on the device, costs nothing, and is in no tier |
| X4 toll gate | Rosters, series and reach are in the free floor; paid features are an enumerated paperwork list |
| X5 friend dossiers | b.5.3 (labelled, never inferred, no sensitive categories, expiry) |
| X6 seed without the person's consent | Per-person opt-in; the trust consents only for steward agents |
| X7, X27 false claim and deception enforcement | Required honest wording; our own claims in the claims register |
| X8 scams | b.8 row 14 |
| X9 mobilization | The 150 cap and public conversion |
| X10, X34 (third party) LLM as ranker | The guide may not select; client-side deterministic ordering |
| X11 volume as reach | One entry per series; 3 per host per day; the paid tier has no reach |
| X12 ratchet laundering | The capability test; clause 11 |
| X13 austerity trigger | Trailing actual burn; the free floor is never cut |
| X14 enforcer starvation and concentration | An escrowed $1M reserve; a fee undertaking; insurance; the TSC seat moved away; a backup enforcer |
| X15 engineered impracticability | Plan D named as the only outcome in the deed; nonprofit asset lock plus the attorney general |
| X16 server-side promises | Ordering and charter on the client; published server build hashes |
| X17 undefined words | Definitions in clauses 1–2; no curation surfaces |
| X18 grants cannot reach the operator | The operator is the charity (b.6.1) |
| X19 wrong denominator | Active host keys; churn; responder costs modelled separately |
| X20 3% optimism | Base 1.5% with a range of 0.75–3%; supporters no longer carry the plan |
| X21 staff versus scope | Scope cut; ladder rebuilt |
| X22 scale collapse | VLOP planning counts viewers; purchasing-power pricing and conversion decay in the sensitivity analysis; **limit L7** |
| X23, X24 adoption | Organizer-first wedge; the series as the way back; the concession stated |
| X25 isolated people | **Limit L4** (the Commons in v2; no synthetic members) |
| X26 name and domain | New name; neutral multi-domain resolution; card identity is its signature |
| X28 BIPA | No facial analysis |
| X29 TCPA | Self-entered, confirmed numbers; one reminder per card |
| X30 state laws | Geo-gating with a public notice; **limit L9** |
| X31 distribution kill | b.11; **limit L3** (native rendering) |
| X32 view from above | Dead; fragments cut |
| X33 wedge | Re-scoped (b.2) |
| X34 mind betrayal | No gateway; charter in the client; seed opt-in; 10-a-day cap; refusals; K8 on the shipped model |
| X35 council capture | Credentials from distinct hosts; staggering; issuance alarm; the TSC seat moved |

## b.16 The second pass: attacking the rebuild, with no mercy

| # | Attack on the rebuild | Fix or documentation |
|---|---|---|
| Y1 | **The IRS denies 501(c)(3) status.** An event-card service looks commercial, and helping people gather is not obviously charitable. | **Fixed as far as structure can go, and documented.** The charitable framing rests on open civic infrastructure, pre-registered research on social connection, and free service to all, with a pre-filing consultation [counsel]. K9 names the fallback (501(c)(4) at caretaker scale). Residual **L2**. |
| Y2 | **A purpose trust as the sole member of a charity** may be challenged as improper control, or the attorney general may insist on a self-perpetuating board. | Documented [counsel]. Fallback: the trust holds the *veto* membership and the enforcement role, and the board is elected by the council and named institutions. That is weaker than trust control, but still has no equity and still has the golden veto. **L2**. |
| Y3 | **Major donors become the new advertisers.** The plan needs $7M in major gifts by month 84, and donor fatigue or steering follows. | The 25% cap means at least 4 major donors a year. There are no conditions and every gift is published. Sensitivity shows "no major gifts" goes negative at M34, which triggers plan B, then C. **Residual L1: this is a philanthropically dependent utility for about a decade.** |
| Y4 | **Institutions pull the product toward their needs.** They will want attendance analytics and "engagement reports". | Clause 5 enumerates what may be paid for. Attendee analytics beyond consented counts is barred by clause 2. A new paid feature needs a council vote. |
| Y5 | **The organizer-first Commons becomes an institutional calendar** that crowds out individuals. | Per-host caps apply to institutions too. Metric 14 tracks organizations' share. A jury review is triggered above 40%. |
| Y6 | **The on-device guide depends on Apple and Google models**, which are incumbent dependencies with their own policies. Owners of older phones get no guide, which is unequal. | The guide is optional, and the deterministic drafter covers the core job. The K8 battery runs against each shipped model, and a model that fails is not used. Residual **L8**. |
| Y7 | **Circles without MLS**: a forwarded circle link grants membership, and removing someone needs a re-key. There is no forward secrecy. | The host re-keys on removal (a new link, old pages re-encrypted), and memory pages expire unless pinned. The claim wording states "for sensitive groups, use Signal". Residual **L6**. |
| Y8 | **The no-link rule and the 150 cap hurt legitimate uses** (a Zoom link, a 400-person community festival). | Map and major video-call links are on the allowlist. Large events convert to a public card with a host key, which is free. The friction is deliberate and small. |
| Y9 | **Client-side ordering is gamed through inclusion instead.** The server decides which cards are in the set. | Inclusion rules are deterministic and published. Daily set hashes are logged. Every removal carries a DSA statement of reasons in the transparency database, so omission is detectable by anyone running a mirror. |
| Y10 | **The enforcement reserve becomes a honeypot**: a captured Veto Foundation files sham suits to drain it. | Draws only on a Chancery filing. The court can award costs against bad faith. Draws are published. Refills are capped at 2% of inflows. |
| Y11 | **Neutral card domains are still domains.** Registries and registrars can suspend them. | Several domains across different registries; card identity is its content hash plus host signature, so any compliant host, including self-hosting, can serve it; plain text first. Residual: a coordinated block of all default domains degrades previews, not the text. |
| Y12 | **The 3× pay cap plus a $300k ceiling makes hiring security talent even harder** (the 04b limit, now worse). | Documented, **L10**. Mitigations: remote-global hiring at a blended cost, security audits bought from outside firms, and open-source contributors. The cap binds only the top, and the median can rise with the market by CPI and council vote. |
| Y13 | **Faster growth kills it** (1.0× growth goes negative at M35). | A pre-committed rule: the staff ladder moves only when **trailing 6-month inflows** cover the next step for 18 months. Growth beyond that is served by the caretaker-grade ops scale, and the waitlist for regions stays. |
| Y14 | **The seed opt-in is itself a mission prompt in the flow.** | The offer lives only on "What shapes me", which the user opens deliberately. It never appears in onboarding or in the guide's messages. The guide mentions it only if asked. |
| Y15 | **Credential rules exclude people who cannot attend often** (disability, caregivers) from governance. | An alternative credential: a verified host key at least 365 days old, plus one confirmation from any host. Jury selection by lot draws from all host keys at least 180 days old, weighted equally. |
| Y16 | **Plan D's "only permitted disposition" might itself be struck by a court** as contrary to public interest, or modified anyway. | Documented [counsel], **L2**. Forkability remains the last line: the spec, the code and portable identity mean a captured or sold operator holds no hostages. |

---

# (c) Honest limits (updated; residual risk stated plainly)

- **L1. The money is philanthropic for about a decade, and none of it is committed.**
  - The plan needs about $14.6M through month 84 ($12.5M of it gifts), of which about $7M is major gifts from at least four donors a year.
  - Earned revenue alone covers operating cost only at about 4–7M active host keys (year 9–11).
  - The downside cases do not reach self-sufficiency. They end at the caretaker scale or in plan D.
  - *Residual risk:* a funding gap in months 30–40 or 46–60 forces plan B or C. That is survivable, but it means a smaller product.
- **L2. The legal form is untested in this combination.** It combines a §3556 trust as sole member of a nonprofit that seeks 501(c)(3) status, a golden-veto membership, an escrowed enforcement reserve and a deed-named impracticability outcome. Each piece has precedent; the assembly does not. The IRS may deny exemption (K9). Courts keep equitable powers. *Residual risk:* falling back to 501(c)(4) or the PBC form, with weaker funding.
- **L3. Incumbents can absorb the open spec.** If WhatsApp or Messages render open cards natively and keep the responses, the spread loop and the independent home both shrink. That may be good for gathering and bad for the independent home. Conformance naming is our only lever.
- **L4. Isolated people still have the weakest door.** The Commons arrives in v2. Meeting strangers carries real physical risk, which can be mitigated but not removed. There will be no synthetic members, ever.
- **L5. Same-platform friend groups are conceded.** The card will not beat iMessage polls or WhatsApp Events inside an all-iPhone or all-WhatsApp chat, and the design no longer claims it does.
- **L6. Circles are weaker cryptographically than MLS.** There is no forward secrecy, and removal is by re-key. Web E2E depends on trusting code delivery until native apps and the verifier arrive, and the product says so.
- **L7. Scale economics beyond about 10M active host keys are unknown.** They include VLOP duties (possibly triggered by card viewers), purchasing-power pricing and conversion decay.
- **L8. The guide depends on incumbents' on-device models, or on devices many people do not own.** It is optional for that reason.
- **L9. State and national law changes month to month.** Age-verification laws may come to cover *answering* cards. Where they do, cards become view-only there, which weakens the wedge in those places.
- **L10. Hiring under tight pay caps** may leave security and cryptography under-staffed. Outside audits mitigate this but do not replace a team.
- **L11. Minors can answer cards that adults paste.** Only a name is collected, but they cannot be age-checked.
- **L12. Harm organized in private** (sealed cards under 150 responses, circles, other apps) stays invisible until someone reports it. This is a chosen trade-off.
- **L13. Governance can be captured by a patient, real-world faction.** The staggered seats, credential alarms and golden veto make it slow and visible, not impossible.
- **L14. The mind is still unproven with a real model.** K8 has never run, and paraphrased drift (F8) is open. The rebuild removes most of the guide's power to betray (no selection, no gateway, no server charter) rather than proving its loyalty. No guide ships until it passes.
- **L15. Figures marked [verify] and [counsel]** may be out of date or wrong: trademark classes and status, the IRS position, on-device model availability, 10DLC, the scope of the §3556 modification rule.
- **L16. It does not replace entertainment feeds.** It competes for the organizer's week and the moment of intention, not for the evening.

---

# (d) Verdict on the original design

**The single most dangerous flaw: its economics were built to fail in the one way that would corrupt it.** Three errors compound:

1. **The build money could not lawfully reach the operator.** The 04b plan counted about $5M of grants and donations as cash in a PBC while its own legal section forbade the transfer. Corrected alone, the base case runs out at **month 21**. With a smaller anchor loan and realistic staffing, it runs out at **month 14**.
2. **The paying unit was the unit the wedge avoids creating.** Revenue was a percentage of account-holders, while the wedge promised that nobody needs an account. Conversion was applied to cumulative sign-ups with no churn, at a rate that even a trust-owned, heavily-asking publisher (The Guardian) does not approach among its readers.
3. **Its protections sat on the servers it controlled, and its triggers ran on its own plans.** The charter slot was in the gateway, ranking was on the server, austerity triggers ran on planned burn, the free guide was not entrenched, and the enforcer had a $60k budget.

Put together, the original was a steward-owned company that would reach month 14–21 short of money, holding a free product nobody had to pay for, and holding exactly the levers ("Civic Insights", a paid guide, a "stricter safety" ratchet, austerity cuts) that turn a starving mission into a gentle extractor. **That is the covenant's "quiet reversal", and the plan's own numbers would have produced it.** Every other attack (the cloned wedge, the smear, the name) hurts. This one turns the project against its purpose.

**Is the rebuild safe from it?**
- **It is safe from the hidden version.**
  - The operator is now an entity that can lawfully receive the gifts and grants the plan depends on.
  - The model counts active users, applies honest conversion and matches staffing to scope.
  - The free floor, including reach, is entrenched by function.
  - Aggregates are data.
  - The austerity triggers run on actual burn and cannot touch the floor.
  - The ratchet can only remove capabilities.
  - The enforcer has money.
  - The impracticability outcome is pre-named as a handover, not a sale.
  - The guide has no server through which it could be turned.
- **It is not safe from the honest version.** It depends on philanthropy for about a decade (L1), and its legal form is untested (L2). But its failure mode has changed. It no longer reverses quietly toward extraction. It shrinks in public to a caretaker utility, or it hands itself over (plan D) with every user's data exportable and every card still resolving. For a home that is meant never to become a trap, that is the right way to fail.

*This is a proposal to be tested, not a claim that the work is finished.*

---

## Appendix A: the rebuild funding model (reproducible)

The attack runs used copies of `run-1/funding-model/model.py` and `final.py` with the changes described in Front 5. Because this phase may modify only this file, the rebuild model is reproduced here. It needs `cum_A` from the same anchors as 04b's `model.py`.

```python
ANCH=[(0,0),(6,300),(12,10_000),(18,40_000),(24,120_000),(30,300_000),(36,600_000),(48,1_800_000),
      (60,3_800_000),(72,6_500_000),(84,10_000_000),(96,14_000_000),(120,22_000_000)]
def cum_A(m,g):                      # 04b anchors, time stretched by growth multiplier g
    t=m*g
    for (m0,a0),(m1,a1) in zip(ANCH,ANCH[1:]):
        if t<=m1:
            return a1*(t-m0)/(m1-m0) if a0==0 else a0*(a1/a0)**((t-m0)/(m1-m0))
    return ANCH[-1][1]
def run(conv=0.015, growth=0.7, active=0.6, org_ratio=1.0, org_net=30, inst_final=1000, inst_net=200,
        var=0.025, staff_cost=175_000, bridge=1_500_000, grant_scale=1.0, major_scale=1.0, horizon=144):
    cash=debt=0; rows=[]
    for m in range(horizon+1):
        A=cum_A(m,growth)*active                                   # ACTIVE host keys
        c=0 if m<9 else conv*min(1,(m-9)/24+0.5)
        orgs=0 if m<10 else max(min(40,4*(m-9)), org_ratio*A/1000)
        inst=0 if m<24 else inst_final*min(1,(m-24)/60)**1.3
        earned=A*c*3.40+orgs*org_net+inst*inst_net
        g=(100_000 if 3<=m<12 else 250_000 if 12<=m<=60 else 125_000)*grant_scale if (m>=3 and m%3==0) else 0
        mg=min(2_000_000,250_000*(m//12))*major_scale if (m>=12 and m%12==0) else 0
        staff=(4 if m<7 else 6 if A<50e3 else 9 if A<300e3 else 14 if A<1.5e6 else 20 if A<4e6 else 28 if A<10e6 else 36)
        other=(20e3 if m<7 else 30e3 if A<50e3 else 45e3 if A<300e3 else 70e3 if A<1.5e6 else 100e3 if A<4e6 else 140e3 if A<10e6 else 190e3)
        one={0:60e3,1:60e3,2:40e3,10:120e3}.get(m,0)+(120e3 if m>=22 and m%12==10 else 0)
        opex=A*var+staff*staff_cost/12+other+one
        inflow=(500_000 if m==0 else 0)+(bridge if m==3 else 0); debt+=bridge if m==3 else 0
        cash+=earned+g+mg-opex+inflow-debt*0.01/12
        rows.append((m,A,earned,g,mg,opex,cash))
    return rows
```

---

## Sources (checked 2026-09-25 unless noted)

- *Facebook v. Power Ventures*: [Mintz](https://www.mintz.com/insights-center/viewpoints/2016-07-19-facebook-v-vachani-user-authorization-can-be-revoked-service) · [EFF](https://www.eff.org/deeplinks/2016/07/ninth-circuit-panel-backs-away-dangerous-password-sharing-decision-creates-even) · [844 F.3d 1058 (vLex)](https://case-law.vlex.com/vid/facebook-inc-v-power-892046987) · [Cert. denied (Crowell)](https://www.crowelltradesecretstrends.com/2017/10/u-s-supreme-court-rejects-cfaa-appeal-by-power-ventures-against-facebook/)
- WhatsApp Events: [WhatsApp blog](https://blog.whatsapp.com/new-feature-roundup-updates-to-group-chats-events-calls-channels-and-more) · [WhatsApp Help](https://faq.whatsapp.com/3313983622238973/?cms_platform=web) · [MacRumors](https://www.macrumors.com/2025/04/10/whatsapp-new-features-roundup/)
- iOS 26 polls: [MacRumors](https://www.macrumors.com/how-to/ios-create-polls-messages-app/) · [AppleInsider](https://appleinsider.com/articles/25/06/16/how-polls-in-ios-26-messages-app-makes-group-planning-easier) · [9to5Mac](https://9to5mac.com/2026/01/12/ios-26s-messages-app-adds-five-great-new-group-chat-features/)
- Apple Invites: [Apple Newsroom](https://www.apple.com/newsroom/2025/02/introducing-apple-invites-a-new-app-that-brings-people-together/) · [Apple Support: RSVP](https://support.apple.com/guide/apple-invites/rsvp-to-an-event-devc9d9cdbd5/ios)
- Partiful: [CNBC](https://www.cnbc.com/2025/04/19/meet-partiful-the-gen-z-party-planning-staple-thats-taking-on-apple.html) · [Sacra](https://sacra.com/c/partiful/) · [Wikipedia](https://en.wikipedia.org/wiki/Partiful)
- Link throttling precedents: [Forbes on Substack links](https://www.forbes.com/sites/mattnovak/2023/04/08/elon-musk-denies-substack-links-are-blocked-on-twitter-a-claim-thats-very-misleading/) · [Michael Tsai](https://mjtsai.com/blog/2023/04/10/twitter-restricts-substack-links/) · [Kansas Reflector](https://kansasreflector.com/2024/04/11/facebooks-ai-failure-wiped-out-kansas-reflector-links-even-facebook-may-not-know-what-went-wrong/) · [Techdirt](https://www.techdirt.com/2024/04/17/kansas-reflector-mostly-admits-that-metas-blocking-of-their-site-wasnt-deliberate/)
- FTC and Zoom: [FTC press release](https://www.ftc.gov/news-events/news/press-releases/2020/11/ftc-requires-zoom-enhance-its-security-practices-part-settlement) · [FTC business blog](https://www.ftc.gov/business-guidance/blog/2020/11/zooming-zooms-unfair-deceptive-security-practices-more-about-ftc-settlement)
- Scam ads: [CNBC on Reuters](https://www.cnbc.com/2025/11/06/meta-reportedly-projected-10percent-of-2024-sales-came-from-scam-fraud-ads.html) · [Lawfare](https://www.lawfaremedia.org/article/reuters-blows-lid-on-meta's-fraud-profit-scandal)
- BIPA and age verification: [ClassAction.org on Juul](https://www.classaction.org/news/juul-labs-hit-with-bipa-class-action-in-illinois-over-online-customer-facial-scans) · [Xident on the double bind (industry source)](https://xident.io/blog/age-verification-private-right-of-action-bipa-class-action-2026/) · [Biometric Update](https://www.biometricupdate.com/202604/bipa-damage-limitation-applies-retroactively-to-pending-class-actions-court)
- Data-business precedents: [PYMNTS on Foursquare](https://www.pymnts.com/connectedeconomy/2022/inside-foursquares-pivot-from-customer-app-location-data-platform/) · [CNBC on Foursquare](https://www.cnbc.com/2022/06/16/remember-foursquare-the-location-tech-used-by-apple-uber-knows-you.html) · [Strava Metro](https://metro.strava.com/) · [Forbes on Strava Metro going free](https://www.forbes.com/sites/carltonreid/2020/09/23/strava-metro-data-service-gifted-to-cities-to-boost-bicycling/)
- The Guardian: [Press Gazette 2024/25](https://pressgazette.co.uk/media_business/guardian-grows-revenue-and-reduces-losses-for-year-to-march-2025/) · [InPublishing 2025/26](https://www.inpublishing.co.uk/articles/guardian-media-group-publishes-202526-statutory-accounts-26908)
- Trademarks: [STOKE: Stoke Space (Justia)](https://trademarks.justia.com/886/48/stoke-88648256.html) · [STOKE: STOKE, SPC](https://trademarks.justia.com/884/80/stoke-88480668.html) · [STOKE: DROPSHIP LLC](https://trademarks.justia.com/906/35/stoke-90635296.html) · [Stoke Technologies](https://trademarks.justia.com/owners/stoke-technologies-inc-4717410) · [TRAVELSTOKE](https://trademarks.justia.com/866/44/travelstoke-86644823.html) · 04b's [USPTO 78443107](https://uspto.report/TM/78443107) (not reachable this session; verify)
- Delaware: [12 Del. C. §3556 (Justia)](https://law.justia.com/codes/delaware/title-12/chapter-35/subchapter-iv/section-3556/) · [Morris Nichols, Trust Act 2025](https://www.morrisnichols.com/insights-delaware-trust-act-2025-legislative-update) · [DGCL §102(f) (McCarter & English)](https://www.mccarter.com/insights/delaware-law-update-delaware-court-of-chancery-addresses-fee-shifting-bylaws-and-raises-the-question-of-whether-fee-shifting-could-be-plausible-by-a-stockholders-own-conduct-or-act-un/)
- Carried forward from 04b (checked there on 2026-09-25): the OpenAI recapitalization (Delaware and California AGs), Bluesky and Mississippi HB 1126, COPPA, the TAKE IT DOWN Act, the DSA minors guidelines, e-Evidence, the Apple TCN litigation, the did:plc specification, Signal's costs. See the 04b source list.
