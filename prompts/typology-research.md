# Prompt: Typology Research

Single-turn prompt version of the `typology-research` skill's brief format -
useful when you want the structured output in a plain chat without Claude
Code's skill auto-triggering.

## Prompt template

```
Research the following money-laundering/terrorist-financing typology and
produce a brief in this exact format:

# Typology: <name>

## Description
## Common variants
## Red flags / indicators
## Detection approach
## Sources

Only include sources you can name specifically (FATF, Egmont Group, a named
national FIU publication, or specific academic literature). If you can't
source a section credibly, say so explicitly rather than presenting an
unsourced summary as fact.

Typology to research: <name, e.g. "trade-based money laundering via
over/under-invoicing">
```

## Example (synthetic, abbreviated)

**Input:** `Typology to research: mule account networks in P2P payment
rails`

**Expected kind of output:**
```
# Typology: Mule account networks in P2P payment rails

## Description
Funds from a predicate offense (e.g. fraud, romance scams, phishing) are
routed through a layer of consenting or unwitting "mule" accounts to
obscure the trail back to the offense before reaching the ultimate
beneficiary...

## Common variants
- Witting mules (recruited, often via "money mule" job scams)
- Unwitting/victim mules (romance scam or fraud victims used as
  intermediaries without knowledge)
- Synthetic-identity mule accounts

## Red flags / indicators
- Rapid pass-through: funds received and forwarded within a short window,
  with the account otherwise low-activity
- Receiving from many unrelated senders, forwarding to one or few receivers
  (fan-in / narrow fan-out)
- Account tenure short relative to transaction volume

## Detection approach
Network/graph analysis (fan-in/fan-out ratio, pass-through timing) rather
than single-transaction thresholds - see pipelines/detectors/fan_in_out.py
and pass_through.py in this repo for a synthetic-data implementation.

## Sources
[Named FATF/Egmont/FIU publication(s) - filled in based on actual research,
not fabricated]
```

## Portability

Plain prompt, no Claude-specific features. See `docs/06-portability.md`.
