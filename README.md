# AI Trend Radar

A scheduled research agent that tracks trends in data management, AI/ML and agentic automation over time.  Each run researches the field, compares what it finds with the previous state, rescores existing trends, proposes new ones and writes a time-stamped snapshot and briefing.  The repo is both the agent's memory and its output.

The analytical lens is the airline industry and the airline commercial analyst.  Keep this repo to public-source research: no customer-specific notes and nothing from internal company sources.

## How it runs

The agent runs as a Claude Code scheduled task in the cloud.  Each run clones this repo, follows the procedure in `CLAUDE.md`, validates its own output and pushes back to `main`.

- `TASK_PROMPT.md` holds the short prompt to paste into the scheduled task.  The real logic lives in `CLAUDE.md` so that it is versioned in Git.
- The task needs web search and network access, and "Allow unrestricted branch pushes" enabled for this repo.  Without that setting each run lands on a `claude/` branch and the next run will not see it.

## Repository layout

```
CLAUDE.md                 Run procedure and rules the agent follows on every run
TASK_PROMPT.md            Prompt to paste into the scheduled task
config/
  rubric.md               Scoring rubric (versioned)
  sources.md              Source tiers, search angles and publication calendar
  scope.md                Domains, lens and what is in or out of scope
state/
  register.json           Canonical trend register (current state)
  ledger.jsonl            Append-only evidence ledger, one JSON object per line
  watchlist.json          Emerging issues not yet promoted to trends
  run_log.jsonl           One line per run
runs/YYYY-MM-DD/
  blind_scan.md           Phase A output, written before the register is read
  snapshot.json           Full state at end of run plus a computed diff
  briefing.md             Human-readable briefing
proposals/
  pending.md              Structural changes proposed by the agent
  decisions.md            Your decisions on those proposals
docs/
  agent-design-playbook.md  How this agent was designed; reusable lessons (not read by the agent)
scripts/
  validate.py             Integrity checks (stdlib only)
  make_snapshot.py        Writes the snapshot and computes the diff against the last run
```

## Who changes what

| Change | Who | Where |
|---|---|---|
| New evidence, scores, momentum, rationale | Agent | `state/` |
| Watch-list items | Agent | `state/watchlist.json` |
| Add, merge, split or retire a trend | Agent proposes, you decide | `proposals/` |
| Corrections to the register | You | `state/register.json` (reported in the next briefing) |
| Rubric, sources, scope | You | `config/` |
| Design notes | You | `docs/` |

## Structural changes

1. **The agent proposes.**  Proposals go in `proposals/pending.md`, using a fixed template that `validate.py` checks.  There is only ever one pending proposal for the same change; later evidence is added to it rather than raising a duplicate.  A rejected change is re-proposed only with new tier 1-2 evidence, and must name the rejected proposal under `Supersedes`.
2. **You decide.**  After reading a run's briefing, add a line to `proposals/decisions.md`:
   - `APPROVE P-2027-01-12-01`
   - `APPROVE P-2027-01-12-01 with title: <revised title>`
   - `REJECT P-2027-01-12-02 reason: duplicate of AG-03`
3. **The next run applies it**, updates the proposal's `Outcome`, and marks your decision line `(applied YYYY-MM-DD)`.
4. **Stale proposals are flagged.**  Anything pending for three or more runs is listed first in the briefing, marked STALE.

What each approved change does to the register:

| Change | Effect |
|---|---|
| Add | New trend with the next free ID in its domain, momentum `baseline`, `origin` recording where it came from.  A promoted watch-list item is marked `promoted`. |
| Merge | Absorbed trend becomes `merged` with `merged_into` set; its evidence is copied to the survivor.  Both get a history `event`. |
| Split | Original becomes `split` with `split_into` listing at least two successors; every piece of its evidence is allocated to a successor.  New successors get new IDs and momentum `baseline`. |
| Retire | Trend becomes `retired` and stays in the register for history. |

IDs are never reused.  Decisions are the normal route for structural change; edit the register directly only to correct mistakes.  The agent never reverses a direct edit, but reports it under "Human edits since last run" in the briefing.

Review routine: after each run, read the briefing, record any decisions, and commit before the next scheduled run.

## Data model

### Register (`state/register.json`)

```json
{
  "rubric_version": "1.0",
  "updated": "2026-11-13",
  "trends": [
    {
      "trend_id": "AG-05",
      "status": "active",
      "category": "agentic",
      "title": "The customer's agent becomes a sales channel",
      "definition": "One or two sentences that pin down the scope",
      "importance": 5,
      "importance_prev": null,
      "industry_relevance": 5,
      "momentum": "baseline",
      "confidence": "high",
      "rationale": "Why the current scores, referencing evidence",
      "industry_note": "Why it matters to airline commercial teams",
      "evidence_ids": ["EV-0018"],
      "counter_evidence_ids": [],
      "first_seen": "2026-11-13",
      "last_changed": "2026-11-13",
      "last_evidence_date": "2026-10-28",
      "merged_into": null,
      "split_into": [],
      "origin": null,
      "history": [{"run_id": "2026-11-13", "importance": 5, "momentum": "baseline", "event": "optional text"}]
    }
  ]
}
```

- `trend_id` is permanent.  Prefixes are `DM` (data management), `AI` (AI/ML) and `AG` (agentic).  IDs are never reused, even after retirement.
- `status` is `active`, `merged`, `split` or `retired`.  Inactive trends stay in the file for history.
- `merged_into` (for merged trends) and `split_into` (for split trends) point to successors.  `origin` is null for run-zero trends, otherwise `{"type": "promoted" | "proposal" | "split", "from": "<ID>"}`.  `split_into` and `origin` may be omitted where empty.
- Each `history` entry records one run.  The optional `event` text explains structural changes, so that a jump in a trend's importance after a merge can be traced.
- `importance` and `industry_relevance` are integers from 1 to 5, defined in `config/rubric.md`.
- `momentum` is `baseline`, `rising`, `stable` or `fading`.
- `confidence` is `high`, `medium` or `low`.

### Evidence ledger (`state/ledger.jsonl`)

One object per line, append-only.  Entries are never edited except to add a `notes` correction.

```json
{"evidence_id": "EV-0001", "url": "https://...", "publisher": "Gartner", "title": "...", "tier": 1, "published_date": "2026-06-16", "retrieved_date": "2026-11-13", "summary": "Paraphrased summary, max 400 characters", "supports": ["DM-01"], "contradicts": [], "secondary": false, "notes": ""}
```

- `tier` is 1 to 4, defined in `config/sources.md`.
- `published_date` is the date of the underlying publication (`YYYY-MM-DD` or `YYYY-MM`, or null if unknown).  `retrieved_date` is the run date.  The difference matters: an old report found for the first time is not new news.
- `secondary` is true when the entry reports someone else's findings, for example press coverage of the Stanford AI Index.
- Summaries are paraphrased.  No article text is stored.  An optional `quote` field may hold one quote of fewer than 15 words.

### Watch list (`state/watchlist.json`)

Emerging issues with too little evidence to be trends.  Each item has an ID (`W-01`), title, description, `first_seen`, `evidence_ids`, `runs_seen` and `status` (`watching`, `promoted` or `dropped`).

## Running checks locally

```
python3 scripts/validate.py
python3 scripts/make_snapshot.py --run-id 2026-11-13 --mode baseline
```

## Run history

Procedure version 1.1 added rules for splits, duplicate, rejected and stale proposals, history events and direct-edit reporting.

Run zero (`2026-11-13`) was seeded by hand from a desk-research exercise.  Its scores are a baseline, so every trend starts with momentum `baseline`.
