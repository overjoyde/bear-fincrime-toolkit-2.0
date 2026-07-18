# Data hygiene: what never goes into a prompt

Read this before anything else in the repo. Everything downstream - profiles,
prompts, skills, MCP - assumes you have internalized this.

## The rule

**No real customer data, case data, or institution-identifying detail ever
goes into an LLM chat, project knowledge base, or MCP-connected store**
unless your institution has an approved, contractually-covered path for it
(enterprise agreement with a data-processing addendum, a self-hosted model,
or a private/VPC deployment your DPO has actually signed off on) - and even
then, only what that approval covers.

Consumer-tier Claude.ai, ChatGPT, or Gemini accounts are not that path.
Neither is a personal API key. If you are not sure whether your organization
has an approved path, assume it does not until someone in compliance/legal/IT
security tells you otherwise in writing.

## What counts as "real customer data"

More than you would think:

- Names, personal numbers/SSNs, account numbers, IBANs, card numbers -
  obviously.
- Free-text case narratives, even "anonymized" ones. Narrative text is
  routinely re-identifiable from context (amounts, dates, merchant names,
  a distinctive transaction pattern) even with names stripped.
- Screenshots of case management systems, alert queues, or dashboards -
  these leak far more than the field you meant to show (window titles,
  other rows, internal system names, colleague names in an assignee column).
- Internal typology names, rule IDs, or threshold values that are specific
  to your institution's tuning - these are not "customer data" but they are
  proprietary/competitively sensitive, and some are supervisory-confidential.
- Regulator correspondence, exam findings, remediation plans - these are
  often the most sensitive documents in the building. Never paste them
  anywhere.

## What's safe to use

- Everything in this repo's `data/` folder - synthetically generated,
  with no link to any real person or institution.
- Publicly documented typologies from FATF, Egmont Group, national FIU
  typology reports, and your own regulator's published guidance (the
  guidance itself, not your institution's internal response to it).
- The regulatory text in `grounding/` - it's public law.
- Aggregate, rounded statistics with no way to reconstruct an individual
  transaction or customer (e.g. "SAR volume by month" is usually fine;
  "list of the 12 SARs filed last week with amounts" is not).

## The synthetic-first workflow this repo assumes

1. Generate synthetic data with `data/synthetic_generator.py` that has the
   same *shape* as your real data (same typologies, similar volume, similar
   noise) but no connection to a real person.
2. Develop and test every prompt, profile, and skill against that synthetic
   data until you trust the output.
3. Only once a prompt/skill is validated do you consider whether your
   institution's approved path allows running it against real data - and
   that is an institutional decision, not something this repo can make for you.

## Redaction is not a substitute for synthetic data

If you are tempted to hand-redact a real case before pasting it in: do not.
Manual redaction misses things (a distinctive amount, a date that matches a
public event, a merchant name that only appears once). Build a synthetic
case with the same structure instead. It takes longer once and saves you
from a disclosure incident forever.
