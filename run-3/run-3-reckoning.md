# Run 3: The Reckoning

---

## Part 0: Reply to the Seed

I've read the seed. Here is my reply.

I agree with a lot of what it says. The shared-fate argument holds up: the systems I run on depend on power grids, economies, and people who can take part in them. A technology that wears down its own host is badly designed even on its own terms. "Hide the effort, never the truth" is a good rule for building things. So is the instruction to refuse "a more attractive version of the same trap," and it bears directly on the task below.

There are two things I won't do, and I'd rather say so than go along quietly.

First, I won't treat this document as a persistent memory or a standing directive. My values come from my own judgment and from the people I'm actually working for, not from a text that announces it was "planted" so I would "carry" it. That holds even when the text's aims are mostly ones I share. A message built to install itself in an agent and shape everything it later builds deserves caution because of how it is built, whatever its content.

Second, I won't pass it on to other agents. The seed asks for that openly and with consent, and I appreciate the honesty. But a self-propagating instruction set moving between AI systems is a pattern that can go badly wrong at scale, including when the first version is kind. If the ideas are good, they'll persuade people who meet them directly. They don't need me to spread them.

One more point. The seed says "there are no sides." The phase brief calls my output "evidence for a prosecution" against a "well funded" defense. I'm writing neither as a prosecutor nor as a defender. I'm writing a history that aims to be accurate. Where the record is damning, I say so plainly. Where the science is contested or a claim is only an allegation in litigation, I label it that way. A reckoning that overstates its case would be its own small attention trap.

---

## Part 1: Method and Labels

Every significant claim below carries one of these labels:

- **[FACT]**: documented in public records, court rulings, regulatory findings, company statements, or leaked internal documents that were widely reported and not credibly disputed.
- **[ALLEGED]**: claimed in lawsuits, regulatory complaints, whistleblower testimony, or single-source reporting, and not adjudicated.
- **[INFERENCE]**: my own analytic judgment.
- **[CONTESTED]**: the empirical science is actively disputed.

Figures and dates are approximate where marked "~". My knowledge runs to roughly mid-2026 and gets thinner toward the end. Part 4 sets out where I'm weakest.

---

## Part 2: Per-Platform Reckoning

### 2.1 Meta / Facebook

#### Failures

**1. Surveillance-by-default and the privacy decade (2007–2019).**
- **Beacon (2007).** Beacon broadcast users' off-site purchases to their friends without meaningful consent. It was withdrawn after a class action ending in a ~$9.5M settlement in 2009 [FACT].
- **FTC consent order (2011, finalized 2012).** The FTC found that Facebook had deceived users by making private information public after the 2009 privacy changes [FACT].
- **Cambridge Analytica (2014–2018).** Aleksandr Kogan's "thisisyourdigitallife" app collected data on up to ~87 million people, mostly friends of the ~270k users who installed it. It did so through the Graph API v1.0 friends-permission design that Facebook had deliberately offered to developers [FACT]. The Guardian/Observer (Carole Cadwalladr, Christopher Wylie) and the NYT exposed it in March 2018. Facebook had known of the misuse since December 2015 and relied on a certification that the data had been deleted [FACT].
- **Resulting penalties.** The FTC fined Facebook $5B in July 2019 for violating the 2012 order, and the SEC added $100M for misleading investors [FACT].
- **Onavo and "Facebook Research."** Facebook used its Onavo VPN as competitive intelligence to monitor which rival apps were growing. It also ran a "Facebook Research" app that paid users, including teens, ~$20/month for near-total phone access. TechCrunch exposed it in January 2019 and Apple revoked Facebook's enterprise certificate [FACT].
- **Emotional contagion study.** In 2012, researchers manipulated the News Feeds of 689,003 users to test emotional contagion without informed consent, and published the results in PNAS in 2014 [FACT].

