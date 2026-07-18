#!/usr/bin/env python3
"""Evaluate detector output against role-aware synthetic ground truth."""

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.run_pipeline import run

TARGET_ROLES = {
    "structuring": {"structurer"},
    "fan_in_out": {"mule"},
    "pass_through": {"conduit"},
    "community_ring": {"ring_member"},
}

DEFAULT_THRESHOLDS = Path(__file__).with_name("thresholds.json")


def calculate_metrics(
    flags: pd.DataFrame,
    ground_truth: pd.DataFrame,
) -> dict[str, dict[str, float | int]]:
    """Calculate entity-level metrics for each detector's intended role."""
    metrics = {}
    for detector, target_roles in TARGET_ROLES.items():
        flagged_entities = set(
            flags.loc[flags["detector"] == detector, "entity_id"].astype(str)
        )
        target_rows = ground_truth[
            (ground_truth["typology"] == detector)
            & (ground_truth["role"].isin(target_roles))
        ]
        ground_truth_entities = set(target_rows["entity_id"].astype(str))

        true_positives = len(flagged_entities & ground_truth_entities)
        false_positives = len(flagged_entities - ground_truth_entities)
        false_negatives = len(ground_truth_entities - flagged_entities)
        precision = (
            true_positives / len(flagged_entities) if flagged_entities else 0.0
        )
        recall = (
            true_positives / len(ground_truth_entities)
            if ground_truth_entities
            else 1.0
        )
        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall
            else 0.0
        )

        metrics[detector] = {
            "true_positives": true_positives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "flagged_entities": len(flagged_entities),
            "ground_truth_entities": len(ground_truth_entities),
        }
    return metrics


def check_thresholds(
    metrics: dict[str, dict[str, float | int]],
    thresholds: dict[str, dict[str, float]],
) -> list[dict[str, float | str]]:
    """Return each configured regression threshold that was not met."""
    failures = []
    for detector, limits in thresholds.items():
        detector_metrics = metrics.get(detector)
        if detector_metrics is None:
            failures.append({
                "detector": detector,
                "metric": "detector",
                "actual": 0.0,
                "minimum": 1.0,
            })
            continue
        for key, minimum in limits.items():
            metric = key.removeprefix("minimum_")
            actual = float(detector_metrics[metric])
            if actual < minimum:
                failures.append({
                    "detector": detector,
                    "metric": metric,
                    "actual": actual,
                    "minimum": minimum,
                })
    return failures


def evaluate(
    transactions_path: Path,
    ground_truth_path: Path,
    thresholds_path: Path = DEFAULT_THRESHOLDS,
) -> dict:
    """Run the pipeline directly and evaluate its entity-level output."""
    flags = run(transactions_path)
    ground_truth = pd.read_csv(ground_truth_path)
    required = {"entity_id", "typology", "role"}
    missing = required - set(ground_truth.columns)
    if missing:
        raise ValueError(
            f"ground-truth CSV is missing required columns: {sorted(missing)}"
        )

    metrics = calculate_metrics(flags, ground_truth)
    with thresholds_path.open(encoding="utf-8") as handle:
        thresholds = json.load(handle)
    failures = check_thresholds(metrics, thresholds)
    return {
        "passed": not failures,
        "detectors": metrics,
        "threshold_failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transactions", type=Path, required=True)
    parser.add_argument("--ground-truth", type=Path, required=True)
    parser.add_argument(
        "--thresholds",
        type=Path,
        default=DEFAULT_THRESHOLDS,
        help="regression threshold JSON (defaults to evaluation/thresholds.json)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("evaluation-results.json"),
    )
    args = parser.parse_args()

    result = evaluate(
        args.transactions,
        args.ground_truth,
        args.thresholds,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )

    for detector, metrics in result["detectors"].items():
        print(
            f"{detector}: precision={metrics['precision']:.2%}, "
            f"recall={metrics['recall']:.2%}, f1={metrics['f1']:.2%}"
        )
    if result["threshold_failures"]:
        print("Regression thresholds not met:")
        for failure in result["threshold_failures"]:
            print(
                f"  {failure['detector']} {failure['metric']}: "
                f"{failure['actual']:.2%} < {failure['minimum']:.2%}"
            )
    print(f"Full results written to {args.out}")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
