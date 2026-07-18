"""Structuring / smurfing detector.

Flags entities receiving several cash deposits that individually sit just
under an illustrative internal scenario threshold and cluster in a short
time window. This is a simple, explainable heuristic - not a production TM
rule - see docs/01-data-hygiene.md and pipelines/README.md for scope.
"""
import json

import pandas as pd

try:
    from ..scoring import normalized_alert_score
except ImportError:  # Support running pipelines/run_pipeline.py as a script.
    from scoring import normalized_alert_score

# Illustrative internal scenario threshold used only for synthetic testing.
# This is not a statutory Swedish threshold for reporting.
SCENARIO_AMOUNT_THRESHOLD = 10000
MIN_DEPOSITS = 3
WINDOW_HOURS = 72
NEAR_THRESHOLD_RATIO = 0.8

RESULT_COLUMNS = [
    "entity_id",
    "detector",
    "reason",
    "score",
    "raw_score",
    "window_start",
    "window_end",
    "transaction_ids",
    "feature_values",
]


def detect(transactions: pd.DataFrame) -> pd.DataFrame:
    df = transactions.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    if "transaction_id" not in df.columns:
        df["transaction_id"] = [f"ROW_{i}" for i in range(len(df))]
    if "channel" in df.columns:
        df = df[df["channel"] == "cash_deposit"]

    near_threshold = df[
        (df["amount"] >= SCENARIO_AMOUNT_THRESHOLD * NEAR_THRESHOLD_RATIO)
        & (df["amount"] < SCENARIO_AMOUNT_THRESHOLD)
    ].sort_values("timestamp")

    flags = []
    for entity_id, group in near_threshold.groupby("receiver_id"):
        group = group.sort_values("timestamp").reset_index(drop=True)
        window_start_idx = 0
        for i in range(len(group)):
            while (group.loc[i, "timestamp"] - group.loc[window_start_idx, "timestamp"]).total_seconds() > WINDOW_HOURS * 3600:
                window_start_idx += 1
            window = group.loc[window_start_idx:i]
            total_amount = window["amount"].sum()
            if len(window) >= MIN_DEPOSITS and total_amount >= SCENARIO_AMOUNT_THRESHOLD:
                raw_score = total_amount / SCENARIO_AMOUNT_THRESHOLD
                deposit_excess = (len(window) - MIN_DEPOSITS) / MIN_DEPOSITS
                amount_excess = raw_score - 1
                flags.append({
                    "entity_id": entity_id,
                    "detector": "structuring",
                    "reason": (
                        f"{len(window)} cash deposits near an illustrative internal "
                        f"scenario threshold of {SCENARIO_AMOUNT_THRESHOLD:.0f} SEK "
                        f"within {WINDOW_HOURS}h, summing to {total_amount:.0f} SEK"
                    ),
                    "score": normalized_alert_score(deposit_excess, amount_excess),
                    "raw_score": round(raw_score, 2),
                    "window_start": window["timestamp"].min(),
                    "window_end": window["timestamp"].max(),
                    "transaction_ids": json.dumps(
                        window["transaction_id"].astype(str).tolist()
                    ),
                    "feature_values": json.dumps({
                        "cash_deposit_count": len(window),
                        "total_amount": round(float(total_amount), 2),
                    }),
                })
                break
    return pd.DataFrame(flags, columns=RESULT_COLUMNS).drop_duplicates(
        subset=["entity_id", "detector"]
    )
