"""Run a small fixed prompt/expected-substring eval set through the exercise 07 loop."""

from anthropic import Anthropic

from common.config import MAX_TOKENS, MODEL  # noqa: F401


def main() -> None:
    client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment  # noqa: F841


if __name__ == "__main__":
    main()
