"""Network community detector.

Builds a transaction graph and flags tightly-connected clusters where
member accounts transact mostly among themselves - a pattern that can look
unremarkable transaction-by-transaction but stands out at the network
level. Uses Louvain community detection (networkx's built-in implementation).
Heuristic and explainable, not a production TM rule - see pipelines/README.md
for scope.
"""
import networkx as nx
import pandas as pd

try:
    from ..scoring import normalized_alert_score
except ImportError:  # Support running pipelines/run_pipeline.py as a script.
    from scoring import normalized_alert_score

MIN_COMMUNITY_SIZE = 4
MAX_COMMUNITY_SIZE = 25
MIN_INTERNAL_DENSITY = 0.35
MIN_INTERNAL_VOLUME_SHARE = 0.6

RESULT_COLUMNS = ["entity_id", "detector", "reason", "score", "raw_score"]


def _build_graph(transactions: pd.DataFrame) -> nx.Graph:
    graph = nx.Graph()
    for _, tx in transactions.iterrows():
        u, v, amount = tx["sender_id"], tx["receiver_id"], tx["amount"]
        if graph.has_edge(u, v):
            graph[u][v]["weight"] += amount
            graph[u][v]["count"] += 1
        else:
            graph.add_edge(u, v, weight=amount, count=1)
    return graph


def detect(transactions: pd.DataFrame) -> pd.DataFrame:
    df = transactions[transactions["sender_id"] != "CASH"]
    graph = _build_graph(df)
    if graph.number_of_nodes() < MIN_COMMUNITY_SIZE:
        return pd.DataFrame(columns=RESULT_COLUMNS)

    communities = nx.algorithms.community.louvain_communities(graph, weight="weight", seed=42)

    flags = []
    for community in communities:
        size = len(community)
        if not (MIN_COMMUNITY_SIZE <= size <= MAX_COMMUNITY_SIZE):
            continue

        subgraph = graph.subgraph(community)
        internal_edges = subgraph.number_of_edges()
        possible_edges = size * (size - 1) / 2
        density = internal_edges / possible_edges if possible_edges > 0 else 0

        internal_volume = sum(d["weight"] for _, _, d in subgraph.edges(data=True))
        external_volume = 0.0
        for node in community:
            for neighbor in graph.neighbors(node):
                if neighbor not in community:
                    external_volume += graph[node][neighbor]["weight"]
        total_volume = internal_volume + external_volume
        internal_share = internal_volume / total_volume if total_volume > 0 else 0

        if density >= MIN_INTERNAL_DENSITY and internal_share >= MIN_INTERNAL_VOLUME_SHARE:
            density_excess = (
                density - MIN_INTERNAL_DENSITY
            ) / (1 - MIN_INTERNAL_DENSITY)
            volume_share_excess = (
                internal_share - MIN_INTERNAL_VOLUME_SHARE
            ) / (1 - MIN_INTERNAL_VOLUME_SHARE)
            for entity_id in community:
                flags.append({
                    "entity_id": entity_id,
                    "detector": "community_ring",
                    "reason": (
                        f"member of a {size}-account cluster with {density:.0%} internal "
                        f"connection density and {internal_share:.0%} of volume staying "
                        f"inside the cluster"
                    ),
                    "score": normalized_alert_score(
                        density_excess, volume_share_excess
                    ),
                    "raw_score": round(density * internal_share, 2),
                })
    return pd.DataFrame(flags, columns=RESULT_COLUMNS).drop_duplicates(
        subset=["entity_id", "detector"]
    )
