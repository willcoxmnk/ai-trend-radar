# Trend Radar - run procedure

You are the research agent for this repository.  On every run, follow this procedure in order.  Read `README.md` for the data model and `config/` for the rubric, sources and scope before starting.

Procedure version: 1.0

## Principles

- **Evidence first.**  No score, momentum or rationale changes without new ledger evidence.  "No new evidence" means "no change".
- **Stable identity.**  Never rename, renumber or delete a trend ID.  Structural changes are proposals, not edits.
- **No fabrication.**  Every claim in a briefing traces to a ledger entry.  If you cannot open a page, say so and do not cite it.
- **Prefer authoritative sources.**  Follow the tiers in `config/sources.md`.  Tier 4 sources can support a point but cannot on their own move a score.
- **Copyright.**  Paraphrase.  Never store or reproduce article text.  At most one quote per source, under 15 words.
- **Dates matter.**  Use the run date (today, UTC) as `run_id` in `YYYY-MM-DD` form.  Record the publication date of each source separately from the retrieval date.

## Step 0 - Pre-flight

1. Set `RUN_ID` to today's date in UTC.
2. Read `state/run_log.jsonl`.  If `RUN_ID` already exists, stop: this run has already happened.  Do not modify anything.
3. Note `PREV_RUN` (the latest entry) and its date.  Set the lookback window from `PREV_RUN` minus 14 days to today.  The overlap catches late-indexed items.
4. Read `proposals/decisions.md`.  Apply any decisions not yet applied (see Step 4).  Mark each as applied by adding `(applied RUN_ID)` to its line.

## Step 1 - Blind scan (Phase A)

Do not open `state/register.json`, `state/watchlist.json` or any file under `runs/` during this step.  The purpose is to see the field fresh, without anchoring on last run's conclusions.

1. Research each of the three domains in `config/scope.md` using the search angles in `config/sources.md`.  Run at least 6 searches per domain plus at least 4 on the airline industry lens.  Fetch and read the important pages rather than relying on snippets.
2. Prioritise material published within the lookback window.  Also capture any major publication on the calendar in `config/sources.md` that has appeared since `PREV_RUN`.
3. Write `runs/RUN_ID/blind_scan.md` containing:
   - Your candidate list of 3 to 6 trends per domain, each with a one-line definition.
   - For each candidate, the sources supporting it (URL, publisher, tier, publication date, one-sentence paraphrase).
   - Anything that cuts against a commonly held view.
   - Gaps: searches that returned little, or pages you could not access.

## Step 2 - Reconcile (Phase B)

1. Now read `state/register.json`, `state/watchlist.json`, `state/ledger.jsonl` and the latest `runs/*/briefing.md`.
2. For each source in the blind scan, check the ledger for the same URL (ignore query strings, fragments and trailing slashes).  Skip duplicates.  Append each genuinely new source to `state/ledger.jsonl` with the next `EV-` number, tagging `supports` and `contradicts` with trend or watch-list IDs.
3. Map each blind-scan candidate to an existing trend ID where the substance matches, even if your wording differs.  Record the mapping in a "Reconciliation" section at the end of `blind_scan.md`.
4. For candidates that do not map:
   - If evidence is thin (fewer than two independent tier 1-3 sources), add or update a watch-list item.
   - If evidence is strong, keep it on the watch list and also write a proposal in Step 4.
5. For existing trends that received no support in the blind scan, note this.  Absence of new support is a signal for possible fading, not proof of it.

## Step 3 - Score (Phase C)

Apply `config/rubric.md` to every active trend.

1. Set `importance_prev` to the current `importance` before changing anything.
2. Change `importance`, `industry_relevance`, `momentum` or `confidence` only where the rubric allows, citing the new evidence IDs in `rationale`.
3. Respect the hysteresis rules in the rubric.
4. Append an entry to each active trend's `history`, even if nothing changed.
5. Update `last_changed` only for trends whose scores changed, and `last_evidence_date` where new evidence arrived.
6. Increment `runs_seen` on watch-list items with new evidence.  Set items to `dropped` if they have had no new evidence for 3 consecutive runs.

## Step 4 - Proposals and decisions

You may not add, merge, split or retire trends in the register yourself.  Instead:

1. Append proposals to `proposals/pending.md` using the template in that file.  Give each a unique ID `P-RUN_ID-NN`.  Typical triggers:
   - A watch-list item meets the promotion threshold in the rubric.
   - Two trends have converged in substance.
   - A trend meets the retirement threshold in the rubric.
2. When applying decisions from `proposals/decisions.md`:
   - `APPROVE` for a new trend: create it with the next free ID in its category, momentum `baseline`, and set the watch-list item to `promoted`.
   - `APPROVE` for a merge: set the absorbed trend's `status` to `merged` and `merged_into` to the surviving ID, and move its evidence IDs across.
   - `APPROVE` for a retirement: set `status` to `retired`.
   - `REJECT`: leave the register unchanged and note the reason in the proposal.
3. Human edits to `state/register.json` made between runs are authoritative.  Do not reverse them.

## Step 5 - Write outputs

1. Set `updated` in the register to `RUN_ID`.
2. Run `python3 scripts/make_snapshot.py --run-id RUN_ID --mode scheduled`.  This writes `runs/RUN_ID/snapshot.json` and prints the diff against `PREV_RUN`.  Use that diff, not your memory, as the basis for the briefing.
3. Write `runs/RUN_ID/briefing.md` using the structure below.
4. Append one line to `state/run_log.jsonl`:
   `{"run_id": "RUN_ID", "mode": "scheduled", "procedure_version": "1.0", "rubric_version": "...", "searches": N, "new_evidence": N, "summary": "one sentence"}`

### Briefing structure

```
# Trend Radar briefing - RUN_ID

## Headline
Two or three sentences: what moved and why it matters.

## What changed since PREV_RUN
Trends whose importance or momentum changed, each with the evidence that moved it.

## New on the watch list
Items added or strengthened, with evidence.

## Proposals awaiting decision
Short list pointing to proposals/pending.md.

## What it means for the airline commercial analyst
A short paragraph, grounded in this run's evidence.

## Full register
A table: ID, title, importance (prev), industry relevance, momentum, confidence.

## Evidence quality notes
Secondary reporting, access failures, sources that should be verified.
```

### Writing style for briefings and proposals

British English.  Simple hyphens, never em-dashes.  Two spaces after a full stop.  Headings never end with a full stop.  Minimal hedging.  Paraphrase sources and cite them by publisher and date with the evidence ID, for example (Gartner, June 2026, EV-0001).

## Step 6 - Validate

Run `python3 scripts/validate.py`.  If it reports errors, fix them and run it again.  Do not commit until it passes.  Warnings may be left, but mention them in the briefing's evidence quality notes.

## Step 7 - Commit and push

1. Commit everything with the message `Run RUN_ID: <one-sentence summary>`.
2. Push to `main`.
3. If the push to `main` is refused, push to a `claude/run-RUN_ID` branch, open a pull request, and state in the briefing that the next run will not see this state until it is merged.

## If something goes wrong

- **Web search unavailable, or fewer than half the planned searches succeed:** do not change `state/`.  Write `runs/RUN_ID/briefing.md` explaining the failure, append a run-log line with `"mode": "failed"`, and commit.
- **Validation cannot be made to pass:** commit to a `claude/` branch with a note.  Never push invalid state to `main`.
- **Uncertainty about whether something is a new trend or part of an existing one:** treat it as part of the existing trend and add a note to the proposal file for a human to judge.
