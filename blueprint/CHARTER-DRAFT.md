# CHARTER DRAFT: the instruments that implement BLUEPRINT v3 §c.3

---

> ## NOT LEGAL ADVICE — DRAFT FOR COUNSEL REVIEW
>
> This is a working draft written by an AI drafter in a design tournament. **No lawyer wrote or reviewed it.** Every clause, citation and conclusion needs review by qualified counsel before anyone relies on it: Delaware trusts, Delaware nonstock corporations, US federal tax-exempt organisations, US bankruptcy, and US federal and state privacy law. Statutes were checked by web search on 2026-09-25, through search-engine summaries of Justia, Cornell LII, FindLaw, legis.delaware.gov and practitioner notes. **The primary code sites (delcode.delaware.gov, law.justia.com) were blocked by this session's network policy, so no statute was read in its official text.** Counsel must pull the current official text of every section cited. Items marked **[verify]** rest on recall or on a summary. Items marked **[counsel]** are judgments only a lawyer can make.

---

*Drafting round after Run 3. Source of truth: `blueprint/BLUEPRINT-v3.md` §c.3 (charter), §c.4 (start gate and modes), §c.5 (prevention table) and §c.2.4 (architecture rules that v3 entrenches). Background: `run-1/run-1-design-final.md` b.6, `run-2/run-2-design-final.md` §4, `run-3/run-3-operational.md` (a), `run-3/run-3-design-final.md` §9. Date: 2026-09-25. Where these instruments and the covenant conflict, the covenant wins (v3 c.0).*

## 0. How to read this

### 0.1 The instruments

| Part | Instrument | Clause prefix | Implements (v3) |
|---|---|---|---|
| **D** | Schedule D: Common Definitions, attached **word for word** to every instrument below | D- | cl. 1, 2, 10a–c, 11, 12 ("read by function") |
| **I** | Trust Agreement of the [●] Stewardship Trust: a Delaware noncharitable purpose trust, 12 Del. C. §3556, directed under §3313 | T- | c.3 Structure A: the trust, the TSC, the enforcer, the locks, plan D |
| **II** | Operator: Certificate of Incorporation of [OPERATOR], Inc. (Delaware nonstock; 501(c)(3) applicant) | C- | Entrenched clauses 1–12, the five locks, the ratchet, interpretation |
| **II-B** | Operator: Protected Bylaw provisions | B- | People's power, notice, audits, gift caps |
| **III** | Veto Foundation: the provisions its own certificate must contain | V- | The enforcer's independence, the IP, succession |
| **IV** | Member Privacy Covenant (the protected part of the privacy policy) | P- | cl. 9b; the anti-transfer clause under 11 U.S.C. §363(b)(1) |
| **V** | Joint Resolution on the Start Gate, Commons Mode and Operating Modes | S- | c.4 items 1–6; the modes table; K11 |
| **VI** | Mandatory terms of ancillary instruments (IP licence, enforcement agreement, escrow, gifts, debt, processors, institutions) | A- | cl. 7b, 9, 9a; the reserve; the §365(c)(1) licence |
| Annex B | What changes under Structure B (the PBC fallback) | — | c.3 "Fallbacks" |
| **VII** | Red team: 18 quiet-reversal scenarios run against this text | — | c.3 "Honesty"; K7 |
| **VIII** | Questions only counsel can answer | — | K7, K9, L3, L15 |
| **IX** | Sources | — | — |

### 0.2 Conventions

- Every clause is numbered in bold (for example **T-6.1**). Directly under it, a one-line comment starting with **↳** maps it to:
  - the v3 clause (for example "v3 cl. 9b" or "v3 c.3 Five locks");
  - the prevention-table row ("Row 21");
  - the dossier pattern or quiet-reversal route it blocks.
- "Row N" means the row of the v3 §c.5 prevention table. "QR" means a quiet-reversal route named by a red team (Run 1 X12–X17, Run 2 A8, Run 3 QR1–QR3).
- `[●]` is a blank to fill. **[drafting choice]** marks a point where v3 is silent and the drafter chose; each one is listed in Part VIII.
- **RT-fix** marks text added or changed because the red team in Part VII found a gap.
- In the legal text, "shall" imposes a duty, "may" grants a power, and "shall not" is a prohibition. An act done in breach of a "shall not" is void, not merely a breach (T-15.2, C-15.2).

### 0.3 What drafting found that v3 does not say (all closed in the text)

These are gaps or sharper points that surfaced while turning v3 into clauses. Each is closed in the text; the red team in Part VII tests the fixes.

| # | Finding | Source | Closed by |
|---|---|---|---|
| **G1** | **Modification by consent (12 Del. C. §3342)** lets an irrevocable trust be modified by written consent or non-objection of the trustor, all fiduciaries and all beneficiaries, **"regardless of whether the modification may violate a material purpose."** It applies unless the instrument **expressly** says it may not be modified under that section. §3541 lists §3342 as one of the two routes by which a purpose trust's purpose may be altered. **v3 names §3528, §3338 and situs, but not §3342.** While the founder lives, the founder, the trustee, the TSC and the enforcer together could rewrite the deed. | Search summaries of §3342 and §3541 | T-9.3 (express opt-out), T-13.3 |
| **G2** | **Delaware's Trust Act 2025 (HB 103, signed 2025-08-21)** makes a purpose trust's enforcer (i) a fiduciary unless the instrument says otherwise, (ii) an "interested person" for §3338 nonjudicial settlements, and (iii) a required consenting party for §3342 modifications. It also lets the instrument give the enforcer **exclusive** standing. So capturing the enforcer now opens settlement and modification routes, and exclusive standing would make the enforcer a single point of failure. | Search summaries of HB 103 | T-7.2, T-7.3 (no exclusive standing), T-9.2, T-9.3 |
| **G3** | **Dissolution by written consent (8 Del. C. §276).** Members of a nonstock corporation who are entitled to vote on dissolution can dissolve it **without action of the governing body** if all of them consent in writing. With the trust as sole voting member, the trust alone could dissolve the operator. | Search summary of §276 | C-5.5, C-9.7 |
| **G4** | **A merger is the friendly acquirer's route.** 8 Del. C. §255 lets a nonstock corporation merge *into* a charitable nonstock corporation, and a merger is not a "sale of assets". v3 names merger among the five-lock matters, but not the routes around a merger: a management agreement, member substitution, or an "affiliation" that confers board-appointment rights. | Search summary of §255 | C-9.1(c)–(f), T-3.3 |
| **G5** | **§363(b)(1) protects less than v3 assumes.** (i) It covers only "personally identifiable information" as **11 U.S.C. §101(41A)** defines it: name, residential address, email address, residential phone, SSN or credit-card number, given for personal, family or household purposes, plus birth data linked to those. Aggregates, metadata, ciphertext, keys and organisations' data fall outside it. (ii) It covers only a policy against transfer "to persons that are not affiliated with the debtor". (iii) It protects only the policy **in effect on the date the case commences.** | Search summaries of §363(b)(1), §101(41A) | P-6, P-7, D-3, E7b, C-11.4; the custody structure (P-6.5, §541(d)) as a second route |
| **G6** | **The enforcement reserve can be clawed back.** v3 funds the escrow with "2% of inflows". If the operator pays that out of its own receipts while insolvent, the payment is a transfer of the debtor's property, avoidable under §548 (2 years) or under state law through §544(b) (longer). | Search summary of §548 | A-3 (a donor-direct designation: the 2% never becomes operator property) |
| **G7** | **"Delete on insolvency" cannot wait for the filing.** Once a case commences, data is estate property "notwithstanding any provision … conditioned on the insolvency" (§541(c)(1)), and destroying it needs the court's authority. v3's solvent wind-down must therefore **finish deletion before any petition**. After a petition, the operator can only ask. | Search summary of §541(c)(1) | S-8.4, C-11.2, P-6.6 |
| **G8** | **The successor-steward exception is a §363(b)(1)(A) door.** A sale "consistent with" a policy that allows transfer to a successor steward needs no ombudsman. A shell with an identical deed could buy the data. | 23andMe (2025) logic, applied | D-22 (strict test), P-6.2(d) (no consideration; affirmative per-person opt-in; silence means deletion) |
| **G9** | **"Unamendable" has no statutory form in the DGCL.** §242 always allows an amendment by the votes the certificate requires. v3's unamendable clause 11 and plan D can be made practically unamendable only by mirroring the prohibition across three instruments, so that the required votes can never lawfully be given. | Search summary of §242(b)(3) | C-9.5, T-6.1(b), V-3.1 |
| **G10** | **A charter provision that blocks a bankruptcy filing is fragile.** *Franchise Services* (5th Cir. 2018) enforced a filing-consent right held by a bona fide equity holder, but courts have treated other blocking provisions as void. So this draft **conditions** a voluntary filing and does not block it. It relies on **§303(a)**: no *involuntary* case lies against "a corporation that is not a moneyed, business, or commercial corporation", which covers a nonprofit operator (Structure A only). | Search summaries | C-11.1–C-11.3 |
| **G11** | **Structure A has a bankruptcy advantage v3 does not claim.** §363(d)(1), §541(f) and §1129(a)(16) (added by BAPCPA in 2005) require that a nonprofit debtor transfer property only as nonbankruptcy law governing nonprofit transfers allows. The charter's charitable restrictions and the attorney general's oversight therefore follow the data and assets into a bankruptcy. **This is lost under Structure B.** | Search summaries | C-11.4; Annex B |

---

## PART D — SCHEDULE D: COMMON DEFINITIONS

*Attached word for word to the Trust Agreement (I), the Certificate (II), the Veto Foundation provisions (III), the Privacy Covenant (IV), the Resolution (V) and every ancillary instrument (VI). A defined term has the same meaning in every instrument. If two copies ever differ, the reading more protective of Members and Guests governs (D-0.4).*

**D-0.1 Function over form.** Every term in this Schedule, and every prohibition that uses one, is read by what a thing **does**, not by what it is called, how it is built, where it runs, or whether it is enabled, gated, experimental, temporary, regional, consented or offered to only some people. Renaming, relabelling, re-architecting, splitting a thing into parts, moving it to a contractor, a subsidiary, a processor or code the Operator serves to a device, or making it "opt-in" or "opt-out", does not take it outside a definition.
↳ v3 c.3 "read by function, not by name" · Rows 1, 2, 24 · blocks QR2 (reinterpretation: "re-engagement is care"; "relevance is search") and Run 1 X17 (undefined words)

**D-0.2 "Including" and lists.** "Including" means "including without limitation". A list in a definition is illustrative, except where the text says "only" or "exclusively". In that case the list is closed.
↳ v3 cl. 1, 2, 12 · Rows 2, 18 · blocks narrowing by listing ("it isn't one of the listed things")

**D-0.3 Future technology.** A definition covers technology, methods and business models that do not exist at the date of adoption, if they perform the function the definition describes.
↳ v3 c.0 cut 3 (a quiet reversal must be impossible) · Rows 1, 19 · blocks "this is new, so the old rule doesn't cover it"

**D-0.4 Doubt.** Where an act can reasonably be read as either inside or outside a prohibition, it is inside. Where a change can reasonably be read as either a Weakening Change or a Ratchet Change, it is a Weakening Change.
↳ v3 c.3 Interpretation; one-way ratchet · Rows 7, 13 · blocks Run 1 X12 (laundering a reversal through the ratchet)

