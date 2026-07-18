from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def make_transactions():
    def build(*rows):
        records = []
        for index, row in enumerate(rows):
            record = {
                "transaction_id": f"T{index + 1}",
                "sender_id": f"S{index + 1}",
                "receiver_id": f"R{index + 1}",
                "amount": 100.0,
                "timestamp": f"2026-01-01 {index:02d}:00:00",
                "channel": "transfer",
            }
            record.update(row)
            records.append(record)
        return pd.DataFrame(records)

    return build
