# Tool Use Loop from Scratch

## Goal

Build a small CLI script that lets Claude answer questions by calling
locally-defined tools, using only raw Messages API calls — no MCP, no SDK
agent/tool-runner helpers.

- Define a `get_weather(location: str)` tool with a proper JSON schema, that
  returns a hardcoded/fake temperature (no real weather API needed).
- Send a user message such as "What's the weather in Tokyo and should I
  bring a jacket?"
- Handle the response: check whether `stop_reason == "tool_use"`, and
  extract the tool call name and input.
- Execute the corresponding fake tool function locally, then send a
  follow-up request that includes the tool result, using the full
  conversation history (not just the result on its own).
- Print Claude's final natural-language answer.
- Once that works end-to-end, add a second tool, e.g.
  `get_current_time(timezone: str)`, and ask a question that requires both
  tools — this forces handling multiple `tool_use` blocks within a single
  response.
