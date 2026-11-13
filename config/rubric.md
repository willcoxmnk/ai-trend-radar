# Scoring rubric

Rubric version: 2.0

Any change to this file must increment the version.  The version is recorded in the register and in each run-log line, so a score change caused by a rubric change can be told apart from one caused by the world changing.

## Importance (1-5)

How significant the trend is for enterprises in general, across industries, over the next two to three years.

| Score | Meaning | Typical evidence |
|---|---|---|
| 5 | Defining shift | Multiple independent tier 1 sources treat it as a headline theme, backed by adoption data or quantified forecasts, and standards, regulatory or major platform activity |
| 4 | Major trend | At least two independent tier 1-2 sources, with quantified forecasts or adoption data |
| 3 | Established but secondary | One tier 1-2 source plus credible tier 3-4 support, or a strong practitioner consensus |
| 2 | Emerging | Credible but limited evidence, mostly tier 3-4, or early signals only |
| 1 | Marginal | Mentioned, but with little substantive evidence or clear counter-evidence |

Importance is industry-agnostic.  Evidence from a single industry counts towards importance only as general adoption evidence, and strong relevance to one industry never on its own justifies a high importance score.  Equally, a trend can score 5 for importance without any industry-specific evidence.

## Industry relevance (1-5, per industry)

How much the trend matters to firms in a given industry.  Each trend has one score for every industry in `config/industries.json`.

| Score | Meaning |
|---|---|
| 5 | Directly changes how firms in the industry compete or operate, with industry-specific evidence (regulators, industry bodies, company disclosures, sector research) |
| 4 | Clear, near-term application in the industry, with at least some industry-specific evidence |
| 3 | Relevant through general enterprise adoption; no industry-specific evidence yet |
| 2 | Indirect or long-term relevance to the industry |
| 1 | Little relevance to the industry |
| null | Not yet assessed |

Scores of 4 or 5 require industry-specific evidence in the ledger.  Where no industry-specific evidence has been found, the default for a generally important trend is 3.

## Signals to weigh

When scoring, consider each of these and name the ones that drove a change in the rationale.

- **S1 Coverage.**  Number of independent tier 1-2 sources treating the trend as significant in the lookback window.
- **S2 Quantification.**  New forecasts, adoption figures, spend data or benchmark results.
- **S3 Institutional action.**  Standards ratified, regulation enacted or delayed, open-source projects moving to neutral foundations, major platform launches.
- **S4 Industry signals.**  Evidence specific to an industry in `config/industries.json`.  This informs industry relevance and counts towards importance only as general adoption evidence.
- **S5 Counter-evidence.**  Failed deployments, cancelled projects, downgraded forecasts, credible sceptical analysis.

## Change rules (hysteresis)

These rules prevent noise.  Apply them strictly.

1. A score may change only if at least one new ledger entry supports or contradicts the trend in this run.  There are two exceptions: a trend's second run, when momentum moves from `baseline` to `stable`, `rising` or `fading`; and a first assessment of an industry relevance score, when it moves from `null` to a value.  A first assessment must still cite evidence, and may draw on existing ledger entries.
2. Importance and each industry relevance score may move by at most 1 point per run, unless two or more new independent tier 1 sources point the same way, in which case it may move by 2.
3. Tier 4 sources alone cannot change any score.
4. Momentum:
   - `rising`: importance increased this run on tier 1-2 evidence, or net supporting evidence has outweighed contradicting evidence for two consecutive runs.
   - `fading`: importance decreased this run on tier 1-2 evidence, or the trend has had no new supporting evidence for two consecutive runs, or contradicting evidence has outweighed support for two consecutive runs.
   - `stable`: anything else after the baseline run.
   - `baseline`: only used for a trend's first run.
5. Confidence:
   - `high`: at least three independent sources, including two or more tier 1-2 primary (not secondary) sources.
   - `medium`: at least two independent sources, at least one tier 1-2.
   - `low`: anything less, or heavy reliance on secondary reporting.

## Thresholds for proposals

- **Promote a watch-list item** when it has at least two independent tier 1-2 sources, or has been seen in three runs with growing evidence.
- **Propose a merge** when two trends share most of their supporting evidence for two consecutive runs.
- **Propose a retirement** when importance has been 2 or less for three consecutive runs, or no new evidence has arrived for six months.
