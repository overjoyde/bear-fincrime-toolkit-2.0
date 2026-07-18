# EU AML/CTF instruments — source register

Verified against EUR-Lex. If you find one of these has been superseded,
open a PR — legal text moves and this file needs to move with it.

## The 2024 AML package (core)

### AMLR — Regulation (EU) 2024/1624
Regulation (EU) 2024/1624 of the European Parliament and of the Council of
31 May 2024 on the prevention of the use of the financial system for the
purposes of money laundering or terrorist financing.

- First **directly applicable** EU rulebook for AML/CFT (a Regulation, not
  a Directive that needs national transposition) — this is the biggest
  structural change in the package.
- Covers: obliged-entity due diligence measures, beneficial ownership
  transparency, limits on anonymous instruments (cash, crypto).
- Entered into force: 9 July 2024. **Applies from 10 July 2027** (most
  provisions) — this is a future date, not current law yet, as of this
  writing.
- Source: https://eur-lex.europa.eu/eli/reg/2024/1624/oj/eng

### AMLD6 — Directive (EU) 2024/1640
Directive (EU) 2024/1640 of the European Parliament and of the Council of
31 May 2024 on the mechanisms to be put in place by Member States for the
prevention of the use of the financial system for money laundering or
terrorist financing purposes.

- Covers: national AML policy mechanisms, FIU responsibilities and powers,
  supervisor responsibilities, beneficial ownership/bank account registers,
  golden-visa (residence-by-investment) restrictions.
- Requires national transposition (it's a Directive) — check your Member
  State's transposing legislation for the actually-binding local text.
- Source: https://eur-lex.europa.eu/eli/dir/2024/1640/oj/eng

### AMLA — Regulation (EU) 2024/1620
Regulation (EU) 2024/1620 of the European Parliament and of the Council of
31 May 2024 establishing the Authority for Anti-Money Laundering and
Countering the Financing of Terrorism (AMLA).

- Creates a new EU-level supervisory authority (seat: Frankfurt am Main)
  with direct supervisory power over a set of "selected" high-risk obliged
  entities, plus a coordination role over national supervisors and FIUs.
- Source: https://eur-lex.europa.eu/eli/reg/2024/1620/oj/eng

All three were adopted the same day (31 May 2024) and are meant to be read
together — a change described as "the AML package" almost always means these
three plus the funds-transfer regulation below.

## Related instruments

### Regulation (EU) 2023/1113 — funds/crypto-asset transfer information ("Travel Rule")
Recast of the 2015 Funds Transfer Regulation, extending information/
traceability requirements to crypto-asset transfers, aligned with the
Markets in Crypto-Assets Regulation (MiCA). Applied from 30 December 2024.

### IPR — Regulation (EU) 2024/886 (Instant Payments Regulation)
Regulation (EU) 2024/886 of 13 March 2024, amending Regulation (EU) No
260/2012, Regulation (EU) 2021/1230, and Directives 98/26/EC and (EU)
2015/2366, on instant credit transfers in euro.

- Relevant to TM because it compresses the time window for screening
  (sanctions screening in particular) around instant euro transfers —
  PSPs must offer instant receiving/sending within tight phased deadlines
  (2025 for eurozone PSPs, 2027 for non-eurozone EU PSPs).
- Source: https://eur-lex.europa.eu/eli/reg/2024/886/oj/eng

### PSD2 — Directive (EU) 2015/2366 (current regime)
The currently-in-force Payment Services Directive. Relevant baseline for
PSP obligations until PSD3/PSR (below) replace it.

### PSD3 / PSR — proposed, not yet in force
The Commission's June 2023 proposals for a third Payment Services Directive
and a new Payment Services Regulation, intended to eventually replace PSD2.
**Treat as a proposal, not binding law**, until adopted and published in the
Official Journal — check EUR-Lex's procedure file for current status before
citing this as if it were settled.

## How to use this file

- Cite the specific article, not just the instrument, when doing gap
  analysis (see `prompts/reg-gap-analysis.md`).
- Always check the "applies from" date, not just the "entered into force"
  date — the AML package in particular has a multi-year gap between the two
  for its core provisions.
- Don't treat this file as a substitute for checking EUR-Lex directly for
  amendments — regulatory text is corrigenda-prone in the months after
  publication.
