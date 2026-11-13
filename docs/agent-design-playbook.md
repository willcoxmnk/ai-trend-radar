# Designing a periodic research agent - lessons from the AI Trend Radar

## Purpose

This note records how the AI Trend Radar agent was designed and deployed, so that the approach can be reused for future agents.  It also sets out how structural changes to the trend register (adding, merging, splitting and retiring trends) are handled, and the rules added in procedure version 1.1 to make that process robust.

## The design process

### 1. Do the job manually first

The agent started life as a one-off desk-research exercise.  Doing it by hand first defined the taxonomy (three domains, 13 trends), the standard of evidence (authoritative sources preferred, vendor material flagged) and the shape of a good output.  That manual output became run zero, the baseline the agent builds on.  Designing the agent before knowing what good looks like would have produced a vaguer specification.

### 2. Decide what must persist between runs

A periodic agent is only as good as its memory.  We separated state into three artefacts with different jobs:

- **Register** - the canonical list of trends, each with a permanent ID (for example DM-01) so that a trend can be tracked across runs rather than rediscovered under a new name.
- **Evidence ledger** - an append-only log of every source, with tier, publication date and retrieval date.  It allows de-duplication ("have I seen this before?") and gives an audit trail.
- **Run snapshots** - the full state at the end of each run, plus a computed diff.  Comparing snapshots is what shows whether a trend is gaining or losing importance.

### 3. Make change evidence-based

The main risk with a recurring agent is noise: scores drifting because the model phrased things differently, not because the world changed.  The controls we put in place:

- A written, versioned scoring rubric, so a rubric change can be distinguished from a real change.
- No score moves without new ledger evidence.
- Hysteresis: limited movement per run, and "rising" or "fading" only after consistent signals.
- Publication date recorded separately from retrieval date, so an old report found late is not treated as news.

### 4. Counter the agent's tendency to confirm what it already believes

Given last month's list, an agent will mostly find support for it.  Each run therefore starts with a blind scan, researching the field without reading the register, before a reconciliation step maps fresh findings onto existing IDs.  Unmapped findings become watch-list items or proposals.  The blindness is enforced by instruction rather than technically, so early runs need checking.

### 5. Keep humans in control of structure

The agent may update evidence, scores and the watch list.  It may only propose structural changes; a human decides.  Without this rule the taxonomy drifts and runs stop being comparable.

### 6. Use code for what code does well

Two small scripts handle the deterministic work: a validator that checks integrity before anything is pushed, and a snapshot script that computes the diff between runs.  The briefing is written from that diff, not from the model's recollection.  The language model is reserved for judgement: finding, reading, classifying and explaining.

### 7. Keep the core general and treat industries as configuration

The first version was framed around one customer's industry, which leaked into the scope, the search plan, the scores and the briefing.  It also inflated one trend's importance, because strong airline evidence was read as general significance.  Version 2.0 separated the two layers: importance is judged for enterprises in general, and relevance is scored per industry from a configuration file.  Customer-specific interpretation is produced on demand from the register, which also keeps customer material out of the repo.  The lesson is to decide early who the output is for, and to keep anything audience-specific in configuration rather than in the procedure.

### 8. Keep the logic in the repository

The scheduled task prompt is deliberately short and points at `CLAUDE.md`, which holds the full procedure.  Changes to behaviour are therefore versioned commits, not edits hidden in task settings.

### 9. Plan for failure

The procedure covers repeat runs on the same day (stop), search failures and page-access failures (record a failed run and leave state untouched, so that missing evidence is never mistaken for a fading trend) and validation failures (never push invalid state to `main`).  The validator was extended to accept failed runs, having initially blocked them.

## Deployment lessons

These are the practical issues encountered during setup:

