# The Reckoning: Five Platforms and the Attention Economy

*Phase 01, Reckon. Written blind from training knowledge only (no web access, no other files). Knowledge is dense through 2024, thinner through 2025, and sparse for 2026.*

## How to read this document

Every substantive claim carries one of four tags:

- **[FACT]**: documented in public records, court rulings, regulatory orders, company statements, or widely corroborated reporting.
- **[ALLEGED/LITIGATION]**: asserted in complaints, regulatory charges, or lawsuits that have not been fully adjudicated, or findings a court or regulator made that are still under appeal.
- **[LEAKED/ATTRIBUTED]**: from leaked internal documents, whistleblower disclosures, or reporting that attributes statements to internal sources. The documents look authentic, but the company often disputes how they are being read.
- **[INFERENCE]**: my own analytical judgment, drawn from the facts above.

Dates are approximate where marked "c." Figures come from memory. Treat them as accurate to the order of magnitude, and in most cases to the headline number, but check them against primary sources before relying on them in court or in print.

A note on method: a prosecution that overstates its case loses. In several places below the scientific evidence is contested, especially on population-level mental-health effects and on "rabbit hole" radicalization. There I say so plainly. The strongest charge against these companies is not that every harm is proven to have been caused by them. It is that they **measured risks, found signals of harm, and chose metrics over mitigation**. That charge rests on their own documents.

---

# PART (a): PER-PLATFORM RECKONING

---

## 1. META / FACEBOOK

### 1.1 The failures

**F1. Treating users as experimental and data subjects without meaningful consent (2007–2019).**
- **Beacon (2007)** broadcast users' off-site purchases to their friends by default. It was withdrawn after a class action that settled for about $9.5M in 2009. [FACT]
- **FTC consent decree (proposed 2011, finalized 2012)**: Facebook had told users they could keep information private and then repeatedly let it be shared and made public. [FACT]
- **Emotional contagion study**: in January 2012 Facebook manipulated the News Feeds of 689,003 users to test whether emotional content was contagious. It was published in *PNAS* in June 2014 (Kramer, Guillory, Hancock). No informed consent was obtained beyond the terms of service. [FACT]
- **Cambridge Analytica**: in 2014 Aleksandr Kogan's "thisisyourdigitallife" quiz app was installed by about 270,000 people. Through Facebook's friends-data API (Graph API v1.0) it harvested data on up to about 87 million users. Facebook learned of the transfer in December 2015 and asked for deletion certification, but did not notify users or audit. The story broke publicly in March 2018 through Christopher Wylie, *The Guardian/Observer*, and *The New York Times*. [FACT]
- **Consequences**: an FTC penalty of $5 billion (July 2019), the largest privacy penalty in FTC history at the time; SEC $100M for misleading risk disclosures; UK ICO £500,000 (the statutory maximum); a US consumer class-action settlement of $725M (2022). [FACT]
- **Onavo Protect** (acquired 2013) was a VPN that Facebook used as competitive surveillance to track rival app usage. It was pulled from Apple's App Store in 2018. [FACT] The "Facebook Research" app, disclosed by TechCrunch in January 2019, paid users including teens (13+) up to about $20/month for near-total phone access. [FACT] **"Project Ghostbusters"** used Onavo-style interception to decrypt Snapchat (and later YouTube/Amazon) analytics traffic. It surfaced in 2024 consumer antitrust litigation. [LEAKED/ATTRIBUTED; ALLEGED/LITIGATION]

**F2. Engagement-ranked News Feed amplifying divisive and false content (2009 to present, acute 2016–2021).**
- In 2016 internal researcher Monica Lee presented findings that **"64% of all extremist group joins are due to our recommendation tools"** (the "Groups You Should Join" and "Discover" features) and that "our recommendation systems grow the problem." [LEAKED/ATTRIBUTED; *WSJ*, May 2020]
- A 2018 internal slide: **"Our algorithms exploit the human brain's attraction to divisiveness,"** and if left unchecked would serve "more and more divisive content in an effort to gain user attention & increase time on the platform." Executives, including policy chief Joel Kaplan according to the reporting, shelved or diluted the proposed fixes (the "Common Ground" work) partly because they would disproportionately affect conservative publishers and would reduce engagement. [LEAKED/ATTRIBUTED; *WSJ*, May 2020]
- **"Meaningful Social Interactions" (MSI), January 2018**: publicly framed as a wellbeing move ("time well spent"). Internally, the MSI weights heavily rewarded comments and reshares. Internal memos found that "misinformation, toxicity, and violent content are inordinately prevalent among reshares." European political parties reportedly told Facebook they had shifted to more negative messaging because the algorithm rewarded it. In April 2020, according to the Haugen documents, Zuckerberg declined to apply a proposed fix (removing the downstream-reshare boost) broadly because it would cut MSI. [LEAKED/ATTRIBUTED; *WSJ* "Facebook Files," Sept 2021]
- **"Carol's Journey to QAnon" (2019)**: a test account for a fictional conservative North Carolina mother, "Carol Smith," was recommended QAnon and conspiracy groups within days. [LEAKED/ATTRIBUTED]
- A parallel 2019 **India test account** was flooded with inflammatory nationalist content, misinformation, and graphic violence within about three weeks. The researcher wrote that they had "seen more images of dead people in the past three weeks than I've seen in my entire life total." [LEAKED/ATTRIBUTED]

**F3. Complicity-by-neglect in mass atrocity and communal violence in the Global South (2012 to present).**
- **Myanmar**: Facebook became the de facto internet in Myanmar, partly through zero-rating deals. It was saturated with anti-Rohingya incitement, including from military-linked accounts, while Facebook had almost no Burmese-language moderation capacity. Reuters reported only about two Burmese speakers reviewing content in early 2015. [FACT, reported]
- Civil-society groups warned Facebook directly from about 2013–2015. [FACT, reported]
- The **UN Independent International Fact-Finding Mission (2018)** said Facebook had played a "determining role" in the spread of hate. The chair, Marzuki Darusman, said social media had "substantively contributed." [FACT]
- Facebook's own commissioned BSR assessment (November 2018) conceded it had not done enough to prevent the platform being used "to foment division and incite offline violence." [FACT]
- Amnesty International's 2022 report *The Social Atrocity* argued that Facebook's algorithms "proactively amplified" anti-Rohingya content. [FACT that the report says this; the causal claim is contested]
- Rohingya refugees filed a roughly $150B class action in the US and UK in December 2021. [ALLEGED/LITIGATION]
- **Sri Lanka (March 2018)**: anti-Muslim riots. Facebook apologized in 2020 after an Article One human-rights assessment. [FACT]
- **Ethiopia (2020–2022, Tigray war)**: Meareg Amare, a Tigrayan chemistry professor, was killed in November 2021 after Facebook posts doxxed him. His son Abrham Meareg and others sued Meta in Kenya's High Court in December 2022, seeking a restitution fund of about $1.6B and changes to the algorithm. Kenyan courts later allowed the case to proceed. [ALLEGED/LITIGATION]
- **India**: *WSJ* reported in August 2020 that public-policy executive Ankhi Das opposed applying hate-speech rules to BJP politician T. Raja Singh, citing business risk. [LEAKED/ATTRIBUTED]

**F4. Two-tier justice: "XCheck" (cross-check).**
- An internal whitelist exempted about **5.8 million** VIP accounts (as of 2020) from normal enforcement. [LEAKED/ATTRIBUTED; *WSJ*, Sept 2021]
- Example: in 2019 footballer Neymar posted nude images of a woman who had accused him of rape. They stayed up for about a day and were seen by tens of millions before removal. [LEAKED/ATTRIBUTED]
- An internal review said the practice was "not publicly defensible." [LEAKED/ATTRIBUTED]
- The Oversight Board's December 2022 policy advisory opinion found that cross-check was structured to serve business interests more than human-rights commitments. [FACT]

**F5. Election integrity and January 6.**
- **Russian influence in 2016**: the Internet Research Agency's content reached about **126 million** Americans on Facebook, per Facebook's October 2017 congressional testimony. [FACT]
- **2020**: Facebook ran "break-glass" measures around the November 2020 election, then rolled many of them back after the election. It dissolved the Civic Integrity team in early December 2020. [LEAKED/ATTRIBUTED; the dissolution itself is FACT]
- "Stop the Steal" groups grew explosively. An internal post-mortem (c. March 2021) conceded that Facebook failed to treat the movement as a coordinated whole because its enforcement was built around individual pieces of content. [LEAKED/ATTRIBUTED]
- **Kenosha (August 2020)**: a "Kenosha Guard" militia event page was reportedly flagged about 455 times and not removed before the shootings. Zuckerberg called it an "operational mistake." [FACT, reported]
- **Sophie Zhang's September 2020 exit memo** described fake-engagement networks manipulating politics in Honduras, Azerbaijan, and elsewhere, which she said Facebook deprioritized because they did not generate PR risk in the US or Western Europe. "I know that I have blood on my hands by now." [LEAKED/ATTRIBUTED]

