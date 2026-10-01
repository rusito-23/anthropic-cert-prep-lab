# Exam Simulation 03 — Full Review

24 questions. Note where a question says **Choose TWO**.
Mark your answers with an `X` next to the option, then ask for grading.

---

## 1. (Applications & Integration)

You want Claude to describe a PNG screenshot. How do you send it?

- A. Put the image URL in the system prompt
- B. Paste the base64 string inside a text block
- C. In the user message's content list, include an image block (`"source": {"type": "base64", "media_type": "image/png", "data": ...}`) along with a text block that holds the question X
- D. Images can only be sent inside `tool_result` blocks

## 2. (Prompt & Context Engineering)

Your prompt mixes a long contract with instructions for analyzing it. Claude sometimes treats contract clauses as instructions. What's the best fix?

- A. Wrap the contract in XML tags such as `<contract>...</contract>` and refer to it by tag in the instructions X
- B. Put the instructions in all caps
- C. Lower the temperature
- D. Move the contract into a tool description

## 3. (Model Selection & Optimization)

You're building an inline code-completion feature in an IDE. It runs on every few keystrokes, has very high volume, and needs very low latency. Which model choice fits best?

- A. The most capable model, with extended thinking
- B. A mid-tier model through the Message Batches API
- C. The most capable model, with streaming
- D. The smallest, fastest model that meets your quality bar on an eval set X

## 4. (Applications & Integration)

During traffic spikes, your app gets 429 `rate_limit_error` responses. What's the best way to handle them?

- A. Retry immediately in a tight loop until the request succeeds
- B. Retry with exponential backoff and jitter, honoring the `retry-after` header when it's present X
- C. Switch to a larger model
- D. Reduce `max_tokens` on every request

## 5. (Security & Safety)

A single-page React app calls the Anthropic API directly from the browser with your API key. What's the right fix?

- A. Obfuscate the key inside the minified JavaScript bundle
- B. Store the key in the browser's localStorage instead
- C. Embed a key with low spending limits
- D. Route calls through your own backend, which keeps the key server-side and authenticates your users X

## 6. (Applications & Integration) — Choose TWO

Which errors should your client generally retry?

- A. 400 `invalid_request_error`
- B. 429 `rate_limit_error` X
- C. 401 `authentication_error`
- D. 529 `overloaded_error` X
- E. 413 `request_too_large`

## 7. (Agents & Workflows)

A chatbot must screen every user message for policy violations without adding latency to its normal answers. Which pattern fits best?

- A. Prompt chaining: screen the message first, then answer
- B. Parallelization (sectioning): one call generates the answer while another screens the input at the same time X
- C. Routing
- D. Evaluator-optimizer

## 8. (Tools & MCP)

Your MCP server should offer a reusable "summarize incident" template that users explicitly choose, for example as a slash command. Which MCP primitive fits?

- A. Tool
- B. Resource
- C. Prompt X
- D. Sampling

## 9. (Applications & Integration)

You force a tool with `tool_choice: {"type": "tool", "name": "record_invoice"}` to get structured data. Where is the structured data in the response?

- A. In the `input` field of the `tool_use` content block X
- B. In the first text block, as a JSON string
- C. In `stop_reason`
- D. You have to execute the tool and read the data from the `tool_result`

## 10. (Model Selection & Optimization)

You put a `cache_control` breakpoint on the last system prompt block. Your app builds the `tools` array in a different order on each request, and the cache hit rate is zero. Why?

- A. Prompt caching doesn't support requests that include tools
- B. Tools come before the system prompt in the cached prefix, so any change to the tools invalidates the cache for everything after them X
- C. The system prompt must be under 1,024 tokens to be cached
- D. `cache_control` has to be placed on a user message

## 11. (Eval, Testing & Debugging)

You've rewritten a production prompt. What's the most reliable way to check that it didn't make things worse?

- A. Try a handful of queries by hand and compare them
- B. Ship the new prompt and monitor user complaints
- C. Ask Claude to rate whether the new prompt is better
- D. Run a fixed eval set of representative cases with automated grading, and compare the results to the old prompt's baseline before shipping X

## 12. (Applications & Integration)

Claude sometimes calls `create_order` and `charge_payment` in the same turn, but `charge_payment` needs the order ID that `create_order` returns. What's the most direct fix?

- A. Set `tool_choice` to `none`
- B. Remove `charge_payment`
- C. Set `disable_parallel_tool_use: true` in `tool_choice`, so Claude calls at most one tool per turn X
- D. Increase `max_tokens`

