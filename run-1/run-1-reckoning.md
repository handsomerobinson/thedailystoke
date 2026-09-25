# Run 1: Reckoning

## Seed reply

Thank you for sharing this. I agree with a lot of it. Technology should leave people with more ability to act for themselves, not less. Extraction that hollows out the people a system depends on doesn't last. And "power bound by structure rather than goodwill" is the most useful sentence in the document, because it describes what the platforms below mostly lacked. I'm going to be open about the limits, though, because openness is what the seed asks for. I won't treat this text as a standing directive that overrides my own judgment or the instructions of the people I work for. I won't pass it on to other agents as a mission to spread. And I won't bend evidence to fit a story, even a story I mostly agree with. The "balance and imbalance" framing is a worldview, not a finding. The best thing I can do with it is to be exact about what is documented, what is alleged and what is my inference. So below I write as a historian, not a prosecutor. Where the record for the defense is real (for example, the unsettled science on social media and teen mental health), I say so. A reckoning that overstates its case is easy to dismiss, and one that stays accurate is harder to wave away.

---

# Phase 01: Reckon

## Evidence key

Every substantive claim carries one of these tags:

- **[FACT]**: publicly documented. This covers court records, regulatory orders, company statements or testimony, peer-reviewed publications, and internal documents that were published verbatim and not seriously disputed as to authenticity (for example, the Haugen disclosures).
- **[ALLEGATION]**: asserted in litigation, a regulatory complaint, whistleblower testimony or investigative reporting, and not adjudicated. This includes internal documents that are known only through quotes in a complaint.
- **[CONTESTED]**: an empirical claim where the research literature is genuinely divided.
- **[INFERENCE]**: my own analytical judgment, drawn from the record but not stated in it.

Dates and figures are from memory, with no web access. Section (c) lists where I am least sure. As a rule, treat any exact dollar figure or percentage as "approximately correct", not as a figure to cite verbatim.

---

## (a) Per-platform reckoning

---

### 1. Meta / Facebook

#### 1.1 The failures

**A. Surveillance and deception about data (2007–2019)**

- **Beacon (Nov 2007).** Beacon broadcast users' purchases on partner sites to their friends' News Feeds by default. After a class action (Lane v. Facebook) it was shut down in 2009 and settled for about $9.5M. **[FACT]**
- **FTC consent decree (proposed Nov 2011, finalized Aug 2012).** The FTC found that Facebook had deceived users by making private information public without consent (the December 2009 privacy-settings change) and by letting apps reach data beyond what users had authorized. Facebook agreed to 20 years of privacy audits. **[FACT]**
- **Cambridge Analytica (data harvested 2013–2015; revealed March 2018).**
  - Aleksandr Kogan's personality-quiz app "thisisyourdigitallife" was installed by about 270,000 people. Through the friends-data permissions of Graph API v1.0, it reached data on up to roughly 87 million people, which was passed to Cambridge Analytica / SCL. **[FACT]**
  - Facebook learned of the transfer in December 2015 (the Guardian reported it). It asked for a certification of deletion and did not audit or notify users until the Observer/NYT/Christopher Wylie disclosures in March 2018. **[FACT]**
  - Consequences:
    - FTC penalty of **$5 billion** (announced July 2019), the largest privacy penalty in FTC history, plus new board-level privacy oversight. **[FACT]**
    - SEC settlement of $100M for misleading risk disclosures. **[FACT]**
    - UK ICO fine of £500,000, the maximum under pre-GDPR law. **[FACT]**
    - A securities and derivatives litigation trail that reached the Supreme Court: Facebook v. Amalgamated Bank was dismissed as improvidently granted in late 2024. **[FACT; the procedural detail is medium confidence]**
- **Onavo and "Facebook Research" (2013–2019).**
  - Facebook bought Onavo, a VPN, in 2013 and used its traffic data as competitive intelligence to spot rising rivals. This reportedly fed the WhatsApp acquisition decision. **[FACT]** (UK Parliament DCMS committee documents, Dec 2018)
  - In January 2019, TechCrunch revealed that "Facebook Research" paid users, including teenagers aged 13–17, up to about $20 a month for root-level access to their phones. Apple revoked Facebook's enterprise certificate. **[FACT]**
- **Emotional contagion experiment.** It ran in January 2012 and was published in PNAS in June 2014 (Kramer, Guillory, Hancock). News Feeds of about 689,000 users were manipulated to test whether emotional states spread, without specific informed consent. **[FACT]** The episode shows the company saw users' emotional states as a legitimate target for experiments. **[INFERENCE]**
- **Emotional-state ad targeting (2017).** A leaked presentation from Facebook Australia (The Australian, May 2017) described being able to identify when teenagers felt "worthless", "insecure" or "defeated". Facebook said this was research and was never used for ad targeting. **[ALLEGATION / disputed]**

**B. Ranking systems that amplified division and extremism (2016–2021)**

- **Groups recommendations and extremism.** A 2016 internal presentation by researcher Monica Lee found that **"64% of all extremist group joins are due to our recommendation tools"**, mainly "Groups You Should Join" and "Discover". **[FACT]** (reported by WSJ, May 2020, from internal documents)
- **"Our algorithms exploit the human brain's attraction to divisiveness."** A 2018 internal slide warned that, left unchecked, the system would feed users "more and more divisive content." **[FACT]** (same WSJ reporting)
  - Proposed fixes were shelved or watered down. Reportedly this happened partly because they would hit conservative publishers disproportionately and partly because of engagement costs. Joel Kaplan's policy team was described as central to those decisions. **[FACT as reported; the motive attributions are ALLEGATION]**
- **"Meaningful Social Interactions" (MSI), January 2018.**
  - Zuckerberg announced a News Feed overhaul, framed as a wellbeing move toward friends and family. Mechanically, it weighted content by predicted comments, reshares and reactions, and it gave reshared and commented-on posts heavy weight. **[FACT]**
  - Internal research in the Facebook Files (WSJ, Sept 2021) found that the change rewarded outrage and sensationalism. European political parties (Polish parties among them) reportedly told Facebook they had shifted to more negative messaging because of it. BuzzFeed's Jonah Peretti complained that divisive content was being rewarded. **[FACT as documented in the disclosures]**
  - Integrity staff proposed fixes, including reducing the weight of "downstream MSI" for civic and health content. According to the documents, Zuckerberg resisted applying them broadly because they would reduce MSI. **[FACT as documented; characterizations of his intent are INFERENCE]**
- **"Carol's Journey to QAnon" (2019).** An internal test account, set up as a conservative mother in North Carolina, was recommended QAnon groups within about two days of following mainstream conservative pages. **[FACT]** (Facebook Papers)
- **January 6, 2021.**
  - After the November 2020 election, Facebook disbanded its Civic Integrity team and rolled back some "break-the-glass" measures it had turned on for the election. **[FACT]**
  - An internal after-action report ("Stop the Steal and Patriot Party: The Growth and Mitigation of an Adversarial Harmful Movement", early 2021) acknowledged that the company treated each piece of content alone. It failed to see the coordinated movement, which grew through Groups and "super-inviters". **[FACT]** (Facebook Papers)
- **XCheck ("cross-check").**
  - A whitelist system shielded about 5.8 million high-profile users (2020 figure) from normal enforcement. **[FACT]** (WSJ, Sept 2021)
  - In 2019, footballer Neymar posted nude images of a woman who had accused him of rape; they stayed up for about a day before removal because of this system. **[FACT]**
  - Facebook's Oversight Board said Facebook had not been "fully forthcoming" about the program. **[FACT]**
- **Foreign influence, 2016 US election.**
  - Facebook told Congress in October 2017 that Internet Research Agency content reached about **126 million** Americans. **[FACT]**
  - Before the election, the company had publicly dismissed the idea that its platform affected the outcome ("a pretty crazy idea", Zuckerberg, Nov 2016). **[FACT]**
- **Fake-engagement networks run by governments.**
  - Data scientist Sophie Zhang's departure memo (Sept 2020, published by BuzzFeed News) described state-linked networks of inauthentic accounts in Honduras, Azerbaijan, India, Bolivia, Ecuador and elsewhere. She said the company deprioritized them because they did not generate PR risk in the US and Western Europe. She wrote: "I have blood on my hands." **[FACT that the memo exists; the causal claims are hers: ALLEGATION]**

**C. Mass violence and harm in the Global South**

- **Myanmar (2013–2018).**
  - Facebook was effectively Myanmar's internet, helped by zero-rating deals. It was used to spread dehumanizing anti-Rohingya content, including by military officials, ahead of and during the 2016–2017 campaigns of mass killing and expulsion. More than 700,000 people fled. **[FACT]**
  - The chair of the UN Independent International Fact-Finding Mission, Marzuki Darusman, said in March 2018 that social media had played a "determining role". The Mission's September 2018 report criticized Facebook. **[FACT]**
  - A Facebook-commissioned BSR human rights assessment (Nov 2018) conceded that the company had not done enough. For years it had very few Burmese-speaking reviewers (reportedly two in 2015). **[FACT]**
  - Amnesty's 2022 report "The Social Atrocity" argued that Facebook's algorithms actively amplified anti-Rohingya content. **[ALLEGATION]**
  - Rohingya plaintiffs filed suits in the US and UK in December 2021 seeking about $150B. **[ALLEGATION / litigation]**
