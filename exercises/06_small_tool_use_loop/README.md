# Small Tool-Use Loop (Chained Calls)

## Goal

Build a manual tool-use loop with two arithmetic tools, and verify Claude
chains them in sequence to answer a question that requires both.

- Define two tools: `add(a, b)` and `multiply(a, b)`.
- Prompt: `"What is (3 + 4) * 2?"` — answering correctly requires calling
  `add` first, then feeding its result into `multiply` (a sequential
  dependency between calls, not just two independent calls in the same
  turn).
- Handle the full loop: detect `tool_use`, execute the right tool locally,
  send the result back, repeat until Claude gives a final answer.
- Verify:
  - Both tools were actually called at some point during the loop (not
    just one, and not the arithmetic done purely by the model itself).
  - The final answer text contains `"14"`.
- This exercise is a variation on exercise 01's loop, focused on a
  sequential/dependent tool-call chain rather than independent parallel
  calls — reuse what you learned there, but this one's fixture is
  arithmetic tools instead of weather/time.
