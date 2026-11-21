"""Command line entry point: `python -m digital_thread_copilot` or `dtc`."""

import argparse
import sys

from digital_thread_copilot import __version__


def build_parser() -> argparse.ArgumentParser:
    """Return the parser of the command line."""
    parser = argparse.ArgumentParser(
        prog="dtc",
        description="Engineering copilot that queries and acts on a system's digital thread.",
    )
    parser.add_argument("--version", action="version", version=f"digital-thread-copilot {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command line and return the process exit code."""
    parser = build_parser()
    parser.parse_args(argv)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
