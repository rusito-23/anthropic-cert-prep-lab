# Streaming Responses

## Goal

Stream a one-sentence answer to a fixed prompt (e.g. "Name the capital of
France in one sentence") using the Messages API's streaming mode, and verify
the stream actually behaves like a stream.

- Send the request in streaming mode rather than a single blocking call.
- Collect the individual streaming events/chunks as they arrive.
- Verify:
  - You received more than one streaming event/chunk before the final
    message completes (i.e. it's genuinely incremental, not one big chunk).
  - The text obtained by concatenating the chunks together is exactly equal
    to the final message's `content` (no dropped or duplicated text).
- Print both the streamed-as-it-arrives output and the final assembled
  answer.