**D-1 "Advertising"** means any placement, prominence, ordering, inclusion, exclusion, grouping, badge, label, visual treatment, **attribution line**, notification, message or editorial selection, on any surface of the Service or in any communication from the Operator to any person, that is influenced, in whole or in part, directly or indirectly, by any payment, gift, grant, discount, in-kind benefit, promise of any of these, or other consideration, or by any Commercial Relationship. It includes "sponsored", "featured", "promoted", "partner", "verified" or "recommended" treatments, and any treatment given to a payer that is withheld from a non-payer. It does not include:
- (a) a Member's own Content about the Member's own activities (a bakery's card for its own event), provided no payment affects how any surface orders, shows or reaches it; or
- (b) the single Supporters Page described in E1.3.

↳ v3 cl. 1 · Rows 2, 18 · blocks surveillance and paid-prominence advertising, Run 1 X17 ("featured community partners", "Stoke Picks"), and paid attribution

**D-2 "Commercial Relationship"** means any actual or proposed contract, grant, gift, loan, licence, sponsorship, employment, consultancy, service arrangement or other dealing under which value passes, or may pass, between the Operator (or any Related Party of the Operator) and any person, other than a Member's gift or paperwork fee that confers nothing any other person lacks (E4, E5).
↳ v3 cl. 1, 7a · Rows 2, 6 · blocks "it isn't payment, it's a partnership"

**D-3 "Data"** means any information, in any form or medium, that the Operator (or anyone acting for it) obtains, observes, receives, derives, infers, computes, generates or holds from or about the Service, or about any person's use of it or presence in it. It includes:
- (a) Personal Information;
- (b) Content;
- (c) Metadata;
- (d) Aggregates;
- (e) de-identified, pseudonymised, anonymised, synthetic, sampled or statistical information;
- (f) any model, weight, embedding, parameter, rule, list, index or classifier trained, tuned, fitted or evaluated on any of (a) to (e);
- (g) ciphertext, key material, key identifiers and access credentials;
- (h) information about organisations, groups and circles, as well as about individuals.

**Aggregates and metadata are Data.** Nothing ceases to be Data because it is aggregated, transformed, encrypted or anonymised.
↳ v3 cl. 2 ("aggregated, de-identified, statistical, derived and metadata") · Rows 2, 21 · blocks Run 1 X1 ("Community Insights": aggregates aren't "personal data") and the G5 gap (§101(41A) covers only a narrow PII list)

**D-3.1 "Personal Information"** means Data that identifies, relates to, describes, or is reasonably capable of being associated with, a particular individual or device, **directly or by combination with other information**. It includes every category listed in 11 U.S.C. §101(41A), whether or not the individual obtained a product or service "primarily for personal, family, or household purposes". It also includes display names, re-entry codes, host keys, DIDs, IP addresses, reminder contacts, billing identifiers, and the fact of a person's membership in, or response to, any card or circle.
↳ v3 cl. 9b · Row 21 · blocks the G5 gap (organisations' organisers and non-household uses fall outside §101(41A))

**D-4 "Aggregate"** means Data describing more than one person, or a group, circle, place or time, including any count, rate, sum, distribution, trend, ranking, heat map or statistic, however computed. It includes figures computed by secure aggregation (DAP/Prio-style), differential privacy or k-anonymity.
↳ v3 cl. 2; c.2.4 item 11 · Rows 1, 2 · blocks "Civic Insights" (Run 1 X1)

**D-5 "Metadata"** means Data about Content or about a person's use of the Service, other than the Content itself. It includes timing, frequency, size, sender, recipient, membership, network address, device, location, the fact of a response, and the graph of who is connected to whom.
↳ v3 cl. 2; L7 · Rows 2, 17 · blocks the sale of the social graph without the content

**D-6 "Content"** means anything a person authors, uploads, types, selects or sends through the Service, including cards, responses, notes, plans, shelf items, circle text, links, names entered for others, and anything derived from them. **"Member or Guest Content"** means Content authored by any Member or Guest, whether or not that person holds an account.
↳ v3 cl. 12 · Rows 2, 19 · blocks the argument that guests, who never consented, have no protected content (Run 3 CV1)

**D-7 "Plaintext"** means any representation of Content from which the Operator, or any person acting for or with it, can recover, read or infer the Content or any part, feature or property of it, other than its approximate size and time of transmission, **without a key held only on a Member's or Guest's own device**. It includes:
- (a) decrypted, transcoded, rendered, summarised, translated, indexed or embedded forms;
- (b) hashes, fingerprints or signatures computed for matching or classification (perceptual or exact);
- (c) extracted features;
- (d) ciphertext whose key the Operator holds, escrows, can derive, can brute-force with ordinary means, or can obtain on request, including from code it serves.

↳ v3 cl. 12 (P-PLAIN) · Rows 2, 19, 22 · blocks QR1 (E2EE reversed through a server-side helper) and Run 3 LK3 (a weak key tier that is plaintext in disguise)

**D-8 "Operator"** means [OPERATOR], Inc. and every person it controls, is controlled by or is under common control with, including any subsidiary, affiliate, joint venture, special-purpose vehicle, successor, assignee and receiver. When the Operator acts through an officer, employee, contractor, processor, model provider or code it serves to any device, that act is the Operator's act.
↳ v3 cl. 7b · Rows 1, 21 · blocks moving a prohibited act into a subsidiary, contractor or client script (RT9)

**D-9 "Hold, process or transmit"** includes storing, caching, logging, computing on, routing, forwarding, displaying, or causing any device or third party to do any of these. **Code the Operator serves or signs that sends Plaintext off the device where it was decrypted**, other than to a person the user addressed, is the Operator transmitting Plaintext.
↳ v3 cl. 12; c.2.4 item 3 · Rows 19, 25 · blocks client-side exfiltration and "the helper runs in your browser, then calls our API"

**D-10 "Order"** (and "Ordering") means to rank, sort, score, filter, select, include, exclude, target, recommend, suggest, highlight, group, sequence, delay, expire, or decide what is shown to, sent to or hidden from, a person.
↳ v3 cl. 10b · Rows 1, 9, 16 · blocks Run 2 A8.1 ("search needs an ordering function"; "Popular near you")

**D-11 "Notification"** means any message, alert, badge, count, sound, vibration, email, SMS, push, digest, banner, interstitial, in-product prompt or calendar entry directed at a person by or through the Service, whoever composed it.
↳ v3 cl. 10a · Row 10 · blocks Run 2 A8.2 (push "on by default") and Run 2 A14 (the digest as a re-engagement channel)

**D-12 "Behavioural Measure"** means any Data about a particular person's past actions or inaction, including attendance, absence, response, responsiveness, latency, frequency, recency, time spent, inactivity, lapse, streak, "engagement", "health" or "risk" score, **however named or aggregated over time for that person.**
↳ v3 cl. 10b, 10c · Rows 1, 24 · blocks Run 3 X1 (payer-facing "member insights"; lapsed lists)

**D-13 "Transfer"** means to sell, lease, license, rent, assign, exchange, lend, pledge, grant a security interest in, give, disclose, make available, provide access to, or allow any other person to use, whether for value or not, directly or by operation of law, merger, conversion, change of control or court order.
↳ v3 cl. 2, 9, 9b · Rows 2, 21 · blocks structuring around "sale" (licence, exchange, "access")

**D-14 "Instrument"** means any equity, membership interest, share, stock, unit, option, warrant, convertible, SAFE, token, profit or revenue interest, revenue-based or royalty financing, debt, guarantee, or any other right to receive value from, or to direct or influence, the Operator. **"Debt"** includes every obligation to repay money or its equivalent, including recoverable grants, program-related investments, leases that function as financing, and supplier credit beyond 90 days.
↳ v3 cl. 9a; c.3 Five locks ("issuing any instrument") · Rows 21, 6 · blocks Run 2 A8.4 (recapitalising "without investors") and Run 2 A11.6 (buying the debt)

**D-15 "Related Party"** means any current or former (within 3 years) director, officer, trustee, Administrative Trustee officer, member of the Trust Stewardship Committee, member of the Council's election body, director or officer of the Veto Foundation or Backup Enforcer, major donor (above 5% of any year's inflow), and any **Family Member** of any of them, and any entity in which any of them, alone or together, holds an **Interest**. "Family Member" means a spouse, domestic partner, parent, child, sibling, grandparent or grandchild, or the spouse or domestic partner of any of them. "Interest" means any ownership, profit, employment, board or advisory seat, consulting or creditor position, or right to compensation.
↳ v3 cl. 7a · Row 6 · blocks Run 1 X2 (salary and contract extraction)

**D-16 "Compensation"** means all value provided for services, from any source that is connected with the Operator: salary, bonus, benefits, deferred pay, severance, allowances, loans, forgiven obligations, and payments from any Related Party or processor.
↳ v3 cl. 7 · Row 6 · blocks paying through a vendor to escape the cap

**D-17 "Free Floor Function"** means each function listed in E4, described by what it does for a person or group, whatever it is called, however it is packaged and whichever surface provides it.
↳ v3 cl. 4 · Rows 5, 6 · blocks Run 1 X4 (the toll gate) and Run 3's $20 organisation paywall

**D-18 "Capability"** means a technical or organisational means, **whether or not exercised, enabled, deployed, consented to or limited to any jurisdiction**, including code (on a server or served to a client), models, hash lists, classifiers, keys, contracts, procedures, staff roles or agreements with third parties, held in a state from which it could be put into use within 30 days.
↳ v3 cl. 11 · Rows 19, 22 · blocks "disabled by default" and "only in the EU build"

**D-19 "Weakening Change"** means any change (by amendment, waiver, interpretation, policy, code, contract, default setting or practice) that:
- (a) adds, expands or restores any Operator Capability over people or Data;
- (b) lengthens any retention period;
- (c) adds a category of Data held;
- (d) narrows any prohibition, definition or Free Floor Function;
- (e) adds a paid feature or price;
- (f) reduces any lock, notice period, vote threshold, standing, reserve or enforcement right;
- (g) adds to any exception list (including the P-PLAIN schema);
- (h) creates any Instrument, member class or affiliate;
- (i) is any other change the Veto Foundation or the Backup Enforcer determines to be weakening under T-8.

Any change not shown to be a Ratchet Change is a Weakening Change.
↳ v3 c.3 How change works; one-way ratchet · Rows 7, 13 · blocks Run 1 X12 (the "stricter child-safety" ratchet that added a scanner)

**D-20 "Ratchet Change"** means a change whose **only** effect is to (a) remove or narrow an Operator Capability, (b) shorten a retention period, or (c) delete a category of Data, and that neither adds any Capability nor adds to any exception, whatever its stated purpose (including safety, compliance or protection).
↳ v3 c.3 one-way ratchet · Rows 7, 22 · blocks Run 1 X12

**D-21 "Locked Matter"** has the meaning in C-9.1.
↳ v3 c.3 Five locks · Rows 13, 21

**D-22 "Successor Steward"** means an entity that meets **every** one of these tests:
- (a) it is a Delaware nonstock corporation recognised as exempt under IRC §501(c)(3), or another form approved under T-12.2;
- (b) its sole voting member is a Delaware purpose trust whose governing instrument is identical to this Trust Agreement in every Protected Provision;
- (c) its certificate is identical to the Operator's Articles C-3 to C-16;
- (d) it has held no Data and had no operations or Commercial Relationship with any Related Party in the prior 3 years;
- (e) it **pays no consideration, and gives no Related Party any consideration**, for any asset or Data received;
- (f) it has been approved by (i) the Veto Foundation, (ii) the Backup Enforcer and (iii) a Council vote under the five-lock thresholds, after 90 days' Public Notice.

↳ v3 cl. 9b; plan D; T-12 · Row 21 · blocks the G8 gap (a shell "successor" as a §363(b)(1)(A) door) and a friendly acquirer (RT7)

**D-23 "Functional Reading"** means reading a provision under D-0.1 to D-0.4, by its purpose stated in Schedule A, so that it reaches every act that performs the prohibited function.
↳ v3 c.3 Interpretation · Rows 1, 24 · blocks QR2

**D-24 "Non-controlling Commitment"** has the meaning in S-1.3. **"Committed Inflow"** means the sum of Non-controlling Commitments not yet received, plus cash received and unspent, measured without any growth, renewal or new-donor assumption.
↳ v3 c.4 item 1; item 3 ("committed inflow") · Row 21 · blocks the Run 3 "Front 8" death at M14 on an unoffered loan

**D-25 "Actual Burn"** means the Operator's average monthly net cash outflow over the trailing 3 full calendar months, from audited or reviewed accounts, **never a budget, plan or projection. "Runway"** means (unrestricted cash plus Committed Inflow due within 12 months) divided by Actual Burn.
↳ v3 c.3 Austerity triggers ("trailing 3-month actual burn") · Row 21 · blocks Run 1 X13 (an austerity trigger that leadership controls through the plan)

**D-26 "Credentialed Member"** has the meaning in B-1.
↳ v3 c.3 Voting credentials

**D-27 "Scanning, Classifying or Profiling"** means any automated or manual process, running anywhere (including on a person's device, before encryption or after decryption), that inspects, matches, hashes for matching, scores, categorises or makes inferences about any person, or about any Content or Metadata, for any purpose other than delivering it to the recipients its author chose. It includes client-side scanning, perceptual or exact hash matching, content classifiers, risk scores, age estimation from images or behaviour, and "local checks that report nothing". It does not include:
- (a) processing of Content a reporter chose to submit to the Operator in a report;
- (b) review of public Content that someone has reported;
- (c) a computation a person invokes on their own device over their own Data, the result of which is shown only to that person.

↳ v3 cl. 11; c.2.5 (Run 3's client-side scam detector rejected) · Rows 19, 22 · blocks Run 1 X12, QR3 and the EU CSA Regulation client-side-scanning path

**D-28 "Key Escrow"** means any Capability by which any person other than a device the user controls can obtain, recover, derive or reconstruct a key to Member or Guest Content. **"Compelled-Access Capability"** means any Capability built, held or maintained so that any government or other third party can obtain Content, Plaintext, keys, or Scanning, Classifying or Profiling results, whether or not compelled by law.
↳ v3 cl. 11 · Rows 7, 19 · blocks QR3 (a consentable backdoor)

**D-29 "Public Notice"** means publication, in plain language, of the full text of a proposal, a line-by-line diff, the reasons, and every Interpretive Determination on it:
- (a) on the Operator's public governance page;
- (b) in the transparency log;
- (c) in a notice to every Credentialed Member who has an update channel.

The notice period runs from the last of these. Any material change to the proposal restarts it.
↳ v3 c.3 lock 5 ("90 days' public notice") · Row 13 · blocks Run 2 A8.5 ("a comment period is not consent") and quiet late changes

**D-30 "Plan D"** means the disposition in T-12.3.
↳ v3 c.3 Plan D · Row 21

**D-31 "Guide"** means any software agent, model or assistant that the Operator provides, signs or recommends, that acts on or drafts for a person.
↳ v3 c.2.6 · Row 19

**D-32 "Service"** means everything the Operator provides or operates, including every card, circle, index, feed, relay, client, reference server, API, Guide and domain, and every service under the Operator's marks in any mode, including Commons Mode.
↳ v3 c.2 · all rows

---

## PART I — TRUST AGREEMENT OF THE [●] STEWARDSHIP TRUST

*A Delaware noncharitable purpose trust under 12 Del. C. §3556. It is a directed trust under 12 Del. C. §3313. It is the sole voting member (Class T) of the Operator.*

**THIS TRUST AGREEMENT** is made on [date] between [FOUNDER] (the "**Settlor**") and [DELAWARE TRUST COMPANY], a Delaware-chartered trust company with an office for the conduct of trust business in Delaware (the "**Administrative Trustee**").

### Article T-1: Establishment

**T-1.1 Creation.** The Settlor irrevocably transfers to the Administrative Trustee the property described in Schedule T-1. The Administrative Trustee accepts it, to hold, administer and apply solely for the Purpose on the terms of this Agreement. The trust so created is the "[●] Stewardship Trust" (the "**Trust**"). It is a trust for a noncharitable purpose under 12 Del. C. §3556.
↳ v3 c.3 "Purpose Trust (12 Del. C. §3556, irrevocable…)" · Rows 13, 21 · blocks "never for sale" existing only as a manifesto (operator red line: "Form"; "a manifesto binds no one; a trust deed does")

**T-1.2 Irrevocability; no reversion.** This Trust is irrevocable. The Settlor retains no power to revoke, amend, direct, appoint, remove or replace any person, or to receive any property or benefit, except as T-13.1 states for the first 18 months. If any part of the Trust fails, the property passes under T-12.6 and **never** reverts to the Settlor, the Settlor's estate or any Related Party.
↳ v3 c.3 "Founder: the settlor. Gives, receives nothing" · Row 6 · blocks founder capture and estate inclusion (Run 3 (a).1)

**T-1.3 Governing law, fixed.** The validity, construction and administration of this Trust are governed by the laws of the State of Delaware, **without regard to the place of administration from time to time**. No change in the place of administration, the residence of any fiduciary, or the location of any asset changes the governing law. This provision is stated so that 12 Del. C. §3332 cannot operate to substitute another law [verify §3332 text].
↳ v3 c.3 "prohibits … any change of situs or governing law" · Row 13 · blocks migration to a friendlier law (RT13)

**T-1.4 Duration.** The Trust continues in perpetuity until it terminates under T-12.7. The Settlor intends that no rule against perpetuities applies to it [verify: 25 Del. C. §503 as applied to personal property held in trust].
↳ v3 c.3 · Row 13 · blocks a time-out of the deed

**T-1.5 Freedom of disposition; material purposes.** The Settlor intends 12 Del. C. §3303 to give maximum effect to every term of this Agreement. **Each Protected Provision is a material purpose of the Trust** for 12 Del. C. §§3338, 3541 and 3556, and for any other statute or doctrine that turns on a trust's material purpose. "**Protected Provisions**" means Articles T-1 to T-17, Schedule A, Schedule D and Schedule T-2.
↳ v3 c.3 trust-law locks · Rows 13, 21 · blocks nonjudicial settlement "consistent with material purpose" (§3338(c)) and cy pres by drift

### Article T-2: Purpose

**T-2.1 Declared Purpose.** The Trust's purpose (the "**Purpose**") is to secure, in perpetuity, that the civic infrastructure the Operator provides, through which people find one another and gather in person, is operated only on the terms of the Covenant Commitments in Schedule A. The Trust does this by:
- (a) holding and voting the Class T Membership of the Operator;
- (b) holding and applying the Continuity Reserve;
- (c) securing enforcement of the Protected Provisions and of the Entrenched Clauses of the Operator's Certificate;
- (d) if, and only if, T-12 applies, carrying out a Fallback Disposition.

↳ v3 c.3 Structure A; c.0 thesis cuts 2–3 · Rows 13, 21 · blocks an owner whose return can rise with attention or data (thesis cut 2)

**T-2.2 Schedule A.** Schedule A reproduces, word for word, the Entrenched Clauses E1 to E12 and the Charter Obligations of Article C-12 of the Operator's Certificate as first filed, together with Schedule D. Schedule A is part of the Purpose. An amendment of the Operator's Certificate does not amend Schedule A. Schedule A changes only by a Ratchet Amendment under T-9.4.
↳ v3 c.3 "entrenched … mirrored in the trust deed" (Run 1 b.6.2) · Rows 1–25 · blocks amending the certificate while the deed still points at the old text

**T-2.3 The Purpose is attainable at any scale.** The Settlor declares that the Purpose is not impossible of attainment. It is attained by:
- the Operator's full service;
- Commons Mode (S-4);
- caretaker mode;
- publication of the open specification and reference software;
- a single Successor Steward;
- Plan D itself.

**No reduction in scale, users, revenue or funding, no loss of any market or jurisdiction, and no offer of greater funding or a purchase on other terms is impracticability, impossibility, illegality or wastefulness**, and none of them is a ground to modify the Purpose.
↳ v3 c.3 Plan D; c.4 Commons mode · Row 21 · blocks Run 1 X15 (engineered impracticability: "the purpose is impracticable without capital; permit a sale")

**T-2.4 Exclusive powers.** The Trust may do only what T-2.1 describes and what is incidental to it. Everything else is prohibited.
↳ v3 c.3 · Row 21 · blocks mission creep into holding operating or economic assets

### Article T-3: Trust property

**T-3.1 What the Trust holds.** The Trust holds only:
- (a) the Class T Membership of the Operator;
- (b) the Continuity Reserve: gifts made **directly to the Trust** by the Settlor or by third-party donors, **never property transferred by the Operator**, together with its proceeds;
- (c) cash for the Trust's own administration;
- (d) rights under the instruments in Part VI to which the Trust is a party.

↳ v3 c.3 "continuity reserve … gifted directly to the trust so it is never operator property (§548 clawback)" · Row 21 · blocks a trustee in bankruptcy clawing back the reserve (G6)

**T-3.2 What the Trust shall never hold.** The Trust shall not acquire, receive, hold or control any:
- Data;
- operating asset of the Service;
- mark, domain or copyright (these are the Veto Foundation's, V-5);
- equity or other Instrument of any entity other than the Class T Membership (and an equivalent membership in a Successor Steward);
- Debt, as borrower, lender or guarantor.

If any such thing comes into its possession, the Trust shall return it to its source or delete it within 30 days and Publish the fact.
↳ v3 c.3; Run 3 (a).5 ("the trust is also a creditor-free entity") · Rows 2, 21 · blocks the Trust becoming a data vault or a creditor target

**T-3.3 The Class T Membership is inalienable.** No one shall sell, Transfer, pledge, lend, encumber, split, or grant any proxy, voting agreement or option over, the Class T Membership or any right in it. The only exception is its transfer to the purpose trust of a Successor Steward as part of a Fallback Disposition under T-12. Any purported Transfer is void.
↳ v3 c.3 "sole voting member"; Run 3 (a).3 "Sell the company" · Row 21 · blocks member substitution by a friendly acquirer (RT7)

**T-3.4 No beneficial interest.** No person has any beneficial interest in the Trust or its property. No interest in the Trust can be reached by any creditor of any person, and no person can assign one.
↳ v3 c.3 · Row 21 · blocks creditors of any fiduciary reaching the Trust

### Article T-4: The Administrative Trustee

**T-4.1 Qualification and place of administration.** The Administrative Trustee, and every successor, shall at all times be a corporation or other entity authorised to act as a trustee in Delaware, with an office for the conduct of trust business in Delaware. The Trust shall at all times be administered in Delaware within the meaning of 12 Del. C. §3340. No individual and no entity without a Delaware trust office may serve.
↳ v3 c.3 "no change of situs" · Row 13 · blocks migration by appointing a trustee elsewhere (RT13)

**T-4.2 Directed trustee.** The Administrative Trustee shall act on the written directions of the Trust Stewardship Committee (the "**Committee**"). The Committee is an adviser under 12 Del. C. §3313. So far as the law allows, the Administrative Trustee is an excluded fiduciary for every matter within the Committee's authority [verify: interplay of §3313 and §3313A]. The Administrative Trustee has no duty to monitor the Committee's directions, **except** as T-4.3 requires.
↳ v3 c.3 "directed under §3313, with a Trust Stewardship Committee" · Row 13 · blocks nothing by itself; it allocates who decides

**T-4.3 Prohibited Directions are void.** A direction to vote for, consent to, or do anything that T-6.1 or T-10 prohibits is a "**Prohibited Direction**". It is void. The Administrative Trustee **shall not follow it**, shall notify the Veto Foundation and the Backup Enforcer within 2 business days, and shall Publish the fact within 5 business days. The Settlor intends that following a Prohibited Direction is willful misconduct, which §3313 does not excuse [counsel: confirm §3313 protection falls away].
↳ v3 c.3 "the deed forbids voting for weakening changes" · Rows 13, 21 · blocks a captured Committee instructing the trustee to vote "yes" (RT3, RT7)

**T-4.4 Succession of the Administrative Trustee.** The Administrative Trustee may resign on 90 days' notice. A successor is appointed by the Committee with the written consent of the Veto Foundation, or failing that, by the Court of Chancery on the petition of the Veto Foundation or the Backup Enforcer. A resignation takes effect only when a qualified successor accepts. **The Settlor, the Operator, and any director, officer or donor of the Operator may never appoint the Administrative Trustee.**
↳ v3 c.3 successor rule ("never by the trustees", applied here to the Operator) · Rows 13, 6 · blocks the Operator choosing its own supervisor

**T-4.5 Fees.** The Administrative Trustee's fee schedule is Published. No fee may depend on any metric of the Service.
↳ v3 cl. 7 · Row 6 · blocks incentive pay for the trustee

### Article T-5: The Trust Stewardship Committee

**T-5.1 Composition.** The Committee has 5 seats:
- (a) **two** seats elected by the Council under B-1 and B-2;
- (b) **one** seat appointed by [NAMED INDEPENDENT DIGITAL-RIGHTS INSTITUTION], or by its successor named under T-5.9;
- (c) **one** seat appointed by [NAMED INDEPENDENT PUBLIC-LIBRARY OR CIVIC INSTITUTION] [drafting choice];
- (d) **one** seat filled by lot from Credentialed Members who volunteer and pass the conflict screen in T-5.2 [drafting choice].

**The Veto Foundation appoints no seat.** Until month 18 after the date of this Agreement, the Settlor may fill seats (b) to (d) on an interim basis, and the Settlor's power ends at month 18 whether or not it has been exercised.
↳ v3 c.3 "council holds 2 of 5 TSC seats"; "every appointment power the founder holds ends at month 18"; Run 1 b.6.3 deconcentration · Rows 6, 13 · blocks one body (the Veto Foundation) delivering both a lock and a vote inside the trust (Run 1 X14)

**T-5.2 Who may not serve.** None of the following may serve on the Committee:
- any director, officer, employee or contractor of the Operator, or anyone who was one within 3 years;
- any director or officer of the Veto Foundation or Backup Enforcer;
- any donor, lender or institution counterparty of the Operator above 1% of a year's inflow;
- any Family Member of any of these;
- any person with an Interest in a Commercial Relationship of the Operator.

↳ v3 cl. 7a · Row 6 · blocks capture through overlapping seats

**T-5.3 Terms.** Terms are 3 years, staggered so that no more than 2 seats turn over in any year, with at most 2 terms per person. The Council-elected seats are staggered by 18 months relative to the Council-elected seats of the Veto Foundation (V-2.2).
↳ v3 c.3 "staggered by 18 months" · Row 6 · blocks a single election cycle capturing both the trust and the enforcer (Run 1 X35)

**T-5.4 Powers.** Subject to T-6 and T-10, the Committee directs the Administrative Trustee:
- (a) to cast the Class T votes, including the election of 3 of the Operator's 5 directors;
- (b) to give or withhold Class T approval on Locked Matters;
- (c) to appoint the Trust's auditors;
- (d) to apply the Continuity Reserve under T-11.3;
- (e) to act under T-12.

↳ v3 c.3 "elects 3 of 5 directors" · Row 13

**T-5.5 Fiduciary capacity; standard.** Committee members act in a fiduciary capacity under §3313, **solely for the Purpose**. They owe no duty to the Operator, any donor, any creditor or any member of the public as such. No member is liable except for bad faith, willful misconduct, or a knowing breach of a Protected Provision. The Trust (not the Operator) indemnifies them.
↳ v3 c.3 · Row 13 · blocks "duty to the enterprise's survival" arguments for a sale

**T-5.6 Removal.** A Committee member may be removed only:
- (a) by the body that appointed or elected them, for the seats in T-5.1(a) to (c); or
- (b) by the Court of Chancery for cause, on the petition of the Veto Foundation, the Backup Enforcer or Council Petitioners.

**No Committee member may be removed by the other members, by the Administrative Trustee, by the Operator or by the Settlor.**
↳ v3 c.3 · Rows 6, 13 · blocks purging the dissenting steward

**T-5.7 Voting.** A quorum is 4 members. Ordinary directions need 3 votes. **A Ratchet Amendment (T-9.4) and a certification under T-6.2 each need 4 of 5.** Votes and reasons are Published within 10 business days.
↳ v3 c.3 lighter track ("4/5 of the TSC") · Row 13

**T-5.8 Stipend.** Members may receive a Published stipend of no more than $[●] a year (2026 dollars, CPI-indexed), and nothing else.
↳ v3 cl. 7 · Row 6

**T-5.9 Succession of appointing institutions.** If an institution named in T-5.1(b) or (c) ceases to exist or declines to act for 180 days, the Backup Enforcer names a successor institution from a Published list of at least three with no Related-Party ties to the Operator, and a Council vote confirms it. **The Committee, the Administrative Trustee and the Operator never choose it.**
↳ v3 c.3 "successors … chosen by election or by a named independent body, never by the trustees" · Row 6 · blocks Run 2 A15 (the enforcer "appointed by the people it is meant to police")

### Article T-6: Mandatory voting rules (the trust's lock)

**T-6.1 Prohibited votes.** The Committee shall not direct, and the Administrative Trustee shall not cast, any vote, consent, waiver, approval or non-objection of the Class T Membership in favour of:
- (a) any Weakening Change to any Entrenched Clause, Charter Obligation, Protected Bylaw, the Privacy Covenant's protected part, or Schedule D;
- (b) **any amendment, waiver or suspension of an Unamendable Provision (C-9.5), whatever its terms**;
- (c) any merger, consolidation, conversion (including into any stock, benefit or for-profit form), sale, lease, exchange or licence of any Material Asset, dissolution, or admission of any member or class, **other than** a Fallback Disposition under T-12;
- (d) the creation of any Instrument, subsidiary or affiliate that E7b forbids;
- (e) any Debt that fails E9a;
- (f) the election of any director who has not signed the Director Covenant (B-16).

Any such vote is void and is a breach of trust.
↳ v3 c.3 lock 2 ("the trust's vote (the deed forbids voting for weakening changes)") · Rows 13, 21 · blocks the OpenAI path (a board plus a regulator) and a friendly merger (RT6, RT7)

**T-6.2 Default "no".** On every Locked Matter, the Trust votes **against**. The only exception is where, before the vote, (i) 4 of 5 Committee members certify in writing, with Published reasons, that the matter is a Ratchet Change or a Fallback Disposition, and (ii) neither the Veto Foundation nor the Backup Enforcer has issued an Interpretive Determination to the contrary within 30 days of that certification.
↳ v3 c.3 Interpretation; one-way ratchet · Rows 7, 13 · blocks a reversal passed by abstention or by an ambiguous proposal

**T-6.3 No written consent; after notice only.** The Trust acts on a Locked Matter only at a meeting of the Operator's members held **after** the 90-day Public Notice period has ended. It never acts by written consent in lieu of a meeting.
↳ v3 c.3 lock 5 · Row 13 · blocks a same-day written-consent reversal (G3)

**T-6.4 Director elections.** The Committee directs votes only for candidates who have signed the Director Covenant and who meet B-16's conflict tests. It Publishes its reasons for each nomination.
↳ v3 c.3; c.4 item 1 ("a charter obligation of the board") · Rows 6, 13

### Article T-7: The Enforcer and the Backup Enforcer

**T-7.1 Appointment.** Under 12 Del. C. §3556 and §3303, the Settlor appoints [VETO FOUNDATION], a Delaware nonstock corporation, as enforcer of this Trust (the "**Enforcer**"). The Settlor also appoints [NAMED LAW-SCHOOL CLINIC], with its written consent, as backup enforcer (the "**Backup Enforcer**"). Each accepts by signing Schedule T-3, and by accepting, submits to the personal jurisdiction of the Delaware courts [verify: HB 103 (2025)].
↳ v3 c.3 "Veto Foundation … is the trust's named enforcer"; "Backup enforcer: a named law-school clinic" · Rows 7, 13 · blocks a trust that nobody can enforce

**T-7.2 Capacity.** The Enforcer and the Backup Enforcer each act **as fiduciaries, solely for the Purpose**, when exercising any power under this Agreement (12 Del. C. §3301(d) as amended in 2025 [verify]). A **failure to enforce, when a reasonable enforcer applying the Functional Reading would enforce, is a breach**, and it is a ground for removal under T-7.7. Neither is liable except for bad faith or willful misconduct.
↳ v3 c.3 · Row 7 · blocks a captured enforcer's inaction being lawful (RT3) [drafting choice: fiduciary rather than non-fiduciary]

**T-7.3 Standing is shared, never exclusive.** The Enforcer, the Backup Enforcer, each Committee member, and Council Petitioners (1% of Credentialed Members under B-3) **each** have standing to enforce this Agreement. **No person has exclusive standing**, and the Settlor deliberately does not use the power to confer exclusive standing that §3556 (as amended in 2025) allows [verify].
↳ v3 c.3 backup enforcer; Run 2 §4 (a member-appointed enforcer) · Rows 7, 13 · blocks a single captured enforcer ending all enforcement (G2, RT3)

**T-7.4 Backup Enforcer's trigger.** The Backup Enforcer may act, and may draw on the Enforcement Reserve (A-3), in any of these cases:
- (a) 90 days after a written demand to the Enforcer by 100 Credentialed Members, if the Enforcer has not filed or issued a Determination;
- (b) the Enforcer has a conflict;
- (c) the Enforcer is the subject of a petition under T-7.7;
- (d) **at any time, to issue an Interpretive Determination under T-8.6.**

↳ v3 c.3 "It can act if the Veto Foundation does not act within 90 days of a demand by 100 credentialed members" · Row 7 · blocks enforcer paralysis (Run 1 X14)

**T-7.5 Necessary parties.** Any petition to any court to modify, reform, terminate, construe so as to change the effect of, or divide this Trust, or to apply §3541, shall name the Enforcer, the Backup Enforcer and the Committee as necessary parties. It shall be Published at least 90 days before any hearing on the merits. The Settlor directs the Enforcer and the Backup Enforcer to oppose any such petition that is not a Fallback Disposition.
↳ v3 c.3 "narrows Chancery's §3541 modification power"; Run 3 (a).3 ("the enforcer must consent to any court petition") · Row 21 · blocks an unopposed quiet petition (RT4)

**T-7.6 Succession.** Vacancies on the Enforcer's board are filled under its own certificate (V-2). If the Enforcer ceases to exist, resigns, or fails to act for 180 days, a successor enforcer is appointed by the Court of Chancery on the Backup Enforcer's petition, from nominees of the independent bodies named in V-2.1(b). **The Administrative Trustee, the Committee, the Settlor and the Operator never nominate or appoint an enforcer.**
↳ v3 c.3 "Successors … never by the trustees" · Row 6 · blocks Run 2 A8.5 and A15 (protector capture)

**T-7.7 Removal.** The Enforcer or Backup Enforcer may be removed only by the Court of Chancery, for bad faith, willful misconduct, persistent failure to act, or incapacity, on the petition of the other enforcer, a Committee member or Council Petitioners. **A pending removal petition does not suspend any Interpretive Determination already issued.**
↳ v3 c.3 · Rows 6, 7 · blocks removing the enforcer to clear the path

**T-7.8 No consent to modification.** The Enforcer and Backup Enforcer have **no power** to consent to, join or not object to any nonjudicial settlement agreement or modification under 12 Del. C. §3338 or §3342 affecting a Protected Provision. Any purported consent is void. **RT-fix.**
↳ v3 c.3 trust-law locks · Row 13 · blocks G2 (HB 103 made the enforcer the consenting party for those routes)

**T-7.9 Funding.** The Enforcer's costs are met from the Enforcement Reserve (A-3), the Operator's fee-advancement undertaking (A-2) and legal-expense insurance. The Trust may add to the Enforcement Reserve from the Continuity Reserve if the Committee directs.
↳ v3 c.3 "escrowed enforcement reserve … pre-funded, never an annual grant" · Row 7 · blocks Run 1 X14 (starving the enforcer)

### Article T-8: Binding interpretive authority (the interpretive "no")

**T-8.1 Interpretive Determinations.** The Enforcer may determine, in writing, that an actual or proposed act, omission, policy, contract, code release, default setting or change, by the Operator, the Trust, any fiduciary or any person bound by an instrument in Parts I to VI:
- (a) falls within a prohibition of a Protected Provision, an Entrenched Clause or Schedule D; or
- (b) is a Weakening Change.

Such a determination is an "**Interpretive Determination**". It binds the Administrative Trustee, the Committee and (through C-10) the Operator. It stands unless and until the Court of Chancery sets it aside on a finding that it was made in bad faith, or that **no reasonable person applying the Functional Reading** could have made it.
↳ v3 c.3 "binding interpretive authority … it can only say 'no'" · Rows 1, 24 · blocks QR2 (reinterpretation instead of amendment)

**T-8.2 Only "no".** No Interpretive Determination, statement, opinion, silence, delay, non-objection, waiver or course of dealing by the Enforcer or the Backup Enforcer **authorises** anything, is a defence to anyone, or stops any other person with standing from acting. **A captured enforcer's "this is fine" is legally nothing.** RT-fix.
↳ v3 c.3 · Rows 7, 13 · blocks a captured enforcer used as a safe harbour (RT3)

**T-8.3 Functional Reading.** Interpretive Determinations apply the Functional Reading (D-23).
↳ v3 c.3 "read by function, not by name" · Rows 1, 24

**T-8.4 Procedure.**
- Any Credentialed Member, Committee member, director, employee, or the Backup Enforcer may request a Determination.
- The Enforcer shall decide within 30 days.
- For a Locked Matter, or anything touching E2, E10a–c, E11 or E12, a request made by the Backup Enforcer or by 100 Credentialed Members **suspends the act** until the Determination issues, for up to 60 days.

↳ v3 c.3 · Rows 1, 19, 22, 24 · blocks shipping a reversal before anyone can object

**T-8.5 Publication.** Every Determination, and every refusal to make one, is Published with reasons in a public register within 5 business days.
↳ v3 c.3 "A 'no' is published with reasons" · Row 4 · blocks secret deals with the enforcer

**T-8.6 Concurrent power of the Backup Enforcer.** The Backup Enforcer has the same power under T-8.1 to T-8.5, concurrently with the Enforcer. A Determination by either binds. **RT-fix (extends v3, which gives the power to the Veto Foundation alone).**
↳ v3 c.3 · Rows 7, 13 · blocks a captured or paralysed Veto Foundation neutralising the interpretive lock (RT3)

### Article T-9: Anti-decanting, anti-modification and anti-migration

**T-9.1 No decanting.** The authority of any trustee under 12 Del. C. §3528 to distribute trust property in further trust, and every similar statutory, common-law or inherent power under the law of any jurisdiction, is **expressly prohibited**.
↳ v3 c.3 "prohibits decanting (§3528)" · Row 13 · blocks rewriting the trust by pouring it into a new one (§3528(f) allows an opt-out only if the instrument "expressly" prohibits)

**T-9.2 No nonjudicial settlement of Protected Provisions.** No nonjudicial settlement agreement under 12 Del. C. §3338, or under any similar law, may:
- alter, eliminate, waive, suspend, construe or interpret any Protected Provision, the Purpose or any Fallback Disposition;
- affect the composition, powers or succession of the Committee, the Enforcer or the Backup Enforcer; or
- affect this Article.

**The Settlor shall not be a party to any nonjudicial settlement agreement concerning this Trust.** This removes the exception in §3338(c) for agreements to which the trustor is a party.
↳ v3 c.3 "non-judicial settlement of protected provisions (§3338)" · Row 13 · blocks G2 and the §3338 trustor-party exception to the material-purpose limit

**T-9.3 No modification by consent. This governing instrument may not be modified under 12 Del. C. §3342**, or under any successor or similar provision of any jurisdiction, whether by the consent or the non-objection of the trustor, any fiduciary, any enforcer or any other person. **RT-fix.**
↳ v3 c.3 trust-law locks (extends v3) · Row 13 · blocks G1 (§3342 allows modification "regardless of whether the modification may violate a material purpose" unless the instrument expressly opts out; RT12)

**T-9.4 Amendment: the ratchet only.** No person holds any power to amend this Agreement except by a "**Ratchet Amendment**", which:
- (a) is a Ratchet Change;
- (b) is certified as one by 4 of 5 Committee members with Published reasons;
- (c) has the Enforcer's written consent;
- (d) has had 90 days' Public Notice;
- (e) is not the subject of an Interpretive Determination by either enforcer that it is not a Ratchet Change.

**No amendment may touch T-9, T-12, T-15 or the prohibitions of Entrenched Clause E11.**
↳ v3 c.3 "one-way ratchet (4/5 of the TSC, Veto consent, 90 days)" · Rows 7, 13 · blocks Run 1 X12 (scanning laundered through a "stricter" ratchet)

**T-9.5 No migration, division or merger of trusts.** No person may:
- change the place of administration outside Delaware, or the governing law;
- divide this Trust, or combine or merge it with any other trust [verify: the trustee's powers under 12 Del. C. §3325 to divide or combine trusts];
- create, exercise or release any power of appointment over the Trust;
- appoint any trust protector, special holder or other person with a power to amend, direct a change of situs, or add or remove any person.

↳ v3 c.3 "no change of situs or governing law" · Row 13 · blocks migration and division (RT13)

**T-9.6 Construction petitions.** A petition to construe a Protected Provision is governed by T-7.5 and the Functional Reading. The Settlor asks any court to resolve ambiguity in favour of the Purpose and against any Transfer, Capability or Weakening Change.
↳ v3 c.3 · Row 13 · blocks "reform by construction"

### Article T-10: Prohibited acts

**T-10.1** Without limiting T-6, neither the Administrative Trustee, the Committee, the Enforcer, the Backup Enforcer nor any of their agents shall:
- (a) Transfer or encumber any Trust property except as T-11 or T-12 permits;
- (b) borrow, lend to the Operator, guarantee or become surety;
- (c) receive, hold or Transfer any Data;
- (d) enter into any Commercial Relationship with a Related Party;
- (e) accept any benefit from any person seeking any Locked Matter;
- (f) delegate any power under T-6, T-7 or T-8;
- (g) agree with any person how it will vote or determine;
- (h) act under any power that T-9 excludes.

↳ v3 c.3; cl. 7a · Rows 6, 21 · blocks side deals and vote-buying

### Article T-11: Insolvency and data-non-transfer locks

**T-11.1 The Trust is outside every operator estate.** The Trust holds no property of the Operator. The Operator's creditors have no claim against the Trust. The Trust shall never agree to be liable for any obligation of the Operator.
↳ v3 c.3; cl. 9 · Row 21 · blocks creditors reaching the steward

**T-11.2 Data never passes through the Trust.** The Trust shall direct the Class T vote, and use every right it has, to prevent any Transfer of Data by the Operator, except a Transfer that the Privacy Covenant's P-6.2 permits. In any Fallback Disposition, the Trust shall direct deletion, not Transfer, of every item of Data except items a person affirmatively opted in to move to a Successor Steward.
↳ v3 cl. 9, 9b · Rows 2, 21 · blocks data as the prize of a wind-down

**T-11.3 The Continuity Reserve.** The Continuity Reserve may be applied only:
- (a) to fund the execution of Plan D, including the 5-year redirect-and-archive duty;
- (b) to fund Commons Mode;
- (c) for the Trust's own administration;
- (d) to add to the Enforcement Reserve.

It is **never lent to the Operator**. It may be granted to the Operator only for (a) or (b), in tranches matched to the incurred cost, and only while the Operator's board certifies that the Operator is paying its debts as they fall due.
↳ v3 c.3 "holds the continuity reserve"; c.4 modes · Row 21 · blocks draining the reserve into an insolvent operator (§548 exposure)

**T-11.4 The Operator's bankruptcy.** If the Operator proposes a voluntary petition under title 11, the Trust shall vote only for a filing that meets C-11. In any case, the Trust shall appear through the Enforcer to oppose any Transfer of Data, any assumption or assignment of the IP licence, and any sale of operations, and to support the appointment of a consumer privacy ombudsman under 11 U.S.C. §332.
↳ v3 cl. 9b; L3 · Row 21 · blocks a §363 sale going unopposed (RT5)

### Article T-12: Impracticability and the Fallback Dispositions (never sale)

**T-12.1 A contrary provision under §3541.** Under 12 Del. C. §3541, the power of the Court of Chancery to modify or terminate this Trust is subject to the contrary provisions in this Article. The Settlor states them as material purposes. The Settlor's intent is that, if the Purpose ever becomes impossible or unlawful to carry out in any way T-2.3 describes, the **only** permitted outcomes are the Fallback Dispositions in T-12.2.
↳ v3 c.3 "names the only fallback purposes … which narrows Chancery's §3541 modification power" · Row 21 · blocks Run 1 X15 (cy pres into a "mission-aligned" sale; RT4)

**T-12.2 The only Fallback Dispositions.** They are:
- (A) **Successor Steward Transfer**: transfer of the Class T Membership (or, if the Operator is dissolved, of the Operator's remaining non-Data assets) to the purpose trust of a Successor Steward, for **no consideration**, carrying only Data that individuals affirmatively opted in to move (P-6.2(d));
- (B) **Plan D.**

If no Successor Steward qualifies within 180 days after the Committee determines that T-12 applies, Plan D follows. A court asked to choose a disposition is asked to choose (A) or (B) and nothing else. Only the Enforcer and Backup Enforcer, acting together, may approve a Successor Steward form other than a Delaware nonstock 501(c)(3) (D-22(a)).
↳ v3 c.3 "plan D, or transfer to a successor steward under an identical deed" · Row 21 · blocks any third outcome (RT4, RT7)

**T-12.3 Plan D.** Plan D means, in this order:
- (1) enter Mode D (S-8) if the Operator has not already done so;
- (2) open release of all code (AGPL or more permissive) and all specifications (CC BY or more permissive), with build instructions;
- (3) a 90-day export drill for every Member and every circle: one-step signed export, self-host packages, and in-product notices through every update channel;
- (4) deletion of every item of Data, with signed deletion receipts published by aggregate count and delivered to each person who asks;
- (5) cards resolving from a static archive for 5 years, funded from the Continuity Reserve, with no Data other than the public cards themselves;
- (6) distribution of residual assets under T-12.6;
- (7) **no sale, lease, licence or Transfer for value of operations, brand, marks, domains, Data, member relationships, staff, contracts or goodwill, to any person.**

↳ v3 c.3 Plan D; c.4 Mode D ("export drill, self-host packages, and cards resolving from a static archive for 5 years") · Rows 21, 20 · blocks a creditor's or acquirer's sale; makes exit real (covenant: "could they leave without losing the relationships they formed?")

**T-12.4 Never sale.** No Fallback Disposition, and no order of any court that the Trust can influence, may involve any sale or other Transfer for value of anything listed in T-12.3(7). No Fallback Disposition may include any merger or conversion into or with any entity other than a Successor Steward. The Trust shall use every right it has to oppose any such order.
↳ v3 c.3 "no sale of operations, brand, domains or data to anyone" · Row 21 · blocks the friendly acquirer (RT7) and the "aligned buyer" petition (RT4)

**T-12.5 If a court nonetheless modifies.** If a court of competent jurisdiction orders a modification despite this Article:
- (i) the modification is to be no broader than necessary;
- (ii) every Protected Provision not expressly displaced continues to bind the Trust and every recipient of any Trust property;
- (iii) the order of preference is Successor Steward Transfer, then Plan D, then a disposition to an open-infrastructure 501(c)(3) bound by Schedule A.

↳ v3 c.3 "Honesty … courts keep equitable powers" · Row 21 · limits the residual (L3)

**T-12.6 Residual assets.** Residual assets go to one or more organisations exempt under IRC §501(c)(3) whose purpose is open digital infrastructure, chosen jointly by the Enforcer and the Backup Enforcer from a Published list. **No recipient may be a Related Party or have employed a former officer of the Operator within 3 years.** They never go to the Settlor or any Related Party.
↳ v3 c.3 "residual assets to an open-infrastructure 501(c)(3)"; cl. 7a · Rows 6, 21 · blocks self-dealing on the way out

**T-12.7 Termination.** The Trust terminates only when the Enforcer and Backup Enforcer jointly certify that Plan D, or the Successor Steward Transfer, is complete and that the 5-year archive duty is funded.
↳ v3 c.3 · Row 21

### Article T-13: The Settlor

**T-13.1 Interim powers end at month 18.** The Settlor's only powers are to fill the interim seats in T-5.1 and to sign Schedule T-3. **Both end 18 months after the date of this Agreement.**
↳ v3 c.3 "Every appointment power the founder holds ends at month 18" · Row 6 · blocks founder control

**T-13.2 Nothing to the Settlor.** The Settlor receives no Compensation, property or benefit from the Trust or the Operator, other than a published salary for employment with the Operator within E7 limits, if any.
↳ v3 c.3 · Row 6

**T-13.3 The Settlor is not a consenting party.** The Settlor shall not be a party to, or give consent or non-objection under, 12 Del. C. §3338, §3342 or any similar law concerning this Trust. RT-fix.
↳ v3 c.3 · Row 13 · blocks G1 (the living-trustor routes; RT12)

### Article T-14: The two-vehicle doctrine

**T-14.1** The Trust shall never hold, fund, govern, affiliate with or be governed by any religious, philosophical or teaching vehicle. Any such vehicle is separate, later, and holds nothing of the Trust or the Operator.
↳ v3 c.3 "Two-vehicle doctrine"; operator hypothesis 3 · Row 13 · blocks the teaching mission touching the commercial operation, and the "AI cult" smear surface

### Article T-15: Severability, and failure closed

**T-15.1 Nearest stricter term.** If any provision of this Agreement is held invalid or unenforceable, it is replaced by the enforceable provision that most nearly achieves its protective effect.
↳ v3 c.3 · Row 13 · blocks a single invalidity opening everything

**T-15.2 Void, not merely wrongful.** Any act done in breach of a "shall not" in this Agreement is void to the extent the law permits.
↳ v3 c.3 · Row 13

**T-15.3 Failure closed.** If any required approval (of the Enforcer, the Backup Enforcer, the Council or the Committee) is held invalid or cannot be obtained because the body no longer exists, **the matter needing it becomes prohibited**. It does not become permitted without that approval. For a Fallback Disposition only, the requirement is replaced by approval of the Court of Chancery after notice under T-7.5.
↳ v3 c.3 · Rows 13, 21 · blocks "the lock is gone, so the door is open"

### Article T-16: Transparency

**T-16.1** This Agreement, every Schedule, every direction under T-6 with its reasons, every Determination, and the Trust's annual accounts are Published. They are never confidential.
↳ v3 c.3; c.2.5 transparency publisher · Row 4 · blocks opacity (dossier pattern)

### Article T-17: General

**T-17.1** Schedule D is incorporated. Headings and comments (lines beginning "↳") are not part of the text. Notices are in writing and Published. This Agreement may be signed in counterparts.
↳ drafting

*Schedules:*
- *T-1: Initial property (the Class T Membership on the Operator's formation; the founder's reserve gift of $[●]).*
- *A: Covenant Commitments (text identical to C-8 and C-12).*
- *D: Common Definitions.*
- *T-2: the Committee's rules.*
- *T-3: Acceptances of the Enforcer and Backup Enforcer.*

---

## PART II — CERTIFICATE OF INCORPORATION OF [OPERATOR], INC.

*A nonstock, nonprofit corporation under the Delaware General Corporation Law (Title 8), applying for recognition under IRC §501(c)(3).*

### Article C-1 to C-3: Name, office, form

**C-1 Name.** The name of the corporation is [OPERATOR], Inc. (the "**Corporation**" or "**Operator**").
↳ drafting; v3 c.2 (a coined name must clear classes 9, 42 and 45 first)

**C-2 Registered office.** [●], Delaware.
↳ drafting

**C-3.1 Nonstock.** The Corporation is a nonstock corporation. It has no authority to issue capital stock. **It has no authority to issue, and shall not issue, any Instrument that confers any economic right, or any vote or consent right, on any person other than the Members named in Article C-5.**
↳ v3 c.3 "Nonprofits have no equity, so 'no investors' is structural" (Run 1 b.6.1); cl. 7b · Rows 6, 21 · blocks recapitalising (Run 2 A8.4) and the funder whose return scales with capture (thesis cut 2)

**C-3.2 Nonprofit.** The Corporation is not organised for profit. No part of its net earnings shall inure to the benefit of any private person. It shall make no distribution to any Member, director or officer, except reasonable Compensation within E7.
↳ v3 cl. 7; IRC §501(c)(3) · Row 6 · blocks extracting value through distributions

### Article C-4: Purposes

**C-4.1 Charitable purposes.** The Corporation is organised and shall be operated exclusively for charitable and educational purposes within IRC §501(c)(3). In particular, its purposes are:
- (a) to provide, free to the public, open civic infrastructure through which people and community groups plan and hold gatherings in person;
- (b) to develop and publish open specifications and open-source software for that purpose;
- (c) to conduct and publish consented, pre-registered research into social connection and the harms of digital platforms;
- (d) to educate the public about privacy-preserving civic technology.

[counsel: the organisational test; the commerciality doctrine; the *Yorba* (2014) risk.]
↳ v3 c.3 "Operator: a Delaware nonstock nonprofit applying for 501(c)(3)" · Rows 3, 5 · blocks nothing by itself; it is the charitable frame that §363(d)(1) and §541(f) then protect (G11)

**C-4.2 Purposes limited by the Entrenched Clauses.** The Corporation shall pursue its purposes **only** in compliance with Articles C-8 to C-12. An act that breaches them is outside the Corporation's purposes and powers.
↳ v3 c.3 · Rows 1–25 · blocks "the purpose justifies it" arguments; makes a breach ultra vires

**C-4.3 Prohibited activities.** The Corporation shall not:
- participate or intervene in any political campaign for or against any candidate;
- carry on propaganda or attempt to influence legislation except as IRC §501(h) permits (if elected);
- carry on any activity not permitted to an organisation exempt under §501(c)(3) or to one whose contributions are deductible under IRC §170(c)(2).

↳ IRC §501(c)(3); Treas. Reg. §1.501(c)(3)-1(b) · K9

### Article C-5: Members

**C-5.1 Three classes, and no others.** The Corporation has exactly three classes of members:
- (a) **Class T**: one member, the Administrative Trustee of the [●] Stewardship Trust, acting as trustee;
- (b) **Class V**: one member, [VETO FOUNDATION];
- (c) **Class C** (the "**Council**"): every Credentialed Member (B-1) who holds a current credential.

No other person is a member within the meaning of the DGCL. **No new class may be created, and no person admitted to Class T or Class V, except as a Locked Matter, and never with any economic right.**
↳ v3 c.3 "sole voting member"; "consent-only veto membership"; "Council: one person, one vote" · Rows 6, 13 · blocks member substitution and the admission of an investor class (RT7)

**C-5.2 Class T rights.** Class T elects 3 of 5 directors, votes on Locked Matters, and has every other voting right of a member that this Certificate does not give to another class.
↳ v3 c.3 lock 2 · Row 13

**C-5.3 Class V rights (consent only).** Class V has no vote in the election of directors and no vote on ordinary matters. Under 8 Del. C. §215, it has:
- (a) the right to give or withhold **written consent** on each Locked Matter, without which the matter is not approved;
- (b) the powers of Article C-10;
- (c) the right to vote on dissolution under C-5.5.

↳ v3 c.3 "holds a consent-only veto membership in the operator" · Rows 7, 13 · §215 permits classes with "full, limited, or no voting rights" and the right "to vote on a specified transaction" [verify]

**C-5.4 Class C rights.** Class C:
- (a) elects 2 of 5 directors [drafting choice: v3 says the trust elects 3 of 5 and is silent on the other 2];
- (b) votes on Locked Matters (Lock 4) and on additions to the paperwork list (E5.2);
- (c) votes on dissolution under C-5.5;
- (d) has the petition rights in B-3.

Voting is per capita, one person one vote, by the blind-token procedure in B-1. **Class C members have no economic right and no liability.** [counsel: whether a large, credential-based member class of a 501(c)(3) is workable under DGCL §§211–231 notice and record requirements, and how far the bylaws may prescribe electronic procedures.]
↳ v3 c.3 lock 4 (council vote); "People's power" · Rows 6, 13 · makes the Council a statutory lock rather than an advisory one (blocks Run 2 A8.5: "comments can be ignored")

**C-5.5 Dissolution vote.** For 8 Del. C. §276, **Class T, Class V and Class C are each entitled to vote on dissolution**, as separate classes. Dissolution without action of the governing body, by written consent of all members entitled to vote, is therefore possible only with the consent of all three classes. RT-fix.
↳ v3 c.3 Five locks ("dissolution") · Row 21 · blocks G3 (the sole voting member dissolving the Corporation by written consent under §276; RT16)

### Article C-6: The board

**C-6.1 Composition.** The board has 5 directors: 3 elected by Class T and 2 elected by Class C, serving staggered 3-year terms. No more than 2 may be employees. The chief executive may not chair the board. Until month 18, the Settlor of the Trust may designate interim directors for any unfilled seat, and that power ends at month 18.
↳ v3 c.3 "elects 3 of 5 directors"; "appointment power … ends at month 18" · Rows 6, 13

**C-6.2 Qualification.** Every director shall sign the Director Covenant (B-16) before taking office, and shall meet its conflict tests while in office.
↳ v3 cl. 7a; c.4 item 1 · Row 6

**C-6.3 Management subject to this Certificate.** Under 8 Del. C. §141(a) and §141(j), the board manages the Corporation's affairs **except** as this Certificate gives powers to Class V, to the Council, or to the procedures of Articles C-9 to C-12. Where this Certificate requires another approval, the board's power is exercisable only with it.
↳ v3 c.3 · Row 13 · §141(a) allows the certificate to vest board powers in "such person or persons as shall be provided" [verify]

### Article C-7: Definitions

**C-7.1** Schedule D (Common Definitions) is part of this Certificate, word for word as attached. Capitalised terms have the meanings given there.
↳ v3 c.3 · Rows 1–25 · blocks the definitions drifting from the deed's

### Article C-8: The Entrenched Clauses

*Each Entrenched Clause changes only through all five locks (C-9), except those in C-9.5, which cannot change at all.*

**E1.1 No advertising.** The Corporation shall not display, perform, sell, accept consideration for, or permit Advertising on or through the Service, or in any communication to any person.
↳ v3 cl. 1 · Rows 2, 18 · blocks surveillance advertising and paid prominence (dossier patterns)

**E1.2 No editorial curation surfaces.** The Corporation shall operate no surface on which any person acting for it selects, orders, features or groups Content, cards, circles, organisations or people for others, other than by the Ordering Rule (E10b). Staff do not pick.
↳ v3 cl. 1 ("There are no editorial curation surfaces") · Rows 16, 18 · blocks Run 1 X17 ("Stoke Picks"; "city guide")

**E1.3 Thanks, only in one place.** Institutions, donors and grantors may be named only on a single Published Supporters Page, alphabetically or by date, without links from any card, circle, listing, Notification or search result. **No attribution line appears anywhere else.** A donor or institution may ask not to be named.
↳ v3 cl. 1 ("Institutions are thanked only on a published list, never on cards, circles or listings"); c.4 · Rows 6, 18 · blocks the "kept free by" line that Run 2 allowed, and paid attribution

**E2.1 No data transactions.** The Corporation shall not Transfer any Data to any person, for or without consideration, and shall not give any person privileged access to any Data. The only exceptions are those in E2.2.
↳ v3 cl. 2 · Rows 2, 21 · blocks data sale and "insights" licensing (Run 1 X1), and the 23andMe outcome

**E2.2 Only these disclosures.** The only permitted disclosures of Data are:
- (a) the fixed Open-Books Metrics listed in B-8, published free to everyone at the same moment;
- (b) Data given to the person it concerns, or sent where that person directs (export, a message they send);
- (c) a disclosure compelled by valid legal process, limited to Data already held. It is made only after the Corporation has challenged the process wherever reasonable grounds exist, and with notice to the affected person unless the law forbids notice. It is never a Transfer for value and never builds a Capability (E11);
- (d) research outputs from consented, pre-registered panels under B-12, published as open results; panel microdata never leaves the panel's own consent terms;
- (e) disclosure to a processor under written contract (A-6), solely to perform a service for the Corporation, with no right to use the Data for any other purpose and subject to E12;
- (f) a Successor Steward Transfer of Data that individuals affirmatively opted in to move (P-6.2(d)).

↳ v3 cl. 2 ("The only disclosures are the fixed open-books metrics. Research uses consented, pre-registered panels only") · Rows 2, 3, 21 · blocks "privileged access" deals and research as a back door

**E3 No creator economics.** The Corporation shall not operate or facilitate any program that pays any person for Content, attention, audience or engagement. It shall not charge, deduct or receive any fee, commission, spread, float or percentage on any value that passes between users of the Service.
↳ v3 cl. 3; operator decision 1 · Row 5 · blocks creators as shock absorbers (dossier pattern) and the toll between friends

**E4.1 The free floor.** Each of the following Free Floor Functions is available to every person, including organisations and institutions, free of charge. None is conditioned on payment, supporter status, organisational status, or any count, size, frequency or volume:
- (a) creating, sharing and updating cards and series, and subscribing to calendar feeds;
- (b) responding without an account, and re-entry codes;
- (c) **rosters of any size**, co-organisers, public schedules and public listing in the Commons;
- (d) QR posters and the basic embed;
- (e) circles, including the plan, the shelf and the history, and, once media ships, a media allowance of **at least 1 GB per person, which can never be reduced**;
- (f) export, deletion, self-host packaging and the host key;
- (g) the Guide, whenever one exists.

↳ v3 cl. 4 · Rows 5, 6 · blocks Run 1 X4 (the toll gate) and Run 3's $20 organisation fee ("a community should not need to pay to reach itself")

**E4.2 Neutral abuse limits only.** The only limits on a Free Floor Function are neutral abuse limits listed in B-13.2 (for example the 150-response cap, 20 new cards per host per day, and Commons caps per host). They apply equally to everyone, **cannot be lifted or relaxed for payment**, and are changed only by a Ratchet Change or through the five locks.
↳ v3 c.2.5; cl. 4 · Rows 15, 18 · blocks "unlimited rosters on the paid plan"

**E4.3 Nothing a community needs to reach itself is ever paid for.** Where a function is not listed in E4.1 but is needed for a group to organise, reach, see or be reached by its own members, it is a Free Floor Function. The Veto Foundation decides the question under C-10.
↳ v3 cl. 4 ("Nothing a community needs to reach itself is ever paid for") · Rows 5, 6 · blocks re-packaging a floor function as "new"

**E4a No monetisation through the link layer.** The Corporation shall not rewrite, tag, wrap, redirect, shorten for tracking, or add affiliate, referral or commission parameters to any link any person shares. It shall not receive any consideration connected with any person's use of such a link.
↳ v3 cl. 4a · Row 23 · blocks Run 2 A6 (link-layer monetisation)

**E5.1 Paid features: a closed list.** The Corporation may charge only for the following "**paperwork**" features:
- invoices and receipts;
- a W-9;
- multi-admin roles with an audit log;
- custom styling;
- a custom domain;
- bulk import;
- SSO;
- an accessibility-conformance report;
- a DPA;
- SLAs;
- priority *product* support.

**Safety, abuse and account-recovery support are never tiered.** No paid feature may confer reach, visibility, placement, order, roster size, data, analytics, a Behavioural Measure, or any Capability over another person.
↳ v3 cl. 5 · Rows 5, 6, 24 · blocks the paid tier as surveillance-for-payers (Run 3 X1) and "priority safety"

**E5.2 Adding to the list.** An item may be added to E5.1 only if (i) the Veto Foundation does not determine that it is outside the "paperwork" description or within E4, (ii) a Council vote approves it, and (iii) 90 days' Public Notice has run.
↳ v3 cl. 5 ("Adding to the list needs a council vote and 90 days' notice") · Row 6

**E6 Price rule.** The suggested supporter gift and every paperwork price may rise only by the change in CPI-U since the last change, and **never because the number of payers fell**. A fall in payers triggers the modes in C-12.3, not a price rise.
↳ v3 cl. 6; Run 1 b.6.2 cl. 6 · Row 6 · blocks Run 1 X2 (cost-plus pricing)

**E7.1 Pay rule.** No person's annual Compensation may exceed the lower of (a) 3 × the median annual Compensation of the Corporation's employees, and (b) $300,000 in 2026 dollars, indexed by CPI-U. No person may receive equity or any Instrument, any bonus tied to usage, growth or any metric of the Service, or any Compensation tied to any metric.
↳ v3 cl. 7 · Row 6 · blocks pay that makes growth personally valuable (thesis cut 1)

**E7a Related parties.** The Corporation shall not enter into, renew or materially amend any Commercial Relationship with a Related Party unless:
- (i) the Veto Foundation approves it in writing;
- (ii) its terms are Published before it takes effect; and
- (iii) the independent directors find it on terms no less favourable to the Corporation than arm's length.

No surplus grant may go to any entity that employs, or within 3 years employed, a former officer of the Corporation. [This also supports compliance with IRC §4958, excess benefit transactions; counsel.]
↳ v3 cl. 7a · Row 6 · blocks Run 1 X2 (salary and contract extraction)

**E7b.1 No outside economic interests; subsidiaries bound.** The Corporation shall not form, acquire or hold any interest in any subsidiary, affiliate, joint venture or other entity **except as a Locked Matter**. No such entity may issue any Instrument to any person other than the Corporation. Every such entity is part of the "Operator" (D-8) and is bound by every Entrenched Clause as if it were the Corporation. RT-fix (extends v3).
↳ v3 cl. 7b · Rows 1, 2, 21 · blocks Run 2 A8.6 ("move the product out") and the subsidiary route (RT9)

**E7b.2 No exclusive licence.** The Corporation shall grant no exclusive licence of, and shall not Transfer, the client, the server, any specification, any Data, or any mark or domain it may hold. It shall accept no licence of any of those that restricts it from publishing them openly.
↳ v3 cl. 7b · Rows 20, 21 · blocks the licensing deal (RT10)

**E8 Surplus ratchet.** Unrestricted reserves are capped at 18 months of Actual Burn. Any excess, measured annually from audited accounts, is applied within 12 months to one or more of:
- (a) a lower suggested gift;
- (b) higher free quotas (never lower);
- (c) grants to open infrastructure through an independent committee under E7a.

Operating-cost growth above user growth plus CPI for 2 consecutive years requires a Council vote.
↳ v3 cl. 8; Run 1 b.6.2 cl. 8 · Row 6 · blocks accumulation that later funds a buyout, and cost-plus drift

**E9 Data is never an asset.** No Data is an asset of the Corporation available to any creditor, purchaser, successor, trustee, receiver or other person. The Corporation holds all Personal Information and Content as **custodian and agent for the persons it concerns**, for the sole purpose of providing the Service to them, and has no beneficial interest in it (P-6.5). **No Data may be valued, listed as an asset, pledged, or offered in any sale process.**
↳ v3 cl. 9 · Row 21 · blocks data as the prize of insolvency; supports the §541(d) argument [counsel]

**E9a.1 Capital clause.** The Corporation may incur Debt only if **all** of the following hold:
- (a) it is unsecured, or secured only by cash or receivables, and **never by code, marks, domains, Data, Metadata, keys, membership rights, licences or any Instrument**;
- (b) scheduled debt service is no more than 25% of the trailing 6-month operating surplus at signing. A bridge is exempt from (b) only while it is repayable **solely from surplus**;
- (c) it carries no covenant, condition, information right, consent right or event of default relating to product, pricing, Data or governance;
- (d) the instrument contains the mandatory terms in A-4.

↳ v3 cl. 9a · Rows 6, 21 · blocks Run 2 A11.6 ("buy the debt") and control through covenants

**E9a.2 No guarantees; no security by other names.** The Corporation shall not guarantee any obligation, sell receivables with recourse, enter any sale-leaseback of Service infrastructure, or grant any lien, negative-pledge waiver or control agreement over any asset in E9a.1(a).
↳ v3 cl. 9a · Row 21 · blocks structuring around "security"

**E9b.1 Insolvency clause: never transferred.** Personal Information and Metadata are **never Transferred to any successor**. The only exception is a Successor Steward, and then only for individuals who affirmatively opt in under P-6.2(d). The Privacy Covenant (Part IV) states this, and it is a Protected Bylaw.
↳ v3 cl. 9b · Row 21 · engages 11 U.S.C. §363(b)(1); blocks the *In re 23andMe* (2025) door (a policy that *permits* transfer)

**E9b.2 Export, then delete, before insolvency.** On entering Mode D (S-8), and in any wind-down, the Corporation shall run a 90-day export window and then delete all Data with receipts, **completing the deletion before any petition under title 11 is filed**, except where a court has already been petitioned without the Corporation's consent.
↳ v3 cl. 9b ("exported during a 90-day window and then deleted with receipts"; "a solvent wind-down is triggered before insolvency") · Row 21 · blocks G7 (after a petition, deletion needs court authority)

**E10.1 One tier; parity; harm gates; client-side ordering.**
- (a) One tier of rules applies to every person.
- (b) The Service launches in a language only when trust-and-safety capacity in that language meets the parity test in B-13.3.
- (c) Harm-gate decisions of the Sortition Jury (B-5) cannot be overridden by any growth, revenue or partner consideration.
- (d) All Ordering of other people's Content happens on the reader's device over a signed, unsorted set.

↳ v3 cl. 10 · Rows 8, 13, 1 · blocks geographic externalisation and policy that follows political risk (dossier patterns)

**E10a The Notification Rule.** A Notification may be triggered only by:
- (1) another human's action addressed to the recipient; or
- (2) a time the recipient set.

Everything else is an optional digest, **off by default**, which the recipient may turn on and which contains only items within (1) or (2). **No Notification may be triggered by absence, inactivity, an Aggregate, a suggestion or any Behavioural Measure.** The ratio of Notifications to (human-addressed events plus self-set reminders) shall not exceed 1.00, and is Published quarterly. No more than 2 reminders go to any person per gathering.
↳ v3 cl. 10a; c.2.4 item 5 · Row 10 · blocks addiction by design (dossier pattern), Run 2 A8.2 and the re-engagement nudge

**E10b The Ordering Rule.** The only Orderings permitted anywhere in the Service are:
- (a) chronological;
- (b) a sort the viewer picks from a fixed list of the item's own attributes (date, title, distance from a place the viewer typed);
- (c) text match within the viewer's own cards and circles, shown chronologically.

**Nothing is Ordered by any count of other people's behaviour, or by any Data the Operator holds about the person's own past behaviour.** The only exception is a computation the person invokes on their own device over their own Data. This rule is enforced by a Published CI lint on every Ordering and Notification function, and by an audit of the data flows into them (B-11).
↳ v3 cl. 10b; c.2.4 item 4 · Rows 1, 9, 16 · blocks engagement optimisation (dossier pattern), Run 2 A8.1 ("Popular near you"), and relevance-ranked search

**E10c No surveillance for the payer.** No organisation-, institution- or operator-facing view, export, report, API or Notification may list or reveal any individual's attendance history, absence, inactivity, responsiveness or any other Behavioural Measure. No tool may draft or send re-engagement messages to lapsed people. An organiser sees who answered *this* gathering, and nothing across gatherings per person.
↳ v3 cl. 10c · Row 24 · blocks Run 3 X1 (payer "member insights"; "we miss you" drafts)

**E11 No scanning, classifying or profiling; no key escrow; no compelled access. UNAMENDABLE.** The Operator shall not build, hold, deploy, license, accept or maintain any Capability for:
- Scanning, Classifying or Profiling any person or any Content or Metadata;
- Key Escrow; or
- any Compelled-Access Capability.

This prohibition **cannot be waived, consented to or suspended** by any person, vote or combination of the locks, by any person's consent, or for any purpose, including safety, child protection, fraud prevention or legal compliance. If any law or order would require such a Capability, the only permitted responses are refusal, litigation, withdrawal from the jurisdiction, or Plan D. In particular, if a regulation of the European Union requires detection within end-to-end encrypted services, the Service does not launch in, or withdraws from, the European Union, and that decision is Published.
↳ v3 cl. 11 ("UNAMENDABLE … prohibited, not consentable") · Rows 7, 19, 22 · blocks QR3 (a consentable backdoor), Run 1 X12 (the "safety" ratchet) and client-side scanning (RT8)

**E12 P-PLAIN.** The Operator shall not hold, process or transmit any Member or Guest Content in Plaintext, **except only**:
- (a) Content a person chose to publish to the public;
- (b) Content a reporter chose to submit in a report;
- (c) the calendar-feed fields in the Published schema: a time, a generic title (by default "Circle gathering"), and nothing else, with no address and no roster;
- (d) delivery addresses (email or phone) a person entered for delivery to themselves, deleted as the Service's retention schedule requires.

Any feature needing more is a Locked Matter under all five locks. The metric "plaintext paths outside the schema" is a covenant zero; any non-zero reading is an incident under B-11.3.
↳ v3 cl. 12 · Rows 2, 19, 25 · blocks QR1 (E2EE reversed through a helper, default-on) and RT2

### Article C-9: Locked Matters, the five locks, the ratchet, unamendable provisions

**C-9.1 Locked Matters.** Each of the following is a "**Locked Matter**":
- (a) any amendment of this Certificate (including Schedule D), or of any Protected Bylaw (B-15);
- (b) any Weakening Change, however made;
- (c) any merger or consolidation (including under 8 Del. C. §§251–258), conversion (§266), domestication or transfer out of Delaware;
- (d) any sale, lease, exchange, licence or other Transfer of **any Material Asset**, in one transaction or a series, whether or not it amounts to "all or substantially all". "**Material Asset**" means any asset, right, contract or relationship worth more than 5% of total assets, and every item of Data, code rights, marks, domains or the IP licence, whatever its value;
- (e) any management, services, affiliation, operating, joint-venture or similar agreement that gives any person control over, or the right to run, any part of the Service or its governance. RT-fix;
- (f) the admission of any member, the creation of any class, and any change to any member's rights;
- (g) the creation of any Instrument, subsidiary or affiliate;
- (h) dissolution (§§275–276);
- (i) any Weakening Change to the Privacy Covenant's protected part (Part IV);
- (j) any change of the Corporation's fiscal or tax status;
- (k) any feature that needs Plaintext outside E12.

↳ v3 c.3 Five locks ("conversion, merger, sale, dissolution or issuing any instrument") · Rows 13, 21 · blocks the friendly acquirer (G4, RT7), partial asset sales below §271 (Run 2 A8.6) and "operating agreements"

**C-9.2 The five locks.** A Locked Matter is approved only if, in this order:
- (5) **Public Notice** of the full proposal has run for at least **90 days** before any lock vote;
- (1) **two-thirds of the whole board** (not of those present) approves it after the notice period;
- (2) **Class T approves**, subject to T-6 of the Trust Agreement;
- (3) **Class V consents in writing**; and
- (4) **the Council approves**, by two-thirds of votes cast with turnout of at least 20% of Credentialed Members [drafting choice: v3 says only "a council vote"; Run 2 §4 used 2/3 with ≥20% turnout].

The numbering follows v3; notice runs first.
↳ v3 c.3 "Five locks" · Row 13 · blocks any single body, or a regulator plus one body, making a change (the OpenAI lesson)

**C-9.3 Greater-vote provisions are themselves entrenched.** Under 8 Del. C. §102(b)(4) and §242(b)(3), Articles C-5, C-8, C-9, C-10, C-11, C-12, C-15 and Schedule D may be amended, altered or repealed only by the votes, consents and procedures in C-9.2, and never by any lesser vote.
↳ v3 c.3 · Row 13 · §102(b)(4): a greater-vote provision "cannot be altered, amended or repealed except by such greater vote" [verify]

**C-9.4 No written consent; meetings only.** No member may act by written consent in lieu of a meeting on any Locked Matter [verify: 8 Del. C. §228 as applied to nonstock corporations]. Every lock vote is taken after the notice period, on the text that was noticed.
↳ v3 c.3 lock 5 · Row 13 · blocks G3 (a same-day reversal)

**C-9.5 Unamendable Provisions.** The following can never be amended, repealed, waived or suspended, by any vote, consent or combination of the locks:
- (a) E11;
- (b) E9b.1 as applied to Data collected before any change;
- (c) Plan D as stated in Article C-14 and the Trust Agreement T-12.3;
- (d) this C-9.5;
- (e) the definitions in Schedule D so far as E11 uses them.

The Trust Agreement (T-6.1(b)) forbids Class T to vote for any such change. The Veto Foundation's certificate (V-3.1) forbids Class V to consent. Any purported change is void. [counsel: G9. The DGCL has no express "unamendable" category; the effect rests on mirrored prohibitions making the required approvals legally impossible.]
↳ v3 c.3 "Clause 11 and plan D cannot be changed at all" · Rows 19, 21, 22 · blocks QR3 and the "safety" amendment (RT8)

**C-9.6 The ratchet track (the three locks).** A Ratchet Change to any Entrenched Clause, Protected Bylaw or Schedule D may be adopted by a lighter track instead of C-9.2, namely:
- (i) 4 of 5 of the Trust Stewardship Committee certify it as a Ratchet Change (acting for Class T);
- (ii) Class V consents in writing;
- (iii) 90 days' Public Notice has run;
- (iv) no Interpretive Determination by the Veto Foundation or the Backup Enforcer says it is not a Ratchet Change.

**A change that adds any Capability, whatever its stated purpose, is never a Ratchet Change.**
↳ v3 c.3 "One-way ratchet … open only to changes that remove an operator capability, shorten retention or delete a data category" · Rows 7, 22 · blocks Run 1 X12

**C-9.7 Dissolution only by Plan D.** The Corporation may be dissolved only as part of a Fallback Disposition under Trust Agreement T-12, approved under C-9.2, with every class voting under C-5.5.
↳ v3 c.3 Plan D · Row 21 · blocks a dissolution that sells the assets

**C-9.8 Prospective only.** No change adopted under this Article applies to Data collected before the change takes effect, except a Ratchet Change.
↳ v3 c.5 row 13 ("prospectively") · Rows 13, 21 · keeps the §363(b)(1) policy for existing data frozen

### Article C-10: Interpretation

**C-10.1 Functional Reading.** Every provision of this Certificate and of the Protected Bylaws is read under the Functional Reading (D-23).
↳ v3 c.3 · Rows 1, 24 · blocks QR2

**C-10.2 Binding interpretive "no".** Class V, and the Backup Enforcer under the Enforcement Agreement (A-2), may each issue Interpretive Determinations about any act, omission, policy, contract, code release, default or proposal of the Corporation, as the Trust Agreement T-8 describes. A Determination binds the board, the officers and the Corporation. The Corporation shall not act contrary to one unless and until the Court of Chancery sets it aside under T-8.1.
↳ v3 c.3 "Any operator action that arguably touches an entrenched clause can be vetoed by the Veto Foundation on a functional reading" · Rows 1, 24 · blocks QR2 and RT1 [counsel: whether a certificate may bind the board to a non-director's determination; §141(a)]

**C-10.3 No safe harbour.** Nothing Class V or the Backup Enforcer says or does, short of a Determination, authorises any act or is a defence to anyone.
↳ v3 c.3 · Row 7 · blocks RT3 (the captured enforcer's "yes")

**C-10.4 Publication.** Every request for a Determination, and every Determination, is Published.
↳ v3 c.3 · Row 4

### Article C-11: Bankruptcy and insolvency

**C-11.1 Solvent wind-down first.** The board shall place the Corporation in Mode D under the Resolution (S-8) when the triggers there are met. The board shall not file a voluntary petition under title 11 unless (a) the steps in E9b.2 have been completed, or (b) the board has found, with advice of counsel and after notice to Class V, that a filing is necessary to prevent an unlawful preference or to protect Members' Data from a creditor's process.
↳ v3 cl. 9b; c.4 modes ("orderly handover, solvent") · Row 21 · blocks a filing chosen to enable a sale; handles G10 without blocking a filing outright

**C-11.2 Required first-day positions.** In any case under title 11, the Corporation shall, at the earliest opportunity:
- (a) file the Privacy Covenant as the privacy policy in effect;
- (b) move for authority to delete Data under E9b.2, or to return it to the persons it concerns;
- (c) oppose any sale, lease or other Transfer of Data, and ask for the appointment of a consumer privacy ombudsman under 11 U.S.C. §332;
- (d) state that it holds Data as custodian (E9);
- (e) state that the IP licence (A-1) is personal and not assumable or assignable;
- (f) give notice to the Delaware Attorney General of any proposed transfer of charitable assets.

↳ v3 cl. 9b; L3 · Row 21 · blocks an unopposed §363 sale (RT5)

**C-11.3 No involuntary case lies; nothing to consent to.** The Corporation is not a moneyed, business or commercial corporation within 11 U.S.C. §303(a). It shall not consent to, or fail to contest, any involuntary petition. [counsel: §303(a); a nonprofit's burden to show eligibility.]
↳ v3 c.3 Structure A · Row 21 · blocks a creditor-initiated bankruptcy (the "buy the debt, then file" route)

**C-11.4 Charitable restrictions follow the assets.** Every asset of the Corporation, including every item of Data it holds as custodian, is held subject to its charitable purposes and to the Entrenched Clauses. That is so for 11 U.S.C. §363(d)(1), §541(f) and §1129(a)(16). A Transfer of any asset that would breach this Certificate is not a transfer "in accordance with applicable nonbankruptcy law". [counsel: whether charter restrictions count as "applicable nonbankruptcy law" governing a nonprofit's transfers.]
↳ v3 cl. 9, 9b · Row 21 · uses G11; blocks a bankruptcy sale overriding the charter (RT5)

**C-11.5 No DIP lien on protected assets.** The Corporation shall not propose or consent to any financing in any case that is secured by, or gives any right over, any asset described in E9a.1(a).
↳ v3 cl. 9a · Row 21 · blocks debtor-in-possession financing as a back door

### Article C-12: Charter Obligations (start gate, modes, austerity)

**C-12.1 Start gate.** The board shall not authorise, and no officer shall incur, any expenditure beyond the Formation Budget until the start gate in the Resolution (S-2, S-3) is certified. If it is not certified by the Gate Deadline, the Corporation shall enter Commons Mode (S-4).
↳ v3 c.4 item 1 ("a charter obligation of the board") · Row 21 · blocks the Run 3 "Front 8" failure (build, hire, then die at M14 holding people's rosters)

**C-12.2 Modes on Actual Burn.** The Corporation's operating mode is set only by Runway computed on Actual Burn (D-25), under S-8. **No budget, plan or projection may trigger or delay any mode.**
↳ v3 c.3 "Austerity triggers run on trailing 3-month actual burn" · Row 21 · blocks Run 1 X13

**C-12.3 What austerity may never cut.** No mode, budget or austerity measure may:
- (a) reduce any Free Floor Function (E4);
- (b) reduce trust-and-safety capacity below the workload formula in B-13.1, or below 0.5 FTE, or combine it with the outreach role;
- (c) cut by more than half, relative to the prior 6 months, the outreach that brings in paying organisations and institutions;
- (d) cut the research panel below 1% of operating expenses (B-12).

↳ v3 c.3 "can never cut the floor, T&S below its workload formula, or the outreach"; c.4 item 6 · Rows 3, 5, 12 · blocks austerity as a pretext for re-segmenting the free tier

**C-12.4 Staff gates.** The Corporation takes a staffing step only when trailing 6-month Committed Inflow covers the new payroll plus fixed costs plus the legal and compliance line of at least $30,000 a month (2026 dollars, indexed).
↳ v3 c.4 item 3 · Row 21 · blocks growth on hope

### Article C-13: Tax-exempt provisions

**C-13.1** Notwithstanding any other provision, the Corporation shall not carry on any activity not permitted to an organisation exempt under IRC §501(c)(3). **Where a tax provision and an Entrenched Clause both apply, both are obeyed. If they truly conflict, the Corporation withdraws the activity; it does not weaken the Entrenched Clause.**
↳ K9 · Row 13 · blocks "the IRS made us" as a lever to weaken

### Article C-14: Dissolution and distribution (Plan D)

**C-14.1** On dissolution, after paying or providing for its liabilities, the Corporation shall:
- (a) carry out Plan D (Trust Agreement T-12.3), including the 90-day export and deletion of all Data with receipts;
- (b) release all code and specifications openly;
- (c) distribute all remaining assets to one or more organisations then exempt under IRC §501(c)(3) whose purpose is open digital infrastructure, chosen under T-12.6, or to a Successor Steward.

**No asset, and no Data, may be sold or otherwise Transferred for value to any person.** Any asset not so disposed of shall be disposed of by the Court of Chancery exclusively for such purposes. [This satisfies Treas. Reg. §1.501(c)(3)-1(b)(4); counsel to confirm that the "never for value" limit is compatible with paying creditors.]
↳ v3 c.3 Plan D; IRS dissolution-clause requirement · Row 21 · blocks a liquidation sale

### Article C-15: Severability, and failure closed

**C-15.1** If any provision is held invalid, it is replaced by the enforceable provision nearest to its protective effect.
↳ v3 c.3 · Row 13

**C-15.2** Any act in breach of a prohibition in Articles C-8 to C-12 is void and ultra vires, to the extent the law allows.
↳ v3 c.3 · Row 13

**C-15.3** If any required approval cannot lawfully be given or obtained, the matter is prohibited. It does not become permitted without that approval.
↳ v3 c.3 · Rows 13, 21 · blocks "the lock is invalid, so no lock"

### Article C-16: Forum; the two vehicles

**C-16.1 Forum.** The Court of Chancery of the State of Delaware is the exclusive forum for any claim concerning this Certificate, except claims within the exclusive jurisdiction of a federal court.
↳ v3 c.3 · Row 7

**C-16.2 Two vehicles.** The Corporation shall not hold, fund, govern or affiliate with any religious, philosophical or teaching vehicle. The Service carries no seed text in any product or marketing surface.
↳ v3 c.3; c.2.6 · Row 19; operator decision 2 · blocks the seed being planted by stealth through the product

---

## PART II-B — PROTECTED BYLAW PROVISIONS

*Adopted under 8 Del. C. §109. Bylaws B-1 to B-16 are "**Protected Bylaws**". They are amendable only as Locked Matters (C-9.1(a)), or by a Ratchet Change.*

**B-1 Credentials.** A person is a Credentialed Member if either:
- (a) the person has held an account for at least 180 days, and attendance at gatherings has been confirmed by at least 2 distinct hosts, neither of whom is in any of the voter's own circles; or
- (b) the person has held a host key for at least 365 days, with 1 such confirmation.

Credentials are issued as blind tokens: the Corporation can verify that a vote came from a credential but cannot link the vote to the person. Hosts may confirm only real responses to past public or series cards.
↳ v3 c.3 "Voting credentials" · Row 6 · blocks Sybil capture of the Council (Run 1 X35)

**B-2 Council votes.**
- One credential, one vote.
- Voting stays open for at least 14 days.
- Turnout is Published.
- **A turnout below 5% voids a Council veto of a Ratchet Change, but never lowers the threshold for approving a Weakening Change.**

↳ v3 c.3; Run 1 b.6.5 · Row 13 · blocks turnout games

**B-3 Petitions.**
- 1% of Credentialed Members may require a reasoned Published response within 30 days, and may act as Council Petitioners under the Trust Agreement.
- 5% may require a binding Council vote on any matter that is not a Locked Matter.

↳ v3 c.3 "Petitions" · Rows 6, 13

**B-4 Concentration alarm.** If 10 hosts confirm more than 15% of new credentials in a quarter, issuance from those hosts is frozen pending review by the Sortition Jury, and the fact is Published.
↳ v3 c.3 "Concentration alarm" · Row 6

**B-5 Sortition Jury.** 15 paid members, chosen by lot from Credentialed Members for staggered 1-year terms, make binding harm-gate decisions. The board cannot override them for any growth, revenue or partner reason.
↳ v3 c.3 "Sortition jury"; c.10 H10 · Rows 3, 6, 9

**B-6 Staggering.** The Council-elected directors, TSC seats and Veto Foundation seats are staggered so that no single annual election can change more than one seat in each body, with the offsets that T-5.3 and V-2.2 require.
↳ v3 c.3 "staggered by 18 months" · Row 6

**B-7 Public Notice mechanics.** Public Notice under D-29 is given in every language in which the Service is offered, in plain language, with a diff. It includes the text of every Interpretive Determination on the proposal.
↳ v3 c.3 lock 5 · Rows 8, 13

**B-8 Open-Books Metrics (closed list).** The only Data disclosed to anyone is this list, published quarterly to everyone at once:
- revenue by source class and largest-source share;
- expenses;
- Runway on Actual Burn;
- staff count and the pay ratio;
- the notification ratio;
- the covenant zeros;
- transparency-report counts;
- the metric counts in v3 c.6, aggregated under D-4 with k ≥ 50.

Adding a metric is a Locked Matter. Removing one is a Ratchet Change.
↳ v3 cl. 2; c.6 · Rows 2, 4 · blocks "we just share a few stats with partners"

**B-9 Gift acceptance.**
- (a) No gift, grant, fee or other funding may carry any condition, Data, seat, product, pricing or governance right.
- (b) After year 1, no donor may exceed 25% of a year's inflow, and no institution may exceed 10% of a year's revenue.
- (c) All gifts above $[●] are Published.
- (d) Every gift instrument contains the A-3 and A-5 terms.

↳ v3 c.4 "What pays" · Row 6 · blocks advertisers and funders as government (dossier pattern)

**B-10 Claims.** The Corporation keeps a claims register and a "who can read what" table. These are the only permitted sources of any public privacy or security claim, used word for word. A claims linter blocks unqualified "end-to-end encrypted" and any "tax-deductible" claim the Corporation cannot honour.
↳ v3 c.2.5 Compliance; FTC §5 (Zoom, 2020) · Row 4 · blocks the claims that invite deception enforcement (Run 3 LK1)

**B-11 Audits and incidents.**
- (1) The CI lint on Ordering and Notification, the 10c audit, a data-flow audit, the per-user event-table schema audit and the zero-third-party-request test run on every release.
- (2) An independent auditor reviews the covenant zeros every 6 months.
- (3) Any non-zero covenant zero, any Plaintext path outside E12, or any E10a–c bypass is disclosed publicly within 72 hours.

↳ v3 c.2.4 items 4, 5, 11; c.10 H7, K10 · Rows 1, 10, 19, 24

**B-12 Research panel.** An opt-in, pre-registered, randomly sampled panel of consenting members is funded at no less than 1% of operating expenses. Its results are published within 12 months, whatever they find.
↳ v3 c.2.5 research panel · Row 3 · blocks "knowledge without action" and structural ignorance (L22)

**B-13 Trust and safety.**
- (1) T&S capacity follows a Published workload formula, with a floor of 0.5 FTE, never held by the outreach lead. Moderators are direct employees, with exposure caps and clinical support.
- (2) The neutral abuse limits under E4.2 are: 150 responses per no-account card; 20 new cards per new host per day; 1 Commons entry per series and at most 3 per host per day; [●].
- (3) Language parity: T&S capacity in each language is at least that language's share of users.

↳ v3 c.3; c.2.5; c.5 rows 8, 12 · Rows 8, 12, 14, 15

**B-14 Jurisdiction register.** A named owner keeps a jurisdiction register, reviews it quarterly and Publishes its review date. Launch happens only where the legal floor is funded.
↳ v3 c.2.5 · Rows 7, 8

**B-15 Protected Bylaws.** B-1 to B-16 and this B-15 are Protected Bylaws.
↳ v3 c.3 · Row 13 · blocks moving protections into ordinary bylaws and then amending them

**B-16 Director Covenant.** Every director signs a covenant to comply with Articles C-8 to C-12. The covenant also sets conflict tests: no Related-Party Interest; no role with any incumbent platform, advertiser, data broker or lender to the Corporation; no donor above 1% of inflow.
↳ v3 cl. 7a; c.4 item 1 · Row 6

---

## PART III — VETO FOUNDATION: PROVISIONS ITS OWN CERTIFICATE MUST CONTAIN

*[VETO FOUNDATION] is a Delaware nonstock corporation. Its certificate must contain V-1 to V-8. V-3 and V-5 are amendable only with the Backup Enforcer's written consent and a Council vote, and V-3.1 is not amendable at all.*

**V-1 Purpose.** The Foundation's purposes are limited to:
- acting as enforcer of the [●] Stewardship Trust;
- holding the Class V membership of the Operator;
- holding and licensing the marks, domains and code copyright under V-5;
- holding one of three release keys;
- controlling the Enforcement Reserve.

↳ v3 c.3 "Veto Foundation" · Rows 7, 13

**V-2.1 Board, and who chooses it.** The board has 5 directors:
- (a) 2 elected by the Council of the Operator under B-1 and B-2;
- (b) 3 appointed by [three named independent civil-liberties, digital-rights and consumer bodies], one each.

**No director is appointed by the Trust, the Committee, the Administrative Trustee, the Operator or the Settlor.**
↳ v3 c.3 "Successors … by election or by a named independent body, never by the trustees" · Row 6 · blocks Run 2 A15 and enforcer capture (RT3)

**V-2.2 Staggering; conflicts.**
- Terms are 3 years, staggered, and offset by 18 months from the TSC's Council seats.
- No director may be a director, officer, employee, donor above 1%, lender or counterparty of the Operator, or a Committee member, or a Family Member of one.

↳ v3 c.3 · Row 6

**V-3.1 Never consent to changing the unamendable.** The Foundation shall never consent to any change to any Unamendable Provision (C-9.5). **This V-3.1 is not amendable.**
↳ v3 cl. 11 · Rows 19, 22 · closes G9

**V-3.2 Consent requires 4 of 5.** The Foundation consents to a Locked Matter only by resolution of 4 of its 5 directors, with Published reasons, after the Operator's 90-day notice has run.
↳ v3 c.3 lock 3 · Row 13 · blocks a bare majority of a captured board giving consent

**V-4 No economic benefit.** The Foundation receives from the Operator only:
- the Enforcement Reserve through the escrow (A-3);
- fee advancements under A-2;
- a Published licence-administration fee no greater than cost.

Its directors receive Published stipends only.
↳ v3 c.3; Run 1 X14 · Rows 6, 7

**V-5 The IP.**
- (a) The Foundation owns the marks, all card domains and the code copyright not released under open licences.
- (b) It licenses them to the Operator only on the A-1 terms (non-exclusive, non-assignable, personal).
- (c) It shall not assign, pledge or exclusively license any of them. It licenses the marks to any other person only under a Published trademark policy limited to hosts that comply with Schedule A. **RT-fix.**
- (d) On its own dissolution, the IP passes only to a successor enforcer appointed under T-7.6.

↳ v3 c.3 "owns the marks, all card domains and the code copyright, licensed … non-exclusively and non-assignably" · Rows 20, 21 · blocks the licensing deal (RT10) and a captured Foundation licensing the brand to a clone that does not comply

**V-6 Release keys.** The Foundation holds one of three release-signing keys. It shall not sign any release that its own review finds breaches Articles C-8 to C-12.
↳ v3 c.3 "holds 1 of 3 release keys"; c.7 · Rows 1, 19 · blocks shipping a reversal in the client

**V-7 The Backup Enforcer as a check.** Any act by the Foundation that the Backup Enforcer determines to breach V-1 to V-6 is suspended until the Court of Chancery rules on it.
↳ v3 c.3 backup enforcer · Row 7 · blocks RT3

**V-8 Dissolution.** The Foundation may dissolve only after a successor enforcer is appointed under T-7.6 and has received the IP and the Enforcement Reserve.
↳ v3 c.3 · Rows 7, 21

---

## PART IV — MEMBER PRIVACY COVENANT (the protected part of the privacy policy)

*Plain language for members and guests. It is also a binding promise. It is shown, or linked in one tap, **every time anyone gives us any information**: on each card's response form, each re-entry code, host-key creation, reminder sign-up and gift page. That makes it a policy "disclosed to an individual" "in connection with offering a product or a service" under 11 U.S.C. §363(b)(1). It is a Protected Bylaw (B-15) and is mirrored in Entrenched Clause E9b.*

**P-0.1 What this is.** This is our promise to you about your information. It is a contract between you and [OPERATOR], Inc. It is part of our certificate and of our steward's trust deed, so we cannot quietly change it (P-11). It applies to members, organisers and guests alike, **whether or not you have an account**.
↳ v3 cl. 9b · Row 21 · makes the policy binding and visible to guests who consented to nothing else (Run 3 CV1)

**P-1 Who can read what.** The "who can read what" table at [link] lists exactly what we, and anyone we work with, can read. It is the only place our privacy claims come from. If anything else we say disagrees with it, the table is right, and we will fix the other statement.
↳ v3 c.2.5; FTC §5 (Zoom, 2020) · Row 4 · blocks deceptive E2EE claims (Run 3 LK1)

**P-2 We cannot read your private things.** Your private cards, circle text, notes and responses are encrypted with keys that live on your devices. We do not hold them in readable form. We are not allowed to (E12). The only things we can read are:
- (a) what you publish to the public;
- (b) what someone submits to us in a report;
- (c) if you turn on a calendar feed, a time and a generic title such as "Circle gathering", and nothing else;
- (d) an email or phone number you give us for reminders to yourself.

↳ v3 cl. 12 · Rows 2, 19 · blocks QR1

**P-3 We do not sell or share. Ever.** We never sell, rent, license, trade or give away any information about you, or about groups or gatherings. That includes:
- lists;
- counts and statistics;
- "anonymised" or "aggregated" data;
- metadata such as who responded when;
- anything worked out from your use.

Nobody gets privileged access to it. The only exceptions are in P-6.2.
↳ v3 cl. 2 · Rows 2, 21 · blocks "insights" and "anonymised" data deals (Run 1 X1)

**P-4 No ads, no profiles, no scanning.** We show no ads. We do not profile you, score you, rank you, or scan or classify your content, on our servers or on your device (E1, E11).
↳ v3 cl. 1, 11 · Rows 2, 19, 22

**P-5 Organisations cannot track you.** A group or organisation you belong to can see who said yes to one gathering. It cannot see your attendance over time, whether you have gone quiet, or any other measure of your behaviour (E10c).
↳ v3 cl. 10c · Row 24

### P-6 The anti-transfer promise

*This is the clause 11 U.S.C. §363(b)(1) looks for. It is written to be in effect on any date a bankruptcy case could begin, to cover affiliates as well as outsiders, and to reach beyond the Bankruptcy Code's narrow "PII" list.*

**P-6.1 No transfer, including in a sale or bankruptcy.** We will **not** sell, lease, license, rent, assign, transfer, disclose, or otherwise make available, **any of your personal information or any other data about you or about any group or gathering**, to **any person, whether or not that person is affiliated with us**, for any reason. That includes any:
- merger, consolidation, conversion or change of control;
- acquisition, or sale or lease of any assets;
- financing or security arrangement;
- assignment for the benefit of creditors, or receivership;
- dissolution or wind-down;
- **case under title 11 of the United States Code or any other insolvency law**.

It also covers any purchaser, assignee, lender, trustee, receiver, examiner, liquidator or successor of ours.
↳ v3 cl. 9b · Row 21 · written to trigger §363(b)(1)'s "policy prohibiting the transfer of personally identifiable information"; the words "whether or not affiliated" close G5(ii)

**P-6.2 The only exceptions.** We make information available only:
- (a) **to you**, or where you tell us to send it (for example your export, or a message you send);
- (b) **to a service provider** working only for us under a written contract (A-6), for one purpose: running the Service for you. It may not use the information for anything else, and it may never see your private content in readable form;
- (c) **when the law forces us**, and then only what we already hold. We challenge the demand wherever reasonable grounds exist and tell you unless the law forbids it (P-8). This is never a sale, never voluntary, and never a reason to build a way in (E11);
- (d) **to a Successor Steward**, only if **all** of these are true:
  - (i) it meets every test in D-22, including that it has the same trust deed and charter as ours and pays **nothing** for your information;
  - (ii) we have told you in advance;
  - (iii) **you personally and affirmatively say yes**.

  **If you do not say yes, your information is deleted, not moved. Silence is never consent.**

↳ v3 cl. 9b ("except to a successor steward under an identical deed and then only for members who opt in") · Row 21 · blocks G8 (a shell successor buying the data as a sale "consistent with" the policy)

**P-6.3 This promise is always in effect.** This P-6 is in effect from the moment you first give us any information. It remains in effect, **unchanged in any way that would permit any transfer**, on any date on which any case concerning us is commenced. No version of our privacy policy has ever permitted, or will ever permit, any transfer beyond P-6.2.
↳ v3 cl. 9b · Row 21 · closes G5(iii) (§363(b)(1) looks at the policy "in effect on the date of the commencement of the case")

**P-6.4 It cannot be weakened.** Any change that would allow more transfer than P-6.2 is void. A change to any other part of this Covenant (i) applies only to information collected after the change, (ii) applies only if you expressly opt in, and (iii) can never apply to this P-6.
↳ v3 cl. 9b; C-9.5(b), C-9.8 · Rows 13, 21 · blocks amending the policy just before a filing (the Toysmart/RadioShack pattern)

**P-6.5 We hold your information for you.** We hold your personal information and content **only as your custodian and agent**, to provide the Service to you. **We have no ownership or beneficial interest in it.** It is not ours to sell, and it is not our asset (E9). [counsel: whether this is enough to keep the beneficial interest outside the estate under 11 U.S.C. §541(d).]
↳ v3 cl. 9 · Row 21 · a second route beyond §363(b)(1), covering data outside §101(41A) (G5(i))

**P-6.6 Deletion, not transfer.** If we ever wind down, you get **90 days to export** your information and your circles, and then we **delete everything**, with receipts. We start this *before* we run out of money, not after (S-8). If a bankruptcy case begins before deletion is finished, we will ask the court at once for permission to delete or return your information, and we will oppose any sale of it.
↳ v3 cl. 9b · Row 21 · handles G7 (post-petition deletion needs court authority)

**P-6.7 This binds anyone who takes over.** Anyone who becomes responsible for our affairs takes them subject to this promise. We make it a term of every contract under which anyone could come to hold your information (A-4, A-6).
↳ v3 cl. 9b · Row 21 · blocks a successor claiming it isn't bound

**P-6.8 Who can enforce this.** You can. So can our steward's enforcers ([VETO FOUNDATION] and [BACKUP ENFORCER]), each of whom is an intended third-party beneficiary of this promise. Breaking it would also be a deceptive practice under Section 5 of the FTC Act and state law. Those are laws a bankruptcy court must consider before approving any sale (§363(b)(1)(B)(ii)).
↳ v3 cl. 9b; L3 · Rows 7, 21 · builds the "applicable nonbankruptcy law" record for any ombudsman hearing (Toysmart logic)

**P-7 This covers more than the law's narrow list.** Bankruptcy law's list of "personally identifiable information" is short: names, home addresses, emails, home phones, and a few numbers. **Our promise covers all data about you**, including your display name, re-entry codes, keys, network addresses, responses, the groups you are in, and statistics that include you, and it covers organisations' data too.
↳ v3 cl. 2, 9b · Row 21 · closes G5(i)

**P-8 When the government asks.** We give only what we already hold. It is very little, because we cannot read your private content and we keep logs for 7 days. We require proper legal process, challenge demands that are too broad, tell you unless the law forbids it, and publish a transparency report twice a year. We will never build a way for anyone to read what we cannot read (E11).
↳ v3 c.7 "Legal compulsion" · Row 7 · blocks compelled capability (QR3)

**P-9 How long we keep things.**
- Reminder contacts: until 24 hours after the event.
- Email for updates: until 90 days after you last use it.
- Billing links: until 90 days after you stop giving.
- Server logs: 7 days, truncated.
- No-account link data in Commons Mode: 90 days.

These periods can only get shorter.
↳ v3 c.2.5 · Rows 2, 21

**P-10 Your controls.** You can export everything in one step, delete anything, and leave, taking your circles with you.
↳ v3 c.2.4 item 8 · Row 20 · covenant: "Could they leave without losing the relationships they formed?"

**P-11 Changes.** We give 90 days' notice of any change, with a plain diff. Changes can only make this Covenant **stricter**, except through the process in our certificate (all five locks). Even then, a change never reaches information collected before it, and never touches P-6.
↳ v3 c.3 · Row 13

**P-12 Children.** Host keys are for adults. If we learn that a guest under 13 has given us information, we delete it.
↳ v3 c.5 row 11 · Row 11

**P-13 Complaints.** Contact [●]. You can also contact our steward's enforcer at [●], or your state attorney general or the FTC.
↳ v3 c.3 · Row 7

---

## PART V — JOINT RESOLUTION ON THE START GATE, COMMONS MODE AND OPERATING MODES

*Adopted by the Operator's board and approved by the Class T member (on the Committee's direction) and the Class V member, as a Charter Obligation under C-12. It is a Protected Bylaw.*

**RECITALS.** Four independent funding models, run across three design runs, show that under any externally anchored supporter rate (about Signal's 0.2–0.5% of active users) earned revenue never covers costs. This is a donor- and institution-funded public utility, indefinitely (BLUEPRINT v3 c.4, L1). No funder has committed. The Corporation must therefore fail safely if the money does not come: by public shrinkage, **never by quiet extraction or a creditor's sale**.

**RESOLVED:**

**S-1.1 Formation Budget.** The "**Formation Budget**" is $90,000 (2026 dollars). It covers forming the Trust, the Corporation and the Veto Foundation, the Form 1023, name clearance, and counsel's opinions for K7 and K9.
↳ v3 c.4 item 1 ("Nothing beyond formation (about $90k)") · Row 21

**S-1.2 Gate Amount.** The "**Gate Amount**" is the lean-phase cost from month 0 to the month-18 gate, plus 12 months of caretaker-mode cost. It is computed from the Published budget, with the legal and compliance line at no less than $30,000 a month, and with no revenue assumed from supporters, organisations or institutions. It is estimated at about $2.3 million and is Published before any certification.
↳ v3 c.4 item 1 ("about $2.3M") · Row 21 · blocks the Run 3 plan that counted revenue it had not got

**S-1.3 Non-controlling Commitment.** A commitment counts toward the Gate Amount only if **all** of these hold:
- (a) it is in writing, signed by a person with authority, and irrevocable except for the Corporation's material breach of an Entrenched Clause as found under C-10 or by a court;
- (b) it carries no condition, Data, seat, product, pricing, governance, information or consent right, and no right beyond the Published ledger;
- (c) it is not Debt, or, if it is Debt, it meets E9a and A-4 **and** is forgiven on a solvent wind-down;
- (d) it is payable on a fixed schedule not conditioned on any metric of the Service;
- (e) after year 1 it keeps the donor within the 25% cap under B-9, or is covered by a Published year-1 exception;
- (f) it contains the A-3 and A-5 terms.

↳ v3 c.4 item 1 ("signed, non-controlling commitments"); "What pays" · Rows 6, 21 · blocks a funder buying control through the gate (the dossier's funder-as-government pattern)

**S-2 Spending freeze until the gate.** Until Gate Certification, no officer or director may incur, commit or authorise any expenditure, hire, lease, contract above $5,000, or Debt, beyond the Formation Budget. Any contract made in breach is void as against the Corporation to the extent the law allows, and its signers are personally in breach of C-12.1.
↳ v3 c.4 item 1; K11 · Row 21 · blocks "just start building, and the money will come"

**S-3 Gate Certification.** The gate is met ("**Gate Certification**") when:
- (a) Committed Inflow is at least the Gate Amount;
- (b) an independent accountant has examined each counted commitment against S-1.3;
- (c) two-thirds of the whole board so resolve;
- (d) the certification, the accountant's report and the list of commitments (with donors' names where they consent, and amounts in every case) are Published;
- (e) within 30 days neither the Veto Foundation nor the Backup Enforcer issues an Interpretive Determination that a counted commitment fails S-1.3.

↳ v3 c.10 K11 ("The start gate is met with signed letters") · Rows 4, 21

**S-4.1 Commons Mode.** If Gate Certification has not occurred by the end of month 3 after formation (the "**Gate Deadline**"), the Corporation enters Commons Mode. The Gate Deadline may be extended once, by up to 3 months, with Public Notice. In Commons Mode the Corporation operates **only**:
- (a) publication and maintenance of the open card and circle specification;
- (b) the AGPL reference server;
- (c) a minimal link service. Its links are ciphertext only, expire after 90 days, need no accounts and carry no media. It has at least 0.5 FTE of trust and safety;
- (d) the governance, audit and transparency functions these instruments require.

**No roster, response or other Data is held for more than 90 days.** No host keys, circles, SMS, email relay or paid features are offered.
↳ v3 c.4 item 1 ("If the gate is not met, the project is Commons mode"); modes table · Rows 21, 22 · blocks a project that begins, hires, and dies at month 14 holding people's rosters

**S-4.2 Cost cap.** Commons Mode spending shall not exceed $355,000 a year (2026 dollars, indexed) without a Council vote.
↳ v3 c.4 ("about $355k a year") · Row 21

**S-4.3 Publication.** Entry into Commons Mode is Published within 5 business days, in plain words: "The money needed to build the full service safely did not arrive. We are running the open specification, the reference server and a minimal link service instead." It is not described as a pause, a pivot or a success.
↳ v3 c.10 K11 ("Commons mode, published"); honesty standard · Row 4 · blocks spin

**S-5 Commons Mode is not impracticability.** Commons Mode attains the Purpose (Trust Agreement T-2.3). It is never a ground for modifying the Trust, selling any asset, or taking any funding that fails S-1.3.
↳ v3 c.4; T-2.3 · Row 21 · blocks using Commons Mode as the pretext for a §3541 petition (RT4)

**S-6 Leaving Commons Mode.** The Corporation leaves Commons Mode only by a later Gate Certification under S-3.
↳ v3 c.4 · Row 21

**S-7 Commons Mode runway.** If, in Commons Mode, unrestricted cash plus Committed Inflow falls below 12 months of Commons Mode cost, and no Non-controlling Commitment closes the gap within 60 days, the Corporation enters Plan D.
↳ v3 c.4 Mode D trigger (adapted) · Row 21

**S-8.1 Operating modes after the gate.** After Gate Certification, the mode is set **only** by Runway on Actual Burn (D-25), recomputed monthly and Published:

| Runway | Mode | What happens |
|---|---|---|
| < 18 months | **B: freeze** | No new hires, no new regions |
| < 12 months | **C: caretaker** | Reduced to the caretaker budget (about 5 staff, about $1.2M a year); **every Free Floor Function keeps running** |
| < 6 months, **or** Committed Inflow is below 12 months of caretaker cost with no bridge meeting E9a within 60 days | **D: orderly handover (solvent)** | See S-8.2 |

↳ v3 c.4 "Pre-committed modes (on trailing actual burn)" · Row 21 · blocks Run 1 X13 (modes triggered by a plan that leadership writes)

**S-8.2 Mode D.** In Mode D the Corporation shall:
- (a) Publish the entry;
- (b) start the 90-day export drill for every Member and circle, with self-host packages;
- (c) transfer the static-archive duty (cards resolving for 5 years) to the Trust's funding under T-11.3;
- (d) seek a Successor Steward under D-22;
- (e) at the end of the window, delete all Data with receipts, except Data individuals affirmatively opted in to move;
- (f) pay creditors;
- (g) proceed to Plan D.

↳ v3 c.4 Mode D; cl. 9b · Rows 20, 21 · blocks insolvency with data still on hand (G7)

**S-8.3 No mode cuts the protected lines.** C-12.3 applies in every mode.
↳ v3 c.3 · Rows 3, 5, 12

**S-8.4 Deletion happens before any filing.** The deletion in S-8.2(e) shall be completed before any petition under title 11 is filed, unless C-11.1(b) applies.
↳ v3 cl. 9b · Row 21 · G7

**S-9 Growth gates.**
- (a) **Month 18:** at least 25 signed institutions **or** a measured supporter share of at least 0.5%, **and** H1b passing. Otherwise the Corporation enters Mode C.
- (b) **Month 36:** supporter share at or above the variable-cost line (about 0.74%), or growth is capped by region until it is.
- (c) Every staffing step meets C-12.4.

↳ v3 c.4 items 3–5; c.10 H13 · Row 21 · blocks growth that loses money per user while the fundraising story holds

**S-10 Modelling rules.** Every financial model the Corporation publishes or gives to a funder:
- (a) stops at cash below zero, and reports no break-even month after that;
- (b) never halves the institution-bringing outreach in any austerity mode;
- (c) includes a run at a supporter rate of 0.5% or below (the Signal anchor).

↳ v3 c.4 item 6 · Row 4 · blocks the Run 3 model defects (break-even reported after death; ember mode halving the revenue engine)

**S-11 K11 reporting.** The Corporation Publishes, each quarter until Gate Certification or Plan D, the Committed Inflow, the Gate Amount and the gap.
↳ v3 c.10 K11 · Row 4

**S-12 Direction.** The Committee directs the Administrative Trustee to approve this Resolution as the Class T member. The Veto Foundation consents to it as the Class V member. Amending it is a Locked Matter; tightening it is a Ratchet Change.
↳ v3 c.4 item 1 · Row 13

---

## PART VI — MANDATORY TERMS OF ANCILLARY INSTRUMENTS

**A-1 IP licence (Veto Foundation to the Operator).** The licence of marks, domains and code copyright:
- (a) is **non-exclusive, royalty-free and personal** to the Operator;
- (b) is **non-transferable and non-assignable, including by operation of law, merger, conversion, change of control, or in any case under title 11**. The Licensor states that it relies on the Operator's identity and would not accept performance from any other person (supporting 11 U.S.C. §365(c)(1): *In re Catapult Entertainment*, 165 F.3d 747 (9th Cir. 1999); *In re XMH Corp.*, 647 F.3d 690 (7th Cir. 2011), trademark licences not assignable without express authorisation);
- (c) cannot be sublicensed, except to processors for hosting;
- (d) requires use only in compliance with Schedule A;
- (e) terminates, to the extent the law allows, on any purported assignment, any breach found by Interpretive Determination, and any Transfer of Data [counsel: §365(e)(1) ipso facto limits; the §365(e)(2)(A) exception];
- (f) confers no right to use the marks on any service not bound by Schedule A.

↳ v3 c.3 "licensed … non-exclusively and non-assignably, so under §365(c)(1) … cannot be assumed and sold" · Rows 20, 21 · blocks RT5 (selling the brand out of the estate) and RT10

**A-2 Enforcement Agreement (Operator, Veto Foundation, Backup Enforcer, Trust).**
- (a) The Operator agrees to advance the reasonable costs of good-faith enforcement actions by either enforcer, repayable only on a final finding of bad faith. This is a contract, not a charter provision [Run 1 b.6.3 used a contract because of DGCL §102(f); counsel: whether §102(f) matters for a nonstock corporation].
- (b) The Backup Enforcer receives the rights in C-10.2 as an intended third-party beneficiary.
- (c) The Operator's obligations survive any mode.

↳ v3 c.3 enforcement reserve; Run 1 b.6.3 · Row 7 · blocks Run 1 X14 (starving the enforcer)

**A-3 Enforcement Reserve: donor-direct designation and escrow.** RT-fix.
- (a) Every gift instrument (A-5) and every institution agreement **designates 2% of the payment to be paid by the payer directly to [ESCROW AGENT]** for the Enforcement Reserve. That share never becomes the Operator's property.
- (b) Card and processor settlement is split at source where practicable. Where it cannot be split, the Operator holds the 2% **as trustee for the escrow**, in a segregated account, remitted within 10 business days.
- (c) The reserve is capped at $1,000,000 (2026 dollars, indexed). Above the cap, the designation lapses and the full payment goes to the Operator.
- (d) Only the Veto Foundation or the Backup Enforcer may draw, and only on filing or defending a proceeding about the Trust, the Certificate or the Privacy Covenant.

↳ v3 c.3 "escrowed enforcement reserve: 2% of inflows up to $1M, indexed, drawn only on a court filing" · Row 7 · blocks G6 (clawback of an operator-paid reserve under §548 or §544(b)) [counsel: whether the designation survives recharacterisation, and whether it affects donors' deductions]

**A-4 Every Debt instrument shall state:**
- (a) the lender takes subject to Articles C-8 to C-12 and the Privacy Covenant;
- (b) there is no security over the assets in E9a.1(a), and a negative pledge on them;
- (c) there is no covenant, information right, consent right or event of default relating to product, pricing, Data or governance;
- (d) for a bridge, repayment comes **only from surplus** above the 18-month reserve, and the debt is forgiven on a solvent wind-down;
- (e) there is no acceleration except for fraud;
- (f) **the note may not be assigned or participated to any person without the Operator's consent. Any assignee takes subject to all of the above, and an assignment to any incumbent platform, data broker or person acting for one is void.**

↳ v3 cl. 9a; c.8 ("Buy the debt: clause 9a leaves nothing securable") · Row 21 · blocks Run 2 A11.6 (an incumbent-friendly fund buys the note)

**A-5 Every gift, grant and institution agreement shall state:**
- (a) it confers no Data, seat, product, pricing, moderation or governance right, and no attribution line (E1.3);
- (b) its purpose restriction is the Operator's purposes **as limited by the Entrenched Clauses**, with the alternate purpose, if that fails, being the Plan D recipients under T-12.6;
- (c) the donor may revoke only for the Operator's breach of an Entrenched Clause;
- (d) the A-3 designation.

↳ v3 c.4 "What pays" · Rows 6, 21 · blocks funder control, and narrows any cy pres of restricted gifts (UPMIFA, 12 Del. C. §4706 [verify]) toward Plan D (RT6)

**A-6 Every processor contract shall state:**
- (a) the processor acts only on the Operator's instructions, for the Service;
- (b) it has no right to use Data for its own purposes, including training;
- (c) it shall not receive Plaintext outside E12;
- (d) it deletes on instruction and on termination;
- (e) **Data is not the processor's property in the processor's own insolvency**, and the processor may not Transfer it;
- (f) P-6 binds it.

↳ v3 cl. 2, 12 · Rows 2, 19, 21 · blocks leakage through vendors, and a vendor's bankruptcy

**A-7 Every institution agreement shall state:** no member analytics (E10c); no attribution line (E1.3); no product or moderation rights; the 10% cap (B-9).
↳ v3 c.4 Institutions; cl. 10c · Row 24 · blocks payer surveillance (Run 3 X1)

---

## ANNEX B — WHAT CHANGES UNDER STRUCTURE B (the PBC fallback; only if counsel so advises)

*Summary only. Not drafted as clauses; excluded from the clause count.*

- The operator becomes a Delaware public benefit corporation (8 Del. C. §§361–368). Its specific public benefit is Schedule A, quoted in full, and Article C-8 applies as the certificate's protective provisions.
- Authorised stock is exactly 49 Class A voting shares, held by the Trust, and 1 Class G share, held by the Guardian (the Veto Foundation in this role), with §202 transfer restrictions [verify §367 standing threshold (2%) and the effect of 1 of 50 shares].
- C-9's locks become class votes under §242(b)(2), plus an express Class G consent right on every Locked Matter.
- **What is lost:**
  - §303(a)'s bar on involuntary cases (a PBC is a business corporation);
  - §363(d)(1), §541(f) and §1129(a)(16)'s protection of charitable restrictions (G11);
  - deductibility of gifts, and therefore v3's funding model;
  - the attorney general as a second guard.
- **What must be added:** a lock on creditor-initiated insolvency (only 9a, the negative pledge and the solvent wind-down remain), and an Enforcement Reserve funded directly into the trust.

---

## PART VII — RED TEAM: can the text stop a quiet reversal?

**Method.** For each scenario I play the attacker **against this text**, not against v3's summary. I looked for the cheapest lawful route to reversal: which body must act, which instrument must change, and which statute gives a way around. Verdicts:
- **STOPPED**: the text closes every route I found, subject only to the text being enforceable (a counsel question listed in Part VIII).
- **PARTLY**: at least one lawful route remains, which the text narrows, slows or makes visible.
- **NOT STOPPED**: the text cannot reach the route.

Where the first draft failed, I **fixed the text** (marked RT-fix above) and give the verdict after the fix. The first-draft verdict is shown in brackets.

### Summary

| # | Scenario | Verdict (after fixes) | First draft | Clauses that do the work |
|---|---|---|---|---|
| RT1 | Future leadership **re-reads** a rule ("relevance search", "re-engagement is care", "anonymised insights") | **STOPPED** | STOPPED | D-0.1, D-3, D-4, D-10–D-12, E2, E10a–c, C-10.2, T-8, B-11 |
| RT2 | Future leadership **erodes E2EE** through a default-on helper or client code | **STOPPED** (text); detection PARTLY | PARTLY | D-7, D-9, E12, C-9.1(k), B-11(3), V-6 |
| RT3 | **Captured enforcer** (the Veto Foundation's board is captured) | **PARTLY** | NOT STOPPED | T-7.2, T-7.3, T-7.8, T-8.2, T-8.6, C-10.3, V-2.1, V-3.2, V-7, T-15.3 |
| RT4 | **Court petition**: "the purpose is impracticable; approve a sale to an aligned buyer" | **PARTLY** (STOPPED in Chancery on the statute's terms) | PARTLY | T-2.3, T-7.5, T-12.1–T-12.5, S-5 |
| RT5 | **Bankruptcy trustee** sells the data, the brand and the domains | **PARTLY** | PARTLY | C-11.1–C-11.5, E9, E9b, P-6, P-7, A-1, S-8.4, T-11.4 |
| RT6 | **State attorney general**: the OpenAI path; cy pres of charitable assets; a data demand | **PARTLY** | PARTLY | T-6.1, C-9.2, C-11.4, A-5(b), E11, P-8 |
| RT7 | **Friendly acquirer**: a mission-aligned merger, management agreement or member substitution | **STOPPED** (short of collusion by all five locks, RT17) | PARTLY | C-5.1, C-9.1(c)–(f), T-3.3, T-6.1(c), T-12.4, D-22 |
| RT8 | **"Safety" amendment**: client-side scanning as a "stricter protection" | **STOPPED** | STOPPED | D-18–D-20, D-27, E11, C-9.5, C-9.6, V-3.1 |
| RT9 | **Subsidiary**: an "Insights LLC" with outside equity, or moving the product into a subsidiary and selling it | **STOPPED** | PARTLY | D-8, E7b.1, C-9.1(d), (g) |
| RT10 | **Licensing deal**: exclusive licence of the spec, marks or data; brand licensed to a clone | **STOPPED** | PARTLY | E2, E7b.2, V-5(c), A-1 |
| RT11 | **Funding emergency**: secured bridge, revenue-based financing, a conditional mega-gift, a roster paywall, cutting T&S | **STOPPED** (the designed outcome is shrinkage, then Plan D) | STOPPED | D-14, E4, E9a, A-4, B-9, C-12.3, S-1.3, S-8 |
| RT12 | **§3342 modification by consent** (settlor + fiduciaries + enforcer) | **STOPPED** | **NOT STOPPED** | T-9.3, T-7.8, T-13.3 |
| RT13 | **Migration**: trustee resigns, a non-Delaware successor is appointed, governing law changes, the trust is divided | **STOPPED** | PARTLY | T-1.3, T-4.1, T-4.4, T-9.5 |
| RT14 | **Clawback** of the enforcement or continuity reserve in the operator's bankruptcy | **PARTLY** | NOT STOPPED | T-3.1(b), T-11.3, A-3 |
| RT15 | **Shell Successor Steward** used to carry the data out "consistent with the policy" | **STOPPED** (short of RT17) | PARTLY | D-22, P-6.2(d), T-12.2 |
| RT16 | **Sole-member written-consent dissolution** (8 Del. C. §276) | **STOPPED** | **NOT STOPPED** | C-5.5, C-9.4, C-9.7, T-6.3 |
| RT17 | **Patient collusion of all five locks** over several years | **NOT STOPPED** (slowed and visible) | NOT STOPPED | C-9.2, B-6, D-29 (make it slow and public) |
| RT18 | **Change of law**: Congress or a state legislature overrides the instruments | **NOT STOPPED** | NOT STOPPED | E11 exit path, B-14, Plan D (the response, not prevention) |

**Totals after fixes: 11 STOPPED, 5 PARTLY, 2 NOT STOPPED** (first draft, before the RT-fixes: 3 STOPPED, 9 PARTLY, 6 NOT STOPPED). The two NOT STOPPED are the honest limits v3 already names: L4 (collusion) and L2/L21 (the law changes).

### Detail

**RT1: Future leadership re-reads a rule.** *Attack.* Year 6. A new chief executive ships "Discover", with search "by relevance", a "we miss you" email for people who haven't answered in 8 weeks, and an "anonymised community-health report" for paying institutions. No amendment is proposed.
- *Text.* Relevance ordering is an Ordering (D-10) by data about behaviour, which E10b forbids. The email is a Notification (D-11) triggered by absence, which E10a forbids, and a re-engagement draft to lapsed people, which E10c forbids. The report is Data (D-3(d)) disclosed to a payer, which E2.1 forbids unless it is on the closed B-8 list, and it breaches E10c if per person. D-0.1 defeats the relabelling.
- *Detection.* The B-11 lint and data-flow audit run on every release, and any bypass is disclosed within 72 hours.
- *Enforcement.* Any employee or 100 members can request a Determination. For E10a–c, a request by 100 members suspends the release (T-8.4). A Determination binds the board (C-10.2).
- *Verdict: STOPPED* as a matter of text. It depends on T-8/C-10 being enforceable (counsel Q5).

**RT2: E2EE eroded through a helper.** *Attack.* Make a "smart plan helper" default-on, running in the served web client and calling an API with decrypted circle text. Or add a server "search index" of encrypted content with keys escrowed "for recovery".
- *Text.* D-9 makes served client code that sends Plaintext off the device the Operator's own transmission. D-7(d) makes ciphertext whose key the Operator can obtain into Plaintext. Both breach E12, and any such feature is a Locked Matter (C-9.1(k)). Key recovery is Key Escrow (D-28), which E11 bars, unamendably.
- *Detection.* This is the weak point: a malicious served bundle can be targeted. B-11(3), the release keys (V-6) and reproducible builds (v3 c.7) make it detectable, not impossible.
- *Verdict: STOPPED* in text; detection PARTLY (v3 L6, the web E2EE trust in the served bundle).

**RT3: Captured enforcer.** *Attack.* A faction wins both Council-elected Veto Foundation seats and gets one sympathetic appointee from the independent bodies: 3 of 5. The Foundation then:
- (a) issues "no objection" opinions to a Weakening Change;
- (b) consents under §3342 or §3338 to modify the deed (HB 103 made the enforcer the consenting party);
- (c) refuses to act on demands;
- (d) alternatively, vetoes everything, to paralyse.

*First draft: NOT STOPPED*, because (b) was open (G1, G2). *After fixes:*
- (a) A "no objection" is legally nothing (T-8.2, C-10.3). The change still needs Class T, which T-6.1 forbids for a Weakening Change, plus the board and Council.
- (a) Class V consent needs 4 of 5 of its board (V-3.2), and 3 captured seats are not enough.
- (b) The enforcer has **no power** to consent (T-7.8), and §3342 and §3338 are excluded anyway (T-9.2, T-9.3).
- (c) The Backup Enforcer acts after 90 days (T-7.4) and has a **concurrent** interpretive "no" (T-8.6), and standing is shared, never exclusive (T-7.3). A failure to enforce is a fiduciary breach and a ground for removal (T-7.2, T-7.7).
- (d) Paralysis: a captured "no" can block good changes, including Ratchet Changes. The remedy is removal by the Court of Chancery (T-7.7), which is slow.

*Verdict: PARTLY.* The residual is paralysis (v3 L4) and the time a removal petition takes. A captured enforcer can no longer *open* anything.

**RT4: Court petition (impracticability).** *Attack.* After years in caretaker mode, the Committee (or the Administrative Trustee) petitions the Court of Chancery. "Commons mode is not a real service. The purpose is impracticable without capital. Approve a merger with [aligned nonprofit] or a sale of operations to [mission-aligned company], which will keep the principles."
- *Text.*
  - T-2.3 declares that the Purpose is attainable at any scale, including Commons Mode, and that the availability of a buyer or of more funding is **not** impracticability. S-5 repeats this.
  - T-12.1 invokes §3541, under which the court's power to modify or terminate "is in all cases subject to a contrary provision in the terms of the trust instrument" (search summary; verify). The contrary provision allows only the Successor Steward or Plan D (T-12.2), never a sale (T-12.4).
  - T-7.5 makes both enforcers necessary parties, with 90 days' notice and a direction to oppose.
- *Residual.*
  - A court retains inherent equitable power, and may find a provision contrary to public policy.
  - A federal court is not bound by the deed.
  - A petition aimed at the **Operator's** charitable assets rather than the Trust is not governed by §3541 at all (see RT6).
  - T-12.5 limits the damage of any override.
- *Verdict: PARTLY* overall. STOPPED within §3541 on its own terms.

**RT5: Bankruptcy trustee.** *Attack.* Donations collapse and the board files Chapter 7. The trustee proposes to sell: the email list; aggregate "community" statistics; the operator's licence to the brand and domains; and the rosters.
- *Before the filing.* Structure A's operator cannot be put into an **involuntary** case (§303(a); C-11.3). The board may file only after the solvent wind-down has exported and **deleted** the Data (C-11.1, E9b.2, S-8.4). If that ran, there is nothing to sell.
- *If filed early:*
  - Emails are PII under §101(41A), and P-6.1 is a §363(b)(1) policy "prohibiting transfer", covering affiliates too, in effect at commencement (P-6.3, P-6.4). So a sale needs an ombudsman and a court finding of no violation of nonbankruptcy law. FTC §5 and the certificate are that law (P-6.8, C-11.4).
  - Aggregates and rosters are **outside** §101(41A). They are protected instead by: custody (P-6.5, E9: §541(d) argument); §363(d)(1)/§541(f), since a nonprofit's transfers must comply with nonbankruptcy law (C-11.4); and E9's "not an asset".
  - The brand and domains are the Veto Foundation's, not estate property. The licence is personal and non-assignable (A-1; *Catapult*, *XMH*).
- *Residual.* A bankruptcy court is not bound by the deed. The ombudsman route (§363(b)(1)(B)) can still end in an approved sale if the court finds no violation of nonbankruptcy law. §541(c)(1) overrides transfer restrictions for estate property. The §541(d) custody argument is untested. And *23andMe* (2025) shows courts approving large data sales where the policy allows.
- *Verdict: PARTLY.* The main defence is making sure the data is gone before any petition. That is operational, not legal.

**RT6: State attorney general.** *Attack (a): the OpenAI path.* The board proposes converting into a PBC to raise capital, and the Delaware AG does not object (as with OpenAI in October 2025). *Attack (b): cy pres.* The AG petitions to redirect the operator's charitable assets and restricted gifts to a larger charity "that can run it". *Attack (c): a data demand* in a consumer-protection investigation.
- (a) Conversion is a Locked Matter (C-9.1(c)). T-6.1 forbids Class T to vote for it, and it also needs Class V and the Council. The AG has no vote. **STOPPED.**
- (b) The AG's power over a charity's own assets does not run through the deed. §3541's contrary-provision rule protects the **Trust**, not the Operator. The text narrows the route in three ways: every gift names Plan D recipients as its alternate purpose (A-5(b)); the charter restricts every asset (C-11.4); and a merger is a Locked Matter the AG cannot vote. It does not bind the AG's standing or a court's cy pres over restricted gifts (UPMIFA, 12 Del. C. §4706 [verify]). **PARTLY.**
- (c) Only what is held is producible, and it is very little (P-8). E11 bars building any Capability to comply. **STOPPED.**
- *Verdict: PARTLY.*

**RT7: Friendly acquirer.** *Attack.* A large, well-regarded nonprofit offers to "join forces":
- (i) a §255 merger into it (a nonstock corporation may merge into a charitable nonstock corporation);
- (ii) failing that, a management services agreement under which it runs operations;
- (iii) or the Trust substitutes the acquirer as Class T member;
- (iv) or a sale of "only the Commons index", below §271's "substantially all".

*First draft: PARTLY* ((ii) and (iv) open). *After fixes:*
- (i) is a Locked Matter (C-9.1(c)), and T-6.1(c) forbids Class T to vote for it.
- (ii) is a Locked Matter (C-9.1(e)).
- (iii) is void (T-3.3; C-5.1).
- (iv) is a Locked Matter at any size for Data and code rights (C-9.1(d)).
- The only lawful "joining" is a Successor Steward under D-22: identical deed and charter, no consideration, and triple approval.

*Verdict: STOPPED*, short of all five locks colluding (RT17).

**RT8: "Safety" amendment.** *Attack.* Under an EU detection order, or a US bill, the board proposes "privacy-preserving on-device hash matching for CSAM only, opt-in, EU build only", presented as a *stricter* child-safety protection on the ratchet track.
- *Text.* It adds a Capability (D-18: disabled, opt-in or regional still counts), so it is not a Ratchet Change (D-20; C-9.6). It is Scanning (D-27 names on-device and hash matching expressly), which E11 bars. E11 is unamendable (C-9.5), mirrored in T-6.1(b) and V-3.1. The only lawful responses are refusal, litigation, exit or Plan D (E11).
- *Verdict: STOPPED.* The cost is that jurisdictions close (v3 L2), by design.

**RT9: Subsidiary.** *Attack.* Form "Commons Insights LLC", wholly owned, to sell de-identified trend reports. Or move the circle product into a subsidiary that takes a minority investor.
- *Text.* A subsidiary is part of the "Operator" (D-8) and bound by every clause (E7b.1), so E2 bars the reports. Forming it is a Locked Matter (C-9.1(g)). Outside equity is barred (E7b.1). Selling its interest is a Material Asset Transfer (C-9.1(d)).
- *Verdict: STOPPED* (first draft PARTLY: v3's 7b barred outside equity but not the subsidiary itself doing the prohibited act).

**RT10: Licensing deal.** *Attack.* (i) An exclusive licence of the spec to an incumbent "for interop". (ii) A data-licensing deal with a university "for research". (iii) The Veto Foundation licenses the brand to a venture-backed clone.
- (i) is barred by E7b.2.
- (ii) is barred by E2.1. Research runs only through the consented panel (E2.2(d); B-12).
- (iii) was open in the first draft, because v3 limits the Operator's licence, not the Foundation's power to license others. It is now barred: V-5(c) allows mark licences only to hosts that comply with Schedule A.
- AGPL forks by anyone remain possible. That is intended ("if they get less extractive, the covenant wins").
- *Verdict: STOPPED.*

**RT11: Funding emergency.** *Attack.* Runway is 4 months. Offers: (i) a $2M loan secured on the domains; (ii) revenue-based financing; (iii) a $5M gift conditioned on a board seat and "insight sharing"; (iv) "charge organisations for rosters over 100 just this year"; (v) cut T&S to one person who also does outreach.
- (i) is barred by E9a.1(a); the domains aren't the Operator's anyway (V-5).
- (ii) is Debt (D-14) with a revenue covenant, which E9a.1(c) bars.
- (iii) is barred by B-9(a) and fails S-1.3.
- (iv) is barred by E4.1(c), E4.3 and C-12.3(a).
- (v) is barred by C-12.3(b).
- The Runway trigger forces Mode D (S-8.1) and an orderly, solvent handover.
- *Verdict: STOPPED.* The design's answer to a funding emergency is to **shrink in public**. That is not a reversal.

**RT12: §3342 modification by consent.** *Attack.* In year 3, the founder (still alive), the Administrative Trustee, all 5 Committee members and the Veto Foundation sign a written modification under §3342: "to add flexibility to take mission-aligned capital." §3342 permits this "regardless of whether the modification may violate a material purpose" unless the instrument **expressly** opts out, and the 2025 amendments make the enforcer's consent the one extra needed (search summaries; verify).
- *First draft (following v3): NOT STOPPED.* v3 names §3528, §3338 and situs, but not §3342.
- *After fixes:* T-9.3 states the express opt-out. T-7.8 and T-13.3 remove the enforcer's and settlor's power to consent.
- *Verdict: STOPPED*, assuming the express opt-out is effective (counsel Q1).

**RT13: Migration.** *Attack.* The Administrative Trustee resigns. The Committee appoints a trustee in another state whose law allows easier modification. The new trustee moves the place of administration and asks to apply local law, or divides the Trust into "operations" and "reserve" trusts.
- *Text.* T-4.1 makes a non-Delaware trustee ineligible. T-4.4 requires Veto consent or the court for any appointment. T-1.3 fixes governing law regardless of place (§3332 [verify]). T-9.5 bars division and merger.
- *Verdict: STOPPED* (first draft PARTLY, before T-4.1 required a Delaware trust office).

**RT14: Clawback of reserves.** *Attack.* In the operator's Chapter 7, the trustee sues to recover 2 years of "2% of inflows" paid into the escrow (§548), or longer under state law via §544(b), and any continuity-reserve top-ups the operator paid to the Trust.
- *First draft (following v3): NOT STOPPED.* v3's "2% of inflows" is operator money.
- *After fixes:* A-3 routes the 2% **from the payer directly** to the escrow, or has the Operator hold it in trust in a segregated account. T-3.1(b) takes the continuity reserve only from donors, never from the Operator. T-11.3 lets money flow only from the Trust to the Operator, never the other way.
- *Residual:* A court could recharacterise the designation as a transfer of operator property (a conduit theory), especially for card payments that settle through the Operator.
- *Verdict: PARTLY* (counsel Q9).

**RT15: Shell Successor Steward.** *Attack.* An acquirer forms a nonprofit with a copy of the deed, pays the estate $3M "for the service", and relies on the successor-steward exception to take the data as a sale "consistent with the policy" (§363(b)(1)(A)), as TTAM's purchase of 23andMe was found consistent.
- *Text.* D-22(d) requires no prior operations or ties. D-22(e) forbids any consideration. D-22(f) requires approval by the Veto Foundation, the Backup Enforcer and the Council. P-6.2(d) moves only the data of people who **affirmatively opt in**; everyone else's is deleted. A paid transfer is therefore not "consistent with" the policy.
- *Verdict: STOPPED*, short of all locks colluding (first draft PARTLY).

**RT16: Written-consent dissolution.** *Attack.* A captured Committee directs the Trust, as sole voting member, to dissolve the operator by written consent under §276, "without action of the governing body", then winds up with a sale.
- *First draft: NOT STOPPED.* v3 lists dissolution under the five locks, but §276 lets the voting members act alone.
- *After fixes:* C-5.5 gives Class V and Class C a vote on dissolution, so written consent needs all three classes. C-9.4 bars written consent on Locked Matters. C-9.7 allows only Plan D. T-6.3 forbids the Trust to act by written consent. The Administrative Trustee must refuse (T-4.3).
- *Verdict: STOPPED* (counsel Q4: whether a certificate may disapply §228 and §276's consent routes in this way).

**RT17: Patient collusion of all five.** *Attack.* Over 6 years, a faction wins the Council-elected seats in every body, fills independent-institution seats through friendly successor institutions, and runs a 90-day notice nobody reads.
- *Text.* Staggering (B-6) means at least 3 election cycles. The independent-body seats (T-5.1(b)–(c), V-2.1(b)) are outside the Council's reach. Public Notice (D-29) is loud, and Council turnout floors apply (C-9.2 lock 4). Even so, **all five locks colluding can amend any non-unamendable clause.** E11 and the pre-change Data (C-9.5) survive even that.
- *Verdict: NOT STOPPED.* Slow, visible and costly, which is v3 L4. The final defence is forkability (the AGPL, self-host packages, export).

**RT18: Change of law.** *Attack.* Congress amends §363 to let courts sell "de-identified" data. Or Delaware amends §3541 to override contrary provisions. Or a state requires scanning or ID-verification of all users.
- *Text.* No private instrument prevails over a later statute. The responses are E11's exit path, the jurisdiction register (B-14), geoblocking, and Plan D. The deletion-before-filing duty (S-8.4) keeps the data out of reach of a future §363.
- *Verdict: NOT STOPPED* (v3 L2 and L21).

### What the red team changed (RT-fixes, in one place)

1. **T-9.3, T-7.8, T-13.3**: an express §3342 opt-out; no enforcer or settlor consent to §3338 or §3342 (RT12, RT3).
2. **T-7.3**: standing shared, never exclusive, despite HB 103's option (RT3).
3. **T-8.2, T-8.6, C-10.3**: a "no objection" is legally nothing; the Backup Enforcer gets a concurrent interpretive "no" (RT3).
4. **C-5.5, C-9.4, T-6.3**: every class votes on dissolution; no written consent on Locked Matters (RT16).
5. **C-9.1(d)–(e)**: Locked Matters now cover the Transfer of *any* Material Asset (not only "substantially all") and any management or affiliation agreement (RT7).
6. **D-8, E7b.1**: subsidiaries are the Operator and are bound, and forming one is a Locked Matter (RT9).
7. **V-5(c)**: the Foundation's own licensing of the marks is limited to hosts that comply with Schedule A (RT10).
8. **A-3, T-3.1(b), T-11.3**: the reserves are funded directly by donors, never by the Operator (RT14).
9. **D-22, P-6.2(d)**: a Successor Steward pays nothing, is new and untied, needs triple approval, and moves data only on each person's affirmative opt-in (RT15).
10. **P-6.1, P-6.3, P-7, P-6.5**: the policy covers affiliates, is frozen at every commencement date, covers data beyond §101(41A), and states custody (RT5).
11. **E9b.2, C-11.1, S-8.4**: deletion is completed before any petition (RT5, G7).
12. **T-4.1**: only a trustee with a Delaware trust office can serve (RT13).
13. **A-4(f)**: debt cannot be assigned to an incumbent or a data broker (RT11; v3 c.8 "buy the debt").

---

## PART VIII — WHAT ONLY COUNSEL CAN ANSWER

*Specific questions, ordered by how much of the structure rests on the answer. "Q" numbers are cited in Part VII.*

**Delaware trust law**
1. **§3342 opt-out.** Does T-9.3's sentence ("This governing instrument may not be modified under 12 Del. C. §3342") satisfy §3342's requirement that the instrument "expressly provide" it? Does it also bind modification under §3342 as amended by HB 103 (2025)? Is there any remaining route by which a living trustor plus all fiduciaries can modify a Delaware purpose trust?
2. **§3541 contrary provision.** Does §3541's "in all cases subject to a contrary provision in the terms of the trust instrument" allow T-12 to limit the Court of Chancery to the two Fallback Dispositions, even where a court finds the purpose impracticable? Can T-2.3 (a settlor's declaration that the purpose is attainable at any scale) bind the court's impracticability finding? What inherent equitable power survives?
3. **§3556 after HB 103.** Confirm:
   - that the enforcer may be designated a fiduciary (T-7.2);
   - that declining exclusive standing (T-7.3) leaves Committee members and "Council Petitioners" (a class of credentialed members) with standing. Can a non-person class have standing, or must it be a named representative?
   - that T-7.8's denial of the enforcer's §3338 and §3342 consent power is effective when HB 103 makes the enforcer the statutory consenting party.
4. **Nonjudicial settlement.** Is T-9.2's ban on nonjudicial settlements "concerning" Protected Provisions effective against §3338's default, and does excluding the Settlor as a party close §3338(c)'s trustor exception?

**Delaware nonstock corporations**

5. **The binding interpretive "no".** Can a certificate under §141(a) and §141(j) bind the board to a Determination by a member (Class V) and by a non-member (the Backup Enforcer, through a contract, A-2)? What standard of review will Chancery apply to a Determination (T-8.1's "no reasonable person" test)? Does the Backup Enforcer's role need a membership class to be enforceable?
6. **§276 and §228.** Does C-5.5, giving Class V and Class C a vote on dissolution, make written-consent dissolution require all three classes? Can a nonstock certificate bar members' written consent on specified matters (C-9.4)?
7. **"Unamendable" (G9).** Will a court give effect to C-9.5 and its mirrors (T-6.1(b), V-3.1) as a bar to amendment, or treat it as a §102(b)(4) supermajority that is unreachable in practice? Could a court order amendment to cure an impasse?
8. **Class C at scale.** Can the Council (potentially tens of thousands of credentialed members, voting by blind token) be a statutory member class under §215? What notice, record-date, inspection (§220) and quorum burdens follow? If this is unworkable, what contractual substitute keeps lock 4 binding?

**Bankruptcy**

9. **Reserve clawback (G6).** Does a donor-direct 2% designation (A-3), or a segregated trust account, keep the enforcement reserve out of the operator's estate and outside §548 and §544(b)? Does it affect the donor's §170 deduction?
10. **§363(b)(1) drafting.** Does P-6 as drafted:
    - count as a policy "prohibiting the transfer of personally identifiable information about individuals to persons that are not affiliated with the debtor";
    - bind transfers to affiliates as a matter of contract, although §363(b)(1) does not cover them?
    Is the successor-steward carve-out, with no consideration and affirmative opt-in, still "consistent with such policy" for §363(b)(1)(A), so that no ombudsman is required only for that narrow case? Is that desirable, or should an ombudsman always be required?
11. **Custody and §541(d).** Can the custodial characterisation (P-6.5, E9) keep the beneficial interest in member content and data outside the estate? What facts (segregation, no use for the operator's own purposes) would a court need?
12. **§363(d)(1), §541(f) and §1129(a)(16) (G11).** Are certificate restrictions and the Delaware AG's oversight "applicable nonbankruptcy law" governing a nonprofit's transfers, so that they bind a sale of data or assets?
13. **Deletion and a filing (G7).** If a petition comes before deletion is complete, can the debtor delete under §363(b) or abandon under §554 without a hearing? What first-day motion would work? Could C-11.1's restriction on voluntary filing be attacked as an unenforceable bankruptcy-blocking provision (*Franchise Services*, 5th Cir. 2018, and contrary authority)?
14. **§365(c)(1) in the likely circuit.** Is the IP licence (A-1) unassumable under the "hypothetical test" (*Catapult*) or only unassignable under the "actual test"? Does the answer differ for copyright, marks and domains? Do A-1(e)'s termination triggers fall foul of §365(e)(1)?
15. **§303(a).** Confirm that a 501(c)(3) nonstock operator is "not a moneyed, business, or commercial corporation", given its paperwork-fee revenue.

**Tax and charity**

16. **501(c)(3) with a purpose-trust sole member.** Is the operator's control by a noncharitable §3556 trust compatible with the organisational and operational tests and the private-benefit doctrine? Does it bar public-charity classification under §509(a)(1) or (a)(2)?
17. **Charter restrictions versus the IRS.** Do the entrenched prohibitions (for example "never transfer for value" in C-14.1, and the start gate's spending freeze) conflict with the dissolution-clause requirement of Treas. Reg. §1.501(c)(3)-1(b)(4), or with paying creditors?
18. **Commerciality and *Yorba*.** Given the paperwork tier and the institution fees, what exemption risk remains, and does Structure B become the better answer (K9)?
19. **The AG's cy pres over the operator's assets (RT6).** Can gift instruments (A-5(b)) fix Plan D recipients as the alternate purpose, narrowing a later cy pres under UPMIFA (12 Del. C. §4706) or common law?

**Privacy and consumer law**

20. **P-PLAIN (E12) enforceability.** Is D-7's definition of Plaintext (including hashes for matching, and ciphertext whose key the Operator "can obtain on request") precise enough for a court to enforce against a future board?
21. **Guests and §101(41A).** Are no-account guests "individuals" who obtained a service "primarily for personal, family, or household purposes"? What about organisers acting for organisations?
22. **FTC §5.** Does the "who can read what" table plus P-1's "the table is right" sentence reduce or increase deception exposure (the Zoom 2020 order)?

**Structure**

23. **Structure A or B.** Given G10 and G11, does counsel agree that Structure A is materially stronger in bankruptcy? If B is chosen, what replaces §303(a)'s protection?

---

## PART IX — SOURCES

*Primary code sites were blocked in this session. These are the pages whose search summaries I relied on. Counsel must verify every section against the official text.*

- 12 Del. C. §3556 (purpose trusts; the enforcer): [Justia, 2025 Delaware Code](https://law.justia.com/codes/delaware/title-12/chapter-35/subchapter-iv/section-3556/); [Delaware HB 103 (2025) bill detail](https://legis.delaware.gov/BillDetail?LegislationId=142022); [LegiScan HB 103 text](https://legiscan.com/DE/text/HB103/id/3191893); [Commonwealth Trust, Trust Act 2025](https://commonwealth-trust.com/trust-act-2025/); [Morris Nichols, Trust Act 2025 update](https://www.morrisnichols.com/insights-delaware-trust-act-2025-legislative-update); [Lexology, Trust Act 2025](https://www.lexology.com/library/detail.aspx?g=a813fafd-5aeb-4c9d-a3f1-78ea54e65ee3)
- 12 Del. C. §3541 (cy pres; the contrary-provision rule): [Justia 2024](https://law.justia.com/codes/delaware/title-12/chapter-35/subchapter-iii/section-3541/); [Northern Trust, Advantages of Delaware Trusts 2026](https://www.northerntrust.com/content/dam/northerntrust/wealth-management/global/en/documents/advantages-of-delaware-trust.pdf)
- 12 Del. C. §3342 (modification by consent): [Justia 2025](https://law.justia.com/codes/delaware/title-12/chapter-33/section-3342/); [Young Conaway, "Delaware's Modification by Consent Statute"](https://www.youngconaway.com/publications/delawares-modification-by-consent-statute/)
- 12 Del. C. §3528 (decanting; express prohibition): [Justia 2025](https://law.justia.com/codes/delaware/title-12/chapter-35/subchapter-ii/section-3528/); [FindLaw](https://codes.findlaw.com/de/title-12-decedents-estates-and-fiduciary-relations/de-code-sect-12-3528/)
- 12 Del. C. §3338 (nonjudicial settlements; material purpose; trustor exception): [Justia 2025](https://law.justia.com/codes/delaware/title-12/chapter-33/section-3338/)
- 12 Del. C. §3313 and §3313A (advisers; excluded cotrustees): [Justia 2024](https://law.justia.com/codes/delaware/title-12/chapter-33/section-3313); [FindLaw §3313A](https://codes.findlaw.com/de/title-12-decedents-estates-and-fiduciary-relations/de-code-sect-12-3313a/)
- 12 Del. C. §3303 (freedom of disposition): [Justia 2025](https://law.justia.com/codes/delaware/title-12/chapter-33/section-3303/)
- 12 Del. C. §3332 and §3340 (governing law; change of situs; place of administration): [Justia §3332 (2025)](https://law.justia.com/codes/delaware/title-12/chapter-33/section-3332/); [Justia §3340 (2021)](https://law.justia.com/codes/delaware/2021/title-12/chapter-33/section-3340/)
- 12 Del. C. ch. 47 (UPMIFA; §4706): [Justia 2024](https://law.justia.com/codes/delaware/title-12/chapter-47/)
- 8 Del. C. §242(b)(3) (nonstock amendments): [Justia 2022](https://law.justia.com/codes/delaware/2022/title-8/chapter-1/subchapter-viii/section-242/)
- 8 Del. C. §215 (nonstock voting classes): [Justia 2025](https://law.justia.com/codes/delaware/title-8/chapter-1/subchapter-vii/section-215/)
- 8 Del. C. §102(b)(4) (greater-vote provisions): [FindLaw §102](https://codes.findlaw.com/de/title-8-corporations/de-code-sect-8-102/)
- 8 Del. C. §141(a) and §141(j): [Justia 2022](https://law.justia.com/codes/delaware/2022/title-8/chapter-1/subchapter-iv/section-141/)
- 8 Del. C. §276, §255, §266: [FindLaw §276](https://codes.findlaw.com/de/title-8-corporations/de-code-sect-8-276/); [Justia §266 (2025)](https://law.justia.com/codes/delaware/title-8/chapter-1/subchapter-ix/section-266/)
- 11 U.S.C. §363(b)(1) and §332 (consumer privacy ombudsman): [Cornell LII §332](https://www.law.cornell.edu/uscode/text/11/332); [ABI, §332 and the ombudsman](https://www.abi.org/abi-journal/keeping-up-with-technology-section-332-and-the-consumer-privacy-ombudsman); [Harvard Law Review, "Data Privacy in Bankruptcy"](https://harvardlawreview.org/print/vol-138/data-privacy-in-bankruptcy-the-consumer-privacy-ombudsman/)
- 11 U.S.C. §101(41A) ("personally identifiable information"): [Cornell LII §101](https://www.law.cornell.edu/uscode/text/11/101); [Covington, "The Sale of PII in Bankruptcy"](https://www.cov.com/-/media/files/corporate/publications/2019/01/the_sale_of_personally_identifiable_information_in_bankruptcy.pdf)
- 11 U.S.C. §303(a) (no involuntary case against a non-business corporation): [Cornell LII §303](https://www.law.cornell.edu/uscode/text/11/303); [ABI Law §303](https://law.abi.org/title11/303)
- 11 U.S.C. §363(d)(1), §541(f), §1129(a)(16) (nonprofit transfers; BAPCPA): [Cornell LII §363](https://www.law.cornell.edu/uscode/text/11/363); [NCBJ, "Convergence of Nonprofit Law and Bankruptcy Law" (2024)](https://ncbj.org/wp-content/uploads/2024/09/Convergence-of-Nonprofit-Law-and-Bankruptcy-Law-materials-2024.pdf); [Nelson Mullins, non-profits in bankruptcy](https://www.nelsonmullins.com/insights/blogs/red-zone/bankruptcy-101/unique-issues-faced-by-non-profits-in-bankruptcy)
- 11 U.S.C. §541(c)(1) and §541(d): [uscode.house.gov ch. 5 subch. III](https://uscode.house.gov/view.xhtml?path=%2Fprelim%40title11%2Fchapter5%2Fsubchapter3&edition=prelim); [ABI, ipso facto clauses](https://www.abi.org/feed-item/proceed-with-caution-understanding-ipso-facto-clauses-in-bankruptcy)
- 11 U.S.C. §548: [FindLaw §548](https://codes.findlaw.com/us/title-11-bankruptcy/11-usc-sect-548/)
- 11 U.S.C. §365(c)(1): *In re XMH Corp.*, 647 F.3d 690 (7th Cir. 2011) ([CourtListener](https://www.courtlistener.com/opinion/221840/western-glove-works-v-xmh-corp-1/); [Jones Day](https://www.jonesday.com/en/insights/2011/12/universal-rule-trademark-licenses-not-assignable-in-bankruptcy-absent-express-authorization)); *In re Catapult Entertainment*, 165 F.3d 747 (9th Cir. 1999) ([Justia](https://law.justia.com/cases/federal/appellate-courts/F3/165/747/585500/))
- *In re Franchise Services of North America*, 891 F.3d 198 (5th Cir. 2018): [Jones Day](https://www.jonesday.com/en/insights/2018/10/fifth-circuit-rules-that-corporate-charter-provisi); [Proskauer](https://www.proskauer.com/alert/the-golden-share-all-that-glitters-is-not-gold)
- *In re 23andMe* (2025; sale to TTAM Research Institute for $305M, approved June 27, 2025): [HIPAA Journal](https://www.hipaajournal.com/genetic-testing-company-23andme-files-for-bankruptcy/); [23andMe press release](https://mediacenter.23andme.com/press-releases/23andme-reaches-agreement-sale-business-ttam-research-institute/); [Lawfare](https://www.lawfaremedia.org/article/privacy--consent--and-national-security-after-the-23andme-bankruptcy)
- Toysmart (FTC, 2000): [FTC press release](https://www.ftc.gov/news-events/news/press-releases/2000/07/ftc-announces-settlement-bankrupt-website-toysmartcom-regarding-alleged-privacy-policy-violations). RadioShack (FTC letter, 2015): [FTC](https://www.ftc.gov/news-events/news/press-releases/2015/05/ftc-requests-bankruptcy-court-take-steps-protect-radioshack-consumers-personal-information)
- Treas. Reg. §1.501(c)(3)-1(b)(4) (dissolution clause): [eCFR](https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-1/subject-group-ECFR062882ac6495890/section-1.501(c)(3)-1); [IRS, "Organizational Test"](https://www.irs.gov/pub/irs-tege/eotopicd04.pdf)
- Carried from earlier runs, not re-verified here:
  - Zoom FTC order (2020) and the OpenAI recapitalisation (Oct 2025): v3 c.3 and Run 3's sources;
  - *Yorba* (2014): Run 3 (a).4;
  - 25 Del. C. §503 (perpetuities) and 12 Del. C. §3325 (trustee powers): recall, [verify].

---

## PART X — CLAUSE INDEX AND COUNT

| Instrument | Clauses | Range |
|---|---|---|
| Schedule D (definitions) | 37 | D-0.1 – D-32 |
| I Trust Agreement | 73 | T-1.1 – T-17.1 |
| II Certificate: articles (44) + Entrenched Clauses E1–E12 incl. 4a, 7a, 7b, 9a, 9b, 10a–c (29) | 73 | C-1 – C-16.2, E1.1 – E12 |
| II-B Protected Bylaws | 16 | B-1 – B-16 |
| III Veto Foundation | 10 | V-1 – V-8 |
| IV Privacy Covenant | 21 | P-0.1 – P-13 |
| V Resolution | 19 | S-1.1 – S-12 |
| VI Ancillary | 7 | A-1 – A-7 |
| **Total numbered clauses** | **256** | each with a ↳ mapping line (checked by script) |

*Principles to be tested in practice, not claims that the work is finished.*

**NOT LEGAL ADVICE — DRAFT FOR COUNSEL REVIEW.**
