# Structured Output

## Goal

Extract structured data from free text using a JSON schema, and verify the
parsed result matches expectations exactly.

- Prompt: `"Extract name and age from: 'John is 34 years old.'"`
- Define a JSON schema describing the desired output shape:
  `{name: string, age: integer}`.
- Constrain the response to that schema (structured outputs), rather than
  asking Claude to "please return JSON" in prose and hoping for the best.
- Verify:
  - The response can be parsed with `json.loads()` without error.
  - The parsed object has `name == "John"` and `age == 34`.
- Keep this to the one fixed example — the point is getting the schema and
  request shape right, not building a general extraction pipeline.
