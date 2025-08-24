#!/usr/bin/env python
"""
Entry point for the application.
"""

from healthcare_cost_navigator import main


def init() -> None:
    """
    Entry point for the application.
    """
    if __name__ == "__main__":
        # pylint: disable=no-value-for-parameter
        main()


if __name__ == "__main__":
    init()