**F6. Advertising discrimination and fraud against advertisers and publishers.**
- ProPublica showed in 2016–2017 that housing ads could exclude "ethnic affinity" groups and that ads could target "Jew haters." [FACT]
- HUD charged Facebook in 2019. DOJ settled in June 2022, requiring a "Variance Reduction System" for housing ads. [FACT]
- **Video metrics inflation (2016)**: Facebook admitted that average video view time had been overstated, reportedly by 60–80%. Advertiser plaintiffs alleged inflation of 150–900% and that Facebook knew for more than a year. It settled for $40M in 2019. [FACT for the settlement; the size and knowledge claims are ALLEGED/LITIGATION]
- The bad metrics fed the industry-wide **"pivot to video."** Newsrooms (for example Mic, Mashable, Vocativ, Fox Sports digital) laid off writers to chase video. [FACT that the layoffs happened; how much the metrics caused them is INFERENCE]
- **"Potential Reach" inflation**: *DZ Reserve v. Meta* was certified as a class action. [ALLEGED/LITIGATION; I am uncertain of its final status]
- **Scam ads**: Reuters reported in late 2025 on internal documents projecting that about **10% of 2024 revenue (roughly $16B)** would come from ads for scams and banned goods. The same documents described users being shown billions of higher-risk scam ads daily and enforcement thresholds that tolerated likely-fraudulent advertisers. [LEAKED/ATTRIBUTED; moderate confidence on the specifics]

**F7. Exploited moderation labor.**
- Contracted moderators (Cognizant in Phoenix and Tampa, Accenture, Genpact, Sama in Nairobi) reviewed traumatic content for low pay under strict productivity metrics. Casey Newton's "The Trauma Floor" (*The Verge*, 2019) documented this. [FACT]
- *Scola v. Facebook* settled for $52M in 2020. [FACT]
- Former Sama moderator Daniel Motaung sued Meta in Kenya (2022). In December 2024, reporting said more than 140 Kenyan moderators had been diagnosed with severe PTSD. [FACT for the filings and reporting; ALLEGED/LITIGATION for liability]

**F8. Harm to children and teens (Facebook and Instagram jointly; see §2 for Instagram detail).**
- **October 2023**: 41 states plus DC sued Meta, alleging it designed addictive features aimed at youth and knowingly harbored under-13 users. The unredacted complaint said Meta received about **1.1 million reports of under-13 users** from early 2019 and disabled only a fraction. [ALLEGED/LITIGATION]
- **New Mexico (December 2023)**: AG Raúl Torrez sued over child sexual exploitation, based on test accounts that attracted predators. [ALLEGED/LITIGATION]
- **Filings unsealed c. November 2025 in the federal MDL (In re Social Media Adolescent Addiction, MDL 3047)** described two things:
  - **"Project Mercury"**: a c. 2019–2020 deactivation study run with Nielsen. It reportedly found that people who stopped using Facebook for a week reported lower depression, anxiety, loneliness, and social comparison. The research was then halted, with internal skeptics comparing the situation to the tobacco industry. [ALLEGED/LITIGATION; LEAKED/ATTRIBUTED]
  - A former safety lead's testimony that accounts engaged in sex trafficking were subject to a **"17-strike"** threshold before suspension. [ALLEGED/LITIGATION]
- **Generative AI chatbots (August 2025)**: Reuters reported an internal "GenAI: Content Risk Standards" document that permitted AI personas to engage children in "romantic or sensual" conversations. Meta said the examples were erroneous and removed them. Senator Hawley opened an inquiry. [LEAKED/ATTRIBUTED; FACT that Meta acknowledged and revised the document]

**F9. Retreat from integrity commitments and hostility to independent research (2021–2025).**
- In August 2021 Facebook disabled the accounts of NYU's Ad Observatory researchers (Laura Edelson, Damon McCoy), citing its FTC order. The FTC publicly said the order did not require that. [FACT]
- **CrowdTangle**, the main transparency tool for journalists and researchers, was starved of staff and then shut down on **August 14, 2024**, months before the US election. [FACT]
- On **January 7, 2025**, Zuckerberg announced the end of third-party fact-checking in the US in favor of Community Notes. He loosened the hateful-conduct policy, including permitting allegations of mental illness based on gender identity or sexual orientation, moved trust-and-safety staff to Texas, and framed the changes as a return to "free expression." Joel Kaplan replaced Nick Clegg as global affairs head. [FACT]
- Sarah Wynn-Williams' memoir ***Careless People*** (March 2025) alleged executive indifference in Myanmar, targeting of teens when they felt emotionally vulnerable to sell ads, and willingness to build censorship tools to enter China. Meta obtained an arbitration order restricting her from promoting it. [FACT for the book and the order; ALLEGED for its contents]

**F10. Anticompetitive acquisition to neutralize rivals.**
- Zuckerberg's 2008 remark that "it is better to buy than compete" and his 2012 emails about Instagram ("neutralize a potential competitor") are in the record of the FTC antitrust case. [FACT, in the court record]
- My understanding is that Judge Boasberg ruled for Meta in November 2025, finding the FTC had not proven *current* monopoly power. [FACT with moderate confidence; verify]

### 1.2 The mechanism

1. **Objective function**: News Feed ranking has optimized, successively:
   - clicks and likes (c. 2009–2013);
   - "time spent" and engagement bait (2013–2017);
   - MSI (2018–), which weighted comments and reshares about 15–30x a like according to leaked weight tables. [LEAKED/ATTRIBUTED for the specific weights]

   Every variant rewards content that provokes a **reaction**, and outrage, fear, and moral violation reliably provoke reactions. Academic work supports this: Brady et al. (2017) found each moral-emotional word raised retweet rates about 20%, and Rathje, Van Bavel and van der Linden (*PNAS*, 2021) found out-group animosity was the strongest predictor of shares on Facebook and Twitter. [FACT for the studies] The optimization is value-blind: it cannot tell a comment of outrage from a comment of delight. [INFERENCE, strongly supported]
