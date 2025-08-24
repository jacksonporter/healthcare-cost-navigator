#!/usr/bin/env python
"""
Execute the enter hook when the project is entered.
"""
from hcn_scripts.tasks.init import main as init_main


def main() -> None:
    """Execute the enter hook when the project is entered."""
    init_main()


def init() -> None:
    """Execute the enter hook when the project is entered."""

    if __name__ == "__main__":
        main()


if __name__ == "__main__":
    init()
