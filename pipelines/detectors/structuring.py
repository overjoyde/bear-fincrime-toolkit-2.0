"""Structuring / smurfing detector.

Flags entities receiving several deposits that individually sit just under
a reporting threshold, clustered in a short time window, summing well above
the threshold. This is a simple, explainable heuristic - not a production
TM rule - see docs/01-data-hygiene.md and pipelines/README.md for scope.
"""
import pandas as pd

THRESHOLD = 10000
MIN_DEPOSITS = 3
WINDOW_HOURS = 72
NEAR_THRESHOLD_RATIO = 0.8


def detect(transactions: pd.DataFrame) -> pd.DataFrame:
    df = transactions.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    near_threshold = df[
        (df["amount"] >= THRESHOLD * NEAR_THRESHOLD_RATIO)
        & (df["amount"] < THRESHOLD)
    ].sort_values("timestamp")

    flags = []
    for entity_id, group in near_threshold.groupby("receiver_id"):
        group = group.sort_values("timestamp").reset_index(drop=True)
        window_start_idx = 0
        for i in range(len(group)):
            while (group.loc[i, "timestamp"] - group.loc[window_start_idx, "timestamp"]).total_seconds() > WINDOW_HOURS * 3600:
                window_start_idx += 1
            window = group.loc[window_start_idx:i]
            if len(window) >= MIN_DEPOSITS and window["amount"].sum() >= THRESHOLD:
                flags.append({
                    "entity_id": entity_id,
                    "detector": "structuring",
                    "reason": (
                        f"{len(window)} deposits of {THRESHOLD * NEAR_THRESHOLD_RATIO:.0f}-"
                        f"{THRESHOLD:.0f} SEK within {WINDOW_HOURS}h, summing to "
                        f"{window['amount'].sum():.0f} SEK"
                    ),
                    "score": round(window["amount"].sum() / THRESHOLD, 2),
                })
                break
    return pd.DataFrame(flags).drop_duplicates(subset=["entity_id", "detector"])
