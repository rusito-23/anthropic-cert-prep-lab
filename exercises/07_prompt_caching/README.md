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

## Result

```
Question: What are the first words of the Terminator?
Response:
# The Terminator's First Words

According to the script provided, the Terminator's first words appear in Scene 3, when he encounters the youth gang members in the playground. When the gang leader asks him what's wrong, the Terminator responds:

**"Nice night for a walk."**

This is a simple, emotionless repetition of what the gang leader had just said to him. It's one of the earliest instances that demonstrates the Terminator's mechanical nature and his ability to mimic human speech patterns while lacking genuine understanding or emotion.

response.usage.cache_creation_input_tokens=36065
response.usage.cache_read_input_tokens=0


Question: What age is Reese?
Response:
According to the script, Kyle Reese is **22 years old**.

This is stated in Scene 5: "KYLE REESE is 22, but his face has been aged by ordeal, the mouth hard, eyes grim."

response.usage.cache_creation_input_tokens=0
response.usage.cache_read_input_tokens=36065
```
