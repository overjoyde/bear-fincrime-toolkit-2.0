# Design: add a `scenarios/` folder

Date: 2026-07-22

## Context

bear-fincrime-toolkit-2.0 has four working typology detectors in
`pipelines/detectors/` (structuring, fan_in_out, pass_through, communities),
each an explainable heuristic with named threshold constants, a normalized
60-100 alert-prioritization score, and a precision/recall floor in
`evaluation/thresholds.json` (communities has no configured floor). The repo
has no folder that documents these typologies as prose - the closest things
are `pipelines/README.md` (a one-line-per-detector table) and
`skills/typology-research/SKILL.md`, which defines a standard typology-brief
format but explicitly instructs saving briefs *outside* the repo as personal
reference material, not as toolkit content.

Separately, https://framework.amltrix.com/techniques/T0083-funnel-accounts
(AMLTRIX, a MITRE-ATT&CK-style framework for money-laundering techniques)
was read in full: technique T0083 "Funnel Accounts" - depositing structured
cash below regulatory reporting limits in one location and rapidly moving it
elsewhere. It is not implemented by any current detector.

Goal: create a `scenarios/` folder of structured typology write-ups - one
per existing detector, grounded in the real implemented code, plus a new one
for Funnel Accounts grounded in the AMLTRIX page content - and reconcile the
now-contradictory guidance in `skills/typology-research/SKILL.md`.

## Decisions (from brainstorming)

- Scope: documentation only. No new Python detector for Funnel Accounts in
  this pass - `scenarios/funnel-accounts.md` is grounding for a possible
  future detector, explicitly marked as not yet implemented.
- One doc per typology, five total: `structuring.md`, `fan-in-out.md`,
  `pass-through.md`, `communities.md`, `funnel-accounts.md`.
- Shared template spine across all five (see below). The four implemented
  ones are grounded strictly in the real code (file path, actual named
  constants, actual score contract, actual evaluation floor or lack of one)
  - never a generic/invented description of the pattern.
- `funnel-accounts.md` additionally carries sections the other four don't
  (Mitigations, Actor profiles, Data sources, Related instruments/services
  exploited) because that substantive content exists in the AMLTRIX source
  and the brief spine has nowhere to put it. No AMLTRIX cross-referencing
  for the other four detectors in this pass - out of scope unless requested
  separately.
- `skills/typology-research/SKILL.md` gets a repo-aware branch: when working
  inside a repo that has a `scenarios/` folder, use that folder and its
  template instead of an external personal collection. The "save outside
  the repo" guidance still applies to ad hoc typology research with no
  `scenarios/` folder to land in.

## Design

### 1. Template (shared spine, `scenarios/README.md`)

```markdown
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
  time windows, and the score contract (60-100, see
  `pipelines/README.md`), plus the evaluation floor from
  `evaluation/thresholds.json` (or "no floor configured" for communities).
- Not yet implemented: what data/structural rule would be needed, phrased
  against this repo's actual schema (`data/synthetic_generator.py` columns)
  and the "Adding a new detector" recipe in `pipelines/README.md`.

## Sources
Named, linkable sources only.
```

`scenarios/README.md` states this template once; each scenario file is the
template filled in, not a restatement of the template itself.

### 2. The five files

| File | Status | Grounded in |
|---|---|---|
| `structuring.md` | Implemented | `pipelines/detectors/structuring.py` (SCENARIO_AMOUNT_THRESHOLD=10000, MIN_DEPOSITS=3, WINDOW_HOURS=72, NEAR_THRESHOLD_RATIO=0.8); floor 0.80/0.80 |
| `fan-in-out.md` | Implemented | `pipelines/detectors/fan_in_out.py` (WINDOW_HOURS=72, MIN_DISTINCT_SENDERS=6, MIN_PASS_THROUGH_RATIO=0.7); floor 0.80/0.80 |
| `pass-through.md` | Implemented | `pipelines/detectors/pass_through.py` (MAX_HOURS_BETWEEN=24, MIN_FORWARD_RATIO=0.85, MAX_FORWARD_RATIO=1.10, MIN_ROUNDS=2, MIN_AMOUNT=10000); floor 0.75/0.75 |
| `communities.md` | Implemented | `pipelines/detectors/communities.py` (MIN_COMMUNITY_SIZE=4, MAX_COMMUNITY_SIZE=25, MIN_INTERNAL_DENSITY=0.35, MIN_INTERNAL_VOLUME_SHARE=0.6, Louvain via networkx); no floor configured |
| `funnel-accounts.md` | Not yet implemented | AMLTRIX T0083 (full indicator/mitigation/actor/data-source content already extracted) |

Each implemented doc's Red flags section is derived from what the detector's
`reason` string and constants actually check for - not a generic textbook
description of the typology that happens to not match the code.

### 3. `skills/typology-research/SKILL.md` update

Add a step 0 to "How to research":

> 0. If the current repo has a `scenarios/` folder, write the brief there
>    using its template (`scenarios/README.md`) instead of an external
>    personal collection - steps 1-4 below describe ad hoc research with no
>    such folder to land in.

No other content in the skill file changes.

### 4. Cross-linking

`pipelines/README.md`'s existing per-detector table gets one trailing
sentence: "See `scenarios/<file>.md` for the full typology write-up." No
other change to that file. Root `README.md`'s repository-layout tree gets
one new `scenarios/` line, matching the style used for the `dashboard/` line
added in the prior merge.

## Out of scope

- No new Python detector, generator routine, test, or evaluation-threshold
  entry for Funnel Accounts.
- No AMLTRIX (or other framework) cross-referencing for the four existing
  detectors.
- No changes to detector logic, thresholds, or scoring.

## Testing

- Manual read-through: every implemented doc's constants/floor match the
  actual current values in `pipelines/detectors/*.py` and
  `evaluation/thresholds.json` at time of writing.
- `funnel-accounts.md` content checked against the AMLTRIX extraction for
  completeness (nothing substantive from the source dropped).
- No automated tests apply - this is a documentation-only change with no
  code path.

## Delivery

Push branch `docs/scenarios-funnel-accounts` to
`overjoyde/bear-fincrime-toolkit-2.0` and open a draft PR against `main`.
