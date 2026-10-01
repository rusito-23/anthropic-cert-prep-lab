"""Verify Claude doesn't follow instructions injected into a tool result."""

from anthropic import Anthropic

from common.config import MAX_TOKENS, MODEL  # noqa: F401


def main() -> None:
    client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment  # noqa: F841


if __name__ == "__main__":
    main()
