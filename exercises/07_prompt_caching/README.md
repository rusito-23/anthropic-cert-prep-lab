# Prompt Caching

## Goal

Send the same large static block of context twice, and verify the prompt
cache actually gets written on the first call and read on the second.

- Prepare a static block of text roughly 2000 tokens long (e.g. a chunk of
  fixed reference text) that doesn't change between calls.
- Enable prompt caching on that block.
- Make two requests, back to back, with identical static content — only
  something trivial can differ (e.g. the user's question), and it must not
  appear before the cached block in the request.
- Verify:
  - On the first call, `usage.cache_creation_input_tokens > 0`.
  - On the second call, `usage.cache_read_input_tokens > 0`.
- Print both calls' usage objects so you can see the before/after
  difference directly, not just the assertions passing.
