"""CLI script implementing a manual tool-use loop against the Messages API."""

import argparse
import json
import logging
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
KNOWN_MISSING_WEATHER = ["moon", "sun", "mars", "outer-space"]


# Tool definition


class RunToolError(Exception):
    """Raised when a tool runs into an error."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


def get_weather(location: str) -> dict:
    if location.strip().lower() in KNOWN_MISSING_WEATHER:
        raise RunToolError(message=f"The weather for the location {location} is unknown.")

    rng = random.Random(location.strip().lower())
    condition = rng.choice(["sunny", "rainy", "snowy", "cloudy"])
    temp_c = rng.randint(-5, 35)
    return {"condition": condition, "temp_c": temp_c}


def get_current_time(timezone: str) -> dict:
    hours = random.randint(0, 23)
    minutes = random.randint(0, 59)
    return {"time": f"{hours:02d}:{minutes:02d}"}


REGISTERED_TOOLS = {
    "get_weather": get_weather,
    "get_current_time": get_current_time,
}

REGISTERED_TOOL_DEFINITIONS = [
    {
        "name": "get_weather",
        "description": """
        Retrieve the current weather for given location.
        The location can be a city, state or general place.
        """,
        "input_schema": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"],
        },
    },
    {
        "name": "get_current_time",
        "description": """
        Retrieve the current time in HH:MM for the given timezone.
        """,
        "input_schema": {
            "type": "object",
            "properties": {"timezone": {"type": "string"}},
            "required": ["timezone"],
        },
    },
]


# Tool Management


def execute_tool(block: ContentBlock) -> dict:
    try:
        tool = REGISTERED_TOOLS[block.name]
        logging.debug(f"Executing tool {block.name} with input {block.input}")

        result = tool(**block.input)
        logging.debug(f"Tool execution {block.name} got output {result}")

        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": json.dumps(result),
        }
    except TypeError as err:
        logging.error(f"Tool execution {block.name} failed with {err}")
        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "is_error": True,
            "content": f"The tool {block.name} does not match provided inputs.",
        }
    except KeyError as err:
        logging.error(f"Tool execution {block.name} failed with {err}")
        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "is_error": True,
            "content": f"The tool {block.name} does not exist.",
        }
    except RunToolError as err:
        logging.error(f"Tool execution {block.name} failed with {err}")
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
        logging.debug(f"Run loop got stop_reason={response.stop_reason}")

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = process_tool_blocks(response.content)
            messages.append({"role": "user", "content": tool_results})
        else:
            return response


# Main


def main() -> None:
    # Setup logger
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="enable debug logging")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)

    # Prompt the user for input
    user_input = input("Enter your question about the weather: ")

    # Run the tool use loop until the model indicates it's done
    response = run_loop(user_input=user_input)

    # Print the response
    for block in response.content:
        if block.type == "text":
            print(block.text)


if __name__ == "__main__":
    main()
