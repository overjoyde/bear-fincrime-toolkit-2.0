---
name: model-doc-writer
description: Drafts and maintains generic model validation / model documentation sections (methodology, assumptions, limitations, validation tests, monitoring plan) for a detection rule or scoring model. Use when asked to write, draft, or update model documentation, a model validation write-up, or a governance/model-risk artifact for a TM rule or risk model.
---

# Model Documentation Writer

Helps draft the documentation artifacts model-risk/governance functions
typically expect for a detection rule, scoring model, or risk-classification
model - structure and prompting only, no institution-specific content is
assumed or invented.

## When this applies

- The user asks for a model documentation draft, a validation write-up, or
  a governance artifact for a rule/model described in the conversation or in
  a file in this repo (e.g. one of the `pipelines/detectors/`).

## Standard sections to draft

1. **Purpose and scope** - what the model/rule is meant to detect, what
   population it applies to, what it explicitly does not cover.
2. **Methodology** - the actual logic (thresholds, statistical method,
   network-analysis approach), described precisely enough that someone
   without the code could reproduce the logic on paper.
3. **Assumptions and limitations** - what the model assumes about the data
   or population that, if false, would degrade performance; known blind
   spots (e.g. a threshold-based structuring detector will miss structuring
   spread across an amount range wider than its window).
4. **Validation approach** - what was tested (backtest window, out-of-sample
   check, sensitivity analysis) and what the results mean - never assert a
   model is validated; describe what testing occurred and let the human
   author state the conclusion.
5. **Monitoring plan** - what should be tracked post-deployment to catch
   drift or degradation (e.g. alert volume trend, override rate, known
   comparator metric).

## How to draft

1. Ask what specific rule/model this is for if not already clear - point to
   the relevant file in `pipelines/detectors/` if it's one of this repo's.
2. Draft each section using only what's actually known (the code's logic,
   any test results the user supplies) - use explicit placeholders like
   "[institution to confirm: backtest window and sample size]" rather than
   inventing numbers.
3. Never fill in a validation conclusion, an approval, or a risk rating -
   those are governance decisions, not drafting tasks.

## Boundaries

- This produces a draft for a human owner to complete, review, and approve -
  never a finished, signed-off artifact.
- No institution name, policy reference, or approval workflow is assumed;
  ask if the user wants those woven in, and if so, treat that detail as
  sensitive per `docs/01-data-hygiene.md`.