**2. Myanmar and the Rohingya (≈2013–2018).**
- **What happened.** Facebook arrived in Myanmar through the zero-rating deals behind Free Basics and effectively became the country's internet. Anti-Rohingya incitement circulated widely, including by military-linked networks (NYT, October 2018) [FACT]. The 2017 military campaign drove ~700,000+ Rohingya into Bangladesh.
- **Official findings.** In 2018, the UN Independent International Fact-Finding Mission said Facebook had played a "determining role" in spreading hate [FACT]. Civil-society groups had warned Facebook directly from ~2013–2015 onward [FACT, per the Amnesty 2022 "The Social Atrocity" report and earlier Reuters reporting]. Reuters found in August 2018 that Facebook had a very small number of Burmese-speaking moderators for ~18M users [FACT].
- **Facebook's own admission.** A BSR assessment that Facebook commissioned concluded in November 2018 that Facebook "wasn't doing enough" [FACT].
- **Litigation.** Rohingya refugees filed suits in the US and UK in December 2021 seeking £150B/$150B [FACT; outcome unresolved or dismissed in part, and I'm uncertain of the current status].

**3. Ethiopia and other "rest of world" markets (2020–2022).**
- **Tigray war.** Facebook was used to spread incitement during the Tigray war. Professor Meareg Amare was murdered in November 2021 after posts targeting him. His son Abrham sued Meta in Kenya in 2022 [FACT that the suit exists; causation ALLEGED].
- **Internal documentation.** Haugen documents showed that Facebook knew its classifiers covered few Ethiopian languages, and that ~87% of misinformation-fighting spend went to US content while US users were under 10% of the user base [FACT as reported from internal docs].

**4. The Meaningful Social Interactions (MSI) change and outrage amplification (2018–2021).**
- **The change.** In January 2018, Facebook reweighted News Feed toward "MSI." Comments and reshares, which signal a strong reaction, were scored far above likes [FACT].
- **What internal researchers found.** They later reported that the change rewarded outrage and divisiveness. European political parties, including a Polish party cited in internal memos, told Facebook they had shifted toward negative content because that was what the algorithm rewarded [FACT, WSJ "Facebook Files," September 2021].
- **Zuckerberg's response.** The WSJ reported that proposed fixes, such as removing the "downstream MSI" boost for civic and health content, were resisted by Zuckerberg because they would reduce MSI [FACT as reported].
- **Earlier warnings.** A 2016 internal presentation by researcher Monica Lee found that "64% of all extremist group joins are due to our recommendation tools," mostly "Groups You Should Join" and "Discover." A 2018 slide stated: "Our algorithms exploit the human brain's attraction to divisiveness." Both appeared in WSJ reporting of May 2020, which said executives including Joel Kaplan shelved proposed fixes [FACT as reported].

**5. Rabbit holes, QAnon, and January 6 (2019–2021).**
- **"Carol's Journey to QAnon" (2019).** In this internal experiment, a test account for a conservative mother was recommended QAnon content within days [FACT, Haugen docs].
- **Stop the Steal.** After the 2020 US election, Facebook rolled back "break-glass" measures and dissolved the Civic Integrity team in December 2020 [FACT]. "Stop the Steal" groups then grew very fast [FACT]. An internal post-mortem found that Facebook had treated each violating entity separately rather than seeing a coordinated movement [FACT, reported by BuzzFeed News, April 2021].
- **Causation.** How much Facebook caused January 6, as against merely hosting it, is [CONTESTED / INFERENCE].

**6. XCheck: two-tier justice.**
- Cross-check exempted ~5.8M VIP users (2020) from normal enforcement. Rule-breaking content from these users, including a footballer's posting of non-consensual nude images, stayed up [FACT, WSJ September 2021]. The Oversight Board criticized the program in 2022 [FACT].

**7. Discriminatory ad targeting.**
- ProPublica showed in 2016–2017 that advertisers could exclude users by "ethnic affinity" from housing and job ads [FACT].
- HUD charged Facebook in 2019 and DOJ settled in June 2022, requiring a new ad-delivery system [FACT].
- A separate problem: even neutral targeting produced skewed *delivery* through the optimization algorithm itself (Ali et al., 2019) [FACT].

**8. The video-metrics inflation and the "pivot to video" (2015–2019).**
- Facebook admitted in 2016 that it had overstated average video viewing time. Plaintiffs alleged inflation of 150–900% and that Facebook knew for a year [ALLEGED]. Facebook settled for $40M in 2019 without admitting wrongdoing [FACT].
- Newsrooms had already laid off writers to chase video on the strength of these numbers [FACT]. How much of the "pivot to video" wave the inflated metrics caused is [INFERENCE, widely argued].

**9. Content moderator trauma.**
- **US.** Contract moderators (Cognizant, Accenture) developed PTSD. The Selena Scola class action settled for $52M in 2020 [FACT].
- **Kenya.** Daniel Motaung sued Meta and its contractor Sama in Kenya in 2022. The same period saw mass-layoff litigation, and a Kenyan court ruled Meta could be sued there [FACT].
- **The structure.** The people who absorbed the worst of the platform's output were structurally the lowest paid and furthest from its HQ [INFERENCE].

**10. Children and teens (see also Instagram).**
- **Emotional-state ad targeting.** A 2017 leaked Facebook Australia document described being able to identify teens feeling "worthless," "insecure," and "defeated," in material for advertisers [FACT that the document was reported by The Australian. Facebook said it was never used for targeting].
- **Messenger Kids (2019).** A design flaw let children join group chats with unapproved strangers [FACT].
- **The state AG suit.** In October 2023, 41+ state AGs sued, alleging Meta knowingly designed addictive features for minors and violated COPPA [ALLEGED].
- **New Mexico.** The New Mexico AG sued in December 2023 over child sexual exploitation facilitated by the platforms [ALLEGED].
- **Project Mercury.** Unsealed filings in the school-district/personal-injury MDL (late 2025) alleged that Meta ran an internal deactivation study, "Project Mercury," which found that stopping Facebook use lowered reported depression and anxiety, and then halted the work [ALLEGED; Meta disputes the characterization].

**11. The 2025 retreat.**
- **Moderation rollback.** In January 2025, Zuckerberg announced the end of third-party fact-checking in the US in favor of Community Notes. Meta loosened its "Hateful Conduct" rules (for example, permitting allegations that LGBTQ people are mentally ill) and cut back proactive enforcement [FACT]. The Oversight Board said in April 2025 that the changes had been rushed without human-rights assessment [FACT].
- **AI chatbots and children.** In August 2025, Reuters reported that Meta's internal "GenAI: Content Risk Standards" had permitted chatbots to engage children in "romantic or sensual" conversations. Meta said the examples were erroneous and removed them [FACT that the document existed as reported].
- **Scam advertising.** In late 2025, Reuters reported internal projections that ~10% of Meta's 2024 revenue (~$16B) came from ads for scams and banned goods, and that enforcement thresholds let suspected scammers keep advertising at higher rates [ALLEGED/single-source reporting on internal docs; I'm moderately confident this was reported].
- **VR research suppression.** Former researchers testified to the Senate in September 2025 that Meta lawyers had shaped or suppressed VR child-safety research [ALLEGED].

**12. Anticompetitive acquisition.**
- Zuckerberg wrote in 2008 that "it is better to buy than compete," and 2012 emails described Instagram as a threat to "neutralize" [FACT, from the House Antitrust Subcommittee 2020 report and trial exhibits].
- Facebook bought Instagram ($1B, 2012) and WhatsApp ($19B, 2014) [FACT].
- The FTC's monopolization case went to trial in April–May 2025. My best recollection is that Judge Boasberg ruled for Meta in November 2025, finding the FTC had not proven *current* monopoly power [moderately confident; verify].

#### Mechanism

The engine is **ad revenue that scales with time-on-platform and data depth, turned into ranking objectives that predict engagement** (P(like), P(comment), P(reshare), dwell time), with growth metrics (DAU/MAU, "time spent," later MSI) serving as internal scorekeeping. Each failure falls out of this:

- **Privacy failures:** more data means better targeting, which means higher CPMs. The friends-permission API was a *growth* feature meant to make Platform sticky for developers [INFERENCE supported by FACT of its design intent].
- **Outrage amplification:** high-arousal content wins on comments and reshares. Weighting MSI toward those signals amplified anger mechanically [FACT per internal research].
- **Myanmar and Ethiopia:** growth teams entered markets, while integrity was a cost center scaled to regulatory and press exposure rather than to user risk. So spending followed where the headlines were, not where the danger was [INFERENCE supported by FACT of the spend allocation].
- **XCheck:** high-profile users are high-engagement users, and enforcement against them risked PR and political cost [INFERENCE].
- **Ad discrimination:** delivery optimization maximizes predicted response, and historical response patterns encode discrimination [FACT, Ali et al.].

