# Exam Simulation 02 — API Mechanics

12 questions. Note where a question says **Choose TWO**.
Mark your answers with an `X` next to the option (like round 1), then ask for grading.

---

## 1. (Applications & Integration)

You pass `stop_sequences=["</answer>"]`, and Claude's output ends right before `</answer>`. What will `stop_reason` be?

- A. `end_turn`
- B. `max_tokens`
- C. `stop_sequence` X
- D. `tool_use`

## 2. (Applications & Integration): find the bug

```python
messages = [{"role": "user", "content": "Weather in Paris and Rome?"}]

while True:
    resp = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )
    if resp.stop_reason != "tool_use":
        break

    results = []
    for block in resp.content:
        if block.type == "tool_use":
            out = run_tool(block.name, block.input)
            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": out,
                }
            )
    messages.append({"role": "user", "content": results})
```

What's wrong?

- A. `tool_use_id` should be `block.name`, not `block.id`
- B. The assistant's response (`resp.content`) is never appended to `messages` before the tool results, so the second request fails
- C. The loop should break on `stop_reason == "end_turn"` only, since other values mean an error X
- D. Each `tool_result` must be sent in its own user message

## 3. (Applications & Integration)

Your `get_weather` tool raises an exception because an external API is down. What's the best way to handle it in the loop?

- A. Stop the loop and return a generic error to the end user
- B. Skip the `tool_result` for that call and send only the successful ones
- C. Retry the same Claude request until the tool succeeds
- D. Return a `tool_result` with `is_error: true` and a short error message, so Claude can adjust (retry, try another approach, or explain) X

## 4. (Applications & Integration)

Where does the system prompt go in a Messages API request?

- A. In the top-level `system` parameter X
- B. As the first message, with `"role": "system"`
- C. As the first user message, wrapped in `<system>` tags
- D. In the `metadata` field

## 5. (Applications & Integration)

In a multi-turn chat, on the second request, Claude has no idea what the user said in the first turn. What's the most likely cause?

- A. The model's context window is too small
- B. Prompt caching was not enabled
- C. The Messages API is stateless, and the app is only sending the latest user message instead of the full conversation history X
- D. The `max_tokens` value is too low to hold the history

## 6. (Tools & MCP)

In a workflow step, Claude must call at least one of the three available tools, but it should decide which one. Which `tool_choice` do you set?

- A. `{"type": "auto"}`
- B. `{"type": "any"}` X
- C. `{"type": "tool", "name": "..."}`
- D. `{"type": "none"}`

## 7. (Applications & Integration)

Your app asks dozens of different questions about the same 80-page PDF over a day. You want to avoid re-sending the document's bytes with every request. What should you use?

- A. Base64-encode the PDF into every request
- B. Paste the extracted text into the system prompt of each request
- C. Split the PDF into images and send only the relevant page
- D. Upload it once with the Files API and reference it by `file_id` X

## 8. (Agents & Workflows)

A support app gets three distinct kinds of queries: billing, technical troubleshooting, and refund requests. Each kind needs a different specialized prompt, and simple billing questions could go to a cheaper model. Which pattern fits best?

- A. Routing X
- B. Prompt chaining
- C. Orchestrator-workers
- D. Autonomous agent

## 9. (Agents & Workflows)

You're translating marketing copy with a lot of nuance. You have clear quality criteria, and a first draft is usually improved by specific written feedback. Which pattern fits best?

- A. Routing
- B. Parallelization (sectioning)
- C. Evaluator-optimizer X
- D. Orchestrator-workers

## 10. (Agents & Workflows) — Choose TWO

When should you prefer a predefined workflow over an autonomous agent?

- A. The task has well-defined, predictable steps X
- B. The number of steps can't be known in advance 
- C. The problem is open-ended and needs the model to plan its own path
- D. You need consistency, predictable cost, and lower latency X
- E. The model needs to recover flexibly from unexpected tool results

## 11. (Model Selection & Optimization)

Before sending very large prompts, you want to know how many input tokens they'll use, so you can estimate cost and stay within the context window. What's the best approach?

- A. Estimate by dividing the character count by 4
- B. Use the token counting endpoint (`count_tokens`) with the same messages, system prompt, and tools X
- C. Send the request with `max_tokens=1` and read the usage
- D. Check the response's `stop_reason`

## 12. (Applications & Integration)

You're streaming a response in which Claude calls a tool. How does the tool's input arrive?

- A. As a complete JSON object in the `message_start` event
- B. Only after the stream ends, in a separate non-streamed request
- C. As partial JSON strings in `input_json_delta` events, which you collect until the block's `content_block_stop` event and then parse X
- D. As `text_delta` events mixed in with the normal text

---

## My answers

1. C — ✅
2. C — ❌ (correct: B)
3. D — ✅
4. A — ✅
5. C — ✅
6. B — ✅
7. D — ✅
8. A — ✅
9. C — ✅
10. A, D — ✅
11. B — ✅
12. C — ✅

**Score: 11/12**
