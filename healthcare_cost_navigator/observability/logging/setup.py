"""
Setup logging for the application.
"""

import sys
from typing import Any

from loguru import logger


def setup_logging(
    level: str | None = None, app_name: str = "healthcare-cost-navigator"
) -> None:
    """Configure Loguru logging for the application.

    Args:
        level: Optional logging level. If not provided, defaults to INFO.
        app_name: Application name to include in log format.
            Defaults to "healthcare-cost-navigator".
    """
    # Remove default handler
    logger.remove()

    # Add console handler with JSON formatting
    logger.add(
        sys.stdout,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {app_name} "
            "| {name}:{function}:{line} | {message}"
        ),
        level=level.upper() if level else "INFO",
        serialize=True,  # This enables JSON output
        backtrace=True,
        diagnose=True,
        colorize=True,
        filter=lambda record: record.update(app_name=app_name),
    )


def get_logger(name: str | None = None) -> Any:
    """Get a logger instance.

    Args:
        name: Optional logger name. If not provided, returns the default logger.

    Returns:
        Loguru logger instance
    """
    if name:
        return logger.bind(name=name)
    return logger
