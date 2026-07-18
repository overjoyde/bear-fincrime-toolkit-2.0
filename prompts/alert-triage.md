# Prompt: Alert Triage

Single-turn prompt for a fast first pass on a TM alert. Pairs well with the
`tm-analyst` profile but works standalone in any chat.

## Prompt template

```
Here is a transaction monitoring alert. Analyze it and give me:
1. The most likely reason this alert fired (be specific about the pattern,
   not just "unusual activity").
2. Whether it resembles a known typology, and which one.
3. One concrete piece of missing information that would most change your
   assessment.
4. A recommended next step (escalate / close / request info) with brief
   reasoning - framed as a recommendation for me to confirm, not a decision.

Alert details:
- Customer type: <e.g. retail, business, PSP-agent>
- Alert trigger: <e.g. threshold breach, velocity, geographic>
- Transactions involved: <amounts, dates, counterparties - synthetic/redacted
  per your data-hygiene policy>
- Account history context: <e.g. tenure, typical activity level>
```

## Example (synthetic)

**Input:**
```
Customer type: retail, 14 months tenure
Alert trigger: six cash deposits between 8,600 and 9,800 SEK within three
days. The institution's illustrative internal scenario threshold is
10,000 SEK. This is not a statutory threshold for reporting.
Account history: typical monthly inflow ~4,000 SEK from stated salary
```

**Expected kind of output:**
- Likely trigger: repeated near-threshold cash deposits within a short window,
  well above the account's historical baseline.
- Typology match: structuring / smurfing (deliberate sub-threshold
  structuring), though a legitimate explanation (e.g. a one-off cash
  windfall) can't be ruled out from this alone.
- Missing info that would matter most: source of the cash (stated
  explanation), and whether this is a one-off deviation or part of a
  recurring pattern.
- Recommendation: escalate for analyst review of source-of-funds
  explanation before closing; volume and pattern both deviate meaningfully
  from baseline.

## Portability

Plain prompt, no Claude-specific features - works in any chat interface.
See `docs/06-portability.md`.
