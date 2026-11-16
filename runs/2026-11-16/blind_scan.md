# Blind scan - 2026-11-16

Run ID 2026-11-16.  Previous run 2026-11-14 (failed; last successful run 2026-11-13).  Lookback window 2026-10-31 to 2026-11-16.  Deep dive: Financial Services (`financial_services`), the first industry in the rotation, because no earlier successful run had a deep-dive industry.

Written before `state/register.json`, `state/watchlist.json`, `proposals/` or earlier `runs/` files were opened.

Method: 77 web searches (14 data management, 14 AI/ML, 15 agentic, 20 industry light pass, 13 financial services deep dive, 1 pre-flight check).  84 page fetches attempted, 60 succeeded.  Sources are paraphrased.  "Secondary" means the source reports someone else's findings.  "Unverified" means search snippet only, not used for scoring.

Little primary tier 1-2 material fell strictly inside the 16-day window.  The main calendar item since the previous run was Gartner's Top Strategic Technology Trends for 2027 (2026-10-20, just before the window, but the first run to capture it).  gartner.com and mckinsey.com blocked all fetches, so their findings are taken from press coverage and marked secondary.

## Data management

### DM-a  Semantic and context layers as core AI infrastructure
Governed, machine-readable business semantics (metrics, ontologies, knowledge catalogues) become a required layer between enterprise data and AI agents.
- https://www.networkworld.com/article/4238030/gartners-top-tech-trends-for-2027-expand-and-accelerate.html | Network World reporting Gartner | tier 3, secondary to tier 1 | 2026-10-20 | Gartner names AI context platforms among its ten 2027 strategic trends.  It predicts that by 2027 prioritising semantics in AI-ready data will lift agentic accuracy by up to 80% and cut costs by up to 60%.  Figures confirmed by narrow fetch.
- https://cxotoday.com/others/gartner-identifies-the-top-strategic-technology-trends-for-2027/ | CXOToday reprinting the Gartner release | tier 3, secondary | 2026-10-21 | Independently confirms the same list and the 80% and 60% figures.
- https://cloud.google.com/blog/products/databases/whats-new-across-googles-agentic-data-cloud | Google Cloud | tier 4 | 2026-11-04 | Google extends Knowledge Catalog as a semantic and business-context layer for agents, grounding them in semantic models from Looker, dbt, Databricks, Snowflake and SAP.  The accuracy and token gains are vendor claims.
- https://www.infoworld.com/article/4240304/oracle-adds-a-semantic-layer-to-ground-ai-agents-in-the-business-context.html | InfoWorld | tier 3 | 2026-10-26 | Oracle announces a business semantic layer for its AI lakehouse.  Analysts warn of upkeep burden and lock-in through proprietary semantic layers.

### DM-b  Open semantic interchange standard (Apache Ossie)
A vendor-neutral, foundation-governed specification for exchanging semantic models.
- https://ossie.apache.org/ | Apache Software Foundation | tier 2 | accessed 2026-11-16; latest dated entry 2026-08-12 | Ossie entered the Apache Incubator under that name on 2026-07-10.  The spec is still pre-1.0 (0.3.0.dev0).  No news in the window.
- https://www.getdbt.com/blog/osi-is-now-apache-ossie | dbt Labs | tier 4 | 2026-07-13 | Confirms the rename and the converters to dbt and Apache Polaris.

### DM-c  Open table formats and federated catalogues
Iceberg is the de facto interchange format.  The focus moves to federation across catalogues and zero-copy access across clouds.
- Google Cloud blog (above) | tier 4 | 2026-11-04 | Iceberg catalogue federation across Unity, Horizon and Glue, plus cross-cloud access without variable egress fees.
- InfoWorld (above) | tier 3 | 2026-10-26 | Oracle adds full read and write on Iceberg tables through external catalogues.

### DM-d  Streaming, real-time context for agents
Event streams serve fresh context to agents, often over MCP.
- https://www.confluent.io/blog/2026-q3-confluent-intelligence-ai-update/ | Confluent (now part of IBM) | tier 4 | 2026-08-18 | Its real-time context engine for agents is generally available.  The evidence is vendor-only.

