# Curated resources

A working reading list for AML/CTF + LLM practitioners, not an exhaustive
link dump. Everything here is something a practitioner would actually
return to, organized so you can find it again. Add your own finds under the
matching category — see `CONTRIBUTING.md`.

> If you're merging in your own compiled list: keep the category structure,
> drop anything paywalled/vendor-gated into "Tools & vendors" rather than
> mixing it with the standards-body material above it, and prefer linking
> the primary source over a summary blog whenever both exist.

## Standard-setters and typology sources

- **FATF (Financial Action Task Force)** — https://www.fatf-gafi.org/ —
  the primary source for global AML/CTF standards (the "40 Recommendations")
  and periodic typology reports. Start here for any typology research.
- **Egmont Group** — https://egmontgroup.org/ — the network of national
  FIUs; publishes cross-border typology and information-sharing material.
- **Wolfsberg Group** — https://www.wolfsberg-principles.com/ — bank-led
  principles and guidance papers, particularly useful for correspondent
  banking and CDD/EDD frameworks.
- **Basel Institute on Governance — Basel AML Index** —
  https://index.baselgovernance.org/ — annual country risk ranking with
  methodology notes; useful for geographic risk-factor reasoning.

## Regulatory and supervisory bodies (EU/SE-anchored, see grounding/*.md for details)

- **European Banking Authority (EBA)** — https://www.eba.europa.eu/ —
  AML/CFT guidelines that sit underneath the EU regulatory package.
- **AMLA (Authority for AML/CFT)** — establishing regulation and mandate
  covered in `eu-instruments.md`; its own site/publications will become
  increasingly relevant as it becomes operational ahead of 2027-2028.
- **Finansinspektionen (Sweden)** — https://www.fi.se/ — supervisor for
  most FFFS 2017:11-covered entities; publishes decisions and guidance.
- **Swedish FIU (Finanspolisen)** — reporting via goAML; see
  `se-instruments.md`.

## Practitioner communities and training

- **ACAMS (Association of Certified Anti-Money Laundering Specialists)** —
  https://www.acams.org/ — certifications (CAMS) and a large practitioner
  article/webinar library; much of the deep content is membership-gated.
- **ACFCS (Association of Certified Financial Crime Specialists)** —
  https://www.acfcs.org/ — comparable to ACAMS, different certification
  track (CFCS).

## Synthetic/public datasets for testing (see also `data/README.md`)

- **SAML-D** — a labeled synthetic AML transaction dataset designed
  specifically for ML-based detection research; check the dataset's current
  hosting (Kaggle/academic mirror) as these move over time.
- **AMLSim** — an agent-based synthetic transaction simulator originally
  developed by IBM Research, designed to generate realistic multi-typology
  transaction graphs with ground truth.
- **PaySim** — a widely-used synthetic mobile-money transaction dataset,
  useful for fraud/AML detection benchmarking though its typologies are
  narrower than AMLSim's.

## Tools & vendors (no endorsement — informational only)

This section is intentionally sparse. This toolkit doesn't recommend paid
products. If you add a vendor tool here, note plainly what it costs and
what it's actually for — don't let a link collection turn into a sales
channel.

## Portability

This file has no Claude-specific content — it's a link list, usable as-is
regardless of which LLM (if any) you're pairing it with.
