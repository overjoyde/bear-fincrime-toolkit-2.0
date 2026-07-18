# Contributing

This toolkit grows by use, not by committee. Useful ways to contribute:

- **New typologies** — add a detector to `pipelines/detectors/`, a matching
  injection routine to `data/synthetic_generator.py`, and a short entry in
  `grounding/resources.md` if you're citing a typology report.
- **New profiles** — a Project-instructions file for a role this toolkit
  doesn't cover yet (e.g. sanctions screening, trade-based ML). Follow the
  structure of the existing files in `profiles/`.
- **Grounding sources** — corrections or additions to `grounding/eu-instruments.md`
  / `se-instruments.md`. Link to the actual instrument (ELI/EUR-Lex, official
  gazette), not a summary blog.
- **Portability notes** — if you've adapted a profile/prompt/skill to a
  non-Claude model and found gotchas, add them to the relevant file's
  portability section.

## Ground rules

- No real customer, case, or institution data — ever, anywhere in this repo,
  including issues and PRs. Use the synthetic generator in `data/` for any
  example that needs realistic-looking transactions.
- No vendor pitches. If a tool needs a paid API key to be useful, say so
  plainly in `grounding/resources.md` rather than baking it into a prompt.
- Keep additions jurisdiction-labeled. AML law is not the same in every
  country — say which regime a profile/prompt assumes.
