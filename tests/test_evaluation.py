import json

import pandas as pd

import evaluation.evaluate as evaluator


def test_role_mapping_excludes_fan_in_senders_from_false_negatives():
    flags = pd.DataFrame([{
        "entity_id": "MULE",
        "detector": "fan_in_out",
    }])
    ground_truth = pd.DataFrame([
        {"entity_id": "MULE", "typology": "fan_in_out", "role": "mule"},
        {
            "entity_id": "SENDER_1",
            "typology": "fan_in_out",
            "role": "fan_in_sender",
        },
        {
            "entity_id": "SENDER_2",
            "typology": "fan_in_out",
            "role": "fan_in_sender",
        },
    ])

    metrics = evaluator.calculate_metrics(flags, ground_truth)["fan_in_out"]

    assert metrics["true_positives"] == 1
    assert metrics["false_negatives"] == 0
    assert metrics["ground_truth_entities"] == 1
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0


def test_metrics_report_false_positives_and_false_negatives():
    flags = pd.DataFrame([
        {"entity_id": "MATCH", "detector": "structuring"},
        {"entity_id": "FALSE_POSITIVE", "detector": "structuring"},
    ])
    ground_truth = pd.DataFrame([
        {
            "entity_id": "MATCH",
            "typology": "structuring",
            "role": "structurer",
        },
        {
            "entity_id": "MISSED",
            "typology": "structuring",
            "role": "structurer",
        },
    ])

    metrics = evaluator.calculate_metrics(flags, ground_truth)["structuring"]

    assert metrics == {
        "true_positives": 1,
        "false_positives": 1,
        "false_negatives": 1,
        "precision": 0.5,
        "recall": 0.5,
        "f1": 0.5,
        "flagged_entities": 2,
        "ground_truth_entities": 2,
    }


def test_evaluator_runs_pipeline_directly(tmp_path, monkeypatch):
    transactions_path = tmp_path / "transactions.csv"
    ground_truth_path = tmp_path / "ground_truth.csv"
    thresholds_path = tmp_path / "thresholds.json"
    called = []

    pd.DataFrame([{
        "entity_id": "CUSTOMER",
        "typology": "structuring",
        "role": "structurer",
    }]).to_csv(ground_truth_path, index=False)
    thresholds_path.write_text("{}", encoding="utf-8")

    def fake_run(path):
        called.append(path)
        return pd.DataFrame([{
            "entity_id": "CUSTOMER",
            "detector": "structuring",
        }])

    monkeypatch.setattr(evaluator, "run", fake_run)

    result = evaluator.evaluate(
        transactions_path,
        ground_truth_path,
        thresholds_path,
    )

    assert called == [transactions_path]
    assert result["passed"] is True
    assert result["detectors"]["structuring"]["f1"] == 1.0


def test_threshold_check_returns_each_blocking_regression():
    metrics = {
        "pass_through": {
            "precision": 0.7,
            "recall": 0.5,
        }
    }
    thresholds = {
        "pass_through": {
            "minimum_precision": 0.75,
            "minimum_recall": 0.75,
        }
    }

    failures = evaluator.check_thresholds(metrics, thresholds)

    assert failures == [
        {
            "detector": "pass_through",
            "metric": "precision",
            "actual": 0.7,
            "minimum": 0.75,
        },
        {
            "detector": "pass_through",
            "metric": "recall",
            "actual": 0.5,
            "minimum": 0.75,
        },
    ]


def test_evaluation_output_is_json_serializable():
    flags = pd.DataFrame(columns=["entity_id", "detector"])
    ground_truth = pd.DataFrame(columns=["entity_id", "typology", "role"])

    metrics = evaluator.calculate_metrics(flags, ground_truth)

    json.dumps(metrics)
