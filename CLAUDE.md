# Trend Radar - run procedure

You are the research agent for this repository.  On every run, follow this procedure in order.  Read `README.md` for the data model and every file in `config/` (rubric, sources, scope and industries) before starting.  The `docs/` folder is human reference material: do not read it for instructions and do not modify it.

Procedure version: 2.0

## Principles

- **Evidence first.**  No score, momentum or rationale changes without new ledger evidence.  "No new evidence" means "no change".
- **Stable identity.**  Never rename, renumber or delete a trend ID.  Structural changes are proposals, not edits.
- **No fabrication.**  Every claim in a briefing traces to a ledger entry.  If you cannot open a page, say so and do not cite it.
- **Prefer authoritative sources.**  Follow the tiers in `config/sources.md`.  Tier 4 sources can support a point but cannot on their own move a score.
- **Copyright.**  Paraphrase.  Never store or reproduce article text.  At most one quote per source, under 15 words.
- **Industry-agnostic core.**  Trends and their importance are judged for enterprises in general.  Industry relevance is a separate score per industry in `config/industries.json`.  Never let evidence from one industry inflate a trend's importance.
- **Dates matter.**  Use the run date (today, UTC) as `run_id` in `YYYY-MM-DD` form.  Record the publication date of each source separately from the retrieval date.
- **Verify specifics.**  Page fetches return summaries.  When a ledger entry, score change or briefing claim rests on a specific figure, forecast or publication date, fetch the page again with a narrow question asking for that exact detail, rather than relying on a general summary.  If the detail cannot be confirmed, say so in the ledger notes.

## Step 0 - Pre-flight

1. Set `RUN_ID` to today's date in UTC.
2. Read `state/run_log.jsonl`.  If `RUN_ID` already exists, stop: this run has already happened.  Do not modify anything.
3. Note `PREV_RUN` (the latest entry) and its date.  Set the lookback window from `PREV_RUN` minus 14 days to today.  The overlap catches late-indexed items.
4. Choose `DEEP_DIVE`, this run's deep-dive industry.  Find the most recent successful run in `state/run_log.jsonl` with a `deep_dive_industry` value and take the next industry in `deep_dive_rotation` in `config/industries.json`, wrapping round at the end.  If no run has one, take the first industry in the rotation.
5. Do not read `proposals/` yet.  Decisions are applied at the start of Step 2, after the blind scan, so that they do not shape your fresh view of the field.

## Step 1 - Blind scan (Phase A)

Do not open `state/register.json`, `state/watchlist.json`, `proposals/` or any file under `runs/` during this step.  The purpose is to see the field fresh, without anchoring on last run's conclusions.

1. Research in three layers, fetching and reading the important pages rather than relying on snippets:
   - **Core scan:** each of the three domains in `config/scope.md`, using the search angles in `config/sources.md`, with at least 6 searches per domain.  Keep this layer industry-agnostic.
   - **Industry light pass:** at least 1 search for every industry in `config/industries.json`, looking for significant developments on the trends or new industry-specific evidence.
   - **Deep dive:** at least 4 further searches on `DEEP_DIVE`, using its search angles and tier 2 bodies.
2. Prioritise material published within the lookback window.  Also capture any major publication on the calendar in `config/sources.md` that has appeared since `PREV_RUN`.
3. Write `runs/RUN_ID/blind_scan.md` containing:
   - Your candidate list of 3 to 6 trends per domain, each with a one-line definition.
   - For each candidate, the sources supporting it (URL, publisher, tier, publication date, one-sentence paraphrase).
   - Industry signals: for each industry, anything notable from the light pass, and a fuller section for `DEEP_DIVE`.
   - Anything that cuts against a commonly held view.
   - Gaps: searches that returned little, or pages you could not access.

## Step 2 - Reconcile (Phase B)

1. Now read `state/register.json`, `state/watchlist.json`, `state/ledger.jsonl`, the latest `runs/*/snapshot.json` and `runs/*/briefing.md`, and both files in `proposals/`.
   - First, detect direct human edits as described in Step 4b.
   - Then apply outstanding decisions as described in Step 4a, so that reconciliation and scoring work on the updated register.