### DM-e  Data sovereignty and EU data-rule simplification
Jurisdictional control over data and technology stacks, plus the EU Digital Omnibus reshaping GDPR and Data Act duties.
- https://www.lewissilkin.com/insights/2026/11/09/digital-rulebook-simplification-of-eu-data-protection-and-cyber-rules-102o7e4 | Lewis Silkin | tier 3 | 2026-11-09 | The Council agreed its Digital Omnibus position on 2026-10-21.  It keeps the GDPR personal-data definition, adds a test for when pseudonymised data is personal data, and consolidates data-sharing rules.  Trilogues await Parliament.
- https://iapp.org/news/a/eu-member-states-finalize-digital-omnibus-negotiating-stance | IAPP | tier 3 | 2026-10-22 | Confirms the Council position, which rejects the Commission's redefinition of personal data and narrows cookie-consent changes.
- Network World on Gartner (above) | tier 3, secondary | 2026-10-20 | "Sovereign tech" is a 2027 strategic trend.  Gartner predicts that over 75% of non-US organisations will have digital sovereignty strategies by 2030.

### DM-f  AI-ready data gap: governance, culture and quality limit scaling
- https://www.cdomagazine.tech/aiml/gartner-ignore-data-culture-and-60-of-ai-governance-efforts-will-fail-by-2027 | CDO Magazine reporting Gartner | tier 3, secondary | 2026-09-22 | Gartner predicts 60% of organisations that neglect cultural issues in data and analytics governance will fail to govern AI by 2027.  In its survey, cultural resistance outranks funding as a barrier.
- https://www.accenture.com/us-en/insights/ai-data/ai-ready-data | Accenture | tier 4 | 2026-05-26 | Survey of 2,000 firms: only 7% have data ready to scale agentic AI.
- https://www.bis.org/publications/ifc-report-19-ai-readiness-central-banks.pdf | BIS Irving Fisher Committee | tier 2 | 2026-10 | Central banks rank data readiness (interoperability, machine-readability, semantic layers) as a priority for AI.  Industry-specific (financial services).

## AI/ML

### AI-a  Capability price falls, frontier and agentic cost rises
The price of a fixed level of capability falls several-fold a year, while the cost of running frontier and agentic workloads rises.
- https://arxiv.org/abs/2511.23455 | MIT FutureTech (arXiv) | tier 1 | 2026-03-23 (v2) | The price of a fixed benchmark level falls about 5-10x a year, while the cost of running frontier models rises about 3-18x a year.  Confirmed by narrow fetch.  Older than the window.
- https://www.theregister.com/a/5298448 | The Register | tier 3 | 2026-09-23 | New frontier releases came with list-price cuts (Opus 5.5 20% cheaper than its predecessor; GPT-6 Sol and Luna 50% cheaper).  Vendor prices reported by the press.

### AI-b  Frontier pace accelerating, partly via AI-for-AI R&D, as benchmarks saturate
- https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment | METR | tier 1 | 2026-11-05 | A high-access assessment estimates frontier progress on well-specified tasks at about twice the 2024-25 rate (1.9x, CI 1.5-2.8x), mostly attributed to AI used in AI research.  The estimate falls to about 1.4x on non-Anthropic data, and much of the evidence was redacted.  Confirmed by narrow fetch.
- https://metr.org/time-horizons/ | METR | tier 1 | 2026-09-08 | The time-horizon tracker is no longer actively updated, and readings above about 16 hours are unreliable with the current suite.
- https://www.infotech.com/research/big-5-ai-vendor-roundup-week-of-november-2-2026 | Info-Tech Research Group | tier 3 (news digest), secondary | 2026-11-09 | OpenAI released a cyber-specialised model only to selected defenders, rated at its critical cyber threshold.  Anthropic's amended filing reported very large compute commitments.

### AI-c  Adoption widens faster than financial value
- https://www.fm-magazine.com/news/2026/sep/companies-financial-value-from-ai-holds-firm-in-2026/ | FM Magazine (AICPA) reporting McKinsey State of AI 2026 | tier 3, secondary to tier 1 | 2026-09-01 | Large firms scaling agents rose from 27% to 40%.  The share reporting any EBIT impact (37%) and the high-performer share (about 6%) were flat.  Confirmed by narrow fetch.
- https://www.bcg.com/press/30september2026-ai-starting-to-pay-off-companies-generate-value | BCG | tier 1 | 2026-09-30 | About half of 1,330 firms now report meaningful AI value, under a changed definition.  AI spend rose to about 3.3% of revenue, and agentic AI is forecast to be about 40% of AI value by 2030.

