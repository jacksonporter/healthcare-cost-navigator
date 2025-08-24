"""
Library for working with commands/executables on the system.
"""

from shutil import which
from subprocess import CompletedProcess, run


def check_for_command(command: str) -> str:
    """Check if a command exists in PATH using the shutil.which library."""
    command_path = which(command)
    if command_path is None:
        raise ValueError(f"Command {command} not found in PATH")
    return command_path


def run_simple_command(
    command: str, *args: str, shell: bool = True, swallow_output: bool = False
) -> CompletedProcess:
    """Run a command with arguments."""
    command_path = check_for_command(command)
    command_list = [command_path, *args]

    if shell:
        command_list = [" ".join(command_list)]

    if swallow_output:
        return run(
            command_list,
            check=True,
            shell=True,
            capture_output=True,
            text=True,
        )

    return run(
        command_list,
        check=True,
        shell=True,
        capture_output=False,
    )
