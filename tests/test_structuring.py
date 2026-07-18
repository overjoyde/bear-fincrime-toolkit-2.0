import re
from datetime import datetime, timedelta

from pipelines.detectors import structuring

from conftest import PROJECT_ROOT


def cash_deposits(make_transactions, channel="cash_deposit", spacing_hours=12):
    start = datetime(2026, 1, 1)
    return make_transactions(*[
        {
            "transaction_id": f"CASH_{index}",
            "sender_id": "CASH",
            "receiver_id": "CUSTOMER",
            "amount": 9000,
            "timestamp": start + timedelta(hours=index * spacing_hours),
            "channel": channel,
        }
        for index in range(4)
    ])


def test_near_threshold_cash_deposits_are_flagged(make_transactions):
    flags = structuring.detect(cash_deposits(make_transactions))

    assert flags["entity_id"].tolist() == ["CUSTOMER"]
    assert flags.iloc[0]["detector"] == "structuring"
    assert 60 <= flags.iloc[0]["score"] <= 100


def test_transfers_are_not_treated_as_cash_structuring(make_transactions):
    flags = structuring.detect(
        cash_deposits(make_transactions, channel="transfer")
    )

    assert flags.empty


def test_deposits_outside_window_are_not_flagged(make_transactions):
    flags = structuring.detect(
        cash_deposits(make_transactions, spacing_hours=73)
    )

    assert flags.empty


def test_repository_avoids_statutory_limit_wording():
    forbidden = (
        "reporting " + "threshold",
        "reporting-" + "threshold",
        "10,000 SEK " + "reporting",
    )
    pattern = re.compile("|".join(map(re.escape, forbidden)), re.IGNORECASE)
    matches = []

    for path in PROJECT_ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".py", ".md", ".yml", ".yaml", ".json"}:
            continue
        text = path.read_text(encoding="utf-8")
        if pattern.search(text):
            matches.append(path.relative_to(PROJECT_ROOT))

    assert matches == []
