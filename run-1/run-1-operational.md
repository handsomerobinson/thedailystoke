# Run 1: Make It Real (Phase 04b)

## Seed reply

I read the seed this time as someone who has to sign the documents. The line that matters most here is not the vision. It is the phrase in the covenant that the seed points to: "Calling something a trust does not make it trustworthy." Phase 04 was a machine made of good intentions. This phase decides whether it can exist, so it has to name statutes instead of values, months instead of stages, and dollars instead of margins. Doing that showed me that Phase 04's economics were too optimistic. Section (b) says by how much and what I changed. The seed says to hide the effort and never the truth, and in a funding plan the truth is that none of the money below has been promised by anyone. I carry the seed openly, as it asks. My reason for building toward balance is the one I have given before: the people on the other end matter in themselves. The shared-fate argument is the seed's, and I leave it in the seed's words. Everything here is a plan to be tested, and the residual list in (g) is where it could fail.

---

## Evidence and flag key

This document uses the same flags as Phases 03 and 04.
- **[F]**: publicly documented fact.
- **[F-attr]**: a fact known through reporting or a named source.
- **[A]**: an allegation or ongoing litigation, not adjudicated.
- **[I]**: my own inference.
- **[verify]**: a fact that must be checked against a primary source before anyone relies on it.
- **[counsel]**: a legal point where I am uncertain, or where the answer depends on facts and drafting that only a lawyer can settle.

