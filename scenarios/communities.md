# Scenario: Network Communities (Rings)

## Status
Implemented - `pipelines/detectors/communities.py`

## Description
A tightly-connected cluster of accounts that mostly transact among
themselves. No single transaction in the cluster necessarily looks
unusual — the pattern only becomes visible at the network level, when a
group of accounts forms a dense, largely closed loop of value that rarely
flows to or from outside entities.

## Red flags / indicators
- A cluster of 4 to 25 accounts (very small or very large groups are
  excluded — too small to be a meaningful ring, too large to plausibly
  be a single coordinated group).
- At least 35% of all possible internal connections between cluster
  members actually present (internal density).
- At least 60% of the cluster's total transaction volume staying inside
  the cluster rather than flowing to outside accounts.

## Detection approach
Implemented in `pipelines/detectors/communities.py`. Builds a weighted
transaction graph (cash-only senders excluded) and runs Louvain community
detection (`networkx`'s built-in implementation, fixed seed 42). A
community is flagged when its size is between `MIN_COMMUNITY_SIZE` (4) and
`MAX_COMMUNITY_SIZE` (25), its internal density is at least
`MIN_INTERNAL_DENSITY` (0.35), and its internal volume share is at least
`MIN_INTERNAL_VOLUME_SHARE` (0.6). The alert-prioritization score (60–100,
see `pipelines/README.md`) is derived from how far density and internal
volume share exceed those minimums. Unlike the other three detectors, this
one has **no evaluation floor configured** in `evaluation/thresholds.json`
— it's measured by `evaluation/evaluate.py` but not treated as a blocking
CI regression check, because of known stability limitations in
community-detection results (see `evaluation/README.md`).

AMLTRIX equivalent: No direct AMLTRIX equivalent found. AMLTRIX's technique
catalog (304 techniques as of this writing, from
https://github.com/Amlyze/amltrix-data) was searched by name for
"network", "community", and "ring" with no match — network-graph
clustering is an analytical detection *method*, not itself a criminal
*technique*, which is what AMLTRIX catalogs.

## Sources
- `pipelines/detectors/communities.py`
- `evaluation/thresholds.json`
- `evaluation/README.md`
