"""CLI script implementing a manual tool-use loop against the Messages API."""

import json
import os
import random
from collections.abc import Iterable

from anthropic import Anthropic
from anthropic.types import ContentBlock
from dotenv import load_dotenv

# Constants


load_dotenv()

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5")
MAX_TOKENS = int(os.environ.get("ANTHROPIC_MAX_TOKENS", "1024"))


FAKE_WEATHER = {
    "tokyo": {"condition": "rainy", "temp_c": 14},
    "san francisco": {"condition": "foggy", "temp_c": 12},
    "cairo": {"condition": "sunny", "temp_c": 34},
}

KNOWN_MISSING_WHEATHER = ["moon", "sun", "mars", "outer-space"]


# Tool definition


class RunToolError(Exception):
    """Raised when a tool runs into an error."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


def get_wheather(location: str) -> dict:
    known = FAKE_WEATHER.get(location.strip().lower())
    if known is not None:
        return known

    if location.strip().lower() in KNOWN_MISSING_WHEATHER:
        raise RunToolError(message=f"The wheather for the location {location} is unknown.")

    rng = random.Random(location.strip().lower())
    condition = rng.choice(["sunny", "rainy", "snowy", "cloudy"])
    temp_c = rng.randint(-5, 35)
    return {"condition": condition, "temp_c": temp_c}


REGISTERED_TOOLS = {"get_wheather": get_wheather}

REGISTERED_TOOL_DEFINITIONS = [
    {
        "name": "get_wheather",
        "description": """
        Retrieve the current wheather for given location.
        The location can be a city, state or general place.
        """,
        "input_schema": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"],
        },
    }
]


# Tool Management


def execute_tool(block: ContentBlock) -> dict:
    try:
        tool = REGISTERED_TOOLS[block.name]
        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": json.dumps(tool(**block.input)),
        }
    except TypeError:
        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "is_error": True,
            "content": f"The tool {block.name} does not match provided inputs.",
        }
    except KeyError:
        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "is_error": True,
            "content": f"The tool {block.name} does not exist.",
        }
    except RunToolError as err:
        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "is_error": True,
            "content": err.message,
        }


def process_tool_blocks(blocks: Iterable[ContentBlock]) -> Iterable[dict]:
    tool_results = []
    for block in blocks:
        if block.type == "tool_use":
            result = execute_tool(block)
            tool_results.append(result)
    return tool_results


# Loop Management


def run_loop(user_input: str):
    # Create client and messages
    client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    messages = [{"role": "user", "content": user_input}]

    while True:
        response = client.messages.create(
            model=MODEL, max_tokens=MAX_TOKENS, messages=messages, tools=REGISTERED_TOOL_DEFINITIONS
        )

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = process_tool_blocks(response.content)
            messages.append({"role": "user", "content": tool_results})
        else:
            return response


# Main


def main() -> None:
    # Prompt the user for input
    user_input = input("Enter your question about the wheather: ")

    # Run the tool use loop until the model indicates it's done
    response = run_loop(user_input=user_input)

    # Print the response
    for block in response.content:
        if block.type == "text":
            print(block.text)


if __name__ == "__main__":
    main()
