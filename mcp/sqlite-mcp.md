# SQLite MCP

Gives Claude query access to a local SQLite database - in this repo, the
`synthetic.db` file `data/synthetic_generator.py --sqlite` produces.

## Why

Lets Claude run targeted `SELECT` queries against synthetic transaction/
customer data instead of you pasting a full CSV into the chat every time.
See `docs/04-mcp-grounding.md` for the fuller reasoning (precision, cost,
auditability).

## Generating the database

```bash
cd data && python synthetic_generator.py --customers 500 --months 6 --out generated/ --sqlite
```

This produces `data/generated/synthetic.db` with two tables: `customers`
and `transactions` (see `data/README.md` for the schema).

## Setup

Example config block using a common SQLite MCP server implementation (see
`mcp/claude_desktop_config.example.json` for where this goes):

```json
{
  "mcpServers": {
    "fincrime-toolkit-db": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-server-sqlite-npx",
        "/absolute/path/to/fincrime-llm-toolkit/data/generated/synthetic.db"
      ]
    }
  }
}
```

Check your MCP client's current documentation for the specific SQLite
server package it recommends - several exist with slightly different
argument conventions, and this ecosystem moves quickly.

## Boundary

Only ever point this at a database built from synthetic data (this repo's
generator) or data your institution has explicitly approved for LLM-assisted
querying. A SQLite MCP connection to a real transaction database is exactly
the kind of "approved path" decision described in `docs/01-data-hygiene.md`
- not something to set up on your own initiative.
