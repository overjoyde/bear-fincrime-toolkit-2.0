#!/usr/bin/env python3
"""Generate the dashboard's checked-in tuning snapshot from the toolkit's
own synthetic data generator, detection pipeline, and ground truth.

Regenerate after changing detector logic or the synthetic generator:
    python dashboard/scripts/export_tuning_snapshot.py
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.run_pipeline import run  # noqa: E402
from evaluation.evaluate import TARGET_ROLES  # noqa: E402

OUT_PATH = Path(__file__).resolve().parents[1] / "src" / "data" / "tuning-snapshot.json"
THRESHOLDS_PATH = ROOT / "evaluation" / "thresholds.json"


def generate_data(out_dir):
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "data" / "synthetic_generator.py"),
            "--customers", "120",
            "--months", "3",
            "--seed", "7",
            "--out", str(out_dir),
        ],
        check=True,
    )
    return out_dir / "transactions.csv", out_dir / "ground_truth.csv"


def build_snapshot(flags, ground_truth, thresholds):
    snapshot = {}
    for detector, target_roles in TARGET_ROLES.items():
        detector_flags = flags[flags["detector"] == detector]
        flagged = [
            {"entity_id": str(row.entity_id), "score": float(row.score)}
            for row in detector_flags.itertuples()
        ]
        target_rows = ground_truth[
            (ground_truth["typology"] == detector)
            & (ground_truth["role"].isin(target_roles))
        ]
        ground_truth_positive_ids = sorted(
            target_rows["entity_id"].astype(str).unique().tolist()
        )
        snapshot[detector] = {
            "flagged": flagged,
            "ground_truth_positive_ids": ground_truth_positive_ids,
            "ground_truth_positive_count": len(ground_truth_positive_ids),
            "floor": thresholds.get(detector),
        }
    return snapshot


def main():
    with tempfile.TemporaryDirectory() as tmp:
        transactions_path, ground_truth_path = generate_data(Path(tmp))
        flags = run(transactions_path)
        ground_truth = pd.read_csv(ground_truth_path)

    with THRESHOLDS_PATH.open(encoding="utf-8") as handle:
        thresholds = json.load(handle)

    snapshot = build_snapshot(flags, ground_truth, thresholds)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    print("Wrote snapshot for " + str(len(snapshot)) + " detectors to " + str(OUT_PATH))


if __name__ == "__main__":
    main()
