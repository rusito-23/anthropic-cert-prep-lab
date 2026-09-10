# MCP Error Handling

## Goal

Extend the stdio MCP server pattern from exercise 04 with a tool that can
fail on bad input, and prove the failure is surfaced correctly through the
MCP protocol rather than crashing the server process.

- Add a `divide(a, b)` tool that intentionally raises when given invalid
  input (e.g. `b=0`).
- The server process must stay alive and keep responding to further
  requests after the failing call — a bad tool call must not take down the
  whole server.
- The client's request for the failing call must come back as a proper MCP
  error response (i.e. a structured tool error the client can inspect),
  not an uncaught exception/stack trace leaking through, and not a silent
  hang.
- Write a small test client (`client.py`) that:
  - Calls `divide` with a valid input and asserts the correct result.
  - Calls `divide` with `b=0` and asserts the response indicates an error
    rather than crashing the client or the server.
- This can be its own standalone server — it doesn't need to import or
  reuse exercise 04's code, just follow the same stdio-server shape.
