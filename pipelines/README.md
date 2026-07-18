# Detection pipelines

Real, runnable Python implementing four common typologies as explainable
heuristics. This is here so you have something to actually run, read, and
adapt - not a production transaction monitoring system, and not a claim
that these thresholds are tuned for any real institution.

## Detectors

| File | Typology | Core logic |
|---|---|---|
| `detectors/structuring.py` | Structuring / smurfing | Sliding time window; flags near-threshold deposits that individually stay under a reporting threshold but sum above it |
| `detectors/fan_in_out.py` | Mule accounts | Flags entities receiving from many distinct senders in a window, then forwarding most of it onward shortly after |
| `detectors/pass_through.py` | Rapid movement / conduit | Flags entities that repeatedly receive a large sum and forward nearly all of it within hours |
| `detectors/communities.py` | Network rings | Louvain community detection on the transaction graph; flags tightly-connected clusters where volume mostly stays inside the cluster |

Every detector takes a pandas DataFrame of transactions and returns a
DataFrame of `entity_id, detector, reason, score` rows. Thresholds are named
constants at the top of each file - change them, don't hardcode new magic
numbers elsewhere.

## Running it

```bash
pip install -r requirements.txt
python run_pipeline.py --input ../data/sample/transactions.csv --out flags.csv
```

Or against a freshly generated dataset:

```bash
cd ../data && python synthetic_generator.py --customers 500 --months 6 --out generated/
cd ../pipelines && python run_pipeline.py --input ../data/generated/transactions.csv
```

Run a subset of detectors with `--only`:

```bash
python run_pipeline.py --input ../data/sample/transactions.csv --only structuring fan_in_out
```

## Checking against ground truth

`data/synthetic_generator.py` writes a `ground_truth.csv` alongside its
transactions - which entities were part of an injected typology, and what
role they played. Compare `flags.csv` against it to see what the pipeline
caught and what it missed; this is a good way to understand each detector's
actual blind spots (for example, `structuring.py`'s window/threshold
constants will miss structuring spread across a wider amount range or a
longer time window than it checks).

## Scope and honesty about limitations

- These are heuristics chosen for clarity, not the result of a validated
  model. Every threshold is a starting point to adapt, not a recommendation.
- False positives are expected and by design not suppressed - the point is
  to give a human analyst a starting hypothesis with an explainable reason,
  not to make a filtering decision.
- None of this is a substitute for your institution's actual TM system,
  validation process, or governance requirements - see
  `skills/model-doc-writer/SKILL.md` if you need to document a real rule
  properly.

## Adding a new detector

1. Add a generator routine for the pattern to `data/synthetic_generator.py`
   first, so you can test against data with the pattern actually present.
2. Add `detectors/<name>.py` with a `detect(transactions) -> pd.DataFrame`
   function returning the same four columns as the existing detectors.
3. Register it in `DETECTORS` in `run_pipeline.py`.
