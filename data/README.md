# Synthetic data

## synthetic_generator.py

Generates a fully synthetic set of customers and transactions with four
injected typologies and a ground-truth label file, so every prompt, profile,
and skill in this repo can be developed and tested without ever touching
real data. See `docs/01-data-hygiene.md` for why this matters.

```bash
python synthetic_generator.py --customers 500 --months 6 --out generated/ --seed 42
```

Output (written to `--out`):

- `transactions.csv` — transaction_id, sender_id, receiver_id, amount,
  currency, timestamp, channel. Looks like a raw export - no typology label
  on the rows themselves, matching how real data actually looks.
- `customers.csv` — customer_id, name, customer_type, expected_monthly_volume,
  onboarding_days_ago.
- `ground_truth.csv` — entity_id, typology, role. Which customers were part
  of an injected pattern, and what role they played (structurer, mule,
  fan_in_sender, conduit, ring_member). Use this to check whether
  `pipelines/run_pipeline.py` actually catches what was injected - it is not
  an input to any detector, only a scorecard.
- `synthetic.db` (with `--sqlite`) — the same customers/transactions tables
  in SQLite, for the MCP setup in `mcp/sqlite-mcp.md`.

### Injected typologies

| Typology | What it looks like |
|---|---|
| `structuring` | Several cash deposits just under a reporting threshold, clustered in a short window, summing well above it |
| `fan_in_out` | A mule account receiving from many unrelated senders in a short window, then forwarding most of it to one or two receivers |
| `pass_through` | An account receiving a large sum and forwarding nearly all of it within hours to a day, repeatedly |
| `community_ring` | A small cluster of accounts transacting mostly among themselves - individually unremarkable transactions, suspicious only as a network |

`--seed` controls reproducibility; the same seed always produces the same
dataset. Re-run with a different seed for a fresh dataset with the same
statistical shape.

### sample/

A small pre-generated dataset (25 customers, 2 months, seed 7) committed to
the repo so you can try the pipeline without generating anything first:

```bash
cd ../pipelines && python run_pipeline.py --input ../data/sample/transactions.csv
```

## Public synthetic datasets, for comparison

This repo's generator is intentionally small and dependency-free so it runs
anywhere with just the standard library. For larger-scale or more
statistically rigorous synthetic data, these public datasets are worth
knowing (see `grounding/resources.md` for more detail and current hosting
locations, since dataset mirrors move over time):

- **SAML-D** — labeled synthetic AML transaction dataset built specifically
  for ML-based detection research.
- **AMLSim** — an agent-based transaction simulator (originally IBM
  Research) that generates larger, more realistic multi-typology
  transaction graphs.
- **PaySim** — a widely-used synthetic mobile-money dataset, strong for
  fraud/AML benchmarking though with narrower typology coverage than AMLSim.

Use this repo's generator for quick iteration on prompts/skills/pipelines;
reach for one of the above when you need a larger or more heavily-cited
benchmark dataset.
