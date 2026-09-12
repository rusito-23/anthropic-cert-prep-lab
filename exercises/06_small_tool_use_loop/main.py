"""Tool-use loop with add and multiply tools chained to answer an arithmetic question."""

import argparse
import json
import logging
from collections.abc import Iterable

from anthropic import Anthropic
from anthropic.types import ContentBlock

from common.config import MAX_TOKENS, MODEL
from common.content import extract_text
from common.logger import add_verbosity_argument, configure_logging

# Constants


logger = logging.getLogger(__name__)


# Tool definition


class RunToolError(Exception):
    """Raised when a tool runs into an error."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


add_called = False
multiply_called = False


def add(num1: int, num2: int) -> int:
    global add_called
    add_called = True
    return num1 + num2


def multiply(num1: int, num2: int) -> int:
    global multiply_called
    multiply_called = True
    return num1 * num2


REGISTERED_TOOLS = {
    "add": add,
    "multiply": multiply,
}

REGISTERED_TOOL_DEFINITIONS = [
    {
        "name": "add",
        "description": "Returns the addition of the two integers.",
        "input_schema": {
            "type": "object",
            "properties": {"num1": {"type": "integer"}, "num2": {"type": "integer"}},
            "required": ["num1", "num2"],
        },
    },
    {
        "name": "multiply",
        "description": "Returns the result of multiplying the two given integers.",
        "input_schema": {
            "type": "object",
            "properties": {"num1": {"type": "integer"}, "num2": {"type": "integer"}},
            "required": ["num1", "num2"],
        },
    },
]


# Tool Management


def execute_tool(block: ContentBlock) -> dict:
    try:
        tool = REGISTERED_TOOLS[block.name]
        logger.debug(f"Executing tool {block.name} with input {block.input}")

        result = tool(**block.input)
        logger.debug(f"Tool execution {block.name} got output {result}")

        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": json.dumps(result),
        }
    except TypeError as err:
        logger.error(f"Tool execution {block.name} failed with {err}")
        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "is_error": True,
            "content": f"The tool {block.name} does not match provided inputs.",
        }
    except KeyError as err:
        logger.error(f"Tool execution {block.name} failed with {err}")
        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "is_error": True,
            "content": f"The tool {block.name} does not exist.",
        }
    except RunToolError as err:
        logger.error(f"Tool execution {block.name} failed with {err}")
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

    # Create system prompt
    system = """
    Perform the math operation asked by the user. Return only the number.
    Leverage the registered math tools.

    <sample_input>What is 2 + 2?</sample_input>
    <ideal_output>4</ideal_output>

    <sample_input>What is 2 + (2 * 2)?</sample_input>
    <ideal_output>6</ideal_output>
    """

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=messages,
            system=system,
            tools=REGISTERED_TOOL_DEFINITIONS,
        )
        logger.debug(f"Run loop got stop_reason={response.stop_reason}")

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
    add_verbosity_argument(parser)
    args = parser.parse_args()
    configure_logging(args.verbose)

    # Run the tool use loop until the model indicates it's done
    response = run_loop("What is (3 + 4) * 2?")

    # Print the response
    result = extract_text(response.content)
    if result != "14":
        raise RuntimeError(f"Wrong result: {result}, expected '14'")

    if not add_called:
        raise RuntimeError("Did not call the expected tool `add`.")

    if not multiply_called:
        raise RuntimeError("Did not call the expected tool `multiply`.")

    print(f"Final result: {result}")


if __name__ == "__main__":
    main()
