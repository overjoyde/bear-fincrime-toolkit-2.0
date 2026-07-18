# Claude Code for TM/KYC analysts

Claude.ai Projects are for reasoning over documents and drafting text. Claude
Code is for when you want to run something - the synthetic generator, a
detection script, a batch of file transformations - with Claude driving the
terminal instead of you copy-pasting code out of a chat window.

## Why this matters for this line of work

The pipelines in this repo (`pipelines/`, `data/synthetic_generator.py`) are
real Python. You can read the code and run it yourself with no LLM involved
at all - that is the point of shipping working code instead of prompts that
describe code. Claude Code is useful on top of that for:

- Adapting a detector's thresholds to your own synthetic data without
  hand-editing every constant.
- Adding a new typology to the generator and a matching detector in the same
  session, so they stay consistent with each other.
- Running the pipeline and iterating on its output interactively (checking
  why a flag rate looks too high) without leaving the terminal.

## Set up a project-level CLAUDE.md

If you clone this repo (or copy parts of it into your own working directory),
add a short CLAUDE.md at the root stating the constraints that matter for
this kind of work, for example:

- Never operate on files outside data/generated/ and data/sample/ - those
  are the only directories that may contain data, and it is always synthetic.
- Detection thresholds live in pipelines/detectors/*.py as named constants,
  not magic numbers - keep it that way when editing.
- Any new typology needs a generator routine in data/synthetic_generator.py
  AND a detector in pipelines/detectors/ - they are a pair.

This is the single highest-leverage thing you can do to keep Claude Code from
making assumptions that do not hold for your setup.

## Skills

The `skills/` folder in this repo ships three Claude Code skills
(transaction-anomaly, model-doc-writer, typology-research). Copy the
folder you want into your own project's skills directory and Claude Code will
pick it up automatically when the task matches. See each skill's SKILL.md
for what it does and when it triggers.

## Guardrail: Claude Code and real data

Everything in `docs/01-data-hygiene.md` applies doubly here - Claude Code can
read and write files directly, which makes it easy to point it at a real
export "just this once." Do not. Point it at `data/generated/` or
`data/sample/` only.
