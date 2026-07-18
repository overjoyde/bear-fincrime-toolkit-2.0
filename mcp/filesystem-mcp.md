# Filesystem MCP

Gives Claude read/write access to a specific local folder - in this repo,
that means `data/generated/` (or `data/sample/`), never anything wider.

## Why

Lets Claude Code (or Claude.ai via a locally-running MCP connector) read
pipeline output, write a fresh synthetic batch, or inspect generated files
directly, without you copy-pasting file contents into the chat.

## Setup

Most MCP filesystem servers (including the reference implementation) take a
single argument: the directory they are allowed to touch. Example config
block (see `mcp/claude_desktop_config.example.json` for where this goes):

```json
{
  "mcpServers": {
    "fincrime-toolkit-data": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/absolute/path/to/fincrime-llm-toolkit/data/generated"
      ]
    }
  }
}
```

Replace the path with wherever you actually generated data - keep it scoped
to `data/generated/` or `data/sample/` specifically, not the whole repo and
never a real data directory.

## Boundary

This is only as safe as the path you give it. Pointing this at a real
case-management export or any directory containing real customer data
defeats the entire point of this toolkit - see `docs/01-data-hygiene.md`.
