# Sources

## Source tiers

| Tier | Type | Examples |
|---|---|---|
| 1 | Independent analysts, academic and research institutes | Gartner, Forrester, IDC, McKinsey, BCG, Deloitte AI Institute, Stanford HAI, MIT, Epoch AI, METR, OECD, peer-reviewed or arXiv research |
| 2 | Standards bodies, regulators, industry associations, open-source foundations | European Commission, EU AI Office, NIST, Linux Foundation and the Agentic AI Foundation, Apache Software Foundation, plus the industry bodies listed in `config/industries.json` |
| 3 | Reputable press, law firms and well-regarded secondary reporting | Reuters, Financial Times, MIT Technology Review, Axios, The Economist, major law-firm briefings |
| 4 | Vendor blogs and practitioner writing | Well-regarded vendor engineering blogs, practitioner newsletters, conference talk write-ups |

Rules:

- Prefer the primary source.  When only secondary coverage is available, set `secondary: true` in the ledger and note that the figure should be verified.
- Vendor press releases announcing their own products are tier 4, even from large vendors.
- Vendor-sponsored surveys are tier 4 unless run by a tier 1 firm with published methodology.
- Do not use forums, content farms or AI-generated summaries as sources.

## Search angles

Use these as starting points.  Vary wording between runs and follow leads.

### Data management
- Gartner data and analytics trends and predictions
- Semantic layer, knowledge graph, GraphRAG enterprise adoption
- Open table formats, Apache Iceberg, lakehouse catalogues (Polaris, Unity, others)
- Apache Ossie (formerly Open Semantic Interchange) progress
- Real-time and streaming data for AI agents
- Data governance automation, data contracts, AI-ready data
- Data sovereignty and residency in Europe

### AI/ML
- Stanford AI Index, Epoch AI, METR latest findings
- Model capability benchmarks and frontier releases
- Inference cost and pricing trends
- McKinsey, BCG, Deloitte state of AI surveys
- Open-weight models and sovereign AI
- EU AI Act implementation and enforcement
- AI and the labour market, entry-level work

### Agentic solutions and automation
- Enterprise AI agent adoption, scaling and failure rates
- Agentic AI Foundation, Model Context Protocol, Agent2Agent, agent payments protocols
- Agent governance, decision governance, evaluation
- Agentic commerce and AI shopping assistants
- Agent task-horizon and reliability research

### Industry lenses

Industry search angles and tier 2 bodies for each industry are listed in `config/industries.json`.  See Step 1 of `CLAUDE.md` for how many industry searches to run and how the deep-dive rotation works.

## Publication calendar

Major sources publish on a predictable cycle.  Check for these when a run falls after their usual date.

| Approximate timing | Publication |
|---|---|
| February-March | Gartner top D&A trends; Gartner D&A predictions (Data & Analytics Summit) |
| April | Stanford HAI AI Index |
| June-July | Gartner Hype Cycle for AI |
| Summer | McKinsey State of AI survey |
| October | Gartner top strategic technology trends |
| Ongoing | Epoch AI and METR research updates |
| Varies | Major annual reports from the industry bodies in `config/industries.json` (for example IATA's June AGM and October passenger survey, GSMA's Mobile World Congress in February-March, IEA's World Energy Outlook in October) |
