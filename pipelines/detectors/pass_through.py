"""Pass-through (rapid movement) detector.

Flags entities that repeatedly receive a large sum and forward nearly all
of it within a short window - little to no funds retained, suggesting a
conduit rather than a genuine counterparty. Heuristic and explainable, not
a production TM rule - see pipelines/README.md for scope.
"""
import pandas as pd

MAX_HOURS_BETWEEN = 24
MIN_FORWARD_RATIO = 0.85
MIN_ROUNDS = 2
MIN_AMOUNT = 10000


def detect(transactions: pd.DataFrame) -> pd.DataFrame:
    df = transactions.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    flags = []
    entities = pd.unique(df[["sender_id", "receiver_id"]].values.ravel())
    for entity_id in entities:
        incoming = df[
            (df["receiver_id"] == entity_id) & (df["amount"] >= MIN_AMOUNT)
        ].sort_values("timestamp")
        outgoing = df[df["sender_id"] == entity_id].sort_values("timestamp")
        if incoming.empty or outgoing.empty:
            continue

        rounds = 0
        details = []
        for _, in_tx in incoming.iterrows():
            candidates = outgoing[
                (outgoing["timestamp"] > in_tx["timestamp"])
                & (outgoing["timestamp"] <= in_tx["timestamp"] + pd.Timedelta(hours=MAX_HOURS_BETWEEN))
            ]
            if candidates.empty:
                continue
            forwarded = candidates["amount"].sum()
            ratio = forwarded / in_tx["amount"]
            if ratio >= MIN_FORWARD_RATIO:
                rounds += 1
                details.append(f"{in_tx['amount']:.0f} in -> {forwarded:.0f} out within {MAX_HOURS_BETWEEN}h")

        if rounds >= MIN_ROUNDS:
            flags.append({
                "entity_id": entity_id,
                "detector": "pass_through",
                "reason": f"{rounds} rounds of near-total pass-through; e.g. {details[0]}",
                "score": rounds,
            })
    return pd.DataFrame(flags).drop_duplicates(subset=["entity_id", "detector"])
