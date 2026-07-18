---
name: typology-research
description: Structures research on a money-laundering or terrorist-financing typology into a standard brief (description, red flags, detection approach, relevant regulatory/typology-report sources). Use when asked to research, summarize, or write up a typology, red flags for a specific pattern, or a typology brief (e.g. trade-based money laundering, mule networks, crypto off-ramping).
---

# Typology Research

Turns typology research into a consistent brief format instead of an
unstructured summary, so briefs accumulate into a comparable reference set
over time.

## When this applies

- The user asks to research or summarize a specific ML/TF typology.
- The user asks for red flags / indicators for a named pattern.
- The user wants to add a new typology brief to a personal or team reference
  set.

## Standard brief format

```markdown
# Typology: <name>

## Description
Plain-language description of the pattern and why it's used to obscure
illicit funds.

## Common variants
Named sub-patterns if the typology has recognized variations (be explicit
this is descriptive, not exhaustive).

## Red flags / indicators
A concrete, checkable list - not vague statements. Each indicator should be
something you could actually look for in transaction or customer data.

## Detection approach
How this typology is typically detected (rule-based threshold, network
analysis, behavioral scoring) - and, if relevant, which detector in
pipelines/detectors/ (if any) implements a related check.

## Sources
Named, linkable sources only - FATF reports, Egmont Group typology
publications, national FIU guidance, or academic literature. Never an
unsourced summary presented as fact.
```

## How to research

1. Check `grounding/resources.md` first for a source that already covers
   this typology.
2. If web research is available, prioritize FATF, Egmont Group, and national
   FIU (e.g. FinCEN, FIU-Sweden via goAML guidance) publications over
   secondary blog summaries.
3. Fill in the brief format above. If a section can't be populated from a
   credible source, say so rather than generalizing from first principles
   and presenting it as sourced.
4. Offer to save the brief into a personal typology-briefs collection
   (outside this repo, since sourced/curated briefs a user builds over time
   are their own reference material, not toolkit content).

## Boundaries

- Every red flag and detection-approach claim should be traceable to a
  source or to this repo's actual code - not invented plausible-sounding
  indicators.
