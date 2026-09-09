"""Sanity check that the environment and API key are wired up correctly."""

import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5")
MAX_TOKENS = int(os.environ.get("ANTHROPIC_MAX_TOKENS", "1024"))


def main() -> None:
    client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": "Say hello in one short sentence."}],
    )
    for block in message.content:
        if block.type == "text":
            print(block.text)


if __name__ == "__main__":
    main()
