# Prompt: Regulatory Gap Analysis

Single-turn prompt for comparing a described internal process or control
against a specific regulatory requirement. Pairs well with the `reg-watch`
profile.

## Prompt template

```
Compare the process I describe below against the regulatory requirement I
cite, and identify gaps. Do not give legal advice - identify textual gaps
and flag anything ambiguous enough to need legal/compliance sign-off.

Regulatory requirement: <cite the specific instrument and article/section -
see grounding/eu-instruments.md and grounding/se-instruments.md for
canonical references>
Requirement text (paste the relevant excerpt): <...>
Current process, as I understand it: <describe the process in plain terms>

Walk me through:
1. What the requirement text actually specifies (obligation, trigger
   condition, timeline, and to whom it applies).
2. Where the described process appears to satisfy the requirement, and
   where it doesn't or where the evidence is unclear.
3. Anything in the requirement that is ambiguous enough that two reasonable
   people could read it differently - flag these explicitly rather than
   picking an interpretation silently.
4. A prioritized list of gaps (if any), each with why it matters, not just
   that it exists.
```

## Example (synthetic)

**Input:**
```
Requirement: [illustrative excerpt requiring reassessment of customer risk
classification "without undue delay" following a materially relevant change
in circumstances]
Current process: risk classifications are reassessed on a fixed annual
schedule; there is no separate trigger for interim reassessment tied to a
specific triggering event.
```

**Expected kind of output:**
- Requirement specifies an event-triggered obligation ("without undue delay"
  after a material change), separate from any periodic review cycle.
- Gap: the described process only has a periodic (annual) trigger, not an
  event-driven one - a material change occurring shortly after the annual
  review could go unaddressed for up to a year.
- Ambiguity to flag: "without undue delay" and "materially relevant change"
  are undefined in the excerpt - what counts as material, and what timeline
  counts as "undue delay," need legal/compliance definition before this gap
  can be sized precisely.
- Priority: this is a structural gap (missing trigger type), not a tuning
  issue - flag for legal/compliance and process-design attention.

## Portability

Plain prompt, no Claude-specific features. See `docs/06-portability.md`.