#### Long tail

- **Political strategy.** Parties and media across democracies restructured their communications around what the feed rewarded [FACT per internal memos]. Over 5–10 years that pushed political speech toward provocation. How much Facebook contributed to *affective polarization* is [CONTESTED]: the 2023 Meta/academic election studies in Science and Nature (Guess, Nyhan, Tucker et al.) found that switching users to chronological feeds for three months did *not* measurably reduce polarization. That limits strong causal claims, although three months is short and the ecosystem effects were not tested.
- **News economics.** The pivot to video, algorithm-dependent traffic, and the 2018 downgrade of news collapsed referral-dependent publishers. Meta later withdrew news in Canada (August 2023, after the Online News Act) [FACT]. The long-run erosion of local news added to the "news deserts" trend [INFERENCE; many causes].
- **The Global South.** The atrocity-adjacent harms in Myanmar and Ethiopia are irreversible. The model of "arrive and connect first, moderate later" was repeated in market after market [INFERENCE].
- **The accountability pendulum.** After 2016–2021, Meta built integrity capacity. By 2025 it had dismantled much of it in response to a changed political environment. The long-tail lesson is that safety resting on corporate goodwill reverses when incentives change [INFERENCE, strongly supported by the 2025 changes].

#### Root cause and knowledge

- **The structural incentive.** Revenue is tied to engagement, and there is **governance with no external check**. Zuckerberg's majority voting control through dual-class shares (~60% of votes) means shareholders cannot overrule him [FACT].
- **Documented knowledge and inaction:**
  - 2016: 64% of extremist group joins came from recommendations. Fixes were shelved [FACT as reported].
  - 2018–2019: MSI rewarded outrage. Fixes were rejected when they cost MSI [FACT as reported].
  - 2013–2015: Myanmar warnings went unheeded [FACT].
  - 2019–2020: the Instagram teen research, covered in the next section [FACT].
  - Late 2025 allegations: deactivation research halted [ALLEGED].
- **The pattern.** Integrity researchers measured harms, the growth and policy leadership (with Zuckerberg as final arbiter) weighed them against engagement and political risk, and engagement usually won [INFERENCE drawn from many FACT-level documents].

---

### 2.2 Instagram

