# Scenario: Structuring / Smurfing

## Status
Implemented - `pipelines/detectors/structuring.py`

## Description
Breaking a larger sum of illicit cash into multiple smaller deposits, each
individually below a reporting or scrutiny threshold, so no single deposit
draws attention on its own. The deposits are usually clustered in a short
time window and, taken together, sum to a materially larger amount than
any one of them suggests.

## Red flags / indicators
- Multiple cash deposits to the same entity, each between 80% and 100% of
  an illustrative internal scenario threshold (10,000 SEK in this repo's
  synthetic data — not a statutory reporting threshold).
- At least 3 such deposits landing within a 72-hour window.
- The deposits in that window summing to at least the full scenario
  threshold, even though none individually reaches it.
- Channel is cash deposit specifically (`channel == "cash_deposit"`), not
  transfers or other movement types.

## Detection approach
Implemented in `pipelines/detectors/structuring.py`. For each entity
receiving cash deposits, the detector slides a window over deposits priced
between `NEAR_THRESHOLD_RATIO` (0.8) and 1.0 of `SCENARIO_AMOUNT_THRESHOLD`
(10,000), and flags the entity once a window of at least `MIN_DEPOSITS` (3)
such deposits within `WINDOW_HOURS` (72) sums to at least
`SCENARIO_AMOUNT_THRESHOLD`. The alert-prioritization score (60–100, see
`pipelines/README.md`) is derived from how far the deposit count and total
amount exceed those minimums. The regression floor in
`evaluation/thresholds.json` is 0.80 minimum precision / 0.80 minimum
recall, checked by `evaluation/evaluate.py` and enforced as blocking in CI.

AMLTRIX equivalent: [T0016 – Structuring](https://framework.amltrix.com/techniques/T0016-structuring)
(sub-techniques: Micro-Structuring, ATM Structuring, Smurfing, Cuckoo
Smurfing). Content used under the
[AMLTRIX License Terms](https://framework.amltrix.com/license) — see
`scenarios/README.md`.

## Sources
- `pipelines/detectors/structuring.py`
- `evaluation/thresholds.json`
- [AMLTRIX T0016 – Structuring](https://framework.amltrix.com/techniques/T0016-structuring)
