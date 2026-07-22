# Scenario: Pass-through (Rapid Movement / Conduit)

## Status
Implemented - `pipelines/detectors/pass_through.py`

## Description
An account repeatedly receives a large sum and forwards nearly all of it
onward within hours — not once, but across multiple separate rounds. Little
to no value is retained between receipt and forwarding, which is more
consistent with a conduit relaying funds on someone else's behalf than a
genuine counterparty transacting for its own purposes.

## Red flags / indicators
- Incoming transfers of at least 10,000 SEK.
- Each followed within 24 hours by outgoing transfers totaling between 85%
  and 110% of the incoming amount (not exactly 100%, since fees/rounding
  are expected — but not wildly more or less either).
- This receive-then-forward pattern repeating across at least 2 separate
  rounds for the same entity.
- Movement restricted to transfer channels (`channel == "transfer"`), not
  cash activity.

## Detection approach
Implemented in `pipelines/detectors/pass_through.py`. For each entity, the
detector matches incoming transfers of at least `MIN_AMOUNT` (10,000) to
outgoing transfers within `MAX_HOURS_BETWEEN` (24) hours whose total falls
between `MIN_FORWARD_RATIO` (0.85) and `MAX_FORWARD_RATIO` (1.10) of the
incoming amount, and flags the entity once at least `MIN_ROUNDS` (2) such
rounds are found. The alert-prioritization score (60–100, see
`pipelines/README.md`) is derived from how far the round count exceeds the
minimum and how close the average forward ratio sits to an exact 100%
pass-through. The regression floor in `evaluation/thresholds.json` is 0.75
minimum precision / 0.75 minimum recall, checked by `evaluation/evaluate.py`
and enforced as blocking in CI.

AMLTRIX equivalent: No direct AMLTRIX equivalent found. AMLTRIX's technique
catalog (304 techniques as of this writing, from
https://github.com/Amlyze/amltrix-data) was searched by name for
"pass-through", "conduit", and "rapid [movement]" with no match — this
pattern doesn't appear to be catalogued there as a distinct named
technique.

## Sources
- `pipelines/detectors/pass_through.py`
- `evaluation/thresholds.json`
