# Development Environment

This project leverages `mise-en-place` to provide quick and repeatable setup of tools on your system, wether you're using Windows, macOS or a Linux Operating System (and x86/ARM).

## mise-en-place

Make sure you have `mise-en-place` installed and configured on your system shell. More information is available on the [mise-en-place](https://mise.jdx.dev/) website.

Once installed, run the following to install/setup all tools (make sure to restart your shell if you just installed).

```shell
mise install
```

> NOTE: there is a KNOWN issue with installing `hadolint` via mise. Please install manually for now.

## Project init

Once `mise-en-place` is ready and tools are installed, you can setup the python project and other necessary setup with the following commands.

```shell
mise exec -- poetry install
mise run `init`
```

## Pre-commit

If you wish to leverage pre-commit locally on each commit for code auditing and formatting, use the following:

```shell
mise exec -- poetry run pre-commit install
```

## Project tasks

You can run any project task using the `mise run` command! This includes any task you may want to run, including starting/stopping the development database!
