# MCP as a grounding layer

## The problem it solves

Pasting a 50,000-row CSV into a chat wastes context and produces worse
answers than letting the model query exactly the rows it needs. It also
means every question re-sends the whole dataset. MCP (Model Context
Protocol) lets Claude query a local file or database directly instead -
smaller context per turn, and answers grounded in an actual query result
instead of the model eyeballing a giant paste.

## Two configs shipped in mcp/

- **filesystem-mcp.md** - read/write access to a specific local folder
  (e.g. data/generated/). Useful for letting Claude Code (or Claude.ai
  via a local MCP connector) read pipeline output or write a new synthetic
  batch without you shuttling files by hand.
- **sqlite-mcp.md** - a local SQLite copy of synthetic transactions, so
  Claude can run SELECT queries (for example, all flagged structuring cases
  over 90,000 SEK in month 3) instead of you searching a CSV yourself and
  pasting the result.

## Why SQLite over "just paste the CSV"

- **Precision** - a query returns exactly the rows relevant to the question,
  not the whole table, so Claude's answer is grounded in a specific, checkable
  result rather than pattern-matching over a wall of text.
- **Cost/latency** - a targeted query is a fraction of the tokens of a full
  CSV, every single turn.
- **Auditability** - the SQL query itself is a record of what was asked and
  what was retrieved, which matters if you ever need to explain how an
  answer was derived.

## Setting it up

See mcp/claude_desktop_config.example.json for the config block, and the
two guide files for what each server needs (paths, and in SQLite's case, the
database file created by data/synthetic_generator.py --sqlite).

## Boundary

MCP file/database access should point only at synthetic data or genuinely
public reference material (e.g. the text in grounding/), for the same
reason as everything else in this repo - see docs/01-data-hygiene.md.
Pointing a filesystem MCP server at a real case-management export defeats
every safeguard in this repo in one config change.