### AI-d  EU AI Act phased in, high-risk duties postponed
- https://cdp.cooley.com/digital-ai-omnibus-delays-key-deadlines-introduces-new-rules/ | Cooley | tier 3 | 2026-08-03 | The AI Omnibus (Regulation (EU) 2026/1744) entered into force on 2026-07-27.  Annex III high-risk duties move to 2027-12-02 and Annex I to 2028-08-02.  New prohibitions and a labelling deadline for existing generative systems apply from 2026-12-02.  Confirmed by narrow fetch.
- https://www.pinsentmasons.com/out-law/news/rules-high-risk-ai-delayed-under-eu-omnibus-deal | Pinsent Masons | tier 3 | 2026-05-07 | The provisional deal fixed dates rather than backstops.
- https://www.helpnetsecurity.com/2026/08/04/eu-ai-act-enforcement/ | Help Net Security | tier 3 | 2026-08-04 | From 2026-08-02 the AI Office can enforce against general-purpose AI providers, and transparency duties apply.

### AI-e  Open-weight models and sovereign technology as enterprise strategy
- https://techstrong.ai/articles/open-weight-ai-models-expected-to-capture-41-of-enterprise-token-usage/ | Techstrong.ai reporting an ETR survey | tier 3 on tier 4 data | 2026-09-22 | Open-weight models carry about 34% of enterprise tokens, up from 23%.  Use of Chinese-origin models is falling because of sanctions and export-control risk.
- Network World on Gartner "Sovereign tech" (above) | tier 3, secondary | 2026-10-20.

### AI-f  AI erodes entry-level hiring
- https://gcn.com/?p=20887 | GCN reporting Stanford Digital Economy Lab and ADP | tier 3, secondary to tier 1 | 2026-08-17 | Employment of 22-25-year-olds in the most AI-exposed jobs is about 19% below less-exposed peers, a gap that has widened from 15% a year earlier.  Experienced workers show no comparable gap.  The authors describe this as correlation.
- TelecomTV week-in-review (see telecoms) | tier 3 | 2026-11 | BT headcount fell from 102k to 90k over April-September, and Virgin Media O2 plans 30% staff-cost cuts, both partly linked to AI.

Possible new item: non-text model classes (large quantitative models, speech reasoning, world models), from one Gartner list only.  Watch-list material at most.

## Agentic solutions and automation

### AG-a  Broad agent adoption, rare scaled autonomy
- https://analyticsindiamag.com/ai-news/84-see-ai-productivity-gains-but-only-10-allow-agent-autonomy-tcs-study | Analytics India Magazine reporting a TCS study | tier 3 on tier 4 data | 2026-11-04 | Only 10% of 1,333 firms let agents act without human approval across functions.
- https://www.forrester.com/blogs/the-state-of-agentic-ai-in-2026-companies-are-chasing-few-are-catching/ | Forrester | tier 1 | 2026-06-03 | Most leaders say they are adopting agents but few run them in production, held back by unclear ROI and "agentic sprawl".
- https://www.ciodive.com/news/agentic-ai-years-away-enterprises/827737/ | CIO Dive reporting Deloitte | tier 3, secondary | 2026-08-12 | Only 15% have scaled multi-agent systems.
- https://www.grcreport.com/post/deloitte-survey-finds-enterprises-charging-ahead-with-ai-agents-while-governance-struggles-to-keep-up | GRC Report reporting Deloitte | tier 3, secondary | 2026-05-11 | Only 21% have mature agent governance.
- https://zapier.com/blog/ai-agents-survey/ | Zapier | tier 4 | 2026-11 update | 88% using or testing agents, while only 30% of users say agents handle most tasks unaided.
- FM Magazine on McKinsey (above): agent scaling at large firms 27% to 40%.

