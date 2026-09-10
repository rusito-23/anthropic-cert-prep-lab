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
