# MCP Server over stdio

## Goal

Build a minimal MCP server that runs over the stdio transport, exposing a
couple of tools and one resource, and prove both normal operation and
error handling work correctly through the MCP protocol.

- **Tool:** `add(a, b)` — takes two numbers and returns their sum.
- **Tool:** `divide(a, b)` — takes two numbers and returns their quotient;
  intentionally raises when given invalid input (e.g. `b=0`).
- **Resource:** one static resource (e.g. a fixed string) reachable at a
  stable URI.
- The server must run over the stdio transport (no HTTP).
- The server process must stay alive and keep responding to further
  requests after a failing call — a bad tool call must not take down the
  whole server.
- A failing call must come back as a proper MCP error response (a
  structured tool error the caller can inspect), not an uncaught
  exception/stack trace leaking through, and not a silent hang.
- Test the server by registering it as a project MCP server (see
  `.mcp.json`) and exercising it from a Claude Code session or the MCP
  Inspector — no standalone Python test client needed.

## Results

`server.py` is registered as a project MCP server via `.mcp.json` and was
exercised directly from a Claude Code session over stdio.

- **Tool:** `add(num1, num2)` (low-level `mcp.server.Server` API, not the
  README's `add(a, b)` naming).
  - `add(2, 3)` → `5`
- **Resource:** `math-ops://add/neutral`, `text/plain`.
  - Listing returns the resource with the correct URI and mime type.
  - Reading it returns clean text with no stray whitespace:
    `"The neutral of the add is 0. Because any number added to 0 returns itself."`
- **Tool:** `divide(num1, num2)` — added with a dedicated `RunToolError`
  for expected domain errors (e.g. division by zero), caught separately
  from unexpected exceptions in `call_tool` so its message can be safely
  surfaced to the caller.
  - `divide(10, 2)` → `5.0`
  - `divide(5, 0)` → structured tool error, message
    `"Division by zero is impossible"` (not a crash, not a generic
    fallback message).
  - Server stayed alive after the error: resource listing succeeded
    immediately afterward in the same session.

Tool calls (`add`, `divide`, including its error path) and resource
list/read round-tripped correctly over stdio via the MCP Inspector and
via Claude Code's MCP client.
