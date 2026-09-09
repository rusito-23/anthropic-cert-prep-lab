"""Sanity check that the environment and API key are wired up correctly."""

from anthropic import Anthropic


def main() -> None:
    client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    message = client.messages.create(
        model="claude-opus-5",
        max_tokens=100,
        messages=[{"role": "user", "content": "Say hello in one short sentence."}],
    )
    for block in message.content:
        if block.type == "text":
            print(block.text)


if __name__ == "__main__":
    main()
