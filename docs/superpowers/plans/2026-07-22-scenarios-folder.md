# scenarios/ Folder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `scenarios/` folder to bear-fincrime-toolkit-2.0 with one structured typology write-up per existing detector (grounded in the real code) plus a new Funnel Accounts write-up sourced from the AMLTRIX framework, and reconcile `skills/typology-research/SKILL.md`'s now-stale "save outside the repo" guidance.

**Architecture:** Pure documentation change — six new markdown files under `scenarios/`, plus three small edits to existing files for cross-linking. No code, no tests, no detector-logic changes.

**Tech Stack:** Markdown only.

## Global Constraints

- Documentation-only: no changes to `pipelines/detectors/*.py`, `evaluation/thresholds.json`, `data/synthetic_generator.py`, or `run_pipeline.py` (per `docs/superpowers/specs/2026-07-22-scenarios-folder-design.md`, "Out of scope").
- Every implemented scenario doc's named constants and evaluation floor must exactly match the current values in `pipelines/detectors/*.py` and `evaluation/thresholds.json` — verified by grep in each task, not eyeballed.
- AMLTRIX content is used under the AMLTRIX License Terms (https://framework.amltrix.com/license) — CC-style, permits reproduction/modification/commercial use, requires attribution and must not imply AMLTRIX's endorsement. Every AMLTRIX-sourced doc/section links back to the source technique page and to the license.
- `structuring.md` and `fan-in-out.md` get a one-line AMLTRIX cross-reference each (T0016, T0011) — no deeper AMLTRIX research for these two beyond the ID/name/sub-technique names already confirmed.
- `pass-through.md` and `communities.md` explicitly state "No direct AMLTRIX equivalent found" (checked, not omitted) rather than lacking the section entirely.

---

### Task 1: `scenarios/README.md` — folder intro and shared template

**Files:**
- Create: `scenarios/README.md`

**Interfaces:**
- Produces: the template structure (`## Status`, `## Description`, `## Red flags / indicators`, `## Detection approach`, `## Sources`) that Tasks 2–6 fill in. No other task depends on code from this one — it's the spine document.

- [ ] **Step 1: Write `scenarios/README.md`**

````markdown
# Scenarios

Structured typology write-ups: one per detector implemented in
`pipelines/detectors/`, plus typologies not yet implemented but worth
tracking. Each file follows the same shape:

```
# Scenario: <Name>

## Status
Implemented - `pipelines/detectors/<file>.py` | Not yet implemented

## Description
Plain-language description of the pattern and why it's used to obscure
illicit funds.

## Red flags / indicators
Concrete, checkable list.

## Detection approach
- Implemented: the real triggering conditions, named threshold constants,
  time windows, and the score contract (see `pipelines/README.md`), plus
  the evaluation floor from `evaluation/thresholds.json` (or "no floor
  configured").
- Not yet implemented: what data/structural rule would be needed, against
  this repo's actual schema and the "Adding a new detector" recipe in
  `pipelines/README.md`.

## Sources
Named, linkable sources only.
```

For the four already-implemented typologies, every claim in "Detection
approach" is grounded in the actual code — not a generic textbook
description that happens not to match what's implemented. If a section
can't be grounded that way, it says so rather than guessing.

## AMLTRIX attribution

`funnel-accounts.md`, and the single AMLTRIX cross-reference lines in
`structuring.md` and `fan-in-out.md`, use content from
[AMLTRIX](https://framework.amltrix.com/) (© UAB "Amlyze"), used under the
[AMLTRIX License Terms](https://framework.amltrix.com/license). This is
attribution, not endorsement — AMLTRIX has not reviewed or approved this
repository's use of its content.

## Files

| File | Status |
|---|---|
| `structuring.md` | Implemented |
| `fan-in-out.md` | Implemented |
| `pass-through.md` | Implemented |
| `communities.md` | Implemented |
| `funnel-accounts.md` | Not yet implemented |
````

- [ ] **Step 2: Commit**

```bash
git add scenarios/README.md
git commit -m "docs: add scenarios/ folder template and index"
```

---

### Task 2: `scenarios/structuring.md`

**Files:**
- Create: `scenarios/structuring.md`

**Interfaces:**
- Consumes: template shape from Task 1 (informational only, no code dependency).

- [ ] **Step 1: Verify the source constants before writing the doc**

Run:
```bash
grep -n "SCENARIO_AMOUNT_THRESHOLD\|MIN_DEPOSITS\|WINDOW_HOURS\|NEAR_THRESHOLD_RATIO" pipelines/detectors/structuring.py
```
Expected output (values the doc below must match):
```
19:SCENARIO_AMOUNT_THRESHOLD = 10000
20:MIN_DEPOSITS = 3
21:WINDOW_HOURS = 72
22:NEAR_THRESHOLD_RATIO = 0.8
```
And:
```bash
python -c "import json; print(json.load(open('evaluation/thresholds.json'))['structuring'])"
```
Expected output: `{'minimum_precision': 0.8, 'minimum_recall': 0.8}`

- [ ] **Step 2: Write `scenarios/structuring.md`**

```markdown
# Scenario: Structuring / Smurfing

## Status
Implemented - `pipelines/detectors/structuring.py`

## Description
Breaking a larger sum of illicit cash into multiple smaller deposits, each
individually below a reporting or scrutiny threshold, so no single deposit
draws attention on its own. The deposits are usually clustered in a short
time window and, taken together, sum to a materially larger amount than
any one of them suggests.

## Red flags / indicators
- Multiple cash deposits to the same entity, each between 80% and 100% of
  an illustrative internal scenario threshold (10,000 SEK in this repo's
  synthetic data — not a statutory reporting threshold).
- At least 3 such deposits landing within a 72-hour window.
- The deposits in that window summing to at least the full scenario
  threshold, even though none individually reaches it.
- Channel is cash deposit specifically (`channel == "cash_deposit"`), not
  transfers or other movement types.

## Detection approach
Implemented in `pipelines/detectors/structuring.py`. For each entity
receiving cash deposits, the detector slides a window over deposits priced
between `NEAR_THRESHOLD_RATIO` (0.8) and 1.0 of `SCENARIO_AMOUNT_THRESHOLD`
(10,000), and flags the entity once a window of at least `MIN_DEPOSITS` (3)
such deposits within `WINDOW_HOURS` (72) sums to at least
`SCENARIO_AMOUNT_THRESHOLD`. The alert-prioritization score (60–100, see
`pipelines/README.md`) is derived from how far the deposit count and total
amount exceed those minimums. The regression floor in
`evaluation/thresholds.json` is 0.80 minimum precision / 0.80 minimum
recall, checked by `evaluation/evaluate.py` and enforced as blocking in CI.

AMLTRIX equivalent: [T0016 – Structuring](https://framework.amltrix.com/techniques/T0016-structuring)
(sub-techniques: Micro-Structuring, ATM Structuring, Smurfing, Cuckoo
Smurfing). Content used under the
[AMLTRIX License Terms](https://framework.amltrix.com/license) — see
`scenarios/README.md`.

## Sources
- `pipelines/detectors/structuring.py`
- `evaluation/thresholds.json`
- [AMLTRIX T0016 – Structuring](https://framework.amltrix.com/techniques/T0016-structuring)
```

- [ ] **Step 3: Confirm no placeholder text made it in**

Run:
```bash
grep -in "TBD\|TODO\|placeholder" scenarios/structuring.md
```
Expected: no output (exit code 1).

- [ ] **Step 4: Commit**

```bash
git add scenarios/structuring.md
git commit -m "docs: add structuring scenario write-up"
```

---

### Task 3: `scenarios/fan-in-out.md`

**Files:**
- Create: `scenarios/fan-in-out.md`

**Interfaces:**
- Consumes: template shape from Task 1.

- [ ] **Step 1: Verify the source constants before writing the doc**

Run:
```bash
grep -n "WINDOW_HOURS\|MIN_DISTINCT_SENDERS\|MIN_PASS_THROUGH_RATIO" pipelines/detectors/fan_in_out.py
```
Expected output:
```
15:WINDOW_HOURS = 72
16:MIN_DISTINCT_SENDERS = 6
17:MIN_PASS_THROUGH_RATIO = 0.7
```
And:
```bash
python -c "import json; print(json.load(open('evaluation/thresholds.json'))['fan_in_out'])"
```
Expected output: `{'minimum_precision': 0.8, 'minimum_recall': 0.8}`

- [ ] **Step 2: Write `scenarios/fan-in-out.md`**

```markdown
# Scenario: Fan-in / Fan-out (Mule Accounts)

## Status
Implemented - `pipelines/detectors/fan_in_out.py`

## Description
The classic mule-account pattern: an account receives money from many
distinct, often unrelated senders in a short window, then forwards most or
all of the accumulated total onward shortly after. The account itself
retains little to nothing — it's a pass-through point that fragments the
link between the original senders and the ultimate destination.

## Red flags / indicators
- An entity receiving from at least 6 distinct counterparties within a
  72-hour window.
- The account then forwarding at least 70% of the total received within
  that same window (rather than retaining it as would be expected of a
  genuine counterparty).
- No plausible business relationship between the entity and its many
  distinct senders.

## Detection approach
Implemented in `pipelines/detectors/fan_in_out.py`. For each entity, the
detector looks at incoming transactions within `WINDOW_HOURS` (72) of a
given first inbound transaction, and flags the entity once distinct senders
in that window reach `MIN_DISTINCT_SENDERS` (6) and outgoing transfers in
the following window forward at least `MIN_PASS_THROUGH_RATIO` (0.7 = 70%)
of the total received. The alert-prioritization score (60–100, see
`pipelines/README.md`) is derived from how far the sender count and
forward ratio exceed those minimums. The regression floor in
`evaluation/thresholds.json` is 0.80 minimum precision / 0.80 minimum
recall, checked by `evaluation/evaluate.py` and enforced as blocking in CI.

AMLTRIX equivalent: [T0011 – Money Mule Exploitation](https://framework.amltrix.com/techniques/T0011-money-mule-exploitation)
(sub-techniques: Regulated Exchange Mule Transactions, Crypto ATM Mule,
Casino Mule Networks). Content used under the
[AMLTRIX License Terms](https://framework.amltrix.com/license) — see
`scenarios/README.md`.

## Sources
- `pipelines/detectors/fan_in_out.py`
- `evaluation/thresholds.json`
- [AMLTRIX T0011 – Money Mule Exploitation](https://framework.amltrix.com/techniques/T0011-money-mule-exploitation)
```

- [ ] **Step 3: Confirm no placeholder text made it in**

Run:
```bash
grep -in "TBD\|TODO\|placeholder" scenarios/fan-in-out.md
```
Expected: no output (exit code 1).

- [ ] **Step 4: Commit**

```bash
git add scenarios/fan-in-out.md
git commit -m "docs: add fan-in/fan-out scenario write-up"
```

---

### Task 4: `scenarios/pass-through.md`

**Files:**
- Create: `scenarios/pass-through.md`

**Interfaces:**
- Consumes: template shape from Task 1.

- [ ] **Step 1: Verify the source constants before writing the doc**

Run:
```bash
grep -n "MAX_HOURS_BETWEEN\|MIN_FORWARD_RATIO\|MAX_FORWARD_RATIO\|MIN_ROUNDS\|MIN_AMOUNT" pipelines/detectors/pass_through.py
```
Expected output:
```
17:MAX_HOURS_BETWEEN = 24
18:MIN_FORWARD_RATIO = 0.85
19:MAX_FORWARD_RATIO = 1.10
20:MIN_ROUNDS = 2
21:MIN_AMOUNT = 10000
```
And:
```bash
python -c "import json; print(json.load(open('evaluation/thresholds.json'))['pass_through'])"
```
Expected output: `{'minimum_precision': 0.75, 'minimum_recall': 0.75}`

- [ ] **Step 2: Write `scenarios/pass-through.md`**

```markdown
# Scenario: Pass-through (Rapid Movement / Conduit)

## Status
Implemented - `pipelines/detectors/pass_through.py`

## Description
An account repeatedly receives a large sum and forwards nearly all of it
onward within hours — not once, but across multiple separate rounds. Little
to no value is retained between receipt and forwarding, which is more
consistent with a conduit relaying funds on someone else's behalf than a
genuine counterparty transacting for its own purposes.

## Red flags / indicators
- Incoming transfers of at least 10,000 SEK.
- Each followed within 24 hours by outgoing transfers totaling between 85%
  and 110% of the incoming amount (not exactly 100%, since fees/rounding
  are expected — but not wildly more or less either).
- This receive-then-forward pattern repeating across at least 2 separate
  rounds for the same entity.
- Movement restricted to transfer channels (`channel == "transfer"`), not
  cash activity.

## Detection approach
Implemented in `pipelines/detectors/pass_through.py`. For each entity, the
detector matches incoming transfers of at least `MIN_AMOUNT` (10,000) to
outgoing transfers within `MAX_HOURS_BETWEEN` (24) hours whose total falls
between `MIN_FORWARD_RATIO` (0.85) and `MAX_FORWARD_RATIO` (1.10) of the
incoming amount, and flags the entity once at least `MIN_ROUNDS` (2) such
rounds are found. The alert-prioritization score (60–100, see
`pipelines/README.md`) is derived from how far the round count exceeds the
minimum and how close the average forward ratio sits to an exact 100%
pass-through. The regression floor in `evaluation/thresholds.json` is 0.75
minimum precision / 0.75 minimum recall, checked by `evaluation/evaluate.py`
and enforced as blocking in CI.

AMLTRIX equivalent: No direct AMLTRIX equivalent found. AMLTRIX's technique
catalog (304 techniques as of this writing, from
https://github.com/Amlyze/amltrix-data) was searched by name for
"pass-through", "conduit", and "rapid [movement]" with no match — this
pattern doesn't appear to be catalogued there as a distinct named
technique.

## Sources
- `pipelines/detectors/pass_through.py`
- `evaluation/thresholds.json`
```

- [ ] **Step 3: Confirm no placeholder text made it in**

Run:
```bash
grep -in "TBD\|TODO\|placeholder" scenarios/pass-through.md
```
Expected: no output (exit code 1).

- [ ] **Step 4: Commit**

```bash
git add scenarios/pass-through.md
git commit -m "docs: add pass-through scenario write-up"
```

---

### Task 5: `scenarios/communities.md`

**Files:**
- Create: `scenarios/communities.md`

**Interfaces:**
- Consumes: template shape from Task 1.

- [ ] **Step 1: Verify the source constants before writing the doc**

Run:
```bash
grep -n "MIN_COMMUNITY_SIZE\|MAX_COMMUNITY_SIZE\|MIN_INTERNAL_DENSITY\|MIN_INTERNAL_VOLUME_SHARE" pipelines/detectors/communities.py
```
Expected output:
```
18:MIN_COMMUNITY_SIZE = 4
19:MAX_COMMUNITY_SIZE = 25
20:MIN_INTERNAL_DENSITY = 0.35
21:MIN_INTERNAL_VOLUME_SHARE = 0.6
```
And:
```bash
python -c "import json; d=json.load(open('evaluation/thresholds.json')); print('communities' in d, 'community_ring' in d)"
```
Expected output: `False False` (confirms no floor is configured, matching the doc below).

- [ ] **Step 2: Write `scenarios/communities.md`**

```markdown
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
```

- [ ] **Step 3: Confirm no placeholder text made it in**

Run:
```bash
grep -in "TBD\|TODO\|placeholder" scenarios/communities.md
```
Expected: no output (exit code 1).

- [ ] **Step 4: Commit**

```bash
git add scenarios/communities.md
git commit -m "docs: add network communities scenario write-up"
```

---

### Task 6: `scenarios/funnel-accounts.md`

**Files:**
- Create: `scenarios/funnel-accounts.md`

**Interfaces:**
- Consumes: template shape from Task 1.

- [ ] **Step 1: Write `scenarios/funnel-accounts.md`**

```markdown
# Scenario: Funnel Accounts

## Status
Not yet implemented. This write-up is grounding for a possible future
detector — no code in `pipelines/detectors/` implements it today.

## Description
Depositing illicit proceeds in one location — often structured below
reporting thresholds — and rapidly transferring or withdrawing them
elsewhere, obscuring the origin of funds and frustrating attempts to trace
a cohesive trail. Criminals commonly deposit structured cash into an
individual or business account in one region, then withdraw or transfer
the funds from a different location shortly after. The technique is also
used to facilitate trade-based money laundering — multiple funnel accounts
may consolidate into a single account that issues payments for goods,
creating a façade of legitimate trade — and has been observed in human
trafficking networks, where perpetrators control or coerce accounts across
different locales and direct victims or third parties to deposit proceeds
before rapidly withdrawing them.

Primary tactic: Layering. Associated risks: Product Risk, Jurisdictional
Risk — funnel accounts exploit deposit/transfer products (personal
checking, business accounts) that accommodate rapid fund movement with
minimal scrutiny, across multiple regions/institutions with varying AML
controls.

## Red flags / indicators
- Funds transferred to multiple beneficiaries in different locations or
  countries with no apparent business or personal relationship with the
  account holder.
- Transactions involving multiple currencies not typically used by the
  account holder.
- Frequent changes to the destination of funds, with new beneficiaries
  regularly added without a clear business or personal rationale.
- Frequent transfers to jurisdictions with lax regulatory oversight or
  officially classified as high-risk, inconsistent with the customer's
  usual activity.
- Accounts receiving funds from a single source but dispersing them to
  multiple unrelated accounts or entities.
- Beneficiaries in multiple regions with no apparent connection to the
  account holder's stated line of business.
- Beneficiaries in jurisdictions known for weak AML controls or high
  levels of secrecy.
- A sudden increase in volume or frequency of international transfers
  without a corresponding rise in legitimate business activity.
- Funds rapidly moved through a series of accounts or countries before
  reaching the final recipient, creating a complex transaction chain.
- Inconsistent or contradictory explanations for the purpose of
  cross-border transfers when questioned.
- Frequent currency exchanges with no evident business requirement.
- Beneficiaries with no previous transaction history with the account
  holder.
- Transaction amounts structured to exploit currency exchange rate
  differences without a legitimate business reason.
- Sudden changes in the direction or volume of transfers without a clear
  explanation.
- Beneficiaries in countries with significant exchange rate volatility,
  facilitating arbitrage-based transactions.
- Repeated structured cash deposits below reporting thresholds at
  multiple branches or ATMs, followed by rapid outbound transfers to
  other regions.
- Multiple unrelated funnel accounts feeding a single account used for
  significant trade-based payments or goods purchases without a
  legitimate commercial explanation.
- Accounts appearing to be controlled by third parties across diverse
  regions, with coerced or forced depositors followed by immediate
  withdrawals.

## Detection approach

**Not yet implemented.** Building this as a real detector, following the
"Adding a new detector" recipe in `pipelines/README.md`, would need:

1. **A generator routine** in `data/synthetic_generator.py` that injects a
   funnel-account pattern: structured cash deposits for one entity across
   multiple simulated branches/locations, followed by transfers or
   withdrawals from a *different* location within a short window. The
   existing schema (`sender_id`, `receiver_id`, `amount`, `timestamp`,
   `channel`, `transaction_id`) has no location/branch field today —
   `structuring.py` only distinguishes `channel == "cash_deposit"`, not
   *where* the deposit happened. A location or branch-id column would need
   to be added to the generator's output before a funnel-account detector
   could check for the cross-location signal that defines this pattern
   (as opposed to `structuring.py`'s existing same-entity, any-location
   check).
2. **A detector** (`pipelines/detectors/funnel_accounts.py`) with a
   `detect(transactions) -> pd.DataFrame` function returning the same
   `entity_id`, `detector`, `reason`, `score`, `raw_score` columns as the
   other four, checking for structured near-threshold cash deposits
   clustering in one location followed by transfers/withdrawals from a
   different location within a short window.
3. **Registration** in `DETECTORS` in `pipelines/run_pipeline.py`.
4. **A regression floor** added to `evaluation/thresholds.json` once the
   detector has been run against generated data enough to pick a
   defensible precision/recall floor (see how the other four detectors'
   floors were set, per `evaluation/README.md`).

Data sources that would matter for detecting this in a real institution
(from AMLTRIX, not this repo's current schema):
- **Geographical & Jurisdictional Risk Data** — consolidated risk ratings
  and AML standards; surfaces suspicious cross-border flows involving
  high-risk jurisdictions.
- **Financial, Business & Tax Records** — official statements, filings,
  and tax returns, to validate whether transfers align with legitimate
  activity.
- **Currency Exchange Transactions** — conversions with timestamps,
  volumes, rates, and counterparties, to identify unexplained
  multi-currency exchanges.
- **Transaction Logs** — deposits, withdrawals, transfers, metadata,
  timestamps, and counterparties, revealing structured deposits and rapid
  inbound-outbound flows.
- **Money Service Business (MSB) Registries** — identifying unlicensed
  remitters potentially used for funnel accounts across borders.
- **Trade Documentation** — invoices, bills of lading, shipping records,
  to distinguish legitimate trade from fabricated sales or trade-based
  layering.
- **KYC & Customer Due Diligence Records** — verified customer information
  and beneficial ownership, to compare declared activity against actual
  transaction patterns.
- **ATM Usage & Geolocation Data** — deposit locations, timestamps, and
  branch details, revealing structured cash deposit patterns across
  multiple locations.
- **Communication Records** — call logs, emails, messaging data, which can
  disclose funnel-account instructions, coercion, or contradictory
  transfer explanations.
- **Geographical Transaction Data** — transaction origins, destinations,
  and geo-coordinates, tracing multi-jurisdictional routes.

## Mitigations (from AMLTRIX)

- **Country Risk Assessment** — identify and categorize jurisdictions
  commonly exploited for funnel accounts due to lax regulation, low
  transparency, or minimal AML oversight; apply extra scrutiny when
  cross-border transfers involve them.
- **Enhanced Due Diligence (EDD)** — deeper verification of ownership
  structure, fund sources, and multi-location deposit reasons; collect
  supporting documentation for cross-border transactions and verify
  beneficiary legitimacy.
- **Customer Due Diligence (CDD)** — verify account holder and authorized
  user identity for cross-regional transfers; ensure business/personal
  activity justifies frequent geographically-dispersed inbound deposits.
- **Transaction Monitoring** — automated scenarios targeting repeated
  sub-threshold cash deposits at different branches/ATMs, immediate
  transfers to unrelated beneficiaries in other regions, frequent
  unexplained currency exchanges, and abrupt velocity/direction changes.
- **Staff AML Training & Awareness** — target training on funnel-account
  indicators specifically: multiple small deposits across branches,
  immediate cross-border withdrawals, inconsistent currency/beneficiary
  explanations.
- **Information Sharing and Collaboration** — exchange intelligence on
  funnel-account typologies and structured-deposit patterns with peer
  institutions and relevant authorities.
- **Service Restriction** — restrict or suspend high-risk services
  (frequent cross-border wires, large currency exchanges) for accounts
  showing repeated funneling signs.
- **Trade Monitoring** — monitor trade-related payments from multiple
  funnel accounts consolidating into a single account; cross-check
  invoices, shipping documents, and valuations for inconsistencies.

## Actor profiles (from AMLTRIX)

- **Human Trafficker** — maintains or coerces control over multiple
  accounts in different locales, directing victims or third parties to
  deposit proceeds, then withdrawing/transferring quickly to fragment
  transaction records.
- **Business Entity** — holds accounts where multiple structured deposits
  converge before transferring funds under the guise of business expenses
  or goods purchases, providing a façade of legitimate operations.
- **Illicit Operator** — establishes or directs accounts across multiple
  regions to deposit structured cash sums below reporting thresholds,
  rapidly transferring or withdrawing to obscure source and ownership.
- **Money Mule** — deposits illicit cash under criminal instruction, often
  below threshold reporting limits, then transfers or withdraws in other
  regions, breaking the chain between deposit and ultimate beneficiary.
- **Financial Institution** — (as an exploited channel) opening/maintaining
  personal and business accounts across branches or locations, enabling
  structured deposits and rapid inter-branch/cross-border transfers that
  limit a unified transactional view.

## Related instruments / services exploited (from AMLTRIX)

- **Instruments:** Bank Accounts (personal or business, receiving
  structured small deposits before rapid onward movement); Cash (physical
  currency structured below reporting thresholds, hard to trace once
  deposited across locations).
- **Services/products:** Electronic Funds Transfer (EFT), ATM Services,
  Peer-to-Peer Payment Systems, Payment Processing Services, Business Bank
  Accounts, Money Transfer and Remittance Services, Personal Checking
  Accounts, Wire Transfer Services — each cited by AMLTRIX as a channel
  that permits fast fund movement/aggregation with minimal scrutiny.

## Sources
- [AMLTRIX T0083 – Funnel Accounts](https://framework.amltrix.com/techniques/T0083-funnel-accounts)
- [AMLTRIX data export (Amlyze/amltrix-data)](https://github.com/Amlyze/amltrix-data) — used to cross-check and complete this write-up against the authoritative CSV records (18 indicators, 8 mitigations, 10 data sources, 5 actor profiles, 2 instruments, 8 services, 1 tactic)
- [AMLTRIX License Terms](https://framework.amltrix.com/license) — content used under this license; see `scenarios/README.md` for the attribution note
- FinCEN (2014-05-28). "Update on U.S. currency restrictions in Mexico: Funnel accounts and TBML." https://www.fincen.gov/resources
- FinCEN (2020). "Supplemental Advisory on Identifying and Reporting Human Trafficking and Related Activity" (FIN-2020-A008). https://www.fincen.gov/resources/advisories/fincen-advisory-fin-2020-a008
- Dixon, D. (2020). "Bonus episode: A deep dive into anti-money laundering." The Compliance Times. https://thecompliancetimes.com
```

- [ ] **Step 2: Confirm no placeholder text made it in**

Run:
```bash
grep -in "TBD\|TODO\|placeholder" scenarios/funnel-accounts.md
```
Expected: no output (exit code 1).

- [ ] **Step 3: Commit**

```bash
git add scenarios/funnel-accounts.md
git commit -m "docs: add funnel accounts scenario write-up (AMLTRIX T0083)"
```

---

### Task 7: Update `skills/typology-research/SKILL.md`

**Files:**
- Modify: `skills/typology-research/SKILL.md:47-49`

**Interfaces:**
- Consumes: none.

- [ ] **Step 1: Confirm current content at the insertion point**

Run:
```bash
sed -n '46,50p' skills/typology-research/SKILL.md
```
Expected output:
```
## How to research

1. Check `grounding/resources.md` first for a source that already covers
   this typology.
```

- [ ] **Step 2: Insert the repo-aware step**

Change:
```markdown
## How to research

1. Check `grounding/resources.md` first for a source that already covers
   this typology.
```
To:
```markdown
## How to research

0. If the current repo has a `scenarios/` folder, write the brief there
   using its template (`scenarios/README.md`) instead of an external
   personal collection — steps 1-4 below describe ad hoc research with no
   such folder to land in.
1. Check `grounding/resources.md` first for a source that already covers
   this typology.
```

- [ ] **Step 3: Verify the edit**

Run:
```bash
grep -n "scenarios/ folder\|scenarios/README.md" skills/typology-research/SKILL.md
```
Expected: two matching lines from the new step 0.

- [ ] **Step 4: Commit**

```bash
git add skills/typology-research/SKILL.md
git commit -m "docs: point typology-research skill at scenarios/ when present"
```

---

### Task 8: Cross-link from `pipelines/README.md`

**Files:**
- Modify: `pipelines/README.md:15-16`

**Interfaces:**
- Consumes: none.

- [ ] **Step 1: Confirm current content at the insertion point**

Run:
```bash
sed -n '10,17p' pipelines/README.md
```
Expected output:
```
| File | Typology | Core logic |
|---|---|---|
| `detectors/structuring.py` | Structuring / smurfing | Sliding time window; flags cash deposits near an illustrative internal scenario threshold |
| `detectors/fan_in_out.py` | Mule accounts | Flags entities receiving from many distinct senders in a window, then forwarding most of it onward shortly after |
| `detectors/pass_through.py` | Rapid movement / conduit | Flags entities that repeatedly receive a large sum and forward nearly all of it within hours |
| `detectors/communities.py` | Network rings | Louvain community detection on the transaction graph; flags tightly-connected clusters where volume mostly stays inside the cluster |

Every detector takes a pandas DataFrame of transactions and returns a
```

- [ ] **Step 2: Add the cross-link sentence after the table**

Insert this new line directly after the table (after the
`detectors/communities.py` row, before the blank line that precedes
"Every detector takes..."):

```markdown
See `scenarios/<name>.md` (e.g. `scenarios/structuring.md`) for the full
typology write-up behind each detector.
```

The section becomes:
```markdown
| File | Typology | Core logic |
|---|---|---|
| `detectors/structuring.py` | Structuring / smurfing | Sliding time window; flags cash deposits near an illustrative internal scenario threshold |
| `detectors/fan_in_out.py` | Mule accounts | Flags entities receiving from many distinct senders in a window, then forwarding most of it onward shortly after |
| `detectors/pass_through.py` | Rapid movement / conduit | Flags entities that repeatedly receive a large sum and forward nearly all of it within hours |
| `detectors/communities.py` | Network rings | Louvain community detection on the transaction graph; flags tightly-connected clusters where volume mostly stays inside the cluster |

See `scenarios/<name>.md` (e.g. `scenarios/structuring.md`) for the full
typology write-up behind each detector.

Every detector takes a pandas DataFrame of transactions and returns a
```

- [ ] **Step 3: Verify the edit**

Run:
```bash
grep -n "scenarios/" pipelines/README.md
```
Expected: one matching line.

- [ ] **Step 4: Commit**

```bash
git add pipelines/README.md
git commit -m "docs: link pipelines/README.md to scenarios/ write-ups"
```

---

### Task 9: Add `scenarios/` to the root repository-layout tree

**Files:**
- Modify: `README.md:109-110`

**Interfaces:**
- Consumes: none.

- [ ] **Step 1: Confirm current content at the insertion point**

Run:
```bash
sed -n '98,111p' README.md
```
Expected output:
```
\`\`\`
fincrime-llm-toolkit/
├── docs/         Setup guides — data hygiene, Claude.ai, Claude Code, MCP,
│                 model selection, portability
├── profiles/     Paste-ready Claude Project instructions per role
├── skills/       Claude Code skills (real code, not just prompts)
├── prompts/      Single-task prompt templates with example input/output
├── grounding/    EU + Swedish source registers, plus curated resources.md
├── pipelines/    Python detection logic run against synthetic data
├── evaluation/   Role-aware precision/recall scoring against ground truth
├── data/         Synthetic transaction generator + sample dataset
├── dashboard/    Model tuning dashboard (React + Vite, client-side)
└── mcp/          MCP config examples (filesystem, SQLite) as a grounding layer
\`\`\`
```

- [ ] **Step 2: Change the `dashboard/` line's connector and add the new `scenarios/` line**

Change:
```
├── dashboard/    Model tuning dashboard (React + Vite, client-side)
└── mcp/          MCP config examples (filesystem, SQLite) as a grounding layer
```
To:
```
├── dashboard/    Model tuning dashboard (React + Vite, client-side)
├── scenarios/    Typology write-ups grounded in the real detectors + AMLTRIX
└── mcp/          MCP config examples (filesystem, SQLite) as a grounding layer
```

- [ ] **Step 3: Verify the edit**

Run:
```bash
grep -n "scenarios/" README.md
```
Expected: one matching line, and:
```bash
grep -c "^├──\|^└──" README.md
```
Expected: unchanged total connector-line count plus one (one line added, no lines removed).

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add scenarios/ to the repository layout tree"
```

---

### Task 10: Push and open the draft PR

**Files:** none (git/GitHub operations only).

- [ ] **Step 1: Push the branch**

```bash
git push -u origin docs/scenarios-funnel-accounts
```

- [ ] **Step 2: Open a draft PR**

```bash
gh pr create --draft \
  --repo overjoyde/bear-fincrime-toolkit-2.0 \
  --title "docs: add scenarios/ folder (structuring, fan-in-out, pass-through, communities, funnel accounts)" \
  --body "$(cat <<'EOF'
## Summary
- Adds `scenarios/` — one write-up per existing detector (structuring, fan-in-out, pass-through, communities), grounded in the real code/thresholds/evaluation floors, plus a new `funnel-accounts.md` sourced from AMLTRIX T0083 (not yet implemented as a detector).
- `structuring.md` and `fan-in-out.md` cross-reference their AMLTRIX equivalents (T0016, T0011); `pass-through.md` and `communities.md` explicitly note no equivalent was found.
- Updates `skills/typology-research/SKILL.md` to point at `scenarios/` when present, since its old guidance predates this folder.
- Cross-links from `pipelines/README.md` and the root `README.md` layout tree.

Spec: `docs/superpowers/specs/2026-07-22-scenarios-folder-design.md`
Plan: `docs/superpowers/plans/2026-07-22-scenarios-folder.md`

## Test plan
- [x] Every implemented scenario doc's constants/floor verified against `pipelines/detectors/*.py` and `evaluation/thresholds.json` via grep (see plan tasks 2-5)
- [x] No placeholder text (`grep -in "TBD\|TODO\|placeholder"`) in any new file
- [x] AMLTRIX content attributed with source links and license link per `scenarios/README.md`
- [ ] Human read-through of all five scenario docs

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 3: Confirm the PR was created**

Run:
```bash
gh pr view --repo overjoyde/bear-fincrime-toolkit-2.0 --json url,isDraft
```
Expected: JSON showing `"isDraft": true` and a valid `url`.
