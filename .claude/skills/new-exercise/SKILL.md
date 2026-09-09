---
name: new-exercise
description: Scaffold a new numbered exercise folder under exercises/ in this repo — a README describing the task and stub file(s) with only common env/client boilerplate (no exercise-specific implementation code). Use when the user wants to start a new certification-prep exercise (e.g. "new exercise: MCP resource server over HTTP", "scaffold an exercise for the Messages API").
arguments: [topic]
---

# New Exercise Scaffold

This repo is for hands-on Anthropic certification practice. The person using it
is writing every line of exercise code themselves on purpose, to learn how things
work under the hood. **Never write implementation logic, solution code, hints
disguised as comments, or pseudocode for the exercise itself.** Your only job
here is to create structure: a folder, a README stating the goal, and empty
stub files.

## Steps

1. **Determine the topic.** Use `$topic` if provided. Otherwise ask the user
   in one short question what the exercise is about (e.g. "MCP tool server
   over stdio", "playground script for the Messages API", "resource MCP
   server over HTTP").

2. **Find the next number.** List existing folders under `exercises/` and take
   the highest `NN_` prefix + 1, zero-padded to 2 digits (e.g. `01`, `02`,
   ... `10`). Slugify the topic into `snake_case` for the folder name:
   `exercises/<NN>_<slug>/`.

3. **Decide stub filenames** based on the topic — don't overthink this, just
   pick sensible entry-point names:
   - A single script/playground exercise (e.g. Messages API experiments) →
     `main.py`
   - An MCP server exercise → `server.py`
   - An MCP server exercise that benefits from a companion test client (e.g.
     to exercise it manually) → `server.py` + `client.py`
   - If genuinely unclear, ask rather than guessing.

   Every stub file gets a one-line module docstring naming its purpose.
   Beyond that, the amount of boilerplate depends on the file's role:

   - **`main.py`** (Messages API playground scripts): also include the
     common environment/client setup every exercise in this repo repeats —
     `load_dotenv()`, the `Anthropic()` client, and the `ANTHROPIC_MODEL` /
     `ANTHROPIC_MAX_TOKENS` env-var constants, plus an empty `main()` and
     `if __name__ == "__main__":` guard. Match the shape used in
     `exercises/00_hello_claude/main.py`:

     ```python
     """<one-line purpose>."""

     import os

     from anthropic import Anthropic
     from dotenv import load_dotenv

     load_dotenv()

     MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5")
     MAX_TOKENS = int(os.environ.get("ANTHROPIC_MAX_TOKENS", "1024"))


     def main() -> None:
         client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment


     if __name__ == "__main__":
         main()
     ```

     This is wiring, not solution code — leave `main()`'s body otherwise
     empty. Never add the tool schemas, message content, request/response
     handling, or any other logic specific to the exercise itself.

   - **`server.py` / `client.py`** (MCP exercises): only the one-line
     docstring — no imports, no `if __name__ == "__main__"`, no
     class/function skeletons, no step-by-step comments. There's no
     established common setup for these yet, so the blank page stays the
     point until a pattern emerges.

4. **Write `exercises/<NN>_<slug>/README.md`** with:
   - A one-line title
   - A short "Goal" section: what the exercise should accomplish, described
     at the level of a spec/requirements list — not an implementation guide.
     Keep it to what a certification exercise would ask for: the desired
     behavior and any constraints (e.g. "must run over stdio and expose at
     least one tool", "must serve at least one resource with a stable URI").
   - Do **not** include: code snippets, library-specific API calls, an
     implementation walkthrough, or links to solutions. Reference official
     docs by name only if useful (e.g. "see the MCP spec for resource URIs")
     — no code from them.

5. **Report back** with the created path(s) and a one-sentence summary of the
   goal. Do not open, edit, or suggest edits to the stub files beyond creation
   — the user writes the content.

## Example

Input: "MCP resource server over HTTP"

Creates:
```
exercises/03_mcp_resource_server_http/
├── README.md
└── server.py
```

`server.py` contains only:
```python
"""MCP resource server exposing resources over Streamable HTTP."""
```

`README.md` contains a title, a Goal section describing what resources to
expose and that it must run over the Streamable HTTP transport — and nothing
else.
