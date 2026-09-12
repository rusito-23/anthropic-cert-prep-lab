"""Extract structured name/age fields from text using a JSON schema."""

import argparse
import json
import logging

from anthropic import Anthropic

from common.config import MAX_TOKENS, MODEL
from common.content import extract_text
from common.logger import add_verbosity_argument, configure_logging

logger = logging.getLogger(__name__)


def main() -> None:
    # Setup logger
    parser = argparse.ArgumentParser()
    add_verbosity_argument(parser)
    args = parser.parse_args()
    configure_logging(args.verbose)

    # Determine constants
    prompt = "Extract name and age from: 'John is 34 years old.'"
    expected_name = "John"
    expected_age = 34

    # Make request
    client = Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
        output_config={
            "format": {
                "type": "json_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                    },
                    "required": ["name", "age"],
                    "additionalProperties": False,
                },
            }
        },
    )

    text_result = extract_text(response.content)
    logger.debug(f"Result: {text_result}")
    result = json.loads(text_result)

    if not result:
        logger.error(f"Invalid JSON result: {text_result}")
        exit(1)

    name = result.get("name")
    age = result.get("age")
    if not name or not age:
        raise RuntimeError(f"JSON result missing properties: {result}")

    if name != expected_name:
        raise RuntimeError(f"Expected name to be {expected_name} but got {name} instead")

    if age != expected_age:
        raise RuntimeError(f"Expected age to be {expected_age} but got {age} instead")

    logger.info("All checks passed successfully.")


if __name__ == "__main__":
    main()
