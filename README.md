# Anthropic Cert Prep Lab

A workspace for hands-on exercises while preparing for Anthropic/Claude certifications.

## Starting fresh

`main` contains my solutions. To work through the exercises yourself, use the
[`starter`](https://github.com/rusito-23/anthropic-cert-prep-lab/tree/starter)
branch — same exercises, READMEs, and setup, but with every solution reset to
its stub and the exam simulation answers cleared:

```bash
git clone -b starter --single-branch https://github.com/rusito-23/anthropic-cert-prep-lab.git
```

## Structure

```
exercises/   # standalone practice exercises, one folder per exercise
notes/       # study notes, gotchas, reference material
```

## Setup

```bash
uv sync
cp .env.example .env   # fill in your ANTHROPIC_API_KEY
```

(`.env` is gitignored — this repo is public, never commit real keys.)

## Run

```bash
uv run exercises/00_hello_claude/main.py
```

## Linting & tests

```bash
uv run ruff check .
uv run pytest
```

## Status

🚧 In progress — tracking hands-on practice toward Anthropic certifications.
