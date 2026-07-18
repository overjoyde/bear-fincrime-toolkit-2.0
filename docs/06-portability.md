# Portability: taking this outside Claude

Everything in profiles/, prompts/, and skills/ is written for Claude,
but almost none of it depends on anything Claude-specific. Here is the
honest mapping.

## Profiles (profiles/*.md)

A profile's "Project Instructions" block is a system prompt. It transfers
directly:

- **ChatGPT** - paste it into a Custom GPT's "Instructions" field, or a
  Project's instructions if you are using ChatGPT Projects. Attach the same
  knowledge files to the GPT's knowledge base.
- **Gemini** - paste it into a Gem's instructions field. Gemini Gems support
  attached files the same way.
- **Anything with a system-prompt field** - API-based tools, local model
  UIs (for example LM Studio, Open WebUI) all take the same block verbatim.

What does not transfer 1:1: Claude.ai's Project-level knowledge behaves
slightly differently from a Custom GPT's knowledge base or a Gem's files in
terms of how much is retrieved per turn vs. held in context. Test retrieval
quality with your synthetic data before trusting it on real workloads.

## Prompts (prompts/*.md)

These are plain single-turn prompts. They work anywhere, unchanged. The
example input/output in each file is model-agnostic - it is there to verify
the task is well-specified, not to demonstrate a Claude-only capability.

## Skills (skills/*/SKILL.md)

This is the one category that is structurally Claude Code-specific - the
SKILL.md format and auto-triggering behavior is a Claude Code feature. The
portable part is the Python underneath (pipelines/, data/): it is plain
Python with no Claude dependency at all, runnable standalone or wrapped by
whatever agent framework or IDE-integrated LLM tool you use elsewhere
(for example a custom GPT Action, a LangChain/LlamaIndex tool, a
Cursor/Windsurf custom command). Rebuild the wrapper, keep the code.

## MCP (mcp/*)

MCP is an open protocol, not Claude-specific - it is increasingly supported
by other clients too. Check your target tool's current MCP support before
assuming the config in mcp/ works unchanged; the server configs themselves
(filesystem, SQLite) are standard MCP servers usable from any MCP client.

## What does not generalize at all

grounding/eu-instruments.md and grounding/se-instruments.md are
jurisdiction- and law-specific, not model-specific - they would need
replacing (not adapting) for a different regulatory regime, same as with
Claude.
