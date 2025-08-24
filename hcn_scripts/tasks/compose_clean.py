#!/usr/bin/env python
"""
Clean the compose project.
"""

from hcn_scripts.lib.command import run_simple_command
from hcn_scripts.lib.containers import get_compose_command


def main() -> None:
    """Clean the compose project."""

    # Check for podman or docker
    compose_command = get_compose_command()

    # Clean the compose project
    run_simple_command(*compose_command, "down", "--volumes", "--rmi", "all")


def init() -> None:
    """Initialize the project."""

    if __name__ == "__main__":
        main()


if __name__ == "__main__":
    init()
