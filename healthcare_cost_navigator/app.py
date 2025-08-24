#!/usr/bin/env python
"""
Entry point for the application.
"""

import click

from healthcare_cost_navigator.api import main as api_main
from healthcare_cost_navigator.etl import main as etl_main


@click.group(name="cli")
def main() -> None:
    """
    Entry point for the application.
    """
    # pylint: disable=unnecessary-pass
    pass


main.add_command(api_main)
main.add_command(etl_main)


def init() -> None:
    """
    Entry point for the application.
    """

    if __name__ == "__main__":
        # pylint: disable=no-value-for-parameter
        main()


if __name__ == "__main__":
    init()
