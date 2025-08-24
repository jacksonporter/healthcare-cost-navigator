#!/usr/bin/env python
"""
Initialize the project.
"""

from hcn_scripts.lib.command import run_simple_command
from hcn_scripts.lib.containers import (
    get_compose_command,
    get_supported_container_engine_command_path,
)


def main() -> None:
    """Initialize the project."""

    # Check for podman or docker
    _ = get_supported_container_engine_command_path()
    _ = get_compose_command()

    # Run poetry install
    run_simple_command("poetry", "install")


def init() -> None:
    """Initialize the project."""

    if __name__ == "__main__":
        main()


if __name__ == "__main__":
    init()
