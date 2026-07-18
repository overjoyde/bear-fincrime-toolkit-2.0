"""Pass-through (rapid movement) detector.

Flags entities that repeatedly receive a large sum and forward nearly all
of it within a short window - little to no funds retained, suggesting a
conduit rather than a genuine counterparty. Heuristic and explainable, not
a production TM rule - see pipelines/README.md for scope.
"""
import json

import pandas as pd

try:
    from ..scoring import normalized_alert_score
except ImportError:  # Support running pipelines/run_pipeline.py as a script.
    from scoring import normalized_alert_score

MAX_HOURS_BETWEEN = 24
MIN_FORWARD_RATIO = 0.85
MAX_FORWARD_RATIO = 1.10
MIN_ROUNDS = 2
MIN_AMOUNT = 10000

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
    else:
        missing_ids = df["transaction_id"].isna()
        for row_index in df.index[missing_ids]:
            df.at[row_index, "transaction_id"] = f"ROW_{row_index}"
    df["transaction_id"] = df["transaction_id"].astype(str)
    movement_df = df
    if "channel" in df.columns:
        movement_df = df[df["channel"] == "transfer"]

    flags = []
    entities = pd.unique(
        movement_df[["sender_id", "receiver_id"]].values.ravel()
    )
    for entity_id in entities:
        if pd.isna(entity_id):
            continue
        incoming = movement_df[
            (movement_df["receiver_id"] == entity_id)
            & (movement_df["amount"] >= MIN_AMOUNT)
        ].sort_values(["timestamp", "transaction_id"])
        outgoing = movement_df[
            movement_df["sender_id"] == entity_id
        ].sort_values(
            ["timestamp", "transaction_id"]
        )
        if incoming.empty or outgoing.empty:
            continue

        used_outgoing_ids: set[str] = set()
        matched_rounds = []
        for _, incoming_tx in incoming.iterrows():
            candidates = outgoing[
                (outgoing["timestamp"] > incoming_tx["timestamp"])
                & (
                    outgoing["timestamp"]
                    <= incoming_tx["timestamp"]
                    + pd.Timedelta(hours=MAX_HOURS_BETWEEN)
                )
                & (~outgoing["transaction_id"].isin(used_outgoing_ids))
            ].sort_values(["timestamp", "transaction_id"])

            selected = []
            matched_amount = 0.0
            for _, outgoing_tx in candidates.iterrows():
                proposed_amount = matched_amount + float(outgoing_tx["amount"])
                if proposed_amount > float(incoming_tx["amount"]) * MAX_FORWARD_RATIO:
                    continue

                selected.append(outgoing_tx)
                matched_amount = proposed_amount
                if matched_amount >= float(incoming_tx["amount"]) * MIN_FORWARD_RATIO:
                    break

            ratio = matched_amount / float(incoming_tx["amount"])
            if MIN_FORWARD_RATIO <= ratio <= MAX_FORWARD_RATIO:
                outgoing_ids = [str(tx["transaction_id"]) for tx in selected]
                used_outgoing_ids.update(outgoing_ids)
                matched_rounds.append({
                    "incoming_id": str(incoming_tx["transaction_id"]),
                    "incoming_amount": float(incoming_tx["amount"]),
                    "incoming_timestamp": incoming_tx["timestamp"],
                    "outgoing_ids": outgoing_ids,
                    "matched_outgoing": matched_amount,
                    "ratio": ratio,
                    "completed_timestamp": selected[-1]["timestamp"],
                })

        if len(matched_rounds) >= MIN_ROUNDS:
            average_forward_ratio = (
                sum(r["ratio"] for r in matched_rounds) / len(matched_rounds)
            )
            total_incoming = sum(r["incoming_amount"] for r in matched_rounds)
            total_matched_outgoing = sum(
                r["matched_outgoing"] for r in matched_rounds
            )
            delays = [
                (
                    r["completed_timestamp"] - r["incoming_timestamp"]
                ).total_seconds() / 3600
                for r in matched_rounds
            ]
            median_delay_hours = float(pd.Series(delays).median())
            round_excess = (len(matched_rounds) - MIN_ROUNDS) / MIN_ROUNDS
            ratio_quality = 1 - (
                abs(1 - average_forward_ratio)
                / max(1 - MIN_FORWARD_RATIO, MAX_FORWARD_RATIO - 1)
            )
            transaction_ids = []
            for matched_round in matched_rounds:
                transaction_ids.append(matched_round["incoming_id"])
                transaction_ids.extend(matched_round["outgoing_ids"])
            feature_values = {
                "matched_rounds": len(matched_rounds),
                "average_forward_ratio": round(average_forward_ratio, 4),
                "median_delay_hours": round(median_delay_hours, 2),
                "total_incoming": round(total_incoming, 2),
                "total_matched_outgoing": round(total_matched_outgoing, 2),
            }
            flags.append({
                "entity_id": entity_id,
                "detector": "pass_through",
                "reason": (
                    f"{len(matched_rounds)} separate rounds forwarded an average of "
                    f"{average_forward_ratio:.0%} within {MAX_HOURS_BETWEEN}h"
                ),
                "score": normalized_alert_score(round_excess, ratio_quality),
                "raw_score": len(matched_rounds),
                "window_start": min(
                    r["incoming_timestamp"] for r in matched_rounds
                ),
                "window_end": max(
                    r["completed_timestamp"] for r in matched_rounds
                ),
                "transaction_ids": json.dumps(transaction_ids),
                "feature_values": json.dumps(feature_values),
            })
    return pd.DataFrame(flags, columns=RESULT_COLUMNS).drop_duplicates(
        subset=["entity_id", "detector"]
    )