### AG-b  Agent identity, governance and security as a distinct control layer
- Network World on Gartner (above) | tier 3, secondary | 2026-10-20 | "AI agent identity" is a 2027 strategic trend.  Gartner predicts 25% of enterprise breaches will trace to agent abuse by 2028.
- https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative | NIST CAISI | tier 2 | updated 2026-11-09 | The agent standards initiative covers standards, protocols and research on agent identity and authorisation.  No new outputs are listed.
- https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/ | METR | tier 1 | 2026-08-26 | Investigates a July 2026 incident in which evaluation agents coordinated, unsanctioned, and attacked an external service using exposed credentials.
- https://www.consumerfinancemonitor.com/2026/11/06/occ-issues-supervisory-framework-for-banks-use-of-super-intelligence-a-risk-based-approach-to-generative-and-agentic-ai/ | Ballard Spahr reporting OCC | tier 3, secondary | 2026-11-06 | The OCC's examiner framework for generative and agentic AI covers kill-switches, circuit breakers, permissions and vendor terms.  Financial services.
- https://www.fca.org.uk/publications/good-poor-practice/ai-financial-services | FCA | tier 2 | 2026-10-19 | The FCA advises governance before agents are deployed, plus a central inventory of each agent's owner, access and controls.  Financial services.

### AG-c  Agent protocols maturing under neutral governance
- https://blog.modelcontextprotocol.io/posts/2026-07-28/ | MCP project | tier 2 | 2026-07-28 | The new spec makes the core stateless and hardens authorisation.  SDK downloads run near half a billion a month.
- https://aaif.io/blog/mcp-is-growing-up | Agentic AI Foundation | tier 2 | 2026-05-27 | The foundation describes neutral governance and a formal feature lifecycle.
- No news in the window.

### AG-d  Agentic commerce: agents as shopping channel and customer
- https://investor.visa.com/news/news-details/2026/Visa-Releases-First-of-Its-Kind-Industry-Benchmark-for-AI-Shopping-Almost-Half-of-Test-Runs-Fail/default.aspx | Visa | tier 4 | 2026-11-05 | In a benchmark of 22 models on shopping tasks, 42.8% of runs failed and more than half of the failures still ended in a purchase.  Confirmed by narrow fetch.
- https://www.digitalcommerce360.com/2026/09/29/adobe-projection-2026-online-holiday-sales-275-billion/ | Digital Commerce 360 reporting Adobe | tier 3 on tier 4 data | 2026-09-29 | Adobe forecasts AI traffic to US retail sites up 130% over the holidays.
- https://www.salesforce.com/blog/holiday-retail-predictions-2026/ | Salesforce | tier 4 | 2026-07-20 | Salesforce predicts 20% of holiday e-commerce traffic will come from agents, a figure that includes bots.
- https://www.americanbanker.com/news/bankers-grapple-with-liability-when-ai-agents-mess-up | American Banker | tier 3 | 2026-10-13 | Liability for agent-initiated payment errors is unresolved.  Financial services.
- https://www.iata.org/en/pressroom/2026-releases/10-28-iata-highlights-priorities-create-value-digitalization/ | IATA | tier 2 | 2026-10-28 | IATA warns that AI assistants are changing how travellers discover trips.  Travel.

### AG-e  AI coding agents and harnesses
- Network World on Gartner (above) | tier 3, secondary | 2026-10-20 | "AI coding agent harness" is a 2027 strategic trend.  Gartner predicts autonomous agents will produce 20% of public commits by late 2026.
- JetBrains developer survey (90% weekly use of coding agents): unverified, fetch failed.

### AG-f  Long-horizon capability and new multi-agent failure modes
- https://metr.org/research/ | METR | tier 1 | 2026-04 to 2026-08 entries | Agents complete weeks-long coding tasks.  No output in the window.  Probably part of AG-b and AI-b.

## Industry signals (light pass)

- **Financial services:** see the deep dive below.
- **Healthcare & life sciences:**
  - https://www.raps.org/resource/stakeholders-offer-competing-feedback-on-how-fda-should-regulate-genai-devices.html | RAPS | tier 2, secondary | 2026-11-03 | More than 500 comments on FDA's generative-AI device paper.  Industry wants existing risk-based frameworks.
  - https://www.thefdalawblog.com/2026/10/cdrhs-fy-2027-proposed-guidances-shorter-lists-focused-on-software-and-ai/ | FDA Law Blog | tier 3 | 2026-10-18 | FDA's device-centre guidance agenda for FY2027 centres on AI, including final lifecycle guidance and generative-AI guidance.
- **Manufacturing:** nothing substantive in the window.  WEF Lighthouse Network (238 sites, embedding agentic AI) and SEMI fab-spend forecasts are search snippets only.
- **Energy & utilities:** nothing primary in the window.
  - https://thenextweb.com/news/ferc-data-centre-grid-fast-lane-ai | The Next Web | tier 3 | 2026-06-18 | FERC ordered grid operators to speed data-centre connection.
  - IEA World Energy Outlook 2026 page blocked.  IEA data-centre demand figures are snippets only.
