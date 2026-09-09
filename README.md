# Anthropic Cert Prep Lab

A workspace for hands-on exercises while preparing for Anthropic/Claude certifications.

## Structure

```
exercises/   # standalone practice exercises, one folder per exercise
notes/       # study notes, gotchas, reference material
```

## Python setup

This repo uses [`uv`](https://github.com/astral-sh/uv) to manage the Python version and dependencies — no `pyenv` or `virtualenvwrapper` needed.

Install `uv` once (macOS):

```bash
brew install uv
```

Then, from the repo root:

```bash
uv sync              # creates .venv/ and installs dependencies, pinned in uv.lock
```

Run an exercise:

```bash
uv run exercises/00_hello_claude/main.py
```

`uv run` automatically uses the project's `.venv` — no manual activation needed. If you prefer an activated shell:

```bash
source .venv/bin/activate
python exercises/00_hello_claude/main.py
```

### Adding dependencies

```bash
uv add <package>          # runtime dependency
uv add --dev <package>    # dev-only dependency (linting, testing, etc.)
```

This updates `pyproject.toml` and `uv.lock` automatically — commit both.

### Anthropic API key

Copy `.env.example` to `.env` and fill in your key:

```bash
cp .env.example .env
```

Load it into your shell before running exercises:

```bash
export $(cat .env | xargs)
```

(`.env` is gitignored — never commit real API keys.)

### Linting & tests

```bash
uv run ruff check .    # lint
uv run pytest          # run tests
```

## Status

🚧 In progress — tracking hands-on practice toward Anthropic certifications.
