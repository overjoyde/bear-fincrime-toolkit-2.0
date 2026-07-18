#!/usr/bin/env python3
"""Run all detectors in pipelines/detectors/ against a transaction CSV.

Illustrative detection logic for practitioners to read, run, and adapt -
not a production transaction monitoring system. Every flag is a hypothesis
for a human analyst to assess, not a finding. See docs/01-data-hygiene.md
before pointing this at anything but synthetic or explicitly-approved data.
"""
import argparse
from pathlib import Path

import pandas as pd

from detectors import structuring, fan_in_out, pass_through, communities

DETECTORS = {
    "structuring": structuring.detect,
    "fan_in_out": fan_in_out.detect,
    "pass_through": pass_through.detect,
    "community_ring": communities.detect,
}


def run(input_path: Path, only=None) -> pd.DataFrame:
    transactions = pd.read_csv(input_path)
    required = {"sender_id", "receiver_id", "amount", "timestamp"}
    missing = required - set(transactions.columns)
    if missing:
        raise ValueError(f"input CSV is missing required columns: {sorted(missing)}")

    results = []
    for name, detect_fn in DETECTORS.items():
        if only and name not in only:
            continue
        flagged = detect_fn(transactions)
        if not flagged.empty:
            results.append(flagged)

    if not results:
        return pd.DataFrame(columns=["entity_id", "detector", "reason", "score"])
    return pd.concat(results, ignore_index=True).sort_values(["detector", "score"], ascending=[True, False])


def summarize(flags: pd.DataFrame) -> str:
    if flags.empty:
        return "No entities flagged by any detector."
    lines = [f"{len(flags)} flag(s) across {flags['entity_id'].nunique()} entities:"]
    for detector, group in flags.groupby("detector"):
        lines.append(f"  {detector}: {len(group)} entit{'y' if len(group) == 1 else 'ies'} flagged")
    top = flags.sort_values("score", ascending=False).head(5)
    lines.append("Top flags:")
    for _, row in top.iterrows():
        lines.append(f"  [{row['detector']}] {row['entity_id']}: {row['reason']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="path to a transactions CSV")
    parser.add_argument("--out", type=Path, default=Path("flags.csv"), help="path to write flagged results")
    parser.add_argument("--only", nargs="*", choices=list(DETECTORS.keys()), help="run only these detectors")
    args = parser.parse_args()

    flags = run(args.input, only=set(args.only) if args.only else None)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    flags.to_csv(args.out, index=False)

    print(summarize(flags))
    print(f"\nFull results written to {args.out}")


if __name__ == "__main__":
    main()
