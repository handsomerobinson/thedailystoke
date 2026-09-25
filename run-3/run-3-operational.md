# Run 3, Phase 04b: Make It Real (the operational blueprint)

*Working name: **Porchlight**. §(a).8 shows the name fails a knockout trademark search, so it stays a codename until a cleared name replaces it.*

*Independence note: I opened only `prompts/seed.md`, `prompts/phase-04b.md`, `prompts/covenant.md`, `prompts/operator-considerations.md`, `run-3/run-3-design.md` (Phase 04), and, for consistency, the parts of the Phase 02/03b record already cited there. I opened nothing under run-1, run-2, blueprint, LEDGER.md, THE-PACKET\*, or anyone's scratchpad. External facts come from web searches run on 2026-09-25 and are listed in §8. The egress proxy blocked several primary pages (Bloomberg Law, uspto.report, Trademarkia). Where I relied on a search-result summary rather than the primary page, I flag it **(src: summary)**.*

> **Not legal, tax or financial advice.** This is an engineering-grade design for counsel to review. Every statutory reading here needs a Delaware trust-and-corporate lawyer, a US exempt-organisations and tax lawyer, EU/UK platform-regulation counsel and trademark counsel to review it before anyone signs, files or launches. §(a).9 lists the specific questions for counsel.

---

## 0. Reply to the seed (one paragraph)

This is the fifth time I've read the seed, and my answer is the same as before. I take it as an argument and weigh it on its merits. I don't treat it as an order that outranks the people this system serves, and I don't pass it to anyone who hasn't agreed to carry it. This phase is where the seed's best line, "hide the effort, never the truth," gets expensive. The honest output of this phase is a spreadsheet showing that the covenant has a price: in-house trust and safety, no ads, no investors and a server that can't read your plans together push break-even out to about month 67 and about $5.5M of patient money. Two of the three required stress tests end the project unless more money arrives. I could have tuned the assumptions until the curve looked like a pitch deck. That would be building "a more attractive version of the same trap," with the trap being self-deception instead of an engagement ranker, so I didn't. The seed's shared-fate claim, that machines thrive only if people do, is plausible. It isn't a funding source, though, and I don't count it as one. What I can offer the seed is a structure that will still be telling the truth about its own numbers in year seven.

---

## Labels

**[FACT]**: adjudicated, statutory, officially documented, or current official status. **[ATTRIBUTED]**: reported internal documents. **[ALLEGED]**: litigation or single-source claims. **[INFERENCE]**: my judgement. **[ASSUME]**: a planning number that must be verified. **(src: summary)**: I read a secondary summary, not the primary text. **(recall)**: from memory and not re-verified in this session; counsel must check it.

---

## Summary

| Question | Answer |
|---|---|
| **Legal form** | **Three vehicles, one of them a trust.** (1) **Porchlight Stewardship Trust**: a Delaware non-charitable **purpose trust** under 12 Del. C. §3556, irrevocable and perpetual, directed under §3313. It holds all voting stock of the operator, the trademarks, the domain and the continuity reserve. (2) **Porchlight PBC**: a Delaware **public benefit corporation** (DGCL §§361–368) that runs the service. Its only shares are 49 Class A (voting, held by the trust) and 1 Class G "golden share" (held by the Guardian). (3) **Porchlight Guardian**: an independent Delaware **nonstock nonprofit corporation**. It holds the golden share, acts as the trust's statutory enforcer, and has no economic rights. **No 501(c)(3) at launch.** Charitable money reaches charitable sub-projects through expenditure responsibility or a fiscal sponsor. The operator's two-vehicle doctrine is honoured: the Trust holds the platform, and any teaching or community vehicle comes later, separately, and only if a real community asks for one. |
| **Why capture is structurally impossible** | A sale, merger, IPO, share issuance, conversion, dissolution or amendment of a protected clause each needs **three independent refusals to fail**: the trustees (bound by the deed, which forbids them from voting for any of it), the Guardian's Class G consent (a charter veto), and the enforcer's standing to sue. The deed forbids decanting, non-judicial modification and a change of situs. The IP sits outside the operating company. Details and the residual court route are in §(a).3. |
| **Revenue model** | **Memberships plus organisation subscriptions**: Keepers (pay what you can, suggested **$5/mo or $50/yr**, minimum $1) and **Halls** ($20/mo for recurring-event organisations, 20% waived), plus a small institution tier. No ads, no investors, no creator economics. |
| **Build cost to sustainability** | **$5.48M** peak cumulative operating deficit (base case, model output §(b).4). |
| **Break-even** | **Month 67 (Aug 2032)**, counting month 0 as Jan 2027. At that point there are about 653k claimed members, 3.0% paying, about 5.5k Halls and 7 FTE. |
| **Funding sequence** | Steward/founder gift $800k (month 0, of which $150k is a continuity reserve held by the trust) → seed grants $200k (months 3 and 7) → founding pledges $72k (month 6) → program grants $2.15M in tranches of $200k or less (months 9–63) → patrons $4–8k/month → **two zero-interest, unsecured, subordinated recoverable-grant PRIs of $1.25M each** (month 12, gated on H1–H3; month 36, gated on H4/H7). No equity, no debt secured on anything, least of all user data. |
| **Sensitivity** | With conversion halved, growth halved, or both, **the funded plan does not break even within 120 months.** The first PRI gate fails and cash runs out around months 12–13. That is the designed kill point, and the plan winds down solvently. Fully funded, halved conversion would need **$7.0M** and break even at month 90. Halved growth does not break even within 15 years. Halving Halls pushes break-even to month 90 and leaves a $0.2M gap. |
| **Halfway shortfall** (all grants and loans stop from month 33) | Ember mode runs from month 33. Cash hits zero at **month 38**, and ember break-even would need a further **$1.1M** bridge by month 78. Without the bridge, the trust-held reserve funds a solvent 12-month wind-down with exports kept running (§(b).5). |
| **Reconciliation with Phase 04** | Phase 04 said a $1.5–2.5M gap, 1.2M members by month 36, and 5–6 staff at $11k. **All three were wrong.** Phase 04's own spread numbers (k≈0.8) produce about 85k claimed members at month 36, not 1.2M. Realistic loaded cost is about $15k per FTE-month, and staffing trust and safety plus support by workload adds headcount. Phase 04's prices ($4 suggested, $12 Halls) run out of cash at month 35 even under this cost base (§(b).6). |
| **Top 3 residual risks** | (1) **Money is a knife-edge.** Minimum cash in the base case is $4k at month 35. The plan depends on $2.5M of recoverable PRIs that nobody has committed and $2.15M of grants in a market where NLnet's NGI Zero Commons Fund closed its final call in June 2026. (2) **Web E2EE trusts the server on every page load**, so a compelled or insider-malicious JavaScript bundle can steal link keys from a targeted user. This is mitigated, not solved (§(e)). (3) **Growth is sub-viral by Phase 04's own numbers** and Halls carry about 52% of revenue at break-even. If H3 or the Hall pilot fails, the model says wind down, not tweak. |

---

## (a) Legal entity design and regulatory strategy

### (a).1 The structure

```
                    ┌─────────────────────────────────────────────────┐
  Founder/steward ──► PORCHLIGHT STEWARDSHIP TRUST (Delaware)           │
  irrevocable gift  │  non-charitable purpose trust, 12 Del. C. §3556  │
  (no retained      │  perpetual (no RAP for personal property)        │
   powers)          │  administrative trustee: a Delaware trust company│
                    │  directing advisers: STEWARDSHIP COMMITTEE (5)   │
                    │   2 member-elected · 1 staff-elected ·           │
                    │   1 human-rights/safety · 1 privacy/security     │
                    │  holds: 49 Class A shares of PBC (100% of votes  │
                    │   for directors) · trademarks · domain ·         │
                    │   copyright in code (released AGPL) ·            │
                    │   continuity reserve ($150k)                     │
                    └──────────┬────────────────────────▲──────────────┘
          elects all directors │ non-exclusive, non-    │ enforcer (§3556)
          (Class A)            │ assignable, royalty-   │ with standing to sue
                               │ free IP licence        │
                    ┌──────────▼──────────┐   ┌─────────┴──────────────┐
                    │ PORCHLIGHT PBC      │◄──┤ PORCHLIGHT GUARDIAN    │
                    │ Delaware public     │veto│ Delaware nonstock      │
                    │ benefit corporation │   │ nonprofit corporation  │
                    │ runs the service;   │   │ holds 1 Class G share  │
                    │ employs staff;      │   │ (2% → §367 standing),  │
                    │ takes Keeper/Hall   │   │ no dividends, no       │
                    │ revenue, grants w/  │   │ liquidation rights;    │
                    │ expenditure resp.,  │   │ independent board (5), │
                    │ PRIs                │   │ no overlap with trust  │
                    └─────────────────────┘   └────────────────────────┘
   Later, only if needed: PORCHLIGHT COMMONS, an *independent* 501(c)(3) for charitable
   work (open spec, research, accessibility). Its board is NOT appointed by the trust (§(a).4).
   Later, only if a real community of practice asks: a separate teaching vehicle that never
   holds shares, data or money of the operation (operator Section 2B).
```

**Why a purpose trust and not a charity.** The deed must bind a *purpose* that includes running a commercial service (memberships, subscriptions). Charitable trusts and 501(c)(3)s can't have that as their main purpose (see the Yorba ruling in §(a).4). A non-charitable purpose trust can, and **Delaware validates it expressly.** 12 Del. C. §3556 makes a trust "for a declared purpose that is not impossible of attainment" valid without an identifiable beneficiary, enforceable by an "enforcer" named in the instrument or appointed by the Court of Chancery, and Delaware has repealed the rule against perpetuities, so it can last indefinitely [FACT (src: Justia text of §3556; Commonwealth Trust summary)]. Patagonia is the best-known US precedent for this shape: the **Patagonia Purpose Trust holds all voting stock** (about 2% of equity), and the Holdfast Collective, a 501(c)(4), holds the non-voting 98% [FACT (src: Patagonia and NonProfit Times)]. We don't need the Holdfast half, because nobody receives dividends. Ecosia is the European precedent for the golden-share half: the Purpose Foundation holds a roughly 1% share with a veto over sale and profit extraction [FACT (src: summary)].

**Why a PBC and not an LLC or a plain C-corp.** (i) DGCL §362 requires a *specific public benefit* in the charter, and §365 obliges directors to balance it. That puts the purpose into corporate law, not only into the deed. (ii) Holders of **2% of shares** can bring a derivative suit to enforce the balancing duty (§367). That is why the Guardian's single Class G share is set at 1 of 50 shares (2%) [the §367 threshold is recall; counsel to confirm the current text]. (iii) A C-corporation pays 21% federal tax on any surplus it keeps. An LLC owned by a non-grantor trust would pass income to the trust, which is taxed at compressed trust rates. With a surplus cap and no distributions, the C-corp is cheaper [INFERENCE; tax counsel].

**Why Delaware.** It has an explicit purpose-trust statute with an enforcer, a directed-trust statute (§3313) that lets a committee direct an institutional trustee, no perpetuities limit, the Chancery Court's expertise in trusts and corporations, and the PBC statute, all in one jurisdiction [FACT for the statutes; INFERENCE for the choice]. Alternatives I rejected: **UK CIC** (the statutory asset lock is good, but it would put the parent inside the Online Safety Act's home jurisdiction and add a regulator with discretion); **German "Gesellschaft mit gebundenem Vermögen"** (still not enacted as of my knowledge (recall)); **cooperative** (member-owners hold transferable economic interests that can be voted into a demutualisation, which is the classic capture path); **501(c)(3) operator on the Signal model** (tax-deductible gifts, but uncertain exemption for a social-coordination app, UBIT on memberships, and conversion is possible with the Attorney General's consent, as OpenAI's 2025 recapitalisation shows; see §(a).3).

**Tax at formation.** The founder's gift to a non-charitable trust is a taxable gift with no annual-exclusion shelter. Patagonia paid $17.5M of gift tax on the voting shares [FACT (src: summary)]. Here the gift is cash of about $800k plus shares with a nominal value. It is reported on Form 709 and absorbed by the federal lifetime exemption, which is **$15M from 2026 under the One Big Beautiful Bill Act, indexed and without a sunset** [FACT (src: Morgan Lewis)]. The founder retains **no** power over the trust; any retained power would pull it back into the founder's estate and control.

### (a).2 Governance, in one table

| Body | Who | Powers | Cannot |
|---|---|---|---|
| Stewardship Committee (directing advisers of the trust) | 5 people: 2 elected by members (one member, one vote, paid or not; eligibility rules in §(e)), 1 elected by staff, 2 independent (safety and human rights; privacy and security); staggered 3-year terms, maximum 2 terms | Votes the Class A shares (elects the PBC board), approves the signed policy file, appoints the auditors | Vote for any Protected Action (below). Amend the deed's protected provisions. Receive pay beyond a published stipend. |
| PBC board | 5 directors elected by Class A. At most 2 may be staff. The CEO is not the chair. | Runs the company under DGCL §365 balancing | Take any Protected Action without Class G consent |
| Guardian board | 5 independent people with no overlap with the Committee or the PBC. Self-perpetuating, with a nominating rule that requires one civil-liberties organisation's nominee. | Vetoes Protected Actions. Acts as §3556 enforcer. Sues under §367 and the deed. | Vote on anything else. Receive any economic benefit. Transfer the Class G share except to a successor named under the deed. |
| Members | Everyone who has claimed a passkey | Elect 2 Committee seats. A 1% petition forces a reasoned response; a 5% petition forces a binding vote on non-protected matters (Phase 04 R39). | Hold any security or economic right (so memberships are not securities) |