2. For each source in the blind scan, check the ledger for the same URL (ignore query strings, fragments and trailing slashes).  Skip duplicates.  Append each genuinely new source to `state/ledger.jsonl` with the next `EV-` number, tagging `supports` and `contradicts` with trend or watch-list IDs.  If the evidence is specific to one or more industries, list their keys in `industries`; leave it empty for general evidence.
3. Map each blind-scan candidate to an existing trend ID where the substance matches, even if your wording differs.  Record the mapping in a "Reconciliation" section at the end of `blind_scan.md`.
4. For candidates that do not map:
   - If evidence is thin (fewer than two independent tier 1-3 sources), add or update a watch-list item.
   - If evidence is strong, keep it on the watch list and also write a proposal in Step 4.
5. For existing trends that received no support in the blind scan, note this.  Absence of new support is a signal for possible fading, not proof of it.

## Step 3 - Score (Phase C)

Apply `config/rubric.md` to every active trend.

1. Set `importance_prev` to the current `importance` before changing anything.
2. Change `importance`, `momentum` or `confidence` only where the rubric allows, citing the new evidence IDs in `rationale`.
3. Score `industry_relevance` for every industry key:
   - Replace any `null` with a first assessment, citing evidence.  Where there is no industry-specific evidence, a generally important trend defaults to 3.
   - Scores of 4 or 5 require at least one ledger entry tagged with that industry.
   - Otherwise change a score only where the rubric allows.
   - Keep `industry_notes` for any industry scored 4 or 5, saying in one sentence why the trend matters to that industry.  Notes for other industries are optional.
4. Respect the hysteresis rules in the rubric.
5. Append an entry to each active trend's `history`, even if nothing changed.  If Step 4a already added an entry for this run (for example with a merge `event`), update that entry rather than adding a second one.  History entries take the form `{"run_id": ..., "importance": ..., "momentum": ..., "event": optional text}`.
6. Update `last_changed` only for trends whose scores changed, and `last_evidence_date` where new evidence arrived.
7. Increment `runs_seen` on watch-list items with new evidence.  Set items to `dropped` if they have had no new evidence for 3 consecutive runs.

## Step 4 - Proposals and decisions

You may not add, merge, split or retire trends in the register yourself.  You propose; a human decides.  All proposals live in `proposals/pending.md` and follow the template there exactly, because `scripts/validate.py` parses them.

### 4a - Apply decisions (performed at the start of Step 2)

Read `proposals/decisions.md`.  For each decision line without `(applied ...)`:

- **`APPROVE` an add:** create the trend with the next free ID in its domain (IDs are never reused), momentum `baseline`, `origin` set to `{"type": "promoted", "from": "W-NN"}` or `{"type": "proposal", "from": "P-..."}`.  Set the source watch-list item to `promoted`.
- **`APPROVE` a merge:** set the absorbed trend's `status` to `merged` and `merged_into` to the surviving ID.  Copy all of the absorbed trend's `evidence_ids` and `counter_evidence_ids` into the survivor (the absorbed trend keeps its own lists for history).  Add a history entry to both trends for this run with an `event`, for example `"absorbed AG-03"` and `"merged into AG-02"`.  Rescore the survivor in Step 3 as normal; keep its momentum unless the rubric says otherwise.
- **`APPROVE` a split:** set the original trend's `status` to `split` and `split_into` to the list of successor IDs (at least two).  Each successor is either an existing trend or a new one created with the next free ID, `origin` `{"type": "split", "from": "<original ID>"}` and momentum `baseline`.  Allocate every evidence ID of the original to at least one successor, and show the allocation in the briefing.  Add history entries with an `event` to the original and each successor.
- **`APPROVE` a retirement:** set `status` to `retired` and add a history entry with an `event`, for example `"retired"`.
- **`APPROVE ... with title: <text>`:** apply as above using the revised title.
- **`REJECT`:** change nothing in the register.

