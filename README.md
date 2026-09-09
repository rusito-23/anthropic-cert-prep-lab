# Anthropic Cert Prep Lab

A workspace for hands-on exercises while preparing for Anthropic/Claude certifications.

## Structure

```
exercises/   # standalone practice exercises, one folder per exercise
notes/       # study notes, gotchas, reference material
```

## Python setup

This repo uses [`uv`](https://github.com/astral-sh/uv) to manage the Python version and dependencies.

```bash
uv sync
```

Run an exercise:

```bash
uv run exercises/00_hello_claude/main.py
```

### Anthropic API key

Copy `.env.example` to `.env` and fill in your key:

```bash
cp .env.example .env
```

(`.env` is gitignored — never commit real API keys.)

Exercise scripts load `.env` automatically via [`python-dotenv`](https://pypi.org/project/python-dotenv/) —
no manual export step, and no re-loading needed in new shells. At the top of
each script that calls the API:

```python
from dotenv import load_dotenv

load_dotenv()
```

### Default model

`.env` also sets `ANTHROPIC_MODEL` (defaults to `claude-haiku-4-5`) to keep
token spend low while practicing. When writing exercise code that calls the
Messages API, read the model from this env var instead of hardcoding a model
string:

```python
import os

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5")
```

### Linting & tests

```bash
uv run ruff check .    # lint
uv run pytest          # run tests
```

## Status

🚧 In progress — tracking hands-on practice toward Anthropic certifications.
