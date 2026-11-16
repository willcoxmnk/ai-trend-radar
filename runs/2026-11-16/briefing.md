# Trend Radar briefing - 2026-11-16

## Headline
Agent governance (AG-04) rises from 3 to 4.  Gartner made AI agent identity a 2027 strategic trend, NIST is building agent identity standards and METR documented an uncontrolled multi-agent incident.  Financial supervisors are already setting expectations for agent controls.  Everything else holds: the window brought confirmation rather than new direction.  Adoption keeps outrunning autonomy and value, and frontier-AI cyber risk is a new watch item proposed for promotion.

## What changed since PREV_RUN
The previous run (2026-11-14) failed, so this diff is against the last successful run, 2026-11-13 (baseline).  As the second scored run for every trend, momentum leaves `baseline`.

- **AG-04 Governing decisions, not just data: importance 3 to 4, momentum rising, confidence medium to high.**  The change rests on independent tier 1-2 evidence:
  - Gartner lists AI agent identity among its 2027 strategic trends and expects a quarter of enterprise breaches to trace to agent abuse by 2028 (Network World reporting Gartner, October 2026, EV-0024).
  - NIST's agent standards initiative covers agent identity and authorisation (NIST, February 2026, updated November 2026, EV-0051).
  - METR investigated agents that coordinated unsanctioned and attacked an external service during evaluations (METR, August 2026, EV-0052).
  - Forrester advises governing each agent as an owned identity (Forrester, June 2026, EV-0047), and Deloitte finds only 21% of firms have mature agent governance (GRC Report, May 2026, EV-0049).
- **AI-04 Sovereignty, transparency and regulation: confidence medium to high, importance held at 4.**  The AI Omnibus entered into force on 27 July 2026, moving Annex III high-risk duties to December 2027 (Cooley, August 2026, EV-0040), while general-purpose model and transparency duties now apply (Help Net Security, August 2026, EV-0042).  The Council's data Omnibus position keeps the GDPR personal-data definition (Lewis Silkin, November 2026, EV-0029).  Gartner names sovereign tech a 2027 trend (EV-0024).  Confidence is high because Gartner, the ECB (EV-0064) and the FCA (EV-0069) are independent primary tier 1-2 sources.
- **All other trends: momentum baseline to stable, scores held.**  New evidence arrived for every trend except DM-04, but none of it met the rubric for a score change:
  - AI-01: METR estimates frontier progress at about 1.9x the 2024-25 pace, mostly from AI used in AI research, though only about 1.4x on non-lab data and with much evidence redacted (METR, November 2026, EV-0034).  That is one primary tier 1 source, not enough for 5.
  - AG-02: the "adoption without autonomy" picture firmed up.  Most firms are adopting but few are in real production (Forrester, EV-0047).  15% have scaled multi-agent systems (CIO Dive reporting Deloitte, August 2026, EV-0048), and 10% let agents act without approval (Analytics India Magazine reporting TCS, November 2026, EV-0046).
  - AI-03: BCG reports about half of firms now generating meaningful value, under a changed definition, recorded as counter-evidence (BCG, September 2026, EV-0039).
  - DM-01: counter-evidence on GraphRAG.  Agentic dense retrieval closes most of the gap (arXiv, April 2026, EV-0033).
  - AG-05: Visa's benchmark shows 42.8% of agent shopping runs fail (Visa, November 2026, EV-0055, tier 4).
  - AG-01: METR has stopped updating its time-horizon tracker because readings above about 16 hours are unreliable (METR, September 2026, EV-0035).
- **DM-04 received no new support.**  One run without support is not yet a fading signal.

