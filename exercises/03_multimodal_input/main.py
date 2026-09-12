"""Send a local image plus a yes/no question to Claude and check the answer."""

import argparse
import base64
import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5")
MAX_TOKENS = int(os.environ.get("ANTHROPIC_MAX_TOKENS", "1024"))


# Main


def main() -> None:
    # Determine which image to load
    parser = argparse.ArgumentParser()
    parser.add_argument("--no_cat", action="store_true", help="Use the no-cat image")
    args = parser.parse_args()
    image_name = "no_cat.jpg" if args.no_cat else "cat.jpg"

    # Load image in base64
    image_path = Path(__file__).parent / image_name
    image_bytes = image_path.read_bytes()
    image = base64.b64encode(image_bytes).decode("utf-8")

    # Create system prompts
    system_prompt = """
    You are a cat image detector. Determine if each image has a cat or not.
    Reply only with "yes" or "no".

    <sample_input> Is there a cat?</sample_input>
    <ideal_output>yes</ideal_output>

    <sample_input> Does this image have a cat?</sample_input>
    <ideal_output>no</ideal_output>
    """

    # Create user prompts
    user_prompt = {
        "role": "user",
        "content": [
            {"type": "text", "text": "Cat or not cat?"},
            {
                "type": "image",
                "source": {"type": "base64", "media_type": "image/jpeg", "data": image},
            },
        ],
    }

    # Run the prompt
    client = Anthropic()
    response = client.messages.create(
        model=MODEL, max_tokens=MAX_TOKENS, system=system_prompt, messages=[user_prompt]
    )

    # Assemble response text
    response_text = "".join([block.text for block in response.content if block.type == "text"])

    # Verify response
    print(response_text)
    if args.no_cat and response_text != "no":
        raise RuntimeError("The model wrongly identified a cat in the image of a dog.")
    elif not args.no_cat and response_text != "yes":
        raise RuntimeError("The model didn't identified the cat in the image.")


if __name__ == "__main__":
    main()
