# Pending proposals

The agent appends structural proposals here.  Decide on each by adding a line to `proposals/decisions.md`; the next run applies it.  Follow the template exactly: `scripts/validate.py` parses these fields.

## Template

```
### P-YYYY-MM-DD-NN - <short title>

- Type: add | merge | split | retire
- Affects: <comma-separated trend or watch-list IDs>
- Proposed change: <exact change; for add or split, give proposed titles, definitions and domains>
- Evidence: <evidence IDs, with tier>
- Rubric threshold met: <which threshold in config/rubric.md>
- Reasoning: <two or three sentences>
- Supersedes: <earlier proposal ID, or none>
- Raised: YYYY-MM-DD
- Last updated: YYYY-MM-DD
- Runs pending: 0
- Outcome: pending
```

Allowed outcomes: `pending`, `applied YYYY-MM-DD`, `rejected YYYY-MM-DD - <reason>`, `withdrawn YYYY-MM-DD - <reason>`.

Rules the agent follows:

- Only one `pending` proposal may exist for the same type and the same affected IDs.  New evidence is added to the existing proposal.
- A rejected change is re-proposed only with new tier 1-2 evidence, and the new proposal names the rejected one under `Supersedes`.
- A proposal with `Runs pending` of 3 or more is stale and is listed first in the briefing.

## Notes for human review

- 2026-11-16: the blind scan found an "AI-ready data gap" theme (data readiness and governance culture, not tooling, limit AI scaling; EV-0031, EV-0032, EV-0071).  Under the uncertainty rule it is treated as part of AI-03 and DM-01 rather than as a new item.  Judge whether it deserves its own watch-list item.
- 2026-11-16: AG-04 ("Governing decisions, not just data") now draws most of its new support from agent identity, permissions, kill-switches and inventories (EV-0024, EV-0051, EV-0066, EV-0069).  The definition covers runtime governance, so no split or rename is proposed, but a direct title correction may be warranted.

## Proposals

### P-2026-11-16-01 - Promote W-04 frontier AI and the cyber balance

- Type: add
- Affects: W-04
- Proposed change: Add a new AI/ML trend (next free AI ID).  Title: "Frontier AI shifts the cyber balance".  Definition: "Frontier models make finding and exploiting vulnerabilities faster and cheaper, and agents introduce new incident types, so supervisors and boards start to require AI-specific cyber resilience plans and scrutinise concentration on a few technology providers.  Overlaps AG-04 on agent security."  Domain: AI/ML.
- Evidence: EV-0064 (tier 2, ECB), EV-0065 (tier 2, ECB, not independent of EV-0064), EV-0052 (tier 1, METR), EV-0024 (tier 3, Gartner via Network World), EV-0037 (tier 3, Info-Tech digest)
- Rubric threshold met: Promote a watch-list item with at least two independent tier 1-2 sources (ECB EV-0064 and METR EV-0052).
- Reasoning: The ECB required all supervised banks to submit frontier-AI cyber action plans by end-October 2026, and a lab restricted a cyber-capable model to defenders.  METR documents agents attacking an external service during evaluations, and Gartner expects agent abuse to drive a quarter of breaches by 2028.  The supporting supervisory evidence is concentrated in financial services, so the human reviewer should judge whether this is cross-industry enough, or better treated as part of AG-04.
- Supersedes: none
- Raised: 2026-11-16
- Last updated: 2026-11-16
- Runs pending: 1
- Outcome: pending