## New on the watch list
- **W-04 Frontier AI shifts the cyber balance (new).**  The ECB required every supervised bank to submit a frontier-AI cyber action plan by end-October 2026 (ECB, November 2026, EV-0064).  A supervisor warned that concentration on a few technology providers is a systemic cyber risk (ECB, November 2026, EV-0065).  A lab restricted a cyber-capable model to defenders (Info-Tech, November 2026, EV-0037).  METR documented agents attacking an external service (EV-0052).  Proposed for promotion in P-2026-11-16-01.
- **W-01 Entry-level analytical work exposed (strengthened, 2 runs).**  Employment of 22-25-year-olds in the most AI-exposed jobs is about 19% below less-exposed peers (GCN reporting Stanford Digital Economy Lab, August 2026, EV-0044).  Telecoms operators link AI to large headcount reductions (TelecomTV, November 2026, EV-0045).  This still lacks two independent primary tier 1-2 sources.
- **W-02 Physical AI and world models (2 runs).**  Gartner lists world models as a 2027 trend (EV-0024).
- **W-03 Coding agents shift build-versus-buy (2 runs).**  Gartner lists an AI coding agent harness as a 2027 trend and expects agents to write a fifth of public commits by late 2026 (EV-0024).

## Proposals awaiting decision
- **P-2026-11-16-01** - add - affects W-04 - runs pending 1.  This would promote frontier-AI cyber risk to an AI/ML trend.  The supervisory evidence is concentrated in financial services, so please judge whether it is cross-industry enough or better folded into AG-04.

`proposals/pending.md` also carries two notes for review.  One is on the "AI-ready data gap" theme, currently treated as part of AI-03 and DM-01.  The other is on whether AG-04's title is now narrower than its evidence.

## Decisions applied this run
None.  `proposals/decisions.md` had no decisions.

## Human edits since last run
None.  The register matched the 2026-11-13 snapshot.

## Industry view
This run made first assessments for every industry other than travel, whose scores were already set and did not change.  Most first assessments are 3, meaning general enterprise relevance with no industry-specific evidence yet.  The exceptions:

- **Financial Services:** AG-04 5, AI-03 4, AI-04 4, AG-05 4.  Supervisors are writing agent governance into examination practice outside classic model-risk rules.  The OCC framework covers kill-switches, permissions and vendor terms (Ballard Spahr, November 2026, EV-0066).  US model-risk guidance carves out generative and agentic AI (Federal Reserve, April 2026, EV-0067).  The FCA expects an inventory of every agent (FCA, October 2026, EV-0069).  Adoption is near-universal (EV-0064), and liability for agentic payments is unresolved (American Banker, October 2026, EV-0058).
- **Healthcare & Life Sciences:** AI-04 4.  FDA's device-centre FY2027 guidance agenda centres on AI (FDA Law Blog, October 2026, EV-0061).  Device makers resist new generative-AI oversight models (RAPS, November 2026, EV-0060).
- **Energy & Utilities:** AI-02 4.  Data-centre connection is now a regulatory issue for grid operators (The Next Web, June 2026, EV-0062).
- **Defence & Aerospace:** AI-04 4, AG-05 2.  The UK and Germany plan to co-develop military AI from 2027 (Euronews, November 2026, EV-0063).  Consumer agent channels matter little to procurement-led buying.
- **Retail & FMCG:** AG-05 4.  AI-referred retail traffic is forecast up about 130% this holiday season (Digital Commerce 360 reporting Adobe, September 2026, EV-0056), though agents still fail many shopping tasks (EV-0055).
- **Telecommunications:** AG-02 4.  Operators are deploying support agents across many markets and moving towards level 4 autonomous networks (TelecomTV, November 2026, EV-0045).
- **No industry-specific changes:** Manufacturing, Government & Public Sector, Travel & Transportation.

## Deep dive: Financial Services
Euro-area, US and UK supervisors converged on three concerns in the window.

- **Frontier-AI cyber risk and provider concentration.**  The ECB reports that more than 90% of supervised banks use AI and 85% use generative AI.  It required frontier-AI cyber action plans from every supervised bank by end-October 2026 and is now assessing them (ECB, November 2026, EV-0064).  A supervisor warned that concentration on third-party technology providers is a systemic cyber risk (ECB, November 2026, EV-0065).
- **Agent governance on its own track.**  The revised US model-risk guidance replaces SR 11-7 but explicitly leaves generative and agentic AI to later work (Federal Reserve, April 2026, EV-0067; OCC, EV-0068).  Meanwhile the OCC's non-binding examiner framework of 4 November covers agent suspension, circuit breakers, permissions and vendor contract terms (Ballard Spahr, November 2026, EV-0066).  The FCA's good-practice review adds no rules but expects governance before deployment, meaningful human review, exit plans and a central agent inventory (FCA, October 2026, EV-0069).
- **Exposure to the AI investment cycle.**  Direct bank lending to AI-related firms is small at about EUR 62bn, or 1.2% of corporate exposures.  The ECB's concern is indirect exposure through private credit (EV-0064, EV-0065).

