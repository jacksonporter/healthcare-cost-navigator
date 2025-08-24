#!/usr/bin/env python
"""
Start the database container in the background.
"""

from hcn_scripts.lib.command import run_simple_command
from hcn_scripts.lib.containers import get_compose_command


def main() -> None:
    """Start the database container in the background."""

    # Check for podman or docker
    compose_command = get_compose_command()

    # Start the database container in the background
    run_simple_command(*compose_command, "up", "-d", "database")


def init() -> None:
    """Initialize the project."""

    if __name__ == "__main__":
        main()


if __name__ == "__main__":
    init()