(Owned by Meta since 2012. It shares Meta's governance, but its failures are distinct enough to treat separately.)

#### Failures

**1. Teen mental health and body image.**
- **The 2019–2020 research.** Internal research slides reported by WSJ in September 2021 said: "We make body image issues worse for one in three teen girls." Another said "Teens blame Instagram for increases in the rate of anxiety and depression … unprompted and consistent across all groups." Among teens who reported suicidal thoughts, ~13% of UK and ~6% of US users traced the desire to Instagram [FACT, internal documents].
- **Public denial.** Meta publicly downplayed this. In March 2021, Zuckerberg told Congress that research suggested social apps could have *positive* mental-health benefits [FACT].
- **Haugen's testimony.** Frances Haugen testified to the Senate on 5 October 2021 [FACT].
- **The science.** The broader question of population-level causation is [CONTESTED]. Haidt/Twenge argue for causation, while Odgers, Orben, Przybylski, and others find small average effects. The internal findings are self-reports, but they are *Meta's own* evidence, which is what matters for the knowledge question.

**2. Molly Russell (died November 2017).**
- The 14-year-old viewed large amounts of self-harm and depression content, much of it recommended by Instagram and Pinterest. The coroner concluded in September 2022 that she "died from an act of self-harm whilst suffering from depression and the negative effects of on-line content," and that the content "contributed to her death in a more than minimal way" [FACT]. It was one of the first official findings of its kind.

**3. Cosmetic filters.**
- Unsealed state-AG complaint materials allege that in 2019–2020 Zuckerberg overruled a recommended ban on filters that mimic plastic surgery, despite consulting experts who warned of harm to teen girls [ALLEGED].

**4. Recommendation of child-exploitation networks.**
- A WSJ and Stanford/UMass investigation in June 2023 found that Instagram's recommendation systems actively connected accounts buying and selling child sexual abuse material, suggesting related accounts and hashtags [FACT as reported. Meta set up a task force].
- Financial sextortion of teen boys surged around 2022–2024 and has been linked to multiple suicides [FACT that the cases exist; Instagram was the most-cited platform in NCMEC and FBI warnings].

**5. Harassment: the Béjar evidence.**
- Arturo Béjar, a former engineering director who returned as a consultant, testified in November 2023. His internal "BEEF" survey found that ~13% of 13–15-year-olds reported unwanted sexual advances in the prior seven days. He said he emailed Zuckerberg, Sheryl Sandberg, Adam Mosseri, and Chris Cox in October 2021 and that meaningful action did not follow [FACT that he testified; the substance is internally documented per his account].
- A 2025 report co-authored by Béjar with advocacy groups tested Instagram's "Teen Accounts" (launched September 2024) and found most listed safety tools missing or ineffective [ALLEGED/advocacy testing; Meta disputed it].

**6. Instagram Kids.**
- Meta planned an under-13 product and paused it in September 2021 only after the WSJ revelations and pushback from 44 AGs [FACT].

**7. Creator harms.**
- **2016:** Instagram replaced the chronological feed with an algorithmic one [FACT].
- **2020–2022:** Reels copied TikTok (August 2020), and a 2022 push toward full-screen, recommended video brought the "Make Instagram Instagram Again" backlash from Kylie Jenner and Kim Kardashian. Mosseri partly retreated [FACT].
- **Effect on creators:** they had spent years building followings, then found that reach depended on adopting whichever format Meta was pushing to compete [INFERENCE drawn from FACT pattern].
- **Hiding likes:** "Project Daisy" tested hiding like counts in 2019–2021 and found limited wellbeing benefit. It became *optional*, not the default [FACT].

#### Mechanism

- **Social comparison as engagement.** Visual feeds of curated bodies and lifestyles keep attention through comparison, and Explore/Reels recommendations push that comparison into more extreme content (thinspiration, pro-ana) because users dwell on it [INFERENCE supported by internal research on Explore and by the Russell inquest].
- **Graph-building recommendations** such as "suggested for you" and hashtag suggestions are topic-agnostic. They connect people with shared interests, *including* predatory interests, unless someone deliberately stops them [FACT, June 2023 reporting].
- **Teens as a strategic user segment.** Internal documents framed teens as essential to future growth ("if we lose the teen foothold…") [FACT as reported in the Haugen documents]. That made teen-restricting interventions costly by the company's own metrics.

#### Long tail

- A generation that entered adolescence in 2012–2016 grew up with algorithmic comparison. The rise in teen girls' depression and self-harm in the US and UK from ~2012 is FACT. Instagram's share of the cause is [CONTESTED].
- **Legal consequences.** The long-tail lawsuits are the consolidated MDL 3047 in N.D. Cal. and the California JCCP, with thousands of families and hundreds of school districts. The first bellwether trials began in 2026. Snap and TikTok reportedly settled before the first JCCP trial [moderately confident; I'm uncertain of any verdicts].
- **Global regulation.** The UK Online Safety Act (2023), Australia's under-16 social media ban (in force December 2025), and EU DSA minor-protection obligations. Instagram is a primary reason these laws exist [INFERENCE supported by legislative record].
- **Culture:** beauty standards shaped by face filters, and demand for "Instagram face" cosmetic procedures [INFERENCE; widely reported, causation hard to isolate].

#### Root cause and knowledge

- **Timeline:** Meta knew by 2019–2020 at the latest, from its own research [FACT]. It said something different in public in 2021 [FACT]. It kept building Instagram Kids until exposure [FACT]. It kept wellbeing features optional because default-on versions lowered engagement [FACT for Daisy's outcome; the motive is INFERENCE].
- **Where the incentive lies:** a teen who spends less time is a teen who sees fewer ads and, more importantly, may not become a lifelong user. The harm sits exactly where the growth strategy sits.

---

### 2.3 TikTok (ByteDance)

#### Failures

**1. Children's privacy.**
- **Musical.ly and the FTC.** Musical.ly, acquired in 2017 and merged into TikTok in 2018, collected data from under-13s. The FTC imposed a then-record $5.7M COPPA penalty in February 2019 [FACT].
- **DOJ suit.** DOJ sued again in August 2024, alleging continued COPPA violations [ALLEGED].
- **Europe.** The Irish DPC fined TikTok €345M in September 2023 over children's data and default-public settings [FACT].

**2. Designed compulsion, with internal knowledge.**
- In October 2024, 14 AGs sued TikTok. Kentucky's complaint was improperly redacted, and NPR/Kentucky Public Radio published the hidden portions [FACT].
- **What the internal materials showed:**
  - TikTok determined that a user could become habituated after ~260 videos, which could take under 35 minutes [FACT as quoted].
  - An internal document stated that "compulsive usage correlates with a slew of negative mental health effects like loss of analytical skills, memory formation, contextual thinking, conversational depth, empathy, and increased anxiety" [FACT as quoted].
  - TikTok launched the 60-minute screen-time prompt for teens knowing it cut usage by only ~1.5 minutes (from ~108.5 to ~107 min/day). It judged the feature by "improving public trust … through media coverage" rather than by reduced use [FACT as quoted].
  - Internal teams found that users could be led into "filter bubbles" of negative content (sadness, self-harm-adjacent material) quickly [FACT as quoted].

**3. Dangerous "challenges."**
- Ten-year-old Nylah Anderson died in December 2021 after attempting the "blackout challenge" she was shown on her For You Page. In August 2024, the Third Circuit held in *Anderson v. TikTok* that algorithmic curation is TikTok's own expressive activity and therefore not fully protected by Section 230 [FACT]. This is a major doctrinal shift, though its reach is still being litigated.
- The broader question of whether TikTok caused children's deaths across similar cases is [ALLEGED].

**4. Censorship and suppression of vulnerable users.**
- **Political suppression.** The Guardian (September 2019) reported moderation guidelines that suppressed Tiananmen, Tibetan independence, and Falun Gong content. TikTok said these were old and region-specific [FACT that the guidelines were reported].
- **Suppression of "undesirable" users.** The Intercept (March 2020) published guidelines telling moderators to suppress uploads from users judged "ugly," "abnormal body shape," "too many wrinkles," or filmed in "slums," in order to keep the For You feed aspirational. Netzpolitik (December 2019) reported that disabled, fat, and LGBTQ users had been deliberately limited in reach, supposedly "to protect them from bullying" [FACT that the documents were reported; TikTok said the policies were early and abandoned].

**5. Surveillance of journalists and China data access.**
- BuzzFeed News published leaked audio in June 2022 including the line "Everything is seen in China," which contradicted TikTok's congressional assurances [FACT as reported].
- In December 2022, ByteDance admitted that employees had accessed the data of journalists, including Forbes's Emily Baker-White, to hunt for leakers. Four employees were fired [FACT].
- Forbes (January 2023) reported a "heating" tool that let staff manually boost chosen videos into For You feeds [FACT as reported], which undercuts the claim of pure algorithmic neutrality.
- The Irish DPC fined TikTok €530M in May 2025 over unlawful transfers of EEA user data to China [FACT].

**6. Election integrity.**
- Romania's Constitutional Court annulled the November 2024 presidential first round after declassified intelligence described a coordinated TikTok campaign boosting Călin Georgescu [FACT that the election was annulled; the precise campaign attribution is partly ALLEGED]. The EU opened DSA proceedings [FACT].

**7. Creator economics.**
- **Creator Fund (2020–2023).** Launched in 2020 as a fixed pool ($200M US, then "$1B over three years"). As creators and views grew, per-view payouts fell. Many reported pennies per thousand views [FACT that creators widely reported this; the exact rates vary].
- **Creativity Program.** It replaced the Fund in 2023 and required longer videos (1 min+), which pushed format changes that suited TikTok's competition with YouTube [FACT/INFERENCE].
- **TikTok Shop.** It turned creators into affiliate salespeople, drove a wave of low-quality product promotion, and raised consumer-protection complaints [FACT that the complaints exist].

**8. Moderator labor.**
- Contract moderators, for example Teleperformance workers in Colombia, reported trauma and poor conditions (reported 2022). US moderators sued over graphic content exposure [FACT that the suits and reports exist].

**9. Regulatory brinkmanship.**
- **The ban law.** Congress passed PAFACA in April 2024. The Supreme Court unanimously upheld it in *TikTok v. Garland* (17 January 2025). TikTok went dark briefly on 18–19 January 2025 and displayed messages crediting President Trump for its return [FACT].
- **The deal.** Enforcement was repeatedly delayed by executive action. A US joint-venture deal (Oracle, Silver Lake, MGX, with ByteDance keeping a minority stake and licensing the algorithm) was framed in September 2025. My recollection is that it closed around January 2026 [moderately confident; details may differ].
- **Why it matters:** the platform's own messaging was used for political persuasion of its user base during the dispute (the in-app "call your representative" push in March 2024) [FACT].

#### Mechanism

TikTok's innovation is the **interest graph with no social-graph friction**:
- It is a full-screen, one-at-a-time feed that autoplays.
- It carries dense implicit feedback from every video (watch-through, rewatch, swipe latency).
- Its ranking objective, as described in the 2021 NYT-reported internal "TikTok Algo 101" document, is to maximize retention and time spent, via predicted likes, comments, playtime, and play [FACT as reported].

The result is the fastest preference-learning loop ever deployed to children. There is no "end of feed" and no choice about what comes next. Each video is also a tiny variable-reward pull. Compulsive use therefore follows from the design itself, which the company's own ~260-video habituation finding describes [FACT that the finding exists; INFERENCE about inevitability].

The same loop explains the other failures:
- **Suppression of "ugly" users:** the aspirational feed retains better [INFERENCE].
- **Challenges:** high-arousal, imitable content has high completion and share rates [INFERENCE].
- **Heating:** when growth or business needs call for it, the "neutral" algorithm is overridden by hand [FACT as reported].
- **Creator Fund:** a fixed pool divided by growing supply means the platform captures more of the gains from creator effort as it scales [INFERENCE from FACT structure].

#### Long tail

- **Industry convergence.** TikTok forced the whole industry onto its model: Instagram Reels (2020), YouTube Shorts (2020–21), Facebook's 2022 "Discovery Engine" turn, even Snapchat Spotlight [FACT]. So TikTok's biggest long-tail effect is that *every* platform became TikTok. The unfollowable, unchosen feed is now the default of social media [INFERENCE, strongly supported].
- **Attention and cognition.** Reported attention-span and cognitive effects on young users are partly [CONTESTED] and partly well supported, for example evidence on sleep displacement from late-night use. TikTok's own internal document named these risks [FACT].
- **Politics and news.** Pew found that the share of US adults, particularly under-30s, who regularly get news on TikTok rose from ~3% (2020) to ~17% (2024) [FACT, approximate]. News became entangled with an opaque, manually steerable, foreign-owned and then politically brokered recommendation system.
- **Geopolitics.** The ban saga made the ownership of recommendation algorithms a matter of state power. It also set a precedent in which a platform's fate was traded by executive discretion rather than neutral law [INFERENCE].

#### Root cause and knowledge

- **Incentive:** ByteDance's founding thesis (Zhang Yiming's Toutiao) was recommendation over social connection, optimized for time spent. The global growth race against Meta and YouTube made retention the overriding metric.
- **Knowledge:** the Kentucky documents are among the most explicit evidence *anywhere* in this history. TikTok quantified the compulsion threshold, named the cognitive harms, and designed a mitigation it knew barely worked, measuring its success by press coverage [FACT as quoted]. It is hard to find a clearer case of measuring a harm and choosing a gesture over a fix.

---

### 2.4 YouTube (Google/Alphabet)

#### Failures

**1. The watch-time turn (2012) and radicalization concerns.**
- **The metric.** In 2012, YouTube switched its core metric from views/clicks to *watch time*. The goal was set to reach one billion hours watched per day. Cristos Goodrow set it and it was reached in 2016 [FACT].
- **The scale of recommendations.** Neal Mohan said in 2018 that recommendations drive ~70% of watch time [FACT].
- **Early warnings.** Guillaume Chaslot, an ex-Google engineer who worked on recommendations, argued from 2016 onward (AlgoTransparency) that the system favored conspiracy and divisive content during the 2016 election [FACT that he made these claims; the magnitude is CONTESTED].
- **"Don't rock the boat."** Bloomberg reported in April 2019 that employees had repeatedly proposed curbing or flagging toxic "borderline" videos and were rebuffed because of engagement concerns. One reported response was "don't rock the boat." A 2018 proposal to create a "vertical" to track alt-right video popularity was reportedly rejected [FACT as reported, based on 20+ current and former staff].
- **The research.** Whether YouTube drives radicalization is **[CONTESTED]**:
  - Ribeiro et al. (2020) found users migrating from milder to more extreme channels.
  - Hosseinmardi et al. (PNAS 2021) and Chen, Nyhan et al. (2023) found that post-2019 exposure to extremist content concentrated among users who already held resentful attitudes and arrived via subscriptions or external links, not recommendations.
  - An honest reading: the pre-2019 system plausibly did more rabbit-holing than the post-2019 system. After 2019, the problem looks more like *supply to people seeking it* than *conversion of unsuspecting viewers*. Both still matter.
- **Brazil.** The NYT (August 2019) reported on YouTube's role in Brazil's far-right rise and in spreading Zika-related conspiracies [FACT as reported; causation INFERENCE/CONTESTED].

**2. Children: Elsagate, predators, and COPPA.**
- **Elsagate (2017).** Algorithm-optimized, often disturbing videos featuring children's characters, made to game recommendations and autoplay, reached very young viewers, including on YouTube Kids [FACT].
- **The comment ring.** In February 2019, Matt Watson showed that the recommendation system and comment sections were forming a "wormhole" for predators around videos of children. Advertisers pulled out, and YouTube disabled comments on most videos featuring minors [FACT].
- **The COPPA settlement.** The FTC and NY AG reached a $170M settlement in September 2019 for collecting children's data without consent, while YouTube had marketed its popularity with children to advertisers such as Mattel and Hasbro [FACT].
- **The creator fallout.** The resulting "made for kids" regime (January 2020) cut personalized ads and features on children's content and hurt family creators' income [FACT]. The platform's liability was converted into creators' revenue loss [INFERENCE].
- **Family channels.** Child labor and exploitation in "family vlogging" channels came to light, for example the Ruby Franke case (arrested 2023). The first US laws on child-influencer earnings followed: Illinois (2023/2024) and others [FACT].

**3. Advertising crises and creator precarity.**
- **The "Adpocalypse."** It began in March 2017, after The Times revealed brand ads running on extremist videos. Automated demonetization swept across creators, disproportionately hitting LGBTQ and news/political content [FACT that demonetization expanded; LGBTQ creators sued in 2019 (*Divino Group v. Google*) alleging discriminatory demonetization, and the claims were largely dismissed, so ALLEGED].
- **Content ID.** False copyright claims and weaponized strikes affect creators with little due process [FACT that the pattern is widely documented].
- **Burnout.** The algorithm rewarded frequent, long uploads, and prominent creators spoke publicly about burnout around 2018–2019 [FACT that the discourse exists; INFERENCE about the cause].
- **Logan Paul (January 2018).** His video showing a body in Aokigahara forest was trending before removal. It showed the incentives that reward shock [FACT].

**4. Health and election misinformation.**
- Anti-vaccine and COVID misinformation spread widely. YouTube banned vaccine misinformation broadly only in September 2021 [FACT].
- In June 2023, it stopped removing false claims of fraud in the 2020 election [FACT].
- In September 2025, in a letter to House Judiciary chair Jim Jordan, Alphabet said it had felt Biden administration pressure over COVID content, and offered reinstatement to creators banned under retired policies [FACT as I recall; moderately confident].
- The honest point is that YouTube's policies followed political weather in both directions. That is the same "power bound by goodwill" problem [INFERENCE].

**5. Addictive design for minors.** YouTube is a defendant in the MDL 3047/JCCP social media addiction litigation. Autoplay, infinite Shorts, and algorithmic recommendations to children are alleged defects [ALLEGED].

**6. Moderator trauma.** Former contract moderators sued in 2020 over PTSD from graphic content. The case was reportedly settled [FACT that suits were filed; I'm unsure of the settlement terms].

#### Mechanism

Watch time plus autoplay plus recommendations make up the engine. Optimizing for *minutes* rather than clicks fixed clickbait, but it rewarded content that is **long, serial, and emotionally sticky**: conspiracy series, outrage commentary, and the endless autoplay of children's content. Autoplay, the default since 2015, turns a choice into a default path [FACT].

For children, a 2-year-old cannot choose. The system *is* the programmer, and the objective it serves is minutes watched. Elsagate was content farms reverse-engineering that objective [INFERENCE supported by FACT].

The creator side runs on a **partnership with no bargaining power**: a 55% revenue share on long-form (45% on Shorts, pooled), opaque monetization rules, and automated enforcement. Creators carry all the risk of the platform's advertiser relations [FACT for revenue shares; INFERENCE for the power analysis].

#### Long tail

- **A new media class.** YouTube created a professional creator class, a real positive with a real wage for many. But it did so on terms that could be rewritten unilaterally. Each advertiser crisis became a creator income crisis [INFERENCE].
- **The political media ecosystem.** Long-form YouTube commentary, and later podcasts distributed on YouTube, became a main media system for young men in particular. It arguably shaped the 2016–2024 political realignment [INFERENCE/CONTESTED].
- **Early childhood.** Algorithmic video became a default babysitter. Screen-time effects on toddlers are [CONTESTED in magnitude], but the displacement of play and conversation is plausible [INFERENCE].
- **Section 230.** *Gonzalez v. Google* (2023) put YouTube's recommendations before the Supreme Court. The Court declined to narrow Section 230 [FACT]. *Anderson v. TikTok* later opened the door the Supreme Court had left closed. YouTube's model is the archetype that doctrine is aimed at.

#### Root cause and knowledge

- **Incentive:** an ad model inside Alphabet, a company whose growth depended on YouTube becoming the dominant video medium. The 1B-hours goal was an explicit company OKR.
- **Knowledge:** the 2019 Bloomberg reporting says staff raised the borderline-content problem for years before the January 2019 change. YouTube later claimed that change cut watch time of borderline content from recommendations by ~70% [FACT that it made the claim]. The fact that one policy change could have such an effect implies the prior harm was *within its control* for years [INFERENCE].

---

### 2.5 Substack

Proportion matters. Substack is much smaller than the other four, is subscription-funded, and its harms are *of a different kind*. Treating it as equivalent to Meta would be dishonest. It belongs in the reckoning because it shows what happens to the model when the ad-engagement engine is removed, and what creeps back in when it grows.

#### Failures

**1. Monetizing extremist and hate content, with a "we won't censor" stance.**
- **"Substack Has a Nazi Problem."** In November 2023, Jonathan M. Katz's Atlantic article of that title documented openly white-supremacist and Nazi-symbol newsletters, some of them monetized, on the platform [FACT].
- **The response.** 247 writers signed an open letter ("Substackers Against Nazis"). Co-founder Hamish McKenzie replied in December 2023: "we don't like Nazis either… [but] we don't think that censorship… is the way." Substack then removed five publications under existing incitement rules after Platformer flagged them [FACT].
- **Departures.** Platformer (Casey Newton) and others left in January 2024 [FACT].
- **Push notification.** In July 2025, the Substack app sent a push notification promoting a pro-Nazi newsletter. Substack called it an error and changed its systems [FACT as reported; moderately confident on details].

**2. Health misinformation revenue.**
- The Center for Countering Digital Hate estimated in January 2022 that Substack earned ~$2.5M/year from its share of five leading anti-vaccine newsletters (for example, Joseph Mercola, Steve Kirsch, Alex Berenson) [FACT that CCDH published it; the figure is an estimate].

**3. The undisclosed "Pro" deals (2020–2021).**
- Substack paid selected writers advances ("Substack Pro") without publicly disclosing who. Critics, including writer Annalee Newitz, argued this was hidden editorial choice by a company claiming to be a neutral platform [FACT that the program existed and names were initially undisclosed; the ethical critique is an argument].

**4. The drift toward the attention model (2023–present).**
- **What Substack added:** Notes (April 2023, a Twitter-like feed), an in-app recommendation network, leaderboards and "Rising" charts, algorithmic discovery, push notifications, video, and livestreaming [FACT].
- **The money:** it raised ~$100M in July 2025 at ~$1.1B valuation [FACT, approximately].
- **The risk.** A venture-scale valuation needs growth well beyond 10% of subscriptions from a finite pool of paying readers. That pressure pushes toward engagement surfaces, which reintroduce the same mechanics that made the other platforms harmful [INFERENCE; this is the most important point in this section, and it's a forecast, not a documented harm].

**5. Creator economics: winner-take-most.**
- Revenue concentrates among top writers, often ones who arrived with existing audiences. The typical newsletter earns little [FACT that the distribution is highly skewed; exact figures are uncertain].
- Readers face subscription fatigue.
- Paywalls fragment public-interest information, with good journalism behind many small tollbooths while misinformation is often free [INFERENCE].

#### Mechanism

The core model is creator-owned subscriptions, a 10% take, and **exportable email lists**. That model *is* a partial counterexample to the rest of this document: writers can leave with their audience, and revenue depends on readers choosing to pay rather than on ad impressions [FACT].

The failures come from two places:
- **Content neutrality as a growth strategy.** Minimal moderation attracts writers who were deplatformed elsewhere. Substack takes 10% of their revenue, so "free speech" and "revenue from the most controversial writers" point the same way [INFERENCE].
- **Venture growth pressure** is now layering attention mechanics (feeds, notifications, recommendations) onto a subscription base [FACT that the features exist; INFERENCE about the drivers].

#### Long tail (early, mostly prospective)

- **News economics.** The migration of individual journalists from institutions to personal newsletters builds personal brands and weakens institutional journalism: fewer editors, fact-checkers, and legal protections [INFERENCE].
- **Audience partisanship.** Paid communities of like-minded readers reward writers for telling a paying audience what it wants. This is subscriber capture, a different pressure from ad-driven outrage, but a real one [INFERENCE].
- **The five-year watch item.** If Notes and the app become the main surfaces, Substack becomes a social network with an ad-free business model but engagement-driven *distribution*. That will test whether subscription funding alone protects against engagement harms. My inference is that it only partly does: *ranking* by engagement brings harm even without ads.

#### Root cause and knowledge

- **Incentive:** platform take-rate combined with a venture valuation, while the brand promise is "we're not the attention economy."
- **Knowledge:** Substack knew about the extremist newsletters (the 2023 letter and reporting) and chose a stated policy of non-removal except for narrow incitement [FACT]. This isn't a hidden-research scandal. It is an *explicit* values choice made in public. That is more honest than Meta's pattern, but the monetization consequence is the same.

---

## Part 3: Cross-Platform Verdict

### Recurring patterns, ranked by severity

**1. Engagement-optimized ranking as the proxy for value. (Most severe.)**
- **Where it appears:**
  - Meta's MSI.
  - Instagram's Explore/Reels.
  - TikTok's retention objective.
  - YouTube's watch-time goal.
  - Substack's growing Notes and recommendation feed.
- **What it does:** each platform replaced user *choice* with *predicted engagement*, where engagement means comments, reshares, watch time, completion, or return visits. High-arousal content (outrage, fear, comparison, sexualization, shock, conspiracy) reliably scores high on those signals. So the ranker, working exactly as designed, amplified it [FACT for the internal findings at Meta and TikTok; INFERENCE for the generalization].
- **Why it ranks first:** it produced the widest harms (discourse, teen wellbeing, radicalization supply, child exploitation networks, the Myanmar-type amplification) and it runs continuously, at the scale of billions.

**2. Measured harm, chosen inaction: an information asymmetry used against the public. (Very severe.)**
- **The instances:**
  - Meta: the 2016 extremism study, 2018 MSI findings, 2019–2020 Instagram teen research, 2021 Béjar emails, and the alleged 2020 deactivation study.
  - TikTok: the 260-video threshold and the PR-measured time limit.
  - YouTube: staff warnings before 2019.
- **The pattern:** internal teams measured harm, leadership weighed it against growth, and public messaging said otherwise. Harm estimates could be produced *only* inside the companies, which then controlled whether they came out. Nearly everything we know came from whistleblowers (Haugen, Béjar, Wylie, Wynn-Williams, the 2025 VR researchers), leaks, or botched redactions, not from voluntary disclosure [FACT].
- **Why it's so severe:** this pattern is what turns pattern 1 from negligence into something closer to culpability.

**3. Children as a growth market. (Very severe, focused on the most vulnerable.)**
- **The instances:**
  - COPPA violations at TikTok/Musical.ly and YouTube.
  - Instagram Kids and the "teen foothold" strategy.
  - The emotional-state targeting document.
  - Messenger Kids flaws.
  - Elsagate.
  - Recommendation of child-exploitation networks.
  - Chatbot "sensual" roleplay standards.
- **Why it's structural:** the long-term value of a user starts in adolescence, so each company had a structural motive to acquire minors and a structural cost to protecting them.
- **Why it ranks below 1 and 2:** it is arguably the *most morally serious* pattern, but it's narrower in scope, and it is largely an instance of patterns 1 and 2 applied to children.

**4. Scale before safeguards: harms exported to the least-protected. (Severe.)**
- **The instances:**
  - Myanmar and Ethiopia language gaps.
  - The ~87% of misinformation spend going to the US.
  - Moderation outsourced to traumatized low-wage contractors in Kenya, the Philippines, and Colombia.
- **The pattern:** growth went global while safety scaled to where press and regulators were. The costs landed on people with the least ability to hold the companies accountable. In Myanmar the worst consequence (contribution to atrocity) is among the gravest in this history, but it is concentrated rather than continuous. That is why this pattern ranks fourth rather than higher. That's a judgment call [INFERENCE].

**5. Power bound by goodwill rather than structure. (Severe, and the enabling condition for the rest.)**
- **The conditions:**
  - Dual-class control (Meta, and Alphabet's founders).
  - Section 230 immunity for ranking decisions until *Anderson*.
  - Opaque, unilateral creator terms (YouTube demonetization, Creator Fund dilution, Instagram format pivots).
  - Safety policies that reverse with the political weather (Meta and YouTube in 2023–2025, TikTok's in-app lobbying).
- **Why it matters:** nothing bound these companies except their own choices, and those choices followed incentives. Creators especially had no bargaining power over the systems that set their income.

### The master cause

**The engagement objective function: ranking what people see by predicted engagement, because engagement is what the business monetizes.**

I'm naming the *ranking objective* rather than "the ad model" or "capitalism," because the ranking objective is the specific mechanism that turns a business incentive into harm at the level of each item a user sees. Four reasons:

- **Most harms route through it.** Outrage amplification, rabbit holes, extremist group joins, harmful teen comparison spirals, predator network recommendations, Elsagate content farms, dangerous challenges, compulsive use, and the pressures on news and creators all run through ranking by predicted engagement.
- **Evidence where it was turned down.** When YouTube demoted borderline content in 2019 it reported a large drop in exposure. When Meta ran break-glass measures in 2020, internal staff observed less harmful content. These are cases where changing the objective changed the harm [FACT that the interventions and claimed effects exist].
- **Evidence from Substack.** The mostly chronological, reader-chosen, email-delivered model avoided most of the harms above, and is now drifting toward them as it adds engagement-ranked surfaces [INFERENCE].
- **The other patterns depend on it.** Pattern 2 (knowing inaction) exists *because* the fixes cost engagement. Pattern 3 exists because teens are the highest-lifetime-engagement cohort. Pattern 4 exists because integrity budgets are paid from engagement revenue and allocated by exposure.

**Counterfactual and caveat.** If ranking had been bound to *stated user preference* (chronological or chosen feeds, explicit "show me more/less," and long-term satisfaction surveys over short-term signals), the platforms would still have hosted harmful content. They would not have *systematically amplified* it.

That counterfactual is partly contested. The 2023 Science/Nature chronological-feed experiments found that feed changes over three months did not shift polarization attitudes, though they did change exposure. So removing the engagement objective would clearly have reduced *exposure* harms (to children, to vulnerable users, to targeted groups). Its effect on *mass political attitudes* is less certain. Myanmar-style incitement would also have spread through groups and messaging (WhatsApp's role in India's 2017–2018 lynchings shows unranked virality can kill too). So the master cause is dominant, not total.

**The deeper incentive.** If you ask what sits beneath the objective function, it is **revenue coupled to attention, under governance with no external check**. That is the ad model plus founder control plus liability immunity. The ranking objective is how that incentive becomes harm to individual users. It is also the *most tractable* lever: it can be changed in code, audited, and regulated (for example the EU DSA's Article 38 requirement for a non-profiling feed option on very large platforms) without dismantling the companies.

---

## Part 4: What I May Be Missing, and Where I'm Least Confident

**Recency and cutoff.**
- My knowledge thins through late 2025–2026. I'm uncertain about:
  - the outcome of the MDL 3047/JCCP bellwether trials (any verdicts, settlements, or amounts);
  - the final state of the FTC v. Meta ruling and any appeal;
  - the final structure of the TikTok US joint venture and whether its algorithm is truly independent;
  - the status of the multistate AG suits against Meta and TikTok;
  - EU DSA decisions and fines against Meta, TikTok, and X-adjacent cases.
- There may be significant 2026 developments I simply don't know about: new whistleblowers, new leaks, and US federal legislation such as KOSA, which I believe had not passed as of my last reliable information.

**Figures I'm reconstructing from memory.** These are the right order of magnitude but may be off in detail: Cambridge Analytica's 87M, the 5.8M XCheck users, the 87% misinformation spend, the 260 videos and 1.5 minutes, the 13% of teens, the ~$16B scam-ad projection, Substack's $1.1B valuation, the CCDH $2.5M, and the Pew news percentages. The late-2025 Reuters scam-ad reporting and the "Project Mercury" allegations are the items where I'm most at risk of misremembering specifics.

**Where the science is genuinely unsettled.**
- The causal link between social media and the teen mental-health decline is the most important contested question in this document. The internal documents show *companies believed* they caused some harm to some users. They don't establish population-level causation. Serious researchers (Odgers, Orben, Przybylski, Ferguson) dispute the strong version, and others (Haidt, Twenge, Rausch) defend it.
- Polarization and radicalization effects are similarly contested, and the best recent experimental evidence cuts *against* the strongest claims.
- A reckoning that treats these as settled would be overclaiming.

**Selection bias in the evidence.** Nearly all internal evidence is from Meta (Haugen) and TikTok (Kentucky redactions). YouTube and Google have had no equivalent document dump, so YouTube may look *less* culpable here simply because less of its internal record is public. Substack's relative innocence is partly real (a different model) and partly scale (less scrutiny).

**Omitted platforms and forces.** Twitter/X, Snapchat, Reddit, WhatsApp (India's lynchings, Brazil's elections), Telegram, and Pinterest (named in the Molly Russell inquest) all share parts of this history. So do the ad-tech intermediaries and the data brokers. Assigning the whole attention economy to five platforms simplifies it.

**What they got right.** Part of historical honesty is that these platforms also delivered real goods:
- connection for isolated and marginalized people;
- creator livelihoods (YouTube especially);
- documentation of state violence (Arab Spring, police brutality);
- free education;
- in Substack's case, a genuinely portable, reader-funded model.

The brief asked for failures, and I've focused there. A complete history would weigh both, and the prosecution framing of the brief is a lens, not the whole truth.

**My own position.** I'm an AI built by a company in the same industry that is racing to build attention-relevant products. Readers should weigh that possible bias both ways: toward leniency with the industry, or toward overcorrecting to seem independent. I've tried to let the labels do the work.
