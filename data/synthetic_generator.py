#!/usr/bin/env python3
"""Synthetic transaction generator with injected AML typologies and ground truth.

Every name, account, and amount here is fabricated by this script. Nothing
in its output is derived from, or resembles, any real person or institution.
Use this to test the profiles/prompts/skills/pipelines in this repo without
ever touching real data - see docs/01-data-hygiene.md for why that matters.
"""
import argparse
import csv
import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

CURRENCY = "SEK"

FIRST_NAMES = [
    "Anna", "Erik", "Lina", "Karl", "Sofia", "Filip", "Maja", "Oskar", "Elin",
    "Viktor", "Freja", "Axel", "Ida", "Leo", "Nora", "Hugo", "Alma", "Emil",
    "Wilma", "Anton",
]
LAST_NAMES = [
    "Andersson", "Johansson", "Karlsson", "Nilsson", "Eriksson", "Larsson",
    "Olsson", "Persson", "Svensson", "Gustafsson", "Pettersson", "Jonsson",
    "Jansson", "Hansson", "Bengtsson",
]
BUSINESS_WORDS = ["Nordic", "Baltic", "Polar", "Fjord", "Skog", "Bro", "Sten", "Vind", "Sol", "Strom"]
BUSINESS_SUFFIX = ["AB", "Handel AB", "Konsult AB", "Trading AB", "Group AB", "Import AB"]


def make_customer(cid, rng, business_ratio=0.15):
    is_business = rng.random() < business_ratio
    if is_business:
        name = f"{rng.choice(BUSINESS_WORDS)} {rng.choice(BUSINESS_WORDS)} {rng.choice(BUSINESS_SUFFIX)}"
        ctype = "business"
        expected_monthly = rng.uniform(20000, 300000)
    else:
        name = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
        ctype = "retail"
        expected_monthly = rng.uniform(3000, 45000)
    return {
        "customer_id": f"C{cid:05d}",
        "name": name,
        "customer_type": ctype,
        "expected_monthly_volume": round(expected_monthly, 2),
        "onboarding_days_ago": rng.randint(30, 2000),
    }


def random_timestamp(start, days, rng):
    offset_seconds = rng.uniform(0, days * 86400)
    return start + timedelta(seconds=offset_seconds)


def gen_baseline(customers, start, days, rng, monthly_tx_per_customer=3, random_counterparty_rate=0.15):
    """Ordinary transfers. Real customers mostly pay the same small set of
    regular counterparties (employer, family, common billers) rather than a
    new random one every time - modeling that matters for community
    detection, since a graph where everyone transacts with everyone looks
    like one giant cluster and hides any real one."""
    txs = []
    n_months = max(days / 30.0, 1)
    ids = [c["customer_id"] for c in customers]
    regulars = {
        c["customer_id"]: rng.sample([i for i in ids if i != c["customer_id"]], min(rng.randint(2, 5), len(ids) - 1))
        for c in customers
    }
    for c in customers:
        n_tx = max(1, int(rng.gauss(monthly_tx_per_customer * n_months, 1.5)))
        per_tx_mean = c["expected_monthly_volume"] * n_months / n_tx
        for _ in range(n_tx):
            if rng.random() < random_counterparty_rate:
                counterparty = rng.choice([i for i in ids if i != c["customer_id"]])
            else:
                counterparty = rng.choice(regulars[c["customer_id"]])
            amount = max(50, rng.gauss(per_tx_mean, per_tx_mean * 0.4))
            txs.append({
                "sender_id": c["customer_id"],
                "receiver_id": counterparty,
                "amount": round(amount, 2),
                "currency": CURRENCY,
                "timestamp": random_timestamp(start, days, rng),
                "channel": rng.choice(["transfer", "card", "transfer", "transfer"]),
            })
    return txs


