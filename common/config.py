"""Shared environment/config loading for exercise scripts.

Usage:
    from common.config import MODEL, MAX_TOKENS
"""

import os

from dotenv import load_dotenv

load_dotenv()

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5")
MAX_TOKENS = int(os.environ.get("ANTHROPIC_MAX_TOKENS", "1024"))