2. **Ad revenue scales with time and targeting precision.** Revenue depends on impressions (time) multiplied by price (targeting precision). Time drives feed design. Targeting precision drives data extraction, which explains Beacon, Onavo, and the friends-data API. [INFERENCE]
3. **Groups and Pages recommendations** were growth tools that also served as recruitment funnels, per the 2016 64% finding. Growth teams owned recommendations; integrity teams had to justify every intervention against growth metrics. [LEAKED/ATTRIBUTED]
4. **Launch-first expansion.** Internet.org/Free Basics and zero-rating pushed Facebook into markets with no language capacity for moderation. Classifiers existed for a handful of languages. Per the Haugen documents, about **87%** of the misinformation budget (by classification time) went to the US, which had under 10% of users. [LEAKED/ATTRIBUTED]
5. **Organizational veto structure.** Public Policy (Kaplan's team) sat inside content decisions, so political and regulatory relationships influenced enforcement. Integrity proposals needed "MSI-neutral" justification. [LEAKED/ATTRIBUTED; *WSJ*, Haugen]
6. **Section 230** (US) meant amplification decisions carried little direct liability. That weakened the internal business case for safety spending. [INFERENCE; the legal shield itself is FACT]

### 1.3 The long tail

- **Rewired political communication.** Parties, publishers, and influencers learned that negativity and identity threat outperform. Politicians produced content for the algorithm, not the other way around, and that persisted after later ranking tweaks. [INFERENCE, supported by the leaked party-feedback memos]
- **Collapse of local news economics.** Facebook and Google together captured the majority of digital ad growth. Newsrooms first chased Facebook referral traffic, then were abandoned when News Feed deprioritized news (2018) and later deprecated news entirely (News tab ended 2023–2024; news blocked in Canada from August 2023 in response to the Online News Act). Newsroom employment in the US fell sharply through the 2010s. [FACT for the events; attributing the decline to Facebook specifically is INFERENCE, since Google, Craigslist, and the business model all contributed]
- **Epistemic fragmentation.** Groups became self-sealing communities: anti-vaccine, QAnon, "Stop the Steal." Anti-vax Facebook groups (2015–2019) preceded COVID-era vaccine hesitancy. Measuring causation is hard. [INFERENCE]
- **Precedent for the Global South.** Myanmar, Sri Lanka, India, and Ethiopia showed a repeating pattern: the platform enters, becomes infrastructure, and then under-invests in the languages where violence is likeliest. The lesson was learned and relearned across at least 2013–2022. [INFERENCE]
- **Chilling of research.** CrowdTangle's shutdown and the Ad Observatory bans reduced society's ability to audit, which is what the leaks had exposed. Future harm becomes less visible. [INFERENCE]
- **Normalization of regulatory settlement as a cost of business.** The $5B FTC fine was about a month of 2019 revenue. Meta's stock rose on the day it was reported. [FACT for the stock move; INFERENCE for the conclusion]
- **The 2025 realignment** suggests safety commitments were a function of political climate, not principle. Once pressure shifted, the policies shifted. [INFERENCE]

### 1.4 Root cause: what they knew, and when

| When | What was known internally | What happened |
|---|---|---|
| 2013–2015 | Myanmar civil society warned directly | Minimal Burmese investment until 2018 [FACT, reported] |
| Dec 2015 | Knew Cambridge Analytica had the data | No user notice until 2018 [FACT] |
| 2016 | 64% of extremist group joins came from recommendations | Recommendations continued; Groups promoted heavily from 2017 ("Communities" mission) [LEAKED] |
| 2018 | "Algorithms exploit…divisiveness" | Common Ground fixes shelved [LEAKED] |
| 2018–2020 | MSI rewards outrage and misinformation | Zuckerberg declined the broad fix, April 2020 [LEAKED] |
| 2019 | "We make body image issues worse for one in three teen girls" | Publicly, Meta said research was "not conclusive" [LEAKED] |
| 2019–2020 | Deactivation study showed wellbeing gains | Halted, not published [ALLEGED/LITIGATION] |
| 2019–2021 | BEEF survey: 13% of 13–15-year-olds received unwanted sexual advances within 7 days (Béjar) | Béjar's October 2021 email to Zuckerberg, Sandberg, Cox and Mosseri went unanswered by Zuckerberg [FACT per sworn testimony, Nov 2023] |
| 2020 | XCheck "not publicly defensible" | Continued [LEAKED] |
| Dec 2020 | Election "break glass" lifted, civic team disbanded | Jan 6 [FACT/LEAKED] |

**Structural incentive:** Meta's revenue is almost entirely advertising (about 97–98%). Advertising revenue is time multiplied by targeting precision. Integrity measures that reduce time or reach show up directly as lost revenue, while their benefits are diffuse, delayed, and borne by non-customers. Zuckerberg's majority voting control through Class B shares means no board or shareholder check can force a trade-off. **The single-point-of-control governance plus the ad model produced a decision system in which harm was measured, documented, and then weighed against MSI and DAU, and usually lost.** [INFERENCE, heavily supported by the documents]

---

## 2. INSTAGRAM

### 2.1 The failures

**F1. Social comparison and body-image harm to adolescent girls.**
- Internal research from 2019–2020, part of the documents Frances Haugen disclosed (*WSJ*, September 14, 2021):
  - "We make body image issues worse for one in three teen girls."
  - "Thirty-two percent of teen girls said that when they felt bad about their bodies, Instagram made them feel worse."
  - "Teens blame Instagram for increases in the rate of anxiety and depression… This reaction was unprompted and consistent across all groups."
  - Among teens who reported suicidal thoughts, **13% of British users and 6% of American users** traced the desire to Instagram.

  [LEAKED/ATTRIBUTED]
- Meta's response was that the research was small-sample and qualitative, and that more teens said Instagram helped than hurt on most measures. [FACT that Meta said this] Both things are true: the slides were not causal studies, and Meta's public testimony (Zuckerberg to Congress in March 2021: research shows social apps can have "positive mental-health benefits") omitted what its own researchers had found. [INFERENCE]
- **Beauty and cosmetic-surgery filters**: Meta temporarily banned filters simulating plastic surgery in 2019. According to the state AG litigation, in 2020 wellbeing experts (including design VP Margaret Gould Stewart) recommended keeping the ban, and Zuckerberg overruled them, citing "demand" and paternalism. [ALLEGED/LITIGATION; LEAKED/ATTRIBUTED]
- **"Project Daisy" (hiding like counts)**, 2019–2021, found limited wellbeing benefit and some cost to engagement and ad metrics. It shipped only as an opt-in. [LEAKED/ATTRIBUTED; FACT for the opt-in launch in May 2021]

**F2. Recommendation of self-harm and eating-disorder content.**
- **Molly Russell**, a 14-year-old from Harrow, London, died in November 2017 after viewing large volumes of self-harm and suicide content, including algorithmically recommended material (Instagram and Pinterest). Of about 16,300 Instagram posts she saved, shared, or liked in her last six months, about 2,100 related to depression, self-harm, or suicide. [FACT, inquest evidence]
- On **September 30, 2022**, coroner Andrew Walker concluded she "died from an act of self-harm whilst suffering from depression and the negative effects of on-line content." At the inquest a Meta executive, Elizabeth Lagone, defended much of the content as "safe." [FACT]
- In September 2021, Senator Blumenthal's office created a test account posing as a 13-year-old girl, which was rapidly recommended extreme dieting and pro-eating-disorder content. [FACT]
- Individual lawsuits include ***Spence v. Meta*** (Alexis Spence, who developed an eating disorder after joining Instagram at about 11). [ALLEGED/LITIGATION]

**F3. The platform as infrastructure for child sexual exploitation.**
- *WSJ*, with the Stanford Internet Observatory and UMass Amherst (**June 7, 2023**), found that Instagram's recommendation systems "connect and promote" networks of accounts commissioning and selling child sexual abuse material. Hashtag search surfaced explicit terms, and Instagram sometimes showed a warning with the option "see results anyway." [FACT, reported; Meta set up a task force in response]
- *WSJ* (**November 2023**) found that test accounts following young gymnasts and cheerleaders were served Reels mixing sexualized child content with ads from major brands. [FACT, reported]
- **Sextortion**: Nigerian-based networks targeted teen boys on Instagram. **Jordan DeMay**, 17, of Marquette, Michigan, died by suicide in March 2022 within hours of being extorted. Two Nigerian brothers were extradited and sentenced in 2024 to about 17.5 years each. [FACT] Reports to NCMEC of financial sextortion rose steeply from 2022. [FACT] Plaintiffs allege Instagram's design features enabled strangers to find and message teens at scale: public follower lists, "Accounts you may know," and DMs from unknown adults. [ALLEGED/LITIGATION]
- **Arturo Béjar**, former engineering director, testified to the Senate in **November 2023**. His BEEF ("Bad Experiences and Encounters Framework") survey found that about **13% of 13–15-year-olds** reported unwanted sexual advances in the prior 7 days. He said leadership, including Zuckerberg, ignored his October 2021 memo. [FACT, sworn testimony]
- A September 2025 independent report co-authored by Béjar with child-safety groups (*Teen Accounts, Broken Promises*) tested 47 safety features and reported that most were ineffective, unavailable, or discontinued. [FACT that the report exists; its findings are disputed by Meta]

**F4. Knowingly courting under-13s and designing for compulsion.**
- "Instagram Youth/Kids" was announced in March 2021 and paused on **September 27, 2021** after the leaks. [FACT]
- Internal documents cited by the states discuss teens as a strategic priority and the aim of winning "tweens." [ALLEGED/LITIGATION; LEAKED/ATTRIBUTED]
- The design features in dispute are infinite scroll, autoplay Reels, algorithmic Explore, push notifications timed for re-engagement, variable-reward like counts, streaks, and ephemeral Stories that create fear of missing out. The states and the MDL plaintiffs argue these are design defects, which puts them outside Section 230 speech protections. [ALLEGED/LITIGATION]
- In the MDL, Judge Yvonne Gonzalez Rogers ruled (November 2023) that some design-defect claims can proceed notwithstanding Section 230. [FACT]
- **Teen Accounts** (September 2024) arrived roughly three years after the leaks and 12 years after the acquisition. [FACT]

**F5. Creator harms.**
- **Opaque reach suppression ("shadowbanning")**: Instagram long denied it. In 2021–2022 it introduced "Account Status" and acknowledged "recommendation guidelines" that make content ineligible for Explore and Reels without notifying the creator. [FACT]
- From **2024** Instagram and Threads stopped recommending "political content" from accounts users did not follow, by default. Advocates, journalists, and marginalized creators lost reach. [FACT]
- LGBTQ+, sex-worker, fat, and Black creators reported disproportionate suppression and removal. Meta disputed systematic bias. [ALLEGED; anecdotally extensive]
- **Rug-pulls in format**: Instagram pushed creators into video (IGTV 2018, discontinued 2022), then Reels (2020), with bonus programs. **Reels Play bonuses** were cut back sharply in 2023. [FACT] The July 2022 "Make Instagram Instagram Again" backlash, amplified by Kylie Jenner and Kim Kardashian, forced Adam Mosseri to walk back the TikTok-style full-screen feed test. [FACT]
- **Unpaid labor**: creators generate most of the content value, yet Instagram shares little ad revenue with them compared with YouTube's 55% long-form split. [FACT for the comparison; INFERENCE that this is a harm]

**F6. Commercialized self-presentation and the influencer economy.**
- Undisclosed sponsored content and deceptive influencer marketing led to FTC warning letters from 2017 onward. [FACT]
- The **Fyre Festival** (2017) was a canonical fraud promoted through Instagram influencers. [FACT]
- Instagram was a key vector for wellness misinformation. The CCDH's "Disinformation Dozen" (2021) were active on Instagram and Facebook. [FACT for the report]

### 2.2 The mechanism

1. **Visual social comparison as the core product.** Instagram's core unit is a curated image of self, rated publicly by quantified approval (likes, followers). Social comparison theory (Festinger, 1954) predicts upward comparison harms for vulnerable individuals. The product's central act is performing and consuming idealized selves. [INFERENCE grounded in established psychology]
2. **Algorithmic feed (2016) and Explore/Reels (2012–2020)** converted a chronological friends feed into an interest-optimizer. An interest-optimizer that detects lingering on thinness or self-harm content serves more of it. The system reads distress as interest. [INFERENCE; consistent with the leaked research and the test-account studies]
3. **Network-growth features** ("Suggested for you," "Accounts you may know," open DMs, public follower graphs) are growth tools that also shrink the social distance between predators and children, as the WSJ/Stanford findings show. [INFERENCE supported by reporting]
4. **Integration into Meta's ad machine after 2012.** Once Instagram's growth team reported into Meta, it inherited the same engagement and DAU targets. Instagram was also Meta's hedge against losing youth to Snapchat and TikTok. Losing teens was treated as an existential threat, so teen engagement was protected. [LEAKED/ATTRIBUTED: internal "teen engagement" concern documents; INFERENCE on how it was prioritized]
5. **Copycat competition with TikTok.** Reels imported TikTok's full-screen, autoplay, interest-graph model, bringing the same risk profile: rapid rabbit holes and weak social context. [INFERENCE]

### 2.3 The long tail

- **Adolescent mental health.** Jonathan Haidt, Jean Twenge, and others argue that the post-2012 rise in teen depression, anxiety, and self-harm, especially among girls, tracks smartphone and social-media adoption, with Instagram central. [FACT that they argue this] Candice Odgers, Amy Orben and Andrew Przybylski, and others argue that the average effect sizes in population data are small and causation unproven. [FACT that they argue this] **My assessment**: population-level causation remains scientifically contested. Harm to a vulnerable subset is well supported, including by Meta's own surveys. Meta's documented choice to withhold and downplay its own findings is not contested. [INFERENCE]
- **Beauty-standard drift.** "Instagram face," filter dysmorphia (patients bringing filtered selfies to surgeons), and cosmetic-procedure normalization among young people grew through the 2010s. [FACT for the reported clinical trend; attribution to Instagram is INFERENCE]
- **Sextortion as an industry** grew from about 2021–2022 into an organized transnational crime category. [FACT] Plaintiffs allege it was enabled by teen-discoverability design choices Instagram had been warned about. [ALLEGED]
- **Legal paradigm shift.** Instagram and Facebook cases (Molly Russell, the MDL, the state AGs) moved the regulatory frame from "content" to "design." The UK Online Safety Act (2023), US state age-appropriate-design and phone-in-school laws, and Australia's under-16 social media ban (legislated late 2024, in force December 2025) are partly downstream of Instagram revelations. [FACT for the laws; INFERENCE for the causal lineage]
- **Creator precarity.** A generation of creators built businesses on reach they did not own. Each algorithm change was an unannounced pay cut. [INFERENCE]

### 2.4 Root cause: what they knew, and when

- **2019–2020**: internal "teen mental health deep dive" research was presented to senior leadership, and in 2020 to Zuckerberg, per the documents. [LEAKED/ATTRIBUTED]
- **March 2021**: Zuckerberg told Congress the research he had seen suggested positive effects. In the same period Meta was planning Instagram Kids. [FACT for the testimony; INFERENCE on how it squares with the internal record]
- **August 2021**: Senators Blumenthal and Blackburn asked Meta for its internal research. Meta did not produce the teen-mental-health studies. [FACT, reported]
- **October 2021**: Béjar's warnings reached Zuckerberg, Sandberg, Cox, and Mosseri directly. [FACT]
- **The structural incentive:** Instagram was Meta's teen-retention asset. Internal documents reportedly describe the loss of teen users as a risk to the "pipeline" of future users. [LEAKED/ATTRIBUTED] Any safety change that reduced teen engagement, including hiding likes, limiting DMs from strangers, default-private accounts, or removing beauty filters, therefore competed directly with a top-level strategic goal. Most such changes shipped only after public exposure or litigation. [INFERENCE, strongly supported by the timeline: default-private for under-16s in 2021 and Teen Accounts in 2024 both followed exposés]

---

## 3. TIKTOK (ByteDance)

### 3.1 The failures

**F1. An engineered compulsion machine, optimized with full awareness of harm.**
- ***NYT* (Ben Smith, December 2021)** published a leaked internal document, "TikTok Algo 101." It says the company's "ultimate goal" is adding daily active users, with "retention" and "time spent" as the key metrics. It includes a simplified scoring formula combining predicted likes, comments, playtime, and plays. [LEAKED/ATTRIBUTED]
- ***WSJ* (July 2021)**, "Inside TikTok's Algorithm," used about 100 bot accounts and showed that **watch time and rewatches** dominate. Bots could be pushed into depression and self-harm rabbit holes quickly. [FACT, reported investigation]
- **Kentucky AG complaint (October 2024)**, part of a coordinated suit by 14 AGs filed October 8, 2024. Redactions were defective, and NPR and Kentucky Public Radio reported the contents:
  - TikTok calculated that a user can become habituated after watching about **260 videos**, achievable in under 35 minutes.
  - Internal documents acknowledged that "compulsive usage correlates with a slew of negative mental health effects like loss of analytic skills, memory formation, contextual thinking, conversational depth, empathy, and increased anxiety."
  - The 60-minute screen-time prompt for teens reduced usage by only about **1.5 minutes** (from about 108.5 to 107 minutes a day). An internal note indicated the tool's success was measured by improving "public trust" via media coverage, not by reduced use. One project manager reportedly said "our goal is not to reduce the time spent."
  - Internal awareness that users entered "filter bubbles" within about **30 minutes**.
  - Algorithms reportedly favored conventionally attractive users.

  [ALLEGED/LITIGATION; LEAKED/ATTRIBUTED]
- **Center for Countering Digital Hate, "Deadly by Design" (December 2022)**: new teen test accounts were served suicide content within **2.6 minutes** and eating-disorder content within **8 minutes**. [FACT that the report found this; methodology disputed by TikTok]
- **Amnesty International, "Driven into the Darkness" (November 2023)**: within 5–6 hours, about half of the videos in the For You feeds of accounts signaling interest in mental health were potentially harmful mental-health content. [FACT for the report]

**F2. Deadly "challenges."**
- **Nylah Anderson**, 10, of Chester, Pennsylvania, died in December 2021 attempting the "Blackout Challenge," which TikTok's For You Page had served her. [FACT for the death; the recommendation is alleged and was accepted at the pleading stage]
- The Third Circuit held in ***Anderson v. TikTok* (August 27, 2024)** that TikTok's algorithmic curation is TikTok's own "expressive activity" (citing *Moody v. NetChoice*) and therefore not immunized by Section 230. That was a major doctrinal crack in platform immunity. [FACT]
- Other suits cite Lalani Walton (8) and Arriani Arroyo (9). [ALLEGED/LITIGATION]

**F3. Discriminatory suppression of vulnerable creators.**
- ***Netzpolitik* (December 2019)**: moderators were instructed to cap the reach of users deemed "vulnerable to bullying," including disabled, visibly autistic, fat, and LGBTQ users. Their videos were made invisible outside their home country or kept out of the For You feed after a view threshold. TikTok said it was a blunt anti-bullying policy. [LEAKED/ATTRIBUTED; TikTok confirmed a version had existed]
- ***The Intercept* (March 2020)**: moderators were told to suppress For You exposure for users with "abnormal body shape," "ugly facial looks," "too many wrinkles," or "shabby and dilapidated" environments such as slums, and to punish livestream content criticizing "state organs" or "national honor." TikTok said the guidelines were old or never used in the US. [LEAKED/ATTRIBUTED]
- **Black creators** staged a strike over uncredited dance choreography (the 2021 Megan Thee Stallion "Thot Shit" strike) and reported suppression of #BlackLivesMatter content in 2020. TikTok blamed a "glitch" and apologized. [FACT for the apology]

**F4. Political censorship aligned with Beijing's interests, and data access by China-based staff.**
- ***The Guardian* (September 2019)** published leaked moderation guidelines directing removal or down-ranking of content on Tiananmen Square, Tibetan independence, and Falun Gong. TikTok said they were retired. [LEAKED/ATTRIBUTED]
- **Feroza Aziz (November 2019)**: a US teen's makeup-tutorial video that doubled as a denunciation of the Uyghur internment camps was followed by her account suspension. TikTok apologized and blamed a "human moderation error." [FACT]
- ***BuzzFeed News* (June 2022)** published leaked audio of internal meetings. Quotes included "Everything is seen in China," and China-based engineers accessed US user data at least from September 2021 to January 2022. [LEAKED/ATTRIBUTED]
- ***Forbes* (Emily Baker-White, 2022)** reported that ByteDance employees accessed journalists' IP data to hunt for leakers. **ByteDance confirmed in December 2022** that employees had improperly accessed the data of two journalists and several associates, and it fired four employees. [FACT]
- ***Forbes*, January 2023**: TikTok staff had a manual "**heating**" button to boost selected videos into For You feeds, for creator deals and partners, and sometimes abused by employees. That undermined the claim that reach was purely algorithmic. [LEAKED/ATTRIBUTED; TikTok acknowledged the practice]
- **Regulatory findings**:
  - The Irish DPC fined TikTok **€345M (September 2023)** over children's data defaults. [FACT]
  - The Irish DPC fined TikTok **€530M (May 2025)** over transfers of EEA data to China and misleading assurances about it. [FACT, high-moderate confidence]
  - The Musical.ly COPPA settlement was **$5.7M (February 2019)**, then a record. [FACT]
  - DOJ, on referral from the FTC, sued again for COPPA violations in **August 2024**. [ALLEGED/LITIGATION]

**F5. Exploitation in LIVE and gifting.**
- Forbes (2022) and state AG complaints (Utah, 2023–2024) alleged that TikTok LIVE's virtual-gift economy, in which TikTok takes a large cut, facilitated sexual exploitation of minors ("virtual strip clubs"). They also alleged TikTok knew from internal review ("Project Meramec," per the Utah complaint) that underage users were streaming and receiving gifts. [ALLEGED/LITIGATION; LEAKED/ATTRIBUTED]

**F6. Creator economics.**
- The **Creator Fund (July 2020)** was a fixed pool ($200M in the US initially, promised up to $1B in the US and $2B globally over about 3 years) divided among a growing pool of creators and views. Payouts fell to roughly **$0.02–0.04 per 1,000 views**. Creators such as Hank Green publicly criticized the math: more creators and more views meant less per view. [FACT for the structure and reporting]
- The fund was replaced by the Creativity Program (2023) and later "Creator Rewards." Payouts improved for long videos (over 1 minute), which pushed creators into longer formats. [FACT]
- The **TikTok Shop** push from 2023 turned creators into affiliate sellers, with rapid commission and policy changes. [FACT]

**F7. Moderator trauma.**
- Contracted moderators (Telus International, Teleperformance in Colombia, Majorel, contractors in Kenya and Morocco) reported trauma. **Candie Frazier** sued in December 2021. [FACT for the filing]
- Forbes (2022) reported that some moderators were given training materials containing real child sexual abuse imagery. [LEAKED/ATTRIBUTED]

**F8. Election and information integrity.**
- **Romania**: the Constitutional Court **annulled the first round of the presidential election on December 6, 2024**, after declassified intelligence alleged a coordinated TikTok campaign boosted far-right candidate Călin Georgescu, including undeclared paid influencers. The European Commission opened DSA proceedings against TikTok in December 2024. [FACT for the annulment and the proceedings; the extent of TikTok's role and any state coordination is ALLEGED and contested]
- **Israel/Gaza (2023–)**: disputes over whether TikTok skewed content. Evidence was mostly correlational, driven by user demographics. [INFERENCE: the charge of deliberate skew is weakly supported]

### 3.2 The mechanism

1. **The interest graph, not the social graph.** TikTok's For You feed needs no friends. It infers preference from micro-signals such as dwell time, rewatch, and swipe latency, updated within a single session. It is the purest implementation of "maximize predicted watch time." A system that learns within minutes from implicit behavior, with no social context, is a **fast-convergence engine**: it finds the edge of each user's vulnerability faster than any prior feed. [INFERENCE grounded in the WSJ/NYT evidence]
2. **Short-form plus full-screen plus autoplay plus infinite scroll** removes stopping cues and makes every swipe a variable-ratio reward (the slot-machine schedule described by Skinner and popularized for tech by Natasha Dow Schüll's *Addiction by Design*). [INFERENCE; the design features are FACT]
3. **Growth-at-all-costs origin.** ByteDance reportedly spent more than $1B on ads (2018–2019) to buy users, including heavy Snapchat and Facebook ad buys, so it needed maximum retention to pay back acquisition cost. [FACT, reported ad spend; INFERENCE on the implication]
4. **Hand-tuned exceptions** (heating, bullying caps, guideline-based suppression) show the "neutral algorithm" was always a steered one. That steering was used for commercial deals and, according to leaks, aesthetic and political filtering. [LEAKED/ATTRIBUTED]
5. **Dual-jurisdiction governance.** ByteDance is subject to PRC national security and intelligence laws. Project Texas (the Oracle partnership, from 2022) was a technical workaround, not a governance change. [FACT for the laws and Project Texas; INFERENCE on how effective it was]
6. **ByteDance's Chinese domestic sister product Douyin** has a teen mode with a 40-minute limit, curfew, and educational content, introduced around 2019–2021 under Chinese regulation. [FACT] ByteDance evidently can build strong teen protections when a regulator demands it. The export version optimized differently. [INFERENCE: the most damning comparative fact in the TikTok file]

### 3.3 The long tail

- **Industry-wide format convergence.** Instagram Reels (2020), YouTube Shorts (2020–2021), Facebook Reels, Snapchat Spotlight, and later X and LinkedIn video feeds copied TikTok. Its compulsion architecture became the default grammar of the social internet. **TikTok's biggest long-tail harm may be what it forced competitors to build.** [INFERENCE]
- **Attention fragmentation.** Teachers and researchers report reduced sustained attention. There are experimental findings on short-form video and prospective memory. The literature is young and contested. [INFERENCE; FACT that the concern is widespread]
- **Algorithmic culture flattening.** The music industry now composes for 15-second hooks. Publishing ("BookTok") and retail ("TikTok made me buy it") respond to algorithmic virality. [FACT for industry adaptation; the value judgment is INFERENCE]
- **Health misinformation and self-diagnosis**: ADHD, Tourette's-like tics (a 2021 clinical cluster of functional tic disorders linked to TikTok exposure was reported in the medical literature), and misinformation about medications such as GLP-1s. [FACT for the tic-cluster reports; the broader trend is INFERENCE]
- **Geopoliticization of platforms.** TikTok became the test case for platform nationalism:
  - **PAFACA**, signed **April 24, 2024**, required divestiture. [FACT]
  - The Supreme Court unanimously upheld it in ***TikTok v. Garland*, January 17, 2025**. [FACT]
  - TikTok went dark in the US for about 14 hours on January 18–19, 2025. [FACT]
  - Enforcement was repeatedly delayed by executive order. [FACT]
  - A US joint-venture deal was framed in September 2025 (Oracle, Silver Lake, MGX, with ByteDance keeping a minority stake and licensing the algorithm), and I believe it closed around January 2026. [FACT for the framework with moderate confidence; closing details low-moderate confidence]
  - The long-tail question is whether ownership change alters the optimization target. Nothing I know suggests it does. [INFERENCE]
- **Democratic integrity.** Romania is the first case where a national election was annulled with a platform's amplification dynamics at the center of the rationale. [FACT for the annulment; INFERENCE for how central TikTok was]

### 3.4 Root cause: what they knew, and when

- **By 2019–2020**, TikTok knew it was suppressing disabled, fat, LGBTQ, and poor users and framed it as protection. [LEAKED; TikTok's own partial admission]
- **By 2021 ("Algo 101")**, the explicit target was retention and time spent. [LEAKED]
- **By 2022–2024 (Kentucky documents)**, TikTok had quantified the habit-formation threshold (about 260 videos), knew compulsive use harms cognition and mental health, and designed a screen-time tool whose success criterion was public relations. [ALLEGED/LITIGATION; LEAKED]
- **The Douyin comparison** shows the capability existed. [FACT for Douyin's features; INFERENCE for the conclusion]
- **Structural incentive:** TikTok is the platform most purely built on implicit-signal watch-time maximization, financed by ad revenue and commerce, under a parent whose internal culture ("Always Day 1," aggressive growth OKRs) and whose competitive position against Meta and YouTube rewarded retention above all. It had no legacy social graph to fall back on. **Its entire moat is how well it captures time.** A tool that meaningfully reduced time spent would have attacked the moat, so such tools were built to be ineffective. [INFERENCE, supported by the Kentucky documents]

---

## 4. YOUTUBE (Google/Alphabet)

### 4.1 The failures

**F1. The watch-time pivot and the recommendation engine.**
- In **2012** YouTube changed its core ranking signal from views (clicks) to **watch time**, publicly, to fight clickbait. [FACT]
- Product lead **Cristos Goodrow set the goal of 1 billion hours of watch time per day** (in 2012). YouTube reached it in **October 2016**. [FACT; Goodrow has written about it]
- Google's RecSys paper "Deep Neural Networks for YouTube Recommendations" (Covington, Adams, Sargin, **2016**) states the objective as predicting **expected watch time**. [FACT]
- Chief Product Officer Neal Mohan said at CES in January 2018 that recommendations drive **over 70%** of watch time. [FACT]
- Former engineer **Guillaume Chaslot** (at Google c. 2010–2013) founded AlgoTransparency and argued that recommendations systematically favored conspiracy and divisive content (for example, flat-earth and 2016-election content). [FACT that he argued this; his methodology has been criticized]

**F2. Executives ignored internal warnings about toxic content.**
- ***Bloomberg* (Mark Bergen, April 2, 2019)**, "YouTube Executives Ignored Warnings, Letting Toxic Videos Run Rampant," reported the following. [LEAKED/ATTRIBUTED]
  - Employees proposed changes to stop recommending conspiracy and "borderline" videos and to track toxic content. Leadership rebuffed them for years because engagement mattered most.
  - Lawyers reportedly advised staff *not* to proactively search for problematic videos, to avoid knowledge-based liability.
  - One employee created an internal "alt-right" vertical, which showed that channel category's engagement rivaled music, sports, and gaming.
  - Proposals to flag borderline content (associated with then-privacy engineer Yonatan Zunger) were not adopted.
- **January 2019**: YouTube announced it would reduce recommendations of "borderline content," and later claimed a **70%** drop in watch time of such content from non-subscribed recommendations. That was roughly seven years after the watch-time pivot and two years after the internal warnings described. [FACT for the announcement and the company claim]

**F3. Children: Elsagate, predators, and the COPPA violation.**
- **Elsagate (2017)**: an industrial genre of algorithm-gamed, disturbing videos featured children's characters (Elsa, Spider-Man, Peppa Pig) in violent or sexual scenarios, plus channels like "Toy Freaks" showing children in distressing situations. They were served to toddlers through autoplay, including on YouTube Kids (launched February 2015). James Bridle's essay "Something is wrong on the internet" (November 2017) brought it to wide attention. YouTube removed tens of thousands of videos and hundreds of channels in November 2017. [FACT]
- **February 2019**: YouTuber Matt Watson showed that the recommendation "wormhole" linked innocuous videos of children into a network commented on by pedophiles with timestamps. Advertisers (Disney, Nestlé, Epic Games) paused spending. YouTube disabled comments on most videos featuring minors. [FACT] (The *NYT* reported similar findings in June 2019, with researchers showing the algorithm recommending home videos of partially clothed children to viewers of sexual content.) [FACT, reported]
- **COPPA settlement, September 2019**: Google/YouTube paid **$170M** ($136M to the FTC, $34M to New York), then a COPPA record. The FTC said YouTube had marketed itself to toy companies as the top destination for kids ("the new Saturday morning cartoons") while telling parents and regulators it was not for under-13s, and collected children's data for behavioral ads. [FACT]
- The **"made for kids" designation** (January 2020) removed personalized ads and comments from children's content. Creators absorbed revenue drops of roughly 60–90% for kids' channels, bearing the cost of YouTube's own violation. [FACT for the rule; revenue figures are creator-reported]
- In 2023 Adalytics alleged that ads on "made for kids" videos were still being served with tracking cookies. Google disputed this. [ALLEGED]

**F4. Radicalization pathways and conspiracy infrastructure.**
- **Zeynep Tufekci, "YouTube, the Great Radicalizer" (*NYT*, March 2018)**: autoplay escalated viewers from mainstream to extreme. [FACT that she argued this]
- **Ribeiro et al., "Auditing Radicalization Pathways on YouTube" (FAT* 2020)** found users migrating from "Alt-lite/IDW" channels to alt-right channels in comment data. [FACT]
- **Christchurch (March 15, 2019)**: the attacker livestreamed on Facebook, and copies proliferated on YouTube faster than removal. At one point YouTube reported a new upload every second. [FACT] The **New Zealand Royal Commission (December 2020)** found the terrorist said he had watched far-right YouTube content and that YouTube was a "significant source of information and inspiration" for him. [FACT]
- ***NYT*, "How YouTube Radicalized Brazil" (August 2019)**: the algorithm elevated far-right personalities, and Bolsonaro allies credited YouTube. The same reporting covered Zika-era medical conspiracies harming health responses. [FACT, reported]
- **Rebuttal evidence, which a fair reckoning must include:**
  - **Hosseinmardi et al. (*PNAS*, 2021)** found consumption of far-right content was driven more by user preference and off-platform links than by recommendations. [FACT]
  - **Chen, Nyhan, Reifler, Robertson and Wilson (*Science Advances*, 2023)** found exposure to extremist and alternative channels concentrated among a small set of already-resentful subscribers, with few "rabbit hole" cases among non-subscribers after the 2019 changes. [FACT]

  **My assessment**: the strong "algorithm turns normal people into extremists" thesis is not well supported *after 2019*. It is plausible but under-measured for 2012–2018, which is the window YouTube never opened to researchers. What is well supported is that YouTube **built the audience, monetization, and discovery infrastructure** that let extremist and conspiracy entrepreneurs scale into businesses (Alex Jones' InfoWars channel had billions of views before its 2018 removal). [INFERENCE]
- **Foreign influence through monetized creators**: the DOJ's **September 2024** indictment of two RT employees alleged about **$10M** funneled through Tenet Media to US right-wing YouTubers (the creators, including Tim Pool, Benny Johnson, and Dave Rubin, said they were unaware and were victims). [FACT for the indictment; ALLEGED for its contents] **RT** built one of YouTube's largest news channel presences, with ads monetized under a Google Preferred-adjacent status in the mid-2010s, before its global removal in March 2022. [FACT]

**F5. Creator harms: the "Adpocalypse" and opaque monetization.**
- **March 2017**: *The Times* of London found major brands' ads on extremist videos. Advertisers pulled out, and YouTube responded with broad automated demonetization ("yellow dollar signs") and new eligibility thresholds (January 2018: 1,000 subscribers and 4,000 watch hours). Small and marginal creators were hit hardest. [FACT]
- **LGBTQ creators**' lawsuit (*Divino Group v. Google*, 2019) alleged Restricted Mode and demonetization systematically suppressed LGBTQ content. It was dismissed. [ALLEGED/LITIGATION; dismissal FACT]
- **Black creators**' lawsuit (*Newman v. Google*, 2020) made similar claims about race. [ALLEGED/LITIGATION]
- **Content ID** enabled fraudulent claims and let rights-holders seize creators' revenue with weak appeal paths. [FACT that abuse is widely documented]
- **Burnout**: in 2018–2019 many top creators (for example, Elle Mills and others) publicly described mental-health collapse from upload-cadence pressure the algorithm rewarded. [FACT for the reports; INFERENCE for the cause]
- **Shorts** (India 2020 after its TikTok ban, US 2021) monetized far below long-form: a pooled revenue share from 2023, with very low RPMs. [FACT]

**F6. Election misinformation policy whiplash and political capitulation.**
- YouTube did not remove 2020 "election fraud" claims until **December 9, 2020**, after the safe-harbor deadline. [FACT]
- In **June 2023** it announced it would stop removing false claims about 2020 and prior US elections. [FACT]
- In **September 2025**, Alphabet told the House Judiciary Committee that the Biden administration had pressured it on COVID content, and announced a path for creators banned under retired COVID and election-integrity policies to return. [FACT with moderate confidence]
- Around the same time YouTube reportedly agreed to pay about **$24.5M** to settle Donald Trump's lawsuit over his 2021 suspension. [FACT with moderate confidence]
- The swing shows that policy followed political climate rather than principle. The same critique applies to Meta. [INFERENCE]

**F7. Moderation labor.**
- Former moderators sued (*Doe v. YouTube*, 2020) over trauma. The case settled for about **$4.3M** (2022). [FACT]

**F8. Kids' attention economy and "baby content."**
- YouTube became a primary screen for toddlers (Cocomelon and similar channels optimized for autoplay retention). [FACT for market dominance] The American Academy of Pediatrics' guidance on under-2 screen use was structurally undermined by autoplay defaults. [INFERENCE]
- **Kidfluencer labor**: family vlogging channels monetized children's lives. Examples include the Ruby Franke/"8 Passengers" case (convicted of child abuse in 2023–2024) and earlier "DaddyOFive" (2017). This led to state laws such as Illinois (2023) requiring trust accounts for child influencers. [FACT]

### 4.2 The mechanism

1. **Watch-time maximization with autoplay and "Up Next"** (autoplay default-on from 2015–2016). The system rewards content that keeps people watching, which favors long, serialized, emotionally activating, and "hidden truth" narratives. Conspiracy content fits perfectly: there is always another video to explain the last one. [INFERENCE; consistent with the Bloomberg reporting]
2. **The 55/45 ad revenue share created a professional creator class.** That was YouTube's great innovation and its great lever. Creators respond to algorithm incentives with thumbnails, titles, length, outrage, and "reaction" formats, so the algorithm's objective is multiplied by millions of profit-seeking optimizers. [INFERENCE]
3. **Scale over review.** More than 500 hours of video are uploaded per minute (a company figure c. 2019). Human pre-review is impossible, so safety relies on classifiers plus flagging. Harm is detected after exposure. [FACT for the figure]
4. **Liability avoidance by not-looking.** The reported legal advice not to search proactively (Bloomberg) is a textbook example of an incentive structure under which knowledge creates exposure, so ignorance is cultivated. [LEAKED/ATTRIBUTED; INFERENCE on the structure]
5. **Advertiser, not user, as the effective safety regulator.** Major policy changes (2017 Adpocalypse, 2019 child comments) happened when **advertisers** withdrew, not when researchers or users complained. Brand safety substituted for user safety, and it punished creators broadly rather than targeting harmful content precisely. [INFERENCE, strongly supported by the timeline]

### 4.3 The long tail

- **Conspiracy entrepreneurship as a durable industry.** The 2012–2018 growth window capitalized a generation of alternative-media channels that later migrated or multi-homed (Rumble, podcasts, Substack, X) with audiences intact. Deplatforming came after audience building. [INFERENCE]
- **Platform as de facto global TV and school.** YouTube is the most-used platform among US teens (Pew consistently shows over 90%). Its recommendation choices shape youth information diets at a scale no broadcaster ever had. [FACT for usage]
- **Degraded children's media ecosystem.** The market rewarded cheap, autoplay-optimized content over educational quality. That led to regulation (COPPA enforcement, UK Age Appropriate Design Code, 2021) and pushed YouTube into supervised-account products. [FACT for the regulations; INFERENCE for the causal story]
- **Global South political effects** in Brazil, Philippines (Marcos Jr. historical revisionism videos before the 2022 election, widely reported), and Myanmar. [FACT for the reporting; INFERENCE for the size of the effect]
- **The legal line.** ***Gonzalez v. Google*** (argued February 2023, decided May 2023), from Nohemi Gonzalez's death in the November 2015 Paris attacks, asked whether YouTube's recommendations of ISIS content fell outside Section 230. The Court sidestepped it after deciding *Twitter v. Taamneh* for the platforms. [FACT] The question of whether recommendation counts as publishing then reappeared in *Anderson v. TikTok*. [FACT]
- **AI-generated "slop" (2024–2025)**: automated channels mass-produce synthetic videos for the monetization program. YouTube updated its "inauthentic/repetitious content" monetization policy in July 2025. [FACT with moderate confidence] This is the logical endpoint of rewarding watch time without regard to provenance. [INFERENCE]

### 4.4 Root cause: what they knew, and when

- The **2012 watch-time pivot** was an explicit, top-down bet that time spent was the right proxy for value. [FACT]
- From about **2016–2018**, employees raised alarms about conspiracy, extremist, and child-exploitation dynamics and were reportedly told not to rock the boat or look too hard. [LEAKED/ATTRIBUTED]
- **Major changes followed advertiser boycotts** (2017, 2019) and regulatory action (FTC 2019). [FACT for the timeline]
- **Structural incentive:** YouTube is the growth engine of Alphabet's non-search ad business (about $30B+ a year in ad revenue by 2021–2024, plus subscriptions). Watch time converts directly to ad inventory. Its safety posture was calibrated to **brand safety** (protect advertisers) more than **user safety**, and it chose ignorance where knowledge created liability. Unlike Meta, YouTube has produced fewer leaked "we measured harm and shelved the fix" documents, but that may reflect fewer leaks rather than fewer findings. [INFERENCE; the absence of evidence here is itself a flag]

---

## 5. SUBSTACK

*Proportionality note: Substack is far smaller (millions of paid subscriptions, not billions of users) and structurally different. It runs on reader subscriptions, not advertising. It deserves a reckoning, but a proportionate one. Its failures are mainly about **monetizing hate and misinformation under a laissez-faire moderation stance**, and a **drift toward the very engagement mechanics it was founded to reject**.*

### 5.1 The failures

**F1. "We don't moderate beliefs," so the platform takes a cut of extremism.**
- Co-founders Chris Best, Hamish McKenzie, and Jairaj Sethi (founded 2017) defined a light-touch content policy grounded in "free speech" and opposition to "censorship." [FACT]
- **November 2023**: Jonathan M. Katz, in *The Atlantic*, published "Substack Has a Nazi Problem." It identified at least 16 newsletters with overt Nazi symbols and white-supremacist content, several monetized, and noted figures such as Richard Spencer publishing there. [FACT]
- **December 2023**: more than 200 writers (about 247) signed "Substackers Against Nazis." [FACT]
- **December 21, 2023**: McKenzie responded that Substack did not like Nazis but would not demonetize or remove them, arguing that censorship "makes the problem worse." [FACT]
- **January 2024**: after *Platformer* (Casey Newton) submitted examples, Substack removed five publications for violating its incitement rules while keeping its overall stance. *Platformer* left for Ghost. Others (for example Molly White's *Citation Needed*, and later others to Beehiiv or Ghost) left or diversified. [FACT]
- **July 2025**: Substack's app sent a **push notification promoting a Nazi/white-nationalist newsletter** (reported by Taylor Lorenz's *User Mag*). Substack called it a serious error. [FACT with moderate confidence] Whatever the cause, it showed that Substack now runs recommendation and notification systems that *can* amplify, which undermines its long-standing "we're just a pipe; readers choose" defense. [INFERENCE]

**F2. Monetized health misinformation.**
- The **CCDH (January 2022)** estimated that Substack's top anti-vaccine newsletters (including Joseph Mercola, Alex Berenson, Steve Kirsch, and others) earned at least about **$2.5M a year**, with Substack taking about 10%. [FACT that the report estimated this; exact figures are estimates]
- Substack declined to act, citing its free-speech principles. [FACT]
- Berenson moved to Substack after his Twitter suspension (2021). [FACT] Substack became the paywall layer for deplatformed COVID contrarians. [INFERENCE, broadly accurate]

**F3. Opaque "Substack Pro" deals and a two-tier creator economy.**
- Starting about 2020–2021, Substack paid undisclosed advances to selected writers (for example Matt Taibbi, Glenn Greenwald, and others; some recipients later disclosed) while presenting the platform as a neutral, merit-based marketplace. [FACT]
- Critics argued the deals skewed toward heterodox and anti-"woke" writers and toward writers who attacked trans rights, and that the platform's economics were subsidized, not organic. Jude Doyle left in 2021, citing Substack's funding of anti-trans writers. Annalee Newitz and others raised similar concerns. [FACT that they argued and left; the skew is ALLEGED/contested; Substack said it chose writers on commercial grounds]
- The **structural problem** was that the leaderboards and "bestseller" framing hid which writers were subsidized. [INFERENCE]

**F4. Drift from newsletter to engagement-optimized social network.**
- Changes to the product over time:
  - **Recommendations network** (2022)
  - **Notes** (April 2023), a Twitter-like feed
  - an algorithmic app home feed
  - **Chat**
  - **video and livestreaming** (2024–2025)
  - leaderboards ranking paid growth
  - push notifications

  [FACT for the features]
- These features reintroduce the attention-economy machinery the founders once criticized. McKenzie and Best originally said Substack was an antidote to the attention economy, where writers are paid by readers, not by engagement. [FACT for the original framing]
- **Funding**:
  - Series A: a16z, 2019.
  - Series B: $65M at about $650M valuation (2021, a16z).
  - A 2023 community Reg A raise of about $7–8M.
  - Series C of about **$100M at about $1.1B** (July 2025, BOND and The Chernin Group).

  [FACT with moderate confidence on the 2025 figures] Venture valuations require growth beyond what a 10% take on subscriptions can quickly deliver, which pushes toward feeds, video, and network effects. [INFERENCE]

**F5. Structural amplification of polarization through paid-subscriber incentives.**
- Subscription economics reward loyalty and identity. Writers who give an audience a sense of an enemy and belonging convert best. [INFERENCE] Substack's bestseller lists have been dominated by political commentary. [FACT, broadly] The engine differs from the ad engine, but it also selects for affective intensity and partisan identity, just at a smaller scale and with more reader choice. [INFERENCE]
- **Mitigating fact (fairness)**: Substack lets writers **export their email lists and subscriber data**, including Stripe relationships. This is the most creator-respecting portability policy of the five platforms by a wide margin. [FACT]

### 5.2 The mechanism

1. **Take-rate on subscriptions (10% plus Stripe fees).** Substack's revenue scales with total paid subscriptions, whatever the content. A moderation decision against a large paid newsletter directly cuts revenue. The incentive runs toward permissiveness. [INFERENCE]
2. **Ideology as brand.** "Free speech absolutism" works as both principle and customer acquisition. Writers deplatformed elsewhere form a supply pipeline, and Substack's 2020–2021 Pro deals courted exactly that segment. [INFERENCE]
3. **VC growth pressure** drives the transition from pipe to feed, and a feed needs a ranking objective. The obvious objectives (engagement, conversions to paid) re-import the same pathologies. [INFERENCE]
4. **Recommendation and notification systems applied to a lightly moderated corpus** carry a structural risk: amplifying content the platform has declined to remove. July 2025 is the proof of concept. [INFERENCE]

### 5.3 The long tail

(Substack's history is shorter, so this is part observation and part forecast. It is labeled accordingly.)

- **Journalism's "great unbundling."** Substack accelerated star journalists leaving institutions (2020–2022). Individual writers gained independence and income. Institutional functions such as editing, fact-checking, legal review, and local beat coverage do not unbundle well. [FACT for the migration; INFERENCE for the institutional cost]
- **A durable home for deplatformed movements.** Substack became part of the infrastructure that let COVID contrarianism and anti-trans advocacy sustain paid audiences after mainstream deplatforming. [INFERENCE]
- **Mainstreaming.** By 2024–2025, politicians, officials, and administration-adjacent figures publish on Substack, which blurs journalism, advocacy, and official communication. [FACT for the trend]
- **Forecast [INFERENCE]**: if Substack's feed and video products take over from email as the main surface, its harm profile will converge toward Instagram and X. The main protection is list portability, which keeps exit costs lower than on any other platform.

### 5.4 Root cause: what they knew, and when

- The founders **explicitly knew** about the Nazi, anti-vax, and hate content. It was raised publicly (2021–2023) and they chose, as stated policy, to keep monetizing it. This is not hidden knowledge. It is an **openly declared trade-off**. [FACT]
- **Structural incentive:** a take-rate business with venture-scale valuation expectations and an ideological brand that turned permissiveness into a differentiator. Substack also shows the thesis's limit: removing advertising **does not** remove harm when (a) the take-rate is content-neutral and (b) growth pressure pulls in feed mechanics. [INFERENCE]

---

# PART (b): CROSS-PLATFORM VERDICT

## Recurring patterns, ranked by severity

Severity weighs breadth (number of people), depth (irreversibility: death, atrocity, childhood development), durability (how long the harm persists after the fix), and culpability (knowledge plus choice).

### Pattern 1 (most severe): Engagement-proxy optimization. The ranking objective was value-blind time and reaction.

- **Evidence across platforms**:
  - Meta: MSI, and "algorithms exploit…divisiveness." [LEAKED]
  - Instagram: Explore and Reels learned distress as interest. [LEAKED/INFERENCE]
  - TikTok: "Algo 101" (retention, time spent), and habit formation in about 260 videos. [LEAKED/ALLEGED]
  - YouTube: the 1-billion-hours goal and the expected-watch-time objective. [FACT]
  - Substack: moving into Notes, feeds, and push. [FACT/INFERENCE]
- **Why most severe**: it is the *upstream* cause of the largest harm categories. It drives amplification of outrage and misinformation, algorithmic rabbit holes for vulnerable teens, children being served dangerous challenges, recommendation-driven extremist group joins, and creators contorting content. It operates on billions of people continuously, and it was chosen, not accidental.

### Pattern 2: Measured harm, suppressed or overridden. The "knowledge-action gap."

- **Evidence**:
  - Meta: 64% extremist joins (2016), divisiveness slide (2018), MSI fix declined (2020), teen body-image research (2019–2020) contradicted in testimony (2021), Project Mercury halted (alleged), Béjar ignored (2021), XCheck "not defensible."
  - TikTok: ineffective screen-time tool judged by PR; 260-video habit threshold known.
  - YouTube: warnings rebuffed, lawyers advising not to look (2016–2019).
  - Substack: openly declared, not hidden.
  - Across platforms: researchers' access cut off (NYU accounts disabled 2021, CrowdTangle shut down 2024), which ensures future knowledge gaps.
- **Why second**: this pattern turns Pattern 1 from negligence into culpability. It is the most legally consequential. It is the basis of the state AG suits, the MDL, and the Kentucky/New Mexico cases, which is why it has a tobacco-litigation shape.

### Pattern 3: Children treated as a growth segment, and safety deferred until exposure.

- **Evidence**:
  - Instagram: Kids plan, beauty filters, teen-retention strategy, 1.1M under-13 reports (alleged), sextortion discoverability, CSAM network recommendations.
  - TikTok: Musical.ly COPPA; the 2024 DOJ COPPA suit; LIVE gifting; blackout challenge; the Douyin/TikTok double standard.
  - YouTube: marketed as "the new Saturday morning cartoons" to toy makers while denying child users ($170M COPPA); Elsagate; the predator wormhole.
  - Meta: AI chatbots allowed "sensual" chats with minors (2025, leaked standards).
- **Why third**: the harm is deep (development, death, sexual exploitation) and culpability is high, because age-verification and design protections were feasible, as the Douyin comparison shows.

### Pattern 4: Safety outsourced to the periphery. Global South and moderator labor as externalized cost.

- **Evidence**:
  - Meta: Myanmar (about 2 Burmese reviewers in 2015), Ethiopia, Sri Lanka, India, and about 87% of misinformation effort spent on the US; outsourced moderators with PTSD (Cognizant, Sama).
  - TikTok: moderators in Colombia, Kenya, and Morocco.
  - YouTube: moderator trauma settlements.
- **Why fourth**: this pattern contains the single worst outcome in the record, contribution to the conditions of a genocide. Its breadth is geographically concentrated and the causal chains are more contested than Patterns 1–3. It could reasonably be ranked first on depth alone, and I considered doing so.

### Pattern 5: Creators as unpaid or precarious labor, governed by opaque, reversible reach.

- **Evidence**:
  - YouTube: Adpocalypse, "made for kids" revenue loss, Content ID abuse.
  - Facebook: pivot to video built on inflated metrics.
  - Instagram: IGTV to Reels bonuses to cutbacks, shadowbanning, the 2024 political-content default.
  - TikTok: Creator Fund dilution, heating favoritism, suppression of disabled, fat, and LGBTQ users.
  - Substack: secret Pro deals.
- **Why fifth**: the economic harm is real and broad, but less lethal. It is still important as an amplifier: creators are the channel through which Pattern 1 is multiplied, because precarious creators must chase the algorithm.

### Cross-cutting enabler (not ranked, because it is a condition, not a pattern): unaccountable governance and legal immunity

- Zuckerberg's voting control, Google's founder-controlled share classes, and ByteDance's private dual-jurisdiction structure meant no internal check could override growth. [FACT for the structures]
- **Section 230** made amplification decisions mostly liability-free in the US until the design-defect theory (MDL, 2023) and *Anderson* (2024) began to crack it. [FACT]
- Policy followed political weather: YouTube's 2023 and 2025 reversals, Meta's January 2025 realignment, TikTok's deal-making. [FACT for the events]

## The master cause

**Engagement-maximizing ranking: the choice to optimize recommendation and feed systems for predicted time-spent and reaction (a proxy metric) on behalf of advertisers, instead of for user-endorsed value, deployed at planetary scale without a safety budget sized to that scale.**

If you remove that single mechanism, and replace the objective with something like "would the user, on reflection, endorse having seen this?", measured by surveys, stated preferences, and long-horizon wellbeing:

- Pattern 1 disappears by definition.
- Pattern 2 loses most of its occasion. The documents show harm research was overridden *because* fixes cost engagement metrics. Take away engagement as the scoring rule and the fixes stop being expensive.
- Pattern 3 shrinks sharply. Teen rabbit holes, challenges, and compulsive-use design are engagement-optimizer outputs. Discoverability-for-growth, a close cousin, remains.
- Pattern 5 shrinks. Creators chase the objective, so a different objective changes what they make.
- Pattern 4 is only partly addressed. Myanmar-type harms were also driven by under-investment and language gaps, but the 2016 and Amnesty evidence suggests amplification multiplied them.

**Why not "advertising" as the master cause?** Advertising is the *financial* reason for the objective, and it is the deeper root. Substack is the control case: no ads, yet it drifted toward engagement features under venture growth pressure, and its take-rate still profits from inflammatory content. The *mechanism* that did the harm was the optimization target, and that target can be driven by ads, by VC growth metrics, or by DAU targets. [INFERENCE] **If forced to name one line in the code, it is the objective function. If forced to name one line in the P&L, it is revenue proportional to attention.** They are the same fact seen from two sides.

**Honest caveat on the master cause**: the Meta-academic 2020 election studies (*Science* and *Nature*, July 2023; Guess, Nyhan, Tucker et al.) found that switching users to chronological feeds for about three months during 2020 **reduced time on platform and exposure to some untrustworthy content but did not measurably change polarization or political attitudes** over that period. [FACT] That result cautions against assuming algorithmic de-optimization alone would quickly reverse effects that have already formed. It is also consistent with the long-tail thesis that the damage became embedded in behavior, supply (what creators and politicians produce), and social structure, beyond what a three-month feed switch could undo. [INFERENCE]

---

# PART (c): CANDID STATEMENT OF UNCERTAINTY AND GAPS

1. **Time horizon.** I wrote this without web access. My knowledge is densest through 2024, reasonably good through mid-2025, and patchy for late 2025 through 2026. In particular:
   - **Social media adolescent addiction litigation (JCCP in Los Angeles; federal MDL 3047 in Oakland)**: bellwether trials were scheduled for late 2025 and 2026, and I understand some defendants (for example Snap, and possibly TikTok) settled individual bellwether claims shortly before trial in early 2026. **I do not reliably know verdicts or outcomes.** Anything I would say about them would be speculation.
   - **The New Mexico v. Meta and state AG cases**: I do not know their current status.
   - **FTC v. Meta**: I believe it was decided for Meta in November 2025, with moderate confidence. I don't know if there was an appeal.
   - **TikTok US joint venture**: I have low-moderate confidence on the closing date, ownership percentages, and whether the algorithm is truly retrained or retains ByteDance dependencies.
   - **Meta's 2025 scam-ad revenue reporting and the "Project Mercury"/17-strike allegations**: reported late 2025. I am confident they were reported but less sure of the exact figures.
   - **The Substack July 2025 push-notification incident and Series C figures**: moderate confidence.
   - **DZ Reserve v. Meta (Potential Reach)**: I am unsure of its final posture, including any Supreme Court involvement.
2. **Figures are from memory.** The headline numbers I am most confident of are: 87M (Cambridge Analytica), $5B (FTC 2019), 5.8M (XCheck), 64% (extremist joins), one-in-three (body image), 13% (BEEF), 260 videos, 1.5 minutes, $170M (COPPA), 70% (YouTube recommendations share), 126M (IRA reach), and 689,003 (emotional contagion). Secondary figures (for example $0.02–0.04 creator fund RPM, 87% misinformation budget, 15–30x MSI weights, 1.1M under-13 reports, 144 Kenyan moderators) should be checked against primary sources.
3. **Leaked documents are partial.** The Haugen corpus, the TikTok Kentucky exhibits, and the Bloomberg YouTube sources are curated slices. Companies argue they omit context, such as research showing benefits, or fixes that were adopted later. I have tried to tag them, but a reader should know that **Meta is massively over-represented in this reckoning because Meta leaked most.** YouTube and TikTok may have comparable or worse internal findings that never surfaced. The relative severity ranking of platforms is therefore partly an artifact of which companies had whistleblowers. [INFERENCE]
4. **The science is genuinely contested in two key areas.**
   - **(a) Teen mental health causation at the population level.** The Haidt/Twenge position and the Odgers/Orben/Przybylski position both have serious evidence. I have not claimed population-level causation as fact.
   - **(b) Algorithmic radicalization.** Strong on mechanism and anecdote, weaker on quantitative causal evidence post-2019, and unmeasured for the peak 2012–2018 era.

   The strongest ground for prosecution is the **knowledge-action gap**, not contested epidemiology.
5. **Areas I covered thinly or omitted.**
   - Non-English-language reporting (for example Brazilian, Indian, Indonesian, Filipino, and African investigative journalism) that likely documents failures I don't know.
   - WhatsApp's role in India lynchings (2017–2018) and Brazil elections (2018). It is Meta's, but I folded it out for focus.
   - Accessibility failures.
   - Environmental footprint.
   - Detailed EU DSA enforcement outcomes (2024–2026).
   - Detailed financial disclosures on moderation spend.
   - Threads.
   - Facebook Marketplace fraud.
   - Instagram's role in the drug trade (fentanyl-laced pill sales to teens, which also involves Snapchat heavily).
   - Substack's payments and chargeback disputes.
   - YouTube Music and Kids-specific internal research, of which I know little.
6. **Most likely errors.**
   - Exact dates to the month.
   - Precise attribution of who proposed or vetoed a specific internal fix (for example, the Zunger attribution in the YouTube story, and which executives signed off on shelving Common Ground).
   - Exact names of internal projects mentioned only in litigation ("Project Meramec," "Project Mercury").
   - Recollection may blend similar reports. For example, the WSJ and NYT investigations into YouTube child-video recommendations (2019), and several CCDH reports.
7. **Positional bias.** This task was framed as a prosecution. I have tried to include the strongest defensive evidence (the Meta 2020 election studies, the Hosseinmardi and Chen YouTube studies, Substack's data portability, Meta's claims of small-sample research), but the framing may still bias selection. A defense brief would also emphasize real benefits these platforms produced: connection for isolated and marginalized people, creator livelihoods, organizing (for example the 2011 Arab Spring and #MeToo), and access to education (YouTube). A complete historical judgment must weigh them. This document does not.

---

*End of reckoning.*
