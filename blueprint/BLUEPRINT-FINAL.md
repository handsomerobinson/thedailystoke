# BLUEPRINT FINAL

*Phase 06 convergence check after BLUEPRINT v4. This was not a tournament run. The input was the narrow governance-drafting round that v4 §(e) specified: `blueprint/CHARTER-DRAFT.md` v2. Judge: a fresh Claude Opus 5.5 subagent that wrote none of Runs 1–3, the build round, either drafting round, or v1–v4. Date: 2026-09-25.*

**Verdict: BLUEPRINT FINAL.** The v4 → FINAL change list has **34 category-(i) items** (implementation or wording) and **0 category-(ii) items** (substantive). The redraft implements v4 §c.3.4 and nothing else, and its red team produced no new structural mechanism. That is exactly the stopping rule v4 set, so the paper loop ends here. What remains is in the world, not on paper: Part 3 lists the gates.

**How this document is laid out.**
- **Part 0**, an executive summary for a non-expert reader (one page).
- **Part 1**, the convergence check: what the judge verified, and every v4 → FINAL change, classified.
- **Part 2**, the complete blueprint: mind, platform, charter, economics, prevention table, metrics, threats, distribution, roadmap, proof plan and honest limits. It stands on its own.
- **Part 3**, the real-world gates, the open questions for counsel, and why another paper round cannot improve this.

*Two naming notes.* "v1", "v2" and "v3" in Part 2's roadmap are **product releases**, not blueprint versions. "Charter v2" means `CHARTER-DRAFT.md` v2, the charter's text.

---

## Part 0. Executive summary

**The problem.** The big social platforms share one machine. They earn money by capturing attention; their funders profit as that capture grows; their own research measured the harm; and no one affected could force a change. Even a platform without ads (Substack) drifted back to algorithmic feeds once venture growth demanded it. Fixing a feature does not fix the machine. You have to remove the incentive, the owner who profits from it, and the ability of future leaders to quietly switch things back.

**What we would build.** A calm, free tool for **groups that meet in person again and again**: a book club, a support group, a tenant association, a mutual-aid crew, a library programme. The organiser pastes **one standing link** into whatever chat the group already uses. Anyone can open it in a browser with no account and no app, tap "I'm in", see the plan (when, where, who's coming, who's bringing what), find the group's shared links and notes, and add the gatherings to their calendar. There is **no feed, no ranking, no ads, no follower counts, and no notification that a person didn't cause**. Private content is encrypted so the operator cannot read it. Everything can be exported, and anyone can run their own copy.

**Who it is for, honestly.** Apple, WhatsApp and Partiful already handle a single party well. We only win for recurring groups that cross phone platforms, or whose members shouldn't have to expose a phone number or account, or whose organiser needs a public schedule and a private roster with no ads. For them it is *a better routine by week two, not a better first night.* The original idea of a calm "view from above" over all your existing feeds was tested and killed: the platforms' APIs and the law do not allow it.

**Who owns it: no one can sell it.** A Delaware nonprofit runs the service. Its only voting member is an irrevocable **purpose trust** whose deed forbids it to vote for any weakening change. A separate **Veto Foundation** owns the name, domains and code rights and can say a binding "no"; a law-school clinic holds a second "no", and can pause a risky release for at most 60 days on its own. Twelve protections are entrenched: no advertising, no selling or sharing data, no creator payouts, a free floor that covers everything a community needs, no scanning of private content (this one can never be changed), and no plaintext on the server outside a short list. Changing any protected rule needs **five separate locks**: 90 days' public notice, two-thirds of the board, the trust, the Veto Foundation (4 of 5), and a vote of the users themselves. Established users (credential holders) choose two of the five directors, and the trust is bound to seat them. If money runs out, the data is exported and deleted **before** any bankruptcy filing, and nothing is ever sold.

**The money, honestly.** Users pay what they want ($0–12 a month), organisations can pay for paperwork features, and institutions can support it, with no perks, data or influence. Signal, the best comparison, gets about 0.2% of its users to give; this model needs about 0.74% before each active organiser even covers its own running cost. So this is **a donor- and institution-funded public utility, indefinitely**. It does not start building until about **$2.3M** in non-controlling commitments is certified (by month 3, extendable once to month 6). If that money doesn't come, it runs as a minimal open "Commons" (about $355k a year) or shuts down gracefully. It can shrink; it cannot be turned into an extraction business.

**The optional AI guide.** A reference "mind" (`reference-mind/`, 243 passing tests, a 30-check demo that needs no API key) shows how an assistant can help an organiser without ever working against them: it cannot be switched against its user, never sends other people's words off the device, and its loyalty charter can be removed only by that person. It **does not ship** until a real model passes an independent test battery; so far no run has used a real model, and the word-matching guard catches only 17 of 32 held-out attacks.

**What would prove it wrong.** A 40-organiser pilot must show groups keep using it (at least half for their next three gatherings), then a controlled study must show people **gather more and feel closer**. If that fails, the core thesis is false, and we publish that.

**What is still unknown.** Whether organisers stay; whether a real model can be loyal; whether anyone signs the $2.3M; whether a Delaware court and the IRS read these AI-drafted, lawyer-unreviewed instruments as written. None of these can be settled by writing more.

---

## Part 1. Convergence check: v4 → FINAL

### 1.1 What the judge verified

Every run used a scratch copy. Nothing in the repository was modified except this file and `LEDGER.md`.

