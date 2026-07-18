# Swedish AML/CTF instruments — source register

## Penningtvättslagen — Lag (2017:630)
Lag (2017:630) om åtgärder mot penningtvätt och finansiering av terrorism
(the Swedish Anti-Money Laundering Act).

- Implements the EU's then-current AML directive (4th AMLD, 2015) into
  Swedish law; in force since 1 August 2017 and amended repeatedly since.
- Applies to a broad set of obliged entities across multiple supervisory
  regimes (not just banks) — check which supervisor applies to your sector,
  since supervision is split across authorities in Sweden.
- Source: https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/lag-2017630-om-atgarder-mot-penningtvatt-och_sfs-2017-630/

## FFFS 2017:11 — Finansinspektionens föreskrifter
Finansinspektionens föreskrifter om åtgärder mot penningtvätt och
finansiering av terrorism.

- Finansinspektionen's (FI, the Swedish FSA) implementing regulations for
  entities under its supervision — the operational detail underneath the
  Act above (risk assessment methodology, customer due diligence
  procedures, monitoring, reporting, internal control).
- Only binds entities FI supervises — if you're supervised by a different
  authority (e.g. gambling operators under Spelinspektionen), check that
  authority's own AML regulations instead; FFFS 2017:11 itself is
  FI-specific.
- Source: https://www.fi.se/sv/vara-register/fffs/sok-fffs/2017/201711/

## goAML — Swedish FIU reporting channel
Sweden's Financial Intelligence Unit (Finanspolisen, part of the Swedish
Police Authority) uses **goAML**, the UNODC-developed case management and
reporting platform, as its channel for receiving suspicious activity/
transaction reports from obliged entities. goAML is used by a large number
of national FIUs worldwide, not just Sweden's — if you're implementing a
reporting integration, check your own jurisdiction's FIU for whether it
uses goAML and what its specific XML schema/registration process requires,
since implementations vary by country even on the same platform.

## How to use this file

- This file assumes Swedish supervision. If you're supervised by a
  different national FSA or FIU, treat this as a template to replace, not
  a source of truth for your regime — see `docs/06-portability.md`'s note
  on what doesn't generalize.
- Swedish AML law will need to change to implement AMLD6 and align with
  AMLR ahead of AMLR's 2027 application date (see `eu-instruments.md`) —
  expect this file to need updates as that transposition happens.
