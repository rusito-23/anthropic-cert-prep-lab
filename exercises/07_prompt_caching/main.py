"""Send a large static block twice and verify prompt cache write/read usage."""

from pathlib import Path

from anthropic import Anthropic

from common.config import MAX_TOKENS, MODEL
from common.content import extract_text

TERMINATOR_SCRIPT = (Path(__file__).parent / "terminator.md").read_text()
SYSTEM_PROMPT = "You are tasked with replying information about the Terminator script."
CACHE_CONTROL = {"type": "ephemeral", "ttl": "5m"}
ASSISTANT_PROMPT = {
    "role": "assistant",
    "content": [
        {
            "type": "text",
            "text": TERMINATOR_SCRIPT,
            "cache_control": CACHE_CONTROL,
        }
    ],
}


client = Anthropic()


def ask(question):
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[
            ASSISTANT_PROMPT,
            {"role": "user", "content": question},
        ],
    )

    print(f"""
Question: {question}
Response:
{extract_text(response.content)}

{response.usage.cache_creation_input_tokens=}
{response.usage.cache_read_input_tokens=}
""")


def main() -> None:
    ask("What are the first words of the Terminator?")
    ask("What age is Reese?")


if __name__ == "__main__":
    main()
