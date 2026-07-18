import json

from pipelines.detectors import pass_through


def two_rounds(make_transactions):
    return make_transactions(
        {
            "transaction_id": "IN_1",
            "sender_id": "UP_1",
            "receiver_id": "ENTITY",
            "amount": 20000,
            "timestamp": "2026-01-01 00:00:00",
        },
        {
            "transaction_id": "OUT_1",
            "sender_id": "ENTITY",
            "receiver_id": "DOWN_1",
            "amount": 19000,
            "timestamp": "2026-01-01 05:00:00",
        },
        {
            "transaction_id": "IN_2",
            "sender_id": "UP_2",
            "receiver_id": "ENTITY",
            "amount": 30000,
            "timestamp": "2026-01-03 00:00:00",
        },
        {
            "transaction_id": "OUT_2",
            "sender_id": "ENTITY",
            "receiver_id": "DOWN_2",
            "amount": 28500,
            "timestamp": "2026-01-03 07:00:00",
        },
    )


def test_two_separate_rounds_are_flagged(make_transactions):
    flags = pass_through.detect(two_rounds(make_transactions))

    assert flags["entity_id"].tolist() == ["ENTITY"]
    assert flags.iloc[0]["raw_score"] == 2


def test_one_round_is_not_flagged(make_transactions):
    transactions = two_rounds(make_transactions).iloc[:2].copy()

    assert pass_through.detect(transactions).empty


def test_outgoing_before_incoming_is_ignored(make_transactions):
    transactions = make_transactions(
        {
            "transaction_id": "OUT_1",
            "sender_id": "ENTITY",
            "receiver_id": "DOWN_1",
            "amount": 9000,
            "timestamp": "2026-01-01 00:00:00",
        },
        {
            "transaction_id": "IN_1",
            "sender_id": "UP_1",
            "receiver_id": "ENTITY",
            "amount": 10000,
            "timestamp": "2026-01-01 01:00:00",
        },
        {
            "transaction_id": "OUT_2",
            "sender_id": "ENTITY",
            "receiver_id": "DOWN_2",
            "amount": 9000,
            "timestamp": "2026-01-03 00:00:00",
        },
        {
            "transaction_id": "IN_2",
            "sender_id": "UP_2",
            "receiver_id": "ENTITY",
            "amount": 10000,
            "timestamp": "2026-01-03 01:00:00",
        },
    )

    assert pass_through.detect(transactions).empty


def test_outgoing_transaction_cannot_be_reused(make_transactions):
    transactions = make_transactions(
        {
            "transaction_id": "IN_1",
            "sender_id": "UP_1",
            "receiver_id": "ENTITY",
            "amount": 10000,
            "timestamp": "2026-01-01 00:00:00",
        },
        {
            "transaction_id": "IN_2",
            "sender_id": "UP_2",
            "receiver_id": "ENTITY",
            "amount": 10000,
            "timestamp": "2026-01-01 01:00:00",
        },
        {
            "transaction_id": "OUT_1",
            "sender_id": "ENTITY",
            "receiver_id": "DOWN",
            "amount": 9000,
            "timestamp": "2026-01-01 02:00:00",
        },
    )

    assert pass_through.detect(transactions).empty


def test_outgoing_over_maximum_ratio_is_rejected(make_transactions):
    transactions = make_transactions(
        {
            "transaction_id": "IN_1",
            "sender_id": "UP_1",
            "receiver_id": "ENTITY",
            "amount": 10000,
            "timestamp": "2026-01-01 00:00:00",
        },
        {
            "transaction_id": "OUT_1",
            "sender_id": "ENTITY",
            "receiver_id": "DOWN_1",
            "amount": 12000,
            "timestamp": "2026-01-01 01:00:00",
        },
        {
            "transaction_id": "IN_2",
            "sender_id": "UP_2",
            "receiver_id": "ENTITY",
            "amount": 10000,
            "timestamp": "2026-01-03 00:00:00",
        },
        {
            "transaction_id": "OUT_2",
            "sender_id": "ENTITY",
            "receiver_id": "DOWN_2",
            "amount": 12000,
            "timestamp": "2026-01-03 01:00:00",
        },
    )

    assert pass_through.detect(transactions).empty


