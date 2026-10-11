# Agent-Accessible CLI Gateway

A small Python command-line application that exposes mock user data and app operations through structured commands. It supports read-only inspection, user-status updates, and a simulated sync workflow. Output is JSON-formatted for easy parsing by scripts and AI agents.

> **Note:** This example uses an in-memory mock database. Changes are not saved after the process exits.

## Requirements

- Python 3.8 or newer

The application uses only Python’s standard library.

## Setup

Save the code to a file, such as `agent_cli.py`. No package installation is required.

## Usage

Run commands from the directory containing the file:

```bash
python agent\_cli.py [--json] <command> [options]