def inject_structuring(customers, start, days, rng, n_cases=6, threshold=10000):
    txs, ground_truth = [], []
    retail = [c for c in customers if c["customer_type"] == "retail"]
    subjects = rng.sample(retail, min(n_cases, len(retail)))
    for cust in subjects:
        window_start = random_timestamp(start, max(days - 5, 1), rng)
        n_deposits = rng.randint(4, 8)
        for i in range(n_deposits):
            amount = rng.uniform(threshold * 0.85, threshold * 0.98)
            txs.append({
                "sender_id": "CASH",
                "receiver_id": cust["customer_id"],
                "amount": round(amount, 2),
                "currency": CURRENCY,
                "timestamp": window_start + timedelta(hours=rng.uniform(0, 60)),
                "channel": "cash_deposit",
            })
        ground_truth.append({"entity_id": cust["customer_id"], "typology": "structuring", "role": "structurer"})
    return txs, ground_truth


def inject_fan_in_fan_out(customers, start, days, rng, n_cases=4, fan_in_size=12):
    txs, ground_truth = [], []
    pool = customers[:]
    for _ in range(n_cases):
        mule = rng.choice(pool)
        senders = rng.sample([c for c in pool if c["customer_id"] != mule["customer_id"]], fan_in_size)
        receivers = rng.sample([c for c in pool if c["customer_id"] != mule["customer_id"]], rng.randint(1, 2))
        window_start = random_timestamp(start, max(days - 3, 1), rng)
        total_in = 0.0
        for sender in senders:
            amount = rng.uniform(1500, 6000)
            total_in += amount
            txs.append({
                "sender_id": sender["customer_id"],
                "receiver_id": mule["customer_id"],
                "amount": round(amount, 2),
                "currency": CURRENCY,
                "timestamp": window_start + timedelta(hours=rng.uniform(0, 36)),
                "channel": "transfer",
            })
            ground_truth.append({"entity_id": sender["customer_id"], "typology": "fan_in_out", "role": "fan_in_sender"})
        remaining = total_in * rng.uniform(0.85, 0.97)
        for receiver in receivers:
            share = remaining / len(receivers)
            txs.append({
                "sender_id": mule["customer_id"],
                "receiver_id": receiver["customer_id"],
                "amount": round(share, 2),
                "currency": CURRENCY,
                "timestamp": window_start + timedelta(hours=rng.uniform(36, 60)),
                "channel": "transfer",
            })
        ground_truth.append({"entity_id": mule["customer_id"], "typology": "fan_in_out", "role": "mule"})
    return txs, ground_truth


def inject_pass_through(customers, start, days, rng, n_cases=4):
    txs, ground_truth = [], []
    pool = customers[:]
    for _ in range(n_cases):
        conduit = rng.choice(pool)
        upstream = rng.choice([c for c in pool if c["customer_id"] != conduit["customer_id"]])
        downstream = rng.choice([c for c in pool if c["customer_id"] not in (conduit["customer_id"], upstream["customer_id"])])
        rounds = rng.randint(3, 6)
        for _ in range(rounds):
            t_in = random_timestamp(start, max(days - 2, 1), rng)
            amount = rng.uniform(15000, 120000)
            txs.append({
                "sender_id": upstream["customer_id"],
                "receiver_id": conduit["customer_id"],
                "amount": round(amount, 2),
                "currency": CURRENCY,
                "timestamp": t_in,
                "channel": "transfer",
            })
            forwarded = amount * rng.uniform(0.9, 0.99)
            txs.append({
                "sender_id": conduit["customer_id"],
                "receiver_id": downstream["customer_id"],
                "amount": round(forwarded, 2),
                "currency": CURRENCY,
                "timestamp": t_in + timedelta(hours=rng.uniform(1, 20)),
                "channel": "transfer",
            })
        ground_truth.append({"entity_id": conduit["customer_id"], "typology": "pass_through", "role": "conduit"})
    return txs, ground_truth


