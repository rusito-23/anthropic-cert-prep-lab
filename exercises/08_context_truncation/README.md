# Context Truncation

## Goal

Implement a truncation function that keeps a simulated conversation history
under a fixed token budget, and verify it behaves correctly.

- Simulate a conversation of 10 short fake turns (alternating user/assistant
  messages is fine — the content just needs to be plausible-looking text,
  it doesn't need to come from a real API call).
- Pick a token budget that the full 10-turn history exceeds (e.g. 500
  tokens) — you'll need a way to measure token counts for your fake turns.
- Implement a function that truncates the history down to fit under that
  budget.
- Verify:
  - The truncated history's token count is under the budget.
  - The truncated history still contains the most recent turn (i.e.
    truncation drops from the oldest end, not the newest).
- Decide and document your own truncation strategy (e.g. drop oldest turns
  one at a time, keep whole turns rather than cutting mid-turn) — the
  exercise doesn't prescribe one, but be consistent and explain the
  tradeoff you picked.