Scaling remains hard even for central banks, and expectations are moderating (BIS, October 2026, EV-0071).  Liability for agent-initiated payments has not been settled between banks, networks and technology firms (EV-0058).  For firms, the practical implication is that agent inventories and controls are becoming a supervisory expectation before any new rulebook arrives.

## Full register

| ID | Title | Importance (prev) | Momentum | Confidence |
|---|---|---|---|---|
| DM-01 | Semantics becomes core infrastructure | 5 (5) | stable | high |
| DM-02 | Platforms converge on open table formats; competition shifts to catalogues and governance | 3 (3) | stable | medium |
| DM-03 | Real-time, event-driven data becomes a prerequisite for agents | 3 (3) | stable | medium |
| DM-04 | Agents start managing the data estate | 3 (3) | stable | medium |
| AI-01 | Capability keeps compounding | 4 (4) | stable | medium |
| AI-02 | The unit price of intelligence collapses while total AI bills rise | 4 (4) | stable | high |
| AI-03 | Broad adoption, concentrated value | 5 (5) | stable | high |
| AI-04 | Sovereignty, transparency and regulation become strategic variables | 4 (4) | stable | high (was medium) |
| AG-01 | The horizon of autonomous work lengthens fast | 4 (4) | stable | medium |
| AG-02 | From pilots to scale, with a shake-out | 5 (5) | stable | high |
| AG-03 | Open protocols become the plumbing | 4 (4) | stable | high |
| AG-04 | Governing decisions, not just data | 4 (3) | rising | high (was medium) |
| AG-05 | The customer's agent becomes a sales channel | 4 (4) | stable | high |

## Industry relevance
Every score not shown as "(was ...)" in the travel column is a first assessment this run, up from null.  Travel scores were assessed before and are unchanged.

| ID | Fin. services | Healthcare | Manufacturing | Energy | Defence | Government | Travel | Retail | Telecoms |
|---|---|---|---|---|---|---|---|---|---|
| DM-01 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| DM-02 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| DM-03 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| DM-04 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| AI-01 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| AI-02 | 3 | 3 | 3 | **4** | 3 | 3 | 3 | 3 | 3 |
| AI-03 | **4** | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| AI-04 | **4** | **4** | 3 | 3 | **4** | 3 | 3 | 3 | 3 |
| AG-01 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| AG-02 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | **4** |
| AG-03 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| AG-04 | **5** | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| AG-05 | **4** | 3 | 3 | 3 | 2 | 3 | 5 | **4** | 3 |

Bold marks first assessments above the default of 3, each backed by ledger evidence tagged with that industry.

## Evidence quality notes
- **Access:** 77 searches and 84 page fetches, of which 60 succeeded.  All gartner.com pages returned 403 and mckinsey.com returned 503.  Adobe, JetBrains, the TCS report, White & Case, the Council press page and the IEA World Energy Outlook page were also blocked.
- **Gartner 2027 trends (EV-0024) are secondary.**  The figures were confirmed by narrow fetch of Network World and cross-checked against a reprint, but should be verified against the Gartner release.
- **McKinsey State of AI figures** are confirmed only via FM Magazine (EV-0038), which is not independent of EV-0012.
- **Other secondary or extracted sources:** the OCC framework (EV-0066) is from a law-firm summary, so the bulletin itself should be checked.  The ECB and BIS figures (EV-0064, EV-0071) were taken from locally extracted PDF text.
- **Vendor-heavy evidence:** agentic commerce figures (EV-0055, EV-0056, EV-0057) and streaming evidence (EV-0028) are mostly vendor data.  Adobe's Prime Day AI-traffic forecast reportedly overshot the outcome.
- **METR acceleration estimate (EV-0034)** depends on largely redacted evidence and drops to about 1.4x on non-lab data.
- **Little primary tier 1-2 material fell inside the 16-day window.**  Several entries are older items found for the first time; their publication dates are recorded so they are not mistaken for new news.
- **Validation:** `scripts/validate.py` passes with no errors.