- **Repo structure.**  Files uploaded as a folder ended up one level down, so `CLAUDE.md` was not at the root.  Upload the contents of the folder, not the folder itself, and create the repo without a default README.
- **Connected is not installed.**  Linking GitHub to Claude is not enough.  The Claude GitHub App must appear under GitHub Settings > Applications > Installed GitHub Apps, with the repo selected, or pushes will fail.
- **Branch restrictions affect memory.**  By default a scheduled task can only push to `claude/` branches.  The next run clones `main`, so unmerged output is invisible to it.  Enable "Allow unrestricted branch pushes" for a dedicated state repo.
- **Account choice.**  Use the personal Claude account consistently for personal-repo agents, and keep account-specific or internal material out of personal repos.
- **Network access.**  Search worked in the default cloud environment, but the agent could not open publisher pages.  Set the environment's network access to full, and test by asking an interactive session to fetch a known page.
- **Summarised fetching.**  Page fetches return summaries, not raw text, so specific figures and dates should be confirmed with a narrow follow-up question.
- **Run IDs.**  A manual baseline dated today blocks a real run until tomorrow.  Date the baseline the day before, or expect to wait.
- **Interface drift.**  The product interface changed faster than its documentation (scheduled tasks became Routines).  When a setting cannot be found, test the underlying capability with an interactive session before assuming the setup is wrong.
- **Scheduling.**  Monthly is not a preset; choose the nearest option and adjust with `/schedule update`.  Always test with "Run now" first.

## Handling structural changes

### The intended workflow

1. The agent writes a proposal to `proposals/pending.md` with an ID such as `P-2027-01-12-01`, citing evidence and the rubric threshold met.
2. I review it after the run and record a decision in `proposals/decisions.md` (`APPROVE`, `APPROVE with title`, or `REJECT reason`).
3. The next run applies the decision and marks it as applied.

A short review after each run, before the next one starts, is what makes this work.  If decisions are not made, proposals simply wait.

### What each change does

- **Add** - a new trend is created with the next free ID in its domain, momentum `baseline`, and an `origin` recording where it came from.  A promoted watch-list item is marked `promoted`.
- **Merge** - the absorbed trend is marked `merged` and points to the survivor via `merged_into`.  Its evidence is copied to the survivor, and both trends get a history `event`.
- **Split** - the original is marked `split`, with `split_into` listing at least two successors.  Every piece of its evidence is allocated to a successor, and the allocation is shown in the briefing.
- **Retire** - the trend is marked `retired` and stays in the register for history.

IDs are never reused.

### Rules added in procedure version 1.1

The first version of the procedure left several gaps.  These were closed before the first scheduled run:

1. **Splits** now have a defined status (`split`), successor list and evidence-allocation rule.
2. **Duplicate proposals** are prevented.  Only one pending proposal may exist for the same type and affected IDs; new evidence is added to it.
3. **Rejected proposals** are re-raised only with new tier 1-2 evidence, and must name the rejected proposal under `Supersedes`.
4. **Stale proposals** (pending for three or more runs) are listed first in the briefing, marked STALE.
5. **Continuity of history** is preserved by an optional `event` on each history entry, so a jump in importance after a merge can be explained.
6. **Two routes to change** are separated.  The decisions file is the normal route; direct register edits are for corrections, are never reversed, and are reported in the next briefing.
7. **Validator coverage** now includes merged evidence being copied, split evidence being allocated, history events, and the proposal and decision files themselves.
8. **Ordering.**  Decisions are applied after the blind scan but before scoring, so they neither bias discovery nor get scored against a stale register.

### Remaining judgement calls

- A merged survivor keeps its momentum unless the rubric says otherwise.  If this produces misleading "rising" signals after merges, add a rule to reset momentum to `stable` on the merge run.
- The blind scan is enforced by instruction, not technically.  Check the first few `blind_scan.md` files for independence.

## Reusable checklist for the next agent

1. Do the task manually once and keep the output as the baseline.
2. Define permanent IDs for whatever the agent tracks.
3. Separate current state, evidence and history.
4. Write a versioned rubric with evidence and hysteresis rules.
5. Separate discovery from reconciliation to reduce anchoring.
6. Let the agent propose structural changes; let a human decide.
7. Put validation and diffing in code.
8. Keep the procedure in the repo and the task prompt short.
9. Define failure behaviour and make runs idempotent.
10. Check repo root, app installation, branch permissions, network access and account before the first scheduled run.
11. Keep the core audience-neutral, with industry or customer lenses in configuration.
12. Make failed runs explicit, so that missing evidence is never read as a real signal.
