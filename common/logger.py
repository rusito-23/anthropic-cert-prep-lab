"""Shared logging setup for exercise scripts.

Usage:
    parser = argparse.ArgumentParser()
    add_verbosity_argument(parser)
    args = parser.parse_args()
    configure_logging(args.verbose)
"""

import argparse
import logging

_LEVELS = [logging.WARNING, logging.INFO, logging.DEBUG]


def add_verbosity_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase logging verbosity (-v for info, -vv for debug)",
    )


def configure_logging(verbosity: int) -> None:
    level = _LEVELS[min(verbosity, len(_LEVELS) - 1)]
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