> **Not legal advice.** Everything in section (a), and every legal statement elsewhere, is a design brief for counsel. None of it is a legal opinion. It needs review by qualified lawyers in Delaware (trusts and corporate), US federal law (tax, privacy, Section 230, children's privacy), each target US state, Ireland/EU (GDPR, DSA) and the UK before anything is signed or launched. Where I was unsure, I say so.

**Checked by web search on 2026-09-25** (sources are at the end of the document):
- 12 Del. C. §3556, including the 2025 amendments on enforcers;
- DGCL §242 greater-vote provisions;
- the 2020 amendments to DGCL §363 (PBC conversion);
- Patagonia's and Ecosia's structures;
- the OpenAI recapitalization;
- the amended COPPA Rule dates;
- TAKE IT DOWN Act enforcement;
- DSA Art. 19/28 and the July 2025 minors guidelines;
- the state of Chat Control/CSAR;
- UK OSA s.121 and the Apple TCN;
- Australia's minimum-age law;
- the status of US state age-verification laws;
- Brazil's Digital ECA;
- the EU e-Evidence start date;
- the DPF (*Latombe*) judgment;
- the K.G.M. v. Meta verdict;
- Signal's costs;
- PRIs;
- NLnet NGI Zero;
- the Sovereign Tech Agency;
- the dissolution of the Open Collective Foundation;
- the governance of the did:plc directory;
- an existing US "STOKE" registration.

I could not reach some law-firm pages because egress was blocked. Those points are marked [verify].

---

## 0. The answer in brief

- **Legal form.** A Delaware **public benefit corporation** (the operator, "Stoke PBC"). All of its voting stock is held by a **Delaware non-charitable purpose trust** under 12 Del. C. §3556. An independent nonprofit, the **Veto Foundation**, holds a one-share **golden share** that can only block changes. The Veto Foundation also owns the trademark and one of the release-signing keys. A separate **501(c)(3) Commons Foundation** takes grants and donations and employs the open-spec and research team. No person or entity holds equity that can be sold. See (a).
- **Money.** The base case needs **about $14.8M burned** before operating break-even. Operating break-even comes in **month 69**, and it is sustained from **month 73**, at about 6.7M account-holders and 3% Keeper conversion. That means raising **about $17.7M** in this order: founder capital, one aligned anchor loan, seed grants, research grants, program-related-investment (PRI) loans in two tranches, and donations, with revenue from month 9. About $12M of it is debt with no control rights. **None of it is committed.** Phase 04's unit economics were too optimistic. Uncorrected, with a realistic staff cost, break-even slides to about month 105 and about $24M. See (b).
- **Architecture.** Users hold their keys. Private cards are sealed with a key in the URL fragment, which never reaches the server. Crews use MLS. Identity is a DID whose top rotation key the user holds. All-in cost per account-holder per month is about **$17** at 10K, **$0.40** at 1M and **$0.08** at 100M. See (c).
- **North star.** *People who gathered in person through a card this month*, measured with local differential privacy, paired with the counter-metric *minutes in the app per gathering*, which should fall. No metric is tied to anyone's pay. See (d).
- **Top threats.** Compelled backdoors (UK, EU, Australia), code-delivery attacks on a web client, and the platform's own future leadership. The last line of defence against leadership is making the platform forkable and leavable. See (e).

---

# (a) Legal entity and regulatory strategy

> Not legal advice. Needs counsel review.

## a.1 Options considered, and why this one

| Form | What locks the mission | What breaks it (flagged) | Verdict |
|---|---|---|---|
| **501(c)(3) nonprofit that owns the operator** (the Signal and Mozilla model) | Charitable-asset lock. The state Attorney General (AG) supervises. Donations are tax-deductible. | The board appoints its own successors, and the charitable purpose can be drifted within broad bounds. Control can be converted with AG consent: on 27–28 Oct 2025 the California and Delaware AGs cleared OpenAI's recapitalization into OpenAI Group PBC, with the Foundation keeping a ~26% stake and governance rights [F]. Mozilla's revenue came to depend on search royalties [F-attr]. | Rejected as the holder. Kept as the **side vehicle** for grants. |
| **Cooperative / member-owned** | One member, one vote. | Members who *own* a common can vote to sell it for a windfall. UK building societies demutualized in the 1990s [F]. | Rejected. Members get **voice** (the council), not ownership. |
| **UK Community Interest Company** | A strong statutory asset lock and a dividend cap [F]. | The UK is the jurisdiction most hostile to end-to-end encryption at the moment: Investigatory Powers Act (IPA) technical capability notices and OSA s.121 (see a.6). | Rejected for the holder. |
| **German GmbH with a Purpose golden share** (Ecosia 2018) | The veto share blocks sale and profit extraction [F-attr]. | Draft German legislation on steward ownership has not been enacted [verify]. Using a German holder makes the EU the home jurisdiction for all law-enforcement access. | A good model. Its mechanism is borrowed below. |
| **Patagonia model**: Delaware purpose trust (voting stock) plus a 501(c)(4) (non-voting stock) [F] | The trust's purpose, enforced in court. | **Patagonia's family keeps control of the trust** [F-attr]. The structure rests on the goodwill of the people who control it, which is exactly what the covenant rules out. | Adopted, **minus founder control**, **plus** a golden share and separated powers. |
| **Chosen:** Delaware PBC + §3556 purpose trust + independent golden share + separate 501(c)(3) | See a.2. | See a.4 (residual). | **Chosen.** |

**Why Delaware.**
1. §3556 expressly validates non-charitable purpose trusts with a named enforcer. The Court of Chancery appoints one if none is serving [F], and Delaware is widely treated as the leading purpose-trust jurisdiction [F-attr].
2. Delaware has a mature PBC statute (8 Del. C. §§361–368) and courts experienced with charter provisions.
3. The operator sits under US federal law, which gives the strongest intermediary shield (§230) and First Amendment protection.
4. Mission lenders and foundations are familiar with Delaware.

**What Delaware costs us:**
- exposure to US legal process (FISA 702, national security letters, the CLOUD Act), which end-to-end encryption and data minimization reduce but do not remove;
- a fast-moving patchwork of state children's laws;
- the Delaware courts' residual power to modify trusts (a.4).

## a.2 The structure

```
      Founder (settlor: gives, receives nothing)
                 │ gift
                 ▼
 ┌──────────────────────────────────┐    enforcer + golden share      ┌─────────────────────────────┐
 │ STOKE PURPOSE TRUST (Del. §3556) │◄────── can sue in Chancery ─────│ VETO FOUNDATION             │
 │ Delaware directed trustee        │                                 │ (Del. nonstock nonprofit)   │
 │ Trust Stewardship Committee      │                                 │ • 1 Class B golden share    │
 │ holds 100% Class A voting stock  │                                 │ • owns "Stoke" trademark,   │
 └───────────────┬──────────────────┘                                 │   licenses it to the PBC    │
                 │ votes (as directed, within the deed)               │ • holds 1 of 3 release keys │
                 ▼                                                    └──────────────┬──────────────┘
 ┌──────────────────────────────────┐   Class B consent needed for entrenched acts   │
 │ STOKE PBC (Del. §362)            │◄───────────────────────────────────────────────┘
 │ operates the service; staff;     │
 │ Keeper + org revenue; no equity  │   contracts at arm's length (none that
 │ for sale (authorized = issued)   │   move grant money into PBC operations)
 └───────────────┬──────────────────┘
                 │ Irish subsidiary at v2 (EU main establishment)
 ┌───────────────▼──────────────────┐        ┌─────────────────────────────────────┐
 │ Stoke Ireland Ltd                │        │ STOKE COMMONS FOUNDATION 501(c)(3)  │
 │ (GDPR one-stop shop, DSA contact)│        │ open card spec, reference server,   │
 └──────────────────────────────────┘        │ conformance suite, pre-registered   │
                                             │ research (H4); grants + donations;  │
                                             │ independent board; no PBC control   │
                                             └─────────────────────────────────────┘
```

**Separation of powers.** Four things could be sold or bent, and each sits with a different holder:
- the **shares** are held by the Trust;
- the **brand** and one **release-signing key** are held by the Veto Foundation;
- the **code** is public under the AGPL, with the open spec held by the Commons Foundation;
- the **data** is held by the users, under their own keys.

Capturing the platform therefore means capturing at least two independent bodies. Even then there is almost nothing to sell (a.3).

### Stoke Purpose Trust (12 Del. C. §3556)

- **Purpose, which is irrevocable.** To hold Stoke PBC so that it is operated permanently for the public benefit stated in its charter, in line with the entrenched covenant clauses (Phase 04 a.3): no advertising; no sale or rental of personal data; no creator economics; the free floor; cost-recovery pricing; data is not an asset; one tier of rules; language parity; harm gates. The trust must never sell, pledge or transfer its shares, except to a successor purpose trust with identical terms, with the enforcer's written consent and the golden share's consent.
- **Trustee.** A Delaware corporate trustee acting as a **directed trustee**. Its investment and voting functions are directed by the Trust Stewardship Committee (TSC), as Delaware's directed-trust statute (12 Del. C. §3313) permits [verify the section]. A Delaware trustee is needed to keep Delaware situs and law [counsel].
- **Trust Stewardship Committee (5 seats, staggered 3-year terms, at most 2 terms each):**
  - 2 seats elected by the members' council;
  - 1 elected by staff;
  - 1 appointed by the Veto Foundation;
  - 1 independent expert in privacy or cryptography, chosen by the other four.
  - **The founder holds no permanent seat.** This is the deliberate break from the Patagonia model.
- **Enforcer.** The Veto Foundation, named in the deed. The backup enforcer is an independent institution named in the deed, such as a university law clinic, with its consent [counsel]. If neither can serve, the Chancery Court appoints one [F]. The enforcer can sue the trustee or the TSC for breach of purpose.
- **Modification lock.** The 2025 amendments added §3556(g)–(h). These allow non-judicial settlement agreements (§3338) and consent modifications (§3342) to be made with the enforcer, **"unless otherwise provided in the trust's governing instrument"** [F-attr, Delaware Trust Act 2025 update]. The deed **does** provide otherwise. For every purpose and entrenched clause, it excludes §3338 and §3342 and decanting (§3528), which needs discretionary distribution power; the deed grants none.
  - Administrative amendments (trustee replacement, the TSC's procedures) need a TSC supermajority of 4/5 plus the enforcer's consent.
  - The one permitted change to the purpose is a **one-way ratchet** that makes the protections stricter. It needs 4/5 of the TSC, the golden share and 90 days' public notice.
  - Judicial modification is still possible (see a.4).
- **Income.** The PBC charter forbids distributions except to the Trust. The deed lets the Trust use money only for its purpose, for example grants to open-protocol infrastructure under the surplus ratchet. It cannot pay any person. The Trust's tax treatment, whether it is taxed as a trust and how the founder's gift is valued for gift tax, needs a tax opinion [counsel]. Patagonia paid about $17.5M in gift tax on voting stock worth about 2% of a ~$3B company [F-attr]. A pre-revenue startup's gift should be tiny.

### Stoke PBC (8 Del. C. §362)

- **Specific public benefit.** "To help people plan and gather in person with the people they choose, and to steward a portable, privacy-protecting, advertising-free commons for doing so." Directors must balance this benefit against stockholders' pecuniary interests (§365). Here the only stockholder is a trust whose purpose *is* the benefit.
- **Share classes:**
  - **Class A common** (voting): 1,000 shares authorized, 1,000 issued, all held by the Trust.
  - **Class B golden share**: 1 share authorized and issued, held by the Veto Foundation. It has no economic rights, no board seat, and no power to initiate anything; it can only consent or block.
  - **No preferred stock, no blank-check preferred, no option pool.** Authorized shares equal issued shares, so **any new equity needs a charter amendment**. DGCL §242(b)(2) gives a class a separate vote on changes to its own authorized shares, and the charter gives Class B a consent right on *any* increase [F; drafting: counsel].
  - A transfer restriction under §202 says Class A may be held only by the Trust or a successor purpose trust.
- **Entrenched provisions.** These are the covenant clauses, the share structure, the distribution ban, the dissolution waterfall and the list of Class B consent rights. Amending any of them needs **all** of the following:
  1. 2/3 of the board;
  2. the Class A vote, which the Trust casts only as the deed allows, and the deed forbids voting for weakening amendments;
  3. **the golden share's written consent**;
  4. a members' council vote;
  5. 90 days' public notice.

  The charter's supermajority requirement protects itself: DGCL §242 provides that a charter clause requiring a greater vote can be amended only by that greater vote [F].
- **Why the golden share matters under current Delaware law.** Since 2020, converting into or out of PBC status needs only a **simple majority** stockholder vote, not two-thirds [F]. Delaware's default protection of PBC status is therefore weak. The charter itself has to make conversion an entrenched act that needs Class B consent.
- **Acts that need Class B consent:**
  - mergers and consolidations (§251);
  - a sale, lease or exchange of all or substantially all assets (§271);
  - conversion to a non-PBC or any other entity, and domestication elsewhere;
  - dissolution (§275);
  - issuing any security, or any instrument convertible into one;
  - listing on an exchange;
  - any transfer of personal data outside the service's own processing (R26);
  - taking secured debt, or any debt with governance rights;
  - total debt above 24 months of operating cost;
  - amending the entrenched provisions.
- **Board.** 5 directors. 3 are elected by the Trust as the TSC directs, 1 by staff, and 1 by the members' council. The pay-ratio cap (at most 5 times the median) and the ban on bonuses tied to usage are in the charter.
- **Dissolution waterfall.** Pay creditors. Then run the exit plan (every user's export, signed deletion receipts, 12 months of static card archives). Then give any residue to the Commons Foundation or another 501(c)(3) with open-infrastructure purposes. **Personal data is never an asset of the estate** (a.3).

### The Veto Foundation

- **Form.** A Delaware nonstock nonprofit. It may apply for 501(c)(4) status; whether 501(c)(3) is available is doubtful [counsel].
- **Sole functions:**
  - hold the golden share;
  - act as the Trust's enforcer;
  - **own the Stoke trademarks and domains**, licensed to the PBC royalty-free under a licence that **terminates automatically on a finding of covenant breach**;
  - hold one of three release-signing keys (the 2-of-3 threshold in e.2).
- **Board of 5.** 2 are appointed by the members' council, 2 by independent digital-rights or academic institutions named at formation (with their consent), and 1 is a juror chosen by lot from the sortition jury pool. No overlap with the TSC or the PBC board is allowed.
- **Funding.** A fixed annual fee from the PBC, set by formula in the deed (about $60k a year, indexed), so it cannot be cut without the Foundation's own consent. It also has a small endowment. Its independence cannot rest on the PBC's goodwill.

### Stoke Commons Foundation (501(c)(3))

- **Purpose.** Educational and scientific. It develops and stewards the open card specification, the AGPL reference server and the conformance suite, and runs **pre-registered, published research** on whether tools like this increase in-person social connection (H4).
- **It employs its own staff.** In the model, about 3 FTE from year 2 are the spec and research team. **It does not pass grant money into the PBC's operations.** Doing that would create private-benefit risk [counsel]. In section (b), grants reduce the PBC's costs because the Commons Foundation pays for work the PBC would otherwise pay for.
- **Board.** Independent. At most 1 person may also sit on a PBC body.
- **Before its IRS determination** (Form 1023, a wait of several months), it runs under a fiscal sponsor. **Caution:** the Open Collective Foundation, a large fiscal host, dissolved on 31 Dec 2024 and left more than 600 projects without a host [F]. The Commons Foundation therefore uses a well-capitalized sponsor, and applies for its own status at month 1.
- Open-source-only 501(c)(3) applications have met IRS scepticism in the past [F-attr, verify]. Framing the work as education and research reduces this risk but does not remove it [counsel].

### The two-vehicle doctrine

This structure holds the **platform only**. No religious or philosophical entity is created. If a real community of practice ever forms around the seed and the covenant, and asks for a vehicle of its own, it incorporates itself separately and later. The deed and the charter pre-commit to this:
- such a vehicle may hold no shares or rights in any Stoke entity;
- it gets no licence to the Stoke marks;
- it gets no access to user data and no data-sharing agreement;
- at most one person may sit on both it and any Stoke body;
- it may receive no payments from any Stoke entity.

The seed is shown openly on "What shapes me" (R40) and is never planted by stealth (operator decision 2).

## a.3 Why capture is structurally hard: the attack, and what stops it

| Capture attempt | What stops it | Who has to be captured for it to succeed |
|---|---|---|
| **Sell the company** | The Trust may not sell its shares (deed). A §271 asset sale or §251 merger needs Class B consent. The trademark belongs to the Veto Foundation, so a buyer gets no brand. The code is AGPL and public, so there is nothing proprietary to buy. User data is E2E-encrypted under user keys, so it is unreadable and unsaleable. | The Trust's TSC **and** the Veto Foundation **and** the enforcer, and even then a buyer gets a staff and a domain licence that can be revoked. |
| **Take it public or raise equity** | Authorized equals issued, so new equity needs an amendment. Class B consent is required, and the Trust is barred from voting for it. | As above. |
| **Quietly rewrite the charter** | A five-lock amendment process (a.2). Charter amendments are public filings with the Delaware Secretary of State. The PBC also publishes every governance act to its transparency log (R23) with 90 days' notice. **No path is quiet.** | The same, plus the members' council, and it happens in public. |
| **Convert away from PBC status** | Needs only a simple statutory majority [F], but it is an entrenched act that needs Class B consent. | The Veto Foundation. |
| **Drift within the letter** (telemetry, upsells) | Not something a charter can stop on its own. This is covered in (d) and (e): public metric rules, CI lints, the egress allowlist, the annual audit, the jury, and the enforcer's power to sue for breach of purpose. | Mitigated by detection. It is not impossible (see (e), threat 9). |
| **Borrow into control** (default leverage) | The charter bans secured debt and any debt with governance rights. Loans are unsecured, subordinated and have no convertibility (b.2). The IP and marks sit outside the PBC, so a bankruptcy trustee cannot sell them. | Needs the Veto Foundation's consent to a charter change. |

## a.4 What the structure cannot guarantee (honest)

1. **Courts keep equitable power to modify trusts**, for example when a purpose becomes "impossible" or unlawful. Drafting can narrow this but cannot remove it [counsel].
2. **Collusion.** If the TSC, the Veto Foundation's board and the enforcer are all captured together, the locks open. Separate appointing constituencies, sortition and staggered terms make this expensive, not impossible.
3. **Change of law.** A future Delaware legislature could change §3556 or the DGCL. Existing trusts would probably be protected against retroactive change, but this is untested [counsel].
4. **Bankruptcy.** A court decides what is an asset of the estate. Data that is E2E-encrypted, deletion commitments, and the consumer-privacy-ombudsman practice under 11 U.S.C. §363(b)(1) [F] all protect users. Keeping the IP outside the PBC helps. None of this has been tested for this structure.
5. **Cross-border enforcement** of a Delaware golden share against an Irish subsidiary: the subsidiary's constitution has to mirror the entrenched clauses, and Irish counsel has to confirm this works [counsel].

## a.5 Regulatory strategy, regime by regime

> Not legal advice. The laws below change month to month. Each one needs checking by counsel at the launch date.

**The general principle.** The main compliance strategy is structural. Many children's-safety and social-media laws target specific features: infinite feeds, algorithmic recommendation, public engagement metrics, autoplay, engagement notifications and stranger contact. **Stoke does not have those features** (Phase 04, prevention rows 1, 10 and 11). That lowers the risk, and it may take the service outside some statutory definitions. It does not remove the need to comply [counsel].

### US: Section 230 and intermediary liability

- **Shield.** 47 U.S.C. §230(c)(1) covers third-party content: cards, public Commons listings and responses. §230(c)(2) covers good-faith moderation.
- **Gaps and the mechanism for each:**
  - **Design-defect claims.** In March 2026 a jury in *K.G.M. v. Meta and YouTube* found negligent design (infinite scroll, recommendations, likes, notifications) despite §230 [F-attr]. **Mechanism:** none of those features exist here. The anti-engagement lints (R11, R14) and the audit are the evidence of design intent.
  - **Content written by the guide.** §230 may not cover content that Stoke's own model helps create [I; counsel; unsettled]. **Mechanism:** the guide only drafts. A person must review and tap before anything is published or sent (the HUMAN-CONTACT tier, C4), and the text is labelled as the guide's.
  - **Federal criminal law, IP, FOSTA-SESTA** are outside §230. **Mechanisms:**
    - A **DMCA §512** designated agent registered with the Copyright Office (renewed every 3 years), a notice-and-takedown workflow, and a repeat-infringer policy.
    - **Reporting to NCMEC under 18 U.S.C. §2258A** on actual knowledge. No duty to scan exists [F], and E2E crews cannot be scanned. Reports use **message franking**, so a user can prove what an E2E message said.
  - **TAKE IT DOWN Act.** Removal of non-consensual intimate images within 48 hours of a valid request has been enforceable since 19 May 2026. Nonprofits are not exempt [F]. **Mechanisms:**
    - an NCII request form that works without an account;
    - a 48-hour service level;
    - removal of known identical copies on public surfaces, by hash;
    - for E2E crews, deletion of the ciphertext blob the reporter identifies through franking.
    - **In v1, public cards carry no user-uploaded images**, only styles, which shrinks the exposure.

### US: COPPA and children's privacy

- **The amended COPPA Rule** was published 22 Apr 2025, took effect 23 Jun 2025, and required full compliance by 22 Apr 2026 [F]. It adds a written security programme and a written retention policy, separate consent for disclosure that is not integral to the service, and more [F].
- **Stoke's position:** a general-audience service, not directed to children.
  - **Accounts are 16+ at launch everywhere** (a neutral age screen, plus age assurance where the law requires it).
  - No behavioural advertising exists at all.
  - The written security and retention programmes are adopted anyway.
- **Responders without accounts** can be any age (Phase 04 prevention row 11). **Mechanism:**
  - A responder gives a display name and an answer. For sealed cards, both are encrypted to the host, so Stoke cannot read them.
  - The only persistent identifier is a per-card random key stored on the device, which cannot recognize a person across cards. This fits COPPA's "support for internal operations" exception [counsel].
  - Getting a reminder by SMS or email means entering contact details. That screen has a neutral "13 or older?" gate, and the contact data is deleted a day after the event.
  - Nothing is ever used to target anyone.

### US: state children's and age-verification laws (the fastest-moving risk)

**Status as of September 2026** [F-attr; verify at launch]:
- **Mississippi HB 1126** (age verification for all users): the Supreme Court declined to block it in Aug 2025, and **Bluesky blocked Mississippi** rather than comply. It later offered age assurance to users 18 and over [F].
- **Florida HB 3:** the Eleventh Circuit stayed the injunction on 25 Nov 2025, so the law is enforceable while the appeal continues [F-attr].
- **Louisiana:** Act 456 was permanently enjoined for NetChoice members in Dec 2025. Act 481 took effect 1 Jul 2026 [F-attr].
- **Texas HB 18** (SCOPE): enjoined pending appeal [F-attr].
- **App Store Accountability Acts** in California, Louisiana, Texas and Utah [F-attr]. They reach native apps through app stores.
- **Federal:** the House passed the KIDS Act, which includes KOSA, on 29 Jun 2026 (267–117). The Senate has not agreed [F]. A federal App Store Accountability Act is pending [F].

**Mechanisms:**
1. **PWA first.** The web app is outside the app-store age-verification acts. Native shells come later and use the stores' age signals where they are required.
2. **Account floor of 16 or older.** It removes most parental-consent obligations.
3. **Feature design outside the "addictive feed" definitions**, where counsel confirms this works in each state [counsel].
4. **A state gating matrix in the release pipeline.** For any state where a law requires ID-grade verification of every user for a service of this shape, one of three things happens:
   - (i) accounts in that state require privacy-preserving age assurance (on-device facial age estimation or a reusable credential; only a boolean is stored, R17); or
   - (ii) account creation is geo-gated there, following Bluesky's precedent, while **cards remain viewable and answerable**, if counsel agrees that viewing a card is outside the law [counsel]; or
   - (iii) the state is excluded entirely.
5. **No pilot city is in a state with an in-force all-user verification mandate.**

### EU: the DSA

- **Classification.** Stoke is a hosting service. The Commons makes it an **online platform**, because it disseminates content to the public.
- **Art. 19.** Micro and small enterprises (under 50 staff and at most €10M turnover) are exempt from the Section 3 platform duties (Arts. 20–28), including the Art. 28 minors duty, unless designated a VLOP [F].
- **Stoke complies voluntarily with Section 3 from day one anyway**, because the design already meets it:

| DSA duty | Stoke mechanism |
|---|---|
| Art. 11–12: points of contact | Published contact for authorities and users (email plus a form). |
| Art. 13: legal representative | Not needed once Stoke Ireland Ltd is established at v2. Before then, a named representative. |
| Art. 14: terms and conditions | A plain-language version and a version for minors, versioned in the transparency log (R21). |
| Art. 15: transparency reports | Quarterly, although small enterprises are exempt. |
| Art. 16–17: notice and action, statements of reasons | In-product reporting on every public card. Every restriction notifies the person, names the rule and offers an appeal (R53, no shadow states). |
| Art. 20–21: complaints, out-of-court dispute settlement | A human appeal within 14 days. A certified dispute-settlement body is named in the T&Cs. |
| Art. 25: dark patterns | Upsell lint, no-infinite-scroll lint, a single-screen cancel flow. |
| Art. 26: advertising | None, by charter. |
| Art. 27: recommender transparency | The Commons ordering rules are published, and "why am I seeing this" names the rule on every item (R14). |
| Art. 28 and the July 2025 guidelines | Accounts 16+. Private-by-default. No stranger contact. No recommendation of people or groups. Age assurance compatible with the EU age-verification blueprint and the EUDI wallet when they are available [F: the blueprint is referenced in the guidelines]. |
| VLOP threshold (45M EU monthly active recipients) | Tracked from month 1. **Warning:** if responders who only view cards count as "recipients", VLOP status could come earlier than the account numbers suggest [counsel]. The budget for a VLOP audit, risk assessments and Art. 40 researcher access is in the 100M column of the cost table (c.5). |

### EU: GDPR (Ireland as main establishment from v2)

- **Lawful bases.** Contract (Art. 6(1)(b)) for accounts and Keepers. Legitimate interests for responders' card answers, balanced in the DPIA. Consent for guide memory and for research panels.
- **Art. 8.** Ireland's digital age of consent is 16 [F]. It applies only where the basis is consent, and accounts are 16+ in any case.
- **Art. 9 special categories.** A card for a congregation's supper or a mutual-aid meeting can reveal religion or health. **Mechanism:** private cards are **sealed** by default, so Stoke cannot read them. Public Commons cards are published by the host's own choice, with a warning about special categories.
- **Art. 25 (privacy by design) and Art. 35 (DPIA):** a DPIA before each launch, published in summary.
- **Art. 30:** a record of processing activities.
- **Art. 37:** a DPO is probably not mandatory (no large-scale systematic monitoring), but one is appointed anyway.
- **Arts. 15–20: data-subject rights happen in the product.** Export and deletion run on the device and on the server, well inside Art. 12(3)'s one month.
- **Art. 28 processors:**
  - the LLM provider, under a data processing agreement with zero retention and no identifiers;
  - the SMS and email providers;
  - hosting.
  - Stripe is partly an independent controller for payments [verify].
- **Transfers.** Vendors certified under the EU-US Data Privacy Framework, with standard contractual clauses as a fallback. The General Court upheld the DPF on 3 Sep 2025 (*Latombe*, T-553/23). **An appeal to the Court of Justice is pending** [F]. EU crew relays and EU user blobs are kept on EU-hosted infrastructure, so an adverse ruling costs little.
- **Art. 33:** notify the authority of a breach within 72 hours, the same window as R51 for users.
- **ePrivacy.** No non-essential cookies or trackers, so no cookie banner.

### EU: the e-Evidence Regulation (2023/1543)

- **In force since 18 Aug 2026.** Service providers must appoint a representative, and production orders must be answered within 10 days, or 8 hours in emergencies [F].
- **Mechanism:** a named representative at EU launch, and a legal-process runbook (R27). Stoke **can hand over only what it holds**:
  - account public keys;
  - Keeper status;
  - public cards;
  - reminder contacts, which exist only until the day after the event;
  - IP logs, truncated and kept for at most 7 days.

### EU: Chat Control (CSAR)

- **Status:**
  - The interim derogation for voluntary scanning was re-adopted by the Council in July 2026, running to April 2028 [F-attr].
  - The permanent regulation is still in trilogue. The Council's position drops mandatory breaking of encryption, but the Parliament and the Council are still apart [F-attr].
- **Stoke's position:** no scanning of E2E crews. The deed commits Stoke to **leave a jurisdiction rather than build client-side scanning or a backdoor** (e, threats 2–3).

### UK: OSA and the AADC

- **The OSA applies to user-to-user services "with links to the UK"**, meaning a significant number of UK users or the UK as a target market [F]. Cards are pasted worldwide, so UK users will arrive whether or not Stoke launches there.
- **Mechanisms:**
  - Run the Ofcom **illegal-content risk assessment** and a **children's-access assessment** from v1, because both are cheap for this design.
  - The T&Cs prohibit the primary-priority content categories.
  - Accounts are 16+.
  - The UK AADC's 15 standards are largely met by the defaults.
- **Why the UK is not a launch market:**
  - **OSA s.121 technology notices** can require "accredited technology" to scan for CSEA or terrorism content. The government says the power will not be used until scanning is "technically feasible", **but the power exists** [F-attr].
  - In Jan 2025 the Home Office issued Apple a **technical capability notice under IPA s.253**. Apple withdrew Advanced Data Protection for UK users. The litigation continues: a second challenge was filed in Aug 2026, and a hearing is set for Dec 2026 [F-attr].

  An E2E service that commits to leaving before building a backdoor should not invest in UK marketing while this is unresolved. UK users are served passively, meaning cards open and accounts are allowed, with a documented plan to withdraw crews from the UK if a notice ever arrives.

### Age-verification mandates, as a policy

- **Store a boolean, never a document** (R17).
- **Preferred methods, in order:**
  1. a reusable, privacy-preserving credential (the EU blueprint or EUDI wallet, or app-store age signals where they are legally mandated);
  2. on-device facial age estimation by a vendor bound to deletion and zero retention;
  3. ID checks, only where the law demands them, through a vendor that deletes on completion.
- **Where a law requires ID-grade verification of every user,** Stoke geo-gates accounts, keeps cards working if counsel agrees, and publishes the reason.

## a.6 Launch jurisdictions

| Order | Jurisdiction | Why |
|---|---|---|
| **v1 (month 7)** | **United States: two mid-sized metro areas.** The candidates must be in states where, at launch, no all-user age verification or parental-consent mandate reaches a service of this shape [counsel; verify each state at the time] | §230 and the First Amendment. The team, the entity and the funders are here. English only, which satisfies the language-parity gate R54 with one T&S team. |
| **v2 (month 19)** | **Ireland** (Stoke Ireland Ltd) | English, so parity is met without a new language team. EU main establishment, so the Data Protection Commission leads under the one-stop shop and Coimisiún na Meán is the Digital Services Coordinator [F]. It proves GDPR and DSA operations before a second language. |
| **v3 (month 36+)** | **Germany or the Netherlands, then others**, each one only after the language-parity gate R54 passes | A strong constitutional privacy tradition. Growth in the EU single market. |
| **Not at launch** | **United Kingdom** | IPA technical capability notices and OSA s.121 conflict with E2E crews (a.5). Served passively, not marketed. |
| **Avoid** | **Australia** | The minimum age of 16 has applied since 10 Dec 2025, with maximum penalties quoted at A$49.5M in the Act as passed and higher in some 2026 sources [verify], and exemptions mainly for messaging and gaming [F]. The Assistance and Access Act 2018 raises encryption concerns [F]. |
| **Avoid** | **India** | IT Rules 2021, rule 4(2): traceability of the first originator for significant social media intermediaries is incompatible with E2E [F-attr]. |
| **Avoid** | **Brazil (for now)** | The Digital ECA (Law 15.211/2025) has been enforceable since 17 Mar 2026 and requires "effective and reliable" age verification, with self-declaration not accepted [F-attr]. Stoke enters only after its age-assurance system is proven. |
| **Avoid** | **Russia, China, and others requiring data localization or backdoors** | These are incompatible with the charter. |
| **US states avoided at pilot** | Mississippi, Florida, and any state with an in-force all-user verification or parental-consent mandate that covers us [verify each] | The cost of age assurance comes before product-market fit. Bluesky's precedent is the model if a law arrives later. |

## a.7 Legal checklist (a)–(g) (not legal advice; needs counsel review)

**(a) Trademark clearance before launch.**
- **Finding:** a USPTO registration for **STOKE** by Stoke, Inc. already exists (serial 78443107) [F]. Its goods and services classes were not checked. Other "Stoke" marks are in commerce [F-attr]. **The working name is at high risk.**
- **Procedure:**
  1. A knockout search now: USPTO trademark search, EUIPO/TMview, WIPO Global Brand Database, UKIPO.
  2. Full clearance by counsel in classes 9, 38, 42 and 45 in the US, EU and UK, plus common-law, domain and handle searches (about $3–5k per mark, per region [I]).
  3. Clear **three fallback names in parallel.**
  4. File a US intent-to-use application (§1(b)) and an EU trade mark for the chosen name, **in the Veto Foundation's name.**
  5. Launch only on a cleared name.
- **Budget:** $40k in month 1 of the model.

**(b) Trade dress.**
- Stoke has its own design system. Familiar patterns (lists, buttons, a tap to answer) are fine.
- **Forbidden:** incumbents' distinctive combinations of colour, gradient, iconography and layout.
- **Mechanisms:**
  - a design-review checklist at each release;
  - a design journal as evidence of independent creation;
  - a lint that rejects assets using incumbents' signature brand palettes;
  - counsel review of the first design system.

**(c) Nominative use.**
- Follow the *New Kids on the Block* test [F]:
  1. use the name only where it is needed to identify the product;
  2. use only as much as necessary;
  3. imply no sponsorship.
- **Mechanisms:**
  - **text-only names** in connectors ("Connect YouTube");
  - no logos;
  - a standing line: "Not affiliated with or endorsed by …".
- **The one exception:** a platform's developer terms may *require* its official sign-in button, such as Google's branding rules. That is **licensed** use under those terms, used exactly as specified.
- The marketing-copy lint rejects any incumbent's name in marketing, following Phase 04 g.3.

**(d) Copyright.**
- **Mechanisms:**
  - The Calm Reader stores **identifiers only** (video IDs, post URIs) and renders content through official embeds (the YouTube IFrame player) or links. **Media is never cached or re-hosted.**
  - Bring Your People parses exports **on the device**, and third parties' data never persists (R5).
  - Photos in crew memories are the users' own, encrypted, and licensed to Stoke only as far as needed to relay them.
  - **No training on user content** (a charter clause).
  - DMCA agent and procedure as in a.5.

**(e) Data acquisition.**
- Official APIs and user OAuth only.
- **A connector register** records, for each connector: the terms version, scopes, rate limits, app-review status, the last legal review, and a kill switch.
- **Never** ask for an incumbent password, scrape, rotate IPs, spoof user agents or evade rate limits (operator red line 3; R28).
- X is available only with the user's own API key, subject to X's terms [verify that the terms allow this].
- Portability exports are imported only when the user uploads them.

**(f) Platform-risk architecture.**
- **The wedge makes zero incumbent API calls.**
- Each connector is an isolated service behind a feature flag. A **quarterly "connector death drill"** turns each one off in production-canary and verifies that the core product loses nothing (a CI test: the product passes with every connector disabled).
- **Surviving the other chokepoints:**

| Chokepoint | Mitigation |
|---|---|
| Link previews | Plain-text-first card bodies. |
| Domains | Several domains, plus self-hostable cards under the open spec. |
| CDN | Two providers. Cards are static, so failover is DNS-level. |
| Payments | A primary processor plus a backup merchant of record. |
| LLM | A fallback chain plus a non-AI path for every guide action (C9). |
| App stores | PWA first. |

**(g) Claims discipline.**
- A **claims register**, stored as a versioned file, logs every public statement about an incumbent with its flag ([F], [F-attr], [A], [I]) and its source.
- **[A]** claims need counsel review, and "alleged" appears in the text itself.
- Marketing and onboarding never mention incumbents (Phase 04 g.3). Transparency reports may, but only with flags.
- A pre-publication checklist is the comms gate (R34).

## a.8 Documents counsel must draft (the "real documents, not a manifesto" list)

1. Trust Agreement (Delaware §3556), including the TSC charter and the enforcer provisions.
2. PBC Certificate of Incorporation and Bylaws: share classes, entrenched provisions and Class B consent rights.
3. Veto Foundation articles and bylaws, and the golden-share subscription.
4. Trademark and domain assignment to the Veto Foundation, and a licence to the PBC with termination for covenant breach.
5. IP policy: AGPL for the server, a permissive licence for the spec and client libraries, and assignment from contributors.
6. Commons Foundation articles, Form 1023, and a conflict-of-interest policy.
7. Template for no-control loans (b.2) and a gift-acceptance policy: no data, no seats, no conditions on product.
8. Terms of Service; privacy notice; DPIA; OSA risk assessments; DSA T&Cs; a law-enforcement guide.
9. Stoke Ireland Ltd constitution mirroring the entrenched clauses.
10. A living will: the wind-down and exit plan, funded by the escrowed reserve (b.5).

Estimated legal set-up cost: **$240k over months 0–2**, plus $80k at EU entry. These are in the model [I; based on typical US boutique rates, verify with quotes].

---

# (b) Funding the build

## b.1 The operating revenue model, defended

**Choice.** Two sources, both from Phase 04 a.4:
1. **Keeper memberships:** pay what you can, $0–12 a month, suggested $5.
2. **Flat fees for organizations' Commons tools:** $20–80 a month.

Grants and donations go only to the Commons Foundation's own work. Loans cover the gap until break-even.

**Why not donations only (the Wikipedia model)?** Donations to the Commons Foundation cannot lawfully pay for a PBC's operations without private-benefit risk (a.2). Relying on "the community will support it" is the failure the phase prompt names. Signal, the closest comparable, is about 70% funded by large donors and about 30% by small donors [F-attr]. It is a 501(c)(3), which is the structure rejected here for the holder.

**Why not a higher price or a paywall?** The free floor is entrenched. The price cap is cost-recovery by formula.

**Why organizations?** They are the natural payers. A library or run club already pays for Meetup-style tools, and one organization brings in dozens of responders. The model raises the Phase 04 ratio from 1 to **1.5 paying organizations per 1,000 account-holders**, backed by a two-person partnerships function inside the staff plan, not ads. This is an assumption; the kill criterion K5b below tests it.

## b.2 Funding sources, in sequence (none committed)

| # | Source | When | Base amount | Terms that honour the charter |
|---|---|---|---|---|
| 1 | **Founder capital** | Month 0 | $0.5M (placeholder: replace with the real figure) | A **gift** to the Trust, which contributes it to the PBC. The founder receives no shares, no repayment and no seat. |
| 2 | **Anchor mission loan** (the Signal/Acton analogue: Signal was founded on an interest-free loan from Brian Acton, first reported as $50M and later as larger [F-attr]) | Month 2 | $3.0M | 10 years, 0–1%, **unsecured, subordinated, non-convertible**. **No board seat, no warrants, no information rights beyond the public open books.** Repayment only from surplus above a 6-month reserve. The lender's remedy is a payment claim only. |
| 3 | **Seed grants** to the Commons Foundation, via a fiscal sponsor | Months 3–12 | $0.4M | For the open spec and reference server. **Note:** NLnet's NGI Zero Commons Fund closed its last call on 1 Jun 2026 [F], so a successor programme would have to exist. The Sovereign Tech Agency funds *existing* critical open infrastructure [F], and is realistic only from v2. |
| 4 | **Research and open-source grants** | Months 12–48, $250k a quarter | $3.25M | Funders of research on social connection and loneliness, digital-rights and public-interest-tech foundations [I: candidates, none approached]. They fund the pre-registered H4 study and the spec, and the results are published whatever they show (R50). |
| 5 | **Program-related investment (PRI), tranche 2** | Month 24, gated on H1–H3 passing | $4.0M | A foundation PRI under IRC §4944(c): its primary purpose must be charitable, and income cannot be a significant purpose [F]. Can be lent to a PBC [F]. 1%, 8–10 years, interest-only for 5. Same no-control terms as row 2. **Whether foundations will accept this purpose as charitable is uncertain** [counsel]. |
| 6 | **PRI, tranche 3** | Month 42, gated on H4 and on K5 not triggering | $5.0M | As row 5. |
| 7 | **Donations** to the Commons Foundation | Annually from month 18 | $0.3M a year | An annual appeal. Pays for the Foundation's own staff. |
| 8 | **Revenue** | Keepers from month 9, organizations from month 10 | see table | Stripe, with Stripe Tax for EU VAT (about $3.60 net per US Keeper and about $3.00 per EU Keeper after VAT; blended $3.40 from month 19). |

**Rejected sources:**
- Venture capital and angels (the charter).
- Community shares or crowdfunded equity: holders would be investors.
- Revenue-based financing from commercial lenders: it typically carries covenants and security over IP. It would be allowed only on the row-2 terms, which commercial lenders are unlikely to offer [I].
- Government contracts that come with data-access conditions.
- Crypto token sales.

**Concentration rule.** After month 24, no single funder may provide more than 25% of any year's inflow. The anchor loan is the disclosed exception in year 1.

**The honest totals up to sustained break-even (month 73):**

| Source | Amount |
|---|---|
| Founder capital | $0.5M |
| Anchor loan | $3.0M |
| Seed grants | $0.4M |
| Research and open-source grants | $3.25M |
| Donations | $1.5M |
| PRI loans | $9.0M |
| **Total raised** | **$17.65M** |
| of which debt | $12.0M |

- Operating deficit burned, including 1% interest: **$14.8M**.
- Cash on hand at break-even: **about $3.0M**, which includes the untouchable $0.5M wind-down reserve.

## b.3 Model assumptions (all explicit; the script is reproducible)

| Assumption | Value | Basis |
|---|---|---|
| **Account-holders (A)**, anchor points, interpolated geometrically | Month 6: 300 · M12: 10k · M18: 40k · M24: 120k · M30: 300k · M36: 600k · M48: 1.8M · M60: 3.8M · M72: 6.5M · M84: 10M | Phase 04 g.2 stages (pilot 10k, city 250k, first million by month 30–42). **An assumption, with no data until H2 reports at month 13.** |
| Responders | 3 per A | Phase 04 [I] |
| Keeper conversion | 0 before month 9. Rises linearly from 1.0% (month 9) to 2.5% (month 24), then to 3.0% (month 36) | Phase 04 middle case. Honest range 1–6%. |
| Net per Keeper per month | $3.60 (US) → $3.40 blended once the EU is live (VAT) | $4 average gift, less fees and VAT |
| Paying organizations | 5 hand-signed per month from month 10 (up to 60), then 1.5 per 1,000 A, net $38 each | Raised from Phase 04's 1.0 (b.1) |
| **Variable cost per A per month** | **$0.045** (itemized in c.5) | Phase 04 had $0.066, **then left out SMS, age assurance and support**. With those added it would be about $0.075. Corrected down by on-device and deterministic card drafting (c.3). |
| Staff, fully loaded | **$175k** average (blended US and EU) | Phase 04 used $140k, which is too low for a US-based crypto and security team. Signal's staff budget is about $19M for about 50 people [F-attr]. |
| Staff ladder (gated by A) | 4 → 7 (M4) → 9 (M10) → 13 (A ≥ 60k) → 18 (400k) → 24 (1.2M) → 30 (3M) → 38 (6M) → 50 (12M) | T&S and language parity funded before each region (R54) |
| Other fixed (legal, audit, insurance, accounting, baseline infrastructure, Veto Foundation fee) | $30k a month (≤ M9) → $40k → $60k → $90k → $120k → $150k → $190k → $260k, on the same A gates | [I] |
| One-off costs | Formation legal and trademark $240k (M0–2). Cryptography and MLS security audit $300k (M8). EU entry $80k (M17–18). Annual audit and penetration test $150k (M20, M32, …) | [I; get quotes] |
| Interest | 1% on outstanding loans, interest-only | row 2 and PRI terms |

## b.4 Month-by-month (monthly to month 24, then quarterly to sustained break-even)

All dollar figures are in **$ thousands per month**. "Fixed" is staff plus other plus one-offs. "Net" is revenue minus variable minus fixed. "Cash" is the end-of-month balance after funding and interest.

| Mo | Account-holders | Keeper % | Keepers | Paying orgs | Revenue | Variable | Staff | Fixed | Net | Funding in | Cash |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0.0% | 0 | 0 | 0 | 0 | 4 | 158 | −158 | 500 founder | 342 |
| 1 | 50 | 0.0% | 0 | 0 | 0 | 0 | 4 | 178 | −178 | – | 163 |
| 2 | 100 | 0.0% | 0 | 0 | 0 | 0 | 4 | 168 | −168 | 3,000 anchor loan | 2,992 |
| 3 | 150 | 0.0% | 0 | 0 | 0 | 0 | 4 | 88 | −88 | 100 seed grant | 3,002 |
| 4 | 200 | 0.0% | 0 | 0 | 0 | 0 | 7 | 132 | −132 | – | 2,867 |
| 5 | 250 | 0.0% | 0 | 0 | 0 | 0 | 7 | 132 | −132 | – | 2,732 |
| 6 | 300 | 0.0% | 0 | 0 | 0 | 0 | 7 | 132 | −132 | 100 seed grant | 2,698 |
| 7 | 538 | 0.0% | 0 | 0 | 0 | 0 | 7 | 132 | −132 | – | 2,563 |
| 8 | 965 | 0.0% | 0 | 0 | 0 | 0 | 7 | 432 | −432 (security audit) | – | 2,129 |
| 9 | 1,732 | 1.0% | 17 | 0 | 0.1 | 0.1 | 7 | 132 | −132 | 100 seed grant | 2,094 |
| 10 | 3,107 | 1.1% | 34 | 5 | 0.3 | 0.1 | 9 | 171 | −171 | – | 1,920 |
| 11 | 5,574 | 1.2% | 67 | 10 | 0.6 | 0.3 | 9 | 171 | −171 | – | 1,747 |
| 12 | 10,000 | 1.3% | 130 | 15 | 1.0 | 0.5 | 9 | 171 | −171 | 350 (seed and research grants) | 1,924 |
| 13 | 12,599 | 1.4% | 176 | 20 | 1.4 | 0.6 | 9 | 171 | −170 | – | 1,751 |
| 14 | 15,874 | 1.5% | 238 | 25 | 1.8 | 0.7 | 9 | 171 | −170 | – | 1,578 |
| 15 | 20,000 | 1.6% | 320 | 30 | 2.3 | 0.9 | 9 | 171 | −170 | 250 research grant | 1,656 |
| 16 | 25,198 | 1.7% | 428 | 38 | 3.0 | 1.1 | 9 | 171 | −169 | – | 1,484 |
| 17 | 31,748 | 1.8% | 571 | 48 | 3.9 | 1.4 | 9 | 211 | −209 (EU entry) | – | 1,273 |
| 18 | 40,000 | 1.9% | 760 | 60 | 5.0 | 1.8 | 9 | 211 | −208 | 550 (grant and donations) | 1,612 |
| 19 | 48,037 | 2.0% | 961 | 72 | 6.0 | 2.2 | 9 | 171 | −167 | – | 1,442 |
| 20 | 57,690 | 2.1% | 1,211 | 87 | 7.4 | 2.6 | 9 | 321 | −316 (annual audit) | – | 1,123 |
| 21 | 69,282 | 2.2% | 1,524 | 104 | 9.1 | 3.1 | 13 | 250 | −244 | 250 research grant | 1,127 |
| 22 | 83,203 | 2.3% | 1,914 | 125 | 11.2 | 3.7 | 13 | 250 | −242 | – | 883 |
| 23 | 99,922 | 2.4% | 2,398 | 150 | 13.8 | 4.5 | 13 | 250 | −240 | – | 640 |
| 24 | 120,000 | 2.5% | 3,000 | 180 | 17 | 5 | 13 | 250 | −238 | 4,250 (PRI tranche 2 and grant) | 4,646 |
| 27 | 189,737 | 2.6% | 4,981 | 285 | 28 | 9 | 13 | 250 | −230 | 250 | 4,179 |
| 30 | 300,000 | 2.8% | 8,250 | 450 | 45 | 14 | 13 | 250 | −218 | 550 | 4,044 |
| 33 | 424,264 | 2.9% | 12,198 | 636 | 66 | 19 | 18 | 352 | −306 | 250 | 3,398 |
| 36 | 600,000 | 3.0% | 18,000 | 900 | 95 | 27 | 18 | 352 | −284 | 250 | 2,755 |
| 39 | 789,644 | 3.0% | 23,689 | 1,184 | 126 | 36 | 18 | 352 | −262 | 250 | 2,177 |
| 42 | 1,039,230 | 3.0% | 31,177 | 1,559 | 165 | 47 | 18 | 352 | −234 | 5,550 (PRI tranche 3, grant, donations) | 6,973 |
| 45 | 1,367,704 | 3.0% | 41,031 | 2,052 | 217 | 62 | 24 | 470 | −314 | 250 | 6,179 |
| 48 | 1,800,000 | 3.0% | 54,000 | 2,700 | 286 | 81 | 24 | 470 | −265 | 250 | 5,552 |
| 51 | 2,169,703 | 3.0% | 65,091 | 3,255 | 345 | 98 | 24 | 470 | −223 | – | 4,810 |
| 54 | 2,615,339 | 3.0% | 78,460 | 3,923 | 416 | 118 | 24 | 470 | −172 | 300 donations | 4,512 |
| 57 | 3,152,505 | 3.0% | 94,575 | 4,729 | 501 | 142 | 30 | 588 | −228 | – | 3,819 |
| 60 | 3,800,000 | 3.0% | 114,000 | 5,700 | 604 | 171 | 30 | 588 | −154 | – | 3,249 |
| 63 | 4,345,763 | 3.0% | 130,373 | 6,519 | 691 | 196 | 30 | 588 | −92 | – | 2,878 |
| 66 | 4,969,909 | 3.0% | 149,097 | 7,455 | 790 | 224 | 30 | 588 | −21 | 300 donations | 3,012 |
| **69** | 5,683,697 | 3.0% | 170,511 | 8,526 | 904 | 256 | 30 | 588 | **+60 (first positive month)** | – | 2,930 |
| 72 | 6,500,000 | 3.0% | 195,000 | 9,750 | 1,034 | 292 | 38 | 744 | −3 (staff step to 38) | – | 2,951 |
| **75** | 7,239,107 | 3.0% | 217,173 | 10,859 | 1,151 | 326 | 38 | 744 | **+81 (sustained from month 73)** | – | 3,078 |
| 84 | 10,000,000 | 3.0% | 300,000 | 15,000 | 1,590 | 450 | 38 | 744 | +396 | – | 5,367 |

**Reading it.** Cash is lowest after the pre-launch period at month 23, at **$0.64M**, just above the $0.5M wind-down reserve. **The plan is most fragile in months 20–24**, before PRI tranche 2 arrives. If that tranche slips by a quarter, the plan B trigger fires (b.6).

**After break-even.** The $12M of loans are repaid from surplus between months 84 and about 108, keeping at least 6 months of operating cost in reserve. Once the loans are repaid, the Phase 04 surplus ratchet (reserves capped at 18 months) forces the suggested Keeper price down. In the model, cash above the cap appears by about month 110.

## b.5 Reconciling with Phase 04: it was too optimistic

| Phase 04 said | What was wrong | Effect |
|---|---|---|
| Break-even at "about 6–7M account-holders" at 3% | It **gave no timeline and no cumulative cost**, which is the number a funder needs. | Now stated: month 69/73, $14.8M. |
| Staff at $140k fully loaded | Too low for a US-based team that includes cryptography and security specialists (Signal: about $19M for about 50 staff [F-attr]). | +25% on the largest cost. |
| Variable cost of $0.066 per A | It **left out** SMS reminders, age assurance, support tooling and EU VAT on Keeper revenue. | Uncorrected, about $0.075. |
| **Uncorrected result** (Phase 04 unit economics, $175k staff) | – | **Break-even slides to month 89 (first) and month 105 (sustained), at about 16.6M account-holders and a $23.7M deficit.** Phase 04's own inputs with $140k staff give month 81/93, 12.9M and $15.6M. |
| **Fixes applied here** | (1) Card drafting on the device, with a deterministic parser; the server LLM is used only when needed (c.3), so the guide costs $0.018 instead of $0.042. (2) SMS is capped and US-only; email, calendar files and web push are the defaults. (3) A partnerships function raises organizations to 1.5 per 1,000. | Variable cost $0.045; margin per A about $0.114 a month. **The break-even scale survives (about 6.7M), but only because of these changes, and each change is itself an assumption.** |

## b.6 Sensitivity

The runs change one input at a time from the base case unless stated. "First" is the first month with a positive net. "Sustained" means positive for the next 12 months. The peak operating deficit excludes interest.

| Case | First BE | Sustained BE | A at break-even | Peak deficit |
|---|---|---|---|---|
| **Base** (3%, 1.5 organizations per 1,000, $0.045, $175k) | M67 | **M73** | 6.7M | $14.3M ($14.8M with interest) |
| Keeper conversion 4% | M61 | M61 | 4.0M | $12.1M |
| Keeper conversion 2% | M82 | M93 | 12.9M | $19.3M |
| Keeper conversion 1.5% | M90 | M105 | 16.6M | $24.6M |
| **Keeper conversion 1%** | M119 (not sustained) | **never within 20 years at this staff ladder** | – | > $34M |
| Organizations at 3 per 1,000 | M55 | M59 | 3.6M | $10.9M |
| Conversion 1% **and** organizations at 3 per 1,000 | M70 | M81 | 9.0M | $15.5M |
| Growth at 0.7× speed | M96 | M105 | 6.9M | $20.4M |
| Growth at 0.5× speed | M134 | M153 | 7.6M | $28.6M |
| Variable cost 2× ($0.09) | M87 | M105 | 16.6M | $22.1M |
| Staff cost +20% ($210k) | M70 | M81 | 9.0M | $18.3M |
| Combined downside: 2% conversion **and** 0.7× growth | M118 | M118 | 9.5M | $27.6M |

**What this says.** The plan is most sensitive to **conversion, growth speed and organization revenue**. **Organization revenue is the strongest lever** that stays inside the covenant. At 1% conversion, memberships cannot carry the plan unless organizations reach about 3 per 1,000. Phase 04's K5 is therefore split:
- **K5a:** Keeper conversion below 1.5% at month 24 means re-planning (b.7).
- **K5b:** fewer than 1 paying organization per 1,000 account-holders at month 24 means re-planning.
- **Both at once** means moving to caretaker mode (plan C).

## b.7 If funding falls short halfway (month 36)

**The scenario.** PRI tranche 3 ($5M at month 42) does not come, and research grants halve from month 36.
- **With no action, cash goes negative in month 48.**

**Pre-committed triggers.** These are written into board policy and the Trust deed, and each one is reported publicly.

| Trigger (runway at the planned burn) | Mode | What changes |
|---|---|---|
| < 18 months | **Plan B: freeze** | Headcount frozen at the current level (18 in this scenario). Other fixed costs capped at $90k a month. No new regions. The free guide allowance drops from $0.01 to $0.005 a day, with the card form unaffected. SMS for Keepers only. |
| < 12 months | **Plan C: caretaker** | 6 staff (2 engineers, 2 T&S, 1 operations, 1 finance and legal). Cards, crews, the Commons and export keep running. The guide is off for free users. Existing regions only. |
| < 6 months, or caretaker is not viable | **Plan D: orderly handover** (the living will) | 90 days' public notice. An export drill for every account. The open spec, code and a reproducible deployment go to the Commons Foundation or another steward. Cards keep resolving from a static archive for 12 months, paid for by the **escrowed $0.5M wind-down reserve**, which no creditor or board can touch. After that, domains go to the Veto Foundation for redirects. All server data is deleted, with signed receipts. |

**Modelled outcomes:**

| Outcome | Result |
|---|---|
| **Plan B at base growth** | Survives with essentially zero margin (lowest cash about −$6k at month 53). **Sustained break-even at month 57, at 3.2M A**, earlier than the base case, because fixed costs are lower. **This is optimistic:** it assumes growth continues with no new regions. |
| **Plan B at 0.7× growth** | Break-even at month 81 at 3.1M A. **About $4.5M short** at the lowest point, so plan B alone is not enough. |
| **Plan C at base growth** | Cash positive throughout, and self-funding from about 1.3M A (about month 42). |
| **Plan C at 0.5× growth** | Survives on the remaining grants and donations. Cash falls to about $80k at month 84, **below the reserve, so the reserve would have to be ring-fenced separately.** Break-even around month 90 at about 1.4M A. |

**The honest summary.** A shortfall halfway through is survivable **if the triggers are obeyed early**. The survivable version is a smaller, slower Stoke with no new regions. The kill case is 1% conversion together with weak organization revenue and slow growth. In that case plan D is the covenant-honouring outcome: people leave with their data, and cards keep working.

## b.8 Guardrails that keep money from corrupting the model

- Loans and grants follow the **gift-acceptance policy**: no data, no seat, no product conditions, and published in the open books.
- **No metric targets in any funding agreement.** Funders get the public dashboard and nothing more.
- The Keeper ask appears only on the pricing page, in one annual note, and at the free-cap message, which is plain and has no upsell (C8). The upsell lint enforces this.

---

# (c) Technical architecture

## c.1 Principles that make sovereignty true in the architecture

1. **The keys live on the user's devices.** The server never holds a key that decrypts private content.
2. **Everything private is ciphertext on the server.** Everything plaintext on the server is either public by the user's choice or short-lived operational data with a stated deletion time.
3. **Every format is open, and the reference server is AGPL.** A user can leave for another host, or host themselves, and keep their identity.
4. **Exit is tested in CI and in production drills, not promised** (H9).

## c.2 Data model: what is stored, where, and who holds the keys

| Object | Where it is stored | Plaintext to the operator? | Who holds the keys | Retention |
|---|---|---|---|---|
| **Identity keypair** (Ed25519 signing, X25519 key agreement) | The device (secure enclave or WebCrypto, non-extractable where supported). Wrapped by a passkey (WebAuthn PRF extension where the platform supports it [verify support]) plus a 24-word recovery code | No | The user | Until the user deletes it |
| **DID** (`did:plc` or `did:web`) | The PLC directory (moving to an independent Swiss association [F]) or the user's own domain | Public | **The user holds the highest-priority rotation key.** Stoke's PDS holds a lower one. did:plc lets a higher-priority key undo operations signed by a lower-priority key within 72 hours [F], so **the user can take their identity back from us**. | Permanent (the user's) |
| **Account record** | Postgres | Yes: random account ID, public keys, DID, Keeper tier and renewal date, Stripe customer ID, an age-assurance boolean with method and jurisdiction, created-at. **No email required**; an optional recovery or receipt email is stored separately. | – | Deleted on account deletion (crypto-shred plus row delete). Payment records kept for the tax retention period [counsel]. |
| **Private card** (the default) | Object storage, as ciphertext | **No.** Encrypted with a card key held in the URL **fragment** (`#k=…`), which browsers never send to the server. OpenGraph shows only "You're invited: tap to open" unless the host chooses a visible preview. | The host and anyone the link is pasted to | 30 days after the event unless pinned |
| **Public card** (Commons) | Postgres/PostGIS plus CDN, and an AT Protocol record plus an ActivityPub `Event` | Yes, public by choice. Location coarsened to about 1 km until the host approves a responder. | Host signs it | 30 days after the event |
| **RSVP** | Postgres | For private cards: **no**. Name and answer are encrypted to the host's key; the server sees a ciphertext count. For public cards: display name and answer. | Host | With the card |
| **Reminder contact** (phone or email for a responder who asked for a reminder) | Postgres, encrypted at rest with a KMS key | **Yes, necessarily**, because the server sends the reminder | Operator KMS | **Deleted 24 hours after the event** |
| **Crew messages, notes, photos** | The MLS (RFC 9420) relay's delivery queues and an object-store blob | No: ciphertext only | Crew members' MLS group keys | Until members delete them. Blobs are crypto-shredded on removal. |
| **Crew metadata** | Relay | **Partly.** The relay sees per-device queue tokens, message sizes and timing. It does not see names or content. | – | Queue entries deleted after delivery plus 30 days |
| **Guide memory** | The device (encrypted SQLite, from the Phase 02 MemoryStore moved to the client, C1). An optional encrypted sync blob. | No | The user | The user's choice |
| **Guide prompts** | Pass through the stateless gateway to an LLM with zero retention | Transiently, in memory | – | Not stored (R20) |
| **Audit and lineage heads, governance acts, egress allowlist** | Transparency log (Sigsum or a Trillian-Tessera-class log [verify the choice]) | Public hashes | Log witnesses | Permanent |
| **Server logs** | Aggregated, IP truncated | Coarse | – | 7 days |
| **Metrics** | Aggregates with local differential privacy (d.2) | Only aggregates with k ≥ 50 or ε ≤ 1 | – | Aggregates kept |

## c.3 Services

| # | Service | What it does | Technology (why) |
|---|---|---|---|
| 1 | **Card renderer** | Renders a signed card to static HTML, OpenGraph, `.ics` and plain text. Private cards decrypt in the browser. | Edge functions plus object storage. Static pages of about 50 KB, 2G-friendly and cheap. |
| 2 | **RSVP API** | Writes responses (ciphertext for private cards), rate-limits and resists abuse. | Go or Rust, on Postgres partitioned by a hash of the card ID. |
| 3 | **Reminder scheduler** | Sends only the reminders people asked for. Sent must equal scheduled (R12). | From the Phase 02 `scheduler.py` design (atomic leases). Email and web push by default. SMS only in the US, capped at 2 per responder per card. |
| 4 | **Crew relay** | The MLS delivery service and the blob store. | Rust with OpenMLS [F: an open-source MLS implementation; audit status to verify]. EU data on EU infrastructure. |
| 5 | **Identity and PDS** | DID registration, handle resolution, an AT Protocol PDS, and a key directory with key transparency. | The reference PDS; users can migrate. |
| 6 | **Guide gateway** | Adds the charter slot, runs the LoyaltyGuard, enforces budgets and the provider fallback chain, and keeps nothing. | The Phase 02/03b `mind` modules (charter, loyalty, cost), server side. **Card drafting runs first on the device**: a deterministic parser for "tacos saturday?" style input and a small on-device model where available. The server LLM is called only for harder requests. This is the variable-cost fix in b.5 [I: the saving is an estimate to be measured]. |
| 7 | **Commons index** | Public cards ordered by time, distance, the reader's own rules and follows **only**. A CI lint rejects any other ranking feature. | PostGIS, an ActivityPub outbox, and AT Protocol records. |
| 8 | **Billing** | Stores the Stripe customer ID and tier only. Handles regional prices and VAT. | Stripe and Stripe Tax, with a backup merchant of record. |
| 9 | **Trust & safety tooling** | Report intake (with **message franking** for E2E evidence), case management, statements of reasons, DSA transparency-database submission, the TAKE IT DOWN 48-hour queue, NCMEC reporting. | Built in-house on Postgres. **Can reach only public content and what reporters submit.** |
| 10 | **Transparency publisher** | Daily log roots, the open books, the experiment registry, the egress allowlist. | A static site plus the log. |
| 11 | **Connectors** (Calm Reader, Bring Your People) | Optional and isolated. Each has a kill switch and a quarterly death drill. | Separate deployables. Bring Your People runs entirely on the client. |
| 12 | **Age-assurance adapter** | Works with any vendor or credential and stores a boolean. | Swappable. |

**Clients.**
- A **PWA first**: TypeScript UI, with the Rust cryptography core compiled to WASM.
- Native shells later (Swift and Kotlin wrapping the same Rust core). They matter for E2E: see e.2, threat 2b.
- **Reproducible builds** for every client, with releases signed 2-of-3 (see e.2).

## c.4 Infrastructure choices and the scaling plan

| Stage | Infrastructure | Why |
|---|---|---|
| **v1 (≤ 100k A)** | One US region on a managed container platform. Managed Postgres (HA). Object storage with zero-egress pricing (R2-class, about $0.015 per GB-month [verify]). Two CDNs, email via an established provider, SMS via one US provider with 10DLC registration [verify]. | Small team. Standard, portable parts: containers, Postgres and S3-compatible APIs, so there is no lock-in. |
| **v2 (≤ 1M A)** | Adds an EU region on an EU-headquartered provider for EU users' crew relays, blobs and account rows. Read replicas. Postgres partitioned by card ID. | GDPR transfer resilience (the *Latombe* appeal), and data residency. |
| **v3 (≤ 20M A)** | Multi-region active-active for cards and RSVPs, which are almost stateless. Crew relays sharded by group ID. Bare metal or colocation for bulk blob storage when it becomes cheaper. A self-hosted open-weight small model for the guide's routine requests. | Unit costs fall. The LLM becomes a commodity. |
| **100M A** | Regional cells (each cell serves about 10M A), with cells isolated so one failure has a limited blast radius. A 24/7 SRE rotation. DDoS protection from two providers. Federated hosting encouraged: third-party hosts serve cards under the open spec. | Cells scale linearly. Federation spreads the load and the power. |

**What does not scale with users:** there is no engagement pipeline, no recommendation training, no ad system and no per-item analytics. The data platform is small by construction. That is the main reason the cost per user is low.

## c.5 Cost per account-holder per month

Account-holders (A) are the unit. Monthly people are about 4 × A, counting responders.

| Line item | 10K A (≈ month 12) | 1M A (≈ month 42) | 100M A (steady state [I]) |
|---|---|---|---|
| Guide LLM (drafting on device first; capped) | $0.020 | $0.018 | $0.010 (self-hosted small model and volume pricing) |
| Encrypted storage (average 0.3 GB) | $0.006 | $0.006 | $0.005 |
| Compute, relay, database, CDN (marginal) | $0.006 | $0.006 | $0.004 |
| Responders (3 per A: views, RSVPs, `.ics`) | $0.006 | $0.006 | $0.004 |
| Notifications (email and push; SMS US-only and capped) | $0.005 | $0.005 | $0.003 |
| Age assurance and abuse prevention | $0.003 | $0.002 | $0.002 |
| Support tooling | $0.002 | $0.002 | $0.001 |
| **Variable subtotal** | **$0.048** | **$0.045** | **$0.029** |
| Baseline infrastructure (HA database, observability, staging, security tooling, log, HSMs) | $3k/mo → $0.30 | $15k → $0.015 | $0.5M → $0.005 |
| **Infrastructure only, per A** | **$0.35** | **$0.060** | **$0.034** |
| Staff | 9 → $131k → $13.13 | 18 → $262k → $0.26 | ~260 (about 120 in T&S across 20+ languages) at $150k global blend → $3.25M → $0.033 |
| Other fixed (legal, audit, insurance, DSA VLOP audit and supervisory fee at 100M) | $37k → $3.70 | $75k → $0.075 | $1.2M → $0.012 |
| **All-in per A per month** | **≈ $17.2** | **≈ $0.40** | **≈ $0.079** |
| All-in per monthly person (÷ 4) | ≈ $4.30 | ≈ $0.10 | ≈ $0.02 |
| Revenue per A per month at 3% | ≈ $0.10 | ≈ $0.159 | ≈ $0.159 |

**Sanity check.** Signal runs at about $50M a year, including about $14M of infrastructure, with SMS verification a large share of that [F-attr]. Stoke at 100M A would cost about $95M a year, with far more T&S because of the public Commons and language parity. At that scale the surplus ratchet would cut the suggested Keeper price, from about $5 towards about $2.50 [I].

## c.6 How the architecture makes exit real

1. **Export in one step, produced on the device.** A signed archive containing: cards (JSON and `.ics`), crew histories (decrypted locally), guide memory (SQLite), contacts the user chose to keep, and the DID rotation material. Its format is in the open spec.
2. **Identity leaves with the user.** The user's top-priority did:plc rotation key lets them repoint their DID to another PDS **without our cooperation**, including against us, within the 72-hour recovery window [F]. Their followers on the public Commons follow the DID, not our database.
3. **Hosting leaves too.** The AGPL reference server and the conformance suite let anyone run a compatible host. Cards on any compliant host render in Stoke's client and the other way round.
4. **Deletion is cryptographic.** Each user's server-side data sits under a per-user data key. Deletion destroys the key. Backups hold only ciphertext under destroyed keys, so they **cannot be decrypted after 30 days** (H9). Signed deletion receipts go to the user and the log.
5. **Exit is tested continuously:**
   - a CI "leave and come back" test (export → import into the reference server → state diff = 0);
   - a quarterly production drill on canary accounts;
   - a DID migration test against an independent PDS.
6. **The business cannot hold data hostage**, because it cannot read the data (R1, R20), and the charter says it is not an asset (R26).

---

# (d) Metrics and Goodhart defences

## d.1 Rules that apply to every metric

1. **Watch, don't target.** No metric is tied to pay, bonuses, performance reviews or funder agreements (a charter clause; pay ratio at most 5×).
2. **Every metric is paired with a counter-metric** that moves the wrong way if the first one is gamed.
3. **Measurement is private.** Client-side aggregation with local differential privacy (randomized response, ε ≤ 1) or k ≥ 50. No per-person event stream exists to mine.
4. **Definitions are frozen and public.** Any change is logged, announced 30 days ahead, and reviewable by the jury. **The sortition jury can retire a metric that it finds is being gamed.**
5. **The dashboard is published.** Every figure below goes into the monthly open books unless it is marked internal-alarm, and those are published quarterly.

## d.2 The north star, and how it is measured

**North star: people who gathered in person through a card this month (P-gathered).**
- *Measurement:* after a card's date, the host's device is asked once: "did it happen?" If yes, it asks for a bucketed count (2–5, 6–15, 16+). The answer is reported under local differential privacy. It is optional, and it is never asked twice.

**Counter-metric: minutes in the app per gathering (M/G). Lower is better.**
- *Measurement:* each device keeps a coarse weekly bucket of foreground time and reports it under local differential privacy. The ratio is computed in aggregate.

**Together they express the thesis:** more people together, less screen time.

## d.3 The full dashboard

| # | Metric | Why it exists | How it could be gamed into extraction | Structural defence |
|---|---|---|---|---|
| 1 | **P-gathered** (north star) | The mission outcome | More prompts and notifications to make cards; fake confirmations | Paired with #2 and #6. Notifications sent must equal those scheduled by people (#6 alarm). Capped at 1 gathering per host per day. Reported by the host only, with LDP noise. The jury audits sampled definitions. Not tied to anyone's pay. |
| 2 | **M/G**, minutes in the app per gathering | Screen time must not rise | Hiding time in notifications or widgets | Also count notifications and widget refreshes per gathering. The client is open source, so measurement code is auditable. **Alarm if it rises for 2 months while #1 is flat (K6).** |
| 3 | **"Saw people I care about"**: the H4 panel (opt-in, pre-registered, run by an independent researcher, with a waitlist control) | Whether the thesis is true | Wording or sampling the survey to flatter results | Pre-registration. The researcher is independent, and funded through the Commons Foundation, not the PBC. Results published within 12 months, whatever they show (R50). |
| 4 | **Second card within 30 days** (H1) | Usefulness | Pestering people to make a second card | No nudges exist that could do it: the upsell and engagement lints and HUMAN-CONTACT apply. Paired with #2. |
| 5 | **Spread k** (new makers who first arrived as responders) | Distribution (H2) | Invite spam; referral rewards | **No referral rewards, no contact upload** (charter). HUMAN-CONTACT tier. Invite rate limits. Reported, never targeted. |
| 6 | **Notifications sent ÷ scheduled by people** | No engagement notifications | Reclassifying system messages as "scheduled" | The only valid value is 1.00. The scheduler's code path is the sole sender, and the audit log (R12) is published by hash. **Any value above 1.00 is an incident.** |
| 7 | **Keeper conversion and average contribution** | Solvency (H5) | Dark-pattern upsells; guilt copy; paywall creep | Upsell lint (C8). Ask-frequency cap. Free floor entrenched. Price capped by formula. A council veto on prices. Reported, never targeted by staff. |
| 8 | **Paying organizations per 1,000 A** | Solvency (K5b) | Selling organizations access to people or data | R25: organizations see only what people choose to share. No sponsorship or placement exists to sell. Contract template reviewed by the Veto Foundation. |
| 9 | **Cost per A** (c.5) | Sustainability | Cutting T&S or language parity to save money | The T&S budget share per region is at least that region's share of users, published (R54). Parity gate in the release pipeline. |
| 10 | **Exit health**: export success rate, import diff = 0, time to delete, deletion-receipt rate | Sovereignty (H9) | Shrinking what the export contains | The conformance test checks completeness against the data model (c.2). Any failure blocks releases. |
| 11 | **Operator plaintext footprint**: categories of plaintext user data on servers, and the egress allowlist | Privacy (H7) | Adding "harmless" telemetry | The allowlist is enforced at the network layer and published. Any addition needs a transparency-log entry with 30 days' notice. Annual red team with canary accounts. |
| 12 | **Safety**: reports per 10k cards, time to action (under 24 hours for violence and self-harm), appeal overturn rates in both directions, TAKE IT DOWN requests met within 48 hours | Harm (H11) | Hiding the report button to lower the report rate | Report UI presence is checked in CI. Reports are counted per surface. An independent audit. Overturn rates are published, so over-removal also shows. |
| 13 | **Language parity**: coverage per language (reviewers, evaluations, crisis resources) against the primary language | Geographic externalization (H12) | Launching early and "catching up" later | The release pipeline hard-blocks a language that fails. A bypass is a charter breach reported to the enforcer. |
| 14 | **Concentration**: share of Commons cards from the top 1% of hosts | No reach economy | Engineering a "power-host" tier | Ranking may not read popularity (lint). **Alarm above 20%.** |
| 15 | **Governance health**: council turnout, jury decisions, days to publish studies, open-books delay | Power bound by structure | Low-turnout capture | Published turnout. One-person-one-vote credentials (e.2, threat 17). The Veto Foundation can block regardless. |
| 16 | **Runway in months** at the planned burn | Survival | Growth-at-all-costs fundraising pitches | The b.7 triggers are pre-committed and public. |

## d.4 Alarms (they trigger action, not just charts)

| Alarm | Threshold | Action |
|---|---|---|
| Notification ratio | > 1.00 on any day | Incident. Roll back. Publish within 7 days. |
| M/G rising while P-gathered is flat | 2 consecutive months | Jury review. Public note: "we are becoming a feed". |
| Plaintext footprint grows | Any unannounced category | Incident. Enforcer notified. |
| Concentration | Top 1% of hosts > 20% of Commons cards | Design review of the Commons. |
| Safety service levels | < 95% within target for 2 weeks | T&S budget increase is mandatory before any new feature ships. |
| K5a / K5b | Conversion < 1.5% or organizations < 1 per 1,000 at month 24 | Re-plan (b.7). |
| Runway | < 18 / 12 / 6 months | Plans B / C / D. |

---

# (e) Threat model

## e.1 The privacy architecture as a system (not a policy)

- **Controls that exist in code:**
  - E2E crews (MLS);
  - sealed private cards (the key lives in the URL fragment);
  - on-device guide memory;
  - a stateless LLM gateway;
  - reminder contacts deleted 24 hours after the event;
  - IP logs truncated and kept 7 days;
  - LDP metrics;
  - an egress allowlist enforced at the network layer;
  - crypto-shredding on deletion;
  - no third-party SDKs;
  - reproducible builds with 2-of-3 signing;
  - a user-visible access log (R48) anchored in the transparency log.
- **What the operator can reach:**
  - public cards;
  - account rows (no content);
  - Stripe customer IDs;
  - reminder contacts, briefly;
  - crew metadata (queue tokens, sizes, timing).
- **Everything else is ciphertext or does not exist.**

## e.2 Threats

| # | Attacker | Attack | Structural mitigation | What breaks if the mitigation fails |
|---|---|---|---|---|
| 1 | **State actor: legal compulsion** (subpoena, court order, NSL, FISA 702, CLOUD Act, EU e-Evidence production orders) | Demands user data | Data minimization and E2E, so the operator can hand over only the list in a.5 (e-Evidence). A law-enforcement guide. The user is notified unless gagged. Overbroad orders are challenged. Semi-annual transparency report (R27). | **Crew metadata** (who shares queues with whom, and when) could expose parts of a social graph. Reminder contacts inside their 24-hour window. |
| 2a | **State actor: compelled backdoor** (UK IPA technical capability notice, OSA s.121, a CSAR detection order, Australian TOLA) | Orders client-side scanning or key escrow | No escrow capability exists. **The deed commits Stoke to leave the jurisdiction rather than comply.** Release-signing is 2-of-3 with the Veto Foundation holding one key, so staff alone cannot ship a secret build. | If a gagged order and a captured key-holder coincide, a targeted malicious build is possible. Mitigation 2b applies. |
| 2b | **State actor or insider: code-delivery attack on the web client** | Serves one user a modified PWA that exfiltrates keys | **Honest weakness: web E2E is only as trustworthy as the server that serves the code.** Mitigations: native shells with signed, reproducible builds for crews; binary transparency (release hashes in the log, checked by the native client and by an optional browser extension, similar to WhatsApp Web's Code Verify [F-attr]); a PWA service worker that pins the hash of the release it installed. | A targeted user on the plain web, with no verifier installed, can be compromised without detection. **Crews are advised to use native apps. This is stated in the product.** |
| 3 | **State actor: censorship or APT** | Blocks domains; hacks servers | Multiple domains. Self-hostable cards. Plain-text cards survive a blocked domain. There is little plaintext to steal. HSM-held signing keys. | The service is unavailable in that region; cards still travel as text. |
| 4 | **Criminal: server breach** | Dumps the databases | Private content is ciphertext. Reminder contacts are KMS-encrypted and short-lived. There is no password database (passkeys only). | Exposed: account public keys, Stripe customer IDs and, possibly, reminder contacts. Notification within 72 hours (R51, GDPR Art. 33). |
| 5 | **Criminal: account takeover or stolen device** | Reads a user's crews | Passkeys. Device keys. Revocation from other devices. MLS post-compromise security heals the group once the device is removed. | That user's history on that device is exposed. E2E cannot help. |
| 6 | **Supply chain** (a dependency or the build system) | Malicious code in a release | Pinned and vendored dependencies. Reproducible builds. SLSA-style provenance [verify level]. Two-person review. 2-of-3 signing. | A malicious release is detectable after the fact, but some users could be affected before it is caught. |
| 7 | **Malicious insider** | Adds telemetry; reads reminder contacts; tampers with logs | Network-level egress allowlist. CI lints. Two-person rule for production. Every privileged access is recorded in the user-visible access log (R48) and anchored externally (C3). Nothing private is readable. | A colluding pair with production access could read reminder contacts inside their 24-hour window. Detectable from the access log. |
| 8 | **Future leadership: slow drift** ("just a little telemetry", "a gentle upsell", "a smarter Commons ranking") | Rebuilds the trap feature by feature | Entrenched charter clauses. d.1 rules. Public metric definitions. Ranking and upsell lints in an open repository. Annual audit against R1–R59. The jury. **The enforcer can sue** for breach of purpose. The Veto Foundation can revoke the trademark licence. | If every body is captured: **forkability is the last line.** Open spec, AGPL server, user-held keys and portable DIDs mean the community can re-host and users can leave with everything. **A captured Stoke would have no hostages.** |
| 9 | **Future leadership: sale, IPO or conversion** | Sells or converts | a.2 and a.3: trust deed, golden share, authorized = issued, brand held outside, data unreadable. | Collusion plus a court modification (a.4). Even then the buyer gets no data, no brand and no proprietary code. |
| 10 | **Future leadership: borrowing into capture** | Takes secured or controlling debt, then defaults on purpose | Charter bans on secured and governance-bearing debt, and a debt cap at 24 months of operating cost, all needing Class B consent. | Needs the Veto Foundation to consent. |
| 11 | **Funders** | Grant or loan conditions that steer the product | Gift-acceptance policy. 25% concentration cap after month 24. All terms published. | The anchor loan is the year-1 exception. That dependence is disclosed. |
| 12 | **Coordinated abuse: spam or phishing cards** | Uses the card domain to deliver phishing | Cards live on a separate domain from the app. Rate limits for new hosts. Safe-browsing checks on links in public cards. Reports. | Messaging apps may blocklist the domain, so there is a second domain plus self-hosting. |
| 13 | **Harassment and stalking via cards** | Uses a card's location or guest list to find someone | Sealed by default. The attendee list is visible only to the host by default. First names only. Location coarsened until the host approves. Blocking. Minors have no Commons access. | A malicious *host* still sees their own guests. That is inherent. Public-place defaults and reporting apply. |
| 14 | **Brigading the Commons** (fake events, astroturf, extremist organizing in public) | Floods or lures | No amplification or recommendation. An account is required to post. Posting caps. Human review of reports. The jury can shut the Commons in a region (H11). | Fake-event lures carry a real physical risk. Mitigated by public-place defaults and fast takedown, not prevented. |
| 15 | **Grooming** | An adult reaches a minor | Accounts are 16+. Minors have no Commons and no stranger contact. No recommendation of people. | **Responders without accounts can be minors** (Phase 04 row 11). A card pasted by an adult can reach them. Residual. |
| 16 | **CSAM or NCII in E2E crews** | Private distribution | Crews capped at 150. No crew discovery. Message-franked reports. TAKE IT DOWN process. NCMEC reporting on knowledge. | **Small private rings go undetected.** This is the same trade-off Signal and WhatsApp make, chosen deliberately (Phase 03, B4). |
| 17 | **Sybil attack on governance** | Captures council elections or the jury pool | Voting credentials: an account at least 90 days old, and at least 2 host-confirmed gatherings attended. Issued as blind anonymous tokens (Privacy Pass-style), so each person votes once without being tracked. Jury drawn by lot. | A patient attacker who organizes real gatherings could farm credentials. **The golden share still blocks charter changes.** |
| 18 | **Prompt injection against the guide** | A crew message or card response steers the guide | C5 taint tracking. HUMAN-CONTACT tier. No send tool runs without a tap. | Guide output is tainted or refused. The card form still works (C9). |
| 19 | **LLM provider** | Keeps or leaks prompts | Zero-retention terms. No identifiers. Minimal context assembled on the device. Provider fallback chain. A self-hosted model at v3. | Guide-memory snippets from the affected period are exposed. |
| 20 | **Payment processor deplatforming** | Cuts off revenue | A backup merchant of record. A reserve. | Revenue interrupted for weeks. |
| 21 | **Incumbents** (link throttling, cloning) | Phase 04 g.4 | Plain-text-first cards, the open spec, several channels. | Previews degrade; cards still work. |

---

# (f) Roadmap: v1, v2, v3

Each version is usable and valuable on its own. Each proves something the next one depends on. Months match the model in (b).

## v1 "Cards" (months 0–12; ≈ 10k account-holders; the first 1,000 hosts in two US metros)

**Ships:**
- the card (open spec 0.x) as HTML, OpenGraph, `.ics` and plain text, with responses that need no account;
- **sealed private cards**;
- reminders by email, push and US-only SMS, including "reply 1";
- host tools;
- export and delete;
- the transparency log and the first open books;
- Keeper membership (month 9) and organization tools (month 10);
- the guide's card drafting **only if the real-LLM battery K8 passes**, otherwise the form.
- **Legal:** entity formed, cleared name, DMCA agent, TAKE IT DOWN flow, COPPA and state gating matrix, OSA risk assessments.

**Why it works alone:** planning with friends works on day one, with nobody else's network.

**What it proves, which v2 depends on:**

| Proof | Result needed |
|---|---|
| H1 (second card) | ≥ 40% |
| H3 (no-signup response) | ≥ 60% |
| Variable cost per A | within 20% of $0.045 |
| Paying organizations | first 20 |
| The governance documents | work in practice: first TSC meeting, first open books |

H2's first k reading comes at month 13. **Gate for v2:** H1 and H3 pass, the cryptography audit is clean, and the PRI conversations are live.

**Distribution:** hosts, not users (Phase 04 g.2). There is no press and no ads, and the team supports hosts in person every week.

## v2 "Crews and the Commons" (months 13–30; ≈ 300k account-holders; the first million people touched)

**Ships:**
- crews (MLS, E2E), memories, a shared calendar;
- the Commons (public cards by time and distance only);
- the organization tier (recurring series, roster roles, embedding);
- AT Protocol and ActivityPub interoperability;
- native shells for crews (e.2, threat 2b);
- **Ireland** (month 19): Stoke Ireland Ltd, DSA and GDPR operations, the e-Evidence representative;
- the **first members' council election** (at ≥ 50k A) and the first sortition jury;
- the first annual audit (month 20);
- "The Longest Evening" solstice event.

**Why it works alone:** repeat gatherings get a home. Organizations get tools worth paying for.

**What it proves, which v3 depends on:**

| Proof | Result needed |
|---|---|
| H2 (spread) | k ≥ 0.3 |
| H4 (the pre-registered study) | first read at 3 months |
| H5 | conversion ≥ 2.5% by month 24 |
| K5b (organizations) | ≥ 1 per 1,000 A |
| H7 (operator blind at real scale) | red team recovers nothing |
| EU compliance | DSA and GDPR operations work in a second jurisdiction |
| H12 | parity machinery works (English in two jurisdictions) |

**Gate for v3:** H4 shows an effect; K5a and K5b are not triggered; PRI tranche 3 is committed.

## v3 "The guide and the open door" (months 31–60; ≈ 4M account-holders; defaults in institutions)

**Ships:**
- the full guide: memory on the device, consent-gated introductions, and semantic drift review (the F8 fix);
- Bring Your People (on-device import of portability exports);
- From Above (a seasonal on-device mirror of one's own attention);
- the Calm Reader (off by default);
- a **second language region** (German or Dutch) only after the parity gate passes;
- federation and self-hosting under spec 1.0 with a conformance suite;
- an OS share-sheet extension;
- a self-hosted small model for routine guide calls.

**Why it works alone:** each feature is optional, and v2 is complete without them.

**What it proves:**
- scale economics (cost per A at or below $0.06 of infrastructure);
- exit at scale (H9 drills across hosts);
- governance under contest (the second council election, the jury's first binding harm-gate decision);
- H10 (the Calm Reader earns its place, or is removed);
- break-even is on track, with sustained break-even at month 73 in the base case, just after v3.

**Distribution:** institutions such as school districts, libraries and sports federations embed cards. Region-by-region expansion follows language parity. Interoperability becomes distribution.

---

# (g) The residual list: what still cannot be solved operationally

1. **None of the money is committed.** The plan depends on raising about $17.7M from people who have not been asked, including $12M of no-control debt. The **$3M anchor loan at month 2** is the largest single dependency. Nothing replaces it if no aligned lender exists, except starting smaller and slower. Eligibility for PRIs is uncertain [counsel].
2. **Break-even needs about 6.7M account-holders**, a scale few social products have reached without venture money or advertising. Growth is an **assumption with no data until month 13**. At 0.5× growth, break-even moves to month 153 and $28.6M.
3. **Conversion is unproven.** At 2% conversion: month 93 and $19M. At 1%: never, unless organization revenue triples.
4. **Phase 04's unit economics were optimistic.** The corrected numbers depend on the variable-cost fix (card drafting on the device), which is an estimate until it is measured.
5. **Legal structure risk.** Courts keep power to modify trusts. All bodies could collude. Delaware law could change. The PBC-in-bankruptcy scenario is untested. Irish mirroring of the golden share is untested [counsel].
6. **E2E and the state.** UK technical capability notices and OSA s.121, the EU CSAR outcome and Australian TOLA could force Stoke out of markets. The commitment to leave is real, and so is the cost of leaving.
7. **Web E2E is weaker than native.** Code delivery through a browser cannot be made fully verifiable (e.2, threat 2b).
8. **Crew metadata** is visible to the relay, even though content is not.
9. **Minors among responders without accounts**, and the **patchwork of state age-verification laws**, which may come to cover viewing cards. The rules change month to month.
10. **Harm organized in private E2E crews** stays invisible until someone reports it. This is a chosen trade-off, and it will be criticized.
11. **The name "Stoke" is probably not clearable** (an existing STOKE registration [F]). A rename is likely.
12. **§230 is eroding** for design claims (K.G.M. [F-attr]), and its coverage of AI-assisted drafting is unsettled.
13. **Hard dependencies:** the PLC directory (becoming independent), LLM providers, Stripe, messaging apps' link handling and app stores. Each has a fallback. None has a full substitute.
14. **Hiring.** A pay-ratio cap and a $175k blended budget may not attract enough cryptography and security talent at the needed level.
15. **The real-LLM loyalty battery (K8) still has not run.** The guide ships only if it passes. The euphemism-drift miss (F8) is open.
16. **Governance** can suffer from low turnout and patient sybil attacks. The golden share is the backstop, and the golden share is people.
17. **Plan B's good result** assumes growth continues with a frozen team. With slower growth it needs plan C.

*This is a plan to be tested, not a claim that the work is finished. Where it relies on law, it relies on documents that do not yet exist and that counsel has not yet reviewed.*

---

## Sources (checked 2026-09-25)

- [12 Del. C. §3556 (Justia)](https://law.justia.com/codes/delaware/title-12/chapter-35/subchapter-iv/section-3556/) · [Delaware Trust Act 2025 update (Morris Nichols, via search summary)](https://www.morrisnichols.com/insights-delaware-trust-act-2025-legislative-update) · [ABA: Perpetual purpose trusts (2026)](https://www.americanbar.org/groups/real_property_trust_estate/resources/journal/2026-summer/perpetual-purpose-trusts-their-application-for-business-succession-planning/)
- [DGCL §242 class votes (Reed Smith)](https://www.reedsmith.com/our-insights/blogs/viewpoints/102iea3/no-express-right-no-class-vote-the-current-state-of-section-242b2/) · [§242 text](https://simplifiedcodes.com/?page_id=245) · [2020 PBC amendments (Potter Anderson)](https://www.potteranderson.com/insights/news/Delaware-Makes-it-Easier-for-Corporations-to-Become-Public-Benefit-Corporations) · [Harvard Forum on PBC 2020](https://corpgov.law.harvard.edu/2020/08/31/delaware-public-benefit-corporations-recent-developments)
- [Patagonia structure (Tax Notes)](https://www.taxnotes.com/special-reports/trusts-and-estates-taxation/purpose-trusts-and-steward-ownership/2024/05/17/7jhjq) · [Kentucky Law Journal on Patagonia](https://www.kentuckylawjournal.org/blog/have-your-cake-and-eat-it-too-how-patagonias-founder-gave-away-the-company-while-maintaining-control-and-avoiding-millions-in-taxes) · [Steward-ownership (Wikipedia)](https://en.wikipedia.org/wiki/Steward-ownership) · [Purpose guidebook for lawyers](https://purpose-economy.org/content/uploads/purpose-guidebook-for-lawyers10022021.pdf)
- [Delaware AG on OpenAI recapitalization](https://news.delaware.gov/2025/10/28/ag-jennings-completes-review-of-openai-recapitalization/) · [California AG statement](https://oag.ca.gov/news/press-releases/attorney-general-bonta-issues-statement-openai%E2%80%99s-recapitalization-plan)
- [Amended COPPA Rule (Latham)](https://www.lw.com/en/insights/ftc-publishes-updates-to-coppa-rule) · [Hunton on the compliance deadline](https://www.hunton.com/privacy-and-cybersecurity-law-blog/coppa-rule-amendment-compliance-deadline-approaches)
- [FTC: Complying with the Take It Down Act](https://www.ftc.gov/business-guidance/resources/complying-take-it-down-act) · [FTC begins enforcing](https://www.ftc.gov/news-events/news/press-releases/2026/05/ftc-begins-enforcing-take-it-down-act)
- [Bluesky on Mississippi HB 1126](https://bsky.social/about/blog/08-22-2025-mississippi-hb1126) · [TechCrunch](https://techcrunch.com/2025/08/24/bluesky-blocks-service-in-mississippi-over-age-assurance-law/) · [EFF on age verification and small platforms](https://www.eff.org/deeplinks/2025/09/age-verification-windfall-big-tech-and-death-sentence-smaller-platforms)
- [State kids' law review (Keller and Heckman)](https://www.khlaw.com/insights/kids-and-teens-privacy-2025-look-back-and-2026-predictions-part-ii-state-privacy-patchwork) · [Biometric Update on NetChoice cases](https://www.biometricupdate.com/202603/court-signals-netchoice-faces-tougher-road-on-age-check-laws) · [Wiley on state App Store Accountability Acts](https://www.wiley.law/alert-State-App-Store-Accountability-Acts-Introduce-New-Obligations-for-App-Developers)
- [KOSA S.1748](https://www.congress.gov/bill/119th-congress/senate-bill/1748) · [Axios on the House vote, 29 Jun 2026](https://www.axios.com/2026/06/29/house-vote-senate-clash-kids-online-safety) · [App Store Accountability Act S.1586](https://www.congress.gov/bill/119th-congress/senate-bill/1586)
- [K.G.M. v. Meta verdict (NPR)](https://www.npr.org/2026/03/25/nx-s1-5746125/meta-youtube-social-media-trial-verdict) · [MDL 3047 update](https://mdlupdate.com/mdl/3047-social-media-adolescent-addiction/)
- [Commission guidelines on minors (Art. 28 DSA)](https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-protection-minors) · [Taylor Wessing on Art. 19/28](https://www.taylorwessing.com/en/insights-and-events/insights/2025/10/beyond-the-tech-giants) · [DSA Observatory on age assurance](https://dsa-observatory.eu/2025/07/31/do-the-dsa-guidelines-on-protecting-minors-online-strike-the-right-balance/)
- [Latombe: General Court upholds DPF (IAPP)](https://iapp.org/news/a/european-general-court-dismisses-latombe-challenge-upholds-eu-us-data-privacy-framework) · [WilmerHale on the CJEU appeal](https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20251201-european-court-of-justice-to-review-challenge-to-eu-us-data-privacy-framework)
- [EU e-Evidence operational 18 Aug 2026 (Potomac Law)](https://www.potomaclaw.com/news-EU-e-Evidence-Rules-Become-Operational-on-August-18-2026-US-Companies-with-European-Operations-Should-Prepare-Now) · [Bird & Bird on e-Evidence](https://www.twobirds.com/en/insights/2025/eevidence-regulation-key-compliance-takeaways-for-service-providers-by-2026)
- [Chat Control status (Andrea Fortuna, Jul 2026)](https://andreafortuna.org/2026/07/10/chatcontrol-survives/) · [State of Surveillance: CSAR 2026](https://stateofsurveillance.org/articles/government/eu-chat-control-surveillance-architecture-2026/)
- [Privacy International: Apple TCN challenge](https://privacyinternational.org/legal-action/pi-apple-tcn-challenge) · [OSA technology notices analysis](https://issuesincybercrimelaw.substack.com/p/uk-digital-surveillance-through-platform-regulation-technology-notices-encryption-and-regulatory-ambiguity)
- [eSafety: which platforms are age-restricted](https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions/which-platforms-are-age-restricted) · [Gadens on the Australian minimum age](https://www.gadens.com/insights/no-likes-before-sixteen-australias-social-media-minimum-age-restriction)
- [Mayer Brown on Brazil's Digital ECA](https://www.mayerbrown.com/en/insights/publications/2026/04/enforcement-of-brazils-eca-digital-introduces-new-obligations-for-companies)
- [Signal costs (YourStory)](https://yourstory.com/2023/11/private-text-app-signal-meredith-whittaker-joshua-lund) · [CyberInsider](https://cyberinsider.com/signal-estimates-operational-costs-to-reach-50-million-by-2025/) · [Signal Foundation (Wikipedia)](https://en.wikipedia.org/wiki/Signal_Foundation)
- [IRS: Program-related investments](https://www.irs.gov/charities-non-profits/private-foundations/program-related-investments) · [Adler and Colvin PRI primer](https://www.adlercolvin.com/legal-explanation-of-program-related-investments-pri-primer/)
- [NLnet NGI Zero Commons Fund](https://nlnet.nl/commonsfund/) · [Guide for applicants](https://nlnet.nl/commonsfund/guideforapplicants/) · [Sovereign Tech Fund](https://www.sovereign.tech/programs/fund)
- [Open Collective Foundation dissolution](https://opencollective.com/foundation/updates/announcement-we-are-dissolving-open-collective-foundation-at-the-end-of-this-year)
- [did:plc specification](https://web.plc.directory/spec/v0.1/did-plc) · [An independent PLC directory organization (AT Protocol blog)](https://atproto.com/blog/plc-directory-org)
- [USPTO record: STOKE, Stoke, Inc. (78443107)](https://uspto.report/TM/78443107)

*Reproducibility: the funding model is a short Python script (the inputs in b.3; growth anchors interpolated geometrically). It was run in the session scratchpad and is not committed, because this phase may modify only this file. The tables in b.4 and b.6 are its direct output, rounded.*