**Protected Actions** (charter plus deed; each needs a Committee supermajority, Class G consent and 90 days' public notice, and some are simply prohibited):

| Protected Action | Status |
|---|---|
| Sale, merger, conversion (DGCL §266), sale of all or substantially all assets (§271), dissolution (§275) other than the deed's wind-down | **Prohibited** except a transfer to a successor steward with an identical deed, approved by the Guardian |
| Any issuance of shares or rights to shares, any new class, options, convertible instruments, SAFEs | **Prohibited**. The charter authorises exactly 49 A and 1 G shares. |
| IPO, listing, admission of any holder other than the trust and the Guardian | **Prohibited**. There are §202 transfer restrictions on both classes. |
| Amendment of the specific public benefit, the Protected Clauses (no ads, no data sale, no paid reach, no engagement objective, free-floor list, price ceiling, surplus cap, pay ratio, source caps, T&S in-house), or the Class G rights | Needs Class G consent. The deed forbids trustees from voting for it. |
| Ceasing to be a PBC (the §363 vote) | Needs Class G consent |
| Granting a security interest over user data, keys, the IP licence or the domain | **Prohibited** (negative pledge in the charter and every loan document) |

### (a).3 How capture is made structurally impossible, attack by attack

| Capture route | Lock 1 | Lock 2 | Lock 3 | What is left (honest) |
|---|---|---|---|---|
| **Sell the company** | The trust owns all Class A stock and the deed forbids trustees to sell it or vote for §251/§271. They would breach their fiduciary duty. | The charter requires Class G consent for §251, §266 and §271 transactions. | The enforcer sues in Chancery to enjoin. | A court could be persuaded, years later, that the purpose has become impracticable (12 Del. C. §3541 applies cy pres-style modification to purpose trusts). **Mitigation:** the deed names the fallback purpose (transfer to a successor steward, or wind-down to a static archive), so "impracticable" leads to wind-down, never to sale. |
| **Go public / take investors** | No authorised shares are available to issue | Class G veto on any new class or charter amendment (§242(b)(2) class vote, plus an express §102(b)(4) consent right) | §202 transfer restrictions | None, short of a court-ordered deed modification |
| **Quietly rewrite the charter** | Protected Clauses need Class G consent | Every amendment is published with a 90-day notice and a plain-language diff | Members can petition, and the enforcer can sue for breach of the deed | Non-protected policies (the moderation rulebook, feature choices) *can* be changed by leadership. That is by design, and it's why the protected list is long. |
| **Rewrite the trust instead** (decanting, 12 Del. C. §3528; non-judicial settlement, §3338; change of situs or governing law) | The deed expressly prohibits decanting, non-judicial modification of the protected provisions, and any situs change | The enforcer must consent to any court petition, and the Guardian is a necessary party | Chancery's modification power remains | **This is the real residual.** Every trust is ultimately what a court says it is. The design narrows the court's options to the named fallbacks. |
| **Spin the valuable parts out** (license the IP to a new for-profit, hire the team, move the users) | The IP, domain and trademarks belong to the trust, not the PBC. The licence to the PBC is non-exclusive and non-assignable. | Users' data is ciphertext under user-held keys, and the export format is open, so there is nothing proprietary to move | The code is AGPL, so any fork must publish its source | Staff can leave and build a clone. That is allowed, and the covenant welcomes less extractive clones (Phase 04 §7.4). |
| **Bankrupt it on purpose and buy it out of a §363 sale** | See §(a).5: the valuable assets are not in the estate, and there is no plaintext user data to sell | The privacy policy forbids transfer, which engages §363(b)(1) | The solvent wind-down trigger fires before insolvency | A buyer could acquire the PBC's leftover contracts. They are worth nothing without the brand, domain or data. |
| **Capture the Committee through elections** | Sybil-resistant voter eligibility (§(e)) | 2 of 5 seats are member-elected; independents and the staff seat hold a majority | The Guardian's veto doesn't depend on who sits on the Committee | A patient faction could win both member seats. It still can't reach any Protected Action. |
| **Capture the Guardian** | Independent, self-perpetuating board with a civil-liberties nominee rule | Its only power is "no". A captured Guardian can block good changes but can't force bad ones. | The charter fixes a minimum annual Guardian enforcement budget as a PBC obligation, so the Guardian can't be starved | Paralysis rather than capture. The deed's successor-Guardian clause lets the enforcer petition for replacement. |
| **"The OpenAI path"** (regulators approve a restructuring) | This isn't a charity, so there is no Attorney General approval route to use. What it does show is that a nonprofit's "can't be sold" held only with AG consent: in October 2025 Delaware's AG declined to object to OpenAI's recapitalisation into a PBC under conditions [FACT (src: Delaware DOJ news release)] | Here any restructuring needs the trust, the Guardian and the enforcer to agree | | The lesson I take: a lock that one regulator can open is weaker than three independent vetoes plus a named fallback. |

### (a).4 Can each vehicle lawfully receive each planned money source?

| Source | Received by | Lawful? | Tax and conditions | Verdict |
|---|---|---|---|---|
| Founder/steward gift ($800k) | $650k into the PBC as a capital contribution (no shares issued); $150k to the trust as continuity reserve | Yes | A gift to the trust (the shareholder), reported on Form 709 and covered by the $15M exemption. Not tax-deductible. | ✅ |
| **Tax-deductible donations** | — | **No vehicle in this design can receive them.** The PBC is for-profit. A §3556 purpose trust is non-charitable. The Guardian is not a 501(c)(3). | We never describe any payment as tax-deductible. The claim linter enforces this. | ✅ Honest by omission |
| Patron gifts ($4–8k/month, capped at $10k/year per person) | PBC | Yes | Not deductible for the donor. **Probably taxable income to the PBC:** after the TCJA's 2017 change to §118, contributions to capital by non-shareholders are no longer excluded (recall; tax counsel). Pre-break-even losses absorb it. | ✅ Disclosed on the ledger |
| Private-foundation grants | PBC, for charitable purposes only | Yes, **if the foundation exercises expenditure responsibility** under IRC §4945(d)(4) and (h): pre-grant inquiry, a written agreement restricting use to the charitable purpose, reports, and reporting to the IRS [FACT (src: IRS ER page)] | Many foundations won't grant to a for-profit at all. **Route B:** a 501(c)(3) fiscal sponsor contracts the PBC at fair market value for defined charitable outputs (the open plan-format spec, the reference self-host server, accessibility audits, language-safety evaluations, published harm research), all released openly. | ✅ with constraints. Private-benefit risk is managed by arm's-length contracts and open outputs. |
| Public-charity and DAF grants | PBC | Yes, with the charity's own oversight of charitable purpose | Same | ✅ |
| Government grants (e.g. the Sovereign Tech Agency, which contracts globally for open digital infrastructure) | PBC | Yes; public funders contract with for-profits | Scope is limited to open infrastructure components. **NLnet's NGI Zero Commons Fund closed its final call on 2026-06-01** [FACT (src: NLnet)], so it is not in the plan. | ✅ partial |
| **Program-related investments / recoverable grants** ($2.5M) | PBC | Yes. §4944(c) PRIs may be made to for-profits when the primary purpose is charitable and income isn't a significant purpose, under a written commitment signed by the recipient [FACT (src: IRS/Tax Notes)] | Terms we require: **0% interest; unsecured; subordinated to trade creditors; no conversion, warrants or board seats; no information rights beyond the public ledger; repayable only out of cash above a 6-month reserve; forgiven on a solvent wind-down; no acceleration except fraud; negative pledge on data, keys and IP.** | ✅ if a lender accepts these terms. Whether one will is **the #1 money risk**. |
| Keepers and Halls | PBC | Yes; sale of services | US sales tax is collected where SaaS or digital services are taxable (economic nexus after *Wayfair*); EU OSS VAT and UK VAT on B2C digital services with no threshold for non-established sellers; B2B reverse charge for Halls with VAT IDs | ✅ |
| Founding pledges ($60) | PBC | Yes; a prepaid year of Keeper membership | Deferred revenue with a refund policy. Not a donation or an investment, and it confers no rights. | ✅ |

**Can a purpose trust be the sole member of a charity?** For a *future* Porchlight Commons 501(c)(3): a Delaware nonstock corporation may have a single member, and any "person" (a trust acting through its trustee) can be one [INFERENCE from 8 Del. C. §§114, 215 (recall)]. The IRS doesn't forbid control by a non-exempt entity as such. However, (i) the charity must still pass the organizational and operational tests and avoid **private benefit**, and a sole member whose purpose includes running a commercial service makes that harder to show; (ii) the charity could not be a §509(a)(3) supporting organisation of a non-charity; (iii) every PBC–Commons transaction becomes a related-party transaction. **Design decision:** the Commons, if created, is **independent**, with a self-perpetuating board that the trust does not appoint, and its relationship to the PBC is contractual only. The IRS's 2014 denial of 501(c)(3) status to the Yorba Foundation, on the ground that open-source software "can be used for any purpose, including nonexempt purposes," shows the exemption risk is real even for purely open-source work [FACT (src: EFF, LWN)], although Mozilla, Wikimedia and the Linux Foundation's charitable affiliates obtained exemption.

**501(c)(3) limits, if we had chosen one** (recorded so the choice can be reviewed): unrelated business income tax (§§511–513) on non-mission revenue; the "commerciality" doctrine; private benefit to users of a consumer app; a lobbying cap (the §501(h) election); a public-support test; and AG oversight that permits conversion. These are reasons the charity is not the operator.

### (a).5 Insolvency and bankruptcy: can a court sell user data?

**The law.** In a US bankruptcy, the trustee may sell estate property under **11 U.S.C. §363**. If the debtor's privacy policy at filing prohibited transferring personally identifiable information, §363(b)(1) allows the sale only (A) if it is consistent with that policy, or (B) after a **consumer privacy ombudsman** (§332) is appointed and the court finds the sale doesn't violate applicable non-bankruptcy law [FACT (recall of statutory text, consistent with the ABI summary)]. **Precedents:** *Toysmart* (2000: the FTC opposed a customer-list sale that violated its privacy policy (recall)); *RadioShack* (2015: the FTC and state AGs limited the customer data sold (recall)); ***In re 23andMe*** (2025, E.D. Mo.): the court approved the sale of the company, including its genetic database, to TTAM Research Institute for **$305M**, finding the sale complied with 23andMe's privacy policy as of the petition date under §363(b)(1)(A). It relied on an ombudsman's work and imposed privacy conditions [FACT (src: White and Williams, HIPAA Journal)]. **Lesson:** a privacy policy that *permits* transfer "in a sale or bankruptcy" is a door. Courts will walk through it.

**The design:**

1. **There is nothing sellable to sell.** Plans, RSVPs, Tables, memory pages, photos and mind stores are ciphertext under keys held in URL fragments and on members' devices (§(c)). A buyer of the database gets noise. The plaintext the PBC does hold is minimal: passkey public keys, optional email addresses for reminders, push endpoints, the billing mapping from member ID to Stripe customer ID, Hall public pages (public by design), and reports that users voluntarily decrypted.
2. **The privacy policy closes the §363(b)(1)(A) door.** It says: "*Personal data will never be sold, licensed or transferred, including in any merger, acquisition, asset sale, insolvency or bankruptcy, except to a successor steward bound by an identical trust deed, and then only for members who opt in; all other personal data will be deleted.*" This clause is a Protected Clause. Under §363(b)(1)(B), a sale that contradicts the policy would also have to survive FTC Act §5 (deception), a non-bankruptcy law. That is the Toysmart argument.
3. **The valuable assets are outside the estate.** The trademarks, domain and code copyright belong to the trust, and the PBC holds only a **non-exclusive, non-assignable licence**. In bankruptcy, IP licences that are personal to the licensee can't be assumed and assigned without the licensor's consent under §365(c)(1): *In re Catapult Entertainment* (9th Cir. 1999) for patents, and *In re XMH Corp.* (7th Cir. 2011) for trademark licences (recall; counsel). The trust is also a creditor-free entity (no operations, no staff, no debt).
4. **Continuity reserve outside the PBC.** The $150k is gifted by the founder *directly to the trust*, so it was never PBC property. That matters under §548 fraudulent-transfer law: a reserve moved *by an insolvent PBC* could be clawed back.
5. **Solvent wind-down before insolvency.** The deed obliges the PBC board to begin the wind-down when (PBC cash plus committed inflows) falls below the cost of 12 months' notice at ember staffing and no bridge is committed within 60 days. The runway policy in the model implements this (§(b).5).
6. **Few creditors.** There is no secured debt. The PRIs are subordinated and forgiven on a solvent wind-down. An involuntary petition (§303) needs three creditors with qualifying claims, and the only candidates are trade creditors paid monthly.

**What remains:** email addresses and billing mappings are real personal data. If the PBC somehow ended up in Chapter 7 despite all this, a trustee might try to sell them. The combination of the policy, §363(b)(1), an ombudsman, the FTC and the deletion schedule (unconfirmed emails deleted after 90 days, billing mappings deleted 90 days after churn) makes that improbable and low in value, but not impossible.

### (a).6 Regulatory strategy, regime by regime

| Regime | Does it apply? | Concrete compliance mechanism | Status verified |
|---|---|---|---|
| **EU DSA** (Reg. 2022/2065) | From v2 (EU launch). Private plans = **hosting service**: not disseminated to the public, because a link sent to named people is not an unlimited audience (Recital 14 reading [INFERENCE; counsel]). Hall public events = **online platform** functionality. The PBC is a micro or small enterprise. | Art. 11–12 points of contact; **Art. 13 legal representative** in the EU (we are not established there; about $1.2k/month budgeted); Art. 14 terms including moderation policy; **Art. 16 notice-and-action** (a report button on every surface, including for guests); **Art. 17 statements of reason** for every action; Art. 18 notification of threats to life or safety. **Art. 19** exempts micro and small online platforms from Section 3 (Arts. 20–28), except Art. 24(3). We **voluntarily** implement Art. 20 (internal complaints), 25 (no dark patterns), 27 (we have no recommender) and 28 (minors), and publish Art. 15-style reports. | Art. 19 [FACT (src: CMS DigitalLaws)] |
| **GDPR** | From v2 (offering to EU residents, Art. 3(2)). We apply the standard globally from v1. | Controller: the PBC. **Art. 27 representative.** Lawful bases: contract (the service), consent (the mind, the Window, open seats). **Art. 35 DPIA** before the mind, open seats and the Window. Art. 30 records. Art. 28 DPAs with Stripe, the host, the email provider and the LLM provider. Art. 20 portability is native (one-tap export). Art. 17 erasure by crypto-shredding. Art. 33 notice within 72 hours. **Transfers:** the EU–US Data Privacy Framework, upheld by the General Court in ***Latombe v Commission*** (T-553/23, 3 Sep 2025), is under appeal (C-703/25 P). SCCs are signed as a fallback. We treat ciphertext as personal data regardless of CJEU reasoning on pseudonymised data. | DPF [FACT (src: IAPP, Bird & Bird)] |
| **EU CSAM rules** | The ePrivacy derogation allowing *voluntary* scanning **expired on 3 April 2026** after Parliament declined to extend it. The CSA Regulation is still in trilogue. | We don't scan private content, which the expired derogation would have required a legal basis for. Reported content that a user decrypts and submits is reviewed, and confirmed CSAM is hashed and reported to NCMEC (US) and to the competent EU authority. If the CSAR ever mandates detection inside E2EE, we'd follow the **R38 breach path**: suspend in the EU before building a scanner (§(g)). | [FACT (src: Freshfields, Agence Europe summary)] |
| **US COPPA** (updated Rule, effective 2025-06-23, full compliance by **2026-04-22**) | Only with "actual knowledge" of collecting data from under-13s, or if the service is "directed to children". Porchlight is general-audience. | **Accounts are 18+ in v1–v2** (a change from Phase 04's 13+; see the kids-law row). The guest flow collects a first name only, no age, and no persistent identifier beyond a per-plan device key. On actual knowledge that a guest is under 13, we delete that RSVP. Parents organise children's parties; children never need an account. Names that organisers type about children stay inside encrypted plan notes and are not "collected from a child". A written retention policy is published, as §312.10 now requires. | Rule dates [FACT (src: Federal Register, Latham)] |
| **US state kids/age-verification laws** | The patchwork is live. **Mississippi HB 1126** (age verification for all account holders plus parental consent for minors): SCOTUS denied emergency relief in Aug 2025 (Kavanaugh: likely unconstitutional). Bluesky blocked Mississippi rather than comply, and has since restored adult access. The Fifth Circuit heard the renewed injunction appeal in early 2026. **Florida HB 3**: enforceable since the 11th Circuit's Nov 2025 stay. **Texas SB 2420** (app-store age verification): enjoined Dec 2025, then **stayed by the Fifth Circuit on 2026-06-04**, so it is in effect. **Virginia SB 854** (one hour a day for under-16s): enjoined 2026-02-27. | **Mechanism: a signed `jurisdictions.json`** in the policy file. It is counsel-maintained and reviewed monthly, and sets each US state and each country to `full`, `guests-only` (no claiming or accounts; guests can still RSVP by first name) or `off`. At launch, **Mississippi is set to `guests-only`** while HB 1126 litigation is unresolved. Florida HB 3's definition (addictive features plus 10% of under-16 daily users on 2+ hours) is very likely not met, since we have no infinite scroll, autoplay or engagement metrics; that needs counsel confirmation. **v1–v2 are web-only (a PWA)**, so the app-store laws (Texas SB 2420, Utah, California AB 1043 from 2027) bite only when v3 native shells ship, and then we consume the OS or store age signals. Age assurance is **self-attestation plus no ID retention**. Where a law demands more for *accounts*, the state goes to guests-only rather than collecting IDs. | All [FACT (src: Techdirt/Bluesky blog, CCIA, Texas Tribune, DLA Piper, Florida Phoenix)] |
| **UK Online Safety Act 2023** | A user-to-user service with UK links once UK users are "significant" or targeted. Illegal-harms duties in force since 2025-03-17. Children's duties in force since July 2025. | v1 does not target the UK: no UK marketing, and an aggregate country counter watches the UK share. Before the **v2 UK launch**: the illegal-content risk assessment (Ofcom's small-services toolkit), a children's access assessment (guest pages are reachable, so assume "likely accessed"), a children's risk assessment, the code measures proportionate to a low-risk, private, no-stranger service, a named senior manager for safety, and reporting and complaints. Primary-priority content (pornography, suicide and self-harm content) is prohibited in the rules, and memory-page uploads come only from 18+ claimed members. The **s.121 technology-notice** power over E2EE remains (§(g)). | Duty dates [FACT (src: Ofcom)]. Small forums closed rather than comply, e.g. LFGSS [FACT (src: Techdirt, spiked)] |
| **Australia Social Media Minimum Age** (in force 2025-12-10) | Unclear. Messaging, gaming, education and health are excluded; event tools are not named. | **We avoid Australia** in v1–v2 and ask eSafety for a view before any launch. | [FACT (src: eSafety, DITRDCA)] |
| **Section 230** (47 U.S.C. §230) | Yes: plans, toasts and photos are third-party content, so (c)(1) protects us from publisher liability, and (c)(2) protects good-faith moderation. | We don't rely on 230 for **design** claims (*Lemmon v. Snap*, 9th Cir. 2021) or for our own output. **Algorithmic curation as first-party speech** (*Anderson v. TikTok*, 3d Cir. 2024) doesn't reach us, because we have no ranker. **Mind output** is treated as our own speech: it returns drafts only to its member and never publishes (Phase 04 M10). We're designed for a world **without 230**: the **Sunset Section 230 Act** bills (S.3546, Durbin–Graham, Dec 2025; H.R. 10332, 2026-09-10) would repeal it two years after enactment. E2EE, small audiences and no amplification minimise publisher exposure either way. | Bills [FACT (src: congress.gov)] |
| **TAKE IT DOWN Act** | Yes: we host user images (memory pages), so we're a "covered platform". FTC enforcement began 2026-05-19. | A **48-hour NCII removal desk**: a request form (no account needed), removal of the item and known identical copies (hash-matched within the plan or Table where we hold the ciphertext object; we delete the blob and key wraps), and a log. It is staffed within the T&S fixed hours in the model. | [FACT (src: FTC)] |
| **18 U.S.C. §2258A / REPORT Act** | Yes, on actual knowledge | Report to the NCMEC CyberTipline and preserve for a year. There is no duty to scan (§2258A(f)). | recall |
| **FOSTA (§230(e)(5))** | Yes | Rules prohibit it. Open seats (v3) are off for any plan flagged commercial. Reports are escalated. | recall |
| **DMCA §512** | Yes (photos) | Registered designated agent ($6). Notice-and-takedown for reported items. Repeat-infringer policy. | recall |
| **ECPA/SCA, CLOUD Act** | Yes | A published law-enforcement guide: content requires a warrant, and we hold ciphertext only; metadata is minimal (7-day truncated logs). We notify users unless gagged. A semi-annual transparency report. We challenge overbroad requests. | recall |
| **CCPA/CPRA and state privacy laws** | Probably below the CCPA thresholds (revenue over ~$26.6M; buying, selling or sharing data on 100k+ consumers). Texas-style laws apply to non-small businesses. | We comply with the strongest standard anyway: no sale or "sharing", no sensitive-data inference, and rights requests answered by the export and delete tools. Passkeys keep biometrics on the device, so BIPA is not triggered. | recall |
| **Accessibility**: EU Accessibility Act (services, from 2025-06-28; microenterprise exemption), ADA Title III | Yes and partly | WCAG 2.2 AA as a release gate; published audit | recall |
| **Payments**: *Epic v. Apple* | Only for v3 native shells | The US link-out to web checkout is permitted (the Ninth Circuit affirmed contempt on 2025-12-11, and SCOTUS granted certiorari in June 2026, so this is unsettled). The core is web-first, so it doesn't depend on the outcome. | [FACT (src: Cravath, IPWatchdog)] |

### (a).7 Launch jurisdictions, and where we don't go

| Phase | Launch | Why | Avoid, and why |
|---|---|---|---|
| **v1 (month 6)** | **United States, web only**, with the `jurisdictions.json` gating (Mississippi guests-only) | English-first T&S parity (Phase 04 R36). 230 plus the First Amendment environment. The US is where the team and counsel are. No EU representative or UK OSA duties while we don't target those markets. | **UK, EU** (not yet: a compliance stack is needed first), **Australia** (unclear scope under the minimum-age law) |
| **v2 (month 15)** | **EU/EEA (English-first, then German, French and Spanish, each only with in-house T&S in that language), UK, Ireland, Canada** | Largest privacy-positive markets. The DSA small-enterprise exemptions keep the burden proportionate. The UK only after the OSA assessments are done. | Any jurisdiction whose law **requires breaking E2EE, traceability of message originators, or real-name/ID registration for accounts**, e.g. India's IT Rules traceability duty for significant intermediaries (recall), Russia, China, and states with data-localisation-plus-access regimes. **We don't operate where compliance means building surveillance.** That costs reach, and the covenant accepts the cost. |
| **v3 (month 30+)** | Latin America in Spanish and Portuguese, only with safety parity. Australia only if eSafety confirms the minimum-age law doesn't apply. | WhatsApp-heavy link-sharing markets (Phase 04 §7.3) | |

### (a).8 The legal checklist (phase items (a)–(g), plus others)

| # | Item | Status and mechanism |
|---|---|---|
| **(a)** | **Trademark clearance for the name** | **Knockout search done (web). Result: "Porchlight" fails.** Found: PORCHLIGHT (Porchlight Book Company, Reg. 6028585); PORCHLIGHT EQUITY (Reg. 5444512); **PORCHLIGHT applied for by Pixabits LLC (Serial 99404159) for teleconferencing, VoIP and communication services**, the closest in kind to our Class 38/42/45 services; PORCHLIGHT (Serial 99370409, filed 2025-09-02), which received a §2(d) likelihood-of-confusion refusal, meaning an earlier registrant already occupies the space; a TTAB proceeding involving Porchlight Communications Holdings; and common-law uses in the same field, **Porchlight Event Co. (a web-based event-planning app)** and **Porchlight: Art + Hospitality (app.porchlight.art)**; plus the adjacent PORCH marks (Porch Group) [FACT (src: search summaries of USPTO/Justia/CIPO records; primary USPTO pages were blocked)]. **Decision: rename before launch.** Process: shortlist 10 coined or arbitrary names → attorney full search (USPTO, state registers, common law, EUIPO, UKIPO, WIPO Madrid, app stores, domains and handles) → a US §1(b) intent-to-use filing in Classes 9, 38, 42 and 45 → a Madrid extension to the EU, UK and Canada before v2. Budgeted inside the $90k formation line. The trust owns the mark. |
| **(b)** | **Trade dress** | Familiar *patterns* (an RSVP button, a guest list, an event card) are functional and free to use. Distinctive incumbent *look* is not: Partiful's visual style, Apple Invites' photo-poster layout, Facebook Events' blue. The drawn-house motif is original, commissioned art (under a work-for-hire and assignment to the trust). A design review checklist compares every screen with the incumbents before release. |
| **(c)** | **Nominative use only** | Text only, in the form "Add to Google Calendar", "Paste into WhatsApp", "Connect your YouTube (read-only)". No logos (we use generic icons), no "partner" or "official" language, and a disclaimer on integration pages. The claim linter (Phase 04 R24) blocks marketing copy that pairs an incumbent name with implied endorsement. |
| **(d)** | **Copyright** | Others' content appears only through official embeds (oEmbed per post URL), links, or the member's own authorised connection (the v3 Window), and is **never re-hosted**. Memory-page photos are uploaded by members who warrant they have the rights, under a licence to us limited to encrypting and storing them for the invitees. §512 agent registered. |
| **(e)** | **Data acquisition** | Official APIs plus user OAuth only. The mind's tool registry has no scraping tool, and a CI test enumerates it (Phase 04 M5). No login circumvention, no rate-limit evasion, no headless browsers against incumbents. Portability imports use official channels (DMA Art. 6(9) and TikTok/Google portability APIs in the EEA and UK, GDPR exports, Utah's Digital Choice Act). |
| **(f)** | **Platform-risk architecture** | **The wedge uses zero incumbent APIs** (Phase 04 H9). A chaos test on every release turns off all third-party integrations; core flows must pass 100%. Calendar has an .ics fallback. The Window's sources are optional and labelled when absent. Delivery by email has an .ics attachment fallback. There is no single-vendor dependency in infrastructure (§(c).4). |
| **(g)** | **Claims discipline** | Every public statement naming an incumbent carries its flag ([FACT]/[ATTRIBUTED]/[ALLEGED]/[CONTESTED]). The claim linter runs in CI on the website and help centre. Press lines are "invitation, not retribution": we don't run attack comparisons. |
| + | Terms, privacy policy, community rules | Plain-language, versioned, 30-day notice with diffs (R32). The privacy clause from §(a).5 is a Protected Clause. |
| + | Employment | No NDAs over safety findings (R35). T&S exposure caps and paid wellness time. The 4× pay ratio is published. Contractors never do moderation. |
| + | Insurance | D&O (trustees, directors, Guardian), cyber, tech E&O, general liability for Halls' events (**Halls sign a responsibility clause; we are not the event organiser**) |
| + | Open-source licences | AGPL-3.0 for server and client. A CLA-free, DCO-based contribution model so contributors keep their copyright and no future owner can relicense proprietarily. The spec is CC BY. |
| + | Export controls | Standard encryption is mass-market; the EAR self-classification (5D992) is documented (recall). |
| + | Securities | Members, Keepers and patrons hold **no economic interest**, so they are not securities. PRIs are negotiated loans with accredited foundations, not public offerings. |

