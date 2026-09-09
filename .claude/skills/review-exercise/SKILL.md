---
name: review-exercise
description: Review a completed exercise under exercises/ against its README goal — correctness, spec compliance, and best practices. Feedback only, never edits code. Use when the user wants their exercise checked, reviewed, or graded (e.g. "review exercise 2", "check my MCP server", "is this correct").
arguments: [exercise]
---

# Review Exercise

The person using this repo is writing every line of exercise code themselves,
on purpose, to learn how things work under the hood. **This skill never edits,
patches, or rewrites their code — feedback only.** If they want a fix applied,
that's a separate, explicit ask outside this skill; don't offer to do it here
beyond naming what's wrong and why.

## Steps

1. **Identify the exercise.** Use `$exercise` if given (a number like `2` or
   `02`, or a folder name). Otherwise list the folders under `exercises/` and
   ask which one to review.

2. **Read the spec.** Read that exercise's `README.md` in full — this is the
   ground truth for what "correct" means here. Don't hold the code to
   requirements the README never asked for.

3. **Read all the code** in the exercise folder.

4. **Check currency before judging API usage.** If the exercise touches the
   Claude Messages API, invoke the `claude-api` skill first and use it to
   verify model IDs, parameter shapes, and idioms — API details drift and
   your training data can be stale. If the exercise is an MCP server
   (stdio or HTTP), check the code against the MCP specification and the
   installed `mcp` Python SDK's actual API (e.g. via `python -c "import mcp; help(...)"`
   or reading the installed package source) rather than recalled patterns —
   the SDK surface has changed across versions.

5. **Evaluate and report**, grouped into:
   - **Correctness** — bugs, protocol/spec violations, things that would
     fail at runtime or fail a grader. Cite the file and line.
   - **Gaps vs. the README** — requirements stated in the README that the
     code doesn't meet yet.
   - **Best practices** — idiomatic usage, error handling, resource cleanup,
     things a certification exam would expect even if not strictly required
     by the README.
   - **Nitpicks** — minor style points, only if nothing more substantive was
     found worth mentioning.

   Skip any category with nothing to say — don't pad the report. If everything
   checks out, say so plainly rather than manufacturing nitpicks.

6. **End with a one-line summary verdict** (e.g. "Meets the goal, one
   correctness issue to fix" / "Not yet meeting the goal — see Correctness").
   Do not apply any fix yourself, and do not open Edit/Write on the exercise
   files during this review.
