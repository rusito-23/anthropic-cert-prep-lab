# MCP Server over stdio

## Goal

Build a minimal MCP server that runs over the stdio transport, exposing one
tool and one resource, plus a small client script to exercise it.

- **Tool:** `add(a, b)` — takes two numbers and returns their sum.
- **Resource:** one static resource (e.g. a fixed string) reachable at a
  stable URI.
- The server must run over the stdio transport (no HTTP).
- Write a small test client (`client.py`) that:
  - Connects to the server over stdio and calls the `add` tool, asserting
    the returned sum is correct for at least one example.
  - Lists the server's resources and asserts your resource's URI is
    present in the listing.
- Keep the server to exactly this one tool and one resource — this
  exercise is about getting the stdio server/client wiring right, not
  building out a larger toolset.

## Results

`client.py` was skipped. Instead, `server.py` was registered as a project
MCP server via `.mcp.json` and exercised directly from a Claude Code
session over stdio.

- **Tool:** `add(num1, num2)` (low-level `mcp.server.Server` API, not the
  README's original `add(a, b)` naming).
  - `add(2, 3)` → `5`
- **Resource:** `math-ops://add/neutral`, `text/plain`.
  - Listing returns the resource with the correct URI and mime type.
  - Reading it returns clean text with no stray whitespace:
    `"The neutral of the add is 0. Because any number added to 0 returns itself."`

Both the tool call and resource list/read round-tripped correctly over
stdio via the MCP Inspector and via Claude Code's MCP client.
