"""Stream a one-sentence answer from the Messages API and verify the chunks."""

from anthropic import Anthropic
from anthropic.types import MessageStreamEvent

from common.config import MAX_TOKENS, MODEL

# Block definitions


class ContentBlock:
    def __init__(self, event: MessageStreamEvent):
        self.index = event.index
        self.text = ""
        self.delta_count = 0

    def apply_delta(self, event: MessageStreamEvent):
        self.text += event.delta.text
        self.delta_count += 1


class ContentBlocks:
    def __init__(self):
        self._blocks = {}

    def init_block(self, event: MessageStreamEvent):
        block = ContentBlock(event=event)
        self._blocks[event.index] = block

    def apply_delta(self, event: MessageStreamEvent):
        self._blocks[event.index].apply_delta(event)

    def assemble(self) -> str:
        return "".join([block.text for block in self._blocks.values()])

    def verify_delta(self) -> bool:
        return all([block.delta_count > 0 for block in self._blocks.values()])


# Main


def main() -> None:
    client = Anthropic()

    # Define initial message:
    initial_message = {"role": "user", "content": "List the last 5 Argentinian Presidents."}

    # Define vars
    messages = [initial_message]
    blocks = ContentBlocks()

    # Run streaming loop
    with client.messages.stream(model=MODEL, max_tokens=MAX_TOKENS, messages=messages) as stream:
        for event in stream:
            if event.type == "content_block_start":
                blocks.init_block(event)

            elif event.type == "content_block_delta":
                print(f"{event.delta.text}", end="", flush=True)
                blocks.apply_delta(event)

            elif event.type == "content_block_stop":
                print("")

    # Get the stream final message
    final_message = stream.get_final_message()

    if not final_message.stop_reason == "end_turn":
        raise RuntimeError("""
        Stream ended before message_stop; discarding partial turn.
        Retry from the last complete turn.
        """)

    # Verify final message
    final_output = "".join([block.text for block in final_message.content])
    assembled_blocks = blocks.assemble()
    if not final_output == assembled_blocks:
        raise RuntimeError(f"""
        The final message does not match the block accumulated content.
        Final Message: {final_output}
        Assembled Blocks: {assembled_blocks}
        """)

    # Verify delta count
    if not blocks.verify_delta():
        raise RuntimeError("The delta count should be > 0 for all blocks.")

    # Print the final message
    print(final_output)


if __name__ == "__main__":
    main()
