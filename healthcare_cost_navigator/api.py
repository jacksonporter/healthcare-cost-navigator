#!/usr/bin/env python
"""
Entry point for the application.
"""

import os
from contextlib import asynccontextmanager
import subprocess

import click
import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

from healthcare_cost_navigator.observability.logging.setup import (
    get_logger,
    setup_logging,
)


DEFAULT_LOGGER = None


def create_app(
    database_url: str = "postgresql+psycopg://hcn:hcn@localhost:54321/hcn",
) -> FastAPI:
    """Create and configure the FastAPI application."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Lifespan context manager for startup/shutdown events."""
        # Create database engine
        engine = create_engine(database_url)

        # Create database tables
        SQLModel.metadata.create_all(engine)

        # Store engine in app state for access in other functions
        app.state.engine = engine

        # Startup
        yield

        # Shutdown (if needed)
        engine.dispose()

    app = FastAPI(lifespan=lifespan)

    # Add routes to the app
    @app.get("/")
    async def root() -> dict[str, str]:
        """
        Root endpoint.
        """
        return {"message": "Hello, World!"}

    return app


def get_session(app: FastAPI):
    """Get database session from app state."""
    with Session(app.state.engine) as session:
        yield session


def prepare_app(log_level: str) -> None:
    """
    Prepare the application.
    """
    # pylint: disable=global-statement
    global DEFAULT_LOGGER

    setup_logging(log_level)
    DEFAULT_LOGGER = get_logger()


# pylint: disable=too-many-arguments
@click.command(name="api")
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default=os.getenv("LOG_LEVEL", "INFO"),
)
@click.option(
    "--host",
    type=str,
    default=os.getenv("HOST", "0.0.0.0"),
)
@click.option(
    "--port",
    type=int,
    default=int(os.getenv("PORT", "8000")),
)
@click.option(
    "--database-url",
    type=str,
    default=os.getenv(
        "DATABASE_URL", "postgresql+psycopg://hcn:hcn@localhost:54321/hcn"
    ),
)
@click.option(
    "--migrate",
    is_flag=True,
    default=True,
)
def main(
    log_level: str,
    host: str,
    port: int,
    database_url: str,
    migrate: bool,
) -> None:
    """
    Entry point for the application.
    """
    prepare_app(log_level)

    # Create the app with runtime configuration
    app = create_app(database_url)

    if migrate:
        subprocess.run(["alembic", "upgrade", "head"], check=True, shell=True)

    uvicorn.run(app, host=host, port=port)


def init() -> None:
    """
    Entry point for the application.
    """

    if __name__ == "__main__":
        # pylint: disable=no-value-for-parameter
        main()


if __name__ == "__main__":
    init()
