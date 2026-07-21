# Scenarios

Structured typology write-ups: one per detector implemented in
`pipelines/detectors/`, plus typologies not yet implemented but worth
tracking. Each file follows the same shape:

```
# Scenario: <Name>

## Status
Implemented - `pipelines/detectors/<file>.py` | Not yet implemented

## Description
Plain-language description of the pattern and why it's used to obscure
illicit funds.

## Red flags / indicators
Concrete, checkable list.

## Detection approach
- Implemented: the real triggering conditions, named threshold constants,
  time windows, and the score contract (see `pipelines/README.md`), plus
  the evaluation floor from `evaluation/thresholds.json` (or "no floor
  configured").
- Not yet implemented: what data/structural rule would be needed, against
  this repo's actual schema and the "Adding a new detector" recipe in
  `pipelines/README.md`.

## Sources
Named, linkable sources only.
```

For the four already-implemented typologies, every claim in "Detection
approach" is grounded in the actual code — not a generic textbook
description that happens not to match what's implemented. If a section
can't be grounded that way, it says so rather than guessing.

## AMLTRIX attribution

`funnel-accounts.md`, and the single AMLTRIX cross-reference lines in
`structuring.md` and `fan-in-out.md`, use content from
[AMLTRIX](https://framework.amltrix.com/) (© UAB "Amlyze"), used under the
[AMLTRIX License Terms](https://framework.amltrix.com/license). This is
attribution, not endorsement — AMLTRIX has not reviewed or approved this
repository's use of its content.

## Files

| File | Status |
|---|---|
| `structuring.md` | Implemented |
| `fan-in-out.md` | Implemented |
| `pass-through.md` | Implemented |
| `communities.md` | Implemented |
| `funnel-accounts.md` | Not yet implemented |
