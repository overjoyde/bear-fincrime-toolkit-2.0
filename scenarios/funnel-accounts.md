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
