# Scheduled task prompt

Paste the text below into the prompt field when you create the scheduled task.  Keep the procedure itself in `CLAUDE.md`, so that changes are versioned in Git rather than hidden in the task settings.

## Task settings

- Repository: this repo, with "Allow unrestricted branch pushes" enabled
- Environment: network access sufficient for web search and fetching public web pages
- Connectors: none required (remove any that are attached by default)
- Schedule: monthly (choose the nearest preset, then set the exact schedule with `/schedule update` in the CLI)

## Prompt

```
You are running a scheduled update of the AI Trend Radar in this repository.

Read CLAUDE.md in the repository root and carry out the run procedure exactly, from Step 0 to Step 7.  Use today's date in UTC as RUN_ID.  Read README.md and every file in config/ before starting research.

Non-negotiable rules:
- Do not read state/register.json, state/watchlist.json or anything under runs/ until Step 1 (blind scan) is complete and runs/RUN_ID/blind_scan.md is written.
- Do not add, merge, split or retire trends yourself.  Propose them in proposals/pending.md.
- Every score change must cite new evidence IDs from state/ledger.jsonl.
- Paraphrase all sources.  Never store article text.
- Run python3 scripts/validate.py and do not push to main until it passes.

When finished, commit with the message "Run RUN_ID: <one-sentence summary>" and push to main.  End by summarising the headline changes in two or three sentences.
```