def test_multiple_smaller_outgoing_transactions_can_match(make_transactions):
    transactions = make_transactions(
        {
            "transaction_id": "IN_1",
            "sender_id": "UP_1",
            "receiver_id": "ENTITY",
            "amount": 20000,
            "timestamp": "2026-01-01 00:00:00",
        },
        {
            "transaction_id": "OUT_1A",
            "sender_id": "ENTITY",
            "receiver_id": "DOWN_1",
            "amount": 5000,
            "timestamp": "2026-01-01 01:00:00",
        },
        {
            "transaction_id": "OUT_1B",
            "sender_id": "ENTITY",
            "receiver_id": "DOWN_1",
            "amount": 6000,
            "timestamp": "2026-01-01 02:00:00",
        },
        {
            "transaction_id": "OUT_1C",
            "sender_id": "ENTITY",
            "receiver_id": "DOWN_1",
            "amount": 7000,
            "timestamp": "2026-01-01 03:00:00",
        },
        {
            "transaction_id": "IN_2",
            "sender_id": "UP_2",
            "receiver_id": "ENTITY",
            "amount": 30000,
            "timestamp": "2026-01-03 00:00:00",
        },
        {
            "transaction_id": "OUT_2A",
            "sender_id": "ENTITY",
            "receiver_id": "DOWN_2",
            "amount": 14000,
            "timestamp": "2026-01-03 01:00:00",
        },
        {
            "transaction_id": "OUT_2B",
            "sender_id": "ENTITY",
            "receiver_id": "DOWN_2",
            "amount": 13000,
            "timestamp": "2026-01-03 02:00:00",
        },
    )

    flags = pass_through.detect(transactions)
    evidence = json.loads(flags.iloc[0]["transaction_ids"])

    assert flags["entity_id"].tolist() == ["ENTITY"]
    assert {"OUT_1A", "OUT_1B", "OUT_1C", "OUT_2A", "OUT_2B"} <= set(evidence)


def test_legitimate_normal_activity_is_not_flagged(make_transactions):
    transactions = make_transactions(
        {
            "sender_id": "UP_1",
            "receiver_id": "ENTITY",
            "amount": 20000,
            "timestamp": "2026-01-01 00:00:00",
        },
        {
            "sender_id": "ENTITY",
            "receiver_id": "BILLER",
            "amount": 4000,
            "timestamp": "2026-01-01 05:00:00",
        },
        {
            "sender_id": "UP_2",
            "receiver_id": "ENTITY",
            "amount": 30000,
            "timestamp": "2026-01-03 00:00:00",
        },
        {
            "sender_id": "ENTITY",
            "receiver_id": "SAVINGS",
            "amount": 5000,
            "timestamp": "2026-01-03 06:00:00",
        },
    )

    assert pass_through.detect(transactions).empty


def test_card_spending_is_not_counted_as_forwarding(make_transactions):
    transactions = two_rounds(make_transactions)
    transactions.loc[
        transactions["transaction_id"].str.startswith("OUT"),
        "channel",
    ] = "card"

    assert pass_through.detect(transactions).empty


def test_result_contains_traceable_evidence(make_transactions):
    flags = pass_through.detect(two_rounds(make_transactions))
    result = flags.iloc[0]
    transaction_ids = json.loads(result["transaction_ids"])
    features = json.loads(result["feature_values"])

    assert {
        "entity_id",
        "detector",
        "reason",
        "score",
        "raw_score",
        "window_start",
        "window_end",
        "transaction_ids",
        "feature_values",
    } <= set(flags.columns)
    assert transaction_ids == ["IN_1", "OUT_1", "IN_2", "OUT_2"]
    assert features["matched_rounds"] == 2
    assert features["average_forward_ratio"] == 0.95


def test_score_is_always_between_60_and_100(make_transactions):
    flags = pass_through.detect(two_rounds(make_transactions))

    assert flags["score"].between(60, 100).all()


def test_missing_transaction_ids_receive_stable_row_ids(make_transactions):
    transactions = two_rounds(make_transactions).drop(
        columns=["transaction_id"]
    )
    flags = pass_through.detect(transactions)
    transaction_ids = json.loads(flags.iloc[0]["transaction_ids"])

    assert transaction_ids == ["ROW_0", "ROW_1", "ROW_2", "ROW_3"]
