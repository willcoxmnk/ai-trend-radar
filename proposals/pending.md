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

## Proposals

None yet.
