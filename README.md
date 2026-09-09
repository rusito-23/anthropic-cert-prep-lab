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

### Default model

`.env` also sets `ANTHROPIC_MODEL` (defaults to `claude-haiku-4-5`) to keep
token spend low while practicing. When writing exercise code that calls the
Messages API, read the model from this env var instead of hardcoding a model
string:

```python
import os

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5")
```

Override it for a single run when an exercise specifically needs a stronger
model:

```bash
ANTHROPIC_MODEL=claude-opus-5 uv run exercises/03_mcp_resource_server_http/server.py
```

### Linting & tests

```bash
uv run ruff check .    # lint
uv run pytest          # run tests
```

## Status

🚧 In progress — tracking hands-on practice toward Anthropic certifications.