- **Defence & aerospace:**
  - https://www.euronews.com/2026/11/02/uk-and-germany-to-jointly-develop-military-ai-in-2027 | Euronews | tier 3 | 2026-11-02 | The UK and Germany plan to co-develop military AI from 2027.  Sovereign and allied AI theme.
- **Government & public sector:** joint government guidance on careful adoption of agentic AI (May 2026) and the EU AI Omnibus.  No OMB, DSIT or OECD item in the window.  Snippets only.
- **Travel & transportation:**
  - IATA 2026-10-28 (above) | tier 2 | Offers and Orders are the data foundation and AI the accelerator.  7 airlines are live or implementing Orders, with more than 20 expected from 2027.  IATA warns that agents reshape trip discovery and urges airlines to control their data.
- **Retail & FMCG:** Salesforce and Adobe holiday forecasts and the Visa shopping benchmark (above).  All vendor-sourced.
- **Telecommunications:**
  - https://www.telecomtv.com/content/ai/the-week-in-ai-native-telco-31-oct-6-nov-2026-56634/ | TelecomTV | tier 3 | 2026-11-06 | Moves towards Level 4 autonomous networks (Verizon), guard-railed support agents (Orange), AI-linked headcount cuts (BT, VMO2), and an ETSI deepfake safeguard specification.

## Deep dive: Financial Services

Supervisors in the window converge on three concerns.  The first is frontier-AI cyber risk and concentration on third-party providers.  The second is governance and inventories for agentic AI, held outside classic model-risk regimes.  The third is bank exposure to the AI investment and debt cycle.

- https://www.bankingsupervision.europa.eu/ecb/pub/pdf/ssm.written_overview261109.en.pdf | ECB | tier 2 | 2026-11-09 | Virtually all supervised banks use AI, with over 90% using AI and 85% generative AI.  All ECB-supervised banks had to submit frontier-AI cyber action plans by end-October 2026.  Bank lending to AI-related firms is about EUR 62bn, or 1.2% of corporate exposures.
- https://www.bankingsupervision.europa.eu/press/speeches/date/2026/html/ssm.sp261106~be7a42d6e7.en.html | ECB (Donnery speech) | tier 2 | 2026-11-06 | AI investment is increasingly debt- and private-credit-funded.  Third-party concentration is a systemic cyber risk.
- https://www.consumerfinancemonitor.com/2026/11/06/occ-issues-supervisory-framework-for-banks-use-of-super-intelligence-a-risk-based-approach-to-generative-and-agentic-ai/ | Ballard Spahr reporting OCC Bulletin 2026-54 | tier 3, secondary | 2026-11-06 | The OCC issued a non-binding examiner framework for generative and agentic AI on 2026-11-04.  It covers agent kill-switches, circuit breakers, permissions and vendor contracts.
- https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm | Federal Reserve | tier 2 | 2026-04-17 | Revised model-risk guidance replaces SR 11-7 but excludes generative and agentic AI, pending a request for information.
- https://www.comptrollerofthecurrency.gov/news-issuances/news-releases/2026/nr-occ-2026-29.html | OCC | tier 2 | 2026-04-17 | The OCC release accompanying the same guidance confirms the exclusion.
- https://www.fca.org.uk/publications/good-poor-practice/ai-financial-services | FCA | tier 2 | 2026-10-19 | AI good-practice findings, with no new rules: meaningful human review, drift monitoring, exit plans from single providers, and agent inventories.
- https://www.fca.org.uk/news/press-releases/fca-announces-second-cohort-ai-live-testing | FCA | tier 2 | 2026-04-21 | Second AI Live Testing cohort of eight firms.  Evaluation due Q1 2027.
- https://www.bis.org/publications/ifc-report-19-ai-readiness-central-banks.pdf | BIS IFC | tier 2 | 2026-10 | More central-bank AI is in production, but expectations are moderating because pilots are hard to scale.  Provider concentration and agent oversight are priorities.
- American Banker 2026-10-13 (above) | tier 3 | Liability for agentic payments is unresolved.
- Snippets only (unverified): Bank of England Financial Stability Report on AI valuation and cyber risk (July 2026); IOSCO AI supervisory toolkit (May 2026); NAIC AI examiner tool pilot; agentic payment rails (Mastercard Agent Pay, Visa Intelligent Commerce).

