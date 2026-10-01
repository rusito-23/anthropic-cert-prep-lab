# Multimodal Input

## Goal

Send a small local image alongside a yes/no question, and check that
Claude's answer matches a known, hardcoded expectation.

- Pick (or add to this folder) one small local image where the correct
  answer to "Is there a cat in this image? Answer yes or no." is known in
  advance — you'll hardcode the expected answer, so the image choice
  matters.
- Send the image plus the question in a single request.
- Constrain the prompt so Claude answers with just "yes" or "no" — no
  extra sentence.
- Verify: assert the response text is exactly `"yes"` or `"no"` (case as
  you define it) and matches the expected answer for your chosen image.
- Note: this is testing the multimodal request shape (how to attach local
  image bytes to a message), not building a vision pipeline — keep it to a
  single request/response.
