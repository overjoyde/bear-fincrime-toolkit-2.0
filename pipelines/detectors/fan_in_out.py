"""Fan-in / fan-out (mule account) detector.

Flags entities that receive from many distinct counterparties in a short
window and then forward most of the total out again shortly after - the
classic mule-account pattern. Heuristic and explainable, not a production
TM rule - see pipelines/README.md for scope.
"""
import pandas as pd

WINDOW_HOURS = 72
MIN_DISTINCT_SENDERS = 6
MIN_PASS_THROUGH_RATIO = 0.7


def detect(transactions: pd.DataFrame) -> pd.DataFrame:
    df = transactions.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    window = pd.Timedelta(hours=WINDOW_HOURS)

    flags = []
    entities = pd.unique(df[["sender_id", "receiver_id"]].values.ravel())
    for entity_id in entities:
        incoming = df[df["receiver_id"] == entity_id].sort_values("timestamp")
        outgoing = df[df["sender_id"] == entity_id].sort_values("timestamp")
        if incoming.empty or outgoing.empty:
            continue
        for _, first_in in incoming.iterrows():
            window_end = first_in["timestamp"] + window
            in_window = incoming[
                (incoming["timestamp"] >= first_in["timestamp"])
                & (incoming["timestamp"] <= window_end)
            ]
            distinct_senders = in_window["sender_id"].nunique()
            if distinct_senders < MIN_DISTINCT_SENDERS:
                continue
            total_in = in_window["amount"].sum()
            out_window = outgoing[
                (outgoing["timestamp"] >= first_in["timestamp"])
                & (outgoing["timestamp"] <= window_end + window)
            ]
            total_out = out_window["amount"].sum()
            if total_in > 0 and (total_out / total_in) >= MIN_PASS_THROUGH_RATIO:
                flags.append({
                    "entity_id": entity_id,
                    "detector": "fan_in_out",
                    "reason": (
                        f"received from {distinct_senders} distinct senders within "
                        f"{WINDOW_HOURS}h ({total_in:.0f} SEK), then forwarded "
                        f"{total_out / total_in:.0%} of it onward"
                    ),
                    "score": round(total_out / total_in, 2),
                })
                break
    return pd.DataFrame(flags).drop_duplicates(subset=["entity_id", "detector"])
