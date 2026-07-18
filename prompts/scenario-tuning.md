# Prompt: Scenario / Rule Tuning

Single-turn prompt for reasoning through a proposed change to a TM rule or
threshold. Pairs well with the `rule-tuning-quant` profile.

## Prompt template

```
I'm considering a change to a transaction monitoring rule. Help me think
through it - do not tell me it's safe to deploy, just help me reason and
identify what I'd need to check.

Current rule: <describe the rule and threshold as it stands today>
Proposed change: <describe the proposed new threshold/logic>
What I know about current performance: <alert volume, known false-positive
rate, any segment-level detail you have>

Walk me through:
1. What assumption the current threshold encodes, and what assumption the
   proposed change encodes instead.
2. What direction and rough magnitude of change I should expect in alert
   volume and in detection coverage, and which customer segment is most
   affected.
3. What a defensible backtest would need to control for (seasonality, any
   other recent tuning change, population drift) so I don't fool myself with
   a misleading before/after comparison.
4. What I'd need to document for model-risk/governance to make this change
   auditable.
```

## Example (synthetic)

**Input:**
```
All amounts and thresholds below are fictitious illustrative internal
scenario settings. They are not statutory thresholds for reporting.

Current rule: flag any single cash deposit over 9,000 SEK for retail
accounts.
Proposed change: raise threshold to 9,800 SEK to reduce false positives
from customers who round large legitimate cash deposits near 10,000 SEK.
What I know: current false-positive rate on this rule is roughly 70% on
manual review; volume is ~400 alerts/month.
```

**Expected kind of output:**
- Current assumption: legitimate retail cash deposits rarely land just under
  10,000 SEK; the threshold targets sub-threshold structuring specifically.
- Expected direction: modest volume reduction concentrated in the
  9,000-9,799 SEK band; coverage loss concentrated on structuring attempts
  that specifically target that narrower band - flag that determined
  structuring could simply shift down a few hundred SEK.
- Backtest considerations: compare FP rate in the affected band specifically
  (not overall rule volume), check for a seasonal cash pattern (e.g. holiday
  bonuses) that could confound the comparison window.
- Documentation: rationale for the new threshold, the specific band analysis,
  and an explicit note that determined structuring below the new threshold
  remains a residual risk this change doesn't address.

## Portability

Plain prompt, no Claude-specific features. See `docs/06-portability.md`.