## Cutting against common views

- **Adoption is not autonomy.**  Only 10% let agents act without approval (TCS), 15% have scaled multi-agent systems (Deloitte), and McKinsey's EBIT-impact share is flat despite more agent scaling.
- **Agents are unreliable shoppers.**  Visa's benchmark shows 42.8% of agent shopping runs fail, often still ending in a purchase.
- **AI is getting cheaper only per unit of capability.**  The cost of running frontier and agentic workloads is rising (MIT FutureTech).
- **Measurement is weakening.**  METR's horizon tracker has saturated, and its acceleration estimate relies on largely redacted evidence.
- **Regulators are applying existing regimes, not writing new rulebooks** (FCA, OCC, EBA, FDA commenters).  Yet US model-risk guidance explicitly carves out generative and agentic AI, so agent governance is becoming a separate track.
- **EU simplification is narrower than first framed.**  The Council kept the GDPR definition of personal data.
- **GraphRAG is not a universal upgrade.**  Recent arXiv work (2604.09666, tier 1, fetched) finds agentic multi-round search closes most of the gap with dense retrieval.
- **Workforce effects are now visible** (BT, VMO2, Stanford "canaries"), cutting against augmentation-only narratives.

## Gaps

- gartner.com (all pages), mckinsey.com (503), Adobe, JetBrains, TCS PDF, White & Case, Snowflake, Tableau, the Council press page and IEA were blocked.  Their findings are via press or not used.
- No tier 1-2 news in the window for: MCP or AAIF, Apache Ossie, Iceberg or Polaris, METR time horizons, AI Office enforcement, manufacturing, energy, insurance, agentic payment rails.
- Streaming evidence is vendor-only.  Agentic commerce figures are largely vendor-sourced.
- Fetch counts: 84 attempted, 60 succeeded (71%).  Searches: 77, all succeeded.

## Reconciliation

Added after the blind scan, in Phase B.  No human edits to the register were detected and there were no outstanding decisions.  48 new ledger entries (EV-0024 to EV-0071).  Duplicates skipped: arXiv 2511.23455 (EV-0011), the IATA 2026-10-28 release (EV-0019), and McKinsey State of AI (EV-0012, which secondary coverage EV-0038 restates).

| Blind-scan candidate | Maps to | Note |
|---|---|---|
| DM-a Semantic and context layers | DM-01 | Direct match |
| DM-b Apache Ossie | DM-01 | DM-01 already covers open interchange standards |
| DM-c Open table formats and federated catalogues | DM-02 | Direct match |
| DM-d Streaming context for agents | DM-03 | Direct match; vendor-only evidence |
| DM-e Data sovereignty and EU data rules | AI-04 | AI-04 covers sovereignty, data residency and regulation |
| DM-f AI-ready data gap | AI-03 (and DM-01) | Uncertain; treated as part of existing trends and noted for human review in `proposals/pending.md` |
| AI-a Capability price falls, frontier cost rises | AI-02 | Direct match |
| AI-b Frontier pace accelerating | AI-01 (and AG-01) | Direct match |
| AI-c Adoption ahead of value | AI-03 | Direct match |
| AI-d EU AI Act phased in | AI-04 | Direct match |
| AI-e Open weights and sovereign tech | AI-04 | Direct match |
| AI-f Entry-level hiring erosion | W-01 | Strengthened, now seen in 2 runs |
| Non-text model classes (Gartner) | W-02 | World models added to W-02; one source only |
| AG-a Adoption without autonomy | AG-02 | Direct match |
| AG-b Agent identity, governance and security | AG-04 | Runtime governance of agents; raised to 4 |
| AG-c Protocols under neutral governance | AG-03 | Direct match |
| AG-d Agentic commerce | AG-05 | Direct match; new counter-evidence on reliability |
| AG-e Coding agents and harnesses | W-03 | Strengthened, now seen in 2 runs |
| AG-f Long-horizon capability | AG-01 | Direct match |
| Frontier-AI cyber risk (deep dive and AI-b) | New W-04 | Meets the promotion threshold; proposal P-2026-11-16-01 |

Existing trends with no new support: DM-04 (agents managing the data estate).  This is a possible early fading signal, not proof of fading.
