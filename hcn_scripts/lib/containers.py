"""
Library for working with containers.
"""

import subprocess

from hcn_scripts.lib.command import check_for_command, run_simple_command


def get_supported_container_engine_command_path() -> str:
    """Get the path to the supported container engine command.

    Returns:
        str: The path to the supported container engine command.
    """

    try:
        command_path = check_for_command("podman")
    except ValueError:
        try:
            command_path = check_for_command("docker")
        except ValueError:
            # pylint: disable=raise-missing-from
            raise ValueError("No supported container engine found in PATH")

    return command_path


def get_compose_command() -> list[str]:
    """Get the compose command."""

    container_engine_command_path = get_supported_container_engine_command_path()
    command_list = [
        container_engine_command_path,
        "compose",
    ]

    try:
        _ = run_simple_command(*command_list, swallow_output=True)
    except subprocess.CalledProcessError as e:
        # Handle the case where the compose command fails
        # e.returncode contains the exit code
        # e.cmd contains the command that was run
        # pylint: disable=raise-missing-from
        raise ValueError(
            f"Compose command failed with exit code {e.returncode}: {e.cmd}"
        )

    return command_list
