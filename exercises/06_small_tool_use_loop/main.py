"""Tool-use loop with add and multiply tools chained to answer an arithmetic question."""

from anthropic import Anthropic

from common.config import MAX_TOKENS, MODEL  # noqa: F401


def main() -> None:
    client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment  # noqa: F841


if __name__ == "__main__":
    main()
