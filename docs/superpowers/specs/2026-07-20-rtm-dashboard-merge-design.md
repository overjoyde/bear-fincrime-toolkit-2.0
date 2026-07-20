# Design: fold rtm-model-tuning-dashboard into bear-fincrime-toolkit-2.0

Date: 2026-07-20

## Context

overjoyde/rtm-model-tuning-dashboard is a bare React + Vite scaffold (no
views implemented yet, no backend, no data storage - "everything runs in
the browser" per its own README). overjoyde/bear-fincrime-toolkit-2.0 is
the practitioner AML/CTF LLM toolkit worked on in the prior session
(prompts/, profiles/, skills/, grounding/, pipelines/, evaluation/, data/,
docs/, mcp/, tests/ - all Python/Markdown).

Goal: fold the dashboard in as part of "toolkit 2.0" (bear-fincrime-toolkit-2.0
specifically, not the separate AMLGentex-llm-toolkit merge from the prior
session), and give it a first real view instead of leaving it a bare scaffold.

## Decisions (from brainstorming)

- Integration depth: side-by-side folder, plus a first real view that
  consumes the toolkit's own detection output - not just a repo merge.
- Tuning mechanics: the toolkit's detectors (see
  pipelines/detectors/structuring.py etc.) only emit a score (60-100) for
  entities that already cleared each detector's internal structural rule
  (e.g. structuring's "3+ near-threshold cash deposits within 72h"). There is
  no continuous score for every entity. "Tuning" therefore means: sweep that
  60-100 score threshold across the already-flagged entities and recompute
  precision/recall/F1 against ground truth live in the browser. Recall is
  capped by whatever each detector's structural rule already caught - a
  slider cannot recover entities the rule never flagged. No detector logic
  changes.
- Folder name: dashboard/ (short, generic - matches the llm-toolkit/
  naming style from the AMLGentex merge).
- Chart: a small hand-rolled inline-SVG line chart, no new npm
  dependency (precision + recall vs threshold, floor as a dashed reference
  line when evaluation/thresholds.json configures one).
- Data flow: checked-in static sample snapshot, not a live/CI-generated
  file. Regenerating it is a documented manual step.
- Testing infra: skip adding Vitest for this pass; manual spot-checks
  of metrics.js against the snapshot are enough given the scaffold has no
  test runner configured yet.
- Landing strategy: PR against main, draft first - same pattern as the
  AMLGentex-llm-toolkit merge.

## Design

### 1. Folder layout

Everything currently at the root of rtm-model-tuning-dashboard
(package.json, package-lock.json, vite.config.js, index.html,
src/, README.md, LICENSE, .gitignore) moves under dashboard/ at the
root of bear-fincrime-toolkit-2.0:

    bear-fincrime-toolkit-2.0/
    |-- prompts/ profiles/ skills/ grounding/ pipelines/ evaluation/ data/ docs/ mcp/ tests/
    |-- README.md, LICENSE, CONTRIBUTING.md, requirements-dev.txt
    |-- .github/workflows/
    |   |-- ci.yml                 (existing Python CI, gets a paths: filter - see 4)
    |   `-- dashboard-ci.yml         <- new
    `-- dashboard/                   <- new
        |-- package.json, package-lock.json, vite.config.js, index.html
        |-- README.md, LICENSE, .gitignore
        |-- scripts/
        |   `-- export_tuning_snapshot.py   <- new
        `-- src/
            |-- App.jsx                      (rewritten - see 5)
            |-- main.jsx                     (unchanged)
            |-- data/tuning-snapshot.json    <- new, checked-in sample
            |-- lib/metrics.js                <- new
            `-- components/
                |-- DetectorTuningPanel.jsx   <- new
                `-- PrecisionRecallChart.jsx  <- new

No filename collisions - the toolkit has no package.json/src/ at its
root.

### 2. History mechanism

Same mechanism as the AMLGentex merge, on a new branch add-rtm-dashboard
off bear-fincrime-toolkit-2.0's main:

git subtree add --prefix=dashboard https://github.com/overjoyde/rtm-model-tuning-dashboard.git main

Preserves the scaffold's history (currently a single initial commit) under
the dashboard/ prefix.

### 3. Data snapshot pipeline and schema

New script dashboard/scripts/export_tuning_snapshot.py, run manually
(not part of CI/build). It:

1. Calls the toolkit's data/synthetic_generator.py with a fixed seed to
   produce a transaction set (same invocation style as ci.yml's
   "Generate evaluation dataset" step: --customers 120 --months 3 --seed 7).
2. Calls pipelines/run_pipeline.run() to get the flagged-entity DataFrame
   (entity_id, detector, reason, score, raw_score, ...).
3. Loads the ground-truth CSV the same way evaluation/evaluate.py does
   (entity_id, typology, role columns), and reuses evaluate.py's
   TARGET_ROLES mapping (structuring->structurer, fan_in_out->mule,
   pass_through->conduit, community_ring->ring_member) to compute each
   detector's ground-truth positive entity set.
4. Loads evaluation/thresholds.json for the floor values.
5. Writes dashboard/src/data/tuning-snapshot.json:

    {
      "structuring": {
        "flagged": [{"entity_id": "C00042", "score": 78.4}],
        "ground_truth_positive_ids": ["C00042", "C00099"],
        "ground_truth_positive_count": 2,
        "floor": {"minimum_precision": 0.80, "minimum_recall": 0.80}
      },
      "fan_in_out": { "...same shape..." },
      "pass_through": { "...same shape..." },
      "community_ring": { "...same shape...", "floor": null }
    }

floor is null for community_ring (no configured threshold, matching
existing evaluation/thresholds.json and CI behavior).

### 4. CI

New .github/workflows/dashboard-ci.yml:
- actions/setup-node@v4 (Node 20), working-directory: dashboard on every
  step.
- npm ci, npm run lint, npm run build.
- paths: ['dashboard/**'] on both push and pull_request triggers.

Existing .github/workflows/ci.yml gets a matching
paths: ['pipelines/**', 'evaluation/**', 'data/**', 'tests/**', 'requirements-dev.txt']
so it stops running on dashboard-only changes (the reverse of the new
workflow's filter). No other changes to ci.yml.

### 5. React app structure

- dashboard/src/lib/metrics.js - pure functions, no React/DOM dependency:
  - computeMetricsAtThreshold(detectorSnapshot, threshold) -> {precision, recall, f1, tp, fp, fn}.
    tp = flagged entities with score >= threshold that are in
    ground_truth_positive_ids; fp = flagged with score >= threshold not
    in that set; fn = ground_truth_positive_count - tp. precision =
    tp/(tp+fp) (0 if no entities pass); recall = tp/ground_truth_positive_count
    (1.0 if ground_truth_positive_count is 0, matching evaluate.py's own
    convention).
  - metricsCurve(detectorSnapshot) -> array of the above computed at every
    distinct score value present in flagged, sorted ascending - the data
    the chart plots.
- dashboard/src/components/PrecisionRecallChart.jsx - inline SVG, no new
  dependency: two polylines (precision, recall) over the curve from
  metricsCurve, plus a dashed horizontal reference line per configured
  floor value when floor is not null.
- dashboard/src/components/DetectorTuningPanel.jsx - one card per detector:
  a range input (min=60 max=100), the live numbers
  (precision/recall/F1/TP/FP/FN) from computeMetricsAtThreshold at the
  slider's current value, the chart, and a pass/fail badge against the
  floor (or "no floor configured" for community_ring).
- dashboard/src/App.jsx - replaces the placeholder scaffold content with a
  page rendering one DetectorTuningPanel per key in the imported
  tuning-snapshot.json.
- dashboard/README.md - rewritten from "bare scaffold, no views
  implemented yet" to describe the tuning view, where the snapshot comes
  from, and the exact command to regenerate it.

### 6. Docs cross-linking

bear-fincrime-toolkit-2.0's root README.md "Repository layout" section
(a fenced tree diagram) gets one new line, and the previous last entry's
tree-connector changes from a corner to a middle branch:

    |-- data/         Synthetic transaction generator + sample dataset
    |-- dashboard/    Model tuning dashboard (React + Vite, client-side)
    `-- mcp/          MCP config examples (filesystem, SQLite) as a grounding layer

No other line in the README changes. (The actual file uses box-drawing
characters for the tree branches - the ASCII above is just this spec
describing the edit; the implementer edits the existing Unicode
characters in place, only inserting the new line and changing one
existing corner-to-middle connector.)

### 7. Out of scope

- No changes to any detector's internal logic (pipelines/detectors/*.py)
  or its structural thresholds - the dashboard tunes the alert-prioritization
  score threshold over already-flagged entities, not the detection rule
  itself.
- No backend, no database, no live data fetching - the dashboard stays
  fully client-side per its own original design intent.
- No Vitest/test-runner addition for this pass.
- No dependency unification between the toolkit's pip and the dashboard's
  npm tooling.

## Testing

- npm run build (inside dashboard/) must succeed - validates the
  snapshot import and component tree actually compile/render.
- npm run lint clean.
- Manual spot-check: for at least one detector, verify the displayed
  precision/recall at two different slider positions match hand-computed
  values from the snapshot JSON.
- Confirm ci.yml's Python suite is unaffected (still passes, still only
  triggers on its own paths).

## Delivery

Push branch add-rtm-dashboard to overjoyde/bear-fincrime-toolkit-2.0 and
open a draft PR against main.
