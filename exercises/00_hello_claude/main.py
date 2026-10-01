"""Sanity check that the environment and API key are wired up correctly."""

from anthropic import Anthropic

from common.config import MAX_TOKENS, MODEL
from common.content import extract_text


def main() -> None:
    client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": "Say hello in one short sentence."}],
    )
    print(extract_text(message.content))


if __name__ == "__main__":
    main()