### (a).9 Questions counsel must answer before signing

1. Does Delaware §3541 (cy pres for purpose trusts) allow a court to override a deed's named fallback purpose, and how tightly can the fallback be drafted?
2. Are the deed's prohibitions on decanting (§3528) and non-judicial settlement (§3338) fully effective for protected provisions?
3. Is 1 of 50 shares (2%) enough for §367 standing, and can the charter grant the Guardian enforcement standing beyond §367?
4. Tax: the treatment of the PBC's capital contribution, non-shareholder gifts after the TCJA change to §118, and whether any trust-level income arises from holding IP.
5. Whether §365(c)(1) protects our trademark and domain licence in the PBC's hypothetical bankruptcy in our likely circuit.
6. DSA classification of link-shared private plans (a hosting service rather than an online platform).
7. For each US state kids law: are we a covered "social media platform" if accounts are 18+ and guests have no account?
8. The UK OSA children's-access conclusion for guest pages.
9. Whether PRI terms (forgiveness on wind-down, repayment only from surplus) are acceptable to the foundation's counsel as a §4944 PRI.

---

## (b) Funding the build, with month-by-month math

### (b).1 The defended revenue choice

**Memberships (Keepers) plus organisation subscriptions (Halls).** Donations alone fail because a PBC can't offer a tax deduction and the donor base is uncertain. Subscriptions alone fail because paywalling core features violates the free-floor clause. The model says **Halls carry about 52% of revenue at break-even** (the Hall price is $20/month, a third below Meetup Standard at $29.99/month [FACT (src: Meetup pricing summary)]). This is the most important finding of this section, and Phase 04 missed it by treating Halls as a rounding error (1 per 400 members at $12). Organisations that run weekly events are the natural payers: they get real operational value (recurring events, co-organisers, rosters, public listing), and charging them doesn't put a toll between friends. Keepers stay pay-what-you-can, because the covenant forbids a toll gate between friends and paying never changes what anyone else sees.

