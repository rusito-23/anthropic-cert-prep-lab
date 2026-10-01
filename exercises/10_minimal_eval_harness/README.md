# Minimal Eval Harness

## Goal

Build a small eval harness that runs a fixed set of prompt/expected-answer
pairs through the tool-use loop from exercise 07, and reports pass/fail.

- Define 5 fixed test cases, each a `(prompt, expected_substring)` pair —
  reuse or adapt exercise 07's two-tool arithmetic loop as the thing under
  test (you can vary the arithmetic expression per case).
- Run all 5 prompts through the loop, capturing each final answer.
- Grade each case by checking whether `expected_substring` appears in the
  corresponding final answer.
- Verify: assert all 5 cases pass.
- Print a pass count (e.g. `4/5 passed`) and which cases failed, so the
  harness is useful for iterating even when something doesn't pass.
- This exercise depends on exercise 07 being done first — reuse its loop
  logic rather than re-deriving it from scratch.