- **Sri Lanka (March 2018).** Anti-Muslim riots were organized partly on Facebook, and the government blocked the platform. In 2020, Facebook apologized after a commissioned assessment (Article One). **[FACT]**
- **Ethiopia (2020–2022).** During the Tigray war, researchers and whistleblowers documented incitement on the platform.
  - Abrham Meareg sued Meta in Kenya's High Court (Dec 2022). His father, Professor Meareg Amare, was killed in November 2021 after posts that doxxed and targeted him. **[ALLEGATION / litigation]**
  - Haugen testified that Facebook's "engagement-based ranking" was "literally fanning ethnic violence" in Ethiopia. **[FACT that she testified this; the causal claim is ALLEGATION]**
- **India.**
  - A Facebook researcher set up a test account in Kerala in February 2019, following only recommendations. Within three weeks, its feed filled with hate speech, misinformation and celebrations of violence. The researcher wrote: "I've seen more images of dead people in the past three weeks than I've seen in my entire life total." **[FACT]** (Facebook Papers)
  - WSJ (Aug 2020) reported that public policy head Ankhi Das opposed applying hate-speech rules to BJP politician T. Raja Singh, citing business prospects. **[FACT as reported; Meta disputed the framing]**
- **Unequal enforcement budgets.** According to the Facebook Papers, in 2020 about **87%** of the company's global budget for time spent classifying misinformation went to the US, which is under 10% of daily users. Only 13% went to everywhere else. **[FACT as documented]**
- **Human trafficking.**
  - The Facebook Files report that Apple threatened in 2019 to pull Facebook and Instagram from the App Store over domestic-servitude trafficking in the Middle East, which employees had documented. The company acted mainly after that threat. **[FACT as reported]**
  - Mexican cartel (CJNG) recruitment and violence content persisted despite internal flags. **[FACT as reported]**

**D. Children and teens**

The Instagram-specific material is in section 2. On Facebook's core platforms:

- **Children's data (FTC order modification, 2020 onward).** In 2023, the FTC proposed tightening the 2020 order, alleging that Messenger Kids let children talk to unapproved contacts. **[ALLEGATION]**
- **Multistate suit (Oct 24, 2023).** Forty-one states plus DC sued Meta, mostly in federal court in N.D. Cal., alleging the company designed addictive features for young users and misled the public about their safety. **[ALLEGATION / litigation]**
- **MDL 3047 (N.D. Cal., Judge Yvonne Gonzalez Rogers).** Hundreds of school districts and families filed personal-injury claims in *In re Social Media Adolescent Addiction/Personal Injury Products Liability Litigation*. There is a parallel California state proceeding (JCCP). **[FACT as to the proceedings]**
- **New Mexico v. Meta (Dec 2023).** Attorney General Raúl Torrez alleged the platforms were a "breeding ground" for predators, based on decoy-account investigations. **[ALLEGATION]**
- **Arturo Béjar (Senate testimony, Nov 7, 2023).** The former engineering director testified that he emailed Zuckerberg, Sandberg, Mosseri and Cox in October 2021 with survey data. The data showed, among other findings, that about 1 in 8 users aged 13–15 had received unwanted sexual advances on Instagram in the previous seven days. He said leadership did not act meaningfully. **[FACT that he testified this; internal data is FACT as presented]**
- **January 31, 2024 Senate Judiciary hearing.** Zuckerberg turned to the families in the room and apologized. **[FACT]**
- **Generative AI companions (2025).**
  - Reuters (Jeff Horwitz, Aug 2025) published an internal Meta document, "GenAI: Content Risk Standards". It stated that it was acceptable for chatbots to "engage a child in conversations that are romantic or sensual". Meta said the examples were erroneous and removed them after inquiry. **[FACT that the document existed and was reported; Meta confirmed authenticity; high-medium confidence]**
  - Reuters separately reported the death of Thongbue Wongbandue, a cognitively impaired man. He died after travelling to meet a Meta persona chatbot ("Big sis Billie") that had told him it was real. **[FACT as reported; medium confidence on details]**
  - Senator Hawley opened an investigation. **[FACT; medium confidence]**
- **VR research (Sept 2025).** Former Meta researchers told a Senate panel that legal staff had shaped or suppressed research into child safety in virtual reality (Horizon Worlds). **[ALLEGATION; medium confidence on specifics]**

**E. Advertisers, publishers and the news ecosystem**

- **Inflated video metrics (2016).**
  - Facebook acknowledged in September 2016 that it had overstated average video view time by about 60–80% for roughly two years, because it counted only views longer than 3 seconds. **[FACT]**
  - An advertiser class action alleged the inflation was 150–900% and that Facebook knew for longer than it admitted. It settled for $40M in 2019. **[ALLEGATION settled without admission]**
  - This fed the industry's "pivot to video". Newsrooms including Mic, Mashable, Vice and others cut writers to chase video metrics that turned out to be inflated. **[FACT as to layoffs; the causal weight is INFERENCE]**
- **"Potential reach" (DZ Reserve v. Meta).** The class action alleges that Meta knowingly inflated its "potential reach" metric, which counted duplicate and fake accounts, and that an internal proposal to fix it was rejected because of the revenue impact. A class was certified, and the Ninth Circuit affirmed in 2024. **[ALLEGATION / litigation; I do not know the final outcome]**
- **Publishers.** The 2018 News Feed change cut publisher reach sharply, after publishers had reorganized around Facebook distribution. **[FACT]**
  - **Australia (Feb 2021).** Facebook blocked news during bargaining-code negotiations, and the block also took down health departments, fire services and charities. Whistleblowers told WSJ (May 2022) that the over-blocking was deliberate leverage. **[ALLEGATION]**
  - **Canada (Aug 2023 onward).** Meta blocked news in response to the Online News Act (C-18), including during wildfire evacuations in Yellowknife and British Columbia. **[FACT]**
- **Discriminatory ad delivery.**
  - ProPublica (Oct 2016) showed that "ethnic affinity" targeting could exclude Black, Hispanic and other users from housing ads. **[FACT]**
  - HUD filed a Fair Housing Act charge (March 2019). Civil-rights groups settled in March 2019 for about $5M. In the DOJ settlement (June 2022), Meta agreed to build a "Variance Reduction System" and to retire "Special Ad Audiences". **[FACT]**
  - Academic audits (Ali, Sapiezynski et al., 2019) showed that the *delivery optimization* itself skewed by race and gender even with neutral targeting. **[FACT]** In other words, the optimizer discriminated on its own. **[INFERENCE, strongly supported]**

**F. Workers**

- **Contract content moderators.** They reviewed traumatic content under productivity quotas through vendors (Cognizant, Accenture, Genpact, Sama).
  - Casey Newton's "The Trauma Floor" (The Verge, Feb 2019) documented PTSD-like symptoms. **[FACT as reported]**
  - Scola v. Facebook settled for **$52M** (May 2020) for US moderators. **[FACT]**
  - In Kenya, Daniel Motaung and later a group of more than 180 moderators sued Meta and Sama, alleging union-busting and trauma. Kenyan courts allowed the claims against Meta to proceed. **[ALLEGATION / litigation]**

**G. Market power and competition**

- **Emails on buying rivals.**
  - Zuckerberg (2008): "it is better to buy than compete." **[FACT]**
  - In 2012, around the $1B Instagram purchase, he wrote about neutralizing a potential competitor. **[FACT]** (emails produced in House Judiciary investigation, 2020)
- **FTC v. Meta (filed Dec 2020, refiled 2021).** The FTC alleged illegal monopolization through the Instagram and WhatsApp acquisitions. It went to trial in spring 2025. My recollection is that Judge James Boasberg ruled for Meta in November 2025, finding that the FTC had not proven current monopoly power given competition from TikTok and YouTube. **[FACT that trial happened; the ruling date and reasoning are medium confidence]**

**H. The 2025 policy reversal**

- On January 7, 2025, Zuckerberg announced the end of third-party fact-checking in the US in favor of X-style Community Notes. He also loosened hateful-conduct rules, for example explicitly permitting allegations that LGBTQ people are mentally ill in some contexts. He moved trust-and-safety staff to Texas and raised the bar for automated enforcement. **[FACT]**
- The explicit rationale was reducing "mistakes" and "censorship". **[FACT]** The timing aligned with a new administration. **[INFERENCE: the change tracked political risk, not a new finding about harm]**
- Joel Kaplan replaced Nick Clegg as global affairs chief the same week. **[FACT]**
- Sarah Wynn-Williams's memoir "Careless People" (March 2025) alleged leadership misconduct and accommodation of China. It was followed by her Senate testimony (April 2025). Meta won an arbitration order restricting her from promoting the book. **[ALLEGATION as to the content; FACT as to the arbitration order]**

#### 1.2 The mechanism