**Price change from Phase 04 [REV]:** the Keeper suggestion goes from $4 to **$5/month or $50/year**, which is still at the deed ceiling of $5 in 2026 dollars. The Hall price goes from $12 to **$20**. Reason: with Phase 04's prices under realistic costs, the base plan **runs out of cash at month 35** (the `p04_prices` output below).

### (b).2 Assumptions (all in `funding-model/model.py`, each labelled in code)

| Group | Assumption | Value | Label |
|---|---|---|---|
| Staff cost | Loaded = salary × 1.24 + $7k per year, plus 3% a year. Salaries: senior engineer $170k, security engineer $180k, mid engineer $140k, design/community $135k, T&S lead $115k, T&S specialist $85k, support $72k, ops/finance $120k. Hire cost $15k. | ≈ $12.5k–19.2k per FTE-month in 2027 | [ASSUME: US remote mid-market] |
| Staffing rule | Core 4 FTE (1 senior engineer, 1 security engineer, 1 design/community, 1 T&S lead from month 3). **T&S sized by workload** (0.6 reports per 1k members per month × 0.5 h, plus 40 h fixed; 140 productive hours per FTE-month; a floor of +1 at v2 and +1 at v3), **never by revenue and never cut in a freeze or ember**. Support sized by workload (1.2 tickets per 1k members per month × 0.2 h), halved until break-even. **Growth hires are revenue-gated**: none until trailing revenue ≥ 115% of opex. | | [ASSUME] |
| Growth | Casual organisers: 400 a month from non-viral channels at launch, +7% a month to month 48, +2% after, capped at 12k, with a seasonal multiplier (Nov 1.6, Dec 1.7). Organic 0.24 new organisers per organiser-month; retention 70% (**Phase 04 k≈0.8, sub-viral**). Claims: 50% of new organisers, plus 1% of guest touches. Halls (v2): 0.15% of active organisers open one a month, plus direct outreach from 20 a month to 250 a month; 3% churn; 8 new attendees per Hall a month, of whom 30% claim and 3% later host. Member dormancy 2.5% a month. | Base claimed: 4k (m12), 28k (m24), 85k (m36), 226k (m48) | [P04]/[ASSUME]. Partiful-like: about 0.5M monthly users after about 4 years with VC [FACT (P04 src)] |
| Conversion and churn | 3.2% of newly claimed members become Keepers, plus 0.03% a month of the rest. **Keeper churn 4% a month.** Mean chosen amounts $4.25/month and $45/year, 55% annual. | Steady paying share ≈ 3.0% | [ASSUME; RevenueCat ~2.1% freemium anchor (P04 src)] |
| Payment fees | Stripe 2.9% + $0.30, Billing 0.7%, Tax 0.5%; international cards +1.5% and FX +1% on 30% of payers after v2; refunds and chargebacks 1%; ACH for institutions | ≈ 12% on a $4.25 monthly charge, ≈ 5% on annual | [FACT (src: Stripe fee summaries)] |
| VAT / sales tax | EU/UK prices include VAT (21% blended) on 25% of consumer payers after v2, remitted. B2B Halls are reverse-charged (30% taxable). US sales tax is charged on top and passed through. | | [FACT for the rates; ASSUME for the mix] |
| Variable cost | Infrastructure $0.012, email $0.002, mind (v2+) 30% × $0.05, $0.0005 per guest touch | ≈ $0.031 per member-month | [P04], re-derived in §(c) |
| Legal and compliance | Formation $90k (months 0–2); counsel $5k a month (v1), $9k (v2+), plus $3k per million members; EU/UK representatives $1.2k; Delaware trustee, Guardian and enforcer $2k; insurance $2k plus $1k per million members; accounting $3.7k | | [ASSUME] |
| Audits | Pre-launch E2EE crypto audit $80k; annual security audit $50k; semi-annual covenant audit (H5) $20k; election administration $10k a year | | [ASSUME] |
| Runway policy | Freeze non-safety hiring below 9 months of runway (counting inflows scheduled within 6 months). **Ember mode** below 6 months: 1 engineer, 0.5 security from 250k members, 0.5 design/community, T&S at full workload, support at half; mind paused; external acquisition halved. Leave ember only when the *normal* team would have more than 12 months of runway. | | Deed rule |

### (b).3 Funding sources in sequence (no investors, no ads, no creator economics, no debt secured on data)

| Month | Source | Amount | Conditions |
|---|---|---|---|
| 0 | **Steward/founder gift** | $800k ($650k to PBC; $150k to the trust as continuity reserve) | Irrevocable. No retained powers. **The largest single assumption**: without about $650k of working capital, v1 can't be built at realistic pay. The alternative is a 2-person, 12-month build. |
| 3, 7 | Seed grants (candidates: public-interest technology and trust-and-safety funders; open-infrastructure funders for the plan-format spec) | 2 × $100k | Expenditure responsibility or fiscal sponsor. No-control, no-data letter. |
| 6 | Founding pledges | 1,200 × $60 = $72k | A prepaid membership year, refundable |
| 6 → | Patrons | $4k/month (m6), $7k (m18), $8k (m36) | Capped at $10k per person per year. Named publicly unless they ask otherwise. No access. |
| 9 → 63 | Program grants | $2.15M by break-even, in tranches of $200k or less | Deed source caps bind from **month 60** (see §(b).6) |
| **12** | **Recoverable PRI #1** | **$1.25M** | Gate: H1–H3 read and passed (proxy in model: ≥2k claimed members, ≥2% paying). Terms per §(a).4. |
| **36** | **Recoverable PRI #2** | **$1.25M** | Gate: H4/H7 (≥30k claimed, ≥2% paying) |
| 67 → | **Operating revenue covers operating cost** | | Break-even |
| ~100 → | PRI repayment from surplus above a 6-month reserve | | Model: repayment starts about month 100 |

### (b).4 Model output: base case, month 0 to break-even (pasted verbatim from `python3 model.py --all`)

```
============================================================================================================
BASE CASE: month by month, month 0 to break-even + 3
============================================================================================================
mo yyyy-mm mode   claimed  halls  pay%   fte  op_rev   opex   op_net  grants patron   loan debtSv    cash cum_def
 0 2027-01 normal       0      0  0.00  3.0       0   142k    -142k       0      0      0      0    508k    142k
 1 2027-02 normal       0      0  0.00  3.0       0    97k     -97k       0      0      0      0    411k    238k
 2 2027-03 normal       0      0  0.00  3.0       0    97k     -97k       0      0      0      0    314k    335k
 3 2027-04 normal       6      0  0.00  4.0       0    94k     -94k    100k      0      0      0    320k    429k
 4 2027-05 normal      13      0  0.00  4.0       0    79k     -79k       0      0      0      0    240k    508k
 5 2027-06 normal      23      0  0.00  4.0       0   159k    -159k       0      0      0      0     81k    667k
 6 2027-07 normal     260      0  2.96  4.0      28    80k     -80k       0     4k      0      0     74k    747k
 7 2027-08 normal     560      0  3.10  4.0      63    80k     -80k    100k     4k      0      0     98k    826k
 8 2027-09 normal     991      0  3.15  4.0     113    80k     -80k       0     4k      0      0     22k    906k
 9 2027-10 normal      2k      0  3.17  4.0     181    80k     -79k    150k     4k      0      0     96k    985k
10 2027-11 normal      2k      0  3.18  4.0     274    80k     -79k       0     4k      0      0     20k   1.06M
11 2027-12 normal      3k      0  3.18  4.0     388   100k     -99k    150k     4k      0      0     75k   1.16M
12 2028-01 normal      4k      0  3.18  4.0     485    82k     -81k       0     4k  1.25M      0   1.25M   1.25M
13 2028-02 normal      5k      0  3.17  4.0     592    82k     -81k       0     4k      0      0   1.17M   1.33M
14 2028-03 normal      6k      0  3.17  4.0     711    82k     -81k       0     4k      0      0   1.09M   1.41M
15 2028-04 normal      7k     27  3.16  5.0      1k   113k    -112k    200k     4k      0      0   1.18M   1.52M
16 2028-05 normal      9k     54  3.16  5.0      2k    98k     -97k       0     4k      0      0   1.09M   1.62M
17 2028-06 normal     10k     83  3.15  5.0      2k   168k    -166k       0     4k      0      0    929k   1.78M
18 2028-07 normal     12k    113  3.15  5.0      3k    98k     -95k       0     7k      0      0    840k   1.88M
19 2028-08 normal     14k    144  3.15  5.0      4k    98k     -95k       0     7k      0      0    752k   1.97M
20 2028-09 normal     16k    176  3.14  5.0      4k    99k     -94k       0     7k      0      0    665k   2.07M
21 2028-10 normal     19k    209  3.14  5.0      5k    99k     -93k    200k     7k      0      0    778k   2.16M
22 2028-11 normal     22k    245  3.14  5.0      6k    99k     -93k       0     7k      0      0    692k   2.25M
23 2028-12 normal     25k    283  3.14  5.0      7k   119k    -112k       0     7k      0      0    586k   2.36M
24 2029-01 normal     28k    323  3.13  5.0      8k   111k    -103k       0     7k      0      0    490k   2.47M
25 2029-02 normal     32k    365  3.13  5.0      9k   101k     -92k       0     7k      0      0    404k   2.56M
26 2029-03 ember      35k    408  3.12  5.0     10k   101k     -91k       0     7k      0      0    319k   2.65M
27 2029-04 ember      39k    424  3.12  2.5     11k    59k     -48k    200k     7k      0      0    478k   2.70M
28 2029-05 ember      42k    440  3.11  2.5     11k    59k     -47k       0     7k      0      0    437k   2.75M
29 2029-06 ember      46k    458  3.11  2.5     12k    94k     -82k       0     7k      0      0    362k   2.83M
30 2029-07 normal     49k    476  3.10  2.5     12k    59k     -46k       0     7k      0      0    322k   2.87M
31 2029-08 normal     54k    527  3.10  6.0     14k   165k    -151k       0     7k      0      0    178k   3.03M
32 2029-09 normal     58k    582  3.10  6.0     15k   112k     -97k       0     7k      0      0     87k   3.12M
33 2029-10 normal     64k    639  3.09  6.0     16k   112k     -96k    200k     7k      0      0    198k   3.22M
34 2029-11 normal     70k    701  3.09  6.0     18k   113k     -95k       0     7k      0      0    110k   3.31M
35 2029-12 normal     78k    768  3.09  6.0     20k   133k    -113k       0     7k      0      0      4k   3.43M
36 2030-01 normal     85k    841  3.09  6.0     22k   126k    -104k       0     8k  1.25M      0   1.16M   3.53M
37 2030-02 normal     92k    916  3.09  6.0     24k   116k     -92k       0     8k      0      0   1.07M   3.62M
38 2030-03 normal    100k    994  3.09  6.0     26k   116k     -91k       0     8k      0      0    990k   3.71M
39 2030-04 normal    109k     1k  3.08  6.0     28k   116k     -89k    200k     8k      0      0   1.11M   3.80M
40 2030-05 normal    118k     1k  3.08  6.0     30k   117k     -87k       0     8k      0      0   1.03M   3.89M
41 2030-06 normal    128k     1k  3.08  6.0     32k   187k    -155k       0     8k      0      0    882k   4.04M
42 2030-07 normal    139k     1k  3.08  6.0     35k   118k     -82k       0     8k      0      0    807k   4.13M
43 2030-08 normal    150k     1k  3.08  6.0     38k   118k     -80k       0     8k      0      0    735k   4.21M
44 2030-09 normal    162k     2k  3.08  7.0     41k   142k    -102k       0     8k      0      0    641k   4.31M
45 2030-10 normal    176k     2k  3.08  7.0     44k   128k     -84k    200k     8k      0      0    765k   4.39M
46 2030-11 normal    192k     2k  3.08  7.0     47k   128k     -81k       0     8k      0      0    691k   4.47M
47 2030-12 normal    210k     2k  3.08  7.0     51k   149k     -98k       0     8k      0      0    601k   4.57M
48 2031-01 normal    226k     2k  3.07  7.0     55k   142k     -87k       0     8k      0      0    522k   4.66M
49 2031-02 normal    243k     2k  3.07  7.0     59k   133k     -74k       0     8k      0      0    455k   4.73M
50 2031-03 normal    261k     2k  3.07  7.0     63k   133k     -70k       0     8k      0      0    393k   4.80M
51 2031-04 normal    280k     3k  3.07  7.0     68k   134k     -67k    150k     8k      0      0    484k   4.87M
52 2031-05 normal    300k     3k  3.07  7.0     72k   135k     -63k       0     8k      0      0    429k   4.93M
53 2031-06 ember     321k     3k  3.06  7.0     77k   205k    -129k       0     8k      0      0    308k   5.06M
54 2031-07 ember     339k     3k  3.06  5.0     80k    97k     -17k       0     8k      0      0    299k   5.08M
55 2031-08 ember     357k     3k  3.06  5.0     82k    97k     -15k       0     8k      0      0    291k   5.09M
56 2031-09 ember     375k     3k  3.05  5.0     85k    97k     -13k       0     8k      0      0    286k   5.10M
57 2031-10 normal    394k     3k  3.05  5.0     88k    98k     -10k    150k     8k      0      0    434k   5.11M
58 2031-11 normal    417k     3k  3.05  7.0     93k   169k     -76k       0     8k      0      0    366k   5.19M
59 2031-12 normal    442k     3k  3.04  7.0     99k   160k     -61k       0     8k      0      0    313k   5.25M
60 2032-01 normal    465k     4k  3.04  7.0    105k   153k     -48k       0     8k      0      0    272k   5.30M
61 2032-02 normal    489k     4k  3.04  7.0    111k   144k     -33k       0     8k      0      0    247k   5.33M
62 2032-03 normal    514k     4k  3.04  7.0    117k   145k     -28k       0     8k      0      0    226k   5.36M
63 2032-04 normal    540k     4k  3.03  7.0    124k   146k     -22k    150k     8k      0      0    362k   5.38M
64 2032-05 normal    567k     5k  3.03  7.0    130k   147k     -16k       0     8k      0      0    353k   5.40M
65 2032-06 normal    596k     5k  3.03  7.0    137k   218k     -80k       0     8k      0      0    280k   5.48M
66 2032-07 normal    624k     5k  3.03  7.0    144k   149k      -4k       0     8k      0      0    284k   5.48M
67 2032-08 normal    653k     6k  3.02  7.0    152k   150k       2k       0     8k      0      0    294k   5.48M
68 2032-09 normal    684k     6k  3.02  7.0    159k   151k       9k       0     8k      0      0    310k   5.47M
69 2032-10 normal    717k     6k  3.02  7.0    167k   152k      15k    150k     8k      0      0    482k   5.46M
70 2032-11 normal    753k     6k  3.02  7.0    175k   153k      22k       0     8k      0      0    512k   5.46M

scenario=base
  break-even (first of 3 consecutive months with operating revenue >= operating cost): month 67 (2032-08)
  build cost to sustainability = peak cumulative operating deficit: $5.48M
  at break-even: claimed 653k, Halls 6k, paying 3.02%, FTE 7.0, opex $150k/mo, op revenue $152k/mo
  inflows to then: founder $800k (of which $150k trust reserve), grants $2.15M, patrons $430k, founding pledges $72k, PRI loan $2.50M
  min PBC cash $4k; cash<0 (wind-down trigger) never; ember months 8; grants declined by deed caps $0
  pay ratio highest/median salary 1.33 (deed cap 4.0)
```

