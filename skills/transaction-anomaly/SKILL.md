---
name: transaction-anomaly
description: Runs the toolkit's detection pipeline (structuring, fan-in/out, pass-through, network communities) against a synthetic or approved transaction CSV and returns flagged entities with reason codes. Use when asked to analyze, screen, or flag transactions for anomalies or AML typologies, or to run/interpret the pipelines/ detectors in this repo.
---

# Transaction Anomaly Detection

Wraps the detectors in `pipelines/` so they can be invoked as part of a
Claude Code session instead of run manually.

## When this applies

- The user attaches or points to a transaction CSV (columns roughly:
  transaction_id, sender_id, receiver_id, amount, currency, timestamp) and
  asks for anomaly/typology analysis.
- The user asks to run, tune, or interpret output from `pipelines/run_pipeline.py`.

## What to do

1. Confirm the input file is synthetic or explicitly approved for LLM-assisted
   analysis (see `docs/01-data-hygiene.md`). If unclear, ask before proceeding.
2. Run the pipeline:
   ```bash
   python pipelines/run_pipeline.py --input <path-to-csv> --out /tmp/flags.csv
   ```
3. Read `/tmp/flags.csv` and summarize the results: how many entities flagged,
   by which detector(s), and the top few by score. Do not just dump the raw
   CSV back at the user - synthesize it.
4. If asked to explain a specific flag, read the relevant detector in
   `pipelines/detectors/` and explain the actual logic that fired (the
   threshold or pattern it checked), not a generic description of the
   typology.
5. If asked to tune a threshold, edit the named constant in the relevant
   detector file (never a magic number inline), re-run, and report the
   before/after flag counts.

## Output format

A short summary (counts, top flags) followed by the path to the full
results CSV. Offer to explain any specific flag in more depth rather than
front-loading every detail.

## Boundaries

- Never treats a flag as a confirmed finding - always "flagged by
  {detector} because {condition}," left for a human analyst to assess.
- Never operates on a file outside `data/generated/`, `data/sample/`, or a
  path the user has explicitly confirmed is approved for this use.