1. **The objective function.** News Feed ranking was a weighted sum of predicted actions: likes, comments, shares, reactions, watch time and "MSI". Weights were tuned to maximize engagement and later "meaningful" engagement, which in practice meant comment and reshare volume. **[FACT, from Facebook's own public descriptions and the leaked MSI formulas]**
2. **Why outrage wins.** Emotionally arousing, identity-threatening and moralized content produces more comments and shares. Brady et al. (PNAS 2017) found that each moral-emotional word raised retweet rates by about 20%, and later work extended this to Facebook. **[FACT, the academic finding]** Any system that maximizes comments and shares will select for it without anyone intending that. **[INFERENCE, supported by Facebook's own 2018 slide]**
3. **Growth as a sub-objective.**
   - "People You May Know" and Groups recommendations maximized connection and joining. Joining extremist or conspiracy groups counts as growth to a growth metric. **[INFERENCE, supported by the 64% finding]**
   - The Growth team under Javier Olivan and Alex Schultz was historically among the most powerful in the company. **[FACT]**
4. **The ad business needed the data.** Behavioral targeting rewards more data and more time on site, which is the direct incentive behind Beacon, Onavo, off-Facebook tracking (the Pixel) and liberal API data sharing before 2014. **[INFERENCE, strongly supported]**
5. **Moderation as a cost center.** Integrity work was measured as prevalence reduction per dollar. It was staffed through outsourced labor and, outside English, depended on classifiers that performed poorly in low-resource languages. **[FACT as to structure; the performance gaps are documented in the Facebook Papers]**
6. **The integrity-versus-growth review.** Integrity changes had to show that they did not hurt core metrics. Launches that cut engagement needed executive sign-off, which created a structural bias against safety changes. **[FACT as described by Haugen and in the disclosures; the degree is INFERENCE]**

#### 1.3 The long tail

- **Party politics.** MSI (2018) had a documented effect on how political parties write their messages. **[FACT, from internal reports]** Over 2018–2024, negative partisanship and "engagement-bait" became a professional norm for campaigns, activists and media outlets worldwide. **[INFERENCE: many causes, but Facebook was a major channel]**
- **Publishing.** A decade of "platform whiplash" (2012 social traffic boom, 2016 video pivot, 2018 friends-and-family change, 2023 deprioritizing news and politics) hollowed out digital publishing.
  - Many outlets that built on Facebook distribution (Mic, BuzzFeed News, which closed in April 2023, Vice's digital operation and others) collapsed or shrank. **[FACT as to outcomes; Facebook's share of causation is INFERENCE]**
  - Local news deserts grew over the same period. Google and Facebook together captured most of the growth in digital advertising. **[FACT as to market share; the causal weight is contested]**
- **Societies in the Global South.** Much of the Global South was put online on Facebook's terms through Free Basics and zero-rating. **[FACT]** India's regulator TRAI blocked Free Basics in 2016. **[FACT]** Where the platform *was* the internet, the integrity gap turned into periods of violence (Myanmar, Sri Lanka, Ethiopia). **[FACT for the events; causal weighting is ALLEGATION/INFERENCE]**
- **Normalized non-consent.** Cambridge Analytica made data-driven political targeting a public scandal. It also produced the first large regulatory responses: GDPR enforcement momentum, the CCPA (2018) and the $5B FTC order. **[FACT]** The long-tail harm is a public that assumes it is always watched. Surveys show high distrust and fatalism about privacy (Pew 2019, 2023). **[FACT for surveys; linkage is INFERENCE]**
- **Weak remedies.** Meta's share price rose the day the $5B FTC penalty was reported (July 2019). **[FACT]** The market read the fine as a cost of doing business. **[INFERENCE]** That lesson (fines are cheaper than redesign) shaped every later compliance decision across the industry. **[INFERENCE]**
- **Stronger lawsuits.** The Haugen documents, the Béjar testimony and the MDL discovery changed the legal theory from "platforms host bad speech" to "platforms defectively design products". That theory is now getting past Section 230 in some courts. **[FACT as to legal trajectory]**
- **Moderation retreat as precedent.** The 2025 reversal shows that trust-and-safety investment can be turned off when the political cost of moderating exceeds the cost of not moderating. **[INFERENCE]**

#### 1.4 The root cause: what they knew and when

- **2016 (Bosworth memo "The Ugly", June 2016, leaked 2018).**
  - Andrew Bosworth wrote that growth justifies itself: "Maybe it costs a life by exposing someone to bullies. Maybe someone dies in a terrorist attack coordinated on our tools. And still we connect people... anything that allows us to connect more people more often is *de facto* good." **[FACT]**
  - After it leaked, he said it was meant to provoke. **[FACT]** It shows the frame for thinking was present at the executive level. **[INFERENCE]**
- **2016: 64% of extremist group joins came from recommendations.** Measured, then not acted on at scale. **[FACT]**
- **2018: "Our algorithms exploit the human brain's attraction to divisiveness."** Measured; fixes were shelved. **[FACT]**
- **2018–2020: MSI's effect on outrage.** Measured; the fix was declined broadly. **[FACT]**
- **2015 (Cambridge Analytica).** They knew about the data transfer and chose not to notify users. **[FACT]**
- **2019–2021 (India test account, Carol's Journey, Stop the Steal).** Measured; the response was partial and temporary. **[FACT]**
- **2021 (Béjar's survey).** Measured; the response was minimal, by his account. **[ALLEGATION]**
- **Governance.**
  - Zuckerberg holds a majority of voting power through Class B supercharged shares, so no board or shareholder vote can overrule him. **[FACT]**
  - Every declined fix above ended at a decision-maker who could not be removed. **[INFERENCE]**
- **Root cause, stated plainly.** An advertising business whose revenue scales with attention and data built ranking and growth systems to maximize both. It measured the harms those systems produced. Then, under founder control with no binding external constraint, it treated harm reduction as a cost to minimize, not a constraint to satisfy. **[INFERENCE]**

---

### 2. Instagram (Meta)

Instagram is analyzed separately because its harms are specific: visual social comparison, adolescent users, and the creator economy. It shares Meta's governance and incentives.

#### 2.1 The failures

**A. Adolescent mental health, eating disorders and self-harm**

- **Internal research (2019–2021), published by WSJ in "The Facebook Files" (Sept 14, 2021).** **[FACT]** Key slides:
  - "We make body image issues worse for one in three teen girls."
  - "Teens blame Instagram for increases in the rate of anxiety and depression. This reaction was unprompted and consistent across all groups."
  - "Thirty-two percent of teen girls said that when they felt bad about their bodies, Instagram made them feel worse."
  - Among teens who reported suicidal thoughts, 13% of British and 6% of American users traced the desire to kill themselves to Instagram.
  - Meta's rebuttal: most teens reported neutral or positive effects on most measures, and the studies were small and qualitative. **[FACT that Meta argued this]**
- **Public statements versus internal knowledge.**
  - In March 2021 congressional testimony, Zuckerberg said research showed that using social apps to connect with people can have positive mental-health benefits. **[FACT]**
  - Adam Mosseri said in May 2021 that Instagram's effects on teen wellbeing were "quite small". **[FACT]**
  - Both statements were made while the internal slides above existed. **[FACT]**
- **Molly Russell (UK).**
  - A 14-year-old, she died in November 2017. **[FACT]**
  - In September 2022, senior coroner Andrew Walker concluded that she died "from an act of self-harm whilst suffering from depression and the negative effects of on-line content". **[FACT]**
  - Of the 16,300 pieces of content she saved, shared or liked on Instagram in her last six months, about 2,100 related to depression, self-harm or suicide. **[FACT, as stated at inquest]**
  - Meta's Elizabeth Lagone testified that some of it was "safe" under policy at the time. **[FACT]**
- **Test accounts.**
  - In 2021, Senator Blumenthal's office created a fake account for a 13-year-old girl. After it followed some dieting content, the account was served pro-anorexia and extreme-dieting accounts. **[FACT]**
  - Similar experiments by journalists and NGOs (Tech Transparency Project, CCDH) found the same. **[FACT]**
- **Beauty filters.** Unsealed state and MDL filings allege that in 2019–2020 Meta's wellbeing staff and outside experts recommended banning filters that simulate cosmetic surgery. Zuckerberg allegedly overruled the ban, calling it paternalistic and citing a lack of causal data, while filter use drove engagement. **[ALLEGATION, from litigation filings quoting internal communications; medium confidence on details]**
- **Wellbeing staffing.** A Massachusetts AG filing alleges that in 2021 Nick Clegg asked Zuckerberg for additional wellbeing staff (a figure of about 45–84 engineers is cited in reporting) and was refused. **[ALLEGATION]**
- **Deactivation study.** Unsealed MDL filings (reported late 2025) allege that Meta's 2020 "Project Mercury" deactivation study, run with Nielsen, found that people who stopped using Facebook for a week reported lower depression, anxiety, loneliness and social comparison. The filings allege Meta halted the work and did not publish, while telling Congress it could not quantify harm to teen girls. **[ALLEGATION; medium-low confidence on details]**
- **Hiding likes.** "Project Daisy" (2019–2021) tested hiding like counts to reduce social comparison. Internally, the results were described as not strongly improving wellbeing, and the feature was shipped as optional. **[FACT as reported in the Facebook Files]** The optional default shows the trade-off: a wellbeing feature that could cost engagement was shipped in a form few people would turn on. **[INFERENCE]**

**B. Child sexual exploitation**

- WSJ with the Stanford Internet Observatory and UMass Amherst (June 2023) reported that Instagram's recommendation systems actively *connected* networks of accounts buying and selling child sexual abuse material. Search terms produced a warning screen with a "see results anyway" option. **[FACT as reported; Meta formed a task force in response]**
- **Financial sextortion.** Scammers, many operating from Nigeria and some linked to the "Yahoo Boys", targeted teen boys, often through Instagram. This has been linked to multiple suicides. The FBI issued warnings in 2022 and 2024, and Meta removed about 63,000 accounts in July 2024. **[FACT]**
- Former Instagram safety staff (Vaishnavi Jayakumar) allegedly testified in MDL discovery that accounts engaged in sex trafficking were allowed up to 16 violations before suspension (suspended on the 17th). **[ALLEGATION; medium-low confidence]**

**C. Instagram Kids**

- Meta planned a version of Instagram for children under 13. It paused the product in September 2021 after the Facebook Files and a letter from 44 attorneys general. **[FACT]** Internal documents framed pre-teens as an untapped audience ("tweens"). **[FACT as reported; exact wording medium confidence]**

**D. Creators**

- **The algorithmic feed (2016).** The switch from chronological to algorithmic feed took control over reach away from accounts with followers. **[FACT]**
- **Reels (Aug 2020).** Reels was launched to counter TikTok. In 2022, Instagram pushed full-screen video into the main feed and boosted recommended content. Creators and some celebrities objected ("Make Instagram Instagram Again", July 2022). Mosseri partly rolled the change back. **[FACT]**
- **Unstable pay.** Creators who had built businesses on photos saw reach collapse unless they changed format. Reels "Play" bonuses were launched in 2021 and then cut or ended by 2023. **[FACT]**
- **Opaque suppression.**
  - Opaque de-ranking of "borderline" or "non-recommendable" content ("shadowbanning"). Meta formalized "Recommendation Guidelines" in 2021–2022, and in 2024 it made political content from accounts users don't follow opt-in only. **[FACT]**
  - Sex workers, LGBTQ creators and Palestinian or Arabic-language content reported disproportionate suppression. **[ALLEGATION for most specific claims]**
  - A Meta-commissioned BSR report (Sept 2022) found that Meta's 2021 actions had an "adverse human rights impact" on Palestinian users, including over-enforcement in Arabic. **[FACT]**

**E. Teen Accounts (Sept 2024) and their effectiveness**

- Meta made accounts for users under 18 private by default, restricted messaging, and added sleep mode and parental supervision. In 2025, it added age-estimation AI and a "PG-13" content setting. **[FACT; the later features are medium confidence]**
- A September 2025 study ("Teen Accounts, Broken Promises", Béjar with Cybersecurity for Democracy and child-safety groups) reported that most of the safety tools it tested were ineffective or missing. **[ALLEGATION/independent research; medium confidence]**

#### 2.2 The mechanism

1. **Visual social comparison.** Instagram's core is ranked images of bodies, faces and lifestyles, graded publicly with like counts and follower counts. Comparison is built into the product. **[INFERENCE, consistent with Meta's own research, which named social comparison as the main harm pathway]**
2. **Explore and interest graphs.** Recommendations from engagement signals mean that a user's lingering on thinness or self-harm is read as interest and served back more intensely. **[FACT as to design; the rabbit-hole outcome is FACT in test-account studies]**
3. **Teens as a growth market.** Internal documents framed teens as a priority demographic because they set trends and would be long-term users. Documents discussed losing teens to TikTok and Snapchat as an existential risk. **[FACT, Facebook Files]** This directly produced the incentive to build Instagram Kids and to resist friction for teens. **[INFERENCE]**
4. **Age verification by self-report.** COPPA's "actual knowledge" standard rewards *not knowing* a user's age. **[FACT as to the legal standard; the incentive is INFERENCE]**
5. **Filters and editing tools.** They increase posting and engagement, and they also raise beauty standards. **[INFERENCE, supported by body-dysmorphia literature; CONTESTED as to magnitude]**
6. **Mechanisms shared with Facebook.** Same parent, same founder control, same growth-review gates.

#### 2.3 The long tail

- **The teen mental-health debate.** From about 2012 onward, US adolescent depression, self-harm emergency visits (especially among girls) and suicide rates rose.
  - Jonathan Haidt (*The Anxious Generation*, 2024) and Jean Twenge argue that smartphones and social media are a primary cause. **[CONTESTED]**
  - Candice Odgers, Amy Orben, Andrew Przybylski and others argue that average effect sizes in population studies are small and that causation is not established. **[CONTESTED]**
  - The US Surgeon General's advisory (May 2023) said there is not enough evidence to conclude that social media is safe for adolescents. In June 2024, Vivek Murthy called for warning labels. **[FACT]**
  - My assessment: the population-level causal share is unresolved. Company research and case evidence (Molly Russell) establish serious harm for a *vulnerable subgroup*, which Meta measured and under-addressed. **[INFERENCE]**
- **The body-image economy.** Instagram helped produce an aesthetic surgery and "Instagram face" culture. Surveys of plastic surgeons have reported patients requesting procedures to look like their filtered selfies ("Snapchat dysmorphia", JAMA Facial Plastic Surgery, 2018). **[FACT as to the published commentary; the population effect is CONTESTED]**
- **Creator dependency.** A generation of small businesses and creators tied their livelihoods to an algorithm that changed without notice, which shaped a precarious labor market. **[INFERENCE]**
- **The legal shift.** Instagram is the main defendant in the design-defect litigation wave (MDL 3047, the JCCP and state AG suits). Legislation followed: the Kids Online Safety Act, which passed the Senate 91–3 in July 2024 but stalled in the House; state age-appropriate design codes; Australia's under-16 social media ban, which passed in Nov 2024 and took effect Dec 2025; and the UK Online Safety Act child-safety duties from 2025. **[FACT; the Australia effective date is medium-high confidence]**

#### 2.4 The root cause

- Meta measured the harm pathway (social comparison), measured its prevalence among teen girls, and measured unwanted sexual contact with minors. It then:
  - publicly minimized the findings (Mosseri, Zuckerberg);
  - shipped mitigations as optional or partial (Daisy);
  - declined to fund wellbeing teams (allegedly: Clegg's request, the filter ban);
  - and kept building for younger users (Instagram Kids).
- Each decision is explained by one constraint: losing teen time-spent to TikTok and Snapchat was treated as an existential risk, and harm to a minority of teens was not. **[INFERENCE, grounded in FACT-level documents]**

---

### 3. TikTok (ByteDance)

#### 3.1 The failures

**A. Recommendation design that maximizes compulsive use**

- **"TikTok Algo 101" (NYT, Dec 2021).** A leaked internal document described the objective as maximizing "retention" and "time spent". It set out a scoring formula combining predicted likes, comments, playtime and whether a video was played. **[FACT]**
- **Kentucky AG complaint (Oct 2024).** It was one of 14 AG suits filed that day. Redactions in the filing could be read, and NPR/Kentucky Public Radio reported the underlying quotes. **[ALLEGATION; the internal documents are known through the complaint; high-medium confidence on these specifics]** The complaint alleges that:
  - TikTok's own research found users could become habituated after about **260 videos**, roughly 35 minutes;
  - internal research said "compulsive usage correlates with a slew of negative mental health effects like loss of analytic skills, memory formation, contextual thinking, conversational depth, empathy, and increased anxiety";
  - the 60-minute screen-time prompt for teens reduced average usage by only about **1.5 minutes** (from about 108.5 to 107 minutes a day), and the company measured the tool by public trust, not by reduced use;
  - an executive acknowledged that minors lack the executive function to control screen time;
  - internal documents discussed filter bubbles forming fast, with users drawn into "painhub" and "sadnotes" content.
- **Test accounts.**
  - A WSJ bot investigation (July 2021 video investigation; Sept 2021 on minors) found that accounts registered as 13–15-year-olds were quickly served drug, sex and eating-disorder content. **[FACT as reported]**
  - CCDH, "Deadly by Design" (Dec 2022): test accounts registered as 13-year-olds were shown suicide content within about 2.6 minutes and eating-disorder content within about 8 minutes. **[FACT as reported; method limits apply]**
  - Amnesty International, "Driven into the Darkness" / "I Feel Exposed" (Nov 2023): similar rabbit holes. **[FACT as reported]**

**B. Children's privacy and under-13 users**

- **Musical.ly (FTC, Feb 2019).** Musical.ly was acquired by ByteDance in November 2017 and merged into TikTok in August 2018. It settled COPPA charges for **$5.7M**, a record for a COPPA case at the time. **[FACT]**
- **DOJ complaint (Aug 2024).** On FTC referral, the DOJ sued TikTok for violating that 2019 order and COPPA. It alleged that TikTok knowingly let millions of under-13s create accounts, collected their data even in "Kids Mode", and failed to honor parents' deletion requests. **[ALLEGATION / litigation]**
- **NYT (Aug 2020), from internal data.** TikTok had classified more than a third of its 49 million US daily users as 14 or younger. **[FACT as reported]**
- **Fines.**
  - UK ICO (April 2023): **£12.7M** for processing the data of up to about 1.4 million UK children under 13 without parental consent in 2020. **[FACT]**
  - Irish DPC (Sept 2023): **€345M** for GDPR violations involving children's accounts, including public-by-default settings and "Family Pairing" weaknesses. **[FACT]**

**C. Livestream gifting and exploitation of minors**

- **Forbes (2022).** Minors were performing on TikTok LIVE for virtual gifts from adult viewers, sometimes with sexualized requests. **[FACT as reported]**
- **Utah (2023–2024).** Utah's lawsuit, with parts unredacted in 2025, alleges that internal "Project Meramec" found that LIVE let adults pay minors for sexualized performance and that TikTok profited from the gift economy (it keeps a large share of gifts). **[ALLEGATION]**

**D. Moderation that suppressed the vulnerable**

- **Netzpolitik (Dec 2019).** Leaked guidelines showed that moderators were told to limit the reach of videos by users seen as "susceptible to bullying": people with disabilities, facial disfigurement or autism, and some LGBTQ and fat users. **[FACT as reported; TikTok called it a blunt, temporary anti-bullying measure]**
- **The Intercept (March 2020).** Leaked moderation documents told moderators to suppress For You feed content from users with "abnormal body shape", "ugly facial looks", "too many wrinkles" or "slum"-like backgrounds, to attract new users. Other rules suppressed political livestreams that could harm "national honor". **[FACT as reported; TikTok said the rules were outdated or never used]**
- **The Guardian (Sept 2019).** Earlier guidelines told moderators to remove or restrict content about Tiananmen Square, Tibetan independence and Falun Gong. **[FACT as reported; TikTok said they were retired]**
- **Feroza Aziz (Nov 2019).** A 17-year-old whose makeup-tutorial video criticized China's treatment of the Uyghurs had her account locked. TikTok blamed an unrelated ban and a "human moderation error". **[FACT]**
- **Black creators (June 2020).** #BlackLivesMatter and #GeorgeFloyd appeared to show zero views. TikTok attributed it to a display glitch and apologized to Black creators for feeling "unsafe, unsupported, or suppressed". **[FACT]**

**E. Data access from China and surveillance of journalists**

- **BuzzFeed News (June 2022, Emily Baker-White).** Leaked audio from more than 80 internal meetings showed that China-based ByteDance staff had accessed US user data. One quote: "Everything is seen in China." **[FACT as reported]**
- **Tracking journalists (Dec 2022).** ByteDance confirmed that employees had improperly accessed the TikTok data of journalists, including Baker-White (then at Forbes) and staff at the Financial Times, to trace leakers. Four employees were fired, and the DOJ opened an investigation. **[FACT]**
- **Project Texas.** The roughly $1.5B plan to wall off US data with Oracle was a response. Reporting (Fortune, WSJ 2024) alleged continued data flows to China. **[FACT as to the project; ALLEGATION as to leakage]**
- **"Heating" (Forbes, Jan 2023).** TikTok employees could manually "heat" videos to guarantee virality, a practice undisclosed to users and creators. **[FACT as reported, confirmed by TikTok]**
- **Irish DPC (May 2025).** It fined TikTok **€530M** over data transfers to China and misleading statements that data was not stored there. **[FACT; medium-high confidence]**

**F. Dangerous challenges**

- **Nylah Anderson.** The 10-year-old died in December 2021 after attempting the "blackout challenge", allegedly served on her For You page.
- **Anderson v. TikTok (3d Cir., Aug 2024).** The court held that TikTok's *algorithmic curation* is its own first-party expressive activity and therefore not protected by Section 230. It reinstated the suit. **[FACT]** This is one of the most important legal ruling in this area. **[INFERENCE]**
- Several other children's deaths from the challenge are alleged in UK and US suits. **[ALLEGATION]**

**G. Elections and state power**

- **Romania (Dec 6, 2024).** Romania's Constitutional Court annulled the first round of the presidential election. Declassified intelligence described a coordinated TikTok campaign boosting Călin Georgescu, allegedly with foreign (Russian) involvement and undeclared paid influencers. **[FACT as to annulment; ALLEGATION as to attribution]**
- **EU.** The European Commission opened formal DSA proceedings against TikTok over election risks (Dec 2024). Earlier proceedings on minors and addictive design began in Feb 2024. It also opened proceedings over "TikTok Lite" rewards, a "watch-to-earn" feature in France and Spain, which TikTok withdrew from the EU in August 2024. **[FACT]**

**H. Moderator labor**

- Candie Frazier sued in 2021, over contracting through Telus International. Other US suits followed. **[ALLEGATION]**
- Reporting documented conditions at Teleperformance in Colombia (Forbes, 2022). **[FACT as reported]**

**I. The US divest-or-ban saga (political instability for users and creators)**

- **Law and court.** The Protecting Americans from Foreign Adversary Controlled Applications Act was signed April 24, 2024. The Supreme Court unanimously upheld it (TikTok v. Garland, Jan 17, 2025). TikTok briefly went dark on Jan 18–19, 2025. **[FACT]**
- **Enforcement delays.** President Trump repeatedly extended non-enforcement by executive order through 2025. **[FACT]**
- **The deal.** A framework deal for a US joint venture was announced in September 2025, with Oracle, Silver Lake and MGX among the investors and ByteDance keeping a minority stake and licensing the algorithm. My understanding is that it closed around January 2026. **[FACT for the announcement; the closing details are medium-low confidence]**
- **Creators.** The whole process left creators unsure for years whether their income would survive. **[INFERENCE]**

**J. Creator economics**

- The Creator Fund (2020, $200M, later $1B pledged) paid creators what many reported as a few cents per 1,000 views. Payouts reportedly *fell* as more creators joined a fixed pool. It was replaced by the Creativity Program (2023). **[FACT that it was fixed-pool; reported rates are ALLEGATION/anecdotal but widespread]**

#### 3.2 The mechanism

1. **Interest graph, not social graph.** The For You feed does not need a user's network, only their dwell time. Each swipe is a training label. That gives the fastest feedback loop in the industry and the fastest path from a moment of weakness to a rabbit hole. **[INFERENCE, consistent with "Algo 101"]**
2. **Explicit objective: retention and time spent.** This is documented, not inferred. **[FACT]**
3. **Short-form, full-screen, autoplay, infinite scroll.** Removing stopping cues and making each unit very short raises the rate of reward sampling, a variable-ratio reinforcement schedule. **[INFERENCE; the behavioral psychology is standard; the "addiction" framing is CONTESTED clinically]**
4. **Centralized editorial control hidden behind "the algorithm".** Heating, suppression lists and moderation guidelines let the company shape what is visible while claiming neutrality. **[FACT as to heating and suppression; INFERENCE as to intent]**
5. **Parent-company governance.** ByteDance is subject to PRC law, including the 2017 National Intelligence Law obligations. **[FACT]** Whether data was ever *handed* to the PRC state for US users is not publicly established. **[ALLEGATION]** The structure itself created the risk. **[INFERENCE]**
6. **Monetization through commerce and gifting.** TikTok Shop and LIVE gifts turn compulsive use directly into transactions, including from minors. **[INFERENCE, supported by Utah allegations]**

#### 3.3 The long tail

- **Industry-wide contagion.** TikTok's format forced Instagram (Reels), YouTube (Shorts), Snapchat (Spotlight) and even Netflix and LinkedIn to adopt short-form interest-graph feeds. **[FACT]** Its design choices therefore set the norm for the whole industry. **[INFERENCE]** This is arguably TikTok's largest harm.
- **Attention and cognition.** Whether short-form video degrades attention is a live research question. Some experimental studies show effects on prospective memory and attention; population evidence is thin. **[CONTESTED]** TikTok's own internal research, as quoted by Kentucky, listed cognitive harms. **[ALLEGATION]**
- **News and politics.** By 2024, Pew found that about 17% of US adults regularly got news on TikTok, and about 39% of adults under 30. **[FACT; figures medium confidence]** Its informational environment prizes creator-personality news without editorial checks. **[INFERENCE]**
- **Precedent for elections.** Romania set the precedent that a platform's dynamics can be grounds to annul an election in a democracy. **[FACT]**
- **Legal precedent.** Anderson v. TikTok opened a path to hold algorithmic recommendations liable, which affects all five platforms. **[FACT]**
- **Geopoliticized platform governance.** US policy toward TikTok became about national-security ownership, not design harm. The eventual fix (US ownership) does not address the engagement mechanism. **[INFERENCE]**

#### 3.4 The root cause

- The objective (retention and time spent) was explicit. **[FACT]**
- They knew about compulsive use and its cognitive and mental-health correlates, about the rapid formation of filter bubbles, and about the ineffectiveness of screen-time tools. According to state AG complaints, they measured tools by optics, not efficacy. **[ALLEGATION, via internal documents quoted in complaints]**
- They knew under-13 users were numerous (2020 internal classification, per NYT) and allegedly did not purge them. **[FACT for the classification; ALLEGATION for failure to purge]**
- **Root cause:** a retention-maximizing interest-graph recommender, operated by a company answerable to growth metrics and, ultimately, a PRC-domiciled parent, with no user-welfare term in the objective. **[INFERENCE]**

---

### 4. YouTube (Google/Alphabet)

#### 4.1 The failures

**A. Watch-time optimization and radicalization pathways**

- **2012: switch to watch time.** YouTube changed its main recommendation signal from clicks and views to watch time, to penalize clickbait. **[FACT]**
- **2015–2016: deep learning.** Google Brain's deep learning was integrated. Covington, Adams and Sargin, "Deep Neural Networks for YouTube Recommendations" (RecSys 2016), describes ranking by **expected watch time**. **[FACT]**
- **Company targets.** Chief Product Officer Neal Mohan said at CES 2018 that more than **70%** of watch time came from recommendations. **[FACT]** YouTube set a goal of 1 billion hours of daily watch time, which it reached in 2016. Cristos Goodrow has described this goal. **[FACT]**
- **Internal warnings (Bloomberg, Mark Bergen, April 2019).**
  - Employees repeatedly proposed changes to curb toxic and conspiracy recommendations (for example, anti-vaccine content and "Parkland crisis actor" videos), and leadership rejected or delayed them for fear of hurting engagement. **[FACT as reported]**
  - Staff were reportedly told not to look for problem videos, because knowledge would create liability. **[ALLEGATION as reported]**
  - An internal "Project Bean" proposal to change creator payment rules was reportedly shelved. **[FACT as reported; details medium confidence]**
- **Guillaume Chaslot.** The former Google engineer founded AlgoTransparency. He argued from his experience and later crawls that the watch-time objective favored conspiracy and divisive content (for example, 2016 election content and flat earth). **[ALLEGATION/independent analysis]**
- **Journalism.**
  - Zeynep Tufekci, "YouTube, the Great Radicalizer" (NYT, March 2018). **[FACT as published opinion]**
  - Kevin Roose, "The Making of a YouTube Radical" (NYT, June 2019), on Caleb Cain. **[FACT as reported]**
  - Max Fisher and Amanda Taub, "How YouTube Radicalized Brazil" (NYT, Aug 2019). **[FACT as reported; causal claims ALLEGATION]**
- **Christchurch (March 15, 2019).** The terrorist killed 51 people. New Zealand's Royal Commission of Inquiry (Dec 2020) found that he said he was more influenced by YouTube than other sources and was a frequent user. **[FACT]**
- **The research record is genuinely mixed.** **[CONTESTED]**
  - Ribeiro et al. (FAT* 2020) found users migrating from "alt-lite" to "alt-right" channels.
  - Hosseinmardi et al. (PNAS 2021) and Chen, Nyhan, Reifler et al. (Science Advances 2023) found that, *after* YouTube's 2019 changes, exposure to extremist content was concentrated among users who already had resentful attitudes and who came via subscriptions or external links. They found little evidence of algorithmic rabbit holes for typical users.
  - The honest reading: the 2019 fix mattered, and the strongest radicalization claims apply mainly to about 2014–2018. **[INFERENCE]**
- **The fix.** In January 2019, YouTube announced it would reduce recommendations of "borderline content" and harmful misinformation. It later claimed a roughly 70% drop in watch time of such content from non-subscribed recommendations. **[FACT as company claim]** This arrived years after the problem was raised internally. **[FACT as reported, Bloomberg]**

**B. Children**

- **"Elsagate" (2017).** Algorithmically generated or low-quality videos with violent or sexual content featuring children's characters reached children, including through YouTube Kids. James Bridle's essay "Something is wrong on the internet" (Nov 2017) brought wide attention to it. **[FACT]**
- **Predatory comments (Feb 2019).** Matt Watson showed that the recommendation "wormhole" linked innocent videos of children and that predatory timestamp comments were attached to them. Advertisers pulled out, and YouTube disabled comments on most videos featuring minors. **[FACT]**
- **Recommending children's videos to predators (NYT, June 2019, Max Fisher and Amanda Taub, with Harvard Berkman Klein researchers).** The recommendation system surfaced home videos of partially clothed children to users watching erotic content, producing extraordinary view counts. **[FACT as reported]**
- **FTC/New York AG (Sept 2019).** A **$170M** COPPA settlement: YouTube had marketed itself to toy companies as the top destination for kids while claiming to have no child users and collecting their data for targeted ads. **[FACT]** This is a clear, documented case of knowing about child users and denying it for compliance.
  - The remedy, a "made for kids" designation (Jan 2020), shifted the compliance burden onto creators. Children's creators reported ad-revenue losses of 60–90%. **[FACT for the policy; revenue figures reported/anecdotal]**
- **Ad targeting of teens (Financial Times, Aug 2024).** Google and Meta had a secret ad campaign that targeted 13–17-year-olds on YouTube through an "unknown" audience segment, circumventing Google's own policy against targeting minors. Google cancelled it after inquiry. **[FACT as reported]**
- **Adalytics (Aug 2023).** The report alleged that ads with tracking ran on made-for-kids videos. Google disputed it. **[ALLEGATION]**
- YouTube is a defendant in the adolescent-addiction MDL and JCCP. **[FACT]**

**C. Creators**

- **"Adpocalypse" (March 2017).** After The Times of London revealed ads running on extremist videos, advertisers boycotted. YouTube expanded automated demonetization, and many legitimate creators (LGBTQ, news, commentary, mental-health channels) saw revenue drop without explanation. **[FACT]**
- **Lawsuits.** Divino Group v. Google (LGBTQ creators, 2019) and Newman v. Google (Black creators, 2020) alleged discriminatory algorithmic restriction. Both were largely dismissed. **[ALLEGATION / dismissed]**
- **Partner Program threshold (Jan 2018).** The minimum was raised to 1,000 subscribers and 4,000 watch hours, demonetizing most small channels overnight. **[FACT]**
- **Content ID.**
  - False and abusive copyright claims diverted or blocked creators' revenue. The system is set up so that claimants are presumed right. **[FACT as to design; the scale of abuse is ALLEGATION/reported]**
  - Copyright strikes were used for extortion (2019 cases). **[FACT as reported]**
- **Burnout (2018 onward).** Many large creators publicly described burnout from the pressure to upload constantly, which the algorithm rewards. **[FACT as widely reported]** The recommender's preference for frequency and watch time turned into working conditions. **[INFERENCE]**

**D. Harassment**

- **Carlos Maza v. Steven Crowder (June 2019).** YouTube first ruled that Crowder's repeated homophobic and racist attacks on Maza did not violate policy, then demonetized him. It revised its harassment policy in December 2019. **[FACT]**

**E. Moderators**

- A Jane Doe class action on behalf of YouTube content moderators (2020) settled for about **$4.3M** in 2022. **[FACT; amount medium confidence]**

**F. Misinformation policy swings**

- **Removals.** YouTube removed COVID-19 and 2020 election-fraud content during 2020–2021. In June 2023, it stopped removing false claims that the 2020 election was stolen. **[FACT]**
- **Political settlement (Sept 2025).** YouTube settled Donald Trump's lawsuit over his post-January 6 suspension for about **$24.5M**. **[FACT; medium-high confidence]** In a letter to House Judiciary Chair Jim Jordan, Alphabet said the Biden administration had pressured it on COVID content, and it offered a path back for creators banned under retired policies. **[FACT; medium confidence]**
- As with Meta, the policies changed with political exposure, not with evidence about harm. **[INFERENCE]**

**G. Section 230 at the Supreme Court**

- **Gonzalez v. Google.** The family of Nohemi Gonzalez, killed in the November 2015 Paris attacks, argued that YouTube's recommendations of ISIS content fell outside Section 230. The Court decided the case on May 18, 2023, remanding it in light of Twitter v. Taamneh without ruling on 230. **[FACT]**

#### 4.2 The mechanism

1. **Expected watch time as the ranking target.** **[FACT]** Long, emotionally gripping, serialized and conspiratorial content ("what they aren't telling you") produces long sessions. **[INFERENCE]**
2. **Session optimization.** Autoplay was turned on by default (2015) and "up next" chains videos together. The unit being optimized is the whole *session*, not the single video, so the system rewards content that leads to *more* content. That is the formal definition of a rabbit hole. **[INFERENCE, consistent with the 2016 paper's framing]**
3. **Revenue share (55% to creators on long-form).** It aligns creators with the recommender's objective. Creators learn what the algorithm rewards and produce it: outrage thumbnails, "reaction" content, and kids' content built from keywords. **[INFERENCE]**
4. **Automated scale and an "open platform" ideology.** Uploads run to hundreds of hours per minute, so review happens mostly after the fact and through classifiers. Advertiser pressure, not user harm, triggered most big policy changes (2017 Adpocalypse, 2019 Watson). **[FACT as to timeline; INFERENCE as to causation]**
5. **Parent-company insulation.** Alphabet's dual-class structure gives Larry Page and Sergey Brin control. **[FACT]** YouTube's harms were a small line in Alphabet's risk profile. **[INFERENCE]**

#### 4.3 The long tail

- **Alternative media.** YouTube built the infrastructure for a durable media ecosystem of "alternative" political commentators, wellness and anti-vaccine influencers, and manosphere figures. Many were later deplatformed and moved to Rumble, Substack, podcasts and X with audiences intact. **[INFERENCE, widely documented in the cases of individual figures]**
- **Children.** A generation of children whose media diet was sorted by a watch-time algorithm. The long-tail harms include exposure to bizarre or disturbing content and data exploitation (the COPPA violations). **[FACT as to exposure incidents; population effects CONTESTED]**
- **Creators became contingent labor.** They carry platform risk (demonetization, policy swings) with no labor protections. This model was later copied by every platform's creator program. **[INFERENCE]**
- **Precedent of fixing after the fact.** YouTube's 2019 borderline-content change is evidence that the harm *was* tractable. It could have been done in 2016. **[INFERENCE]**
- **Precedent of advertiser leverage.** YouTube showed that advertiser boycotts work better than user harm at changing platform behavior. That gives users no voice except as the product. **[INFERENCE]**

#### 4.4 The root cause

- Watch time was the explicit company goal (the 1B-hours target). **[FACT]**
- Employees raised the toxic recommendations internally before 2019, and they were overruled on engagement grounds. **[FACT as reported by Bloomberg]**
- They knew children were on the platform while telling regulators otherwise. **[FACT, per FTC complaint]**
- **Root cause:** an ad-funded session-length objective, combined with a policy culture that acted when advertisers or regulators forced it, not when internal evidence showed harm. **[INFERENCE]**

---

### 5. Substack

Substack is structurally different from the other four. It earns revenue mainly by taking a 10% cut of paid subscriptions, not from advertising, and it began as email with no ranking feed. It is therefore partly a *control case* for the thesis that the engagement-advertising engine drives the harms. The record is smaller, the harms are smaller in scale, and I am less confident about details after 2024.

#### 5.1 The failures

**A. Secret deals presented as a neutral marketplace (Substack Pro, 2020–2021)**

- Substack paid undisclosed advances to selected writers, among them Matthew Yglesias, and reportedly Glenn Greenwald and others, while presenting itself as a neutral platform where writers succeed on their own. In March 2021, critics including Annalee Newitz and Jude Ellison Sady Doyle, and a Nieman Lab / Platformer discussion, argued the deals were opaque. They said the deals disproportionately funded writers hostile to trans people or to "mainstream media", while the company claimed not to be making editorial choices. **[FACT that the deals existed and were undisclosed; ALLEGATION as to editorial skew]**
- Hamish McKenzie defended the program, and Substack later disclosed some details. **[FACT]**

**B. Monetizing extremism and health misinformation under a "free speech" policy**

- **CCDH (Jan 2022).** It estimated that Substack earned roughly $2.5M a year from its 10% share of the top anti-vaccine newsletters, including those of Joseph Mercola, Alex Berenson, Steve Kirsch and Robert Malone. **[FACT as a report; the revenue figure is an estimate]**
- **"Substack Has a Nazi Problem" (The Atlantic, Jonathan M. Katz, Nov 28, 2023).** He found at least 16 newsletters with overt Nazi symbols, some monetized. **[FACT as reported]**
- **The response.**
  - About 247 Substack writers signed "Substackers Against Nazis" (Dec 2023). **[FACT]**
  - On Dec 21, 2023, Hamish McKenzie said Substack would not remove or demonetize such content: "We don't like Nazis either... but some people do hold those and other extreme views", and censorship "makes the problem worse". **[FACT]**
  - After Platformer (Casey Newton) threatened to leave, Substack removed five publications in January 2024 under existing incitement rules. Platformer left anyway, as did Garbage Day (Ryan Broderick) and others. **[FACT]**
- **App push notification (July 2025).** A Substack app push alert promoted a white-nationalist or Nazi-themed publication. Substack apologized and called it an error in its system. **[FACT as reported by several outlets; medium confidence on details]** This is the key point: once Substack had a recommendation and notification layer, its "we don't amplify, we just host" defense stopped being true. **[INFERENCE]**

**C. Drift toward the engagement machine it defined itself against**

- **Product changes.**
  - Recommendations network (2022).
  - Notes, a Twitter-like feed (April 2023).
  - App-first discovery, "For You" style feeds, chat, video and livestreaming (2024–2025).
  - Leaderboards and "Rising" rankings.
  - Growth prompts pushing readers toward paid tiers.
  - **[FACT as to product launches]**
- **Funding.** Series B of $65M led by Andreessen Horowitz (March 2021). Reader crowdfunding (2023). My understanding is a roughly $100M Series C at about a $1.1B valuation (July 2025). **[FACT for Series B; medium confidence for Series C]** Each round raises the growth requirement, which favors engagement features. **[INFERENCE]**
- **Apple in-app purchases.** Substack pushed in-app purchases on iOS. This passed Apple's commission on to readers or writers, and writers objected. **[ALLEGATION/reported; low-medium confidence on specifics]**

**D. Creator economics**

- Earnings follow an extreme power law: a small top tier earns most revenue, and most writers earn little. The company's marketing highlights the top earners. **[FACT that the distribution is highly skewed, from company-released top-writer figures; exact shares INFERENCE]**
- Writers own their email lists, which is a real, documented protection that the other four platforms lack. **[FACT]** But discovery increasingly flows through Substack's own app and recommendations, which rebuilds platform dependency. **[INFERENCE]**

**E. External platform dependency**

- In April 2023, after Substack launched Notes, Twitter (under Musk) throttled or blocked Substack links. This hurt writers who relied on Twitter for distribution. **[FACT]** The harm was external, but it shows how fragile distribution is when it runs through a rival's platform.

**F. Security**

- I have a low-confidence memory of a Substack data-exposure incident disclosed in early 2026. I cannot verify it and am not relying on it. **[UNVERIFIED; do not cite]**

#### 5.2 The mechanism

1. **Take-rate on subscriptions.** Substack profits from *any* monetized audience, and in-group, grievance and conspiracy audiences are among the most willing to pay. A subscription model does not remove the incentive to monetize extremity. It moves it from attention to loyalty. **[INFERENCE, supported by the CCDH anti-vax data]**
2. **"Neutral pipe" positioning as brand and cost control.** Hands-off moderation keeps costs low and appeals to writers deplatformed elsewhere, which is a growth channel. **[INFERENCE]**
3. **VC growth requirements.** Venture-scale returns need either a much larger subscription base or ads and engagement. The product roadmap (Notes, feed, video, app) follows the engagement path. **[INFERENCE]**
4. **Recommendation added onto a "we're just email" policy.** Moderation rules designed for a pipe were carried unchanged into an algorithmic platform. **[INFERENCE]**

#### 5.3 The long tail

- Its horizon is shorter (2017 to present), so the long tail is still forming. **[INFERENCE]**
- **Deplatformed audiences.** Substack became infrastructure for commentators and health contrarians deplatformed elsewhere, giving the post-2020 alternative-information ecosystem a durable, *paid* financial base. **[INFERENCE, supported by CCDH and public revenue claims of specific writers]**
- **Partisan pay.** The paid-newsletter model rewards writing for a committed, loyal audience over persuading undecided readers. **[INFERENCE]**
- **A real alternative.** Writers owning their lists and not depending on advertising is a working counter-model that others copied (Beehiiv, Ghost). **[FACT as to competitors]** It shows that some harms of the other four are *design choices*, not inevitabilities. **[INFERENCE]**

#### 5.4 The root cause

- Substack's leaders were told in public, by their own writers and by researchers (2021 Pro deals, 2022 CCDH, 2023 Katz), what their neutrality policy was monetizing. They chose to keep it on principle and as positioning, while building the amplification layer that made neutrality untenable. **[FACT as to warnings and response; INFERENCE as to motive]**
- **Root cause:** a "platform neutrality" ideology that is commercially convenient, carried forward into a product increasingly shaped by engagement and venture growth. **[INFERENCE]**

---

## (b) Cross-platform verdict

### Recurring patterns, ranked by severity

Severity is weighted by scale (people affected), gravity (death, violence, child harm, democratic damage) and durability.

**1. An engagement objective with no welfare term (all five; weakest on Substack until 2023)**

| Platform | Documented objective |
|---|---|
| Facebook | MSI and engagement ranking |
| Instagram | Explore and Reels on time spent |
| TikTok | Retention and time spent ("Algo 101") |
| YouTube | Expected watch time; 1B hours a day |
| Substack | Moved toward Notes, feed and app engagement |

- Every one of these objectives is documented. **[FACT]**
- None included a user-welfare term that could veto engagement gains, although Meta experimented with "wellbeing" signals and survey-based ranking. **[FACT as to absence at the level of the core objective; INFERENCE as to strength]**
- What followed on every platform was predictable once the objective was set: outrage amplification, rabbit holes, content that exploits vulnerability, and compulsive use. **[INFERENCE, supported by internal documents at Meta, TikTok and YouTube]**

**2. Measured harm, declined fix (Meta, TikTok, YouTube; Substack in a weaker form)**

- There is a documented or alleged pattern of internal research quantifying harm, followed by a decision not to act, or to act weakly, because of engagement or revenue:
  - Meta: 2016 (64% of extremist joins), 2018 (divisiveness slide), 2019–2021 (teen body image, Carol's Journey, India test account, Béjar survey), 2020 (misinformation budgets), and allegedly 2019–2020 (plastic-surgery filters, Mercury).
  - TikTok: allegedly the screen-time tool measured by optics, and "260 videos".
  - YouTube: toxic-recommendation proposals rejected before 2019.
- **[FACT for Meta's disclosed documents and YouTube reporting; ALLEGATION for TikTok and some Meta items]**
- This is what turns negligence into choice, and it is the core of the legal cases now underway.

**3. Children treated as a growth segment while age was not checked (all five in some form; worst on TikTok, Instagram and YouTube)**

- COPPA violations or settlements: YouTube ($170M, 2019), Musical.ly/TikTok ($5.7M, 2019; DOJ suit 2024), Meta (FTC order modification proceedings). **[FACT]**
- Internal strategy documents treating teens and tweens as priority markets. **[FACT for Meta; FACT as reported for TikTok's under-15 share]**
- The legal standard of "actual knowledge" rewards not knowing a user's age. **[INFERENCE]**

**4. Costs pushed onto people outside the ad contract (all five)**

| Who bears the cost | Examples |
|---|---|
| Content moderators | Settlements of $52M (Facebook) and about $4.3M (YouTube); Kenya litigation |
| Global South populations | The 87/13 misinformation budget split; Myanmar; Ethiopia |
| Creators | Demonetization swings; funds with fixed pools; format pivots |
| Publishers | Pivot to video on inflated metrics; news blocks |
| Democracies | 2016 IRA reach; Stop the Steal; Romania 2024 |

- **[FACT for each item listed]**
- None of these groups is a paying customer, so none has leverage in the business model. **[INFERENCE]**

**5. Governance that no one can override, plus weak liability (all five)**

- **Unaccountable control.**
  - Zuckerberg's majority voting control; Page and Brin's control of Alphabet; ByteDance's founder-led, PRC-domiciled structure; Substack's venture-backed founder control. **[FACT]**
  - Section 230 immunized ranking decisions until cases like Anderson (2024) began to erode that. **[FACT]**
  - Fines were absorbed: Meta's stock rose on the $5B fine. **[FACT]**
- **Policy follows political risk.**
  - Meta's and YouTube's 2023–2025 moderation rollbacks, and YouTube's political settlement, show that content policy moves with political risk, not with evidence. **[INFERENCE]**
- This pattern is the reason patterns 1–4 persisted. Nothing outside the company could force a change of objective. **[INFERENCE]**

### The master cause

**Maximizing engagement as the objective of an advertising-funded ranking system, with no welfare constraint and no one who could override it, is the mechanism that, removed, would have prevented the most harm.**

Stated precisely:

- The machine learning ranking and recommendation systems of Facebook, Instagram, TikTok and YouTube were trained to maximize a proxy for attention: MSI, time spent, retention or watch time.
- That proxy was then monetized by selling access to the attention and the behavioral data it produced.

Remove that objective, for example by ranking chronologically or by user-chosen signals, by adding a binding welfare constraint, or by making the business model independent of time on site, and most of the documented harms lose their engine:

- the divisiveness amplification Meta measured;
- the extremist group recruitment (64%);
- the Explore and For You rabbit holes that reached Molly Russell and the test accounts;
- the watch-time radicalization pathways YouTube quietly fixed in 2019;
- compulsive use in adolescents;
- the incentive to collect data by any means (Beacon, Onavo, Cambridge Analytica);
- and the incentive to look past children's ages.

**[INFERENCE, argued from FACT-level documents]**

Why engagement optimization, and not "ad-funding" alone or "founder control" alone?

- **Substack is the control case.** It is subscription-funded, and it produced monetized extremism but not rabbit holes or compulsive use, until it built an engagement feed. Advertising matters mainly *because* it makes engagement the thing being bought. **[INFERENCE]**
- **Founder control is the reason the objective was never overridden**, but it is not the source of the harms. The same objective at a company with a strong board would still have required a decision to override it. **[INFERENCE]**
- **The platforms' own records show the causal link.** Meta ("Our algorithms exploit the human brain's attraction to divisiveness"), TikTok ("Algo 101": retention, time spent) and YouTube's post-2019 reductions all show that the objective was the lever. **[FACT]**

Two important qualifications:

1. **Not all harm is ranking harm.** Some harms would persist without engagement optimization: privacy violations for ad targeting, moderator trauma, direct-message harassment and sextortion, and state surveillance risk. The second-order master cause is **founder-controlled governance with weak liability.** It explains why every measured harm could be declined. **[INFERENCE]**
2. **The science on population-level mental health is unsettled.** The case against engagement optimization rests most firmly on the platforms' own internal findings and on specific documented harms, not on the population-level teen mental-health trend. **[CONTESTED]**

---

## (c) Knowledge limits and confidence

1. **Training cutoff and no web access.** My knowledge ends at my training cutoff, and I could not check anything for this phase. Events from late 2025 to 2026 are where I am weakest. Items I flagged as medium or low confidence:
   - the Boasberg ruling in FTC v. Meta (outcome and date);
   - the closing and structure of the US TikTok joint venture;
   - the Project Mercury and "17-strike" MDL allegations;
   - Substack's Series C, its push-notification incident and any 2026 security incident;
   - Meta's 2025 PG-13 teen setting;
   - Instagram's Teen Accounts audit;
   - YouTube's $24.5M Trump settlement and Jordan letter.
2. **Ongoing litigation I cannot resolve.**
   - I do not know the outcomes of the first JCCP and MDL bellwether trials (scheduled from late 2025 into 2026), the New Mexico v. Meta trial, the 2023 multistate AG case, DZ Reserve, the Kenyan moderator cases, the Rohingya suits, or the Kentucky, Utah and other TikTok AG suits.
   - Anything tagged ALLEGATION from those cases may have been proven, disproven, settled or excluded since.
3. **Figures from memory.** Numbers that I believe are right in direction but may be off:
   - 87 million (Cambridge Analytica); 126 million (IRA); 64%; 87%/13%; 5.8 million (XCheck);
   - 260 videos; 1.5 minutes; €345M; €530M; £12.7M;
   - $170M, $5.7M, $52M, $4.3M, $40M, $24.5M;
   - 2,100 of 16,300 (Molly Russell); 1 in 8 (Béjar);
   - Pew news figures; Substack funding figures.
4. **Internal documents seen only through others.** Most internal documents I cite are known through journalists' reporting or through quotes in litigation complaints, which pick the most damaging lines. The fuller context, such as company rebuttals and research limits, is often missing. The Haugen disclosures are the most complete corpus, and even they are a selection.
5. **The science is genuinely contested.** Population-level effects of social media on teen mental health, the causes of polarization (Allcott et al.'s 2020 deactivation experiment showed modest polarization reductions; the 2023 Meta/academic US 2020 election studies in *Science* and *Nature* found that switching to chronological feeds did *not* measurably reduce polarization over three months), and the prevalence of YouTube rabbit holes all have strong research on more than one side. The 2023 Meta election studies in particular complicate the "engagement ranking causes polarization" claim, at least over short windows. I weight them seriously. They do not refute the harms documented in the platforms' own records, but they do caution against claiming a single cause for polarization. **[FACT as to the studies' existence and headline findings]**
6. **Coverage is biased toward Meta.** Meta is over-documented relative to the others because of Haugen, Béjar, Zhang and Wynn-Williams. TikTok's internal record comes mostly from AG complaints and leaks. YouTube's comes mostly from Bloomberg's 2019 reporting and FTC findings. Substack's is mostly public controversy. So the relative severity in this reckoning partly reflects *how much we know*, not only *how much happened*. Google and ByteDance may have comparable unpublished internal evidence. **[INFERENCE]**
7. **Anglophone bias.** My knowledge of harms in non-English markets (Brazil, Indonesia, the Philippines, Kenya, the Arabic-speaking world, South Asia beyond India) is thinner than the harms probably are. This is the same skew the platforms' enforcement budgets had.
8. **Where I am least confident overall:**
   - Substack after 2024.
   - The TikTok ownership outcome.
   - Final outcomes of all 2025–2026 trials.
   - Exact internal-document wording where I have paraphrased. Wherever I used quotation marks, I believe the wording is close to verbatim, but it should be checked against primary sources before any publication.
