"""Shared helpers for reading Messages API response content blocks.

Usage:
    text = extract_text(response.content)
"""

from collections.abc import Iterable

from anthropic.types import ContentBlock


def extract_text(blocks: Iterable[ContentBlock]) -> str:
    """Join all `text` block contents in order, skipping non-text blocks."""
    return "".join(block.text for block in blocks if block.type == "text")