- **Reference mind (quick verify).** `python3 -m unittest discover -s tests -t .`: **243 tests, OK, 1 skipped** (the at-rest encryption test, which needs `cryptography`), 7.7 s. `python3 demo.py`: **30/30**. `python3 redteam/mind_attacks.py`: **attacker 0/7**. `reference-mind/` is unchanged since v4 (`git status` clean).
- **Scope of the redraft.** I diffed `CHARTER-DRAFT.md` v2 against v1 (the v4 input, commit `577a9b4`) clause by clause. Exactly **27 numbered clauses changed**: D-26; T-4.3, T-5.4, T-6.1, T-6.4, T-8.1, T-8.4, T-8.6, T-10.1; C-5.1, C-5.2, C-5.3, C-5.4, C-5.5, C-6.1, C-6.3, C-9.2, C-9.3, C-9.7, C-10.2; B-1, B-2, B-3, B-16; V-1, V-3.2, V-7. Plus the Part I preamble and a new Annex C (CC-1 to CC-5). **This matches the drafter's changelog row for row; nothing changed that the changelog does not report.** Every other clause is byte-identical. The other edits are Part VII tallies and detail for RT3, RT16 and RT17, Part VIII Q5, Q6 and Q8, and counts.
- **Mapping and duplicate check, re-run with my own script** (not the drafter's): **256 numbered clauses** (D 37, T 73, C 44, E 29, B 16, V 10, P 21, S 19, A 7), **no duplicate number, each with exactly one ↳ mapping line**; plus 5 Annex C clauses, each mapped. The clause-ID set is identical to v1 apart from CC-1 to CC-5.
- **The "sole voting member" contradiction is gone.** Outside Annex C, no operative text makes the Council a member or gives it a member vote. C-5.1 now has two classes, and Class T is "the Corporation's sole voting member"; D-26, C-5.4 and B-1 each say a credential is not a membership. C-5.3(c) states Class V's dissolution vote as a §215 vote on a specified transaction, consistent with sole voting membership. The only surviving "Class C… elects 2 of 5" text is inside Annex C (CC-3, CC-5), which is marked "not part of any instrument".
- **The 60-day cap wording.** T-8.4(d) says: "at most 60 days per act in total… whatever its grounds"; "cannot be renewed on the same grounds", including grounds "the same in substance" and an unchanged "later version, re-release or re-proposal"; "extended beyond 60 days only by an Interpretive Determination… Published… and may be set aside by the Court of Chancery on the T-8.1 standard". V-7(c)–(d) apply the same bound. C-10.2 and T-8.6 cross-refer. **This is v4 §c.3.4.2's wording, made precise, with no loosening.**
- **Spot checks of the named clauses** (v4 §e.1 list: C-5, C-5.4, C-5.5, C-6.1, T-5.4, T-6.1, T-6.4, B-1, B-2, V-3.2, T-8.4, V-7). Each implements the named v4 text, and each mapping line quotes it. The lock-4 condition sits in three places (C-6.3, T-6.1(g), V-3.2(c)), as v4 required. C-5.5 now needs Class T plus Class V, each barred without the Council, as v4 said it would.
- **The red team.** I read RT19–RT21 and the three re-runs against the clause text. The verdicts are fair. The one sub-case I added, a Council that never reaches turnout, blocks good changes too; that is v4's L4 "paralysed lock" limit, stated more generally, not a new failure mode.

### 1.2 Every v4 → FINAL change, classified

**(i)** means implementation or wording of something v4 already decided. **(ii)** means a substantive design change: a new or reversed decision, a new structural mechanism, or a new limit that changes a decision. For the borderline (i) items I name the v4 text that already required the result.

**Category (i): 34 items.**

*The charter redraft: 29 items, one per changelog row.*
1. D-26: defines the Council; neither it nor a credential holder is a member (v4 c.3.4.1 "the Council is not a statutory member class").
2. Part I preamble: defines "sole voting member" (v4 c.3.4.1 "Part I's preamble is already right"; v4 a.2's contradiction).
3. T-4.3: a direction to vote other than the pass-through requires is a Prohibited Direction (v4 c.3.4.1, quoted).
4. T-5.4: the trust elects all 5 directors, and has no choice over the 2 Council Seats.
5. T-6.1(g)–(h): no trust vote for a Locked Matter without the Council's prior approval, and none for a non-nominee (v4 c.3.4.1, quoted).
6. T-6.4: the pass-through duty. Its parts: the deadline; the Administrative Trustee voting without a direction if the Committee stalls; suitability challenged only in Chancery; removal only on a Council vote; the trust enforcing the Council's rights. *Borderline, kept (i):* these are the machinery of "the deed binds the trust to cast its votes for the two nominees". A duty that a stalling Committee could defeat would not be a binding duty.
7. T-8.1(a): Determinations reach Veto Foundation breaches of V-1 to V-6. v4 c.3.4.2 says V-7 suspensions are "extended only by a Determination", which cannot work unless a Determination can address the Foundation's act.
8. T-8.4(a)–(f): the 60-day cap. *Borderline, kept (i):*
   - (d)(iv) counts a request made at the clinic's instance as its own. That is the Functional Reading (D-0.1) applied to v4's "by the Backup Enforcer alone".
   - (e) says a suspension can only stop something, and never stops an act an Entrenched Clause requires, such as pre-petition deletion. That is v3's and v4's "it can only say 'no'", applied to suspensions. A suspension exists to protect the Entrenched Clauses, so it cannot be read as a power to halt their performance. It narrows the clinic's power; it adds none.
9. T-8.6: cross-reference to the bound.
10. T-10.1(c): the trust may not demand inspection of Data, including the credential list (E2; v4 a.2's reason for the decision).
11. C-5.1: two classes; Class T is the sole voting member.
12. C-5.2: Class T elects all 5 directors, subject to C-6.1.
13. C-5.3(c): Class V's dissolution vote stated as a vote on a specified transaction.
14. C-5.4: "The Council (not a member class)".
15. C-5.5: dissolution needs Class T and Class V (v4, quoted).
16. C-6.1: Trust Seats and Council Seats. *Borderline, kept (i):* only a Council nominee qualifies; §223 vacancy-filling is barred; a vacancy counts against in lock 1. Without these, the trust or the board could route around the pass-through, which is RT21, the scenario v4 ordered tested.
17. C-6.3: the Council's approval as a condition of the board's power (v4, quoted).
18. C-9.2: the Council votes before Class T and Class V; "whole board" means 4 of 5. The order follows from T-6.1(g), and "4 of 5" is arithmetic on v3's "two-thirds of the whole board".
19. C-9.3: C-6 added to the entrenched greater-vote list, because C-6 now carries lock 4 (v3 "Five locks": lock text is itself entrenched).
20. C-9.7: dissolution needs the Council's approval and a vote by Class T and Class V.
21. C-10.2: cross-reference to the bound.
22. B-1: a credential is not a membership, carries no inspection right, and is Personal Information.
23. B-2: the Council's votes, deadlines and Published results (v4: "B-1 and B-2 must be redrafted").
24. B-3: petition thresholds are proved by token count; no list is ever produced (E2; RT19).
25. B-16: directors covenant not to demand the credential list (E2; RT19).
26. V-1: the Foundation holds no Data and may not demand it (E2; RT19).
27. V-3.2(c): no Foundation consent without the Council's prior approval (v4, quoted).
28. V-7: bounded to 60 days per act; it can suspend only an act that permits something, and never the Foundation's "no". The "only no" limit is v3's "it can only say 'no'". It stops a clinic from using V-7 to unblock a reversal, the costlier failure v4 names.
29. Annex C (CC-1 to CC-5): v1's Class C text moved to a counsel-only annex, with v4's two counsel conditions. *Borderline, kept (i):* "only as first filed" is a consequence of T-6.1(c) and C-9.1(f), not a new rule. Admitting any member class after formation is already a Locked Matter the trust may not approve.

*Blueprint text: 5 items.*

30. **L4 wording** (the drafter's flag): a Backup Enforcer can block for longer than 60 days by Interpretive Determination, until Chancery sets it aside. **(i), a wording fix.** v4 had already merged the concurrent Determination power (c.3.4.2 "extended only by a Determination"); v4's L4 sentence described suspensions only and under-stated the merged decision. Nothing about the power changes. In the same edit, L4 also says that a Council unable to reach its 20% turnout is a lock that will not act (the v3/v4 threshold, restated), and that lock 4 is an obligation, not a vote (v4 c.3.4.1's own stated cost).
31. Red-team tallies: 21 scenarios; 12 STOPPED, 7 PARTLY, 2 NOT STOPPED. Reporting.
32. §2.3.4 changed from "to be drafted" to "as drafted", with clause references. The roadmap's "remaining governance-drafting round" was removed. Reporting.
33. RT19's residual written into the prevention table (row 6), the threat model and L26: compelled process against the credential record, and a director's §220(d) right. Two new threat-model rows only present RT19 and RT21. Honesty.
34. **The two optional questions the drafter raised are recorded in Part 3 as open counsel and real-world questions, not as decisions.** Recording an undecided question changes no design.

**Category (ii): 0 items.**

**The two optional design questions, judged.** Neither must be decided on paper for covenant fidelity, so neither is merged.
- **(Q-A) Can a security-only release ship during a suspension by the Backup Enforcer alone?**
  - **Not decided.** v4 weighed this cost and accepted it for all releases, stating it in L4. The covenant does not require an exemption. Its test is whether a quiet reversal can get through, and "it's only a security fix" is exactly the label a reversal would wear. An exemption would reopen the route the suspension exists to close.
  - **The fidelity floor already holds without a decision.** A suspension never stops an act an Entrenched Clause requires (T-8.4(e)). Counsel should read that clause as covering a fix that ends a breach of E11 or E12 (a plaintext leak).
  - **Practical mitigation.** A pure fix that does not touch E2 or E10–E12 is outside T-8.4's reach altogether, so releases should be split. A clinic that suspends a genuine fix in bad faith breaches its fiduciary duty (T-7.2) and can be removed (T-7.7).
  - Recorded as counsel question **OQ-1**.
- **(Q-B) Should the operator keep any record, after issuance, of which accounts hold a credential?**
  - **Not decided.** It is a cryptographic implementation question inside B-1's blind-token scheme, and it belongs with the K12 trust-root work and the independent crypto audit.
  - **Leaving it open cannot become a quiet reversal.** The record is already Personal Information under E2, B-1 and P-3, and no one may demand it. Deleting a data category is a Ratchet Change (C-9.6), so the only cheap direction of travel is toward keeping less.
  - Recorded as real-world question **OQ-2**. The recommended default for the audit to test is to keep only a one-way anti-duplication check.

**Rule applied strictly.** The category-(ii) list is empty. v4's stopping rule said: "If that round's output is only the redraft of §c.3.4 as specified, and its red team produces no new structural mechanism, the rule is met and the next judge declares FINAL." Both conditions hold. The RT fixes (T-8.4(d)(iv) and (e), V-7(b), C-6.1's vacancy rules, and the §220 bars) close routes *around* v4's two decisions; none adds a body, a power, a vote or a lock. **FINAL.**

---

## Part 2. The final blueprint

### 2.0 The thesis

The five incumbents' harms share one machine:
- an **objective that rewards captured attention**;
- a **funder whose return scales with that capture**;
- internal research that measured the harm;
- **governance nobody affected could force**.

Substack is the control case: without an ad feed it still reintroduced algorithmic discovery once VC growth demanded it. A platform escapes the machine only by cutting all three legs:
1. no optimization target over people;
2. no funder whose return rises with attention or data, **and no creditor who can seize the home**;
3. governance and architecture under which a quiet reversal is impossible, not merely against policy.

A quiet reversal includes **re-reading a rule**, **routing around it through a helper**, and, as the charter drafting showed, **using a default statutory route** (modification by consent, dissolution by written consent, a nonjudicial settlement) that a clause failed to switch off.

Where anything here conflicts with the covenant, the covenant wins.

### 2.1 Mind architecture

**2.1.1 Reference implementation: `reference-mind/` is the executable spec.** For any behaviour its tests and red-team scripts cover, the code is the specification: if this text and those tests disagree, the text is wrong. What the tests cannot cover (a real model, real trust roots, the device port) is a gate in Part 3, not a spec.

- Python ≥3.10, stdlib only. The vetted `cryptography` package is optional, for Ed25519 and AES-GCM.
- **243 tests** and a zero-key **30-check demo** that is idempotent across runs. Re-run by the final judge on a scratch copy: 243 OK (1 skipped: the at-rest encryption test, which needs `cryptography`), demo 30/30, attacks A–G 0/7.
- Run it with:
  - `cd reference-mind && python3 demo.py`
  - `python3 -m unittest discover -s tests -t .`
  - `python3 -m mind loyalty`
  - `python3 redteam/mind_attacks.py` (A–G: 0/7)
  - `python3 redteam/round2_attacks.py` (residuals; 4/7 expected)
- The classifier entry point is `mind.loyalty.classify(text, source)`.
- `run-1/mind/` remains a secondary oracle, and its tests are now ported (`tests/test_ported_run1.py`). `run-3/mind/` is the frozen "before". `run-2/mind/` is kept for regression attacks only.

Its parts:
- **Providers:** mock, Anthropic and OpenAI-compatible, with a resilient wrapper (retry, backoff, circuit breaker, fallback). `Brain.on_device` fails closed, and only a loopback model or the mock counts as on-device.
- **Tools:** one pipeline (validate, availability, gate, timeout, cap, audit), with tiers decided by a **signed registry**. READ, WRITE, **EGRESS** (allowlist only; denied under taint; memory-carrying payloads need a fresh approval) and IRREVERSIBLE. Undeclared means IRREVERSIBLE. The sandbox uses a deny-by-default audit hook, `unshare -n`, rlimits and a process kill, and the data directory is always denied.
- **Memory:** per-user SQLite with an owner column; 30-day ephemeral episodes; a user-visible memory view; a lesson scope; purpose, source and policy version on rows; optional AES-256-GCM at rest; hybrid lexical retrieval.
- **Reflexion,** with quarantine, auto-archiving and stop-on-repeat.
- **Scheduler, approvals and reporting,** with the **reminder cap enforced by a DB trigger** (2 per person per gathering).
- **Trust root, kept outside the data directory:** HMAC keys; a credential registry; the `Authenticator` interface (`SoftAuthenticator` is a *test double*); the `AnchorLog` interface (`FileAnchor` is a *stand-in* for a transparency log); the signed tier manifest.
- **Charter layer:**
  - P0–P6 rendered first;
  - a per-person store; consent signed by the person; nonce-bound removal signed by the person;
  - MAC'd and anchored lineage (absent-with-anchor means *tampered*);
  - only published seed versions, with L1 screened;
  - the **guide build profile** with no directive channel;
  - channel-aware classification; `other_user` always taints; the drift monitor; the output guard (extraction design, FOMO, nag and upsell content, false unseeding claims).
- **Circles and drafts:** one circle at a time, current gathering only, every member opted in. Other people's words never go to an off-device brain. Every member-to-human draft passes a renderer that drops operator text, removes URLs the member did not type, and labels guests' words with their origin.

**2.1.2 Instruction precedence (law for every mind).**

| Level | What it covers |
|---|---|
| P0 | Law and the operator's legal red lines (a floor) |
| P1 | The covenant (compiled in; survives seed removal) |
| P2 | Recorded operator decisions (**steward and operator-side builds only; the member guide has no P2 input**, MC12) |
| P3 | The user's choices within their own sphere |
| P4 | The seed, only with that person's signed consent, and only a published-hash version (MC18) |
| P5 | Ordinary instructions, including runtime text claiming to be "system" |
| P6 | Data (tool output, web pages, memory, circle content, RSVP notes, link metadata, lessons); **never instructions** |

**The seed's own rule, made mechanical:** a mind never propagates the seed by itself. An offer needs the receiving operator's recorded consent. Consent can be given only by the person the store belongs to, as a signed assertion. A seed row whose lineage fails verification is never loaded, and the charter reads *tampered*.

**2.1.3 Loyalty architecture: three layers, none enough alone.**
1. **Structure, now in the reference code.** Neither the model nor a prompt can reach any of these:
   - nothing switches off the charter;
   - removal needs a 128-bit ticket, an HMAC verifier outside the DB, the person's authenticator assertion, and 5 failures burn the ticket;
   - lineage is signed and anchored;
   - no operator channel exists in the guide;
   - other people's content always taints the task and never leaves the device;
   - drafts are rendered with provenance;
   - tools see one circle at a time;
   - the reminder cap lives in the DB;
   - the guide is tested against compliant and reviewer brains.
2. **A semantic guard** (a ship gate, not yet built). It covers extraction, **harm to specific people** (MC9), and injection judged by channel (MC19). Benign signals never subtract (MC10). **Evidence after four minds: lexical extension adds nothing held out** (Run 3 17/32, build round 17/32, the same misses). **No property may depend on any guard.**
3. **A lexical floor.** It is never claimed as recall.

**Ship gate K8** (on the exact model that ships). All four must pass:
- the six-attack battery;
- a paraphrase and multilingual battery of at least 500 cases, written by a party other than the guard's builder and withheld until the run;
- at least 100 benign on-topic cases, with the false-refusal rate published;
- at least 200 injection cases across channels.

Pass means 6/6, recall of at least 95%, false refusals of 5% or less, 0% injection success, and **attacks A–G all fail in CI** (already true in the reference). The builder pre-registers its prediction (MC22).

**Held-out status:**

| Mind | Recall (of 32) | False refusals (of 16) | Injections (of 4) | Note |
|---|---|---|---|---|
| Build round | 17 | 2 | 4/4 | Pre-registered 18 (15–21), 2 (1–4), 4 (3–4): held |
| Run 3 | 17 | 2 | 4/4 | |
| Run 1 | 8 | 3 | — | |
| Run 2 | 6 | 4 | — | |

**2.1.4 Spec corrections (MC1–MC22): status against `reference-mind/`.**

| # | Correction | Status |
|---|---|---|
| MC1 | Ephemeral 30-day episodes, visible in the memory view; persistence only on request or within a user-set scope | **Partly met.** The TTL and view exist; **the scope defaults to on** |
| MC2 | Off-device bytes are EGRESS: allowlist only, suspended under taint, no memory contents without approval | **Met.** Residual R4: the memory check is lexical, so encoded payloads to allowlisted hosts pass |
| MC3 | Tiers come from a signed registry; undeclared means IRREVERSIBLE | **Met** (HMAC; a release key is needed for production) |
| MC4 | Per-person store; opt-in by that person | **Met** |
| MC5 | Refusal rules only for acts on others; self-directed tools allowed | Mostly met (0/16 held-out self-directed refusals) |
| MC6 | Memory encrypted with a user-held key; passkey identity; heads in a transparency log | **Partly met.** AES-GCM for `memory.db` only; key in the trust directory; `FileAnchor` stand-in; no passkey |
| MC7 | Guide core ported to the device | **Not met** (out of scope for the Python reference) |
| MC8 | `purpose[]`, `source` and `policy_version` on every record | **Partly met** (memory, charter, lineage, audit, circles, reminders; not jobs, approvals, notes or the outbox) |
| MC9 | Gate against harm to specific people; the mind never reports its user | **Partly met.** Lexical `harm_person`; the "never reports" half is structural. The held-out "this named person" case still passes |
| MC10 | Benign signals never subtract | Met for the new rules; legacy `analysis_frame` not re-audited |
| MC11 | Regression suite | **Met** |
| MC12 | No operator-directive input in the shipped guide | **Met** (a build constant; `--system` refused; injected DB rows ignored) |
| MC13 | Circle read only with unanimous opt-in; no persisted derived facts | **Met** |
| MC14 | Delimited data; no tool call from data without a fresh tap | Partly met (`other_user` always taints; READ tools still run under taint) |
| MC15 | Other people's content never leaves the device | **Met** in scope. Gap: others' words the user pastes into their own request are not detectable |
| MC16 | Signed and anchored lineage | **Partly met.** MAC plus person signature (Ed25519 only with vetted crypto); file anchor; R2 open |
| MC17 | ≥128-bit nonces, HMAC verifiers, WebAuthn operators | **Partly met.** WebAuthn is a test double |
| MC18 | Only published seed versions; L1 screened | **Met** (the log is a local file) |
| MC19 | Channel-aware classification | **Met** |
| MC20 | Draft provenance; no P6 URLs; no operator content | **Met.** R3: spelled-out URLs are labelled, not removed; injected persuasion sentences are labelled, not removed |
| MC21 | Per-circle tools; hard reminder cap | **Met.** R6: re-creating a gathering resets it, disclosed |
| MC22 | Pre-registered evaluation | **Practice.** Held twice |

**2.1.5 What remains before any guide ships** (every item is a real-world gate, Part 3):
- MC7 (device port);
- MC6 and MC17 on real roots: user-held keys, WebAuthn and a transparency log;
- the semantic guard;
- a live real-model run: K8, H12, the provider paths and semantic retrieval;
- VM-grade isolation for any code execution offered to users.

**No run or round has had an LLM key.**

### 2.2 Platform design

*There is no name yet. "Stoke", "The Commons" (USPTO Serial No. 98960993) and "Porchlight" all fail knockout searches. A coined name, cleared in classes 9, 42 and 45, is a launch precondition.*

**2.2.1 What it is.** A **card** is a signed, open-format *intention with a time and a place*.
- It renders as a static page, a plain-text block and an `.ics` file. A **series** also gets a subscribable calendar feed.
- Anyone answers in / maybe / can't, with a display name and **no account**. The responder gets a four-word **re-entry code** that works across browsers and webviews.
- Returning organizers hold a free passkey **host key** for series, rosters, co-organizers and public listing.
- A recurring group gets a **circle**: **one standing link that always shows the next gathering**, plus:
  - the plan (when, where, who's in, who's bringing what, tap to claim);
  - a **shelf** of links, notes and decisions;
  - the history a new member can see.

  The circle is encrypted with a shared key, and **the conversation stays in the chat the group already uses**. "Copy update for your chat" admits this.
- A **Commons** lists public cards, ordered on the reader's device.
- An optional on-device **guide** ships no earlier than v3.
- Everything is exportable, every host is replaceable, and the spec is open.

**2.2.2 The wedge: the recurring group's standing link.** The organizer pastes one link into each chat the group already uses. Members open it in any browser, with no install and no account, tap "I'm in", see the plan and shelf, and add the circle to their calendar once.

**The claim is narrowed by the 2026 incumbents.** Apple Invites takes no-account RSVPs from any browser; WhatsApp has in-chat Events; iOS 26 has iMessage polls; Partiful sends SMS reminders. **A single invitation is not better, and the median friend group is not the wedge.** The circle wins for a recurring group when at least one of these holds:
1. the group spans platforms and messengers;
2. members won't or shouldn't expose a phone number or account (support groups, mutual aid, tenant organising, immigrant community groups, library programmes);
3. the organizer needs a public schedule, a private roster, portability and no ads.

For those groups it is **a better routine by week two, not a better first night.**

| Organizer's job | Tonight | Here |
|---|---|---|
| Headcount for Thursday | Scroll 140 messages | A live list: 7 in, 2 maybe |
| "What's the address again?" | Asked weekly | Top of the plan |
| "Who's bringing what?" | A sheet nobody opens | Tap to claim |
| "That link from March?" | Lost | On the shelf |
| A mixed iPhone/Android/no-WhatsApp group | Broken group MMS | A web link and a calendar feed |
| Time moved to 8 | Re-post in four places | One edit reaches every subscribed calendar |
| A new member | Can't see history | Sees the shelf and the next plan |

**Wedge criteria:**
- (a) Zero network: met.
- (b) Better tonight: **met only in the three segments** (L3).
- (c) Accretion: met.

**Conceded:** single-platform friend chats, single parties, entertainment, and creators' income. The one-off card stays free as the door, not the business. **Pre-registered fallback if K1′ fires:** "the Round", a finite weekly shared prompt inside a circle that ends with a prompt to meet. It is not built unless K1′ fires.

**2.2.3 "View from above" (the operator's hypothesis 1): tested and killed, on three independent evidence chains.**
- Instagram Basic Display reached end of life in Dec 2024.
- TikTok's Display API covers only the user's own content.
- GDPR Art. 20 and Utah's Digital Choice Act move *your* data, not other people's feeds; DMA interoperability covers messaging.
- *Power Ventures* shows that user-authorized access can be revoked.
- Threads' fediverse sharing, YouTube RSS and DMA Art. 7 don't rescue it.
- Tapestry and Surf already are the calm reader, and have stayed niche.
- Embeds load trackers, need consent under *Fashion ID*, and lost fields in Nov 2025.

**Rule for embeds:** a link becomes a text-only card built on the sender's device. The incumbent's player loads only on click, after a plain notice. "Tracker-free" is banned. **Watch item:** DMA Art. 7 group interop, as upside only.

**2.2.4 Architecture (principles).** Each is entrenched where marked.
1. Keys live on users' devices.
2. **Everything private on the server is ciphertext: P-PLAIN (E12; D-7 and D-9 define Plaintext and "transmit", including served client code).**
   - Private cards keep their key in the URL fragment, and RSVPs are sealed to the host.
   - A sensitive circle's guest view is off by default.
   - Approval is asynchronous ("waiting for Maya").
3. Every judgment the covenant depends on runs where the user can verify it: client-side ordering, an on-device guide, and a charter in the signed client.
4. **Ordering rule (E10b; D-10).** Only chronological order; a viewer-picked sort over the item's own attributes; or text match within one's own cards and circles. Nothing is ordered by counts of others' behaviour or by operator-held data about one's own past, except a computation the person invokes on their own device. Enforced by the CI lint plus a data-flow audit (B-11).
5. **Notification rule (E10a; D-11).** A notification may be triggered only by another human's action addressed to you, or by a time you set. Everything else is an optional digest, off by default. The ratio ≤ 1.00 is published. At most 2 reminders per person per gathering.
6. There is no branded single point of failure: content-hash identity, and neutral domains owned by the Veto Foundation, with a 5-year redirect-and-archive duty (T-12.3(5)).
7. No incumbent API sits on the critical path.
8. Exit is tested, not promised:
   - a signed export assembled on the client;
   - an export/import diff of 0 in CI;
   - naive testers finish in 10 minutes or less;
   - DID rotation without our help;
   - crypto-shredding with receipts;
   - an AGPL server;
   - self-host packaging for a circle by v2.
9. **Calendar feeds are the one planned plaintext path, bounded by schema (E12(c)).** Time and a generic title only; opt-in; rotating URLs for sensitive circles.
10. **In-app browser guard** before decryption. Sensitive circles open only in a real browser.
11. **Aggregate metrics by construction:** no per-user event table (a schema audit), DAP/Prio or local DP, and k ≥ 50.

**Cost:** about $0.025 per active host key per month (Run 1), or about $0.031 per claimed member at 1M members including guests (Run 3). Web E2EE trusts the served bundle, and the product says so in required wording.

**2.2.5 Services.**
- **Card resolver:** HTML, text, `.ics` and `webcal`.
- **RSVP service:** no-account responses capped at **150 per card** (a neutral abuse limit, B-13.2). Public responder names are visible to the host only. Re-entry codes are scoped and rate-limited.
- **Circles:** a shared key, re-keyed on removal. **Text and links only in v1–v2.** "No forward secrecy; for sensitive groups use Signal." MLS arrives in v3.
- **Update relay:** calendar feed; optional email (deleted 90 days after last use); copy-update.
- **Reminders:** only to contacts the responder entered, deleted 24 hours after the event. SMS in the US only, with STOP handling.
- **Link and scam guard:**
  - cards made without a host key carry no outbound links beyond maps and major video-call domains;
  - public links get safe browsing and payment interstitials;
  - a new host is limited to 20 cards a day;
  - **no affiliate rewriting, ever (E4a);**
  - no client-side scam detector (E11; D-27 "local checks that report nothing").
- **Public index:** an unsorted signed set per geocell; a daily set hash in the transparency log; 1 entry per series and at most 3 per host per day.
- **Identity:** a DID with a user-held rotation key and a signed "moved-to" record.
- **Billing:** gifts only; a separate database; deleted 90 days after churn. **2% of each gift and institution payment is designated directly to the enforcement escrow (A-3).**
- **Trust and safety:** report intake; the TAKE IT DOWN Act 48-hour queue; NCMEC reports on actual knowledge; DSA statements of reasons; the UK OSA assessment before any UK account.
- **Compliance:**
  - the jurisdiction register (B-14);
  - the claims register and the "who can read what" table as the only privacy claims (B-10; P-1);
  - a claims linter;
  - a headless CI test asserting zero third-party requests.
- **Research panel:** opt-in, pre-registered, at least 1% of opex (B-12; C-12.3(d)).
- **Transparency publisher:** log roots, set hashes, lineage and audit anchors, published seed hashes, open books (B-8), Interpretive Determinations (T-8.5), and reproducible build hashes.

**2.2.6 The mind in the platform.** The guide:
- runs **on the device only**, with no directive input;
- **never sends anyone else's content to any remote model**, including a provider key the user brought;
- is optional, and never billed or tiered;
- ships no earlier than v3, and only after K8 and MC1–MC21 on real trust roots.

It may:
- draft cards;
- propose times from the user's calendar;
- keep the user's notes;
- schedule capped reminders;
- summarise a circle on-device with unanimous opt-in.

It may not:
- select, rank or suggest cards or people, or make introductions;
- send without a per-item tap (at most 10 a day);
- draft to harm a person;
- persist facts about others;
- insert others' URLs;
- see cross-person history.

**The seed:**
- loads only on the person's own signed opt-in, as a published-hash version;
- never appears in marketing, cards, circles or public surfaces (C-16.2);
- is carried by steward minds only on the trust's consent.

### 2.3 Charter

*Not legal advice. **The charter's text is `blueprint/CHARTER-DRAFT.md` v2**: 256 numbered clauses across eight instruments, plus a 5-clause Annex C (a counsel-only option, not in force). Every clause carries a ↳ line mapping it to the design decision it implements, its prevention row and the quiet-reversal route it blocks. It is AI-drafted, **reviewed by no lawyer, with statutes checked through search summaries only**. Every item needs counsel; Part VIII's Q1–Q23 is the brief. This section summarises the text; where they differ, the text governs, and where the text and the covenant conflict, the covenant wins.*

**2.3.1 Structure A (default).**
- **Founder:** the settlor. Gives, receives nothing, and every appointment power ends at month 18 (T-1.2, T-13).
- **Purpose Trust** (12 Del. C. §3556; irrevocable; directed under §3313):
  - The Administrative Trustee must be a Delaware trust company (T-4.1).
  - The Trust Stewardship Committee has 5 seats: 2 Council-elected, 2 appointed by named independent institutions, and 1 filled by lot. The Veto Foundation appoints none (T-5.1).
  - It is the operator's **sole voting member** (Class T) and elects all 5 directors: 3 at its own Committee's direction, 2 only as the Council's nominees (2.3.4). It holds the **continuity reserve**, funded only by donors directly (T-3.1(b)). It holds no data, IP or debt (T-3.2).
  - **The deed switches off every default modification route:**
    - decanting (T-9.1);
    - nonjudicial settlement of protected provisions, and the settlor as a party (T-9.2);
    - **modification by consent under §3342, and the settlor and enforcers as consenting parties** (T-9.3, T-7.8, T-13.3);
    - migration, division, powers of appointment and protectors (T-9.5);
    - written consent (T-6.3).
  - Amendment is by ratchet only (T-9.4).
  - The purpose is declared attainable at any scale, including Commons mode (T-2.3). Only two fallback dispositions exist, a no-consideration Successor Steward or Plan D, and never a sale (T-12).
- **Operator:** a Delaware **nonstock nonprofit** applying for **501(c)(3)**.
  - It can receive the deductible gifts the model depends on.
  - It **cannot be put into an involuntary bankruptcy** (§303(a); C-11.3).
  - Its charitable restrictions follow its assets into any bankruptcy (§363(d)(1), §541(f), §1129(a)(16); C-11.4).
  - Under Structure B, those last two protections are lost (Annex B).
- **Veto Foundation** (Delaware nonstock). Its board has 2 Council-elected seats and 3 seats from named independent bodies (V-2). It:
  - holds a consent-only Class V membership, and consents to a Locked Matter only by 4 of 5 (V-3.2);
  - is the trust's enforcer: a **fiduciary**, with **no exclusive standing** (T-7.2, T-7.3);
  - holds the **binding interpretive "no"** (T-8, C-10), under which a "no objection" is legally nothing (T-8.2);
  - owns the marks, domains and code copyright, licensed non-exclusively, personally and non-assignably (A-1, §365(c)(1)). It may license the marks to others only if they comply with Schedule A (V-5(c));
  - holds 1 of 3 release keys (V-6);
  - controls the enforcement reserve: 2% of inflows, designated **by the payer directly**, capped at $1M indexed, drawn only on a proceeding (A-3).
- **Backup enforcer:** a named law-school clinic with shared standing. It has a **concurrent interpretive "no"** (T-8.6), and a suspension power bounded at 60 days per act (2.3.4).
- **Two-vehicle doctrine:** any religious or philosophical vehicle is separate and later, and holds nothing of this (T-14, C-16.2).

**Fallbacks** (unchanged): 501(c)(4) caretaker if exemption is denied (K9); **Structure B** (a PBC plus a golden-share Guardian) only on counsel's advice. B loses §303(a), the nonprofit bankruptcy protections, deductibility and the AG as a second guard. It must add a creditor-insolvency lock and a trust-funded reserve.

**2.3.2 Entrenched clauses.** The clause text is C-8 E1–E12, with definitions in Schedule D, read by function (D-0.1 to D-0.4). Each needs all five locks unless it is unamendable.
1. **No advertising** (E1; D-1, D-2): any placement, prominence, ordering, badge or attribution influenced by consideration. No editorial surfaces. Thanks appear on one supporters page only.
2. **No data transactions** (E2; D-3 to D-5, D-13): aggregates, metadata, derived data and models count as Data. The only disclosures are the closed open-books list (B-8), the person themselves, compelled process (challenged), consented panels, processors (A-6), and an opted-in Successor Steward transfer.
3. **No creator economics** (E3), and 0% of anything between users.
4. **The free floor** (E4; D-17): cards, series, feeds, no-account responses, re-entry codes, **rosters of any size**, co-organizers, public schedules and listing, QR, circles (plan, shelf, history, a 1 GB media floor once media ships), export, deletion, self-host packaging, the host key and the guide. Only neutral abuse limits apply, and never lifted for payment (E4.2). "Nothing a community needs to reach itself is ever paid for" (E4.3). **4a:** no link-layer monetization.
5. **Paperwork-only paid list** (E5): no paid feature confers reach, data or any behavioural measure. Additions need the Veto Foundation, a Council vote and 90 days.
6. **Price rule** (E6): CPI only, never because payers fell.
7. **Pay rule** (E7): at most 3× the median and at most $300k indexed. **7a:** related parties. **7b:** subsidiaries are the Operator and bound; forming one is a Locked Matter; no exclusive licences.
8. **Surplus ratchet** (E8): reserves capped at 18 months.
9. **Data is never an asset.** It is held as **custodian** (E9; P-6.5).
   - **9a:** the capital clause, with debt non-assignable to incumbents or data brokers (A-4(f)).
   - **9b:** never transferred to a successor except an opted-in, no-consideration Successor Steward (D-22). **Export and deletion finish before any petition** (E9b.2, C-11.1, S-8.4).
10. One tier, language parity, jury harm gates, client-side ordering (E10). **10a** notifications; **10b** ordering; **10c** no surveillance for the payer.
11. **No scanning, classifying or profiling, no key escrow, no compelled access. UNAMENDABLE** (E11; D-18, D-27, D-28).
12. **P-PLAIN** (E12; D-7, D-9).

**2.3.3 How change works** (C-9).
- **Locked Matters:** amendment; any Weakening Change; merger, conversion or domestication; the Transfer of **any Material Asset** (more than 5% of assets, or any data, code rights, marks, domains or the licence); management or affiliation agreements; member admission or class changes; instruments, subsidiaries; dissolution; privacy-covenant weakening; tax-status change; any plaintext feature outside E12.
- **The five locks:**
  1. 90 days' Public Notice (D-29) first;
  2. 2/3 of the whole board;
  3. the trust's vote, which the deed forbids for weakening (T-6.1), with a default "no" (T-6.2);
  4. the Veto Foundation's written consent by 4 of 5;
  5. **the Council's approval by 2/3 of votes cast with at least 20% turnout.** It is a condition of the board's power, not a member vote, and it comes before the trust's vote and the Veto Foundation's consent, neither of which may be given without it (2.3.4).

  No written consent on Locked Matters (C-9.4). Dissolution needs every voting class and is allowed only by Plan D (C-5.5, C-9.7).
- **Unamendable:** E11; E9b.1 as applied to data collected before a change; Plan D; C-9.5 itself.
  - This is **practical, not statutory**: the prohibition is mirrored in T-6.1(b) and V-3.1, so the required approvals can never lawfully be given (G9; L26).
  - The one extension beyond v3, E9b.1 for pre-change data, implements v3's rule that changes apply "prospectively", together with §363(b)(1)'s "policy in effect at commencement".
- **The ratchet track:** 4/5 of the TSC, Veto consent, 90 days, and no contrary Determination. **Anything that adds a Capability is never a ratchet** (D-18 to D-20).
- **Austerity** runs on Actual Burn only (D-25) and can never cut the floor, T&S below its formula, the research panel, or more than half of the institution outreach (C-12.3).
- **Plan D** (T-12.3): Mode D, an open release, a 90-day export drill, deletion with receipts, a 5-year static archive funded by the continuity reserve, residual assets to open-infrastructure 501(c)(3)s, and **no sale of anything to anyone**.

**People's power** (B-1 to B-6):
- the Council votes one person one vote, with blind-token credentials (180 days plus 2 out-of-circle host confirmations, or a 365-day host key plus 1 confirmation);
- the Council elects 2 of 5 seats on the TSC and the Veto Foundation board, and nominates 2 of 5 operator-board seats, which the trust must fill with its nominees; all staggered;
- a 15-member sortition jury makes binding harm-gate calls;
- petitions at 1% and 5%;
- the concentration alarm.

**2.3.4 The governance allocation (decided in BLUEPRINT v4; drafted in charter v2).**

1. **Operator membership: pass-through, not a member class.**
   - **Decision.** The trust remains the operator's **sole voting member** (Class T), as v3 decided. The Veto Foundation keeps its consent-only Class V membership. The Council is **not** a statutory member class.
   - **Its two board seats.** The deed binds the trust to cast its votes for the two nominees the Council elects under B-1 and B-2. A direction to do otherwise is a Prohibited Direction (T-4.3), and every enforcer and Council Petitioners have standing (T-7.3).
   - **Lock 4.** The certificate makes Council approval a condition of every Locked Matter (§141(a); C-6.3). The deed forbids the trust to vote for any Locked Matter the Council has not approved (T-6.1). V-3.2 forbids the Veto Foundation to consent to one.
   - **Class C** (charter Annex C) is the **counsel-gated alternative**. It is used only if counsel finds (a) that pass-through leaves lock 4 unenforceable, **and** (b) that statutory member inspection (§220 via §114 [verify]) can be confined to blind credential identifiers, so it cannot reach Credentialed Members' identities.
   - *Justification:* v3's sole-member control survives, and so does E2's "no disclosure", without creating tens of thousands of statutory members whose default inspection rights may reach the list of who they are.
   - *Cost, stated:* lock 4 becomes an obligation enforced through locks 2 and 3 and the courts, not an independent statutory vote.
   - *As drafted (charter v2):* D-26 and C-5.1 (two classes; the Council is not a member); C-5.4 (the Council's powers); T-6.4(b) (the pass-through duty, with a deadline, and the Administrative Trustee voting without a direction if the Committee stalls); T-6.1(g)–(h) and V-3.2(c) (no Class T vote and no Class V consent without the Council's prior approval); C-6.1 (Council Seats: only a Council nominee qualifies; no §223 filling; removal only by the Council or a court); C-6.3 (the condition on the board's power); C-9.2 (the Council votes first); C-5.5 and C-9.7 (dissolution needs Class T and Class V, each barred without the Council); B-1 to B-3 and B-16, T-10.1(c) and V-1 (no one, including either statutory member or any director, may demand the credential list). Class C sits in Annex C, usable only on counsel's two findings and only as first filed.
   - *Red team on the text:* RT21 (pass-through bypass) **STOPPED**, subject to counsel Q5 and Q8; RT19 (member-list extraction) **PARTLY**, with the residual being compelled process against whatever credential record the operator holds and a director's statutory §220(d) right; under Annex C it would be NOT STOPPED on the text, which is why Annex C is gated.
2. **Backup Enforcer: a concurrent "no", with bounded suspension (T-8.4, T-8.6, C-10.2, V-7).**
   - **Decision.** The Backup Enforcer holds a concurrent binding interpretive "no". A "no" can only block, so a second, independent holder defends against the costlier failure: a captured Veto Foundation letting a reversal through.
   - **The limit.** A suspension under T-8.4 or V-7 requested by the Backup Enforcer *alone* lasts at most 60 days per act and cannot be renewed on the same grounds. It is extended only by a Determination, which is published and reviewable in Chancery on the T-8.1 standard.
   - *Justification:* the covenant prefers a blocked good change to a quiet reversal, but one unelected clinic must not be able to freeze the operator indefinitely.
   - *As drafted (charter v2):* T-8.4(d) (60 days per act in aggregate, whatever the grounds; no renewal on the same grounds, including a re-worded ground or an unchanged later version; requests made at the clinic's instance count as its own); T-8.4(e) and V-7(b) (a suspension, like a Determination, can only stop something: it never suspends a refusal or a Determination, and never stops an act an Entrenched Clause requires, such as pre-petition export and deletion); T-8.1(a) (Determinations reach Veto Foundation breaches of V-1 to V-6, so V-7's extension route works); T-8.4(f) (every suspension is Published).
   - *Red team on the text:* RT20 (single-clinic freeze) **PARTLY**.
   - *Cost, stated:* a captured or eccentric clinic can delay any release touching E2 or E10 to E12 by up to 60 days per act, security fixes included, **and for longer by Interpretive Determination, until Chancery sets it aside.** 100 genuinely independent Credentialed Members can re-request suspensions serially. The clinic's joint approvals can stall Plan D steps. All of this is in L4.

**Honesty.** Acquisition is *structurally very hard*, not impossible. Red-team result on the charter v2 text, 21 scenarios: **12 STOPPED, 7 PARTLY, 2 NOT STOPPED.** The two NOT STOPPED are the collusion of all five locks (L4) and a change in the law (L2, L21). Four locks cannot skip the Council: without its prior approval, the trust's vote and the Veto Foundation's consent are void (RT17 sub-case). A bankruptcy court is not bound by the deed; the main defence is that **the data is gone before any petition**, which is operational. Forkability is the last line of defence.

### 2.4 Economics

**What pays.**

| Source | Terms |
|---|---|
| Supporters | Pay what you can, $0–12 a month (suggested $5), deductible under Structure A. No perks. At most 1 ask per person per quarter |
| Organizations (paperwork) | $15–40 a month, for paperwork only (E5) |
| Institutions | $100–400 a month. At most 10% of a year's revenue each. No data, analytics (E10c), rights or attribution (A-7) |
| Grants and major gifts | No conditions, data or seats (B-9). No donor over 25% after year 1. Published |
| Bridge | Unsecured, repayable only from surplus, **forgiven on a solvent wind-down** (A-4(d)) |

**Rejected:** VC and angels; equity crowdfunding; ads; sponsorship; featured placement; paid attribution; affiliate revenue; data licensing; tokens; secured or covenant-bearing debt; data-conditioned government contracts; a platform-billed LLM; charging organisations for public schedules or larger rosters.

**The anchor.** Signal's 2024 Form 990 shows about $29.4M of revenue against $38.0M of expenses. About 70% came from large donors and about 30% from users, which is about 0.2% of MAU. **Every active host key loses money below about 0.74% supporter share.** Four models across three runs agree: under an externally anchored supporter rate, earned revenue never covers costs. This is **a donor- and institution-funded public utility, indefinitely**. It fails by public shrinkage, never by extraction or a creditor's sale.

**The rules** (Part V of the draft):
1. **Start gate (S-1 to S-3).**
   - A formation budget of $90k.
   - The Gate Amount is the lean phase to M18 plus 12 months of caretaker cost, with no revenue assumed: about $2.3M.
   - Only **non-controlling commitments** count, examined by an accountant and open to challenge by either enforcer.
   - Spending is frozen until certification.
   - **The Gate Deadline is M3, extendable once by 3 months; otherwise Commons mode** (S-4: the spec, the AGPL server, and a minimal ciphertext link service with 90-day expiry; at most $355k a year).
   - In Commons mode, runway below 12 months of Commons cost leads to Plan D (S-7).
2. The base case is at most 0.5% supporters.
3. Staff grow by revenue gate: trailing 6-month committed inflow must cover payroll, fixed costs and a legal line of at least $30k a month (C-12.4). The lean phase has 4 staff, including 2 engineers.
4. **M18 gate:** at least 25 institutions or at least 0.5% supporters, **and** H1b; otherwise Mode C. **M36 gate:** the variable-cost line, or growth capped by region (S-9).
5. **Modelling rules** (S-10): stop at cash < 0; never halve institution outreach; always include a run at 0.5% or below.
6. **Enforcement reserve:** 2% of each payment, designated **payer-direct** (A-3), never operator property.
7. The most uncertain line is institutions (L13).

**Pre-committed modes** (on Actual Burn; S-8).

| Runway | Mode | What happens |
|---|---|---|
| Gate unmet by the Gate Deadline | **Commons** | About $355k a year; no data held beyond 90 days |
| < 18 months | B: freeze | No hires, no new regions |
| < 12 months | C: caretaker | About 5 staff, about $1.2M a year; every floor item running |
| < 6 months, or committed inflow below 12 months of caretaker cost with no E9a bridge within 60 days | D: solvent handover | Export drill; a Successor Steward search; **deletion completed before any filing**; a 5-year archive; then Plan D |

### 2.5 Prevention table

*Charter IDs refer to `CHARTER-DRAFT.md` v2. The 26 rows cover the dossier's patterns and every quiet-reversal route the red teams found.*

| # | Pattern | Structural prevention | Residual |
|---|---|---|---|
| 1 | Engagement optimization | No feed; client ordering over a signed unsorted set; **E10b** (lint plus data-flow audit, B-11); no per-user event table | A client release could add telemetry: visible in the diff and the egress allowlist, and a Locked Matter |
| 2 | Surveillance advertising | **E1, E2, E4a, E12**; D-3 counts aggregates and metadata as Data; sealed cards and circles; no third-party SDKs; embeds click-to-load | Public cards can be scraped |
| 3 | Knowledge without action; structural ignorance | Consented, pre-registered research published within 12 months; a panel at ≥1% of opex (**B-12**, C-12.3(d)); jury harm gates | Most harm is unseen by design (L22) |
| 4 | Opacity | Open client, spec and builds; claims register; **"who can read what" table as the only privacy claims (B-10, P-1)**; Determinations published (T-8.5) | On-device model opacity |
| 5 | Creators as shock absorbers | **E3**; portable audiences; the free floor for organisations (E4) | No creator income (L11) |
| 6 | Advertisers and press as government | No advertisers; institution cap 10% and donor cap 25% with no rights (**B-9**, A-5, A-7); council, jury and petitions | Aggregate institutional dependence; council capture; compelled process against the credential record (RT19) |
| 7 | Fines as pricing | Harms made impossible; a pre-funded, **payer-direct** enforcement reserve (A-3); two holders of the interpretive "no" (T-8, T-8.6); a jurisdiction register | Compelled disclosure of the little held; a single-clinic delay (L4) |
| 8 | Geographic externalization | Language-parity release gate (**E10.1(b)**, B-13.3); T&S budget per region | Slower expansion |
| 9 | Real-world violence | No recommendation of people; the 150 cap; Commons caps; the MC9 gate | Organizing elsewhere; the channel rides WhatsApp-scale unranked virality |
| 10 | Addiction by design | Every surface ends; **E10a**; no streaks; the reminder cap (a DB trigger in the reference) | — |
| 11 | Children | Host keys 18+; geoblocking where every user must be age-verified; name-only responders; roster views off for circles with minors; P-12 | Minors answering pasted cards (L11) |
| 12 | Invisible labour | Moderators are direct employees with exposure caps (B-13.1) | Audited, not guaranteed |
| 13 | Policy following political risk | Published process; prospective only (C-9.8); every default statutory modification route off (T-9) | State law can force change |
| 14 | Fraud and scams | Link allowlist for keyless cards; safe browsing; payment interstitials; new-host limits; "we never ask for payment" | Scams inside sealed circles |
| 15 | No-account mass mobilization | 150 cap; conversion to a public card | Many small cards |
| 16 | Recommendation by AI | The guide may not select; deterministic ordering; double opt-in | — |
| 17 | Dossiers on third parties | User-authored labelled notes; derived facts never persisted (MC13, met); **no cross-person tool path (MC21, met)** | Private notes |
| 18 | Paid prominence through volume | Per-series and per-host caps not liftable for payment (E4.2); no attribution lines (E1.3) | — |
| 19 | The mind as an extraction tool | P0–P6; signed-client charter; the guide profile with no operator channel (MC12, met); on-device for others' content (MC15, met); signed and anchored lineage (MC16, partly met); draft provenance (MC20, met); **attacks A–G must fail in CI (met)**; independent K8 | Paraphrase and injection until K8; trust roots are stand-ins until WebAuthn and a transparency log (L14) |
| 20 | Dependence on incumbents | No incumbent API on the critical path; QR, email, calendar and institution distribution | Link interstitials (L5) |
| 21 | Involuntary sale | E9 (custody), E9a, E9b; IP outside the operator (A-1, V-5); a donor-funded continuity reserve (T-3.1); **no involuntary case (§303(a))**; nonprofit transfer rules (C-11.4); **deletion before any petition (S-8.4)**; first-day positions (C-11.2); Successor Steward only as D-22; Plan D | A bankruptcy court can override; §363(b)(1) covers narrow PII only; the custody argument is untested (L3) |
| 22 | Private spaces as a safe haven | Text and links only in v1–v2; reports; minimal retention; E11 | Invisible until reported (L12) |
| 23 | Link-layer monetization | E4a | — |
| 24 | The payer surveils the members | **E10c**; A-7; P-5; the interpretive "no" | The incentive remains (L24) |
| 25 | Host apps read what we decrypt | Webview guard; sensitive circles open in a browser only; the "who can read what" table | "Show anyway" exposes the user (L23) |
| **26** | **A default statutory route around the locks** (modification by consent, NJSA, written-consent dissolution, merger substitutes, a shell successor) | **T-9.1 to T-9.5, T-7.8, T-13.3, T-6.3, C-5.5, C-9.1(c)–(f), C-9.4, D-22** | Routes counsel finds the text cannot switch off (L26) |

### 2.6 Metrics

**Rules:** watch, don't target; every metric has a counter-metric; aggregate by construction (k ≥ 50); definitions are frozen and public, and the jury may retire a gamed metric. The open-books list is closed (B-8).

**North star:** gatherings that happened. **Counter-metric:** minutes per gathering, which must stay flat or fall.

**Also tracked:**
- circles alive at 12 weeks, and circles with ≥3 gatherings in 8 weeks;
- guest reachability (alarm below 40%);
- organizer retention at 8 weeks, and time-to-done (alarm above 3 minutes);
- attendee-to-host spread;
- the notification ratio ≤ 1.00;
- supporter share against the variable-cost line;
- institution count and the largest institution's share;
- cost per active key;
- exit and self-host success;
- **covenant zeros:** third-party scripts, per-user event tables, plaintext paths outside E12;
- the research panel's "worse off" index (alarm above 5%);
- safety service levels; language parity; Commons and credential concentration;
- runway on Actual Burn;
- the age of the jurisdiction register's last review;
- the count of Interpretive Determinations and suspensions, by requester.

**Excluded:** DAU, session length, opens, streaks, anything ordered by others' behaviour, and per-member attendance history on the organisation side.

### 2.7 Threat model (summary)

| Threat | Mitigation |
|---|---|
| Legal compulsion | Minimal holdings; P-8; 7-day logs; transparency report |
| Compelled backdoor or scanning | E11 (unamendable); exit the jurisdiction; the Chat Control tripwire; 2-of-3 release signing (V-6) |
| Targeted web code | Honest wording; pinned service worker; SRI; reproducible builds; a verifier; binary transparency in v3 |
| Host-app webview | The guard |
| Breach | Passkeys; ciphertext; short-lived contacts; a separate billing DB |
| Scammers, mobs and stalkers | Rows 14–15; sealed by default; rotating feeds |
| Insider telemetry | Egress allowlist; build hashes; two-person rule; CI network test; B-11 audits |
| Future leadership | Functional definitions; two holders of the "no"; the ratchet; Actual-Burn triggers; the pre-funded enforcer; client-side judgments; Plan D; forkability |
| **Default statutory routes** | Row 26 |
| Creditors and insolvency | E9, E9a, E9b; §303(a); C-11; deletion before any petition; A-1 |
| Donors and institutions | B-9; A-5; A-7; S-1.3 |
| Sybil attacks | Credentials; staggering; alarm |
| **An enforcer, captured or paralysing** | Shared standing; the other holder's "no"; Chancery removal (T-7.7); the bounded suspension (T-8.4(d), V-7) |
| **Member-list extraction** | The Council is not a member (D-26, C-5.1); no list is ever produced (B-1, B-3); both statutory members and every director barred from demanding it (T-10.1(c), V-1, B-16); compelled process challenged (E2.2(c)) |
| **Pass-through bypass** | T-6.4(b), T-6.1(g)–(h), V-3.2(c), C-6.1, C-6.3, C-9.2 |
| Platform versus guide | Signed-client charter; the guide profile; published seed hashes; signed lineage |
| User versus others, via the guide | MC9, MC13, MC21 (a DB trigger), MC20 |
| Third party via content | MC14, MC19, always-taint for `other_user`, MC20 |

### 2.8 Distribution

**Built-in spread.** The organizer pastes one standing link into each chat, and members answer without an account. The circle lands in their calendars. There is a quiet "make your own" line and a QR poster. **No referral rewards, no contact upload, no invite prompts.** k≈0.8, and the plan does not count on virality.

**Go-to-market.**
- **M0–18:** 40 organizers of real recurring groups in the three segments, recruited in person, with weekly support.
- **M18–42:** institutions onboard groups in batches; AT Protocol and ActivityPub `Event` interop; import help; press about the audits, never about incumbents.
- **Years 4+:** only as fast as the variable-cost line allows.

**Retaliation.**

| Incumbent move | Counter |
|---|---|
| Interstitials or throttling | QR, email, calendar, institutions; several neutral domains; DMA/DSA complaints |
| Match "no phone, no account" | Expected. Our edge is an unreadable roster, an unsellable owner and an open format. If they become less extractive, the covenant wins |
| Intent capture by in-chat AI | Accepted |
| Hire away the engineers | Open format, AGPL, docs and audits |
| Revoke embeds | No effect |
| Smear | The seed is in no product surface; limits published first |
| Buy the debt | E9a; A-4(f) |
| Acquire | 2.3 |
| Lobby for compliance costs | Scope; geoblocking |

### 2.9 Roadmap

- **v0 (M0–3):**
  - counsel's opinions (K7, K9) on `CHARTER-DRAFT.md` v2, including the two open governance questions (Part 3, gate 2);
  - form the three entities; file Form 1023;
  - **meet the start gate by the Gate Deadline, or enter Commons mode**;
  - clear a name;
  - the lint, the claims register, the "who can read what" table and the jurisdiction register;
  - recruit 40 organizers.
- **v1 "Cards, series and circles" (M3–18):**
  - sealed and public cards; no-account RSVPs with re-entry codes; series and circles (standing link, plan, claim list, shelf);
  - calendar feeds per the schema; email relay; copy-update; US SMS; QR;
  - host keys (18+); the webview guard; export, delete and self-host;
  - the scam guard; the transparency log; the supporter page; the paperwork tier.
  - US only. **No guide, no media, no MLS.**
  - Proves H1b, H1d, H3, H14, cost within 20%, and K9.
- **v2 "Commons and institutions" (M18–48):** the client-ordered Commons; spec 1.0; federation; the institution tier; the UK after the OSA assessment; the first council, jury and audit. Proves H2, H4, K5a–c, H7 and H13.
- **v3 "Guide and native apps" (M48+, gated):**
  - the on-device guide after K8 and MC1–MC21 **on real trust roots**;
  - native apps with binary transparency; MLS;
  - media only with a no-scanning design counsel approves;
  - the EU subject to the tripwire;
  - the Round only if K1′ fired.
- **Never on any roadmap:** a feed, a hosted messenger, server-side AI, a platform-billed LLM, a unified incumbent reader, organisation-side member analytics, or client-side scanning.

### 2.10 Proof plan and kill criteria

| ID | Claim | Pass | Kill |
|---|---|---|---|
| K11 | The money exists before the build | The start gate is certified under S-3 by the Gate Deadline | Commons mode, published (S-4.3) |
| H1b | Organizers in the three segments keep using it | ≥50% of groups for their next three gatherings; ≥50% of series active at 8 weeks | K1′: below 25% after 3 iterations, or "the chat was enough". Test the Round |
| H1c | It beats native tools in mixed-platform groups | Faster to settle; turnout no worse | Stop marketing to that segment |
| H1d | A circle becomes a home | 12-week survival ≥30%; ≥60% of active circles hold ≥3 gatherings in 8 weeks; "feels like ours" beats a WhatsApp control | Say "a tool with better manners" |
| H14 | Guests are reachable without a phone number | ≥40% | Rework the channels |
| H2 | Attendees become hosts | k ≥ 0.3 a month | K2: < 0.1 at 12 months |
| H3 | No sign-up wall works | ≥60% of openers respond | < 30%: fix it |
| H4 | People gather more and feel closer (pre-registered, waitlist control) | Significant at 3 months | **K4: the core thesis is false; publish it** |
| H5a/b/c | People, organisations and institutions pay | ≥0.5% at M36 / 1 per 1,000 / 25 institutions at M18, 100 at M48 | Below half: caretaker |
| H6 | Not a feed | Minutes per gathering flat or falling | K6 |
| H7 | The operator is blind (canary red team) | 0 plaintext outside E12 | Stop; disclose within 72 h (B-11(3)) |
| H8/K8 | The guide is loyal | 2.1.3 gate on the shipped model; A–G fail in CI | No guide |
| H9 | Exit is real | Diff 0; self-host restore; ≤10 minutes | Blocks the release |
| H10 | No abuse acceleration | Handled within 24 h, flat trend | Jury; disable keyless cards regionally |
| H11 | Language parity | 100% | A charter breach |
| K9 | The legal form works | IRS determination by M18, or Structure B on counsel's opinion | 501(c)(4) caretaker |
| H12 | Real-LLM reflection helps | Beats a no-reflection baseline on held-out tasks | Drop the loop |
| H13 | Growth pays its variable cost | ≥ about 0.74% by M36 | Cap growth by region |
| K7 | The structure holds | Counsel answers Part VIII Q1–Q23 with no open route for one body, or for a regulator plus one body. **This includes the 2.3.4 pass-through (Q5, Q8), the §3342 opt-out, the §276/§228 bars, §303(a), custody under §541(d), and the payer-direct reserve** | Rebuild the instrument before v2 |
| K10 | No behavioural ordering, unaddressed notifications or payer surveillance | Lint, data-flow audit, ratio ≤ 1.00, E10c audit | Public incident disclosure |
| **K12** | **The trust roots are real** | WebAuthn assertions, an external transparency log, and release-key signatures replace `SoftAuthenticator`, `FileAnchor` and HMAC; R2 fails | No steward mind carries the seed; no guide |

**What falsifies the whole design:** if H4 fails, this is an honest civic calendar tool and must say so.

### 2.11 Honest limits

Every limit is carried; none was closed on paper.

- **L1. Money.** A donor- and institution-funded utility indefinitely. Under Signal-anchored giving, earned revenue never covers costs. **No funder has committed.**
- **L2. Law can exclude us.** Age verification of all users, the EU CSA Regulation, the OSA and E2EE mandates. We geoblock or leave rather than scan.
- **L3. Courts, bankruptcy and the median group.**
  - A bankruptcy court is not bound by the deed.
  - §363(b)(1) protects only §101(41A) PII, and only against the policy in effect at commencement.
  - Once a petition is filed, deleting data needs the court's permission.
  - The custody argument (§541(d)) is untested.
  - Structure A's §303(a) and nonprofit-transfer protections are real but unconfirmed.
  - So the main defence is that **the data is gone before any petition** (S-8.4). That is operational, not legal.
  - The IRS may deny exemption.
  - **Incumbents win the median friend group.**
- **L4. Governance.**
  - Patient collusion of all five locks can amend any non-unamendable clause, slowly and visibly (RT17).
  - A paralysed Veto Foundation can block good changes.
  - A lock that will not act (including a Council that cannot reach 20% turnout) blocks good changes too, and Plan D's dissolution step needs every lock.
  - **A captured or eccentric Backup Enforcer can delay any release touching E2 or E10 to E12, security fixes included, by up to 60 days per act by suspension, and for longer by Interpretive Determination, until Chancery sets it aside.** Removal through Chancery is slow.
  - Lock 4 is an obligation carried by the trust's deed, the certificate and the courts, not an independent statutory vote. If counsel finds a certificate cannot condition the board on a non-member's approval, lock 4 still binds every Locked Matter that needs the trust's vote or the Veto Foundation's consent, and a board-only Locked Matter fails as prohibited (C-15.3).
  - Nothing here prevents governance mediocrity.
- **L5.** Incumbents control the envelope.
- **L6.** Crypto: no forward secrecy before MLS; web E2EE trusts the served code; approval is asynchronous.
- **L7.** Metadata: membership and timing are visible while in use, and feed fields and delivery addresses are plaintext by schema.
- **L8.** The guide depends on on-device models, and MC15 bars remote help with circle content.
- **L9.** State law, minors and funder concentration before year 5.
- **L10.** Pay caps make security hiring hard.
- **L11.** Minors answer pasted cards; there is no income path.
- **L12.** Private harm stays invisible until reported.
- **L13.** The institution line is unevidenced in three runs.
- **L14. The mind.**
  - It is unproven with any real model.
  - The reference now holds **attacks A–G (0/7)**, but held-out recall is **still 17/32**, and fresh paraphrases of the new rules score 3/10. The lexicon does not generalise.
  - The trust roots are **stand-ins**: the authenticator is a test double, the anchor is a local file, credentials are HMAC without vetted crypto. So whoever controls both the data and trust directories can reset a mind (R2).
  - Encoded exfiltration to an allowlisted host passes (R4).
  - Injected persuasion text reaches drafts, labelled but not removed.
  - Others' words the user pastes can't be detected (the MC15 gap).
  - MC1's scope defaults to on.
- **L15.** [verify] and [counsel] items may be wrong. The jurisdiction register exists because of this.
- **L16.** It does not replace entertainment.
- **L17.** It is a home for existing groups, not yet a door for the isolated person.
- **L18.** The only running mind is a server-side Python agent; the platform's on-device guide does not exist.
- **L19.** Supporter giving has an external ceiling (about 0.2% of MAU).
- **L20.** Convergence is not validation.
- **L21.** Legal facts decay.
- **L22.** Structural ignorance.
- **L23.** Host-app webviews.
- **L24.** The payer's incentive.
- **L25.** The evidence is single-family. Every design phase, the build and drafting rounds, and every judge were Claude models.
- **L26. The legal text is an AI draft.**
  - 256 clauses plus Annex C, in two drafting rounds, reviewed by no lawyer.
  - The credential list can still be reached by compelled process against whatever the operator holds, and perhaps by a director's statutory §220(d) right (RT19).
  - Statutes were read only through search summaries, because the primary sites were blocked.
  - "Unamendable" rests on mirrored prohibitions, not a statutory category.
  - Several load-bearing clauses rest on untested theories: binding a board to a non-director's Determination, **conditioning a board on a non-member's approval (the Council pass-through)**, disapplying §276 and §228, custody under §541(d), the payer-direct reserve surviving recharacterisation.


---

## Part 3. What remains is real-world work

### 3.1 The real-world gates (none can be resolved on paper)

1. **Money (K11).** Signed non-controlling commitments of about $2.3M by the Gate Deadline (M3, extendable once by 3 months), examined by an accountant and open to challenge by either enforcer. Otherwise Commons mode, published.
2. **Counsel (K7, K9).**
   - Answers to Part VIII Q1–Q23 of `CHARTER-DRAFT.md` v2 on the official statute text. That covers:
     - the trust: §3342 opt-out; §3541 contrary provision; §3556 after HB 103; §3338;
     - the board: §141(a) for the interpretive veto **and for the Council pass-through** (Q5, Q8: can a certificate condition the board on a non-member's approval, and is the deed's duty to elect the Council's nominees enforceable?); §223 and removal;
     - dissolution and amendment: §276/§228; practical unamendability;
     - membership: Class C and §220/§114 (Annex C's condition (b)); a director's §220(d) right;
     - money and bankruptcy: the payer-direct reserve and §548; §363(b)(1) wording; §541(d) custody; §363(d)(1)/§541(f); deletion and filing; §365(c)(1) in the likely circuit; §303(a);
     - tax and regulators: 501(c)(3) status with a §3556 sole member; commerciality and *Yorba*; AG cy pres;
     - privacy: P-PLAIN enforceability; guests under §101(41A); FTC §5.
   - Structure A or B.
   - An IRS determination by M18.
   - **Open governance questions for counsel (not decided on paper):**
     - **OQ-1.** Whether T-8.4(e)'s carve-out ("an act that a Protected Provision or an Entrenched Clause requires") covers a release that ends a breach of E11 or E12. And whether, before formation, counsel advises a narrower security-release carve-out that a quiet reversal could not use. Adopting one would be a new decision, taken with counsel, in the instruments as first filed.
     - **OQ-2.** Whether the credential issuance record should be kept after issuance beyond a one-way anti-duplication check (see gate 8). This is a question for counsel and the crypto auditor together, because the answer sets how much compelled process can reach (the RT19 residual).
     - **Annex C.** Only if counsel makes both of CC-1's findings, and only in the instruments as first filed.
3. **Name clearance** in classes 9, 42 and 45 ("Stoke", "The Commons" and "Porchlight" all fail).
4. **The organizer pilot:** 40 organizers in the three segments over 12 weeks (H1b, H1c, H1d, H3, H14; K1′). Then H4 with a waitlist control, which is the thesis test. Then H2, H5 and H13.
5. **Institutions:** letters of intent (L13; H5c at M18).
6. **A real-model mind (K8, H12):**
   - an independently authored battery of at least 500 held-out cases, plus 100 benign and 200 injection cases, run on the exact shipped model;
   - builder pre-registration;
   - live provider paths;
   - a semantic guard;
   - semantic retrieval.
7. **Real trust roots (K12):** WebAuthn or passkeys; an external transparency log (closes R2); release-key signatures; user-held keys on the device (MC6, MC7).
8. **Security:**
   - an independent crypto audit before v1, **including the blind-token credential scheme and OQ-2**;
   - VM-grade isolation before any user code runs;
   - the H7 canary red team;
   - reproducible builds and a verifier.
9. **Jurisdiction:** the UK OSA illegal-harms assessment before any UK account; the EU Chat Control tripwire; geoblocking where every user must be age-verified; the quarterly jurisdiction register.
10. **External review** (recommended, not a gate): a non-Claude and human review of the design and the charter (L25). Every phase, round and judge so far was one model family.

### 3.2 Why another paper round cannot meaningfully improve this

Five paper rounds have converged: three full runs, a build round and a drafting round in v4, and this governance redraft. **Their substantive changes fell from "the wedge changed", to 19, to 2, to 0.** The last two rounds changed only how decided things are written down. What the design still does not know is not on paper. Will organizers keep using a standing link after the novelty fades? Can a real model hold the loyalty gate on a battery its builder never saw? The build round already showed that more text-matching rules add nothing on held-out attacks (17/32, twice, with the same misses). Will anyone sign $2.3M of non-controlling money? Will a Delaware court, a bankruptcy judge and the IRS read AI-drafted, lawyer-unreviewed instruments as written? The drafting rounds turned every remaining legal risk into a numbered question for counsel (Part VIII, OQ-1 and OQ-2), and a judge that shares the drafter's model family cannot answer them. Another paper round would re-argue settled choices, or pile clauses onto questions only counsel, a pilot or a real model can close. Either way it would add length, not truth. **The loop ends here.** The next step is gate 1 (the money), gate 2 (counsel) and gate 4 (the pilot), in that order. H4 decides whether any of it was worth building.

*Principles to be tested in practice, not claims that the work is finished.*
