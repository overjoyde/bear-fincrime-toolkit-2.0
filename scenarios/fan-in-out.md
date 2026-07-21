# Scenario: Fan-in / Fan-out (Mule Accounts)

## Status
Implemented - `pipelines/detectors/fan_in_out.py`

## Description
The classic mule-account pattern: an account receives money from many
distinct, often unrelated senders in a short window, then forwards most or
all of the accumulated total onward shortly after. The account itself
retains little to nothing — it's a pass-through point that fragments the
link between the original senders and the ultimate destination.

## Red flags / indicators
- An entity receiving from at least 6 distinct counterparties within a
  72-hour window.
- The account then forwarding at least 70% of the total received within
  that same window (rather than retaining it as would be expected of a
  genuine counterparty).
- No plausible business relationship between the entity and its many
  distinct senders.

## Detection approach
Implemented in `pipelines/detectors/fan_in_out.py`. For each entity, the
detector looks at incoming transactions within `WINDOW_HOURS` (72) of a
given first inbound transaction, and flags the entity once distinct senders
in that window reach `MIN_DISTINCT_SENDERS` (6) and outgoing transfers from
that same starting point out to 144 hours later (2× WINDOW_HOURS) forward at
least `MIN_PASS_THROUGH_RATIO` (0.7 = 70%) of the total received. The alert-prioritization score (60–100, see
`pipelines/README.md`) is derived from how far the sender count and
forward ratio exceed those minimums. The regression floor in
`evaluation/thresholds.json` is 0.80 minimum precision / 0.80 minimum
recall, checked by `evaluation/evaluate.py` and enforced as blocking in CI.

AMLTRIX equivalent: [T0011 – Money Mule Exploitation](https://framework.amltrix.com/techniques/T0011-money-mule-exploitation)
(sub-techniques: Regulated Exchange Mule Transactions, Crypto ATM Mule,
Casino Mule Networks). Content used under the
[AMLTRIX License Terms](https://framework.amltrix.com/license) — see
`scenarios/README.md`.

## Sources
- `pipelines/detectors/fan_in_out.py`
- `evaluation/thresholds.json`
- [AMLTRIX T0011 – Money Mule Exploitation](https://framework.amltrix.com/techniques/T0011-money-mule-exploitation)