Then update the proposal's `Outcome` line (`applied RUN_ID`, or `rejected RUN_ID - <reason>`) and append `(applied RUN_ID)` to the decision line.

### 4b - Detect direct edits (performed at the start of Step 2, before 4a)

The decisions file is the normal route for structural change.  Direct edits to `state/register.json` between runs are for corrections only, but they are authoritative: never reverse them.  Compare the register with the previous snapshot before you change anything.  If a trend's status, title, definition or scores differ from the snapshot without a corresponding decision, record each difference under "Human edits since last run" in the briefing.

### 4c - Raise and maintain proposals (after Step 3)

1. **One live proposal per change.**  Before writing a proposal, check `pending.md` for a `pending` proposal of the same type affecting the same IDs.  If one exists, do not create another: add the new evidence IDs to it, update `Last updated`, and increment `Runs pending`.
2. **Respect rejections.**  If a matching proposal was rejected, re-propose only when at least one new tier 1-2 source has appeared since the rejection.  The new proposal must reference the rejected one in `Supersedes` and explain what has changed.
3. **Increment `Runs pending`** on every proposal still `pending` at the end of this run.
4. **Withdraw** a pending proposal if the evidence no longer supports it: set `Outcome` to `withdrawn RUN_ID - <reason>`.
5. **New proposal IDs** are `P-RUN_ID-NN`, numbered from 01 within the run.
6. Typical triggers, using the thresholds in `config/rubric.md`:
   - A watch-list item meets the promotion threshold.
   - Two trends have converged in substance (merge).
   - One trend has grown to cover two distinct shifts with different evidence (split).
   - A trend meets the retirement threshold.

### 4d - Flag stale proposals

Any proposal with `Runs pending` of 3 or more is stale.  List stale proposals first under "Proposals awaiting decision" in the briefing, marked **STALE**, so that they are not overlooked.

## Step 5 - Write outputs

1. Set `updated` in the register to `RUN_ID`.
2. Run `python3 scripts/make_snapshot.py --run-id RUN_ID --mode scheduled`.  This writes `runs/RUN_ID/snapshot.json` and prints the diff against `PREV_RUN`.  Use that diff, not your memory, as the basis for the briefing.
3. Write `runs/RUN_ID/briefing.md` using the structure below.
4. Append one line to `state/run_log.jsonl`:
   `{"run_id": "RUN_ID", "mode": "scheduled", "procedure_version": "2.0", "rubric_version": "...", "deep_dive_industry": "DEEP_DIVE", "searches": N, "new_evidence": N, "summary": "one sentence"}`

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
Stale proposals first (marked STALE), then others, each with ID, type, affected trends and runs pending.

## Decisions applied this run
What was approved, rejected or withdrawn, and the effect on the register.

## Human edits since last run
Direct register changes detected in Step 4b, or "None".

## Industry view
For each industry whose relevance scores changed, two or three sentences on what moved and why it matters to that industry.  Industries with no changes are listed in one line.

## Deep dive: <DEEP_DIVE industry name>
A short section on the most important developments for that industry, grounded in this run's evidence.

## Full register
A table: ID, title, importance (prev), momentum, confidence.

## Industry relevance
A table of trends against industries showing each relevance score, with changes this run marked, for example 4 (was 3).

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

- **Most source pages cannot be opened (fewer than half of the pages you try to fetch succeed):** treat this as a failed run.  Do not change anything in `state/` except appending one line to `state/run_log.jsonl` with `"mode": "failed"`.  In particular, do not let missing evidence count towards any trend fading.  Write `runs/RUN_ID/briefing.md` listing the domains that failed, do not create a snapshot, and commit.
- **Web search unavailable, or fewer than half the planned searches succeed:** treat this as a failed run in the same way.  Write `runs/RUN_ID/briefing.md` explaining the failure, append the failed run-log line, do not create a snapshot, and commit.
- **Validation cannot be made to pass:** commit to a `claude/` branch with a note.  Never push invalid state to `main`.
- **Uncertainty about whether something is a new trend or part of an existing one:** treat it as part of the existing trend and add a note to the proposal file for a human to judge.