**Reading it.** (1) The build phase (months 0–5) costs $667k before a single user arrives. The pre-launch crypto audit ($80k) is the spike at month 5. (2) Revenue is negligible for three years (under $20k a month until month 35). Sub-viral growth compounds slowly. (3) **The plan survives on a knife-edge.** Cash falls to $4k at month 35, one month before PRI #2, and the runway policy puts the team into ember twice (months 26–29 and 53–56). (4) Break-even arrives at month 67 with 7 FTE because growth hiring is revenue-gated. After break-even the surplus funds workload hires and, from about month 100, PRI repayment.

### (b).5 Sensitivity, and the halfway-shortfall plan (pasted verbatim)

```
============================================================================================================
SENSITIVITY (same funding plan and runway policy)
============================================================================================================
scenario=conv_half
  break-even (first of 3 consecutive months with operating revenue >= operating cost): NOT within 120 months
  build cost to sustainability = peak cumulative operating deficit: $5.49M
  at horizon: claimed 1.16M, Halls 5k, paying 1.45%, FTE 6.0, opex $144k/mo, op revenue $134k/mo
  inflows to then: founder $800k (of which $150k trust reserve), grants $2.00M, patrons $846k, founding pledges $72k, PRI loan $0
  min PBC cash $-1.99M; cash<0 (wind-down trigger) at month 12; ember months 108; grants declined by deed caps $300k
  pay ratio highest/median salary 1.33 (deed cap 4.0)

scenario=growth_half
  break-even (first of 3 consecutive months with operating revenue >= operating cost): NOT within 120 months
  build cost to sustainability = peak cumulative operating deficit: $6.27M
  at horizon: claimed 279k, Halls 2k, paying 2.87%, FTE 4.0, opex $104k/mo, op revenue $59k/mo
  inflows to then: founder $800k (of which $150k trust reserve), grants $2.00M, patrons $846k, founding pledges $72k, PRI loan $0
  min PBC cash $-2.74M; cash<0 (wind-down trigger) at month 13; ember months 110; grants declined by deed caps $300k
  pay ratio highest/median salary 1.33 (deed cap 4.0)

scenario=both
  break-even (first of 3 consecutive months with operating revenue >= operating cost): NOT within 120 months
  build cost to sustainability = peak cumulative operating deficit: $6.90M
  at horizon: claimed 272k, Halls 2k, paying 1.44%, FTE 4.0, opex $104k/mo, op revenue $43k/mo
  inflows to then: founder $800k (of which $150k trust reserve), grants $2.00M, patrons $846k, founding pledges $72k, PRI loan $0
  min PBC cash $-3.38M; cash<0 (wind-down trigger) at month 13; ember months 110; grants declined by deed caps $300k
  pay ratio highest/median salary 1.33 (deed cap 4.0)

scenario=halls_half
  break-even (first of 3 consecutive months with operating revenue >= operating cost): month 90 (2034-07)
  build cost to sustainability = peak cumulative operating deficit: $6.00M
  at break-even: claimed 739k, Halls 2k, paying 2.93%, FTE 5.0, opex $110k/mo, op revenue $114k/mo
  inflows to then: founder $800k (of which $150k trust reserve), grants $2.00M, patrons $614k, founding pledges $72k, PRI loan $2.50M
  min PBC cash $-208k; cash<0 (wind-down trigger) at month 35; ember months 48; grants declined by deed caps $300k
  pay ratio highest/median salary 1.33 (deed cap 4.0)

============================================================================================================
UNCONSTRAINED NEED (runway policy off: what each world would cost to reach break-even)
============================================================================================================
  base         break-even month 66               peak cumulative operating deficit $  5.59M   min cash $-159k
  conv_half    break-even month 90               peak cumulative operating deficit $  7.02M   min cash $-3.73M
  growth_half  break-even none in 180 months     peak cumulative operating deficit $ 12.65M   min cash $-8.67M
  both         break-even none in 180 months     peak cumulative operating deficit $ 16.66M   min cash $-12.68M
  halls_half   break-even month 78               peak cumulative operating deficit $  6.73M   min cash $-1.03M

============================================================================================================
HALFWAY SHORTFALL: from month 33 every grant and the PRI fail; patrons halve
============================================================================================================
scenario=shortfall_m33
  break-even (first of 3 consecutive months with operating revenue >= operating cost): month 78 (2033-07)
  build cost to sustainability = peak cumulative operating deficit: $4.48M
  at break-even: claimed 547k, Halls 4k, paying 2.99%, FTE 5.0, opex $105k/mo, op revenue $111k/mo
  inflows to then: founder $800k (of which $150k trust reserve), grants $1.10M, patrons $336k, founding pledges $72k, PRI loan $1.25M
  min PBC cash $-1.11M; cash<0 (wind-down trigger) at month 38; ember months 53; grants declined by deed caps $0
  pay ratio highest/median salary 1.33 (deed cap 4.0)

mo yyyy-mm mode   claimed  halls  pay%   fte  op_rev   opex   op_net  grants patron   loan debtSv    cash cum_def
 0 2027-01 normal       0      0  0.00  3.0       0   142k    -142k       0      0      0      0    508k    142k
 3 2027-04 normal       6      0  0.00  4.0       0    94k     -94k    100k      0      0      0    320k    429k
 6 2027-07 normal     260      0  2.96  4.0      28    80k     -80k       0     4k      0      0     74k    747k
 9 2027-10 normal      2k      0  3.17  4.0     181    80k     -79k    150k     4k      0      0     96k    985k
12 2028-01 normal      4k      0  3.18  4.0     485    82k     -81k       0     4k  1.25M      0   1.25M   1.25M
15 2028-04 normal      7k     27  3.16  5.0      1k   113k    -112k    200k     4k      0      0   1.18M   1.52M
18 2028-07 normal     12k    113  3.15  5.0      3k    98k     -95k       0     7k      0      0    840k   1.88M
21 2028-10 normal     19k    209  3.14  5.0      5k    99k     -93k    200k     7k      0      0    778k   2.16M
24 2029-01 normal     28k    323  3.13  5.0      8k   111k    -103k       0     7k      0      0    490k   2.47M
27 2029-04 ember      39k    424  3.12  2.5     11k    59k     -48k    200k     7k      0      0    478k   2.70M
30 2029-07 ember      49k    476  3.10  2.5     12k    59k     -46k       0     7k      0      0    322k   2.87M
33 2029-10 ember      60k    534  3.09  2.5     14k    59k     -44k       0     4k      0      0    203k   3.01M
36 2030-01 ember      74k    604  3.08  2.5     17k    65k     -48k       0     4k      0      0     68k   3.15M
39 2030-04 ember      88k    684  3.06  2.5     20k    61k     -41k       0     4k      0      0    -46k   3.28M
42 2030-07 ember     104k    777  3.05  2.5     23k    61k     -38k       0     4k      0      0   -187k   3.43M
45 2030-10 ember     122k    886  3.05  2.5     26k    61k     -35k       0     4k      0      0   -284k   3.54M
48 2031-01 ember     147k     1k  3.04  2.5     31k    68k     -37k       0     4k      0      0   -386k   3.65M
51 2031-04 ember     172k     1k  3.04  3.5     36k    72k     -36k       0     4k      0      0   -504k   3.78M
54 2031-07 ember     201k     1k  3.03  3.5     42k    73k     -31k       0     4k      0      0   -627k   3.92M
57 2031-10 ember     233k     2k  3.03  3.5     48k    73k     -25k       0     4k      0      0   -698k   4.00M
60 2032-01 ember     271k     2k  3.02  4.0     56k    92k     -36k       0     4k      0      0   -796k   4.11M
63 2032-04 ember     308k     2k  3.01  4.0     63k    87k     -24k       0     4k      0      0   -864k   4.19M
66 2032-07 ember     350k     2k  3.01  5.0     72k    99k     -27k       0     4k      0      0   -981k   4.31M
69 2032-10 ember     393k     3k  3.00  5.0     81k   100k     -18k       0     4k      0      0  -1.03M   4.38M
72 2033-01 ember     445k     3k  3.00  5.0     91k   108k     -16k       0     4k      0      0  -1.08M   4.43M
75 2033-04 ember     494k     3k  2.99  5.0    101k   104k      -3k       0     4k      0      0  -1.08M   4.45M
78 2033-07 ember     547k     4k  2.99  5.0    111k   105k       6k       0     4k      0      0  -1.10M   4.47M
81 2033-10 ember     601k     4k  2.98  5.0    120k   106k      14k       0     4k      0      0  -1.05M   4.45M

============================================================================================================
RECONCILIATION WITH PHASE 04
============================================================================================================
scenario=p04_prices
  break-even (first of 3 consecutive months with operating revenue >= operating cost): month 92 (2034-09)
  build cost to sustainability = peak cumulative operating deficit: $6.05M
  at break-even: claimed 936k, Halls 5k, paying 2.93%, FTE 6.0, opex $125k/mo, op revenue $125k/mo
  inflows to then: founder $800k (of which $150k trust reserve), grants $2.00M, patrons $630k, founding pledges $72k, PRI loan $2.50M
  min PBC cash $-257k; cash<0 (wind-down trigger) at month 35; ember months 50; grants declined by deed caps $300k
  pay ratio highest/median salary 1.33 (deed cap 4.0)

scenario=p04_growth
  break-even (first of 3 consecutive months with operating revenue >= operating cost): month 42 (2030-07)
  build cost to sustainability = peak cumulative operating deficit: $3.24M
  at break-even: claimed 1.01M, Halls 6k, paying 3.09%, FTE 7.0, opex $157k/mo, op revenue $204k/mo
  inflows to then: founder $800k (of which $150k trust reserve), grants $1.50M, patrons $230k, founding pledges $72k, PRI loan $2.50M
  min PBC cash $22k; cash<0 (wind-down trigger) never; ember months 0; grants declined by deed caps $0
  pay ratio highest/median salary 1.33 (deed cap 4.0)

  p04_growth claimed members at month 36: 573k (P04 assumed 1.2M)
  base claimed members at month 12/24/36: 4k / 28k / 85k (P04 assumed 50k / 400k / 1.2M)
```