def inject_community_ring(customers, start, days, rng, n_rings=3, ring_size=7):
    """A small tightly-connected cluster of retail accounts transacts mostly
    among themselves, at amounts well above their normal baseline activity -
    a pattern that can look unremarkable transaction-by-transaction but
    stands out as a dense, disjoint cluster at the network level. Restricted
    to retail customers and disjoint across rings so the injected signal
    is not swamped by an overlapping ring or a business account's unrelated
    high-volume baseline traffic."""
    txs, ground_truth = [], []
    retail = [c for c in customers if c["customer_type"] == "retail"]
    used_ids = set()
    for _ in range(n_rings):
        available = [c for c in retail if c["customer_id"] not in used_ids]
        if len(available) < ring_size:
            break
        ring = rng.sample(available, ring_size)
        ring_ids = [c["customer_id"] for c in ring]
        used_ids.update(ring_ids)
        n_internal_tx = ring_size * rng.randint(10, 16)
        for _ in range(n_internal_tx):
            sender, receiver = rng.sample(ring_ids, 2)
            amount = rng.uniform(15000, 50000)
            txs.append({
                "sender_id": sender,
                "receiver_id": receiver,
                "amount": round(amount, 2),
                "currency": CURRENCY,
                "timestamp": random_timestamp(start, days, rng),
                "channel": "transfer",
            })
        for cid in ring_ids:
            ground_truth.append({"entity_id": cid, "typology": "community_ring", "role": "ring_member"})
    return txs, ground_truth


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_sqlite(db_path, customers, transactions):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()
    conn = sqlite3.connect(db_path)
    conn.execute("""CREATE TABLE customers (
        customer_id TEXT PRIMARY KEY, name TEXT, customer_type TEXT,
        expected_monthly_volume REAL, onboarding_days_ago INTEGER)""")
    conn.executemany(
        "INSERT INTO customers VALUES (:customer_id, :name, :customer_type, "
        ":expected_monthly_volume, :onboarding_days_ago)", customers)
    conn.execute("""CREATE TABLE transactions (
        transaction_id TEXT PRIMARY KEY, sender_id TEXT, receiver_id TEXT,
        amount REAL, currency TEXT, timestamp TEXT, channel TEXT)""")
    conn.executemany(
        "INSERT INTO transactions VALUES (:transaction_id, :sender_id, "
        ":receiver_id, :amount, :currency, :timestamp, :channel)", transactions)
    conn.commit()
    conn.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--customers", type=int, default=300, help="number of customers to generate")
    parser.add_argument("--months", type=float, default=6, help="period length in months")
    parser.add_argument("--out", type=Path, default=Path("generated"), help="output directory")
    parser.add_argument("--seed", type=int, default=42, help="random seed, for reproducible output")
    parser.add_argument("--sqlite", action="store_true", help="also write a SQLite database")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    days = int(args.months * 30)
    start = datetime(2026, 1, 1)

    customers = [make_customer(i, rng) for i in range(1, args.customers + 1)]

    all_txs = gen_baseline(customers, start, days, rng)
    ground_truth = []
    for injector in (inject_structuring, inject_fan_in_fan_out, inject_pass_through, inject_community_ring):
        txs, gt = injector(customers, start, days, rng)
        all_txs.extend(txs)
        ground_truth.extend(gt)

    all_txs.sort(key=lambda t: t["timestamp"])
    for i, tx in enumerate(all_txs, start=1):
        tx["transaction_id"] = f"T{i:07d}"
        tx["timestamp"] = tx["timestamp"].isoformat(sep=" ", timespec="seconds")

    tx_fields = ["transaction_id", "sender_id", "receiver_id", "amount", "currency", "timestamp", "channel"]
    cust_fields = ["customer_id", "name", "customer_type", "expected_monthly_volume", "onboarding_days_ago"]
    gt_fields = ["entity_id", "typology", "role"]

    write_csv(args.out / "transactions.csv", all_txs, tx_fields)
    write_csv(args.out / "customers.csv", customers, cust_fields)
    write_csv(args.out / "ground_truth.csv", ground_truth, gt_fields)

    if args.sqlite:
        write_sqlite(args.out / "synthetic.db", customers, all_txs)

    print(f"Wrote {len(customers)} customers, {len(all_txs)} transactions, "
          f"{len(ground_truth)} ground-truth entity labels to {args.out}/")


if __name__ == "__main__":
    main()