## 13. (Prompt & Context Engineering)

You're sending a 60k-token document plus a question about it. Where should the parts go for the best results?

- A. Instructions and question first, the document at the end
- B. The document at the top, and the instructions and question at the end
- C. Split the document between the system prompt and the user message X
- D. It makes no difference

## 14. (Agents & Workflows)

An autonomous agent sometimes gets stuck calling the same tools over and over, and runs up large bills. What's the best safeguard?

- A. Set stopping conditions, such as a maximum number of iterations or a token budget, and add checkpoints where a human can review X
- B. Use a model with a larger context window
- C. Lower the temperature
- D. Remove the tools after the first call

## 15. (Security & Safety) — Choose TWO

An agent answers analytics questions by running SQL through a `run_query` tool. How do you limit the damage it could do?

- A. Give it admin credentials so queries never fail
- B. Give it read-only database credentials scoped to only the tables it needs X
- C. Tell it in the system prompt never to run DELETE or DROP
- D. Put the connection string in the system prompt so the agent can manage connections
- E. Validate or allowlist queries in the tool's server-side code before running them X

## 16. (Applications & Integration)

You submit 10,000 requests through the Message Batches API. How do you match each result to its original request?

- A. Results come back in the order you submitted them
- B. Results are sorted by completion timestamp
- C. Only successful results are returned, so their positions match the successful inputs
- D. Match each result to its request by the `custom_id` you assigned, since the order isn't guaranteed X

## 17. (Model Selection & Optimization) — Choose TWO

A live customer chatbot sends the same 30k-token system prompt with every request. You need to cut costs.

- A. Enable prompt caching on the system prompt X
- B. Move the live chat to the Message Batches API
- C. Route simple queries to a smaller model, where evals show the quality holds up X
- D. Send the system prompt only on the first turn of each conversation
- E. Raise the temperature to shorten responses

## 18. (Claude Code)

Your team wants Claude Code to never run `rm -rf` or read `.env` files in your repo, and the rule should apply to everyone. What should you use?

- A. Add "Never run rm -rf or read .env" to CLAUDE.md
- B. Add deny rules to the project's `.claude/settings.json` and commit it to the repo X
- C. Add a user-scoped MCP server
- D. Add `.env` to `.gitignore`

## 19. (Applications & Integration): find the bug

```python
resp = client.messages.create(model=..., max_tokens=1024, tools=tools, messages=messages)
answer = resp.content[0].text
```

This code sometimes raises an `AttributeError`. Why?

- A. `resp.content` is a list of blocks of different types, and the first block isn't always a text block (it can be a `tool_use` or `thinking` block, for example). Iterate over the blocks and pick the ones with `type == "text"`. X
- B. Text is only available in `resp.text`
- C. The API returns a plain string when the response is short
- D. `content` is only filled in when `stop_reason` is `end_turn`

## 20. (Agents & Workflows)

A research agent hands broad searches to subagents. What's the main architectural benefit?

- A. The subagents share one context window, so they work faster
- B. Subagents remove the need for tools
- C. Each subagent explores in its own clean context and returns a condensed result, which keeps the orchestrator's context focused X
- D. Multi-agent setups always use fewer total tokens

## 21. (Tools & MCP)

You're deploying one MCP server for many users to reach over the network. Which transport fits?

- A. Streamable HTTP X
- B. stdio
- C. A project-scoped `.mcp.json`
- D. MCP only supports local servers

## 22. (Applications & Integration)

How can you confirm that prompt caching is actually working on a request?

- A. `stop_reason` will be `"cached"`
- B. Check `usage.cache_read_input_tokens` in the response; if it's above zero, part of the prompt was read from the cache X
- C. Look for an `x-cache: HIT` response header
- D. The number of output tokens goes down

## 23. (Prompt & Context Engineering)

Claude's output format varies from call to call, even though your instructions describe the format clearly. What's usually the most effective fix?

- A. Write "MUST" in capital letters in the format instructions
- B. Raise the temperature
- C. Make the format description longer
- D. Add 3–5 varied examples of the exact output format, wrapped in `<example>` tags X

## 24. (Model Selection & Optimization)

You need a one-off, complex refactoring plan for a large legacy codebase. Accuracy matters most, and cost is secondary. Which choice fits best?

- A. The smallest model, with several retries
- B. A small model through the Message Batches API
- C. The most capable model, optionally with extended thinking X
- D. A mid-tier model with a lower `max_tokens`

---

## My answers