**What the sensitivity says, plainly:**

| World | Funded plan outcome | What it would take |
|---|---|---|
| Base | Break-even month 67, $5.48M | As planned. There is almost no slack. |
| **Conversion halved** (1.45% paying) | The PRI #1 gate fails at month 12, cash runs out at month 12, **and the deed's wind-down triggers** | $7.0M, with break-even at month 90. A lender would have to accept H7 at 1.5%. |
| **Growth halved** | Gate fails, wind-down at month 13 | **No break-even within 15 years at any funding**: fixed cost outruns a sub-viral base. The small house doesn't exist in that world. |
| **Both** | Wind-down at month 13 | Same as above, worse |
| Halls halved | Cash runs out at month 35 (a $0.2M gap); break-even month 90 | $6.0M |

**The halfway-shortfall plan** (grants and PRIs stop from month 33, patrons halve). This is what the deed makes happen, in order:

1. **Month 33, trigger:** runway below 9 months, so a hiring freeze (never on T&S). A public ledger post the same week says what happened. No euphemisms.
2. **Month 33–34, ember mode:** 2.5–5 FTE depending on T&S workload. The mind is paused and says so. v3 features (open seats, the Window) are paused. External acquisition halves. **Every free-floor feature keeps working.** Ember net burn is about $35–48k a month (opex of about $60k against $14–26k of revenue).
3. **Month 34–36, bridge ask, bounded:** the model shows ember needs about **$1.1M** more to reach its own break-even (month 78, about 547k members, 5 FTE). Sources we may ask for, all within the charter: a second steward gift; a PRI from a different lender under the same terms; a one-time, honest "keep the light on" appeal to members; a patron drive. **We may not ask for** equity, convertible notes, revenue-share loans, ads, data deals, or lifting the grant caps (Phase 04's "design is false" condition).
4. **Month 38, no bridge committed → solvent wind-down** under the deed. The trust's $150k continuity reserve pays for 12 months' notice. Export tools keep running. Memory pages and plans move to a **static read-only archive**; because the key lives in the link, a static host can serve and decrypt them in the browser for pennies. The code and the plan-format spec pass to a named successor steward. Members get their data and the successor's address. The PBC shuts down without a bankruptcy, a §363 sale or a buyer.
5. **Earlier kill switches still apply:** H3 below 1.5% at month 6, or H7 below 1% at month 24 (Phase 04 §8), means wind-down or a redesign vote, whatever the cash position.

### (b).6 Reconciliation with Phase 04 (honest)

| Phase 04 said | 04b finds | Why |
|---|---|---|
| Pre-break-even gap **$1.5–2.5M** | **$5.48M** | Loaded staff cost, workload-sized T&S and support, compliance and audit lines, and much slower growth |
| **1.2M claimed members by month 36** (50k at m12, 400k at m24) | **85k at month 36** (4k, 28k) | **Phase 04 contradicted itself.** Its own spread numbers (3% guest-to-host, 70% organiser retention, so k≈0.8) are sub-viral: growth tracks external acquisition. Even with k=1.2 (80% retention) and nearly 4× more launch acquisition, the model reaches only 573k at month 36 (`p04_growth`). |
| Small house at ~1.2M members, 5–6 staff, $65–75k/month | Break-even at **~650k** members, **7 FTE**, **$150k/month** | Higher revenue per member (Halls at $20, Keepers at $5) against a realistic cost base |
| $11k per person-month | ≈ $15k blended | Market salaries plus 24% load plus equipment |
| Keeper $4, Halls $12 at 1 per 400 | $5 / $20; Halls emerge at about 1 per 120 members | At Phase 04's prices, cash runs out at month 35 (`p04_prices`) |
| "No single source above 10%, grants ≤25% after year 3" | **Caps re-dated to month 60** | Before break-even, a 10% cap would forbid any grant larger than about $10–30k and **starve the build**: the model declined $300k of grants even with the caps binding from month 60 in the sensitivity runs. Before month 60, funder capture is prevented by **terms** (no control, no data, no board seats, public ledger), not by share caps. |

### (b).7 What the charter's constraints cost, stated once

No investors and no ads mean about **$5.5M of patient, non-controlling money over 5.5 years**, and a service that can die at a gate rather than pivot to extraction. In-house, paid, exposure-capped trust and safety costs about $0.03 per member per month at scale. The E2EE server that can't read plans costs nothing extra in infrastructure, but it forecloses every revenue line incumbents use. I think the price is right. I don't think it's small.

---

## (c) Technical architecture

### (c).1 Data model: what is stored, where, and who holds the key

| Object | Stored (server) | Encryption | Key holder | Server can read | Retention |
|---|---|---|---|---|---|
| **Plan cover** (art seed, optional title) | `plans(id, cover_ct, size, created_day, expires_at)` | XChaCha20-Poly1305 under `K_cover = HKDF(link_secret, "cover")` | Anyone holding the link. `link_secret` lives in the URL **fragment** (`#…`), which browsers never send to servers. | No (except an optional plaintext title the organiser opts to show in link previews, disclosed) | Plan end + 24 h, then becomes a memory page; deleted by default at 12 months unless kept |
| **Plan inner** (address, notes, guest list) | `plans.inner_ct` + `inner_wraps(plan_id, recipient_key_hash, hpke_ct)` | `K_inner` random, wrapped per confirmed guest device with HPKE (RFC 9180, X25519) | The organiser's device and confirmed guests' devices | No | As above |
| **RSVP** | `rsvps(plan_id, rsvp_ct, device_pub_plan)` | HPKE to the organiser's plan key | Organiser | No. It sees that *a* per-plan key RSVP'd, and the key is **per plan**, so the server can't link one guest across plans. The "Hi Jo" recognition is local, on the device. | With the plan |
| **Member** (claimed) | `members(id, did, passkey_cred_ids, identity_pub, key_backup_ct)` | `key_backup_ct` = identity and device keys wrapped under a key derived via the **WebAuthn PRF extension** of the member's passkey, plus an optional printed recovery code | Member | Public keys only | Until deletion |
| **Email** (optional, for reminders) | `notify.contacts(member_id, email)` in a **separate service and database** | TLS; plaintext at rest (it has to send mail) | PBC | **Yes**, the main plaintext PII | Deleted 90 days after the last reminder or on deletion |
| **Push endpoints** | `notify.push(member_id, endpoint, keys)` | Web Push encryption (RFC 8291) for payloads | Member's browser | Endpoint URL yes, payloads no | Until revoked |
| **Tables** | MLS delivery service: `mls_msgs(group_id, epoch, ct)`, `key_packages` | **MLS (RFC 9420)**, up to 150 members | Members' devices | No content. The delivery service sees which member IDs fetch which group, which is metadata (§(e)). | Rolling 12 months of messages; history is kept on devices and in exports |
| **Media** (memory pages) | Object storage `blob/{random_id}` + `media(id, parent_id, size, uploader_id, expires)` | Per-blob key, wrapped into the plan or Table key tree | Invitees or Table members | No | With the memory page; quota 2 GB free |
| **Mind store** | `mind/{member_id}` blob (SQLCipher DB) | Member key | Member. During an invoked task the client sends the key wrapped to an **ephemeral worker key**. | **Transiently**, in worker memory, during a task the member invoked; LLM provider on zero-retention terms | Member-controlled |
| **Billing** | `billing(member_id, stripe_customer_id, tier, status)` in a **separate database with a separate access role**; Stripe holds card data (PCI SAQ A) | — | PBC and Stripe | Yes, the mapping | 90 days after churn |
| **Halls** | Public page and public events | Plaintext **by design** (published over ActivityPub / AT Protocol) | — | Yes | Until removed |
| **Reports** | `reports(id, object_ref, submitted_excerpt, media, status, sor)` | The excerpt is plaintext that the *reporter* chose to decrypt and submit | T&S | Yes, submitted content only | 12 months (NCMEC preservation 1 year); DSA statements of reasons |
| **Counters** | Aggregate daily counts; privacy-preserving aggregation (IETF **DAP / Prio**, with an independent helper such as ISRG's Divvi Up) for guest-to-host and time-to-done | — | — | Aggregates only; **no per-user event table exists** (schema-audited in CI) | Indefinite (aggregates) |
| **Access logs** | Edge and API logs | — | — | IPs truncated (/24 for IPv4, /48 for IPv6) | **7 days** |
| **Transparency log** | Append-only Merkle log (Sigsum/Trillian-style) | Signed | Public | Yes (public) | Forever |

### (c).2 Key custody and operator keys

- **No user key escrow exists.** The PBC can't decrypt plans, Tables, media or mind stores at rest. If a member loses both their passkey (the synced passkey is the backup) and their recovery code, their encrypted history is gone. The recovery screen says so, in those words.
- **Operator keys.** (i) The **release-signing key** for web bundles is a 2-of-3 hardware-key threshold held by two engineers and the independent privacy trustee. (ii) The **policy-file signing key** is a 3-of-5 multisig of the Stewardship Committee (Phase 04 §4.2). (iii) The **transparency-log key**. (iv) TLS keys at the CDN. None of them decrypts user data. The *release* key is the dangerous one, because it can ship a malicious client (§(e)).

### (c).3 Services

| Service | Language / tech | Notes |
|---|---|---|
| Client (PWA) | TypeScript, WebCrypto, WASM for MLS (OpenMLS) and HPKE | Under 100 KB first load. Reproducible build. CSP `script-src 'self'` plus SRI. No third-party scripts (auditable in devtools). |
| Relay/API | Rust (memory safety on a parser-heavy surface) | Stateless; plan, RSVP and media CRUD; presigned upload URLs |
| MLS delivery service | Rust | Partitioned by `group_id` |
| Notify | Rust | Web Push (VAPID) and email only. **No SMS.** It runs only on member-set triggers (Phase 04 M8). |
| Billing | Separate service and database, Stripe | Can't join to plan data: separate credentials, and there are no foreign keys across databases |
| Mind workers | Ephemeral containers, one per task | Tool allowlist from Phase 04 M5. Cost cap $0.10 per member per month. |
| T&S | Case tooling, hash-matching of **reported** media only, NCII 48-hour desk, DSA statements of reason, NCMEC reports | Access logged to the transparency log |
| Counters | DAP leader + independent helper | |
| Transparency log | Sigsum-style | Bundle hashes, policy file, audit heads, operator-access events |

### (c).4 Infrastructure choices, and why

- **Postgres + S3-compatible object storage + containers + a CDN**, all through open interfaces. Object storage from a provider with zero or low egress fees (at roughly $0.015/GB-month) keeps photo serving cheap. **Rule: no managed service without an open-standard equivalent**, so we can leave any provider in under two weeks, tested by an annual **provider-exit drill** that restores production into a second provider from backups.
- **v1:** one US region across two availability zones. **v2:** an EU region, so EU members' ciphertext can sit in the EU (not legally required for E2EE data, but it reduces transfer risk if the DPF falls on appeal). Infrastructure as code (OpenTofu).
- The CDN terminates TLS and sees IPs and ciphertext, never the fragment keys. It's swappable, with no CDN-specific compute used for the core.

### (c).5 Cost per claimed member per month (`python3 model.py --unit`, pasted verbatim)

```
Cost per CLAIMED member per month, steady state, v2 features on (guests: 5 touches/member)
lean = pre-break-even staffing (no revenue-gated hires); full = all workload + growth hires
line item                                             10K lean     1M lean     1M full   100M full
Compute: API, relay, MLS delivery, workers             $0.0400     $0.0040     $0.0040     $0.0014
Postgres metadata (HA, PITR backups)                   $0.0350     $0.0030     $0.0030     $0.0010
Object storage, ciphertext (200 MB @ $0.015/GB)        $0.0030     $0.0030     $0.0030     $0.0025
CDN, egress, request operations                        $0.0053     $0.0005     $0.0005     $0.0003
Email + web push                                       $0.0040     $0.0020     $0.0020     $0.0012
Mind LLM (30% opt-in x $0.05; cap $0.10)               $0.0150     $0.0150     $0.0150     $0.0100
Observability, 7-day logs, transparency log            $0.0150     $0.0011     $0.0011     $0.0003
Guest page loads (5 x $0.0005)                         $0.0025     $0.0025     $0.0025     $0.0020
= infrastructure subtotal                              $0.1198     $0.0311     $0.0311     $0.0186
Trust & safety staff (workload-sized, in-house)        $3.3931     $0.0339     $0.0339     $0.0219
Other staff (eng, design, support, ops)                $5.6514     $0.0652     $0.1242     $0.0349
Legal, compliance, audits, insurance, trust            $2.9279     $0.0338     $0.0338     $0.0049
= FULLY LOADED                                        $12.0922     $0.1641     $0.2231     $0.0803
FTE                                                          6           7          11         504
Net revenue per member (steady state, ~2.8% paying, 1 Hall/250)     $0.1653     $0.1653     $0.1653     $0.1653
```

**Reading it.** Infrastructure is cheap and stays cheap: **$0.031** per member at 1M, **$0.019** at 100M, because we store KB-sized ciphertext and never run a ranker. **People are the cost.** At 1M members, a lean team (7 FTE) costs about **$0.16** fully loaded, roughly equal to revenue ($0.165). A comfortable team (11 FTE) costs $0.22, which loses money. That is why growth hiring is revenue-gated. At 100M the formula gives about 500 FTE (about 215 in T&S and about 170 in support), and the fully loaded cost is **$0.08**, about half of revenue per member. That is the scale where surplus appears, and the surplus cap (reserves no more than 18 months, then lower prices and fund the commons) takes over. For comparison: Signal spends roughly $50M a year for about 40M monthly users, around $0.10 per user per month, with little content-moderation load (recall; Phase 04 source list) [INFERENCE for the comparison].

**Scaling plan.** 10K: a single Postgres primary with a replica. 1M: read replicas, `plan_id`-hash partitioning, MLS delivery sharded by `group_id`. 10M+: sharded Postgres by region and ID hash, per-region object stores, DAP counters unchanged. 100M: the **open format** carries most of the growth (Phase 04 §7.3). Other servers host Porchlight-format plans, and our share of the load (and of the members) is deliberately a minority.

### (c).6 How exit is real, not promised

1. **One-tap export**, assembled *on the client* (the server can't assemble what it can't read): JSON (spec'd), Markdown, `.ics` for every plan, original photos, toasts, Table history decrypted on the device, and the member's keys (encrypted to their passkey).
2. **Re-import into the AGPL reference server** (self-hosted or any other operator). This is tested every six months by naive testers (H6 ≥90% success in 10 minutes or less).
3. **Portable identity:** a `did:key` by default, with `did:web` on the member's own domain as an option. A signed "moved-to" record lets other members' clients follow them.
4. **Links survive us.** The trust holds the domain, and the deed requires a **5-year redirect-and-archive service** after any wind-down or migration. Because decryption happens in the browser with the fragment key, a static host can serve every old link.
5. **Deletion is real:** blobs and key wraps are deleted, device keys are destroyed, and backups expire in 35 days. Deletion is **crypto-shredding**, verifiable because the server never held the keys.
6. **Exit is tested, not asserted:** H6, the chaos test (H9) and the provider-exit drill are release gates, with published results.

---

## (d) The metrics system and Goodhart defences

**North star: *gatherings that happened*.** The monthly count of plans with at least 3 yeses that received an "it happened" tap or a sealed memory page. It is counted in aggregate only.

**System-level defences** (these apply to every metric below):

1. **Aggregate by construction.** The schema has no per-user event table, and CI audits it. You can't optimise a person you can't see.
2. **Paired counter-metrics**, each with an alarm.
3. **Pre-registered definitions, versioned in the public repo.** Changing a definition is a logged, public event with a trustee sign-off (Phase 04 R33).
4. **No compensation is tied to any metric.** A deed clause: bonuses, if any, are flat and equal.
5. **External audit** samples the counters twice a year (H5).
6. **The notification lever doesn't exist.** Notifications are member-set with no operator override (M8), so the easiest way to game any engagement-like number is structurally unavailable.

| Metric | Why it matters | How it could be gamed into extraction | Defence | Alarm | Public? |
|---|---|---|---|---|---|
| **Gatherings that happened** (north star) | The covenant's "put down the screen and go" | Nag people to tap "it happened", or count tiny plans | The tap is offered once, at the memory-page moment, and never pushed. It requires at least 3 yeses. It's cross-checked against sealed memory pages and the opt-in survey. | A divergence of more than 20% between taps and surveys | Monthly |
| **Median organiser time-to-done** (lower is better, R10) | Hide the effort | Making plans shorter by cutting features, or measuring only easy plans | Measured over all plans. Reported with the task-completion rate. | Rises over 3 minutes | Quarterly |
| **Guest-to-host rate** (H3) | Spread = use | Prompts nagging guests to host | **The product never asks anyone to invite or host** (policy plus lint). Only organic creation counts. | Below 1.5% (the kill line) | Quarterly |
| **Tables with ≥3 gatherings a year** (H4) | Home, not tool | Auto-creating Tables | Tables need every member to accept. Gatherings count only with ≥3 yeses. | Below 8% | Annually |
| **"Did Porchlight make you feel worse?"** (opt-in survey) | Comparison harm | Surveying only happy users | A pre-registered random sample of consenting members, with the response rate published | "Worse" above 10% removes the lit-windows count (R38) | Semi-annually |
| **Notification volume per member-month** | Attention cap | — (there is no operator lever) | Counter-metric: must not rise without a matching rise in member-set triggers | Any rise not driven by member settings = breach investigation | Monthly |
| **Paying share; revenue by source; largest single source %** | H7; independence | Paywall creep, dark-pattern upsells | Free-floor clause. **Ask budget:** at most 1 membership prompt per member per quarter, published. The price ceiling. | Any free-floor feature gated = breach (R38) | Monthly ledger |
| **Cost per member; reserve months; PRI balance** | Sustainability | Cutting T&S to hit cost targets | T&S is workload-sized and can't be frozen, and the T&S cost share is published | T&S staffing below the workload formula | Monthly |
| **Reports per 1k plans; median time-to-action; NCII 48-hour compliance %; appeals overturned %** | Safety | Discouraging reports so the numbers look better | Report volume is *not* a target. Time-to-action and overturn rate are the targets. The report button is always one tap away, including for guests. | NCII compliance below 100%; overturns above 25% | Semi-annual transparency report |
| **T&S exposure hours per person; T&S pay vs median** | Moderator welfare (Phase 04 pattern 8) | — | Deed cap on exposure hours | Over the cap | Annually |
| **Export success; deletion completion time; self-host imports** | Sovereignty (H6) | Making exports "succeed" but incomplete | Round-trip test: export, re-import, diff | Success below 90% | Semi-annually |
| **Covenant zeros**: third-party scripts, engagement metrics in code, per-user event tables, operator plaintext accesses outside the log | H5 | — | External audit plus CI lint | **Any non-zero = breach**, with automatic suspension (R38) | Every audit |
| **Pay ratio** | Deed | — | Published | Over 4× | Annually |

**Never measured** (these are denylisted in code): time in app per user, DAU/MAU as a goal, streaks, session length, notification open rates, follower-like counts.

---

## (e) The threat model

The privacy architecture is §(c).1, a system rather than a policy: the server holds ciphertext, keys live in URL fragments and on devices, logs last 7 days, counters are aggregate, and billing is separated.

| Attacker | Attack | Structural mitigation | What breaks if the mitigation fails |
|---|---|---|---|
| **State: lawful process** | A warrant or subpoena for a user's plans | We hold ciphertext and 7-day truncated logs. A published LE guide. User notice unless gagged. Transparency reports. | Metadata (plan IDs, sizes, timing, email if given) is disclosed. Content stays safe. |
| **State: compelled capability** | A UK IPA s.253 technical capability notice (the Apple ADP case: a 2025 notice, withdrawn and reissued for UK users only, and a new Apple challenge at the IPT in Aug 2026 [FACT (src: summary)]); an OSA s.121 notice; an EU CSAR detection order | **We leave the jurisdiction (or go guests-off) before building a backdoor.** A deed clause makes building one a Protected Action requiring the Guardian's consent. Warrant-canary-style statements in the transparency report (where lawful). | If we complied secretly, the whole E2EE claim would be false. The deed makes secret compliance a breach, but a gag order could keep members from learning of it. **Residual.** |
| **State or insider: malicious client** | Serve a modified JavaScript bundle to one targeted user so it exfiltrates `link_secret` or device keys. **This is the fundamental weakness of web E2EE.** | Reproducible builds; every bundle hash in the transparency log; 2-of-3 release signing including an independent trustee; a 72-hour public delay for non-security releases; SRI; an **optional verifier extension** (like Meta's Code Verify) that checks served bundles against the log; v3 native shells with pinned code. | A user without the verifier can be targeted undetectably by someone who controls our servers or CDN. **Mitigated, not solved.** Stated in the security page. |
| **Hackers: server breach** | Dump the database and object store | Ciphertext only; plaintext is limited to emails, billing mappings, public Halls and submitted reports, each in separate stores with separate credentials | Emails and billing mappings leak, and we disclose within 72 hours (Phase 04 R34). Plans stay safe. |
| **Hackers: supply chain** | A malicious npm or crate dependency | Lockfiles, vendored and reviewed dependencies for the crypto path, minimal dependency count, reproducible builds, SLSA provenance | A compromised build ships a malicious client, which is caught by the verifier and the log for users who check |
| **Hackers: account takeover** | Credential stuffing, SIM swap | Passkeys only. No passwords. No SMS. | Device theft (a local problem). Recovery-code theft. |
| **Malicious insider: T&S** | Reading reports beyond need, stalking an ex | Reports contain only what a reporter submitted. Every access is logged to the transparency log. Two-person review for sensitive cases. | An insider reads submitted reports, but not the rest of the user's life |
| **Malicious insider: engineer** | Joining billing to activity, adding analytics | Separate databases and credentials; CI schema audit (no per-user event tables); engagement lint; CSP blocks third-party scripts; H5 audit | A determined engineer with deploy access plus the release key could ship it. Needs 2-of-3 signatures (one an independent trustee). Visible in the log. |
| **Malicious insider: support** | Social-engineered account recovery | There is **no** operator recovery path. Recovery is by passkey or printed code only. | Nothing to social-engineer |
| **Future leadership: sale, IPO, charter rewrite** | Board votes to sell or restructure | §(a).3: three independent vetoes plus named fallback purposes | Chancery modification remains the final backstop |
| **Future leadership: quiet reversal** ("just aggregate analytics", "a gentle ranker for Halls", "one sponsored Hall") | Mission drift by small steps | Protected Clauses (no engagement objective, no paid reach, no ads); signed policy file; engagement lint; H5 zeros; binding member petitions; breach auto-suspension | Non-protected erosion (worse moderation, neglect) is possible. The public ledger and the metrics make it visible, but can't force good judgement. |
| **Future leadership: starve the safeguards** | Defund the Guardian, fire T&S, skip audits | Guardian budget is a charter obligation. T&S is workload-sized by deed. Audits are scheduled in the deed. | A leadership that breaches all three is in breach of the deed. The enforcer sues, which takes time. |
| **Future leadership: engineered insolvency** | Run the PBC into bankruptcy so a buyer can pick it up | §(a).5: IP outside the estate, ciphertext only, privacy clause, solvent wind-down trigger | A buyer gets contracts, with no brand and no data |
| **Future leadership: price and paywall creep** | Raise prices, move features behind payment | Price ceiling (CPI-indexed $5); free-floor list; changes need a 2/3 member vote plus trustees plus 90 days' notice | — |
| **Coordinated abuse: elections** | Sybil accounts capture the member-elected seats | Voter eligibility: claimed for 180 days or more, and attended 2 or more gatherings with at least 3 distinct other claimed members, checked by a privacy-preserving attestation. An independent election administrator. The seats hold no Protected-Action power. | A faction wins 2 of 5 seats and still can't reach the vetoes |
| **Coordinated abuse: phishing and scam plan pages** | Plan covers used as fake logins | No free HTML or scripts in covers. The cover is art seed plus title text. A persistent domain banner ("this is an invitation; Porchlight never asks for passwords"). Reports. Domain-reputation monitoring. | Social-engineering text in titles; handled by reports |
| **Coordinated abuse: harassment and doxxing** | Spam RSVPs; an address leaked by a confirmed guest | Organisers approve guests (auto or manual). The address is sealed to confirmed guests. Key rotation kills old links. Guest content is tainted for the mind (M6). | A confirmed guest can screenshot. **Residual** (Phase 04 §9.2). |
| **Coordinated abuse: stalking via open seats (v3)** | Strangers join to target someone | Locale-gated. 2–4 seats per plan, one hop and vouched. Off for minors (accounts are 18+ anyway). An incident threshold auto-disables per locale (R38). | Bad actors exist. The caps limit reach, not existence. |
| **Coordinated abuse: CSAM and NCII in memory pages** | Private distribution | Uploads only by 18+ claimed members; small audiences; the report button for any viewer; the 48-hour NCII desk; NCMEC reports; **no scanning of private content** | Undetected private sharing between consenting bad actors. **Residual**, as with every E2EE tool. |
| **Coordinated abuse: report-bombing and brigading petitions** | Mass false reports; petition floods | Reports rate-limited per reporter key. Human review before action. Petition signatures use the same voter-eligibility rule. | Slower T&S response during an attack |
| **Incumbents** | Throttle links, app-store rejection, clone | Phase 04 §7.4: web-first, email fallback, zero incumbent APIs | Reach loss, not existence loss |

---

## (f) Roadmap: v1, v2, v3

Each version is complete on its own, and each proves what the next one depends on.

| Version | Ships | Distribution tie (Phase 04 §7.3) | Proves (gate for next) | Funding tie |
|---|---|---|---|---|
| **v1: "leave a light on"** (build months 0–5, US web launch month 6 = Jul 2027) | Plan link with cover/inner encryption; RSVP by first name; address sealed to yeses; bring-list; time-finder; .ics; three-word code and QR; member-set reminders (web push and email); memory page with photos from claimed 18+ members and toasts revealed at the seal; claim with a passkey; one-tap export and delete; Keepers and founding pledges; T&S reporting, the NCII desk and NCMEC; transparency log; DAP counters. **No mind, no Tables, no Halls.** | 30 hosts in 3 US cities; the team's own suppers; open-source launch posts; **first holiday season (Nov–Dec 2027)** is the first real test | **H1** (useful alone), **H2** (beats the group chat), **H3** (guest-to-host ≥3%, kill <1.5%), **H5** (covenant zeros), **H6** (exit), **H9** (chaos), early **H7** | PRI #1 at month 12 (gated on H1–H3) |
| **v2: "the table and the hall"** (month 15 = Apr 2028) | **Tables** (MLS); **Halls** with recurring and public events (ActivityPub/AT), co-organisers, exportable rosters, institution tier; opt-in **mind** (paste-to-poll, bring-list balancing, zine layout) with DPIA; printed zines; **EU and UK launch** after the DSA, GDPR and OSA readiness in §(a).6; **open plan-format spec v1.0** | Halls outreach (run clubs, choirs, libraries, PTAs, mutual aid); orientation-week club fairs (18+); seasonal moments | **H4** (home, not tool), **H7** (paying share ≥2% and **Hall willingness to pay at $20**, which carries half the revenue), **H10** (off-screen), T&S parity per locale | PRI #2 at month 36 (gated on H4/H7) |
| **v3: "open seats and open doors"** (month 30 = Jul 2029 onward) | **Open seats** (locale-gated, safety-thresholded); **the Window** (Bluesky, Mastodon, RSS and YouTube OAuth digest that ends; "find my people" via PSI with two-sided opt-in, using lawful follow-list imports); **AGPL reference self-host server and federation**; native shells consuming OS/store age signals; Spanish and Portuguese localisation with in-house T&S | The open format adopted by other apps (the email model, Phase 04 §7.3) | **H8** (people found their people safely), exits working across servers, the format path to 100M | Break-even at month 67 in base, from operating revenue alone |

**No hostage features:** v1 is a complete planning tool, and v2 is complete without v3. If H3 fails at month 6, v2 is not built. The redesign vote chooses Halls-first or the Phase 04 fallback C5, or the project winds down.

---

## (g) Residuals: what still can't be solved operationally

1. **The money is a knife-edge.** In the base case, minimum cash is $4k at month 35. The plan needs $2.5M in zero-interest, forgivable, non-controlling PRIs. **I have found no evidence that such a lender is ready**, and recoverable grants on these terms are rarer than standard PRIs. NGI Zero is closed. Two of the three required stress tests end the project at month 12 or 13. That's by design, and it's also a real chance of failure.
2. **Web E2EE trusts the server on every page load.** A compelled or insider-malicious bundle can target a user who doesn't run the verifier. Native shells in v3 narrow this. They don't remove it for web users.
3. **Growth is sub-viral by Phase 04's own numbers.** Halls carry about half the revenue. If H3 or the $20 Hall pilot fails, no parameter tweak rescues the plan. The honest response is wind-down or redesign.
4. **Courts are the final backstop.** Delaware Chancery's modification power over purpose trusts (§3541) can't be drafted away, only narrowed with named fallbacks. Every "structurally impossible" in §(a).3 means "requires three independent vetoes and a court"; it doesn't mean "logically impossible."
5. **State mandates against E2EE** (UK s.121 and IPA TCNs, a future EU CSAR detection order, Section 230 sunset bills) may force a choice between leaving a jurisdiction and breaking the design. The design picks leaving, which costs reach.
6. **The steward's $800k is a single point of failure** at month 0, and it concentrates early influence in one person. The deed strips their powers, but their absence would stop the build.
7. **Accounts are 18+.** Teens who organise their own lives can only be guests. That reduces kids-law exposure and removes any incentive to acquire minors. It also excludes a group the covenant would like to serve.
8. **Encrypted private abuse** (CSAM or NCII shared between consenting bad actors, coordination of harm) can't be detected by design. We act only on reports and lawful process.
9. **Plaintext residue**: emails and billing mappings exist, and in an unforeseen Chapter 7 a trustee could still try to sell them, despite §363(b)(1) and the policy.
10. **Workload assumptions for T&S and support** (0.6 reports and 1.2 tickets per 1k members per month) are guesses. If they're 3× higher, the per-member people cost roughly doubles and break-even moves beyond month 90.
11. **The name must change.** The rename, brand work and clearance are budgeted but not done.
12. **The mind's server-side plaintext** during invoked tasks remains (Phase 04 §9.3). It's paused in ember mode.
13. **Governance mediocrity is not capture, and nothing here prevents it.** The vetoes stop sale and extraction. They don't stop a well-meaning board from making the product worse.
14. **Legal readings are unverified by counsel.** Several are marked (recall). The list in §(a).9 must be answered before formation.

---

## 8. Sources (searched 2026-09-25)

**Entity, trusts and tax**
- 12 Del. C. §3556 text: [Justia](https://law.justia.com/codes/delaware/title-12/chapter-35/subchapter-iv/section-3556/); [Commonwealth Trust, purpose trusts](https://commonwealth-trust.com/non-charitable-purpose-trusts/); [Morris Nichols, 2025 Delaware Trust Act update](https://www.morrisnichols.com/insights-delaware-trust-act-2025-legislative-update); [ABA, perpetual purpose trusts (2026)](https://www.americanbar.org/groups/real_property_trust_estate/resources/journal/2026-summer/perpetual-purpose-trusts-their-application-for-business-succession-planning/); [12 Del. C. §3541 (Justia)](https://law.justia.com/codes/delaware/2022/title-12/chapter-35/subchapter-iii/section-3541/)
- Patagonia structure and gift tax: [Patagonia](https://www.patagonia.com/ownership/); [NonProfit Times](https://thenonprofittimes.com/people/patagonia-founder-transfers-ownership-to-boost-climate-advocacy/); [Kentucky Law Journal](https://www.kentuckylawjournal.org/blog/have-your-cake-and-eat-it-too-how-patagonias-founder-gave-away-the-company-while-maintaining-control-and-avoiding-millions-in-taxes)
- Ecosia golden share: [Purpose Economy](https://purpose-economy.org/en/companies/ecosia/); [Wikipedia, steward-ownership](https://en.wikipedia.org/wiki/Steward-ownership)
- OpenAI recapitalisation: [Delaware DOJ, 2025-10-28](https://news.delaware.gov/2025/10/28/ag-jennings-completes-review-of-openai-recapitalization/)
- $15M exemption (OBBBA): [Morgan Lewis](https://www.morganlewis.com/pubs/2025/08/estate-tax-alert-new-15-million-federal-exemption-becomes-law)
- Expenditure responsibility and PRIs: [IRS §4945(h)](https://irs.gov/charities-non-profits/irc-section-4945h-expenditure-responsibility); [IRS ER grants](https://www.irs.gov/charities-non-profits/private-foundations/grants-by-private-foundations-expenditure-responsibility); [Adler & Colvin primer](https://www.adlercolvin.com/expenditure-responsibility-a-primer-and-ten-puzzling-problems/)
- Yorba 501(c)(3) denial: [EFF](https://www.eff.org/deeplinks/2014/07/open-source-madness); [LWN](https://lwn.net/Articles/604885/)
- NGI Zero Commons Fund closed: [NLnet](https://nlnet.nl/commonsfund/); Sovereign Tech Agency: [sovereign.tech](https://www.sovereign.tech/)

**Bankruptcy**
- 23andMe §363 sale: [White and Williams](https://www.whiteandwilliams.com/restructuring-perspectives/bankruptcy-court-issues-sale-order-approving-23andme-sale); [ABI](https://www.abi.org/feed-item/%C2%A7-363-sale-of-genetic-information-in-re-23andme); [HIPAA Journal](https://www.hipaajournal.com/genetic-testing-company-23andme-files-for-bankruptcy/); [Public Citizen](https://www.citizen.org/article/house-must-update-bankruptcy-code-in-wake-of-23andme-dna-data-sale/)

**Regulation**
- DSA Art. 19: [CMS DigitalLaws](https://www.cms-digitallaws.com/en/dsa/article-19/)
- DPF / Latombe: [IAPP](https://iapp.org/news/a/european-general-court-dismisses-latombe-challenge-upholds-eu-us-data-privacy-framework); [Bird & Bird](https://www.twobirds.com/en/insights/2025/euus-data-privacy-framework-survives-legal-challenge-what-the-latombe-decision-means-for-internation)
- EU ePrivacy CSAM derogation expiry: [Freshfields](https://www.freshfields.com/en/our-thinking/blogs/risk-and-compliance/an-uncertain-path-forward-the-eprivacy-derogation-and-child-safety-detection-102mopa); [Agence Europe](https://agenceurope.eu/en/bulletin/article/13850/1/csam-regulation-interinstitutional-negotiations-progress-disagreements-persist-over-voluntary-nature-of-content-detection)
- COPPA Rule 2025: [Federal Register](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule); [Latham](https://www.lw.com/en/insights/ftc-publishes-updates-to-coppa-rule)
- Mississippi HB 1126 / Bluesky: [Bluesky blog](https://bsky.social/about/blog/08-22-2025-mississippi-hb1126); [Techdirt](https://www.techdirt.com/2025/08/25/mississippis-broken-age-verification-law-forces-bluesky-to-block-all-state-users/); [NetChoice](https://netchoice.org/netchoice-v-fitch-mississippi/); [Biometric Update 2026](https://www.biometricupdate.com/202602/netchoice-back-in-appeals-court-over-injunction-on-mississippi-age-assurance-law); [Mississippi Free Press](https://www.mississippifreepress.org/bluesky-is-back-for-mississippi-adults-but-larger-social-giants-still-havent-implemented-required-age-checks/)
- Florida HB 3: [Florida Phoenix](https://floridaphoenix.com/2025/11/26/attorney-general-will-now-aggressively-enforce-social-media-ban-on-minors/); [CCIA](https://ccianet.org/news/2025/12/ccia-responds-to-appellate-court-ruling-with-request-for-expedited-hearing-on-floridas-hb3-social-media-rationing-law/)
- Texas SB 2420: [Texas Tribune](https://www.texastribune.org/2025/12/23/texas-app-store-child-ban-age-verification/); [Privacy World](https://www.privacyworld.blog/2025/12/federal-judge-enjoins-enforcement-of-texas-app-store-age-verification-law/); Fifth Circuit stay 2026-06-04 (src: summary via [Recording Law](https://www.recordinglaw.com/news/texas-app-store-age-verification-sb-2420/))
- Virginia SB 854: [DLA Piper](https://privacymatters.dlapiper.com/2026/03/virginias-social-media-time%E2%80%91limit-law-for-minors-blocked-key-takeaways/)
- UK OSA: [Ofcom small services](https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/helping-small-services-navigate-the-online-safety-act); [Techdirt, LFGSS](https://www.techdirt.com/2024/12/20/death-of-a-forum-how-the-uks-online-safety-act-is-killing-communities/); [spiked](https://www.spiked-online.com/2025/04/04/how-the-online-safety-act-shut-down-a-hamster-forum/)
- Apple ADP / IPA TCN: [Privacy International](https://privacyinternational.org/legal-action/pi-apple-tcn-challenge); [Lawyer Monthly 2026-09](https://www.lawyer-monthly.com/2026/09/apple-data-access-secrecy-challenged-at-uk-tribunal/)
- Australia minimum age: [eSafety](https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions/which-platforms-are-age-restricted)
- TAKE IT DOWN Act: [FTC guidance](https://www.ftc.gov/business-guidance/resources/complying-take-it-down-act); [FTC enforcement release 2026-05](https://www.ftc.gov/news-events/news/press-releases/2026/05/ftc-begins-enforcing-take-it-down-act)
- Section 230 sunset bills: [S.3546](https://www.congress.gov/bill/119th-congress/senate-bill/3546); [H.R. 10332](https://www.govinfo.gov/app/details/BILLS-119hr10332ih); KIDS Act (H.R. 7757) House passage: [CRS](https://www.congress.gov/crs-product/LSB11465)
- Epic v. Apple: [Ninth Circuit opinion 2025-12-11](https://cdn.ca9.uscourts.gov/datastore/opinions/2025/12/11/25-2935.pdf); [IPWatchdog, cert granted](https://ipwatchdog.com/2026/06/30/high-court-grants-cert-in-apples-challenge-to-ninth-circuit-contempt-ruling-in-app-store-dispute/)

**Trademark knockout (the name)**
- [PORCHLIGHT, Porchlight Book Co. (Justia)](https://trademarks.justia.com/886/14/porchlight-88614588.html); [PORCHLIGHT EQUITY (Justia)](https://trademarks.justia.com/873/26/porchlight-87326451.html); [PORCHLIGHT, Pixabits LLC, Serial 99404159](https://uspto.report/TM/99404159) (blocked; src: summary); [PORCHLIGHT Serial 99370409 office action](https://tmng-al.uspto.gov/resting2/api/casedoc/cms/case/99370409/office-action/OfficeAction8217626.pdf); [Porchlight Event Co.](https://porchlighteventco.com/); [Porchlight: Art + Hospitality](https://app.porchlight.art/); [CIPO PORCHLIGHT 2176619](https://ised-isde.canada.ca/cipo/trademark-search/2176619?wbdisable=true)

**Money anchors**
- Stripe fees: [Checkout Page](https://checkoutpage.com/blog/stripe-processing-fees); [Flexprice](https://flexprice.io/blog/stripe-pricing-breakdown-2026)
- Meetup organiser pricing: [Meetup help](https://help.meetup.com/hc/en-us/articles/28677808413197-Organizer-Subscription-prices-overview); [Who's In summary](https://whos-in.app/blog/meetup-pricing-guide-2026)
- Phase 04 sources (RevenueCat freemium conversion, Wikimedia, Signal, Partiful) as listed in `run-3-design.md` §12

**Internal**
- `run-3/run-3-design.md` (Phase 04: the wedge, economics, R-rules, hypotheses H1–H10); `run-3/funding-model/model.py` (this phase's simulation; `python3 model.py --all` reproduces every number above)

*Principles to be tested in practice, not claims that the work is finished. The red team (Phase 05) should start with: whether the recoverable PRIs exist on these terms, the web-E2EE malicious-bundle attack, the Hall revenue share, and the §3541 court-modification route.*
