from pathlib import Path

import pandas as pd
import pytest

from pipelines import run_pipeline

from conftest import PROJECT_ROOT


def test_pipeline_sorts_all_flags_by_normalized_score(tmp_path, monkeypatch):
    transactions_path = tmp_path / "transactions.csv"
    pd.DataFrame([{
        "sender_id": "A",
        "receiver_id": "B",
        "amount": 100,
        "timestamp": "2026-01-01 00:00:00",
    }]).to_csv(transactions_path, index=False)

    def detector(name, score):
        def detect(_transactions):
            return pd.DataFrame([{
                "entity_id": name,
                "detector": name,
                "reason": "test",
                "score": score,
                "raw_score": 1,
            }])

        return detect

    monkeypatch.setattr(run_pipeline, "DETECTORS", {
        "lower": detector("lower", 65),
        "higher": detector("higher", 95),
        "middle": detector("middle", 80),
    })

    flags = run_pipeline.run(transactions_path)

    assert flags["score"].tolist() == [95, 80, 65]


def test_pipeline_scores_use_shared_range():
    flags = run_pipeline.run(
        PROJECT_ROOT / "data" / "sample" / "transactions.csv"
    )

    assert not flags.empty
    assert flags["score"].between(60, 100).all()
    assert flags["raw_score"].notna().all()


def test_pipeline_rejects_missing_required_columns(tmp_path):
    input_path = tmp_path / "invalid.csv"
    pd.DataFrame([{"amount": 100}]).to_csv(input_path, index=False)

    with pytest.raises(ValueError, match="missing required columns"):
        run_pipeline.run(Path(input_path))
